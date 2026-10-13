"""Pinned per-API contract, source and license metadata for the review package."""

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

# Key order is the API order of the generated documents. "external" contracts
# stay in ../mock-projects and are referenced by the adapted manifests;
# "included" contracts are copied once to `schema` inside the package. The
# license is copied from `license_file` or written from `license_text`.
API_METADATA = {
    "vampi": {
        "label": "VAmPI",
        "contract": "external",
        "schema": "../mock-projects/VAmPI/openapi_specs/openapi3.yml",
        "source": "VAmPI (`f16052dce83f05847133ec98f01c5193a41de7d8`)",
        "license": "MIT",
        "license_file": "../mock-projects/VAmPI/LICENSE",
        "license_copy": "vampi-LICENSE.txt",
    },
    "petclinic": {
        "label": "Spring Petclinic REST",
        "contract": "external",
        "schema": (
            "../mock-projects/spring-petclinic-rest/src/main/resources/openapi.yml"
        ),
        "source": (
            "spring-petclinic-rest (`c7b5f5e9e90af2e5b94a40dd77b2a53dc33f67bd`)"
        ),
        "license": "Apache-2.0",
        "license_file": "../mock-projects/spring-petclinic-rest/LICENSE.txt",
        "license_copy": "petclinic-LICENSE.txt",
    },
    "crapi": {
        "label": "crAPI",
        "contract": "external",
        "schema": "../mock-projects/crAPI/openapi-spec/crapi-openapi-spec.json",
        "source": "crAPI (`73d309cc8f28bbdeed31dbb35f05dba8354de3c9`)",
        "license": "Apache-2.0",
        "license_file": "../mock-projects/crAPI/LICENSE.md",
        "license_copy": "crapi-LICENSE.txt",
    },
    "realworld": {
        "label": "RealWorld/Conduit",
        "contract": "external",
        "schema": "../mock-projects/realworld/specs/api/openapi.yml",
        "source": (
            "RealWorld specification (`98f29fb3f8bcb1dd614b91f2851371bf22c34775`)"
        ),
        "license": "MIT",
        "license_file": "../mock-projects/realworld/LICENSE",
        "license_copy": "realworld-LICENSE.txt",
    },
    "meilisearch": {
        "label": "Meilisearch",
        "contract_label": "Meilisearch v1.45.1",
        "contract": "included",
        "schema": "contracts/meilisearch-v1.45.1-openapi.json",
        "source": "Asset comunitário em `contracts/`",
        "license": "MIT — asset comunitário MIT-only segundo o upstream",
        "license_text": MEILISEARCH_MIT_LICENSE,
        "license_copy": "meilisearch-LICENSE-MIT.txt",
    },
}

# Paragraphs appended to LICENSES.md, in this order, when their API is present.
LICENSE_NOTES = (
    (
        "meilisearch",
        f"Asset: [{MEILISEARCH_ASSET_URL}]({MEILISEARCH_ASSET_URL}). "
        "O upstream o lista entre os assets exclusivamente MIT na "
        f"[decisão de separar os assets Community e Enterprise]"
        f"({MEILISEARCH_LICENSE_EVIDENCE_URL}); o aviso está em "
        f"[`licenses/meilisearch-LICENSE-MIT.txt`]"
        f"(licenses/meilisearch-LICENSE-MIT.txt), obtido de "
        f"[{MEILISEARCH_LICENSE_URL}]({MEILISEARCH_LICENSE_URL}).",
    ),
    (
        "vampi",
        "O contrato VAmPI não foi copiado porque contém um exemplo "
        "com formato de JWT.",
    ),
    (
        "meilisearch",
        "O contrato Meilisearch mantém um valor com aparência de "
        "chave apenas no exemplo textual do esquema Bearer. O pacote "
        "não o altera para preservar o hash do asset; não há evidência "
        "no contrato de que o exemplo seja uma credencial ativa.",
    ),
)
