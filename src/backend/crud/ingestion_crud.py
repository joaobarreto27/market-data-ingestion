from typing import Any


def get_ingestion_status() -> dict[str, Any]:
    return {"status": "ok", "message": "Serviço de ingestão ativo"}
