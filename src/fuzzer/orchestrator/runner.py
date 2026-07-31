import asyncio

from fuzzer.executor.executor import Executor
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.endpoint import Endpoint
from fuzzer.utils.types import Headers, ExecutionPlan


class ExecutionRunner:
    def __init__(self, executor: Executor, concurrency: int, delay_ms: int = 0):
        self.executor = executor
        self.semaphore = asyncio.Semaphore(concurrency)
        self.delay = delay_ms / 1000

    async def _run_one(
        self,
        case_id: str,
        endpoint: Endpoint,
        path: str,
        payload: object,
        headers: Headers,
    ) -> ExecutionResult:
        async with self.semaphore:
            result = await self.executor.execute(
                case_id=case_id,
                endpoint=endpoint,
                path=path,
                payload=payload,
                headers=headers,
            )
            if self.delay > 0:
                await asyncio.sleep(self.delay)
            return result

    async def run(
        self,
        tasks: ExecutionPlan,
    ) -> list[ExecutionResult]:
        coroutines = [
            self._run_one(
                entry.case_id,
                entry.endpoint,
                entry.path,
                entry.payload,
                entry.headers,
            )
            for entry in tasks
        ]

        results = await asyncio.gather(*coroutines)
        await self.executor.close()
        return results
