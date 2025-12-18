import sys

from pathlib import Path
from typing import Any

import httpx
import yaml


def _extract_by_path(data: Any, path: list[str | int]) -> Any:
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            print(f"[AUTH ERROR] Failed to extract value at path: {path}")
            sys.exit(1)

    return current

async def resolve_auth_headers(auth_config_path: Path) -> dict[str, str]:
    with auth_config_path.open("r") as f:
        config_file = yaml.safe_load(f)

    auth_config = config_file.get("auth")
    if not auth_config:
        raise ValueError("No 'auth' section found in the auth config file.")

    request_cfg = auth_config["request"]
    response_cfg = auth_config["response"]
    inject_cfg = auth_config.get("inject", {})

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

    print("Authentication request successful. Extracting values...")

    # 1. Extrai os valores declarados
    extracted: dict[str, Any] = {}
    for name, path in response_cfg["extract"].items():
        extracted[name] = _extract_by_path(data, path)

    # 2. Monta headers finais
    headers: dict[str, str] = {}
    for header_name, template in inject_cfg['headers'].items():
        headers[header_name] = str(template).format(**extracted)

    return headers