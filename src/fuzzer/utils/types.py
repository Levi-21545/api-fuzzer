from collections.abc import Iterable, Generator
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from fuzzer.model.endpoint import Endpoint


StatusCode = int
ResponseTimeMs = float
ResponseSize = int
SchemeName = str
Scope = str

Headers = dict[str, str] # nome → valor
AuthContext = dict[str, str] # email, username, password → valor
AuthResult = tuple[Headers, AuthContext]

# Alternativas (OR): [{"bearerAuth": ["admin"]}, {"apiKey": []}]
SecurityRequirement = list[dict[SchemeName, list[Scope]]]

# {"bearerAuth": {"type": "http", "scheme": "bearer"}}
SecuritySchemes = dict[SchemeName, dict[str, Any]]

PayloadEntry = tuple[str, Headers, dict | None] # (path, headers, body)
PayloadGenerator = Generator[PayloadEntry, None, None]
ExecutionPlanEntry = tuple["Endpoint", str, Any | None, Headers]  # (endpoint, path, payload, headers)
ExecutionPlan = Iterable[ExecutionPlanEntry]
