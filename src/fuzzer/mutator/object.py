from typing import Any

from fuzzer.model.schema import Schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.base import Mutator as BaseMutator


class ObjectMutator(BaseMutator):
    """
    Mutations for object schemas.
    Focuses on structural and semantic violations.
    """

    def mutate(self, baseline: Any, schema: Schema) -> list[Any]:
        mutations: list[Any] = []

        if not schema.properties:
            return [{}]

        # Baseline utilizável
        if isinstance(baseline, dict):
            base_object = dict(baseline)
        else:
            base_object = {
                name: generate_valid_value(prop_schema)
                for name, prop_schema in schema.properties.items()
                if not schema.required or name in schema.required
            }

        # 1. Baseline
        mutations.append(base_object)
        
        required_fields = set(schema.required or [])

        # 2. Remoção de campo obrigatório (um por vez)
        for field in required_fields:
            if field in base_object:
                mutated = dict(base_object)
                mutated.pop(field)
                mutations.append(mutated)

        # 3. Campo com tipo inválido
        for field, prop_schema in schema.properties.items():
            if field in base_object:
                mutated = dict(base_object)
                mutated[field] = self._invalid_value_for(prop_schema)
                mutations.append(mutated)

        # 4. Campo extra inesperado
        mutated = dict(base_object)
        mutated["__unexpected__"] = "unexpected"
        mutations.append(mutated)

        # 5. Objeto vazio
        mutations.append({})

        # 6. Violação estrutural
        mutations.append("not-an-object")

        return mutations