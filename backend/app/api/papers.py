from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.paper import PaperMetadata
from app.core.arxiv_service import ArxivService
from app.core.summarizer_service import SummarizerService
from app.core.download_service import DownloadService
from app.core.processing_service import ProcessingService
from app.core.rag_service import RAGService
import datetime
from pathlib import Path
import threading

papers_bp = Blueprint('papers_bp', __name__)

def process_paper_background(app_context, paper_metadata_id):
    """Helper function to run paper processing in a background thread."""
    with app_context:
        current_app.logger.info(f"Background processing started for paper ID: {paper_metadata_id}")
        paper = db.session.get(PaperMetadata, paper_metadata_id)
        if not paper:
            current_app.logger.error(f"PaperMetadata with id {paper_metadata_id} not found in background task.")
            return

        try:
            # Download PDF if not already downloaded
            if not paper.local_pdf_path or not Path(paper.local_pdf_path).exists():
                pdf_info = [{"pdf_url": paper.pdf_url, "paper_id": paper.arxiv_id}]
                downloaded_paths = DownloadService.download_paper_pdfs(pdf_info)
                if downloaded_paths:
                    paper.local_pdf_path = downloaded_paths[0]
                    paper.downloaded_at = datetime.datetime.now(datetime.timezone.utc)
                    db.session.commit()
                    current_app.logger.info(f"PDF downloaded for {paper.arxiv_id} to {paper.local_pdf_path}")
                else:
                    current_app.logger.error(f"Failed to download PDF for {paper.arxiv_id}")
                    paper.source = f"{paper.source} (Download Failed)"
                    db.session.commit()
                    return

            # Extract text from PDF
            raw_text = ProcessingService.extract_text(paper.local_pdf_path)
            if raw_text:
                paper.text_extracted_at = datetime.datetime.now(datetime.timezone.utc)
                db.session.commit()
                current_app.logger.info(f"Text extracted for {paper.arxiv_id}")
            else:
                current_app.logger.error(f"Failed to extract text for {paper.arxiv_id}")
                paper.source = f"{paper.source} (Extraction Failed)"
                db.session.commit()
                return

            # Clean extracted text
            cleaned_text = ProcessingService.clean_text(raw_text)
            paper.cleaned_text_at = datetime.datetime.now(datetime.timezone.utc)
            db.session.commit()
            current_app.logger.info(f"Text cleaned for {paper.arxiv_id}")

            # Chunk and index in vector database
            collection_name = RAGService.index_paper_content(
                paper_id=paper.arxiv_id,
                paper_title=paper.title,
                paper_text=cleaned_text
            )
            if collection_name:
                paper.qdrant_collection_name = collection_name
                paper.indexed_at = datetime.datetime.now(datetime.timezone.utc)
                db.session.commit()
                current_app.logger.info(f"Paper {paper.arxiv_id} indexed into Qdrant collection: {collection_name}")
            else:
                current_app.logger.error(f"Failed to index paper {paper.arxiv_id}")
                paper.source = f"{paper.source} (Indexing Failed)"
                db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Error processing paper {paper.arxiv_id} in background: {e}")
            paper.source = f"{paper.source} (Processing Error: {str(e)[:50]})"
            db.session.commit()


