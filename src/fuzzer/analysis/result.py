from dataclasses import dataclass
from typing import Any
from fuzzer.analysis.classification import Anomaly, AnomalySeverity
from fuzzer.executor.result import ExecutionResult
from fuzzer.utils.types import Headers


@dataclass
class AnalysisResult:
    classification: Anomaly
    description: str
    endpoint_id: str
    request_payload: Any | None
    request_headers: Headers
    execution_result: ExecutionResult
    severity_score: float = 0.0
    severity: AnomalySeverity = AnomalySeverity.LOW
    severity_assessment: dict[str, Any] | None = None
    case_id: str = "case-unassigned"
