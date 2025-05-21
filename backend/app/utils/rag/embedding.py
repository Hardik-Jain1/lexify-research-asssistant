import litellm
import numpy as np

def get_embedding(data, model="gemini/text-embedding-004", batch_size=100):
    all_embeddings = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        embeddings = litellm.embedding(model=model, input=batch)
        all_embeddings.extend([obj["embedding"] for obj in embeddings.data])
    return np.array(all_embeddings)