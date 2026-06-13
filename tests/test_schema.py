from fuzzer.model.schema import Schema, walk_schema


def test_schema_defaults():
    s = Schema(type="string")
    assert s.type == "string"
    assert s.format is None
    assert s.constraints == {}
    assert s.properties == {}
    assert s.items is None
    assert s.required == []


def test_to_jsonschema_simple(string_schema):
    js = string_schema.to_jsonschema()
    assert js == {"type": "string"}


def test_to_jsonschema_with_constraints():
    s = Schema(type="string", constraints={"minLength": 1, "maxLength": 10})
    js = s.to_jsonschema()
    assert js["minLength"] == 1
    assert js["maxLength"] == 10


def test_to_jsonschema_with_enum():
    s = Schema(type="string", constraints={"enum": ["a", "b", "c"]})
    js = s.to_jsonschema()
    assert js["enum"] == ["a", "b", "c"]


def test_to_jsonschema_object(object_schema):
    js = object_schema.to_jsonschema()
    assert js["type"] == "object"
    assert "properties" in js
    assert "name" in js["properties"]
    assert "age" in js["properties"]
    assert js["required"] == ["name"]


def test_to_jsonschema_array(array_schema):
    js = array_schema.to_jsonschema()
    assert js["type"] == "array"
    assert js["items"] == {"type": "string"}


def test_to_jsonschema_array_with_bounds():
    s = Schema(type="array", items=Schema(type="integer"), min_items=1, max_items=10)
    js = s.to_jsonschema()
    assert js["minItems"] == 1
    assert js["maxItems"] == 10


def test_to_jsonschema_nested(nested_schema):
    js = nested_schema.to_jsonschema()
    assert js["type"] == "object"
    assert js["properties"]["user"]["type"] == "object"
    assert js["properties"]["user"]["properties"]["email"]["format"] == "email"
    assert js["properties"]["user"]["properties"]["roles"]["type"] == "array"


def test_to_jsonschema_none_type():
    s = Schema(type=None)
    assert s.to_jsonschema() == {}


def test_walk_schema_flat(string_schema):
    paths = list(walk_schema(string_schema))
    assert len(paths) == 1
    assert paths[0] == ((), string_schema)


def test_walk_schema_object(object_schema):
    paths = list(walk_schema(object_schema))
    assert len(paths) == 3
    assert paths[0] == ((), object_schema)
    assert paths[1][0] == ("name",)
    assert paths[1][1].type == "string"
    assert paths[2][0] == ("age",)
    assert paths[2][1].type == "integer"


def test_walk_schema_nested(nested_schema):
    paths = list(walk_schema(nested_schema))
    assert len(paths) == 5
    path_names = [p for p, _ in paths]
    assert ("user",) in path_names
    assert ("user", "email") in path_names
    assert ("user", "roles") in path_names
    assert ("user", "roles", "*") in path_names
