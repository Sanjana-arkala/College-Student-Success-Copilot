import json
import os
from datetime import datetime, timezone

from app.config import settings


def audit(event: str, **details) -> None:
    """Append one JSON line per event (FR-16)."""
    os.makedirs(os.path.dirname(settings.audit_log_path) or ".", exist_ok=True)
    record = {"ts": datetime.now(timezone.utc).isoformat(), "event": event, **details}
    with open(settings.audit_log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
