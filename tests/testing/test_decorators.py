import boto3
import pytest

from localstack.sdk.aws import AWSClient
from localstack.sdk.pods import PodsClient
from localstack.sdk.state import StateClient
from localstack.sdk.testing import cloudpods

DECORATOR_POD_NAME = "ls-sdk-pod-decorator"
QUEUE_NAME = "ls-decorator-queue"


@pytest.fixture(scope="class", autouse=True)
def create_state_and_pod():
    sdk_client = AWSClient()
    pods_client = PodsClient()
    sqs_client = boto3.client(
        "sqs",
        endpoint_url=sdk_client.configuration.host,
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
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
        sqs_client = boto3.client(
            "sqs",
            endpoint_url="http://localhost.localstack.cloud:4566",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
        assert sqs_client.get_queue_url(QueueName=QUEUE_NAME), "state from pod not restored"
