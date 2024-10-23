import json

from localstack.clients import BaseClient
from localstack.sdk.api.aws_api import AwsApi
from localstack.sdk.models import Message


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
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._client = AwsApi(self._api_client)

    def list_sqs_messages(self, account_id: str, region: str, queue_name: str) -> list[Message]:
        response = self._client.list_sqs_messages_with_http_info(
            account_id=account_id, region=region, queue_name=queue_name
        )
        return _from_sqs_query_to_json(json.loads(response.raw_data))

    def list_sqs_messages_from_queue_url(self, queue_url) -> list[Message]:
        response = self._client.list_all_sqs_messages_with_http_info(queue_url=queue_url)
        return _from_sqs_query_to_json(json.loads(response.raw_data))


def get_default(**args) -> AwsApi:
    """Return a client with a default configuration"""
    return AwsApi(args)
