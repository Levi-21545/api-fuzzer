from dataclasses import dataclass
from typing import Any
from fuzzer.analysis.classification import Anomaly
from fuzzer.executor.result import ExecutionResult

@dataclass
class AnalysisResult:
    classification: Anomaly
    description: str
    endpoint_id: str
    request_payload: Any | None
    request_headers: dict
    execution_result: ExecutionResult
