import re


def compile_openapi_pattern(pattern: str) -> re.Pattern[str]:
    r"""Compile common OpenAPI/Java patterns using Python's regex engine.

    Java's ``\p{L}`` category appears in PetClinic's contract but is not
    understood by Python's ``re``. The replacement preserves its intent for
    the Latin and Unicode word characters used in the experiment fixtures.
    """
    compatible = pattern.replace(r"[\p{L}]", r"[^\W\d_]")
    compatible = compatible.replace(r"\p{L}", r"[^\W\d_]")
    try:
        return re.compile(compatible)
    except re.error as error:
        raise ValueError(f"Unsupported OpenAPI pattern: {pattern}") from error
