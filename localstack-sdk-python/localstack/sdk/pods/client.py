import base64
import json

from localstack.sdk.api import PodsApi
from localstack.sdk.clients import BaseClient
from localstack.sdk.models import PodList, PodSaveRequest, RemoteConfig
from localstack.sdk.pods.exceptions import PodLoadException, PodSaveException


def _empty_remote_config() -> RemoteConfig:
    return RemoteConfig(oneof_schema_1_validator={}, actual_instance={})


def _read_ndjson(raw_content: bytes) -> list[dict]:
    """
    Reads the byte content of a ndjson response into a list of dictionaries.
    :param raw_content: the byte content of a ndjson response.
    :return: a list of dicts.
    """
    ndjson_str = raw_content.decode("utf-8")
    return [json.loads(line) for line in ndjson_str.splitlines()]


def _get_completion_event(streamed_response: list[dict]) -> dict | None:
    """
    Parses the chucked response returned form the Cloud Pod save and load endpoints and return the completion event,
    i.e., the one summarizing the output (success or error) of the operation.
    :param streamed_response: a list of dictionaries for the chunked response.
    :return: the dictionary of the completion event, if found. None otherwise.
    """
    completion_events = [line for line in streamed_response if line.get("event") == "completion"]
    return completion_events[0] if completion_events else None


class PodsClient(BaseClient):
    """
    The client to interact with the Cloud Pod feature.
    """

    def __init__(self, **args) -> None:
        """
        Initializes a Cloud Pods client.
        :param auth_token: if provided, this token will be used for platform authentication. If not, it will be
            fetched from within the container itself.
        """
        super().__init__(**args)
        self._client = PodsApi(self._api_client)
        if self.auth_token:
            # If an auth token is provided, it will be used to authenticate platform calls for Cloud Pods.
            #   Only the pods tied to this token will be visible. If not provided, the token will be fetched from the
            #   container. This allows to separate container identity for caller identity, if needed.
            auth_header = get_platform_auth_header(self.auth_token)
            self._api_client.set_default_header("Authorization", auth_header["Authorization"])

    def save_pod(self, pod_name: str) -> None:
        """
        Saves the state in the LocalStack container into a Cloud Pod and uploads it to the LocalStack's platform.
        If a Cloud Pod with the given name already exists, a new version is created.
        :param pod_name: the name of the Cloud Pod to be saved.
        :return: None
        :raises PodSaveException: if the save operation returns an error
        """
        response = self._client.save_pod_with_http_info(
            name=pod_name, pod_save_request=PodSaveRequest()
        )
        if response.status_code != 200:
            raise PodSaveException(pod_name=pod_name)
        streamed_response = _read_ndjson(response.raw_data)
        completion_event = _get_completion_event(streamed_response)
        if completion_event["status"] == "error":
            raise PodSaveException(pod_name=pod_name, error=completion_event.get("message"))

    def load_pod(self, pod_name: str) -> None:
        """
        Loads a Cloud Pod into the LocalStack container.
        :param pod_name: the name of the Cloud Pod to load
        :return: None
        :raises PodLoadException: if the load operation returns an error
        """
        response = self._client.load_pod_with_http_info(
            name=pod_name, remote_config=_empty_remote_config()
        )
        if response.status_code != 200:
            raise PodLoadException(pod_name=pod_name)
        streamed_response = _read_ndjson(response.raw_data)
        completion_event = _get_completion_event(streamed_response)
        if completion_event["status"] == "error":
            raise PodLoadException(pod_name=pod_name, error=completion_event.get("message"))

    def delete_pod(self, pod_name: str) -> None:
        """
        Deletes a Cloud Pod.
        :param pod_name: the name of the Cloud Pod to be deleted.
        :return: None
        """
        return self._client.delete_pod(name=pod_name, remote_config=_empty_remote_config())

    def list_pods(self) -> PodList:
        """
        Returns the list of the Cloud Pods visible in the organization.
        :return: a PodList object
        """
        pods = self._client.list_pods(remote_config=_empty_remote_config())
        return pods


def get_platform_auth_header(token: str) -> dict[str, str]:
    """
    Given the auth token, crafts the authorization header to authenticate platform calls.
    :param token: the localstack auth token
    :return: a dictionary for the authorization header
    """
    _token = f":{token}"
    auth_encoded = base64.b64encode(_token.encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {auth_encoded}"}
