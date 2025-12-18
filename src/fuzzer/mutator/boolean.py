from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema


class BooleanMutator(Mutator):
    def mutate(self, baseline: bool, schema: Schema):
        return [not baseline, None]
