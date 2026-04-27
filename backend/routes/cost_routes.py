from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.models.schemas import AnalyzeResponse
from backend.services.data_service import parse_upload, persist_records, fetch_records
from backend.services.agent_service import AnalyzerAgent, OptimizerAgent, ForecastAgent

router = APIRouter()
analyzer = AnalyzerAgent()
optimizer = OptimizerAgent()
forecaster = ForecastAgent()


@router.post("/upload-data")
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    raw = await file.read()
    try:
        rows = parse_upload(raw, file.filename)
        count = persist_records(db, rows)
        return {"status": "ok", "ingested": count}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/analyze", response_model=AnalyzeResponse)
def analyze(db: Session = Depends(get_db)):
    records = fetch_records(db)
    return analyzer.run(records)


@router.get("/recommend")
def recommend(db: Session = Depends(get_db)):
    records = fetch_records(db)
    analysis = analyzer.run(records)
    simulation = optimizer.run(records, analysis)
    return {"actions": simulation["actions"], "recommendations": analysis["recommendations"]}


@router.get("/simulate")
def run_simulation(db: Session = Depends(get_db)):
    records = fetch_records(db)
    analysis = analyzer.run(records)
    simulation = optimizer.run(records, analysis)
    return simulation


@router.get("/forecast")
def forecast(db: Session = Depends(get_db)):
    records = fetch_records(db)
    analysis = analyzer.run(records)
    simulation = optimizer.run(records, analysis)
    return forecaster.run(records, simulation)


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    records = fetch_records(db)
    totals = {"EC2": 0, "S3": 0, "Lambda": 0, "DataTransfer": 0}
    for r in records:
        totals[r.service] = totals.get(r.service, 0) + r.cost
    return {"total_cost": round(sum(totals.values()), 2), "breakdown": totals}
