import random
import string
import httpx

from typing import Optional

from fuzzer.model.api_spec import APISpec
from fuzzer.model.endpoint import Endpoint
from fuzzer.model.http import HttpMethod
from fuzzer.model.schema import Schema
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.utils.types import Headers, AuthContext, AuthResult


def _random_suffix() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=8))

def _random_creds() -> dict[str, str]:
    suffix = _random_suffix()
    return {
        "username": f"fuzzer_{suffix}",
        "password": f"pass_{suffix}",
        "email": f"{suffix}@fuzzer.com",
    }


def _find_ep(spec: APISpec, *keywords: str) -> Optional[Endpoint]:
    for ep in spec.endpoints:
        name = f"{ep.method.value} {ep.path}".lower()
        if any(k in name for k in keywords):
            return ep
    return None


_IDENTITY_FIELDS = ["email", "username", "login", "user", "name"]
_LOGIN_FIELDS = ["email", "username", "login", "user"]


def _build_body_from_schema(
    schema: Optional[Schema],
    override: dict[str, str],
    unique: bool = False,
) -> object:
    """Generate a valid body from schema and override known fields with provided values."""
    body = generate_valid_value(schema)
    if isinstance(body, dict):
        for key, val in override.items():
            if key in body:
                body[key] = val
        if unique:
            suffix = _random_suffix()
            for key in list(body.keys()):
                if key not in override and isinstance(body[key], str):
                    body[key] = f"{key}_{suffix}"
    return body


def _extract_identity(body: object) -> str:
    """Extract the identity value (email or username) from a generated body."""
    if isinstance(body, dict):
        for field in _IDENTITY_FIELDS:
            if field in body:
                return str(body[field])
    return str(body)


async def bootstrap_auth(spec: APISpec, base_url: str) -> AuthResult:
    register_ep = _find_ep(spec, "register", "signup")
    login_ep = _find_ep(spec, "login", "signin", "token")

    if not register_ep or not login_ep:
        print("[AUTO-AUTH] No register/login endpoints found in spec. Skipping auto-auth.")
        return {}, {}

    creds = _random_creds()
    reg_body: object = None
    scheme_headers: Headers = {}

    async with httpx.AsyncClient() as client:
        if register_ep.method in (HttpMethod.POST, HttpMethod.PUT):
            reg_url = f"{base_url.rstrip('/')}{register_ep.path}"
            print(f"[AUTO-AUTH] Registering user at {reg_url} ...")
            reg_body = _build_body_from_schema(
                register_ep.request_body.schema if register_ep.request_body else None,
                {"password": creds["password"]},
                unique=True,
            )
            if isinstance(reg_body, dict):
                reg_body["email"] = creds["email"]
                if "name" in reg_body:
                    reg_body["name"] = reg_body["email"].split("@")[0]
            reg_resp = await client.request(
                method=register_ep.method.value,
                url=reg_url,
                json=reg_body,
            )
            if reg_resp.is_success or reg_resp.status_code == 409:
                print(f"[AUTO-AUTH] Registration OK (status={reg_resp.status_code})")
            else:
                print(f"[AUTO-AUTH] Registration returned {reg_resp.status_code}, attempting login anyway...")

        token = await _try_login(client, base_url, login_ep, creds, reg_body)
        if token:
            scheme_headers = _build_scheme_headers(spec, token)

    if not token:
        print("[AUTO-AUTH] Failed to obtain auth token.")
        return {}, {}

    auth_context = _build_auth_context(reg_body, creds)
    print(f"[AUTO-AUTH] Injected headers for {len(scheme_headers)} scheme(s): {list(scheme_headers.keys())}")
    return scheme_headers, auth_context


async def _try_login(
    client: httpx.AsyncClient,
    base_url: str,
    login_ep: Endpoint,
    creds: dict[str, str],
    reg_body: object,
) -> Optional[str]:
    if login_ep.method not in (HttpMethod.POST, HttpMethod.GET):
        return None

    login_url = f"{base_url.rstrip('/')}{login_ep.path}"
    print(f"[AUTO-AUTH] Logging in at {login_url} ...")
    login_body = _build_body_from_schema(
        login_ep.request_body.schema if login_ep.request_body else None,
        {"password": creds["password"]},
    )
    if isinstance(login_body, dict):
        identity = _extract_identity(reg_body)
        for field in _LOGIN_FIELDS:
            if field in login_body:
                login_body[field] = identity
                break

    login_resp = await client.request(
        method=login_ep.method.value,
        url=login_url,
        json=login_body if login_ep.method == HttpMethod.POST else None,
    )
    if login_resp.is_success:
        data = login_resp.json()
        for key in ("auth_token", "token", "access_token", "id_token", "jwt"):
            if key in data:
                token = data[key]
                if token:
                    print("[AUTO-AUTH] Token obtained successfully.")
                    return token
    return None


def _build_scheme_headers(spec: APISpec, token: str) -> Headers:
    headers: Headers = {}
    for scheme_def in spec.security_schemes.values():
        stype = scheme_def.get("type", "")
        if stype == "http":
            sscheme = scheme_def.get("scheme", "bearer")
            if sscheme == "bearer":
                headers["Authorization"] = f"Bearer {token}"
            elif sscheme == "basic":
                headers["Authorization"] = f"Basic {token}"
        elif stype == "apiKey":
            in_ = scheme_def.get("in", "header")
            name = scheme_def.get("name", "X-API-Key")
            if in_ == "header":
                headers[name] = token
    return headers


def _build_auth_context(reg_body: object, creds: dict[str, str]) -> AuthContext:
    identity = _extract_identity(reg_body)
    ctx: AuthContext = {
        "email": identity if "@" in identity else creds["email"],
        "password": creds["password"],
    }
    if "@" in identity:
        ctx["username"] = identity.split("@")[0]
    else:
        ctx["username"] = identity
    return ctx
