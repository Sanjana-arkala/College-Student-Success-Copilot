"""Human-in-the-loop store. Nothing is 'sent' without explicit approval (FR-14, AC-06).
In-memory for the MVP; move to a DB table for production."""
import uuid

from app.audit.logger import audit

_DRAFTS: dict[str, dict] = {}


def create_draft(kind: str, student_id: str, content: str) -> dict:
    draft = {"id": uuid.uuid4().hex[:8], "kind": kind, "student_id": student_id,
             "content": content, "status": "pending"}
    _DRAFTS[draft["id"]] = draft
    audit("draft_created", draft_id=draft["id"], kind=kind, student_id=student_id)
    return draft


def list_drafts() -> list[dict]:
    return list(_DRAFTS.values())


def decide(draft_id: str, approve: bool, reviewer: str = "faculty") -> dict | None:
    d = _DRAFTS.get(draft_id)
    if not d or d["status"] != "pending":
        return d
    d["status"] = "approved" if approve else "cancelled"
    audit("draft_" + d["status"], draft_id=draft_id, reviewer=reviewer)
    # Hook for real delivery (email/portal notification) goes here, only when approved.
    return d
