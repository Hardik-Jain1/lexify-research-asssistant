# rag/context_retriever.py
from typing import List, Dict
# No direct qdrant import needed here if client is passed
# No direct embedding import if func is passed

def retrieve_context(
    selected_papers_metadata: List[Dict], # Expects list of PaperMetadata like dicts with 'arxiv_id' and 'title', 'qdrant_collection_name'
    query: str,
    qdrant_client_instance, # Pass the initialized Qdrant client
    embedding_func,         # Pass app.services.embedding_service.get_embedding
    top_k: int = 5
) -> Dict:
    context_dict = {}
    query_vector = embedding_func([query])[0] # Get embedding for the query

    for paper_meta in selected_papers_metadata:
        paper_id = paper_meta["arxiv_id"] # Use the DB arxiv_id
        paper_title = paper_meta["title"]
        # collection_name = f"paper_{paper_id.replace('.', '_').replace(':', '_').replace('/', '_')}"
        collection_name = paper_meta.get("qdrant_collection_name")

        if not collection_name:
            print(f"Warning: Qdrant collection name not found for paper {paper_id}. Skipping context retrieval for this paper.")
            # current_app.logger.warning(f"Qdrant collection name not found for paper {paper_id}. Skipping.")
            continue
        
        try:
            # Qdrant's search method was renamed to query_points previously, now it's search
            search_result = qdrant_client_instance.search(
                collection_name=collection_name,
                query_vector=query_vector.tolist(), # Ensure it's a list
                limit=top_k,
                with_payload=True # To get the text and other metadata
            )
            # search_result is a list of ScoredPoint objects
            # combined_text = "\n".join([hit.payload["text"] for hit in search_result]) # search_result is already a list of points
            
            # Filter out low-scoring results if necessary, though `limit` handles top_k
            # Some vector DBs might return results even with very low scores.
            # Add a score threshold if needed:
            # relevant_hits = [hit for hit in search_result if hit.score > YOUR_SCORE_THRESHOLD]

            combined_text = "\n\n---\n\n".join([hit.payload["text"] for hit in search_result if hit.payload and "text" in hit.payload])

            context_dict[paper_id] = {
                "title": paper_title,
                "text": combined_text,
                "_chunks": [
                    {
                        "chunk_id": hit.payload.get("chunk_id", hit.id), # Use payload chunk_id if available, else point id
                        "score": hit.score,
                        "text": hit.payload["text"]
                    }
                    for hit in search_result if hit.payload and "text" in hit.payload
                ]
            }
        except Exception as e:
            # current_app.logger.error(f"Error retrieving context from Qdrant for {collection_name} with query '{query}': {e}")
            print(f"Error retrieving context from Qdrant for {collection_name}: {e}")
            context_dict[paper_id] = { # Provide empty context on error for this paper
                "title": paper_title,
                "text": "Error retrieving context for this paper.",
                "_chunks": []
            }
    return context_dict