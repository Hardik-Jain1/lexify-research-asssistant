from typing import List, Dict

def retrieve_context(
    selected_papers_metadata: List[Dict],
    query: str,
    qdrant_client_instance,
    embedding_func,
    top_k: int = 5
) -> Dict:
    context_dict = {}
    query_vector = embedding_func([query])[0]

    for paper_meta in selected_papers_metadata:
        paper_id = paper_meta["arxiv_id"]
        paper_title = paper_meta["title"]
        collection_name = paper_meta.get("qdrant_collection_name")

        if not collection_name:
            print(f"Warning: Qdrant collection name not found for paper {paper_id}. Skipping context retrieval for this paper.")
            continue
        
        try:
            search_result = qdrant_client_instance.search(
                collection_name=collection_name,
                query_vector=query_vector.tolist(),
                limit=top_k,
                with_payload=True
            )

            combined_text = "\n\n---\n\n".join([hit.payload["text"] for hit in search_result if hit.payload and "text" in hit.payload])

            context_dict[paper_id] = {
                "title": paper_title,
                "text": combined_text,
                "_chunks": [
                    {
                        "chunk_id": hit.payload.get("chunk_id", hit.id),
                        "score": hit.score,
                        "text": hit.payload["text"]
                    }
                    for hit in search_result if hit.payload and "text" in hit.payload
                ]
            }
        except Exception as e:
            print(f"Error retrieving context from Qdrant for {collection_name}: {e}")
            context_dict[paper_id] = {
                "title": paper_title,
                "text": "Error retrieving context for this paper.",
                "_chunks": []
            }
    return context_dict