from typing import Literal

Layer = Literal["bronze", "silver"]


def resolve_layer(file_extension: str) -> Layer:
    ext = file_extension.lower().strip()
    if ext == ".json":
        return "bronze"
    if ext == ".parquet":
        return "silver"
    raise ValueError(f"Extensão de arquivo não suportada: {file_extension}")


def build_s3_key(file_name: str, layer: Layer, prefix: str | None = None) -> str:
    prefix = prefix.strip().rstrip("/") if prefix else ""
    if prefix:
        return f"{prefix}/{layer}/{file_name}"
    return f"{layer}/{file_name}"
