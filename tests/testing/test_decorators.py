import pytest

from localstack.sdk.pods import PodsClient
from localstack.sdk.state import StateClient
from localstack.sdk.testing import cloudpods
from tests.utils import boto_client

DECORATOR_POD_NAME = "ls-sdk-pod-decorator"
QUEUE_NAME = "ls-decorator-queue"


@pytest.fixture(scope="class", autouse=True)
def create_state_and_pod():
    pods_client = PodsClient()
    sqs_client = boto_client("sqs")
    queue_url = sqs_client.create_queue(QueueName=QUEUE_NAME)["QueueUrl"]
    pods_client.save_pod(DECORATOR_POD_NAME)
    sqs_client.delete_queue(QueueUrl=queue_url)
    yield
    state_client = StateClient()
    state_client.reset_state()
    pods_client.delete_pod(DECORATOR_POD_NAME)


class TestPodsDecorators:
    @cloudpods(name=DECORATOR_POD_NAME)
    def test_pod_load_decorator(self):
        sqs_client = boto_client("sqs")
        assert sqs_client.get_queue_url(QueueName=QUEUE_NAME), "state from pod not restored"
