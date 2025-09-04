from flask import current_app
from app.services.qdrant_client_setup import get_qdrant_client, create_qdrant_collection
from app.services.embedding_service import get_embedding as get_embedding_func
from app.services.litellm_service import completion as litellm_completion_wrapper
from app.utils.rag.chunk_and_index import chunk_and_index_paper as chunk_and_index_external
from app.utils.rag.context_retriever import retrieve_context as retrieve_context_external
from app.utils.rag.format_context import format_llm_context
from app.utils.rag.chat_with_papers import chat_with_papers as chat_with_papers_external

class RAGService:
    @staticmethod
    def index_paper_content(paper_id: str, paper_title: str, paper_text: str) -> str | None:
        """Chunks text and indexes it in Qdrant. Returns collection name if successful."""
        qdrant_client = get_qdrant_client()
        try:
            collection_name = chunk_and_index_external(
                paper_id=paper_id,
                paper_title=paper_title,
                paper_text=paper_text,
                qdrant_client_instance=qdrant_client,
                create_collection_func=create_qdrant_collection,
                embedding_func=get_embedding_func,
            )
            return collection_name
        except Exception as e:
            current_app.logger.error(f"Error in RAGService during indexing paper {paper_id}: {e}")
            raise

    @staticmethod
    def get_relevant_context(selected_papers_metadata: list[dict], query: str) -> tuple[str, dict]:
        """Retrieves context from selected papers for a query."""
        qdrant_client = get_qdrant_client()
        try:
            raw_context_dict = retrieve_context_external(
                selected_papers_metadata=selected_papers_metadata,
                query=query,
                qdrant_client_instance=qdrant_client,
                embedding_func=get_embedding_func,
            )
            formatted_context = format_llm_context(raw_context_dict)
            return formatted_context, raw_context_dict
        except Exception as e:
            current_app.logger.error(f"Error in RAGService retrieving context for query '{query}': {e}")
            raise

    @staticmethod
    def get_chat_response(
            selected_papers_metadata: list[dict],
            query: str,
            chat_history: list = None
        ) -> dict:
        """Handles the RAG chat logic."""
        try:
            # Retrieve context
            formatted_llm_context, raw_context_dict = RAGService.get_relevant_context(selected_papers_metadata, query)

            # Call LLM for chat response
            response_data = chat_with_papers_external(
                llm_context=formatted_llm_context,
                query=query,
                config=current_app.config,
                llm_completion_func=litellm_completion_wrapper,
                chat_history=chat_history,
            )
            
            # Add sources to response for frontend
            response_data["sources"] = raw_context_dict
            return response_data
        except Exception as e:
            current_app.logger.error(f"Error in RAGService getting chat response for query '{query}': {e}")
            raise