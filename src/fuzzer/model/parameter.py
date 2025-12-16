from dataclasses import dataclass

from fuzzer.model.schema import Schema

@dataclass
class Parameter:
    name: str
    location: str  # path, query, header
    required: bool
    schema: Schema