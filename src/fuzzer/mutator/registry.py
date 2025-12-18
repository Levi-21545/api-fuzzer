from typing import List

from fuzzer.model.schema import Schema
from fuzzer.mutator.base import Mutator

from fuzzer.mutator.string import StringMutator
from fuzzer.mutator.numeric import NumericMutator
from fuzzer.mutator.boolean import BooleanMutator
from fuzzer.mutator.array import ArrayMutator
from fuzzer.mutator.object import ObjectMutator


def get_mutators_for_schema(schema: Schema) -> List[Mutator]:
    """
    Return the list of mutators applicable to a given schema type.
    """

    mutators: list[Mutator] = []

    if schema.type == "string":
        mutators.append(StringMutator())

    elif schema.type in ("integer", "number"):
        mutators.append(NumericMutator())

    elif schema.type == "boolean":
        mutators.append(BooleanMutator())

    elif schema.type == "array":
        mutators.append(ArrayMutator())

    elif schema.type == "object":
        mutators.append(ObjectMutator())

    return mutators
