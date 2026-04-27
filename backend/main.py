from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.database import Base, engine
from backend.routes.cost_routes import router
from backend.utils.config import get_settings

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"service": settings.app_name, "status": "running"}
