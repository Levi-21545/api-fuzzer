from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class BooleanMutator(Mutator):
    def mutate(self, value: bool, schema: Schema):
        return [not value, None]
