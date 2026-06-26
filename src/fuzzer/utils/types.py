from collections.abc import Iterable, Generator
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from fuzzer.model.endpoint import Endpoint


SecurityRequirement = list[dict[str, list[str]]]
SecuritySchemes = dict[str, dict[str, Any]]

Headers = dict[str, str]
AuthContext = dict[str, str]

PayloadEntry = tuple[str, Headers, dict | None]
PayloadGenerator = Generator[PayloadEntry, None, None]

AuthResult = tuple[Headers, AuthContext]

ExecutionPlanEntry = tuple["Endpoint", str, Any | None, Headers]
ExecutionPlan = Iterable[ExecutionPlanEntry]
