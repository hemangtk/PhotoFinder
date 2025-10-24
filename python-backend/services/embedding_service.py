from sentence_transformers import SentenceTransformer
from typing import List, Union

model = None

def load_embedding_model():
    global model
    if model is None:
        print("Loading sentence-transformers model...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("Embedding model loaded successfully!")

def generate_embedding(text: str) -> List[float]:
    load_embedding_model()

    embedding = model.encode(text, convert_to_numpy=True)

    return embedding.tolist()

def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    load_embedding_model()

    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    return embeddings.tolist()
