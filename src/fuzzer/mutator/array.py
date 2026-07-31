from fuzzer.model.schema import Schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.base import Mutator
from fuzzer.mutator.mutation_operation import MutationOp


class ArrayMutator(Mutator):
    """
    Mutations for array schemas.
    Focuses on size constraints and item validity.
    """

    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        mutations: list[MutationOp] = []

        item_schema = schema.items
        if item_schema is None:
            return []

        min_items = schema.min_items
        max_items = schema.max_items

        min_items = min_items if isinstance(min_items, int) else 0

        # 1. Smallest valid non-empty array.
        size = max(min_items, 1)
        mutations.append(
            MutationOp(
                path=path,
                op="replace",
                value=[generate_valid_value(item_schema) for _ in range(size)],
                operator="minimum_valid_size",
                constraint="minItems" if min_items > 0 else None,
                expected_valid=True,
            )
        )

        # 2. Empty array when it violates minItems.
        if min_items > 0:
            mutations.append(
                MutationOp(
                    path=path,
                    op="replace",
                    value=[],
                    operator="below_min_items",
                    constraint="minItems",
                )
            )

        # 3. Array larger than maxItems.
        if isinstance(max_items, int):
            oversized = [
                generate_valid_value(item_schema)
                for _ in range(max_items + 1)
            ]
            mutations.append(
                MutationOp(
                    path=path,
                    op="replace",
                    value=oversized,
                    operator="above_max_items",
                    constraint="maxItems",
                )
            )

        # 4. Item with an invalid type.
        if item_schema:
            mutations.append(
                MutationOp(
                    path=path,
                    op="replace",
                    value=[self._invalid_value_for(item_schema)],
                    operator="invalid_item_type",
                    constraint="items.type",
                )
            )

        # 5. Array containing null.
        mutations.append(
            MutationOp(
                path=path,
                op="replace",
                value=[None],
                operator="null_item",
                constraint="items.type",
            )
        )

        # 6. Value with the wrong container type.
        mutations.append(
            MutationOp(
                path=path,
                op="replace",
                value={"not": "an array"},
                operator="wrong_type",
                constraint="type",
            )
        )

        return mutations
