# Student Success Copilot

MCP + Agentic AI for a college portal. FastAPI, PostgreSQL, SQLAlchemy, MCP, Claude, ChromaDB, Streamlit.

## Quick start

```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # set ANTHROPIC_API_KEY (DATABASE_URL matches docker-compose by default)
docker compose up -d            # PostgreSQL (or use your own and update DATABASE_URL)

python scripts/generate_data.py # optional: regenerate synthetic CSVs
python -m app.db.seed           # CSVs -> PostgreSQL
python -m app.rag.ingest        # index data/policies into ChromaDB

uvicorn app.api.main:app --reload --port 8000    # backend (spawns the MCP server itself over stdio)
streamlit run ui/streamlit_app.py                # UI in another terminal
pytest                                           # tests
```

The MCP server (`python -m app.mcp_server.server`) is started automatically by the agents. Run it by hand only to test with an MCP inspector.

## Try these prompts
1. Analyze my CSE 6th semester class and identify students who may need support
2. What does our college policy say about attendance?
3. Prepare an intervention plan for student 2023CSE104
4. Draft a message to student 2023CSE104
5. Show details for 2023CSE999  (must return "Student not found")

## Layout
- `app/mcp_server/` MCP tools (student, attendance, marks, course, policy)
- `app/agents/` planner, analysis, policy, success, communication, orchestrator
- `app/rag/` policy ingestion + retrieval
- `app/approvals.py` human approval store; `app/audit/` audit log
- `data/policies/` SAMPLE policies. Replace with your college's real documents, then re-run ingest.

## Before real data
- Add authentication and RBAC (faculty see only their own classes). `role` in `/chat` is a placeholder.
- Move drafts from memory to a DB table.
- Get the college's sign-off before connecting real student records.
