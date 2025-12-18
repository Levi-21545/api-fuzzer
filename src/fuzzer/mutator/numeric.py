from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class NumericMutator(Mutator):
    def mutate(self, value: int | float, schema: Schema) -> list[int | float]:
        mutations = []

        if value is None:
            return mutations

        mutations.extend([
            -1,
            0,
            value + 1,
            value - 1,
            2**31,
        ])

        return mutations
