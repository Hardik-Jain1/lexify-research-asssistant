from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct

def chunk_and_index_paper(
    paper_id: str,
    paper_title: str,
    paper_text: str,
    qdrant_client_instance,
    create_collection_func,
    embedding_func,
    chunk_size: int = 2000,
    chunk_overlap: int = 300
):
    collection_name = f"paper_{paper_id.replace('.', '_').replace(':', '_').replace('/', '_')}"

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(paper_text)

    if not chunks:
        print(f"Warning: No chunks generated for paper {paper_id}. Text might be too short or empty.")
        return None

    vectors = embedding_func(chunks)
    if vectors is None or len(vectors) == 0:
        print(f"Error: Failed to generate embeddings for paper {paper_id}.")
        return None
    
    vector_size = vectors.shape[1]

    if not create_collection_func(collection_name, vector_size):
         print(f"Error: Failed to create or ensure Qdrant collection: {collection_name}")
         return None

    points = [
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={
                "paper_id": paper_id,
                "paper_title": paper_title,
                "chunk_id": i,
                "text": chunk_text
            }
        )
        for i, (vector, chunk_text) in enumerate(zip(vectors, chunks))
    ]

    try:
        qdrant_client_instance.upsert(collection_name=collection_name, points=points)
        print(f"Successfully indexed {len(chunks)} chunks for paper {paper_id} into {collection_name}.")
    except Exception as e:
        print(f"Error: Failed to upsert points to Qdrant for {collection_name}: {e}")
        return None
        
    return collection_name