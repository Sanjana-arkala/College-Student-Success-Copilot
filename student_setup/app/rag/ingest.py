"""Chunk and index policy docs. Run: python -m app.rag.ingest"""
from pathlib import Path

from pypdf import PdfReader

from app.config import settings
from app.rag.store import get_collection


def read_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8")


def chunk(text: str, size: int, overlap: int) -> list[str]:
    out, start = [], 0
    while start < len(text):
        out.append(text[start:start + size])
        start += size - overlap
    return [c.strip() for c in out if c.strip()]


def main() -> None:
    col = get_collection()
    ids, docs, metas = [], [], []
    for path in sorted(Path(settings.policy_docs_dir).glob("*")):
        if path.suffix.lower() not in {".txt", ".md", ".pdf"}:
            continue
        for i, c in enumerate(chunk(read_file(path), settings.rag_chunk_size, settings.rag_chunk_overlap)):
            ids.append(f"{path.name}-{i}")
            docs.append(c)
            metas.append({"source": path.name, "chunk": i})
    if ids:
        col.upsert(ids=ids, documents=docs, metadatas=metas)
    print(f"Indexed {len(ids)} chunks from {settings.policy_docs_dir}")


if __name__ == "__main__":
    main()

