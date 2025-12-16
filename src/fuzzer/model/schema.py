from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class Schema:
    type: Optional[str]
    format: Optional[str] = None
    constraints: Dict[str, Any] = None
    properties: Dict[str, "Schema"] = None
    items: Optional["Schema"] = None
    required: List[str] = None