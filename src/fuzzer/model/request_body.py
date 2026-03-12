from dataclasses import dataclass
from typing import Optional

from fuzzer.model.schema import Schema


@dataclass
class RequestBody:
    content_type: str
    schema: Optional[Schema] = None
