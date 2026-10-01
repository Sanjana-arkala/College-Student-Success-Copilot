from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import approvals
from app.agents import orchestrator

app = FastAPI(title="Student Success Copilot")


class ChatRequest(BaseModel):
    message: str
    role: str = "faculty"  # TODO: derive from portal auth (RBAC, FR-17)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    return await orchestrator.handle(req.message, req.role)


@app.get("/drafts")
def drafts():
    return approvals.list_drafts()


@app.post("/drafts/{draft_id}/approve")
def approve(draft_id: str):
    d = approvals.decide(draft_id, True)
    if not d:
        raise HTTPException(404, "Draft not found")
    return d


@app.post("/drafts/{draft_id}/cancel")
def cancel(draft_id: str):
    d = approvals.decide(draft_id, False)
    if not d:
        raise HTTPException(404, "Draft not found")
    return d

