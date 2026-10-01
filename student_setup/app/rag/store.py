import chromadb
from chromadb.utils import embedding_functions

from app.config import settings

COLLECTION = "college_policies"


def get_collection():
    client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=settings.embedding_model)
    return client.get_or_create_collection(COLLECTION, embedding_function=ef)

