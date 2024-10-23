import json

import boto3

import localstack.sdk.aws
from utils import short_uid


class TestLocalStackAWS:
    client = localstack.sdk.aws.AWSClient()

    def test_list_sqs_messages(self):
        sqs_client = boto3.client(
            "sqs",
            endpoint_url=self.client.configuration.host,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
        queue_name = f"queue-{short_uid()}"
        sqs_client.create_queue(QueueName=queue_name)
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]

        for i in range(5):
            send_result = sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(
                    {"event": f"random-event-{i}", "message": f"random-message-{i}"}
                ),
            )
            assert send_result["MessageId"]

        messages = self.client.list_sqs_messages_from_queue_url(queue_url=queue_url)
        assert len(messages) == 5

    def test_list_sqs_messages_from_account_region(self):
        sqs_client_us = boto3.client(
            "sqs",
            endpoint_url=self.client.configuration.host,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
        queue_name = f"queue-{short_uid()}"
        sqs_client_us.create_queue(QueueName=queue_name)
        queue_url = sqs_client_us.get_queue_url(QueueName=queue_name)["QueueUrl"]

        send_result = sqs_client_us.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({"event": "random-event", "message": "random-message"}),
        )
        assert send_result["MessageId"]

        messages = self.client.list_sqs_messages(
            account_id="000000000000", region="us-east-1", queue_name=queue_name
        )
        assert messages[0].message_id == send_result["MessageId"]

    def test_empty_queue(self):
        sqs_client = boto3.client(
            "sqs",
            endpoint_url=self.client.configuration.host,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
        queue_name = f"queue-{short_uid()}"
        sqs_client.create_queue(QueueName=queue_name)
        messages = self.client.list_sqs_messages(
            account_id="000000000000", region="us-east-1", queue_name=queue_name
        )
        assert messages == []
