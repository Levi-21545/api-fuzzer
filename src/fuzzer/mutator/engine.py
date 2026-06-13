from typing import Any, Iterable, Optional
from itertools import combinations
from copy import deepcopy

from fuzzer.model.schema import Schema, walk_schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.registry import get_mutators_for_schema
from fuzzer.mutator.mutation_operation import MutationOp


class MutationEngine:
    def __init__(self, level: int, max_mutations: Optional[int] = 20):
        self.level = level
        self.max_mutations: Optional[int] = max_mutations

    def generate(self, target_schema: Schema) -> list[Any]:
        baseline = generate_valid_value(target_schema)

        # Level 0
        if self.level == 0:
            return [baseline]

        level1_ops = self.generate_level1_mutations(target_schema)

        payloads: list[Any] = []

        # Level 1 — mutações unitárias
        for op in level1_ops:
            payloads.append(
                self.apply_mutation(baseline, op)
            )

        if self.level == 1:
            return payloads[: self.max_mutations]

        # Level 2 — combinações explícitas
        for payload in self.generate_level2_payloads(baseline, level1_ops):
            payloads.append(payload)

            if self.max_mutations is not None and len(payloads) >= self.max_mutations:
                break

        return payloads

    def generate_level1_mutations(self, schema: Schema) -> list[MutationOp]:
        mutations: list[MutationOp] = []

        for path, sub_schema in walk_schema(schema):
            for mutator in get_mutators_for_schema(sub_schema):
                mutations.extend(
                    mutator.mutate(path, sub_schema)
                )

        return mutations

    def generate_level2_payloads(
        self,
        baseline: dict,
        mutations: list[MutationOp],
    ) -> Iterable[Any]:

        for m1, m2 in combinations(mutations, 2):

            if not m1.path or not m2.path:
                continue  # ignora mutações de raiz em combinações

            # caminhos iguais → ignora
            if m1.path == m2.path:
                continue

            # evita conflitos estruturais diretos
            if (
                m1.path[: len(m2.path)] == m2.path
                or m2.path[: len(m1.path)] == m1.path
            ):
                continue

            payload = self.apply_mutation(baseline, m1)
            payload = self.apply_mutation(payload, m2)

            yield payload

    def apply_mutation(self, payload: dict, mutation: MutationOp) -> dict:
        # Caso especial: mutação na raiz
        if not mutation.path:
            if mutation.op == "replace":
                return mutation.value
            return payload  # delete na raiz não faz sentido

        data = deepcopy(payload)
        current = data

        for key in mutation.path[:-1]:
            if not isinstance(current, dict) or key not in current:
                return data
            current = current[key]

        leaf = mutation.path[-1]

        if mutation.op == "delete":
            if isinstance(current, dict):
                current.pop(leaf, None)

        elif mutation.op == "replace":
            if isinstance(current, dict):
                current[leaf] = mutation.value

        return data
