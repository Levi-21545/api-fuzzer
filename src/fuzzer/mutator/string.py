from fuzzer.mutator.mutation_operation import MutationOp
from fuzzer.mutator.base import Mutator
from fuzzer.model.schema import Schema
from fuzzer.utils.patterns import compile_openapi_pattern


class StringMutator(Mutator):
    def mutate(self, path: tuple[str, ...], schema: Schema) -> list[MutationOp]:
        operations = [
            MutationOp(
                path,
                "replace",
                123,
                operator="wrong_type",
                constraint="type",
            ),
        ]

        constraints = schema.constraints or {}

        enum = constraints.get("enum")
        if isinstance(enum, list) and enum:
            invalid_enum = "__contract_fuzzer_not_in_enum__"
            while invalid_enum in enum:
                invalid_enum += "_x"
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    invalid_enum,
                    operator="enum_violation",
                    constraint="enum",
                )
            )

        min_length = constraints.get("minLength")
        if isinstance(min_length, int) and min_length > 0:
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    "A" * (min_length - 1),
                    operator="below_min_length",
                    constraint="minLength",
                )
            )

        max_length = constraints.get("maxLength")
        if isinstance(max_length, int) and 0 <= max_length < 10_000:
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    "A" * (max_length + 1),
                    operator="above_max_length",
                    constraint="maxLength",
                )
            )

        pattern = constraints.get("pattern")
        mismatch = self._pattern_mismatch(pattern)
        if mismatch is not None:
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    mismatch,
                    operator="pattern_mismatch",
                    constraint="pattern",
                )
            )

        invalid_formats = {
            "uuid": "not-a-uuid",
            "email": "not-an-email",
            "date": "not-a-date",
            "date-time": "not-a-date-time",
        }
        invalid_format = (
            invalid_formats.get(schema.format)
            if schema.format is not None
            else None
        )

        if invalid_format is not None:
            operations.append(
                MutationOp(
                    path,
                    "replace",
                    invalid_format,
                    operator="format_violation",
                    constraint="format",
                )
            )

        return operations

    @staticmethod
    def _pattern_mismatch(pattern: object) -> str | None:
        if not isinstance(pattern, str):
            return None
        try:
            compiled = compile_openapi_pattern(pattern)
        except ValueError:
            return None

        for candidate in ("", "__contract_fuzzer_pattern_mismatch__", "!!!", "0"):
            if compiled.search(candidate) is None:
                return candidate
        return None
