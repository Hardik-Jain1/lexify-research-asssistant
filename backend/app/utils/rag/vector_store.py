from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from dotenv import load_dotenv
load_dotenv()
import os

# qdrant = QdrantClient(path="/qdrant_collections")
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def get_collections():
    return qdrant.get_collections()

def collection_exists(collection_name: str) -> bool:
    collections = get_collections().collections
    return any(c.name == collection_name for c in collections)

def create_collection(collection_name: str, vector_size: int):
    if collection_exists(collection_name):
        qdrant.delete_collection(collection_name=collection_name)
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

def delete_collection(collection_name: str):
    if collection_exists(collection_name):
        qdrant.delete_collection(collection_name=collection_name)