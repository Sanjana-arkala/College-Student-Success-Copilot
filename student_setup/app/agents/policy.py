""""Policy Agent: answers only from retrieved policy passages (AC-03)."""

from app.agents.llm import ask_llm
from app.rag.retriever import search_policy


SYSTEM = (
    "You answer questions about college policy using ONLY the provided passages. "
    "Cite the source file name. If the passages do not contain the answer, say the policy "
    "documents do not cover it. Never use outside knowledge."
)


async def answer_policy(session, query: str, trace: list) -> dict:
    # Policy documents are retrieved directly through the RAG layer.
    # Structured student/academic data continues to use MCP.
    passages = search_policy(query)

    trace.append("Policy Agent: searched college policy documents using RAG")

    if not passages:
        return {
            "answer": "No relevant policy found in the configured documents.",
            "sources": [],
        }

    context = "\n\n".join(
        f"[{p['source']}]\n{p['text']}"
        for p in passages
    )

    try:
        answer = ask_llm(
            SYSTEM,
            f"Passages:\n{context}\n\nQuestion: {query}",
        )
    except Exception:
        answer = "LLM unavailable. Retrieved passages:\n\n" + context

    return {
        "answer": answer,
        "sources": sorted({p["source"] for p in passages}),
    }