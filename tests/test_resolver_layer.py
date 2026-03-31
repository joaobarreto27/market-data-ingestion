import pytest

from src.core.resolver_layer import build_s3_key, resolve_layer


def test_resolve_layer_json():
    assert resolve_layer(".json") == "bronze"


def test_resolve_layer_parquet():
    assert resolve_layer(".parquet") == "silver"


def test_resolve_layer_invalid():
    with pytest.raises(ValueError):
        resolve_layer(".csv")


def test_build_s3_key_without_prefix():
    assert build_s3_key("data.json", "bronze") == "bronze/data.json"


def test_build_s3_key_with_prefix():
    assert (
        build_s3_key("data.parquet", "silver", "project")
        == "project/silver/data.parquet"
    )
