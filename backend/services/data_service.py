import io
import json
import pandas as pd
from sqlalchemy.orm import Session
from backend.models.entities import UsageRecord


VALID_COLUMNS = {
    "service", "resource_id", "instance_type", "hours_used", "cpu_utilization",
    "storage_gb", "requests", "invocations", "duration", "bandwidth", "cost", "usage_date"
}


def parse_upload(file_bytes: bytes, filename: str) -> list[dict]:
    if filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
        data = df.to_dict(orient="records")
    elif filename.endswith(".json"):
        payload = json.loads(file_bytes.decode("utf-8"))
        data = payload if isinstance(payload, list) else payload.get("records", [])
    else:
        raise ValueError("Unsupported file type. Upload CSV or JSON")

    cleaned = []
    for row in data:
        cleaned.append({k: row.get(k) for k in VALID_COLUMNS})
    return cleaned


def persist_records(db: Session, rows: list[dict]) -> int:
    objects = [UsageRecord(**row) for row in rows]
    db.bulk_save_objects(objects)
    db.commit()
    return len(objects)


def fetch_records(db: Session) -> list[UsageRecord]:
    return db.query(UsageRecord).all()
