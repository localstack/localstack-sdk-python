from localstack.sdk.api import StateApi
from localstack.sdk.clients import BaseClient


class StateClient(BaseClient):
    """
    Initializes a client to handle LocalStack's state.
    """

    def __init__(self, **args) -> None:
        super().__init__(**args)
        self._client = StateApi(self._api_client)

    def reset_state(self) -> None:
        """
        Resets the state of LocalStack for all running services.
        :return: None
        """
        self._client.localstack_state_reset_post()
