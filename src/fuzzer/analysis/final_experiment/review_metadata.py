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
MEILISEARCH_ASSET_URL = (
    "https://github.com/meilisearch/meilisearch/releases/download/"
    "v1.45.1/meilisearch-openapi.json"
)
MEILISEARCH_LICENSE_URL = (
    "https://github.com/meilisearch/meilisearch/blob/v1.45.1/LICENSE-MIT"
)
MEILISEARCH_LICENSE_EVIDENCE_URL = "https://github.com/meilisearch/meilisearch/issues/6010"
MEILISEARCH_MIT_LICENSE = """MIT License

Copyright (c) 2019-2025 Meili SAS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
