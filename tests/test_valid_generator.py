from datetime import date

from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.model.schema import Schema


def test_string():
    s = Schema(type="string")
    val = generate_valid_value(s)
    assert isinstance(val, str)
    assert len(val) >= 1


def test_string_with_enum():
    s = Schema(type="string", constraints={"enum": ["foo", "bar"]})
    assert generate_valid_value(s) == "foo"


def test_string_uuid_format():
    s = Schema(type="string", format="uuid")
    val = generate_valid_value(s)
    assert isinstance(val, str)
    assert len(val) == 36


def test_string_email_format():
    s = Schema(type="string", format="email")
    val = generate_valid_value(s)
    assert "@" in val


def test_string_date_format():
    s = Schema(type="string", format="date")
    val = generate_valid_value(s)
    assert date.fromisoformat(val) == date(2000, 1, 1)


def test_integer():
    s = Schema(type="integer")
    val = generate_valid_value(s)
    assert val == 0


def test_integer_with_minimum():
    s = Schema(type="integer", constraints={"minimum": 10})
    val = generate_valid_value(s)
    assert val == 10


def test_number():
    s = Schema(type="number")
    val = generate_valid_value(s)
    assert isinstance(val, float)
    assert val == 0.0


def test_boolean():
    s = Schema(type="boolean")
    assert generate_valid_value(s) is True


def test_array():
    s = Schema(type="array", items=Schema(type="string"))
    val = generate_valid_value(s)
    assert isinstance(val, list)
    assert len(val) == 1
    assert isinstance(val[0], str)


def test_object():
    s = Schema(
        type="object",
        properties={
            "name": Schema(type="string"),
            "age": Schema(type="integer"),
        },
        required=["name"],
    )
    val = generate_valid_value(s)
    assert isinstance(val, dict)
    assert "name" in val
    assert "age" not in val


def test_object_omits_read_only_properties_from_request_baseline():
    s = Schema(
        type="object",
        properties={
            "name": Schema(type="string"),
            "id": Schema(type="integer", read_only=True),
        },
        required=["name", "id"],
    )

    assert generate_valid_value(s) == {"name": "A"}


def test_none_type():
    s = Schema(type=None)
    assert generate_valid_value(s) is None
