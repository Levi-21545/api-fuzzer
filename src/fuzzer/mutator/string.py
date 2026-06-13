from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class StringMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        return [
            MutationOp(path, "replace", ""),
            MutationOp(path, "replace", "A" * 500),
            MutationOp(path, "replace", 123),
            MutationOp(path, "delete"),
        ]
