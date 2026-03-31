from fastapi import APIRouter

from ..crud.ingestion_crud import get_ingestion_status

router = APIRouter()


@router.get("/health")
def health_check():
    return get_ingestion_status()
