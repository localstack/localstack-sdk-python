from localstack.clients import BaseClient
from localstack.sdk.api import StateApi


class StateClient(BaseClient):
    def __init__(self, **args) -> None:
        super().__init__(**args)
        self._client = StateApi(self._api_client)

    def reset_state(self) -> None:
        self._client.localstack_state_reset_post_0()
