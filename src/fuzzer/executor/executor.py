from typing import Optional, Any

import httpx
import time

from fuzzer.model.api_spec import APISpec
from fuzzer.model.endpoint import Endpoint
from fuzzer.executor.result import ExecutionResult


class Executor:
    def __init__(
        self,
        spec: APISpec,
        override_base_url: Optional[str] = None,
        timeout: float = 10.0,
    ):
        self.spec = spec
        self.override_base_url = override_base_url
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))

    async def execute(
        self,
        endpoint: Endpoint,
        path: str,
        payload: Any | None,
        headers: dict[str, str],
    ) -> ExecutionResult:
        base_url = self._resolve_base_url(endpoint)
        url = f"{base_url.rstrip('/')}{path}"

        start = time.perf_counter()

        try:
            response = await self.client.request(
                method=endpoint.method.value,
                url=url,
                json=payload,
                headers=headers,
            )

            elapsed_ms = (time.perf_counter() - start) * 1000

            return ExecutionResult(
                endpoint_id=endpoint.id,
                method=endpoint.method,
                url=url,
                status_code=response.status_code,
                response_time_ms=elapsed_ms,
                response_size=len(response.content) if response.content else 0,
                raw_response=response.text,
                error=None,
            )

        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000

            return ExecutionResult(
                endpoint_id=endpoint.id,
                method=endpoint.method,
                url=url,
                status_code=None,
                response_time_ms=elapsed_ms,
                response_size=None,
                raw_response=None,
                error=str(exc) or type(exc).__name__,
            )

    def _resolve_base_url(self, endpoint: Endpoint) -> str:
        if self.override_base_url:
            return self.override_base_url

        if endpoint.servers:
            return endpoint.servers[0]

        return self.spec.base_urls[0]

    async def close(self):
        await self.client.aclose()
