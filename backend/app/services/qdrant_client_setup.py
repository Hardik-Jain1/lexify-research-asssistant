from qdrant_client import QdrantClient
from flask import current_app
from qdrant_client.models import VectorParams, Distance

qdrant_client = None

def get_qdrant_client():
    global qdrant_client
    if qdrant_client is None:
        qdrant_url = current_app.config.get('QDRANT_URL')
        qdrant_api_key = current_app.config.get('QDRANT_API_KEY')

        if not qdrant_url:
            raise ValueError("QDRANT_URL is not set in the application configuration.")

        try:
            current_app.logger.info(f"Initializing Qdrant client with URL: {qdrant_url}")
            if qdrant_api_key:
                qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
                current_app.logger.info("Qdrant client initialized with API key.")
            else:
                qdrant_client = QdrantClient(url=qdrant_url)
                current_app.logger.info("Qdrant client initialized without API key (local/unsecured).")
                
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Qdrant client: {e}")
            raise
    return qdrant_client

def create_qdrant_collection(collection_name: str, vector_size: int, distance: Distance = Distance.COSINE):
    client = get_qdrant_client()
    try:
        try:
            client.get_collection(collection_name=collection_name)
            current_app.logger.info(f"Collection '{collection_name}' already exists.")
            return True
        except Exception:
            current_app.logger.info(f"Collection '{collection_name}' does not exist. Creating...")

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance)
        )
        current_app.logger.info(f"Collection '{collection_name}' created successfully with vector size {vector_size}.")
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to create or check collection '{collection_name}': {e}")
        return False