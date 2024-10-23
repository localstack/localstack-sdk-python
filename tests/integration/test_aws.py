import json

import boto3

import localstack.sdk.aws


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
        sqs_client.create_queue(QueueName="test-queue")
        queue_url = sqs_client.get_queue_url(QueueName="test-queue")["QueueUrl"]

        for i in range(5):
            send_result = sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps({"event": f"random-event-{i}", "message": f"random-message-{i}"}),
            )
            assert send_result["MessageId"]

        response = self.client.list_all_sqs_messages(queue_url=queue_url)
        assert len(response.messages) == 5
