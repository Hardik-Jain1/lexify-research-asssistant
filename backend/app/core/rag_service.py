# app/core/rag_service.py
from flask import current_app
from app.services.qdrant_client_setup import get_qdrant_client, create_qdrant_collection
from app.services.embedding_service import get_embedding as get_embedding_func # Renamed for clarity
from app.services.litellm_service import completion as litellm_completion_wrapper

# Assuming rag.chunk_and_index, rag.context_retriever, rag.format_context, rag.chat_with_papers are accessible
# and have been ADAPTED as discussed earlier.
from app.utils.rag.chunk_and_index import chunk_and_index_paper as chunk_and_index_external
from app.utils.rag.context_retriever import retrieve_context as retrieve_context_external
from app.utils.rag.format_context import format_llm_context # This one might not need changes if it's pure Python
from app.utils.rag.chat_with_papers import chat_with_papers as chat_with_papers_external

class RAGService:
    @staticmethod
    def index_paper_content(paper_id: str, paper_title: str, paper_text: str) -> str | None:
        """
        Chunks text and indexes it in Qdrant.
        Returns the Qdrant collection name if successful, else None.
        """
        qdrant_client = get_qdrant_client()
        try:
            # Pass the client, create_collection function, and embedding function
            collection_name = chunk_and_index_external(
                paper_id=paper_id,
                paper_title=paper_title,
                paper_text=paper_text,
                qdrant_client_instance=qdrant_client,
                create_collection_func=create_qdrant_collection, # From qdrant_client_setup
                embedding_func=get_embedding_func, # From embedding_service
                # chunk_size and chunk_overlap can be taken from current_app.config if needed
            )
            return collection_name
        except Exception as e:
            current_app.logger.error(f"Error in RAGService during indexing paper {paper_id}: {e}")
            raise # Or return None and handle in API layer

    @staticmethod
    def get_relevant_context(selected_papers_metadata: list[dict], query: str) -> tuple[str, dict]:
        """
        Retrieves context from selected papers for a query.
        selected_papers_metadata: List of dicts, each with 'arxiv_id', 'title', 'qdrant_collection_name'.
        Returns a tuple: (formatted_llm_context_string, raw_context_dict_with_sources).
        """
        qdrant_client = get_qdrant_client()
        try:
            # retrieve_context_external now expects paper_meta with 'qdrant_collection_name'
            raw_context_dict = retrieve_context_external(
                selected_papers_metadata=selected_papers_metadata,
                query=query,
                qdrant_client_instance=qdrant_client,
                embedding_func=get_embedding_func,
                # top_k can be from current_app.config
            )
            formatted_context = format_llm_context(raw_context_dict)
            return formatted_context, raw_context_dict # Return both for LLM and for sending sources to frontend
        except Exception as e:
            current_app.logger.error(f"Error in RAGService retrieving context for query '{query}': {e}")
            raise

    @staticmethod
    def get_chat_response(
            selected_papers_metadata: list[dict], # To fetch context
            query: str,
            chat_history: list = None # List of {'role': 'user'/'assistant', 'content': '...'}
        ) -> dict:
        """
        Handles the RAG chat logic.
        selected_papers_metadata: List of dicts from DB (PaperMetadata).
        """
        try:
            # 1. Retrieve context
            formatted_llm_context, raw_context_dict = RAGService.get_relevant_context(selected_papers_metadata, query)

            # 2. Call LLM for chat response
            # chat_with_papers_external now takes formatted_llm_context directly
            response_data = chat_with_papers_external(
                llm_context=formatted_llm_context,
                query=query,
                config=current_app.config, # Pass app config for prompts, model names
                llm_completion_func=litellm_completion_wrapper, # Pass LiteLLM wrapper
                chat_history=chat_history,
                # history_window, max_tokens, temperature, top_p can be from current_app.config
            )
            
            # Add sources (retrieved context chunks) to the response for the frontend
            response_data["sources"] = raw_context_dict
            return response_data # dict with 'response', 'token_usage', 'sources'
        except Exception as e:
            current_app.logger.error(f"Error in RAGService getting chat response for query '{query}': {e}")
            raise