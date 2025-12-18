from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class StringMutator(Mutator):
    def mutate(self, value: str, schema: Schema) -> list[str]:
        mutations = []

        if value is None:
            return mutations

        mutations.append("")                      # vazio
        mutations.append(value * 10)              # muito longo
        mutations.append(value + "\x00")          # null byte
        mutations.append("A" * 1024)               # overflow-like

        if schema.enum:
            mutations.append("INVALID_ENUM")

        return mutations
