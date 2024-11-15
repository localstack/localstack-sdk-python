from functools import wraps

import pytest

from localstack.sdk.pods import PodsClient
# from localstack.sdk.state import StateClient


@pytest.hookimpl
def pytest_configure(config):
    """Make cloudpods available globally in pytest."""
    pytest.cloudpods = cloudpods

def cloudpods(*args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*test_args, **test_kwargs):
            # Pre-test logic
            print(kwargs)
            print(test_args)
            print(test_kwargs)
            # pod_name = kwargs["name"]
            pods_client = PodsClient()
            pods = pods_client.list_pods()
            print(pods)
            # pods_client.load_pod(pod_name=pod_name)
            print("before!")
            try:
                # Run the actual test function
                result = func(*test_args, **test_kwargs)
            finally:
                print("after!")
                # state_client = StateClient()
                # state_client.reset_state()
            return result
        return wrapper
    return decorator