from contextlib import contextmanager

from localstack.sdk.chaos.client import get_default
from localstack.sdk.models import FaultRule


@contextmanager
def fault_configuration(fault_rules: list[FaultRule]):
    """
    This is a context manager that temporarily applies a given set of fault rules.
    :param fault_rules: a list of FaultRule to be applied.
    :return: None
    """
    client = get_default()
    try:
        client.set_fault_rules(fault_rules=fault_rules)
        yield
    finally:
        client.delete_fault_rules(fault_rules=fault_rules)
