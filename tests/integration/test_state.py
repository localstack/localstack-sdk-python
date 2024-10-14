import boto3
import pytest

from localstack.sdk.state import StateClient


class TestStateClient:
    client = StateClient()

    def test_reset_state(self):
        sqs_client = boto3.client("sqs", endpoint_url=self.client.configuration.host)
        sqs_client.create_queue(QueueName="test-queue")
        url = sqs_client.get_queue_url(QueueName="test-queue")["QueueUrl"]
        assert url

        self.client.reset_state()

        with pytest.raises(Exception) as exc:
            sqs_client.get_queue_url(QueueName="test-queue")
        assert "AWS.SimpleQueueService.NonExistentQueue" == exc.value.response["Error"]["Code"]  # noqa
