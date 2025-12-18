from fuzzer.model.schema import Schema
from fuzzer.mutator.base import Mutator
from fuzzer.mutator.mutation_operation import MutationOp


class BooleanMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        return [
            # Inversão lógica
            MutationOp(
                path=path,
                op="replace",
                value=False,
            ),
            # Null
            MutationOp(
                path=path,
                op="replace",
                value=None,
            ),
            # Tipo inválido
            MutationOp(
                path=path,
                op="replace",
                value="not-a-boolean",
            ),
        ]
