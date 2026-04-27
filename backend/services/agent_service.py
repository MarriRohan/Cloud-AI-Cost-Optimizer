from backend.services.ai_service import analyze_with_llm
from backend.services.decision_service import simulate
from backend.services.forecast_service import forecast_30_days


class AnalyzerAgent:
    def run(self, records):
        return analyze_with_llm(records)


class OptimizerAgent:
    def run(self, records, analysis):
        return simulate(records, analysis)


class ForecastAgent:
    def run(self, records, simulation):
        return forecast_30_days(records, simulation["monthly_projected_savings"])
