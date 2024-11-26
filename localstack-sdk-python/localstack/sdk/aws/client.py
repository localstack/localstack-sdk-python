import json

from localstack.sdk.api.aws_api import AwsApi
from localstack.sdk.clients import BaseClient
from localstack.sdk.models import (
    Message,
    SesSentEmail,
    SNSPlatformEndpointResponse,
    SNSSMSMessagesResponse,
)


def _from_sqs_query_to_json(xml_dict: dict) -> list[Message]:
    """
    todo: developer endpoint implements sqs-query protocol. Remove this workaround one we move them to json.
    """
    raw_messages = (
        xml_dict.get("ReceiveMessageResponse", {}).get("ReceiveMessageResult", {}) or {}
    ).get("Message", [])
    if isinstance(raw_messages, dict):
        raw_messages = [raw_messages]
    messages = []
    for msg in raw_messages:
        _attributes = msg.get("Attribute", [])
        attributes = {i["Name"]: i["Value"] for i in _attributes}
        _m = {
            "MessageId": msg.get("MessageId"),
            "ReceiptHandle": msg.get("ReceiptHandle"),
            "MD5OfBody": msg.get("MD5OfBody"),
            "Body": msg.get("Body"),
            "Attributes": attributes,
        }
        m = Message.from_dict(_m)
        messages.append(m)
    return messages


class AWSClient(BaseClient):
    """
    The client to interact with all the LocalStack's AWS endpoints.
    These endpoints offer specific features in addition to the ones offered by the AWS services. For instance,
    access all the messages withing a SQS without the side effect of deleting them.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._client = AwsApi(self._api_client)

    ########
    # SQS
    ########

    def list_sqs_messages(self, account_id: str, region: str, queue_name: str) -> list[Message]:
        """
        Lists all the SQS messages in a given queue in a specific account id and region, without any side effect.

        :param account_id: the account id of the queue
        :param region: the region of the queue
        :param queue_name: the name of the queue
        :return: the list of messages in the queue
        """
        response = self._client.list_sqs_messages_with_http_info(
            account_id=account_id, region=region, queue_name=queue_name
        )
        return _from_sqs_query_to_json(json.loads(response.raw_data))

    def list_sqs_messages_from_queue_url(self, queue_url: str) -> list[Message]:
        """
        Lists all the SQS messages in a given queue, without any side effect.

        :param queue_url: the URL of the queue
        :return: the list of messages in the queue
        """
        response = self._client.list_all_sqs_messages_with_http_info(queue_url=queue_url)
        return _from_sqs_query_to_json(json.loads(response.raw_data))

    ########
    # SES
    ########

    def get_ses_messages(
        self, id_filter: str | None = None, email_filter: str | None = None
    ) -> list[SesSentEmail]:
        """
        Returns all the in-memory saved SES messages. They can be filtered by message ID and/or message source.

        :param id_filter: the message id used as filter for the SES messages
        :param email_filter: the message source filter
        :return: a list of email sent with SES
        """
        response = self._client.get_ses_messages(id=id_filter, email=email_filter)
        return response.messages

    def discard_ses_messages(self, id_filter: str | None = None) -> None:
        """
        Clears all SES messages. An ID filter can be provided to delete only a specific message.

        :param id_filter: the id filter
        :return: None
        """
        return self._client.discard_ses_messages(id=id_filter)

    ########
    # SNS
    ########

    def get_sns_sms_messages(
        self,
        phone_number: str | None = None,
        account_id: str = "000000000000",
        region: str = "us-east-1",
    ) -> SNSSMSMessagesResponse:
        """
        Returns all SMS messages published to a phone number.

        :param phone_number: the phone number to which the messages have been published. If not specified, all messages
            are returned.
        :param account_id: the AWS Account ID from which the messages have been published. '000000000000' by default
        :param region:  the AWS region from which the messages have been published. us-east-1 by default
        :return:
        """
        return self._client.get_sns_sms_messages(
            phone_number=phone_number, account_id=account_id, region=region
        )

    def discard_sns_sms_messages(
        self,
        phone_number: str | None = None,
        account_id: str = "000000000000",
        region: str = "us-east-1",
    ) -> None:
        """
        Discards all SMS messages published to a phone number.

        :param phone_number: the phone number to which the messages have been published. If not specified, all messages
            are deleted.
        :param account_id: the AWS Account ID from which the messages have been published. '000000000000' by default
        :param region:  the AWS region from which the messages have been published. us-east-1 by default
        :return: None
        """
        return self._client.discard_sns_sms_messages(
            phone_number=phone_number, account_id=account_id, region=region
        )

    def get_sns_endpoint_messages(
        self,
        endpoint_arn: str | None = None,
        account_id: str = "000000000000",
        region: str = "us-east-1",
    ) -> SNSPlatformEndpointResponse:
        """
        Returns all the messages published to a platform endpoint.

        :param endpoint_arn: the ARN to which the messages have been published. If not specified, will return all the
            messages.
        :param account_id: the AWS Account ID from which the messages have been published. 000000000000 if not specified
        :param region: the AWS region from which the messages have been published. us-east-1 by default
        :return: a response with the list of messages and the queried region
        """
        return self._client.get_sns_endpoint_messages(
            endpoint_arn=endpoint_arn, account_id=account_id, region=region
        )

    def discard_sns_endpoint_messages(
        self,
        endpoint_arn: str | None = None,
        account_id: str = "000000000000",
        region: str = "us-east-1",
    ) -> None:
        """
        Discards all the messaged published to a platform endpoint.

        :param endpoint_arn: the ARN to which the messages have been published. If not specified, will discard all the
            messages.
        :param account_id: the AWS Account ID from which the messages have been published. 000000000000 if not specified
        :param region: the AWS region from which the messages have been published. us-east-1 by default
        :return: None
        """
        return self._client.discard_sns_endpoint_messages(
            endpoint_arn=endpoint_arn, account_id=account_id, region=region
        )


def get_default(**args) -> AwsApi:
    """Return a client with a default configuration"""
    return AwsApi(args)
