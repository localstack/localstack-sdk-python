import pytest

from localstack.sdk.state import StateClient


@pytest.fixture
def reset_state():
    """This fixture is used to completely reset the state of LocalStack after a test runs."""
    yield
    state_client = StateClient()
    state_client.reset_state()
