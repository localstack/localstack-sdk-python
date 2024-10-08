from localstack.clients import BaseClient
from localstack.api.chaos_api import ChaosApi
from localstack.models import FaultRule, NetworkEffectsConfig


class ChaosClient(BaseClient):
    """
    The client for the ChaosAPI.
    This is mostly a wrapper of the ChaosApi class, which is automatically generated from the OpenAPI specs.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._client = ChaosApi(self._api_client)

    def set_fault_rules(self, fault_rules: list[FaultRule]) -> list[FaultRule]:
        return self._client.set_fault_rules(fault_rule=fault_rules)

    def add_fault_rules(self, fault_rules: list[FaultRule]) -> list[FaultRule]:
        return self._client.add_fault_rules(fault_rule=fault_rules)

    def delete_fault_rules(self, fault_rules: list[FaultRule]) -> list[FaultRule]:
        return self._client.delete_fault_rules(fault_rule=fault_rules)

    def get_fault_rules(self) -> list[FaultRule]:
        return self._client.get_fault_rules()

    def get_network_effects(self) -> NetworkEffectsConfig:
        return self._client.get_network_effects()

    def set_network_effects(
        self, network_effects_config: NetworkEffectsConfig
    ) -> NetworkEffectsConfig:
        return self._client.set_network_effects(
            network_effects_config=network_effects_config
        )


def get_default(**args) -> ChaosClient:
    """Return a default chaos client with a default configuration"""
    return ChaosClient(**args)