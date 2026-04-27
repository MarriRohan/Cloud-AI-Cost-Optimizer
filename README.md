# Cloud AI Cost Optimizer

Production-grade full-stack system that simulates enterprise AWS environments and applies Generative AI + decision intelligence to reduce cloud spend.

## Problem Statement
Cloud costs grow quickly in large-scale environments because teams over-provision compute, keep cold storage on premium tiers, and miss savings opportunities in networking and serverless services. This project provides an internal FinOps-style platform to ingest AWS-like usage telemetry, detect inefficiencies, simulate optimization actions, and forecast business impact.

## Architecture (Text Diagram)

```text
                 +-------------------------+
                 |  React Dashboard (Vite) |
                 |  - Overview             |
                 |  - Recommendations      |
                 |  - Simulation           |
                 |  - Forecast             |
                 +------------+------------+
                              |
                              | REST APIs
                              v
+--------------------------------------------------------------+
|                  FastAPI Backend (Modular)                   |
| routes/                                                      |
|   - /upload-data /analyze /recommend /simulate /forecast     |
| services/                                                    |
|   - data_service (ingest + validate)                         |
|   - ai_service (LLM + fallback heuristics)                   |
|   - decision_service (action mapping + cost simulation)      |
|   - forecast_service (linear regression forecast)            |
|   - agent_service (Analyzer, Optimizer, Forecast agents)     |
| models/                                                      |
|   - SQLAlchemy entities + schemas                            |
| utils/                                                       |
|   - config and settings                                      |
+----------------------+---------------------------------------+
                       |
                       v
               SQLite/PostgreSQL database
```

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Pandas, scikit-learn
- **Frontend:** React, Vite, Recharts, Axios
- **AI Layer:** OpenAI API (strict JSON analysis prompt)
- **Database:** SQLite (local dev) / PostgreSQL-ready via `DATABASE_URL`

## Key Features
1. **Data ingestion** from CSV/JSON AWS Cost Explorer-like datasets (`POST /upload-data`).
2. **LLM-based analysis** with strict JSON contract:
   ```json
   {
     "issues": [],
     "recommendations": [],
     "estimated_savings": []
   }
   ```
3. **Decision engine** converts recommendations into executable actions (`t3.large -> t3.medium`, lifecycle policy, egress optimization).
4. **Optimization simulation** computes before/after costs, savings %, and utilization improvement.
5. **Forecasting engine** predicts next 30 days with and without optimization using linear regression.
6. **Multi-agent workflow** (Analyzer Agent, Optimizer Agent, Forecast Agent).
7. **Recruiter-friendly dashboard** with cost breakdown, recommendation view, simulation metrics, and forecast graph.

## API Endpoints
- `POST /upload-data`
- `GET /analyze`
- `GET /recommend`
- `GET /simulate`
- `GET /forecast`
- `GET /overview`

## Project Structure
```text
backend/
  main.py
  routes/
  services/
  models/
  utils/
  data/sample_aws_usage.csv
frontend/
  src/
    components/
    pages/
    services/
```

## Local Setup
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Demo Flow
1. Upload sample data:
```bash
curl -X POST "http://localhost:8000/upload-data" \
  -F "file=@backend/data/sample_aws_usage.csv"
```
2. Call simulation:
```bash
curl "http://localhost:8000/simulate"
```
3. Open UI on `http://localhost:5173`.

## Example Results (from sample data)
- **Before cost:** `$3,404.35`
- **After optimization:** `~$2,647.60`
- **Estimated savings:** `~22.2%`
- **Monthly projected savings:** `~$756.75`
- **30-day forecast comparison:** optimized trajectory remains lower than baseline across the horizon.

## Why this is Resume-Ready
- Demonstrates production-minded architecture, modular services, and clean contracts.
- Shows LLM integration for structured reasoning, not just chat output.
- Quantifies business impact through decision simulation and forecasting.
- Mirrors internal FinOps and cloud governance tooling patterns used at scale.
