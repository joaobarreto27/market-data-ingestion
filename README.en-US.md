# market-data-ingestion

## Description

Streamlit app to ingest files into AWS S3 bucket.

- Supports multi-file upload for `.json` and `.parquet`.
- `.json` is saved to `bronze/`.
- `.parquet` is saved to `silver/`.
- Uses `resolver_layer` to map ingestion layer.

## Project structure

- `src/core/` - S3 client, validation, and resolver layer.
- `src/backend/` - routes and CRUD (FastAPI support).
- `src/frontend/app/` - Streamlit app.
- `tests/` - unit tests.

## Setup

1. Create `.env` in `market_data_ingestion`:

```env
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_REGION=<your-region>
STORAGE_BUCKET=<your-bucket>
```

2. Install dependencies:

```bash
pip install -e .
```

3. Run Streamlit:

```bash
streamlit run src/frontend/app/app.py
```

## Health API (optional)

```bash
uvicorn src.backend.app.main:app --reload --port 8000
```

GET http://localhost:8000/api/health

## Tests

```bash
python -m pytest -q
```

## Ingestion path

- `.json` → `bronze/<prefix>/<filename>.json`
- `.parquet` → `silver/<prefix>/<filename>.parquet`
