from localstack.sdk.api.chaos_api import ChaosApi
from localstack.sdk.clients import BaseClient
from localstack.sdk.models import FaultRule, NetworkEffectsConfig


class ChaosClient(BaseClient):
    """
    The client to interact with the LocalStack's Chaos API.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._client = ChaosApi(self._api_client)

    def set_fault_rules(self, fault_rules: list[FaultRule]) -> list[FaultRule]:
        """
        Creates a new sets of fault rules. It overwrites the previous ones.
        :param fault_rules: the list of FaultRule we want to set
        :return: the list of FaultRule currently in place
        """
        return self._client.set_fault_rules(fault_rule=fault_rules)

    def add_fault_rules(self, fault_rules: list[FaultRule]) -> list[FaultRule]:
        """
        Adds a new set of rules to the current fault configuration.
        :param fault_rules: the FaultRule rules to add
        :return: the list of FaultRule currently in place
        """
        return self._client.add_fault_rules(fault_rule=fault_rules)

    def delete_fault_rules(self, fault_rules: list[FaultRule]) -> list[FaultRule]:
        """
        Deletes a set of rules from the fault configuration.
        :param fault_rules: the FaultRule to delete
        :return: the list of FaultRule currently in place
        """
        return self._client.delete_fault_rules(fault_rule=fault_rules)

    def get_fault_rules(self) -> list[FaultRule]:
        """
        Gets the current fault configuration.
        :return: the list of FaultRule of the current configuration
        """
        return self._client.get_fault_rules()

    def get_network_effects(self) -> NetworkEffectsConfig:
        """
        Gets the current network effect configuration.
        :return: the current NetworkEffectsConfig
        """
        return self._client.get_network_effects()

    def set_network_effects(
        self, network_effects_config: NetworkEffectsConfig
    ) -> NetworkEffectsConfig:
        """
        Configure a new network effect, e.g, latency.
        :param network_effects_config: the network config to be set
        :return: the current configuration of network effects
        """
        return self._client.set_network_effects(network_effects_config=network_effects_config)


def get_default(**args) -> ChaosClient:
    """
    Return a chaos client with a default configuration. You can pass a host argument to overwrite the fault one
    (http://localhost.localstack.cloud:4566).
    """
    return ChaosClient(**args)
