from dataclasses import dataclass
from typing import List, Optional

from fuzzer.model.http import HttpMethod
from fuzzer.model.parameter import Parameter
from fuzzer.model.request_body import RequestBody
from fuzzer.model.schema import Schema


@dataclass
class Endpoint:
    path: str
    method: HttpMethod
    parameters: List[Parameter]
    request_body: Optional[RequestBody]
    responses: dict[str, Schema]
    servers: Optional[List[str]] = None

    @property
    def id(self) -> str:
        return f"{self.method.value} {self.path}"
