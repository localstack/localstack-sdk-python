import logging
from functools import wraps

from localstack.sdk.pods import PodsClient
from localstack.sdk.state import StateClient

LOG = logging.getLogger(__name__)


def cloudpods(*args, **kwargs):
    """This is a decorator that loads a cloud pod before a test and resets the state afterward."""

    def decorator(func):
        @wraps(func)
        def wrapper(*test_args, **test_kwargs):
            if not (pod_name := kwargs.get("name")):
                raise Exception("Specify a Cloud Pod name in the `name` arg")
            pods_client = PodsClient()
            LOG.debug("Loading %s", pod_name)
            pods_client.load_pod(pod_name=pod_name)
            try:
                result = func(*test_args, **test_kwargs)
            finally:
                LOG.debug("Reset state of the container")
                state_client = StateClient()
                state_client.reset_state()
            return result

        return wrapper

    return decorator
