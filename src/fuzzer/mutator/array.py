from typing import Any

from fuzzer.model.schema import Schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.base import Mutator as BaseMutator


class ArrayMutator(BaseMutator):
    """
    Mutations for array schemas.
    Focuses on size constraints and item validity.
    """

    def mutate(self, schema: Schema) -> list[Any]:
        mutations: list[Any] = []

        item_schema = schema.items
        if not item_schema:
            return [[]]

        min_items = schema.min_items or 0
        max_items = schema.max_items

        # 1. Array válido mínimo
        valid_size = max(min_items, 1)
        valid_array = [
            generate_valid_value(item_schema)
            for _ in range(valid_size)
        ]
        mutations.append(valid_array)

        # 2. Array vazio (se viola minItems)
        if min_items > 0:
            mutations.append([])

        # 3. Array grande demais (se maxItems existir)
        if max_items is not None:
            oversized = [
                generate_valid_value(item_schema)
                for _ in range(max_items + 1)
            ]
            mutations.append(oversized)

        # 4. Item com tipo inválido
        invalid_item = self._invalid_value_for(item_schema)
        mutations.append([invalid_item])

        # 5. Item null
        mutations.append([None])

        # 6. Estrutura errada (objeto no lugar de array)
        mutations.append({"not": "an array"})

        return mutations
