from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class NumericMutator(Mutator):
    def mutate(self, baseline: int | float, schema: Schema) -> list[int | float]:
        mutations = []

        if baseline is None:
            return mutations

        mutations.extend([
            -1,
            0,
            baseline + 1,
            baseline - 1,
            2**31,
        ])

        return mutations
