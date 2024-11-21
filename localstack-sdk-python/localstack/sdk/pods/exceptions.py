class PodSaveException(Exception):
    message = "An error occurred while saving the Cloud Pod"

    def __init__(self, pod_name: str, error: str | None = None) -> None:
        _message = f"{self.message} '{pod_name}'"
        if error:
            _message += f": {error}"
        super().__init__(_message)


class PodLoadException(Exception):
    message = "An error occurred while loading the Cloud Pod"

    def __init__(self, pod_name: str, error: str | None = None) -> None:
        _message = f"{self.message} '{pod_name}'"
        if error:
            _message += f": {error}"
        super().__init__(_message)
