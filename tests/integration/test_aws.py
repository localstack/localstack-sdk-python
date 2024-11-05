import json

import boto3

import localstack.sdk.aws
from tests.utils import short_uid

SAMPLE_SIMPLE_EMAIL = {
    "Subject": {
        "Data": "SOME_SUBJECT",
    },
    "Body": {
        "Text": {
            "Data": "SOME_MESSAGE",
        },
        "Html": {
            "Data": "<p>SOME_HTML</p>",
        },
    },
}


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

    def test_get_and_discard_ses_messages(self):
        aws_client = boto3.client(
            "ses",
            endpoint_url=self.client.configuration.host,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )

        email = f"user-{short_uid()}@example.com"
        aws_client.verify_email_address(EmailAddress=email)

        message1 = aws_client.send_email(
            Source=email,
            Message=SAMPLE_SIMPLE_EMAIL,
            Destination={
                "ToAddresses": ["success@example.com"],
            },
        )
        message1_id = message1["MessageId"]

        # Send a raw message
        raw_message_data = f"From: {email}\nTo: recipient@example.com\nSubject: test\n\nThis is the message body.\n\n"
        message2 = aws_client.send_raw_email(RawMessage={"Data": raw_message_data})
        message2_id = message2["MessageId"]

        # filter by message id
        messages = self.client.get_ses_messages(id_filter=message1_id)
        assert len(messages) == 1
        assert messages[0].id == message1_id
        assert messages[0].subject == "SOME_SUBJECT"
        assert messages[0].body.html_part == "<p>SOME_HTML</p>"
        assert messages[0].body.text_part == "SOME_MESSAGE"

        messages = self.client.get_ses_messages(id_filter=message2_id)
        assert len(messages) == 1

        # filter by email body
        messages = self.client.get_ses_messages(email_filter="none@example.com")
        assert len(messages) == 0
        messages = self.client.get_ses_messages(email_filter=email)
        assert len(messages) == 2

        # no filter
        messages = self.client.get_ses_messages()
        assert len(messages) == 2

        # discard messages
        self.client.discard_ses_messages(id_filter=message1_id)
        messages = self.client.get_ses_messages(id_filter=message2_id)
        assert len(messages) == 1
        assert messages[0].id == message2_id

        self.client.discard_ses_messages()
        assert not self.client.get_ses_messages()
