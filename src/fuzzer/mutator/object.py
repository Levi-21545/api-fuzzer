from fuzzer.model.schema import Schema
from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.base import Mutator


class ObjectMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        ops = [
            MutationOp(path, "replace", "not-an-object"),
            MutationOp(path, "replace", {}),
        ]

        for field in schema.required or []:
            ops.append(
                MutationOp(path + (field,), "delete")
            )

        return ops
