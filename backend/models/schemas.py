from pydantic import BaseModel
from typing import Any


class UsageIn(BaseModel):
    service: str
    resource_id: str | None = None
    instance_type: str | None = None
    hours_used: float = 0
    cpu_utilization: float = 0
    storage_gb: float = 0
    requests: float = 0
    invocations: float = 0
    duration: float = 0
    bandwidth: float = 0
    cost: float
    usage_date: str | None = None


class AnalyzeResponse(BaseModel):
    issues: list[str]
    recommendations: list[str]
    estimated_savings: list[dict[str, Any]]


class SimulationResponse(BaseModel):
    before_cost: float
    after_cost: float
    savings_percent: float
    monthly_projected_savings: float
    utilization_improvement_percent: float


class ForecastPoint(BaseModel):
    day: int
    baseline_cost: float
    optimized_cost: float


class ForecastResponse(BaseModel):
    points: list[ForecastPoint]
    baseline_total_30d: float
    optimized_total_30d: float
