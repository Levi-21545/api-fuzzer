from __future__ import annotations

from collections.abc import Iterable, Generator
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING, Literal


if TYPE_CHECKING:
    from fuzzer.model.endpoint import Endpoint


StatusCode = int
ResponseTimeMs = float
ResponseSize = int

Headers = dict[str, str]
AuthContext = dict[str, str]
AuthResult = tuple[Headers, AuthContext]

PayloadEntry = tuple[str, Headers, Any | None, dict[str, Any]]
PayloadGenerator = Generator[PayloadEntry, None, None]


@dataclass(slots=True)
class ExecutionPlanEntry:
    endpoint: Endpoint
    path: str
    payload: Any | None
    headers: Headers
    case_id: str
    case_kind: Literal["baseline", "mutation", "auth_probe"]
    mutations: list[dict[str, Any]] = field(default_factory=list)
    auth_probe_kind: Literal["missing_credential", "invalid_credential"] | None = None

    @property
    def expects_rejection(self) -> bool:
        return self.case_kind == "auth_probe" or (
            bool(self.mutations)
            and any(
                not mutation.get("expected_valid", False)
                for mutation in self.mutations
            )
        )


ExecutionPlan = Iterable[ExecutionPlanEntry]
