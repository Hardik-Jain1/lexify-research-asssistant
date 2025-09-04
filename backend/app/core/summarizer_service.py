from flask import current_app
from app.utils.summarizer.llm_summarizer import (
    summarize_arxiv_papers as summarize_arxiv_papers_external,
    synthesize_insights_from_summaries as synthesize_insights_external
)
from app.services.litellm_service import completion as litellm_completion_wrapper

class SummarizerService:
    @staticmethod
    def generate_individual_summaries(arxiv_results: list[dict]) -> list[dict]:
        """Generates individual summaries for a list of arXiv results."""
        try:
            summaries = summarize_arxiv_papers_external(
                arxiv_results=arxiv_results,
                config=current_app.config,
                llm_completion_func=litellm_completion_wrapper,
            )
            return summaries
        except Exception as e:
            current_app.logger.error(f"Error generating individual summaries: {e}")
            raise

    @staticmethod
    def generate_consolidated_summary(paper_summaries: list[dict], query: str) -> dict:
        """Generates a consolidated summary from individual paper summaries."""
        try:
            synthesized_insight = synthesize_insights_external(
                paper_summaries=paper_summaries,
                query=query,
                config=current_app.config,
                llm_completion_func=litellm_completion_wrapper,
            )
            return synthesized_insight
        except Exception as e:
            current_app.logger.error(f"Error generating consolidated summary for query '{query}': {e}")
            raise