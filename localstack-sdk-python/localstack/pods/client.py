import base64
import json

from localstack.api import PodsApi
from localstack.clients import BaseClient
from localstack.models import RemoteConfig, PodSaveRequest


def _empty_remote_config() -> RemoteConfig:
    return RemoteConfig(
        oneof_schema_1_validator={},
        actual_instance={}
    )


def _read_ndjson(raw_content: bytes) -> list[dict]:
    ndjson_str = raw_content.decode('utf-8')
    return [json.loads(line) for line in ndjson_str.splitlines()]


def _get_completion_event(streamed_response: list[dict]) -> dict | None:
    completion_events = [
        line for line in streamed_response if line.get("event") == "completion"
    ]
    return completion_events[0] if completion_events else None

class PodsClient(BaseClient):

    def __init__(self, **args) -> None:
        super().__init__(**args)
        self._client = PodsApi(self._api_client)
        # https://github.com/localstack/localstack-ext/pull/3469 could be avoided after this
        assert self.auth_token
        auth_header = get_platform_auth_header(self.auth_token)
        self._api_client.set_default_header("Authorization", auth_header["Authorization"])

    def save_pod(self, pod_name: str) -> None:
        """
        :raise exception if the save does not succeed
        """
        try:
            response = self._client.save_pod_with_http_info(name=pod_name, pod_save_request=PodSaveRequest())
        except Exception as e:
            raise(e)
        if response.status_code != 200:
            pass
        streamed_response = _read_ndjson(response.raw_data)
        completion_event = _get_completion_event(streamed_response)
        if completion_event["status"] == "error":
            # todo: define exception
            raise Exception(completion_event.get("message"))

    def load_pod(self, pod_name: str) -> None:
        """
        :raise exception if the load does not succeed
        """
        response = self._client.load_pod_with_http_info(name=pod_name, remote_config=_empty_remote_config())
        if response.status_code != 200:
            pass
        streamed_response = _read_ndjson(response.raw_data)
        completion_event = _get_completion_event(streamed_response)
        if completion_event["status"] == "error":
            # todo: define exception
            raise Exception(completion_event.get("message"))

    def delete_pod(self, pod_name: str) -> None:
        return self._client.delete_pod(name=pod_name, remote_config=_empty_remote_config())

    def list_pods(self):
        # todo: fix CloudPodInner model;
        pods = self._client.list_pods(remote_config=_empty_remote_config())
        return pods


def get_platform_auth_header(token: str) -> dict[str, str]:
    _token = f":{token}"
    auth_encoded = base64.b64encode(_token.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {auth_encoded}"}

