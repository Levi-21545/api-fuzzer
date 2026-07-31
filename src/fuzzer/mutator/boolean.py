from fuzzer.model.schema import Schema
from fuzzer.mutator.base import Mutator
from fuzzer.mutator.mutation_operation import MutationOp


class BooleanMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        return [
            # Alternate valid boolean value.
            MutationOp(
                path=path,
                op="replace",
                value=False,
                operator="alternate_boolean",
                expected_valid=True,
            ),
            # Null violates a non-nullable boolean schema.
            MutationOp(
                path=path,
                op="replace",
                value=None,
                operator="null_value",
                constraint="type",
            ),
            # String value violates the declared type.
            MutationOp(
                path=path,
                op="replace",
                value="not-a-boolean",
                operator="wrong_type",
                constraint="type",
            ),
        ]
