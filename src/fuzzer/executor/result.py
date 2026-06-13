from dataclasses import dataclass
from typing import Optional
from fuzzer.model.http import HttpMethod


@dataclass(slots=True)
class ExecutionResult:
    endpoint_id: str
    method: HttpMethod
    url: str

    status_code: Optional[int]
    response_time_ms: float
    response_size: Optional[int]

    raw_response: Optional[str]
    error: Optional[str]

    def to_dict(self) -> dict:
        return {
            "endpoint_id": self.endpoint_id,
            "method": self.method.value,
            "url": self.url,
            "status_code": self.status_code,
            "response_time_ms": round(self.response_time_ms, 2),
            "response_size": self.response_size,
            "error": self.error,
            "raw_response": self.raw_response,
        }
