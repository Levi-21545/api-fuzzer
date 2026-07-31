from abc import ABC, abstractmethod
from typing import Any

from fuzzer.model.schema import Schema
from fuzzer.mutator.mutation_operation import MutationOp


class Mutator(ABC):
    @abstractmethod
    def mutate(
        self,
        path: tuple[str, ...],
        schema: Schema,
    ) -> list[MutationOp]:
        ...

    def _invalid_value_for(self, schema: Schema) -> Any:
        """
        Generate a value that violates the schema type.
        """
        if schema.type == "string":
            return 123

        if schema.type in ("integer", "number"):
            return "not-a-number"

        if schema.type == "boolean":
            return "true"

        if schema.type == "array":
            return {}

        if schema.type == "object":
            return "not-an-object"

        return None
