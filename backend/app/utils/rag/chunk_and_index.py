# rag/chunk_and_index.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct # VectorParams, Distance are used by create_collection_func

def chunk_and_index_paper(
    paper_id: str,
    paper_title: str,
    paper_text: str,
    qdrant_client_instance, # Pass the initialized Qdrant client
    create_collection_func, # Pass app.services.qdrant_client_setup.create_qdrant_collection
    embedding_func,         # Pass app.services.embedding_service.get_embedding
    chunk_size: int = 2000, # Consider making these configurable via app.config
    chunk_overlap: int = 300
):
    # Collection name might need to be more globally unique or versioned if re-indexing is possible
    # For ArXiv, paper_id usually includes version, e.g., "2303.08774v1"
    collection_name = f"paper_{paper_id.replace('.', '_').replace(':', '_').replace('/', '_')}" # Make it more filesystem/URL safe

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(paper_text)

    if not chunks:
        # current_app.logger.warning(f"No chunks generated for paper {paper_id}. Text might be too short or empty.")
        print(f"Warning: No chunks generated for paper {paper_id}. Text might be too short or empty.")
        return None # Or handle appropriately

    # Assuming embedding_func returns a NumPy array as per your original code
    vectors = embedding_func(chunks) # This now calls the service
    if vectors is None or len(vectors) == 0:
        # current_app.logger.error(f"Failed to generate embeddings for paper {paper_id}.")
        print(f"Error: Failed to generate embeddings for paper {paper_id}.")
        return None # Or raise an error
    
    vector_size = vectors.shape[1]

    # Create collection if it doesn't exist using the passed function
    # The create_collection_func should handle the logic of checking existence.
    # It should also take vector_size as an argument.
    if not create_collection_func(collection_name, vector_size):
         # current_app.logger.error(f"Failed to create or ensure Qdrant collection: {collection_name}")
         print(f"Error: Failed to create or ensure Qdrant collection: {collection_name}")
         return None # Or raise error

    points = [
        PointStruct(
            id=i, # Chunk index within the paper
            vector=vector.tolist(),
            payload={
                "paper_id": paper_id,       # Original ArXiv ID
                "paper_title": paper_title,
                "chunk_id": i,
                "text": chunk_text
            }
        )
        for i, (vector, chunk_text) in enumerate(zip(vectors, chunks))
    ]

    try:
        qdrant_client_instance.upsert(collection_name=collection_name, points=points)
        # current_app.logger.info(f"Successfully indexed {len(chunks)} chunks for paper {paper_id} into {collection_name}.")
        print(f"Successfully indexed {len(chunks)} chunks for paper {paper_id} into {collection_name}.")
    except Exception as e:
        # current_app.logger.error(f"Failed to upsert points to Qdrant for {collection_name}: {e}")
        print(f"Error: Failed to upsert points to Qdrant for {collection_name}: {e}")
        return None # Or raise error
        
    return collection_name