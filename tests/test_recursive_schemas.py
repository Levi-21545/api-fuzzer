"""Recursive schemas must stay bounded for generation, not for validation."""

import json
from copy import deepcopy

import pytest
from jsonschema import ValidationError, validate

from fuzzer.analysis.analyzer import Analyzer
from fuzzer.executor.result import ExecutionResult
from fuzzer.generator.valid_generator import (
    RecursiveGenerationError,
    generate_valid_value,
)
from fuzzer.model.schema import Schema, walk_schema
from fuzzer.mutator.array import ArrayMutator
from fuzzer.mutator.engine import MutationEngine
from fuzzer.parser.openapi_parser import OpenAPIParser
from fuzzer.utils.types import ExecutionPlanEntry


def node_schema():
    return {
        "type": "object",
        "required": ["name", "children"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "children": {
                "type": "array",
                "minItems": 0,
                "items": {"$ref": "#/components/schemas/Node"},
            },
        },
    }


def parse_schemas(tmp_path, schemas, root="Node"):
    body = {"application/json": {"schema": {"$ref": f"#/components/schemas/{root}"}}}
    raw = {
        "openapi": "3.0.1",
        "components": {"schemas": schemas},
        "paths": {
            "/tree": {
                "post": {
                    "requestBody": {"content": body},
                    "responses": {"200": {"content": body}},
                },
            },
        },
    }
    path = tmp_path / "contract.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    spec = OpenAPIParser(str(path)).parse()
    # Independent oracle: the original test schema, not its internal conversion.
    oracle = {
        "$ref": f"#/components/schemas/{root}",
        "components": raw["components"],
    }
    return spec, oracle


def tree(depth):
    result = {"name": "leaf", "children": []}
    for _ in range(depth):
        result = {"name": "branch", "children": [result]}
    return result


def test_self_reference_preserves_identity_and_full_validation(tmp_path):
    spec, oracle = parse_schemas(tmp_path, {"Node": node_schema()})
    endpoint = spec.endpoints[0]
    schema = endpoint.responses["200"]
    assert schema is endpoint.request_body.schema
    assert schema.properties["children"].items is schema
    converted = schema.to_jsonschema()
    assert converted["properties"]["children"]["items"] == {"$ref": "#"}

    valid = tree(8)
    validate(valid, oracle)
    validate(valid, converted)
    invalid = deepcopy(valid)
    child = invalid
    for _ in range(8):
        child = child["children"][0]
    child["name"] = 123
    for definition in (oracle, converted):
        with pytest.raises(ValidationError) as error:
            validate(invalid, definition)
        assert list(error.value.absolute_path) == ["children", 0] * 8 + ["name"]


def test_mutual_references_generate_and_validate_finite_values(tmp_path):
    schemas = {
        "Node": {
            "type": "object",
            "properties": {"other": {"$ref": "#/components/schemas/Other"}},
        },
        "Other": {
            "type": "object",
            "properties": {"back": {"$ref": "#/components/schemas/Node"}},
        },
    }
    spec, oracle = parse_schemas(tmp_path, schemas)
    schema = spec.endpoints[0].responses["200"]
    assert schema.properties["other"].properties["back"] is schema
    baseline = generate_valid_value(schema)
    assert len(json.dumps(baseline)) < 200
    validate(baseline, oracle)
    validate(baseline, schema.to_jsonschema())


def test_shared_nodes_are_visited_on_both_paths(tmp_path):
    schemas = {
        "Node": node_schema(),
        "Pair": {
            "type": "object",
            "properties": {
                "left": {"$ref": "#/components/schemas/Node"},
                "right": {"$ref": "#/components/schemas/Node"},
            },
        },
    }
    spec, oracle = parse_schemas(tmp_path, schemas, "Pair")
    schema = spec.endpoints[0].responses["200"]
    paths = [path for path, _ in walk_schema(schema)]
    assert ("left", "name") in paths
    assert ("right", "name") in paths
    assert ("left", "children", "*", "name") in paths
    assert ("right", "children", "*", "name") in paths
    assert len(paths) < 30
    baseline = generate_valid_value(schema)
    validate(baseline, oracle)
    validate(baseline, schema.to_jsonschema())


