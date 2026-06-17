import sys
import logging

from pathlib import Path
from typing import Any

import httpx
import yaml


logger = logging.getLogger(__name__)


def _extract_by_path(data: Any, path: list[str | int]) -> Any:
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            print(f"[AUTH ERROR] Failed to extract value at path: {path}")
            sys.exit(1)

    return current


def _build_headers_from_config(headers_cfg: dict[str, str], extracted: dict[str, Any] | None = None) -> dict[str, str]:
    headers: dict[str, str] = {}
    for header_name, template in headers_cfg.items():
        value = str(template)
        if extracted:
            value = value.format(**extracted)
        headers[header_name] = value
    return headers


async def resolve_auth_headers(auth_config_path: Path) -> dict[str, str]:
    with auth_config_path.open("r") as f:
        config_file = yaml.safe_load(f)

    auth_config = config_file.get("auth")
    if not auth_config:
        raise ValueError("No 'auth' section found in the auth config file.")

    if auth_config.get("enabled") is False:
        logger.info("Auth is disabled, no headers will be injected.")
        return {}

    inject_cfg = auth_config.get("inject", {})
    headers_cfg = inject_cfg.get("headers", {}) or {}

    request_cfg = auth_config.get("request")
    response_cfg = auth_config.get("response")

    if request_cfg and response_cfg:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request_cfg["method"],
                url=request_cfg["url"],
                headers=request_cfg.get("headers"),
                json=request_cfg.get("body"),
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(f"[AUTH ERROR] Authentication failed ({exc.response.status_code})")
            sys.exit(1)

        data = response.json()
        logger.info("Authentication request successful. Extracting values...")

        extracted: dict[str, Any] = {}
        for name, path in response_cfg["extract"].items():
            extracted[name] = _extract_by_path(data, path)

        return _build_headers_from_config(headers_cfg, extracted)

    if headers_cfg:
        logger.info("No auth request/response configured; using static headers.")
        return _build_headers_from_config(headers_cfg)

    return {}
