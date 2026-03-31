import pytest

from src.core.s3_client import get_bucket_name, get_env_variable


def test_get_env_variable_raises_if_missing(monkeypatch):
    monkeypatch.delenv("SOME_VAR", raising=False)
    with pytest.raises(EnvironmentError):
        get_env_variable("SOME_VAR")


def test_get_bucket_name(monkeypatch):
    monkeypatch.setenv("BUCKET_NAME", "test-bucket")
    assert get_bucket_name() == "test-bucket"
