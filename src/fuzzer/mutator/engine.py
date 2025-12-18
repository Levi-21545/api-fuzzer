from typing import Any

from fuzzer.model.schema import Schema

from fuzzer.generator.valid_generator import generate_valid_value

from fuzzer.mutator.string import StringMutator
from fuzzer.mutator.numeric import NumericMutator
from fuzzer.mutator.boolean import BooleanMutator
from fuzzer.mutator.object import ObjectMutator
from fuzzer.mutator.array import ArrayMutator

class MutationEngine:
    def __init__(self, level: int, max_mutations: int):
        self.level = level
        self.max_mutations = max_mutations
        self.mutators = {
            "string": StringMutator(),
            "integer": NumericMutator(),
            "number": NumericMutator(),
            "boolean": BooleanMutator(),
			"array": ArrayMutator(),
            "object": ObjectMutator(),
        }

    def generate(self, target_schema: Schema) -> list[Any]:
        baseline = generate_valid_value(target_schema)

        if self.level == 0:
            return [baseline]

        mutator = self.mutators.get(target_schema.type)
        if not mutator:
            return [baseline]

        mutations = mutator.mutate(baseline, target_schema)
        return mutations[: self.max_mutations]
        # return [baseline] + mutations[: self.max_mutations]
