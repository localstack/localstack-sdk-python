import os

from localstack.api_client import ApiClient
from localstack.configuration import Configuration


class BaseClient:
    """A BaseClient creates a configuration and instantiate a ApiClient"""
    configuration: Configuration
    _api_client: ApiClient
    auth_token: str | None

    def __init__(self, host: str | None = None, auth_token: str | None = None, **kwargs) -> None:
        _host = host or "http://localhost.localstack.cloud:4566"
        self.auth_token = auth_token or os.getenv("LOCALSTACK_AUTH_TOKEN", "").strip("'\" ")
        self.configuration = Configuration(host=_host)
        self._api_client = ApiClient(configuration=self.configuration)