from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Response:
	status_code: int
	schema: Optional[Dict[str, Any]] = None