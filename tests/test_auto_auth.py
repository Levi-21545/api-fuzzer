from fuzzer.orchestrator.auto_auth import (
    _build_auth_context,
    _login_identity_values,
)


def test_login_identity_preserves_registered_username_and_email():
    credentials = {
        "username": "fuzzer_original",
        "password": "secret",
        "email": "original@example.com",
    }
    registration = {
        "username": "username_generated",
        "password": "secret",
        "email": "registered@example.com",
    }

    values = _login_identity_values(registration, credentials)

    assert values["username"] == "username_generated"
    assert values["email"] == "registered@example.com"


def test_auth_context_uses_the_registered_path_identity():
    credentials = {
        "username": "fuzzer_original",
        "password": "secret",
        "email": "original@example.com",
    }
    registration = {
        "username": "username_generated",
        "password": "secret",
        "email": "registered@example.com",
    }

    context = _build_auth_context(registration, credentials)

    assert context["username"] == "username_generated"
    assert context["email"] == "registered@example.com"
    assert context["user_id"] == "username_generated"
