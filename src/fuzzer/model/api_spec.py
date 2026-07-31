from dataclasses import dataclass, field
from typing import List, Optional

from fuzzer.model.endpoint import Endpoint
from fuzzer.model.security import SecurityRequirement, SecuritySchemes


@dataclass
class APISpec:
    base_urls: List[str]
    endpoints: List[Endpoint]
    security_schemes: SecuritySchemes = field(default_factory=dict)
    global_security: Optional[SecurityRequirement] = None
