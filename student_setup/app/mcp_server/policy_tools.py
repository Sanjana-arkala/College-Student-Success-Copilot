from app.mcp_server.instance import mcp
from app.rag.retriever import search_policy


@mcp.tool()
def search_college_policy(query: str) -> dict:
    """Search the college's policy documents. Answers must be grounded in the returned passages."""
    return {"query": query, "passages": search_policy(query)}
