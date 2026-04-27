from collections import defaultdict
import numpy as np
from sklearn.linear_model import LinearRegression
from backend.models.entities import UsageRecord


def forecast_30_days(records: list[UsageRecord], optimized_monthly_savings: float) -> dict:
    daily = defaultdict(float)
    for r in records:
        day = r.usage_date or "2026-01-01"
        daily[day] += r.cost

    series = list(daily.values())
    if len(series) < 2:
        avg = sum(series) / len(series) if series else 0
        series = [avg + i * 2 for i in range(10)]

    x = np.arange(len(series)).reshape(-1, 1)
    y = np.array(series)
    model = LinearRegression().fit(x, y)

    future_days = np.arange(len(series), len(series) + 30).reshape(-1, 1)
    baseline = model.predict(future_days)
    per_day_savings = optimized_monthly_savings / 30
    optimized = np.maximum(baseline - per_day_savings, 0)

    points = [
        {"day": i + 1, "baseline_cost": round(float(b), 2), "optimized_cost": round(float(o), 2)}
        for i, (b, o) in enumerate(zip(baseline, optimized))
    ]

    return {
        "points": points,
        "baseline_total_30d": round(float(baseline.sum()), 2),
        "optimized_total_30d": round(float(optimized.sum()), 2),
    }