def test_reference_siblings_do_not_contaminate_other_uses(tmp_path):
    schemas = {
        "Text": {"type": "string", "minLength": 1},
        "Node": {
            "type": "object",
            "properties": {
                "short": {"$ref": "#/components/schemas/Text", "maxLength": 2},
                "long": {"$ref": "#/components/schemas/Text", "minLength": 5},
                "plain": {"$ref": "#/components/schemas/Text"},
            },
        },
    }
    spec, oracle = parse_schemas(tmp_path, schemas)
    schema = spec.endpoints[0].responses["200"]
    assert schema.properties["short"].constraints == {"minLength": 1, "maxLength": 2}
    assert schema.properties["long"].constraints == {"minLength": 5}
    assert schema.properties["plain"].constraints == {"minLength": 1}
    validate(generate_valid_value(schema), oracle)


def test_recursive_reference_siblings_remain_finite(tmp_path):
    schema = node_schema()
    schema["properties"]["children"]["items"]["description"] = "recursive child"
    spec, oracle = parse_schemas(tmp_path, {"Node": schema})
    parsed = spec.endpoints[0].responses["200"]
    validate(tree(4), parsed.to_jsonschema())
    validate(generate_valid_value(parsed), oracle)


def test_json_pointer_escapes_recursive_property_names():
    node = Schema(type="object", required=["name"])
    node.properties = {"name": Schema(type="string"), "next": node}
    root = Schema(type="object", properties={"a/~ b#é": node})
    converted = root.to_jsonschema()
    value = {"a/~ b#é": {"name": "a", "next": {"name": "b"}}}
    validate(value, converted)
    value["a/~ b#é"]["next"]["name"] = 0
    with pytest.raises(ValidationError):
        validate(value, converted)


def test_allof_can_contain_recursive_properties(tmp_path):
    node = node_schema()
    node["properties"].pop("name")
    schemas = {
        "Named": {
            "type": "object",
            "required": ["name"],
            "properties": {"name": {"type": "string", "minLength": 1}},
        },
        "Node": {"allOf": [{"$ref": "#/components/schemas/Named"}, node]},
    }
    spec, oracle = parse_schemas(tmp_path, schemas)
    schema = spec.endpoints[0].responses["200"]
    validate(tree(4), schema.to_jsonschema())
    validate(generate_valid_value(schema), oracle)


def test_recursive_single_allof_aliases_link_to_the_target(tmp_path):
    child = {"allOf": [{"$ref": "#/components/schemas/Node"}], "description": "child"}
    node = node_schema()
    node["properties"]["children"]["items"] = child
    spec, oracle = parse_schemas(
        tmp_path,
        {
            "Node": {"allOf": [{"$ref": "#/components/schemas/Branch"}]},
            "Branch": node,
        },
    )
    schema = spec.endpoints[0].responses["200"]
    assert schema.properties["children"].items is schema
    validate(tree(5), schema.to_jsonschema())
    validate(generate_valid_value(schema), oracle)


def test_recursive_allof_inheritance_fails_instead_of_dropping_constraints(tmp_path):
    schemas = {
        "Node": {
            "allOf": [
                {"$ref": "#/components/schemas/Node"},
                {"type": "object", "required": ["name"]},
            ]
        },
    }
    with pytest.raises(ValueError, match="Recursive allOf"):
        parse_schemas(tmp_path, schemas)


@pytest.mark.parametrize("root", ["Node", "Extended"])
def test_allof_inheritance_with_property_recursion_is_order_independent(tmp_path, root):
    schemas = {
        "Node": {
            "type": "object",
            "properties": {"child": {"$ref": "#/components/schemas/Extended"}},
        },
        "Extended": {
            "allOf": [
                {"$ref": "#/components/schemas/Node"},
                {
                    "type": "object",
                    "required": ["name"],
                    "properties": {"name": {"type": "string"}},
                },
            ],
        },
    }
    spec, oracle = parse_schemas(tmp_path, schemas, root)
    schema = spec.endpoints[0].responses["200"]
    value = {"child": {"name": "a", "child": {"name": "b"}}}
    if root == "Extended":
        value["name"] = "root"
    validate(value, oracle)
    validate(value, schema.to_jsonschema())
    validate(generate_valid_value(schema), oracle)
    del value["child"]["child"]["name"]
    for definition in (oracle, schema.to_jsonschema()):
        with pytest.raises(ValidationError):
            validate(value, definition)


