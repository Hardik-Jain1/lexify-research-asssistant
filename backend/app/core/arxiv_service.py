from flask import current_app
from app.utils.retriever.arxiv_client import search_arxiv as search_arxiv_external

class ArxivService:
    @staticmethod
    def search_papers(query: str):
        max_results = current_app.config.get('MAX_ARXIV_RESULTS', 5)
        try:
            results, _ = search_arxiv_external(query=query, max_results=max_results)
            return results
        except Exception as e:
            current_app.logger.error(f"Error searching arXiv for query '{query}': {e}")
            raise