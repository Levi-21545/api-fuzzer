from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class NumericMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        return [
            MutationOp(path, "replace", -1),
            MutationOp(path, "replace", 0),
            MutationOp(path, "replace", "NaN"),
            MutationOp(path, "delete"),
        ]