def test_allof_mutual_inheritance_fails_explicitly(tmp_path):
    schemas = {
        "Node": {"allOf": [{"$ref": "#/components/schemas/Other"}, {"type": "object"}]},
        "Other": {"allOf": [{"$ref": "#/components/schemas/Node"}, {"type": "object"}]},
    }
    with pytest.raises(ValueError, match="Recursive allOf"):
        parse_schemas(tmp_path, schemas)


def test_yaml_allof_alias_cycle_fails_instead_of_looping(tmp_path):
    path = tmp_path / "anchors.yaml"
    path.write_text("components:\n  schemas:\n    Loop: &loop\n      allOf: [*loop]\n")
    parser = OpenAPIParser(str(path))
    with pytest.raises(ValueError, match="Cyclic.*allOf aliases"):
        parser._parse_schema(parser.raw["components"]["schemas"]["Loop"])


@pytest.mark.parametrize(
    "schemas, message",
    [
        ({"Node": {"$ref": "#/components/schemas/Node"}}, "Cyclic.*aliases"),
        (
            {
                "Node": {"$ref": "#/components/schemas/B"},
                "B": {"$ref": "#/components/schemas/Node"},
            },
            "Cyclic.*aliases",
        ),
        ({"Node": {"$ref": "#/components/schemas/Missing"}}, "Unresolvable"),
        ({"Node": {"$ref": "https://example.com/schema.json"}}, "Only local"),
        (
            {"Node": {"allOf": [{"$ref": "#/components/schemas/Node"}]}},
            "Cyclic.*aliases",
        ),
    ],
)
def test_unsupported_reference_cycles_fail_explicitly(tmp_path, schemas, message):
    with pytest.raises(ValueError, match=message):
        parse_schemas(tmp_path, schemas)


def test_recursive_baseline_is_finite_and_honors_required_children(tmp_path):
    spec, oracle = parse_schemas(tmp_path, {"Node": node_schema()})
    schema = spec.endpoints[0].request_body.schema
    value = generate_valid_value(schema)
    assert value == {"name": "A", "children": [{"name": "A", "children": []}]}
    validate(value, oracle)


def test_optional_recursive_property_can_be_omitted(tmp_path):
    schemas = {
        "Node": {
            "type": "object",
            "properties": {"next": {"$ref": "#/components/schemas/Node"}},
        }
    }
    spec, oracle = parse_schemas(tmp_path, schemas)
    value = generate_valid_value(spec.endpoints[0].request_body.schema)
    assert value == {"next": {}}
    validate(value, oracle)


@pytest.mark.parametrize("through_array", [False, True])
def test_required_recursion_without_supported_termination_fails(
    tmp_path, through_array
):
    child = {"$ref": "#/components/schemas/Node"}
    if through_array:
        child = {"type": "array", "items": child, "minItems": 1}
    spec, _ = parse_schemas(
        tmp_path,
        {
            "Node": {
                "type": "object",
                "required": ["next"],
                "properties": {"next": child},
            }
        },
    )
    schema = spec.endpoints[0].request_body.schema
    for level in (0, 1, 2):
        with pytest.raises(RecursiveGenerationError, match="finite value"):
            MutationEngine(level).generate_cases(schema)


