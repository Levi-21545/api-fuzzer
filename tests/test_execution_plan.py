from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.model.parameter import Parameter
from fuzzer.model.request_body import RequestBody
from fuzzer.model.schema import Schema
from fuzzer.mutator.engine import MutationEngine
from fuzzer.orchestrator.execution_plan_builder import (
    build_execution_plan,
    build_auth_probes,
)
from fuzzer.utils.types import Headers, AuthContext


def _ep(
    path: str = "/test",
    method: HttpMethod = HttpMethod.GET,
    security: bool = False,
    has_body: bool = False,
    params: list | None = None,
) -> Endpoint:
    body = (
        RequestBody(
            content_type="application/json",
            schema=Schema(type="object", properties={"x": Schema(type="string")}),
        )
        if has_body
        else None
    )
    return Endpoint(
        path=path,
        method=method,
        parameters=params or [],
        request_body=body,
        responses={},
        security=[{"bearerAuth": []}] if security else None,
    )


def _engine() -> MutationEngine:
    return MutationEngine(level=0, max_mutations=0)


# ── build_execution_plan ──────────────────────────────────────────────


def test_injects_auth_headers_on_auth_endpoints():
    ep_pub = _ep(path="/public", security=False, has_body=True)
    ep_auth = _ep(path="/secret", security=True, has_body=True)
    plan = list(build_execution_plan([ep_pub, ep_auth], _engine(), auth_headers={"Authorization": "Bearer x"}))

    pub_entry = [e for e in plan if e[0].path == "/public"]
    assert len(pub_entry) == 1
    _, _, _, pub_hdrs = pub_entry[0]
    assert "Authorization" not in pub_hdrs

    auth_entry = [e for e in plan if e[0].path == "/secret"]
    assert len(auth_entry) == 1
    _, _, _, auth_hdrs = auth_entry[0]
    assert auth_hdrs.get("Authorization") == "Bearer x"


def test_empty_auth_headers_does_not_inject():
    ep = _ep(path="/secret", security=True, has_body=True)
    plan = list(build_execution_plan([ep], _engine(), auth_headers={}))
    _, _, _, hdrs = plan[0]
    assert "Authorization" not in hdrs


def test_no_auth_headers_does_not_inject():
    ep = _ep(path="/secret", security=True, has_body=True)
    plan = list(build_execution_plan([ep], _engine()))
    _, _, _, hdrs = plan[0]
    assert "Authorization" not in hdrs


def test_plan_includes_baseline_payload():
    ep = _ep(path="/test", has_body=True)
    plan = list(build_execution_plan([ep], _engine()))
    assert len(plan) == 1
    _, _, _, hdrs = plan[0]
    assert "Content-Type" in hdrs


# ── build_auth_probes ─────────────────────────────────────────────────


def test_auth_probes_skips_public_endpoints():
    ep_pub = _ep(path="/public", security=False)
    ep_auth = _ep(path="/secret", security=True)
    probes = build_auth_probes([ep_pub, ep_auth])
    assert len(probes) == 2
    for ep, path, payload, hdrs in probes:
        assert ep.path == "/secret"


def test_auth_probes_two_per_auth_endpoint():
    ep1 = _ep(path="/a", security=True)
    ep2 = _ep(path="/b", security=True)
    probes = build_auth_probes([ep1, ep2])
    assert len(probes) == 4

    paths = [p for _, p, _, _ in probes]
    assert paths.count("/a") == 2
    assert paths.count("/b") == 2


def test_auth_probe_no_token_headers():
    ep = _ep(path="/secret", security=True)
    probes = build_auth_probes([ep])
    _, _, _, hdrs = probes[0]
    assert "Authorization" not in hdrs


def test_auth_probe_invalid_token():
    ep = _ep(path="/secret", security=True)
    probes = build_auth_probes([ep])
    _, _, _, hdrs = probes[1]
    assert hdrs.get("Authorization") == "Bearer invalid_token"


def test_auth_probe_resolves_path_params():
    ep = _ep(
        path="/users/{userId}/items",
        security=True,
        params=[Parameter(name="userId", location="path", required=True, schema=Schema(type="string"))],
    )
    ctx: AuthContext = {"username": "myuser"}
    probes = build_auth_probes([ep], ctx)
    _, path, _, _ = probes[0]
    assert "{userId}" not in path
    assert path != ep.path


def test_auth_probe_body_for_post():
    ep = _ep(path="/secret", method=HttpMethod.POST, security=True, has_body=True)
    probes = build_auth_probes([ep])
    # probe 0: no token
    _, _, body, hdrs = probes[0]
    assert body is not None
    assert hdrs.get("Content-Type") == "application/json"
    # probe 1: invalid token
    _, _, body, hdrs = probes[1]
    assert body is not None
    assert hdrs.get("Authorization") == "Bearer invalid_token"


def test_auth_probe_no_body_for_get():
    ep = _ep(path="/secret", method=HttpMethod.GET, security=True, has_body=False)
    probes = build_auth_probes([ep])
    for _, _, body, _ in probes:
        assert body is None
