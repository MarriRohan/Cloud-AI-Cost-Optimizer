import json
from collections import defaultdict
from openai import OpenAI
from backend.models.entities import UsageRecord
from backend.utils.config import get_settings

settings = get_settings()


def _heuristic_analysis(records: list[UsageRecord]) -> dict:
    issues, recs, savings = [], [], []
    for r in records:
        if r.service == "EC2" and r.cpu_utilization < 20 and r.hours_used > 200:
            issues.append(f"Idle/over-provisioned EC2 {r.resource_id} ({r.instance_type})")
            recs.append(f"Rightsize {r.instance_type} to next smaller class for {r.resource_id}")
            savings.append({"resource_id": r.resource_id, "amount": round(r.cost * 0.35, 2)})
        if r.service == "S3" and r.storage_gb > 500 and r.requests < 10000:
            issues.append(f"Cold S3 storage likely on Standard tier for {r.resource_id}")
            recs.append(f"Move {r.resource_id} to S3 Intelligent-Tiering/Glacier")
            savings.append({"resource_id": r.resource_id, "amount": round(r.cost * 0.25, 2)})
        if r.service == "Lambda" and r.duration > 1500:
            issues.append(f"High Lambda duration for {r.resource_id}")
            recs.append(f"Optimize memory/runtime and introduce provisioned concurrency policy for {r.resource_id}")
            savings.append({"resource_id": r.resource_id, "amount": round(r.cost * 0.20, 2)})
        if r.service == "DataTransfer" and r.bandwidth > 800:
            issues.append(f"Large egress from {r.resource_id}")
            recs.append(f"Add CloudFront + compression for {r.resource_id}")
            savings.append({"resource_id": r.resource_id, "amount": round(r.cost * 0.18, 2)})

    if not issues:
        issues = ["No severe inefficiencies detected."]
        recs = ["Maintain current resource governance and monitor utilization."]
        savings = [{"resource_id": "all", "amount": 0}]

    return {"issues": issues, "recommendations": recs, "estimated_savings": savings}


def analyze_with_llm(records: list[UsageRecord]) -> dict:
    baseline = _heuristic_analysis(records)
    if not settings.openai_api_key:
        return baseline

    grouped: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        grouped[r.service].append({
            "resource_id": r.resource_id,
            "instance_type": r.instance_type,
            "hours_used": r.hours_used,
            "cpu_utilization": r.cpu_utilization,
            "storage_gb": r.storage_gb,
            "requests": r.requests,
            "invocations": r.invocations,
            "duration": r.duration,
            "bandwidth": r.bandwidth,
            "cost": r.cost,
        })

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = (
        "Input: structured AWS usage data. Task: detect inefficiencies (idle resources, over-provisioning, "
        "unused storage, inefficient pricing models). Output strict JSON with keys issues, recommendations, estimated_savings.\n"
        f"DATA={json.dumps(grouped)}"
    )

    try:
        resp = client.responses.create(
            model=settings.openai_model,
            input=prompt,
            temperature=0,
            response_format={"type": "json_object"},
        )
        payload = json.loads(resp.output_text)
        for key in ["issues", "recommendations", "estimated_savings"]:
            payload.setdefault(key, baseline[key])
        return payload
    except Exception:
        return baseline
