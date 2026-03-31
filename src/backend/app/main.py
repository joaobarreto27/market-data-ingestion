from fastapi import FastAPI

from src.backend.routes.routes_ingest import router as ingest_router

app = FastAPI(title="Market Data Ingestion")

app.include_router(ingest_router, prefix="/api")


@app.get("/")
def health():
    return {"status": "ok", "service": "market_data_ingestion"}
