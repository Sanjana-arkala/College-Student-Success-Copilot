import json
import subprocess
import sys
from pathlib import Path

from app.mcp_server.instance import mcp


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@mcp.tool()
def search_college_policy(query: str) -> dict:
    """Search the college policy documents through the RAG worker."""

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "app.rag.policy_search_worker",
                query,
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )

        passages = json.loads(result.stdout)

        return {
            "query": query,
            "passages": passages,
        }

    except subprocess.TimeoutExpired:
        return {
            "query": query,
            "passages": [],
            "error": "Policy search timed out.",
        }

    except subprocess.CalledProcessError as e:
        return {
            "query": query,
            "passages": [],
            "error": f"Policy search failed: {e.stderr.strip()}",
        }

    except json.JSONDecodeError:
        return {
            "query": query,
            "passages": [],
            "error": "Policy worker returned invalid JSON.",
        }