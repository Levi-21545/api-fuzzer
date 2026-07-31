from dataclasses import dataclass

from fuzzer.model.schema import Schema


@dataclass
class RequestBody:
    content_type: str
    schema: Schema
