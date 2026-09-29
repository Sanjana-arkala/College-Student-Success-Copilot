from app.config import settings
from app.rag.store import get_collection


def search_policy(query: str) -> list[dict]:
    res = get_collection().query(query_texts=[query], n_results=settings.rag_top_k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return [{"text": d, "source": m.get("source")} for d, m in zip(docs, metas)]
