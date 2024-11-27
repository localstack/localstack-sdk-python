import json
import random

import localstack.sdk.aws
from tests.utils import boto_client, retry, short_uid

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
        sqs_client = boto_client("sqs")
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
        sqs_client = boto_client("sqs")
        queue_name = f"queue-{short_uid()}"
        sqs_client.create_queue(QueueName=queue_name)
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]

        send_result = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({"event": "random-event", "message": "random-message"}),
        )
        assert send_result["MessageId"]

        messages = self.client.list_sqs_messages(
            account_id="000000000000", region="us-east-1", queue_name=queue_name
        )
        assert messages[0].message_id == send_result["MessageId"]

    def test_empty_queue(self):
        sqs_client = boto_client("sqs")
        queue_name = f"queue-{short_uid()}"
        sqs_client.create_queue(QueueName=queue_name)
        messages = self.client.list_sqs_messages(
            account_id="000000000000", region="us-east-1", queue_name=queue_name
        )
        assert messages == []

    def test_get_and_discard_ses_messages(self):
        aws_client = boto_client("ses")
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

    def test_sns_platform_endpoint_messages(self):
        client = boto_client("sns")
        # create a topic
        topic_name = f"topic-{short_uid()}"
        topic_arn = client.create_topic(Name=topic_name)["TopicArn"]

        app_name = f"app-name-{short_uid()}"
        platform_arn = client.create_platform_application(
            Name=app_name,
            Platform="APNS",
            Attributes={},
        )["PlatformApplicationArn"]

        endpoint_arn = client.create_platform_endpoint(
            PlatformApplicationArn=platform_arn, Token=short_uid()
        )["EndpointArn"]

        client.subscribe(
            TopicArn=topic_arn,
            Protocol="application",
            Endpoint=endpoint_arn,
        )

        message_for_topic = {
            "default": "This is the default message which must be present when publishing a message to a topic.",
            "APNS": json.dumps({"aps": {"content-available": 1}}),
        }
        message_for_topic_string = json.dumps(message_for_topic)
        message_attributes = {
            "AWS.SNS.MOBILE.APNS.TOPIC": {
                "DataType": "String",
                "StringValue": "com.amazon.mobile.messaging.myapp",
            },
            "AWS.SNS.MOBILE.APNS.PUSH_TYPE": {
                "DataType": "String",
                "StringValue": "background",
            },
            "AWS.SNS.MOBILE.APNS.PRIORITY": {
                "DataType": "String",
                "StringValue": "5",
            },
        }

        client.publish(
            TopicArn=topic_arn,
            Message=message_for_topic_string,
            MessageAttributes=message_attributes,
            MessageStructure="json",
        )

        msg_response = self.client.get_sns_endpoint_messages(endpoint_arn=endpoint_arn)
        assert msg_response.region == "us-east-1"
        assert len(msg_response.platform_endpoint_messages[endpoint_arn]) >= 0

        assert msg_response.platform_endpoint_messages[endpoint_arn][0].message == json.dumps(
            message_for_topic["APNS"]
        )
        assert (
            msg_response.platform_endpoint_messages[endpoint_arn][0].message_attributes
            == message_attributes
        )

        self.client.discard_sns_endpoint_messages(endpoint_arn=endpoint_arn)
        msg_response = self.client.get_sns_endpoint_messages(endpoint_arn=endpoint_arn)
        # todo: the endpoint arn remains as key; verify that this is intended behavior
        assert not msg_response.platform_endpoint_messages[
            endpoint_arn
        ], "platform messages not cleared"

    def test_sns_messages(self):
        client = boto_client("sns")
        numbers = [
            f"+{random.randint(100000000, 9999999999)}",
            f"+{random.randint(100000000, 9999999999)}",
            f"+{random.randint(100000000, 9999999999)}",
        ]

        topic_name = f"topic-{short_uid()}"
        topic_arn = client.create_topic(Name=topic_name)["TopicArn"]

        for number in numbers:
            client.subscribe(
                TopicArn=topic_arn,
                Protocol="sms",
                Endpoint=number,
            )

        client.publish(Message="Hello World", TopicArn=topic_arn)
        client.publish(PhoneNumber=numbers[0], Message="Hello World")

        def _check_messages():
            msg_response = self.client.get_sns_sms_messages()
            assert len(msg_response.sms_messages) == 3
            return msg_response.sms_messages

        msgs = retry(_check_messages)
        assert len(msgs[numbers[0]]) == 2
        assert len(msgs[numbers[1]]) == 1
        assert len(msgs[numbers[2]]) == 1

        # selective discard
        self.client.discard_sns_sms_messages(phone_number=numbers[0])
        msg_response = self.client.get_sns_sms_messages()
        assert numbers[0] not in msg_response.sms_messages

        self.client.discard_sns_sms_messages()
        msg_response = self.client.get_sns_sms_messages()
        assert not msg_response.sms_messages
