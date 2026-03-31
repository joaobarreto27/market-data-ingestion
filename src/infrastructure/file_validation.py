import json


def validate_json_bytes(content: bytes) -> bool:
    try:
        _ = json.loads(content.decode("utf-8"))
        return True
    except Exception:
        return False


def validate_parquet_bytes(content: bytes) -> bool:
    try:
        import pyarrow.parquet as pq
        from pyarrow import BufferReader

        buf = BufferReader(content)
        pq.read_table(buf)
        return True
    except Exception:
        return False


def is_supported_extension(filename: str) -> bool:
    filename_lower = filename.lower()
    return filename_lower.endswith(".json") or filename_lower.endswith(".parquet")
