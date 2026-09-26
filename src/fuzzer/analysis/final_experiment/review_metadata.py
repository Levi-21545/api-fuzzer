"""Pinned source and license references used by the review package."""

REVIEW_SCHEMA_REFERENCES = {
    "vampi": "../mock-projects/VAmPI/openapi_specs/openapi3.yml",
    "petclinic": (
        "../mock-projects/spring-petclinic-rest/src/main/resources/openapi.yml"
    ),
    "crapi": "../mock-projects/crAPI/openapi-spec/crapi-openapi-spec.json",
    "realworld": "../mock-projects/realworld/specs/api/openapi.yml",
}
REVIEW_LICENSES = {
    "vampi": ("MIT", "../mock-projects/VAmPI/LICENSE"),
    "petclinic": (
        "Apache-2.0",
        "../mock-projects/spring-petclinic-rest/LICENSE.txt",
    ),
    "crapi": ("Apache-2.0", "../mock-projects/crAPI/LICENSE.md"),
    "realworld": ("MIT", "../mock-projects/realworld/LICENSE"),
}
REVIEW_PROVENANCE = {
    "vampi": "VAmPI (`f16052dce83f05847133ec98f01c5193a41de7d8`)",
    "petclinic": ("spring-petclinic-rest (`c7b5f5e9e90af2e5b94a40dd77b2a53dc33f67bd`)"),
    "crapi": "crAPI (`73d309cc8f28bbdeed31dbb35f05dba8354de3c9`)",
    "realworld": (
        "RealWorld specification (`98f29fb3f8bcb1dd614b91f2851371bf22c34775`)"
    ),
}
