from dataclasses import dataclass
from typing import Any, Literal

@dataclass(frozen=True)
class MutationOp:
    path: tuple[str, ...]
    op: Literal["replace", "delete"]
    value: Any = None
