from fuzzer.model.schema import Schema
from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.base import Mutator


class ObjectMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        writable_required = [
            field
            for field in schema.required
            if field not in schema.properties
            or not schema.properties[field].read_only
        ]
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
                constraint="required" if writable_required else None,
                expected_valid=not bool(writable_required),
            ),
        ]

        for field in writable_required:
            ops.append(
                MutationOp(
                    path + (field,),
                    "delete",
                    operator="remove_required_property",
                    constraint="required",
                )
            )

        return ops
