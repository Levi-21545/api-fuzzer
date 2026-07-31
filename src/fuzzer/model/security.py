from typing import Any


SchemeName = str
Scope = str

SecurityRequirement = list[dict[SchemeName, list[Scope]]]
SecuritySchemes = dict[SchemeName, dict[str, Any]]
