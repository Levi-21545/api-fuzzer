from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class StringMutator(Mutator):
    def mutate(self, baseline: str, schema: Schema) -> list[str]:
        mutations = []

        if baseline is None:
            return mutations

        mutations.append("")                      # vazio
        mutations.append(baseline * 10)           # muito longo
        mutations.append(baseline + "\x00")       # null byte
        mutations.append("A" * 1024)              # overflow-like

        if schema.enum:
            mutations.append("INVALID_ENUM")

        return mutations
