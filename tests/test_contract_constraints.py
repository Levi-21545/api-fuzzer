import pytest
from jsonschema import ValidationError, validate

from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.model.schema import Schema
from fuzzer.mutator.numeric import NumericMutator
from fuzzer.mutator.string import StringMutator
from fuzzer.mutator.engine import MutationEngine


def test_string_baseline_honors_length_and_numeric_pattern():
    schema = Schema(
        type="string",
        constraints={
            "minLength": 1,
            "maxLength": 8,
            "pattern": r"^\d{0,18}(\.\d{0,2})?$",
        },
    )
    value = generate_valid_value(schema)
    validate(value, schema.to_jsonschema())


def test_java_unicode_letter_pattern_is_supported():
    schema = Schema(
        type="string",
        constraints={"pattern": r"^[\p{L}]+([ '-][\p{L}]+){0,2}$"},
    )
    value = generate_valid_value(schema)
    validate(value, schema.to_jsonschema())


def test_string_mutations_name_violated_constraints():
    schema = Schema(
        type="string",
        constraints={
            "minLength": 2,
            "maxLength": 4,
            "pattern": r"^[0-9]*$",
            "enum": ["12"],
        },
    )
    operations = StringMutator().mutate(("code",), schema)
    constraints = {operation.constraint for operation in operations}
    assert {"type", "enum", "minLength", "maxLength", "pattern"} <= constraints


def test_numeric_mutations_cover_bounds_and_multiple_of():
    schema = Schema(
        type="integer",
        constraints={"minimum": 10, "maximum": 20, "multipleOf": 2},
    )
    baseline = generate_valid_value(schema)
    validate(baseline, schema.to_jsonschema())

    operations = NumericMutator().mutate(("quantity",), schema)
    constraints = {operation.constraint for operation in operations}
    assert {"type", "minimum", "maximum", "multipleOf"} <= constraints


def test_mutation_level_always_includes_a_baseline_case():
    schema = Schema(
        type="object",
        properties={"name": Schema(type="string")},
        required=["name"],
    )

    cases = MutationEngine(level=1, max_mutations=1).generate_cases(schema)

    assert cases[0].kind == "baseline"
    assert cases[0].operations == ()
    assert cases[1].kind == "mutation"


def test_nested_array_item_mutation_changes_the_generated_payload():
    schema = Schema(
        type="object",
        properties={
            "tags": Schema(
                type="array",
                items=Schema(type="string"),
                min_items=1,
            ),
        },
        required=["tags"],
    )

    cases = MutationEngine(level=1, max_mutations=None).generate_cases(schema)
    item_type_case = next(
        case
        for case in cases
        if case.operations
        and case.operations[0].path == ("tags", "*")
        and case.operations[0].operator == "wrong_type"
    )

    assert item_type_case.payload["tags"] == [123]
    with pytest.raises(ValidationError):
        validate(item_type_case.payload, schema.to_jsonschema())
