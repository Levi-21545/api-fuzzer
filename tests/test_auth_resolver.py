import yaml
from pathlib import Path

from fuzzer.orchestrator.auth_resolver import _build_headers_from_config, resolve_auth_headers


def test_build_headers_static():
    cfg = {"Authorization": "Bearer static-token"}
    result = _build_headers_from_config(cfg)
    assert result == {"Authorization": "Bearer static-token"}


def test_build_headers_with_template():
    cfg = {"Authorization": "Bearer {token}"}
    result = _build_headers_from_config(cfg, {"token": "abc123"})
    assert result == {"Authorization": "Bearer abc123"}


async def test_static_token_no_login(tmp_path):
    auth_file = tmp_path / "auth.yaml"
    auth_file.write_text(yaml.dump({
        "auth": {
            "inject": {
                "headers": {
                    "Authorization": "Bearer static-token"
                }
            }
        }
    }))
    result = await resolve_auth_headers(auth_file)
    assert result == {"Authorization": "Bearer static-token"}


async def test_disabled_returns_empty(tmp_path):
    auth_file = tmp_path / "auth.yaml"
    auth_file.write_text(yaml.dump({
        "auth": {
            "enabled": False,
            "inject": {
                "headers": {
                    "Authorization": "Bearer should-not-appear"
                }
            }
        }
    }))
    result = await resolve_auth_headers(auth_file)
    assert result == {}


async def test_no_auth_section_raises(tmp_path):
    auth_file = tmp_path / "auth.yaml"
    auth_file.write_text(yaml.dump({"other": "data"}))
    import pytest
    with pytest.raises(ValueError, match="No 'auth' section"):
        await resolve_auth_headers(auth_file)
