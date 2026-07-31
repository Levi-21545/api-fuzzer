from typing import Any, Iterable, Optional
from itertools import combinations
from copy import deepcopy

from fuzzer.model.schema import Schema, walk_schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.registry import get_mutators_for_schema
from fuzzer.mutator.mutation_operation import MutationCase, MutationOp


class MutationEngine:
    def __init__(self, level: int, max_mutations: Optional[int] = 10):
        self.level = level
        self.max_mutations: Optional[int] = max_mutations

    def generate(self, target_schema: Schema) -> list[Any]:
        return [case.payload for case in self.generate_cases(target_schema)]

    def generate_cases(self, target_schema: Schema) -> list[MutationCase]:
        baseline = generate_valid_value(target_schema)

        # Level 0: baseline only.
        if self.level == 0:
            return [MutationCase(payload=baseline, kind="baseline")]

        level1_ops = self.generate_level1_mutations(target_schema)

        cases: list[MutationCase] = [
            MutationCase(payload=baseline, kind="baseline"),
        ]
        mutation_count = 0

        # Level 1: one mutation per case.
        for op in level1_ops:
            if (
                self.max_mutations is not None
                and mutation_count >= self.max_mutations
            ):
                break
            cases.append(
                MutationCase(
                    payload=self.apply_mutation(baseline, op),
                    kind="mutation",
                    operations=(op,),
                )
            )
            mutation_count += 1

        if self.level == 1:
            return cases

        # Level 2: explicit pairs of compatible mutations.
        for case in self.generate_level2_cases(baseline, level1_ops):
            if (
                self.max_mutations is not None
                and mutation_count >= self.max_mutations
            ):
                break
            cases.append(case)
            mutation_count += 1

        return cases

    def generate_level1_mutations(self, schema: Schema) -> list[MutationOp]:
        mutations: list[MutationOp] = []

        for path, sub_schema in walk_schema(schema):
            for mutator in get_mutators_for_schema(sub_schema):
                mutations.extend(
                    mutator.mutate(path, sub_schema)
                )

        return mutations

    def generate_level2_cases(
        self,
        baseline: Any,
        mutations: list[MutationOp],
    ) -> Iterable[MutationCase]:

        for m1, m2 in combinations(mutations, 2):

            if not m1.path or not m2.path:
                continue  # Root mutations cannot be combined safely.

            # Skip mutations targeting the same path.
            if m1.path == m2.path:
                continue

            # Avoid direct parent-child structural conflicts.
            if (
                m1.path[: len(m2.path)] == m2.path
                or m2.path[: len(m1.path)] == m1.path
            ):
                continue

            payload = self.apply_mutation(baseline, m1)
            payload = self.apply_mutation(payload, m2)

            yield MutationCase(
                payload=payload,
                kind="mutation",
                operations=(m1, m2),
            )

    def apply_mutation(self, payload: Any, mutation: MutationOp) -> Any:
        # Root replacement is the only meaningful root mutation.
        if not mutation.path:
            if mutation.op == "replace":
                return mutation.value
            return payload  # Deleting the root payload is not meaningful.

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
