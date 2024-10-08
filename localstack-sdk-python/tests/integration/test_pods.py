from localstack.pods import PodsClient

POD_NAME = f"ls-sdk-integration"


class TestPodsClient():
    client = PodsClient()

    def test_pod_list(self):
        pods = self.client.list_pods()
        assert pods

    def test_pod_crud(self):
        self.client.save_pod(pod_name=POD_NAME)
        self.client.load_pod(pod_name=POD_NAME)
        self.client.delete_pod(pod_name=POD_NAME)