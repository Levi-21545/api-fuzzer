"""Pinned per-API contract, source and license metadata for the review package."""

MEILISEARCH_ASSET_URL = (
    "https://github.com/meilisearch/meilisearch/releases/download/"
    "v1.45.1/meilisearch-openapi.json"
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

# Key order is the API order of the generated documents. Each contract is copied
# unchanged to contracts/<contract_file>; `source` is the markdown link to the
# exact upstream revision. The license is copied from `license_file` or written
# from `license_text`.
API_METADATA = {
    "vampi": {
        "label": "VAmPI",
        "contract_file": "vampi-openapi3.yml",
        "source": (
            "[erev0s/VAmPI](https://github.com/erev0s/VAmPI/tree/"
            "f16052dce83f05847133ec98f01c5193a41de7d8) @ `f16052d`"
        ),
        "license": "MIT",
        "license_file": "../mock-projects/VAmPI/LICENSE",
        "license_copy": "vampi-LICENSE.txt",
    },
    "petclinic": {
        "label": "Spring Petclinic REST",
        "contract_file": "petclinic-openapi.yml",
        "source": (
            "[spring-petclinic/spring-petclinic-rest]"
            "(https://github.com/spring-petclinic/spring-petclinic-rest/tree/"
            "c7b5f5e9e90af2e5b94a40dd77b2a53dc33f67bd) @ `c7b5f5e`"
        ),
        "license": "Apache-2.0",
        "license_file": "../mock-projects/spring-petclinic-rest/LICENSE.txt",
        "license_copy": "petclinic-LICENSE.txt",
    },
    "crapi": {
        "label": "crAPI",
        "contract_file": "crapi-openapi-spec.json",
        "source": (
            "[OWASP/crAPI](https://github.com/OWASP/crAPI/tree/"
            "73d309cc8f28bbdeed31dbb35f05dba8354de3c9) @ `73d309c`"
        ),
        "license": "Apache-2.0",
        "license_file": "../mock-projects/crAPI/LICENSE.md",
        "license_copy": "crapi-LICENSE.txt",
    },
    "realworld": {
        "label": "RealWorld/Conduit",
        "contract_file": "realworld-openapi.yml",
        "source": (
            "[realworld-apps/realworld](https://github.com/realworld-apps/"
            "realworld/tree/98f29fb3f8bcb1dd614b91f2851371bf22c34775) @ `98f29fb`"
        ),
        "license": "MIT",
        "license_file": "../mock-projects/realworld/LICENSE",
        "license_copy": "realworld-LICENSE.txt",
    },
    "meilisearch": {
        "label": "Meilisearch",
        "contract_file": "meilisearch-v1.45.1-openapi.json",
        "source": f"[asset da release v1.45.1]({MEILISEARCH_ASSET_URL})",
        "license": "MIT",
        "license_text": MEILISEARCH_MIT_LICENSE,
        "license_copy": "meilisearch-LICENSE-MIT.txt",
    },
}

# Paragraphs appended to LICENSES.md, in this order, when their API is present.
LICENSE_NOTES = (
    (
        "meilisearch",
        "O Meilisearch distribui este contrato entre os assets exclusivamente "
        f"MIT ([issue #6010]({MEILISEARCH_LICENSE_EVIDENCE_URL})).",
    ),
    (
        "vampi",
        "Os tokens de exemplo nos contratos (VAmPI, Meilisearch) vêm da "
        "documentação original e não são credenciais.",
    ),
)
