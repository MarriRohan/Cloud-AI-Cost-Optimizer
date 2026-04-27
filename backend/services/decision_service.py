from backend.models.entities import UsageRecord


def build_actions(analysis: dict) -> list[dict]:
    actions = []
    for rec in analysis.get("recommendations", []):
        if "Rightsize" in rec:
            actions.append({"action": "downsize_instance", "detail": rec, "factor": 0.65})
        elif "Intelligent-Tiering" in rec or "Glacier" in rec:
            actions.append({"action": "s3_lifecycle_policy", "detail": rec, "factor": 0.75})
        elif "CloudFront" in rec:
            actions.append({"action": "egress_optimization", "detail": rec, "factor": 0.82})
        elif "Lambda" in rec or "runtime" in rec:
            actions.append({"action": "lambda_tuning", "detail": rec, "factor": 0.80})
    return actions


def simulate(records: list[UsageRecord], analysis: dict) -> dict:
    before = sum(r.cost for r in records)
    estimated_save = sum(float(x.get("amount", 0)) for x in analysis.get("estimated_savings", []))
    after = max(before - estimated_save, 0)
    savings_percent = round((estimated_save / before) * 100, 2) if before else 0

    avg_cpu_before = sum(r.cpu_utilization for r in records if r.service == "EC2") / max(len([r for r in records if r.service == "EC2"]), 1)
    avg_cpu_after = min(avg_cpu_before + 18, 100)
    util_improvement = round(((avg_cpu_after - avg_cpu_before) / max(avg_cpu_before, 1)) * 100, 2)

    return {
        "before_cost": round(before, 2),
        "after_cost": round(after, 2),
        "savings_percent": savings_percent,
        "monthly_projected_savings": round(estimated_save, 2),
        "utilization_improvement_percent": util_improvement,
        "actions": build_actions(analysis),
    }
