import httpx
import time
from typing import Dict, Optional
from fuzzer.model.http import HttpMethod

class AsyncHttpClient:
    def __init__(self, timeout: float = 10.0):
        self._client = httpx.AsyncClient(timeout=timeout)

    async def request(
        self,
        method: HttpMethod,
        url: str,
        headers: Dict[str, str],
        body: Optional[str],
    ) -> tuple[int | None, float, int | None, str | None]:
        start = time.perf_counter()
        try:
            response = await self._client.request(
                method=method,
                url=url,
                headers=headers,
                content=body,
            )
            elapsed = (time.perf_counter() - start) * 1000

            return (
                response.status_code,
                elapsed,
                len(response.content),
                response.text[:10_000],  # Defensive response-size limit.
            )

        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            return None, elapsed, None, str(exc)

    async def close(self):
        await self._client.aclose()
