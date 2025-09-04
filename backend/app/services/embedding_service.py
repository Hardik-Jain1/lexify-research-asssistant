from flask import current_app
from app.services.litellm_service import embedding as litellm_embedding

def get_embedding(texts: list[str], model_type: str = "litellm", batch_size: int = 100):
    """Generates embeddings for a list of texts, processing in batches."""
    if not texts:
        return []

    import numpy as np

    if model_type == "litellm":
        model_name = current_app.config.get('EMBEDDING_MODEL_NAME_LITELLM', 'gemini/text-embedding-004')
        all_embeddings_list = []
        try:
            current_app.logger.info(f"Generating embeddings for {len(texts)} texts using LiteLLM model: {model_name} in batches of {batch_size}")
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                current_app.logger.debug(f"Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size} with {len(batch_texts)} texts.")
                response = litellm_embedding(model=model_name, input=batch_texts)
                batch_embeddings = [item['embedding'] for item in response.data]
                all_embeddings_list.extend(batch_embeddings)
            
            current_app.logger.info(f"Successfully generated {len(all_embeddings_list)} embeddings.")
            return np.array(all_embeddings_list)
        except Exception as e:
            current_app.logger.error(f"Error generating embeddings with LiteLLM: {e}")
            raise
    else:
        raise ValueError(f"Unsupported embedding model type: {model_type}")