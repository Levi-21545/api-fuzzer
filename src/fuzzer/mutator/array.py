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
        if item_schema is None:
            return []

        min_items = getattr(schema, "minItems", None)
        max_items = getattr(schema, "maxItems", None)

        min_items = min_items if isinstance(min_items, int) else 0

        # 1. array válido mínimo
        size = max(min_items, 1)
        mutations.append(
            MutationOp(
                path=path,
                op="replace",
                value=[generate_valid_value(item_schema) for _ in range(size)],
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
