from typing import Any

from fuzzer.model.schema import Schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.base import Mutator as BaseMutator


class ArrayMutator(BaseMutator):
    """
    Mutations for array schemas.
    Focuses on size constraints, item validity and structure.
    """

    def mutate(self, baseline: Any, schema: Schema) -> list[Any]:
        mutations: list[Any] = []

        item_schema = schema.items
        min_items = schema.min_items or 0
        max_items = schema.max_items

        # Garantir baseline utilizável
        if isinstance(baseline, list):
            base_array = list(baseline)
        else:
            base_array = []

        # 1. Baseline como mutação válida
        if base_array:
            mutations.append(base_array)

        # 2. Array mínimo válido
        if item_schema:
            size = max(min_items, 1)
            mutations.append(
                [generate_valid_value(item_schema) for _ in range(size)]
            )

        # 3. Violação: array vazio
        if min_items > 0:
            mutations.append([])

        # 4. Violação: array grande demais
        if max_items is not None and item_schema:
            mutations.append(
                [generate_valid_value(item_schema) for _ in range(max_items + 1)]
            )

        # 5. Violação: item com tipo inválido
        if item_schema:
            mutated = list(base_array) or [generate_valid_value(item_schema)]
            mutated[0] = self._invalid_value_for(item_schema)
            mutations.append(mutated)

        # 6. Violação: item nulo
        if base_array:
            mutated = list(base_array)
            mutated[0] = None
            mutations.append(mutated)
        elif item_schema:
            mutations.append([None])

        # 7. Violação estrutural
        mutations.append({"not": "an array"})

        return mutations
