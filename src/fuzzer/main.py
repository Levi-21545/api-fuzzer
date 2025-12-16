import sys
from fuzzer.parser.openapi_parser import OpenAPIParser


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <openapi.yaml> <base_url>")
        sys.exit(1)

    spec_path = sys.argv[1]
    base_url = sys.argv[2]

    parser = OpenAPIParser(spec_path)
    api = parser.parse()

    print(f"Loaded API with {len(api.endpoints)} endpoints")
    for ep in api.endpoints:
        print(f"{ep.method} {ep.path}")
        if ep.request_body:
            print(f"  request body: {ep.request_body}")
        if ep.parameters:
            print(f"  parameters: {[p.name for p in ep.parameters]}")
        if ep.responses:
            print(f"  responses: {[ep.responses]}")


if __name__ == "__main__":
    main()