async def test_unconstructible_endpoint_fails_mixed_plan_before_any_http(
    tmp_path, monkeypatch
):
    from fuzzer import main
    from fuzzer.cli.args import parse_args
    from fuzzer.orchestrator.runner import ExecutionRunner

    parse_schemas(
        tmp_path,
        {
            "Node": {
                "type": "object",
                "required": ["next"],
                "properties": {"next": {"$ref": "#/components/schemas/Node"}},
            }
        },
    )
    path = tmp_path / "contract.json"
    raw = json.loads(path.read_text())
    simple = deepcopy(raw["paths"]["/tree"])
    simple["post"]["requestBody"]["content"]["application/json"]["schema"] = {
        "type": "string",
    }
    raw["paths"] = {"/simple": simple, **raw["paths"]}
    path.write_text(json.dumps(raw))
    output = tmp_path / "runs"
    args = parse_args(
        [
            str(path),
            "--base-url",
            "http://127.0.0.1:1",
            "--all",
            "--output-dir",
            str(output),
            "--run-id",
            "mixed",
            "--level",
            "2",
        ]
    )
    monkeypatch.setattr(main, "parse_args", lambda: args)
    calls = []

    async def record_execution(*_args, **_kwargs):
        calls.append(True)
        return []

    monkeypatch.setattr(ExecutionRunner, "run", record_execution)
    with pytest.raises(RecursiveGenerationError):
        await main.async_main()
    assert not calls
    manifest = json.loads((output / "mixed" / "run_manifest.json").read_text())
    assert manifest["status"] == "failed"
    assert manifest["counts"]["selected_endpoints"] == 2
    # None is the existing manifest value for an execution not yet started.
    assert manifest["counts"]["completed_requests"] is None
    assert not (output / "mixed" / "data" / "results.json").exists()
    assert manifest["error"]["type"] == "RecursiveGenerationError"


def test_recursive_array_can_terminate_with_an_empty_array():
    schema = Schema(type="array")
    schema.items = schema
    value = generate_valid_value(schema)
    assert value == [[]]
    validate(value, schema.to_jsonschema())


def test_acyclic_depth_is_not_limited():
    schema = Schema(type="string")
    for _ in range(20):
        schema = Schema(type="object", properties={"next": schema}, required=["next"])
    value = generate_valid_value(schema)
    validate(value, schema.to_jsonschema())
    assert len(list(walk_schema(schema))) == 21


@pytest.mark.parametrize("level", [0, 1, 2])
def test_recursive_mutations_terminate_and_preserve_validity_labels(tmp_path, level):
    spec, oracle = parse_schemas(tmp_path, {"Node": node_schema()})
    cases = MutationEngine(level, max_mutations=6, max_pairs=3).generate_cases(
        spec.endpoints[0].request_body.schema
    )
    assert cases[0].kind == "baseline"
    assert len(cases) <= (1 if level == 0 else 7 if level == 1 else 10)
    for case in cases:
        assert len(json.dumps(case.payload)) < 5000
        if all(op.expected_valid for op in case.operations):
            validate(case.payload, oracle)
        else:
            with pytest.raises(ValidationError):
                validate(case.payload, oracle)


def test_array_mutator_skips_unconstructible_valid_items():
    item = Schema(type="object", required=["next"])
    item.properties["next"] = item
    array = Schema(type="array", items=item, max_items=1)
    assert generate_valid_value(array) == []
    operations = ArrayMutator().mutate((), array)
    assert operations
    assert not any(op.expected_valid for op in operations)
    cases = MutationEngine(2, max_mutations=6, max_pairs=3).generate_cases(array)
    assert cases[0].payload == []


def test_analyzer_and_fis_validate_deep_recursive_responses(tmp_path):
    spec, _ = parse_schemas(tmp_path, {"Node": node_schema()})
    endpoint = spec.endpoints[0]
    entry = ExecutionPlanEntry(
        endpoint=endpoint,
        path="/tree",
        payload=tree(0),
        headers={},
        case_id="case-1",
        case_kind="baseline",
    )
    body = tree(6)
    result = ExecutionResult(
        endpoint_id=endpoint.id,
        method=endpoint.method,
        url="http://localhost/tree",
        status_code=200,
        response_time_ms=1,
        response_size=1,
        raw_response=json.dumps(body),
        error=None,
        case_id="case-1",
    )
    analyzer = Analyzer(spec)
    assert analyzer.analyze_all([result], [entry]) == []
    leaf = body
    for _ in range(6):
        leaf = leaf["children"][0]
    del leaf["name"]
    result.raw_response = json.dumps(body)
    findings = analyzer.analyze_all([result], [entry])
    assert len(findings) == 1
    assert findings[0].classification.name == "SUCCESS_CONTRADICTION"
    assert findings[0].severity_assessment["inputs"]["behavior_contradiction"] == 0.65
