# app/services/qdrant_client_setup.py
from qdrant_client import QdrantClient
from flask import current_app

qdrant_client = None

def get_qdrant_client():
    global qdrant_client
    if qdrant_client is None:
        qdrant_url = current_app.config.get('QDRANT_URL')
        qdrant_api_key = current_app.config.get('QDRANT_API_KEY') # This might be None

        if not qdrant_url:
            raise ValueError("QDRANT_URL is not set in the application configuration.")

        try:
            current_app.logger.info(f"Initializing Qdrant client with URL: {qdrant_url}")
            if qdrant_api_key:
                qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
                current_app.logger.info("Qdrant client initialized with API key.")
            else:
                # For local Qdrant or instances without an API key
                qdrant_client = QdrantClient(url=qdrant_url)
                current_app.logger.info("Qdrant client initialized without API key (local/unsecured).")
            
            # Test connection (optional, but good for startup)
            # try:
            #     qdrant_client.meta_ops_api.health_check() # This is an old way, check new SDK
            #     # For newer versions, check if client can list collections or a similar light operation
            #     qdrant_client.get_collections() # Example operation
            #     current_app.logger.info("Qdrant client connection successful.")
            # except Exception as e:
            #     current_app.logger.error(f"Qdrant client connection test failed: {e}")
            #     # Depending on severity, you might want to raise an error or handle gracefully
                
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Qdrant client: {e}")
            raise  # Re-raise the exception to halt startup if Qdrant is critical
    return qdrant_client

# Your existing vector_store.py content would go here or be adapted.
# For example, create_collection might use get_qdrant_client()
from qdrant_client.models import VectorParams, Distance

def create_qdrant_collection(collection_name: str, vector_size: int, distance: Distance = Distance.COSINE):
    client = get_qdrant_client()
    try:
        # Check if collection already exists
        try:
            client.get_collection(collection_name=collection_name)
            current_app.logger.info(f"Collection '{collection_name}' already exists.")
            return True # Or handle as needed
        except Exception: # Specific exception for collection not found is better
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