from fuzzer.model.schema import Schema
from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.base import Mutator


class ObjectMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        ops = [
            MutationOp(
                path,
                "replace",
                "not-an-object",
                operator="wrong_type",
                constraint="type",
            ),
            MutationOp(
                path,
                "replace",
                {},
                operator="empty_object",
                constraint="required" if schema.required else None,
                expected_valid=not bool(schema.required),
            ),
        ]

        for field in schema.required or []:
            ops.append(
                MutationOp(
                    path + (field,),
                    "delete",
                    operator="remove_required_property",
                    constraint="required",
                )
            )

        return ops
