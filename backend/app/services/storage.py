from datetime import datetime
from pathlib import Path

import boto3

from app.core.config import settings


def _local_store(content: bytes, filename: str) -> str:
    base_path = Path(settings.local_storage_path)
    base_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_name = filename.replace("/", "_").replace("\\", "_")
    target = base_path / f"{timestamp}-{safe_name}"
    target.write_bytes(content)
    return str(target)


def upload_to_s3(content: bytes, filename: str) -> str:
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        return _local_store(content, filename)

    session = boto3.Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.s3_region,
    )
    client = session.client("s3")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    key = f"{settings.s3_prefix}/{timestamp}-{filename}"
    client.put_object(Bucket=settings.s3_bucket, Key=key, Body=content)
    return key
