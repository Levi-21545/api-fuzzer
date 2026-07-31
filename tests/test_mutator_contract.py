import pytest

from fuzzer.model.schema import Schema
from fuzzer.mutator.base import Mutator
from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.registry import get_mutators_for_schema


@pytest.mark.parametrize(
    "schema",
    [
        Schema(type="string"),
        Schema(type="integer"),
        Schema(type="number"),
        Schema(type="boolean"),
        Schema(type="array", items=Schema(type="string")),
        Schema(type="object"),
    ],
)
def test_registered_mutators_follow_the_base_contract(schema: Schema):
    mutators = get_mutators_for_schema(schema)

    assert mutators
    assert all(isinstance(mutator, Mutator) for mutator in mutators)

    for mutator in mutators:
        operations = mutator.mutate((), schema)
        assert all(isinstance(operation, MutationOp) for operation in operations)
