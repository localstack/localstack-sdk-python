import localstack.sdk.aws
from localstack.sdk import version


def test_client_version():
    client = localstack.sdk.aws.AWSClient()
    assert version.version in client._api_client.user_agent
