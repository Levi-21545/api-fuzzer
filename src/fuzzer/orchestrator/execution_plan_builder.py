from typing import Any, Iterable
from fuzzer.model.endpoint import Endpoint
from fuzzer.mutator.engine import MutationEngine
from fuzzer.payloads.generator import generates_payloads


def build_execution_plan(
        endpoints: list[Endpoint],
        mutation_engine: MutationEngine
    ) -> Iterable[tuple[Endpoint, Any | None, dict[str, str]]]:
    """
    Transforma endpoints em uma sequência de
    (endpoint, payload, headers)
    """
    for endpoint in endpoints:
        for payload, headers in generates_payloads(endpoint, mutation_engine):
            yield endpoint, payload, headers
