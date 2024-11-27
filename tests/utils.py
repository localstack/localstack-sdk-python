import time
import uuid
from typing import Callable, TypeVar

import boto3


def short_uid():
    return str(uuid.uuid4())[:8]


T = TypeVar("T")


def retry(function: Callable[..., T], retries=3, sleep=1.0, sleep_before=0, **kwargs) -> T:
    raise_error = None
    if sleep_before > 0:
        time.sleep(sleep_before)
    retries = int(retries)
    for i in range(0, retries + 1):
        try:
            return function(**kwargs)
        except Exception as error:
            raise_error = error
            time.sleep(sleep)
    raise raise_error


def boto_client(service: str):
    return boto3.client(
        service,
        endpoint_url="http://localhost.localstack.cloud:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
