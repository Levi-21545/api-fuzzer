import json
from typing import Any, Iterable, Optional
from itertools import combinations
from copy import deepcopy

from fuzzer.model.schema import Schema, walk_schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.mutator.registry import get_mutators_for_schema
from fuzzer.mutator.mutation_operation import MutationCase, MutationOp


class MutationEngine:
    def __init__(
        self,
        level: int,
        max_mutations: Optional[int] = 10,
        max_pairs: Optional[int] = None,
    ):
        self.level = level
        self.max_mutations: Optional[int] = max_mutations
        self.max_pairs: Optional[int] = max_pairs

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
            payload = self.apply_mutation(baseline, op)
            if payload == baseline:
                continue
            cases.append(
                MutationCase(payload=payload, kind="mutation", operations=(op,))
            )
            mutation_count += 1

        if self.level == 1:
            return cases

        # Level 2: an independent budget of compatible mutation pairs.
        pair_cases = self._select_diverse_level2_cases(
            self.generate_level2_cases(baseline, level1_ops),
            self.max_pairs,
        )
        for case in pair_cases:
            cases.append(case)

        return cases

    def _select_diverse_level2_cases(
        self,
        cases: Iterable[MutationCase],
        limit: Optional[int],
    ) -> list[MutationCase]:
        unique_cases: list[MutationCase] = []
        seen_payloads: set[str] = set()
        for case in cases:
            payload_key = json.dumps(
                case.payload,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            if payload_key in seen_payloads:
                continue
            seen_payloads.add(payload_key)
            unique_cases.append(case)

        if limit is None or len(unique_cases) <= limit:
            return unique_cases
        if limit <= 0:
            return []

        selected: list[MutationCase] = []
        remaining = list(unique_cases)
        covered_paths: set[tuple[str, ...]] = set()
        covered_operators: set[str] = set()
        covered_path_pairs: set[tuple[tuple[str, ...], ...]] = set()
        covered_operator_pairs: set[tuple[str, ...]] = set()

        while remaining and len(selected) < limit:
            best_index = max(
                range(len(remaining)),
                key=lambda index: self._diversity_score(
                    remaining[index],
                    covered_paths,
                    covered_operators,
                    covered_path_pairs,
                    covered_operator_pairs,
                    index,
                ),
            )
            case = remaining.pop(best_index)
            selected.append(case)
            paths = {operation.path for operation in case.operations}
            operators = {operation.operator for operation in case.operations}
            covered_paths.update(paths)
            covered_operators.update(operators)
            covered_path_pairs.add(tuple(sorted(paths)))
            covered_operator_pairs.add(tuple(sorted(operators)))

        return selected

    @staticmethod
    def _diversity_score(
        case: MutationCase,
        covered_paths: set[tuple[str, ...]],
        covered_operators: set[str],
        covered_path_pairs: set[tuple[tuple[str, ...], ...]],
        covered_operator_pairs: set[tuple[str, ...]],
        index: int,
    ) -> tuple[int, int, int, int, int]:
        paths = {operation.path for operation in case.operations}
        operators = {operation.operator for operation in case.operations}
        path_pair = tuple(sorted(paths))
        operator_pair = tuple(sorted(operators))
        return (
            int(path_pair not in covered_path_pairs),
            len(paths - covered_paths),
            int(operator_pair not in covered_operator_pairs),
            len(operators - covered_operators),
            -index,
        )

    def generate_level1_mutations(self, schema: Schema) -> list[MutationOp]:
        mutations: list[MutationOp] = []

        for path, sub_schema in walk_schema(schema):
            if sub_schema.read_only:
                continue
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
            if payload == baseline:
                continue
            combined_payload = self.apply_mutation(payload, m2)
            if combined_payload == payload:
                continue

            yield MutationCase(
                payload=combined_payload,
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
            if isinstance(current, dict) and key in current:
                current = current[key]
                continue
            if isinstance(current, list) and key == "*" and current:
                current = current[0]
                continue
            return data

        leaf = mutation.path[-1]

        if mutation.op == "delete":
            if isinstance(current, dict):
                current.pop(leaf, None)
            elif isinstance(current, list) and leaf == "*" and current:
                current.pop(0)

        elif mutation.op == "replace":
            if isinstance(current, dict):
                current[leaf] = mutation.value
            elif isinstance(current, list) and leaf == "*" and current:
                current[0] = mutation.value

        return data
