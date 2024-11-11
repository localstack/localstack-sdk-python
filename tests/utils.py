import time
import uuid
from typing import Callable, TypeVar


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
