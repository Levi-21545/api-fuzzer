from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class NumericMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        operations = [
            MutationOp(
                path,
                "replace",
                "not-a-number",
                operator="wrong_type",
                constraint="type",
            ),
        ]
        constraints = schema.constraints or {}

        if "minimum" in constraints:
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    constraints["minimum"] - 1,
                    operator="below_minimum",
                    constraint="minimum",
                )
            )

        if "maximum" in constraints:
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    constraints["maximum"] + 1,
                    operator="above_maximum",
                    constraint="maximum",
                )
            )

        if isinstance(constraints.get("exclusiveMinimum"), (int, float)) and not isinstance(
            constraints.get("exclusiveMinimum"), bool
        ):
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    constraints["exclusiveMinimum"],
                    operator="at_exclusive_minimum",
                    constraint="exclusiveMinimum",
                )
            )

        if isinstance(constraints.get("exclusiveMaximum"), (int, float)) and not isinstance(
            constraints.get("exclusiveMaximum"), bool
        ):
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    constraints["exclusiveMaximum"],
                    operator="at_exclusive_maximum",
                    constraint="exclusiveMaximum",
                )
            )

        multiple_of = constraints.get("multipleOf")
        if isinstance(multiple_of, (int, float)) and multiple_of > 0:
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    multiple_of / 2,
                    operator="multiple_of_violation",
                    constraint="multipleOf",
                )
            )

        return operations
