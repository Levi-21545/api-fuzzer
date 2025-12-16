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


@dataclass
class Parameter:
    name: str
    location: str  # path, query, header
    required: bool
    schema: Schema


@dataclass
class Endpoint:
    path: str
    method: str
    parameters: List[Parameter]
    request_body: Optional[Schema]
    responses: Dict[str, Schema]


@dataclass
class APISpec:
    base_url: str
    endpoints: List[Endpoint]
