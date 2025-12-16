import asyncio
from collections.abc import Iterable

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
        payload: str | None,
        headers: dict[str, str],
    ) -> ExecutionResult:
        async with self.semaphore:
            return await self.executor.execute(
                endpoint=endpoint,
                payload=payload,
                headers=headers,
            )

    async def run(
        self,
        tasks: Iterable[tuple[Endpoint, str | None, dict[str, str]]],
    ) -> list[ExecutionResult]:
        coroutines = [
            self._run_one(endpoint, payload, headers)
            for endpoint, payload, headers in tasks
        ]

        results = await asyncio.gather(*coroutines)
        await self.executor.close()
        return results
