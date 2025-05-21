# app/api/papers.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.paper import PaperMetadata
from app.core.arxiv_service import ArxivService
from app.core.summarizer_service import SummarizerService
from app.core.download_service import DownloadService
from app.core.processing_service import ProcessingService
from app.core.rag_service import RAGService # For indexing
import datetime
from pathlib import Path # For Path object
from joblib import Parallel, delayed # For parallel processing

papers_bp = Blueprint('papers_bp', __name__)

def process_paper_background(paper_metadata_id):
    """Helper function to run paper processing in a background job."""
    with current_app.app_context(): # Use current_app context within the job
        current_app.logger.info(f"Background processing started for paper ID: {paper_metadata_id}")
        paper = db.session.get(PaperMetadata, paper_metadata_id) # Use db.session.get for simplicity
        if not paper:
            current_app.logger.error(f"PaperMetadata with id {paper_metadata_id} not found in background task.")
            return

        try:
            # 1. Download (if not already) - DownloadService now returns path
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
                    paper.source = f"{paper.source} (Download Failed)" # Update status
                    db.session.commit()
                    return # Stop if download fails

            # 2. Extract Text
            raw_text = ProcessingService.extract_text(paper.local_pdf_path)
            if raw_text:
                paper.text_extracted_at = datetime.datetime.now(datetime.timezone.utc)
                db.session.commit()
                current_app.logger.info(f"Text extracted for {paper.arxiv_id}")
            else:
                current_app.logger.error(f"Failed to extract text for {paper.arxiv_id}")
                paper.source = f"{paper.source} (Extraction Failed)"
                db.session.commit()
                return # Stop if extraction fails

            # 3. Clean Text
            cleaned_text = ProcessingService.clean_text(raw_text)
            paper.cleaned_text_at = datetime.datetime.now(datetime.timezone.utc)
            # Not storing full cleaned_text in DB to avoid large data, it's used for indexing
            db.session.commit()
            current_app.logger.info(f"Text cleaned for {paper.arxiv_id}")

            # 4. Chunk and Index
            collection_name = RAGService.index_paper_content(
                paper_id=paper.arxiv_id, # This is the ArXiv ID like "2303.08774v1"
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
            paper.source = f"{paper.source} (Processing Error: {str(e)[:50]})" # Store a snippet of the error
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
        # 1. Search ArXiv
        arxiv_results = ArxivService.search_papers(query) # List of dicts
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
                    authors=res['authors'], # Assuming this is JSON compatible (list of strings)
                    abstract=res.get('abstract'), # res['abstract']
                    published_date=res['published'], # Ensure this is a date object or parsable string
                    pdf_url=res['pdf_url'],
                    entry_id=res['entry_id'],
                    source=res.get('source', 'arXiv')
                )
                db.session.add(paper)
            else: # Update if exists, e.g. abstract or pdf_url might change (though unlikely for arxiv_id)
                paper.title = res['title']
                paper.authors = res['authors']
                paper.abstract = res.get('abstract')
                paper.published_date = res['published']
                paper.pdf_url = res['pdf_url']
                paper.entry_id = res['entry_id']
                paper.updated_at = datetime.datetime.now(datetime.timezone.utc)
            db.session.flush() # Assigns ID to 'paper' if new, before commit

            papers_for_summary.append({
                "paper_id": paper.arxiv_id,
                "title": paper.title,
                "abstract": paper.abstract,
                "pdf_url": paper.pdf_url, # For frontend to show link
                "db_id": paper.id # Internal DB ID
            })
            paper_objects_for_processing.append(paper)
        
        db.session.commit() # Commit all new/updated papers

        # 2. Generate Individual Summaries (based on abstracts)
        # These are quick summaries from abstracts, not full text
        individual_summaries = SummarizerService.generate_individual_summaries(papers_for_summary)

        # 3. Generate Consolidated Summary (from individual summaries)
        consolidated_summary_data = SummarizerService.generate_consolidated_summary(individual_summaries, query)

        # 4. Asynchronously download, extract text, clean, and index papers
        # Create a list of tasks for joblib
        tasks = []
        for p_obj in paper_objects_for_processing:
            # Only process if not already indexed or failed previously
            if not p_obj.indexed_at and "Failed" not in (p_obj.source or "") and "Error" not in (p_obj.source or ""):
                 tasks.append(delayed(process_paper_background)(p_obj.id))
            elif p_obj.indexed_at:
                current_app.logger.info(f"Paper {p_obj.arxiv_id} already indexed. Skipping background processing.")
            else:
                current_app.logger.info(f"Paper {p_obj.arxiv_id} previously failed processing or download. Skipping background processing.")
        
        if tasks:
            # Run tasks in parallel using all available CPUs
            # Consider adjusting n_jobs based on your environment and task nature
            Parallel(n_jobs=-1)(tasks)


        # Combine results for the frontend
        # Frontend needs: consolidated summary, and table of individual papers with their summaries
        # Each item in individual_summaries already has paper_id, title, abstract, summary.
        # We should merge this with other metadata from arxiv_results.
        
        output_papers = []
        for res in arxiv_results: # Original search results
            paper_id = res['paper_id']
            ind_summary_obj = next((s for s in individual_summaries if s['paper_id'] == paper_id), None)
            db_paper = next((p for p in paper_objects_for_processing if p.arxiv_id == paper_id), None)

            output_papers.append({
                "db_id": db_paper.id if db_paper else None,
                "paper_id": paper_id,
                "title": res['title'],
                "authors": res['authors'],
                "published": str(res['published']), # Ensure string for JSON
                "pdf_url": res['pdf_url'],
                "abstract": res.get('abstract'),
                "individual_summary": ind_summary_obj['summary'] if ind_summary_obj else "Summary not available.",
                "source": res.get('source', 'arXiv'),
                "is_processed_for_chat": bool(db_paper.indexed_at) if db_paper else False, # Indicate if ready for chat
                "qdrant_collection_name": db_paper.qdrant_collection_name if db_paper and db_paper.indexed_at else None
            })
            
        return jsonify({
            "consolidated_summary": consolidated_summary_data['content'], # This is the text
            "token_usage_consolidated": {
                "input": consolidated_summary_data.get('input_tokens'),
                "output": consolidated_summary_data.get('output_tokens')
            },
            "papers": output_papers # List of papers with their individual summaries & metadata
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
        "processing_status_notes": paper.source # If any errors were appended here
    }), 200






# Optional: Manual trigger for processing a paper if needed for retry
@papers_bp.route('/<int:paper_db_id>/process-manual', methods=['POST'])
@jwt_required()
def manual_process_paper(paper_db_id):
    paper = db.session.get(PaperMetadata, paper_db_id)
    if not paper:
        return jsonify({"msg": "Paper not found"}), 404

    if paper.indexed_at:
        return jsonify({"msg": "Paper already processed and indexed."}), 200
    
    if "Failed" in (paper.source or "") or "Error" in (paper.source or ""):
        # Optionally reset status before retrying
        # paper.source = "arXiv (Retrying)" # Or original source
        # paper.downloaded_at = None
        # ... reset other statuses
        # db.session.commit()
        current_app.logger.info(f"Retrying processing for paper {paper.arxiv_id} (DB ID: {paper.id}) which previously failed.")
    
    # Run the processing task using joblib. n_jobs=1 as it's a single task.
    Parallel(n_jobs=1)(delayed(process_paper_background)(paper.id))
    
    return jsonify({"msg": f"Processing re-initiated for paper {paper.arxiv_id}. Check status endpoint."}), 202