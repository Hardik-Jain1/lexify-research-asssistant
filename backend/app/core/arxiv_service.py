# app/core/arxiv_service.py
from flask import current_app
from app.utils.retriever.arxiv_client import search_arxiv as search_arxiv_external # Assuming this is accessible
# If retriever is a sub-module of app, e.g., app.retriever.arxiv_client:
# from app.retriever.arxiv_client import search_arxiv as search_arxiv_external

class ArxivService:
    @staticmethod
    def search_papers(query: str):
        max_results = current_app.config.get('MAX_ARXIV_RESULTS', 5)
        try:
            # search_arxiv_external returns (results, pdf_urls)
            # We are interested in the 'results' part which is List[Dict]
            results, _ = search_arxiv_external(query=query, max_results=max_results)
            # Ensure results have 'paper_id' which is 'result.get_short_id()' from your client
            # Your arxiv_client.py already creates 'paper_id'.
            return results
        except Exception as e:
            current_app.logger.error(f"Error searching arXiv for query '{query}': {e}")
            # Consider re-raising a custom service exception or returning an error indicator
            raise  # Or return None / empty list and handle in API layer