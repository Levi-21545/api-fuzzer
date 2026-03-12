import asyncio
from collections.abc import Iterable
from typing import Any

from fuzzer.executor.executor import Executor
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.endpoint import Endpoint


class ExecutionRunner:
    def __init__(self, executor: Executor, concurrency: int):
        self.executor = executor
        self.semaphore = asyncio.Semaphore(concurrency)

    async def _run_one(
        self,
        endpoint: Endpoint,
        path: str,
        payload: Any | None,
        headers: dict[str, str],
    ) -> ExecutionResult:
        async with self.semaphore:
            return await self.executor.execute(
                endpoint=endpoint,
                path=path,
                payload=payload,
                headers=headers,
            )

    async def run(
        self,
        tasks: Iterable[tuple[Endpoint, str, Any | None, dict[str, str]]],
    ) -> list[ExecutionResult]:
        coroutines = [
            self._run_one(endpoint, path, payload, headers)
            for endpoint, path, payload, headers in tasks
        ]

        results = await asyncio.gather(*coroutines)
        await self.executor.close()
        return results