@papers_bp.route('/search', methods=['POST'])
@jwt_required()
def search_and_summarize_papers():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"msg": "Query is required"}), 400

    try:
        # Search ArXiv
        arxiv_results = ArxivService.search_papers(query)
        if not arxiv_results:
            return jsonify({"msg": "No papers found for your query."}), 404

        # Store/Update paper metadata in DB and prepare for summary
        papers_for_summary = []
        paper_objects_for_processing = []
        for res in arxiv_results:
            paper = PaperMetadata.query.filter_by(arxiv_id=res['paper_id']).first()
            if not paper:
                paper = PaperMetadata(
                    arxiv_id=res['paper_id'],
                    title=res['title'],
                    authors=res['authors'],
                    abstract=res.get('abstract'),
                    published_date=res['published'],
                    pdf_url=res['pdf_url'],
                    entry_id=res['entry_id'],
                    source=res.get('source', 'arXiv')
                )
                db.session.add(paper)
            else:
                paper.title = res['title']
                paper.authors = res['authors']
                paper.abstract = res.get('abstract')
                paper.published_date = res['published']
                paper.pdf_url = res['pdf_url']
                paper.entry_id = res['entry_id']
                paper.updated_at = datetime.datetime.now(datetime.timezone.utc)
            db.session.flush()

            papers_for_summary.append({
                "paper_id": paper.arxiv_id,
                "title": paper.title,
                "abstract": paper.abstract,
                "pdf_url": paper.pdf_url,
                "db_id": paper.id
            })
            paper_objects_for_processing.append(paper)
        
        db.session.commit()

        # Generate individual summaries from abstracts
        individual_summaries = SummarizerService.generate_individual_summaries(papers_for_summary)

        # Generate consolidated summary
        consolidated_summary_data = SummarizerService.generate_consolidated_summary(individual_summaries, query)

        # Asynchronously process papers (download, extract, clean, index)
        app_ctx = current_app.app_context()
        for p_obj in paper_objects_for_processing:
            if not p_obj.indexed_at and "Failed" not in (p_obj.source or "") and "Error" not in (p_obj.source or ""):
                 thread = threading.Thread(target=process_paper_background, args=(app_ctx, p_obj.id))
                 thread.start()
            elif p_obj.indexed_at:
                current_app.logger.info(f"Paper {p_obj.arxiv_id} already indexed. Skipping background processing.")
            else:
                current_app.logger.info(f"Paper {p_obj.arxiv_id} previously failed processing or download. Skipping background processing.")

        # Combine results for frontend
        output_papers = []
        for res in arxiv_results:
            paper_id = res['paper_id']
            ind_summary_obj = next((s for s in individual_summaries if s['paper_id'] == paper_id), None)
            db_paper = next((p for p in paper_objects_for_processing if p.arxiv_id == paper_id), None)

            output_papers.append({
                "db_id": db_paper.id if db_paper else None,
                "paper_id": paper_id,
                "title": res['title'],
                "authors": res['authors'],
                "published": str(res['published']),
                "pdf_url": res['pdf_url'],
                "abstract": res.get('abstract'),
                "individual_summary": ind_summary_obj['summary'] if ind_summary_obj else "Summary not available.",
                "source": res.get('source', 'arXiv'),
                "is_processed_for_chat": bool(db_paper.indexed_at) if db_paper else False,
                "qdrant_collection_name": db_paper.qdrant_collection_name if db_paper and db_paper.indexed_at else None
            })
            
        return jsonify({
            "consolidated_summary": consolidated_summary_data['content'],
            "token_usage_consolidated": {
                "input": consolidated_summary_data.get('input_tokens'),
                "output": consolidated_summary_data.get('output_tokens')
            },
            "papers": output_papers
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error in search_and_summarize_papers: {e}", exc_info=True)
        return jsonify({"msg": "An internal error occurred.", "error": str(e)}), 500


@papers_bp.route('/<int:paper_db_id>/status', methods=['GET'])
@jwt_required()
def get_paper_processing_status(paper_db_id):
    """Endpoint for frontend to poll processing status."""
    paper = db.session.get(PaperMetadata, paper_db_id)
    if not paper:
        return jsonify({"msg": "Paper not found"}), 404
    
    return jsonify({
        "paper_id": paper.arxiv_id,
        "db_id": paper.id,
        "title": paper.title,
        "downloaded_at": paper.downloaded_at.isoformat() if paper.downloaded_at else None,
        "text_extracted_at": paper.text_extracted_at.isoformat() if paper.text_extracted_at else None,
        "cleaned_text_at": paper.cleaned_text_at.isoformat() if paper.cleaned_text_at else None,
        "indexed_at": paper.indexed_at.isoformat() if paper.indexed_at else None,
        "qdrant_collection_name": paper.qdrant_collection_name,
        "is_ready_for_chat": bool(paper.indexed_at),
        "processing_status_notes": paper.source
    }), 200


@papers_bp.route('/<int:paper_db_id>/process-manual', methods=['POST'])
@jwt_required()
def manual_process_paper(paper_db_id):
    paper = db.session.get(PaperMetadata, paper_db_id)
    if not paper:
        return jsonify({"msg": "Paper not found"}), 404

    if paper.indexed_at:
        return jsonify({"msg": "Paper already processed and indexed."}), 200
    
    if "Failed" in (paper.source or "") or "Error" in (paper.source or ""):
        current_app.logger.info(f"Retrying processing for paper {paper.arxiv_id} (DB ID: {paper.id}) which previously failed.")
    
    app_ctx = current_app.app_context()
    thread = threading.Thread(target=process_paper_background, args=(app_ctx, paper.id))
    thread.start()
    
    return jsonify({"msg": f"Processing re-initiated for paper {paper.arxiv_id}. Check status endpoint."}), 202
