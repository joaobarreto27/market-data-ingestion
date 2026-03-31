import os
from typing import Any

import boto3
from botocore.client import BaseClient
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name: str, required: bool = True) -> str:
    value = os.getenv(name)
    if not value:
        if required:
            raise EnvironmentError(f"Variável de ambiente '{name}' não configurada")
        return ""
    return value


def get_s3_client() -> BaseClient:
    aws_access_key_id = get_env_variable("AWS_ACCESS_KEY_ID", required=False)
    aws_secret_access_key = get_env_variable("AWS_SECRET_ACCESS_KEY", required=False)
    aws_region = get_env_variable("AWS_REGION", required=False)

    client_kwargs = {}

    if aws_access_key_id and aws_secret_access_key:
        client_kwargs["aws_access_key_id"] = aws_access_key_id
        client_kwargs["aws_secret_access_key"] = aws_secret_access_key

    if aws_region:
        client_kwargs["region_name"] = aws_region

    return boto3.client("s3", **client_kwargs)


def get_bucket_name() -> str:
    load_dotenv()
    return get_env_variable("STORAGE_BUCKET")


def upload_fileobj_to_s3(
    s3_client: BaseClient, file_obj: Any, bucket: str, key: str
) -> None:
    s3_client.upload_fileobj(file_obj, bucket, key)
