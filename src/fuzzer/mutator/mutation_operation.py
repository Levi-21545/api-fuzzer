from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class MutationOp:
    path: tuple[str, ...]
    op: Literal["replace", "delete"]
    value: Any = None
    operator: str = "generic"
    constraint: str | None = None
    expected_valid: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": list(self.path),
            "operation": self.op,
            "operator": self.operator,
            "constraint": self.constraint,
            "expected_valid": self.expected_valid,
            "value": self.value,
        }


@dataclass(frozen=True)
class MutationCase:
    payload: Any
    kind: Literal["baseline", "mutation"]
    operations: tuple[MutationOp, ...] = ()
