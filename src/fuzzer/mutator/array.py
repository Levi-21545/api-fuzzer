from typing import Any

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
        min_items = schema.min_items or 0
        max_items = schema.max_items

        # 1. Array válido mínimo
        valid_size = max(min_items, 1)
        valid_array = (
            [generate_valid_value(item_schema) for _ in range(valid_size)]
            if item_schema
            else []
        )

        mutations.append(
            MutationOp(
                path=path,
                op="replace",
                value=valid_array,
            )
        )

        # 2. Array vazio (se viola minItems)
        if min_items > 0:
            mutations.append(
                MutationOp(
                    path=path,
                    op="replace",
                    value=[],
                )
            )

        # 3. Array grande demais
        if max_items is not None and item_schema:
            oversized = [
                generate_valid_value(item_schema)
                for _ in range(max_items + 1)
            ]
            mutations.append(
                MutationOp(
                    path=path,
                    op="replace",
                    value=oversized,
                )
            )

        # 4. Item com tipo inválido
        if item_schema:
            mutations.append(
                MutationOp(
                    path=path,
                    op="replace",
                    value=[self._invalid_value_for(item_schema)],
                )
            )

        # 5. Array com null
        mutations.append(
            MutationOp(
                path=path,
                op="replace",
                value=[None],
            )
        )

        # 6. Estrutura errada
        mutations.append(
            MutationOp(
                path=path,
                op="replace",
                value={"not": "an array"},
            )
        )

        return mutations
