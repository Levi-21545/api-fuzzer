import fnmatch
from typing import Iterable

from fuzzer.model.endpoint import Endpoint


def select_endpoints(
    endpoints: list[Endpoint],
    *,
    limit: int | None = None,
    all: bool = False,
    path_filter: str | None = None,
    excluded_paths: list[str] | None = None,
) -> list[Endpoint]:
    if not all and limit is None and path_filter is None:
        limit = 10

    selected: Iterable[Endpoint] = endpoints

    if path_filter:
        selected = (
            ep for ep in selected
            if fnmatch.fnmatch(ep.path, path_filter)
        )

    for excluded_path in excluded_paths or []:
        selected = [
            ep for ep in selected
            if not fnmatch.fnmatch(ep.path, excluded_path)
        ]

    selected = list(selected)

    if not all:
        if limit is not None:
            selected = selected[:limit]

    return selected
