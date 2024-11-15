from localstack.sdk.api_client import ApiClient
from localstack.sdk.configuration import Configuration


class BaseClient:
    """A BaseClient creates a configuration and instantiate a ApiClient"""

    configuration: Configuration
    _api_client: ApiClient
    auth_token: str | None

    def __init__(self, host: str | None = None, auth_token: str | None = None, **kwargs) -> None:
        """
        Initialize a base client to interact with LocalStack developer endpoint.
        :param host: the host, http://localhost.localstack.cloud:4566 by default.
        :param auth_token: if provided, this token would be used for authentication against platform. It not, the
            LocalStack runtime will use the one used to start the container. The token used determines the Cloud
            Pods identity, i.e., which pods are available.
        """
        _host = host or "http://localhost.localstack.cloud:4566"
        self.auth_token = auth_token
        self.configuration = Configuration(host=_host)
        self._api_client = ApiClient(configuration=self.configuration)
