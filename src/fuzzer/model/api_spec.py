from dataclasses import dataclass
from typing import List

from fuzzer.model.endpoint import Endpoint


@dataclass
class APISpec:
    base_urls: List[str]
    endpoints: List[Endpoint]
