from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class RequestBody:
	content_type: str
	schema: Optional[Dict[str, Any]] = None