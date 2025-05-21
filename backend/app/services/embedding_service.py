# app/services/embedding_service.py
from flask import current_app
# Option 1: Using LiteLLM for embeddings
from app.services.litellm_service import embedding as litellm_embedding

# Option 2: Using a library like sentence-transformers (example)
# from sentence_transformers import SentenceTransformer
# SBERT_MODEL = None

# def get_sbert_model():
#     global SBERT_MODEL
#     if SBERT_MODEL is None:
#         model_name = current_app.config.get('EMBEDDING_MODEL_NAME', 'all-MiniLM-L6-v2')
#         current_app.logger.info(f"Loading SentenceTransformer model: {model_name}")
#         SBERT_MODEL = SentenceTransformer(model_name)
#         current_app.logger.info("SentenceTransformer model loaded.")
#     return SBERT_MODEL

def get_embedding(texts: list[str], model_type: str = "litellm", batch_size: int = 100): # or "sbert"
    """
    Generates embeddings for a list of texts, processing in batches.
    `model_type` can be used to switch between embedding providers if you have multiple.
    `batch_size` controls how many texts are processed at once for "litellm".
    """
    if not texts:
        return []

    import numpy as np

    if model_type == "litellm":
        model_name = current_app.config.get('EMBEDDING_MODEL_NAME_LITELLM', 'gemini/text-embedding-004') # Example, configure as needed
        all_embeddings_list = []
        try:
            current_app.logger.info(f"Generating embeddings for {len(texts)} texts using LiteLLM model: {model_name} in batches of {batch_size}")
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                current_app.logger.debug(f"Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size} with {len(batch_texts)} texts.")
                response = litellm_embedding(model=model_name, input=batch_texts)
                # LiteLLM embedding response is a ModelResponse object.
                # The embeddings are in response.data, which is a list of EmbeddingObject.
                # Each EmbeddingObject has an 'embedding' attribute (list of floats).
                batch_embeddings = [item['embedding'] for item in response.data]
                all_embeddings_list.extend(batch_embeddings)
            
            current_app.logger.info(f"Successfully generated {len(all_embeddings_list)} embeddings.")
            return np.array(all_embeddings_list)
        except Exception as e:
            current_app.logger.error(f"Error generating embeddings with LiteLLM: {e}")
            raise
    # elif model_type == "sbert":
    #     model = get_sbert_model()
    #     current_app.logger.info(f"Generating embeddings for {len(texts)} texts using SentenceTransformer.")
    #     # SentenceTransformer's encode method handles batching internally if needed,
    #     # or can process the whole list if memory allows.
    #     # For very large lists, manual batching might still be beneficial depending on the model and system.
    #     embeddings = model.encode(texts, batch_size=batch_size) # SBERT's encode can take batch_size
    #     return embeddings # Already a numpy array
    else:
        raise ValueError(f"Unsupported embedding model type: {model_type}")

# Your rag/embedding.py should be adapted to use this service function.
# For example, in rag/chunk_and_index.py, replace direct embedding calls:
# from app.services.embedding_service import get_embedding
# vectors = get_embedding(chunks) # This now returns a NumPy array