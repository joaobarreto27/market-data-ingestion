import os
from typing import Any

import boto3
from botocore.client import BaseClient
from dotenv import load_dotenv


def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Variável de ambiente '{name}' não configurada")
    return value


def get_s3_client() -> BaseClient:
    load_dotenv()

    aws_access_key_id = get_env_variable("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_env_variable("AWS_SECRET_ACCESS_KEY")
    aws_region = get_env_variable("AWS_REGION")

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )


def get_bucket_name() -> str:
    load_dotenv()
    return get_env_variable("STORAGE_BUCKET")


def upload_fileobj_to_s3(
    s3_client: BaseClient, file_obj: Any, bucket: str, key: str
) -> None:
    s3_client.upload_fileobj(file_obj, bucket, key)
