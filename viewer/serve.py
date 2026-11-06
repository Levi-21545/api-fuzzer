#!/usr/bin/env python3
"""Servidor local, somente leitura, do visualizador de resultados do api-fuzzer.

Procura pacotes e campanhas sob as raízes configuradas e entrega os arquivos
desses artefatos ao navegador. Não escreve em disco, não executa comandos e só
responde a GET em 127.0.0.1.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

VIEWER_DIR = Path(__file__).resolve().parent
APP_DIR = VIEWER_DIR / "app"
DEFAULT_REPO = VIEWER_DIR.parent

# Tipos de arquivo que a interface pode ler. Logs, binários e qualquer outra
# extensão ficam de fora mesmo sob uma raiz configurada.
ARTIFACT_TYPES = {
    ".json": "application/json; charset=utf-8",
    ".md": "text/plain; charset=utf-8",
    ".csv": "text/plain; charset=utf-8",
    ".yml": "text/plain; charset=utf-8",
    ".yaml": "text/plain; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
}
APP_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
}
PACKAGE_MARKERS = ("final-analysis.json", "provenance-index.json")
MAX_SCAN_DEPTH = 6
MAX_FILE_BYTES = 64 * 1024 * 1024

SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
        "base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
}


@dataclass(frozen=True)
class Source:
    label: str
    root: Path


def resolve_inside(root: Path, relative: str | None) -> Path | None:
    """Resolve `relative` sob `root`, recusando fuga da raiz e nomes ocultos."""
    if relative is None:
        return None
    if relative == "":
        return root
    parts = relative.split("/")
    if relative.startswith("/") or "\\" in relative:
        return None
    if any(part == "" or part.startswith(".") for part in parts):
        return None
    candidate = (root / relative).resolve()
    if candidate != root and root not in candidate.parents:
        return None
    # Um symlink dentro da raiz pode apontar para um arquivo oculto da raiz.
    if any(part.startswith(".") for part in candidate.relative_to(root).parts):
        return None
    return candidate


def is_campaign_dir(directory: Path, names: set[str]) -> bool:
    if "run_manifest.json" in names:
        return True
    return (directory / "data" / "execution_plan.json").is_file()


def discover(root: Path) -> dict:
    """Lista pacotes finais e campanhas sob `root`.

    Um pacote tem `final-analysis.json` e `provenance-index.json`; suas
    campanhas são lidas a partir da análise publicada, então a busca não desce
    nele. Uma campanha tem `run_manifest.json` ou `data/execution_plan.json`.
    """
    packages: list[str] = []
    campaigns: list[str] = []
    problems: list[str] = []

    def walk(directory: Path, depth: int) -> None:
        relative = directory.relative_to(root).as_posix()
        relative = "" if relative == "." else relative
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as error:
            problems.append(f"{relative or '.'}: {error.strerror}")
            return
        names = {entry.name for entry in entries}
        if all(marker in names for marker in PACKAGE_MARKERS):
            packages.append(relative)
            return
        if is_campaign_dir(directory, names):
            campaigns.append(relative)
            return
        if depth >= MAX_SCAN_DEPTH:
            return
        for entry in entries:
            if entry.name.startswith("."):
                continue
            if entry.is_dir(follow_symlinks=False):
                walk(Path(entry.path), depth + 1)

    walk(root, 0)
    return {"packages": packages, "campaigns": campaigns, "problems": problems}


class ViewerHandler(BaseHTTPRequestHandler):
    server_version = "api-fuzzer-viewer"
    sys_version = ""
    sources: list[Source] = []
    allowed_hosts: set[str] = set()

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        sys.stderr.write(f"{self.address_string()} {format % args}\n")

    def send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for name, value in SECURITY_HEADERS.items():
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_bytes(status, body, "application/json; charset=utf-8")

    def send_error_json(self, status: int, message: str) -> None:
        self.send_json(status, {"error": message})

    def reject_method(self) -> None:
        self.send_error_json(HTTPStatus.METHOD_NOT_ALLOWED, "somente leitura")

    do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = reject_method

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_GET(self) -> None:
        # Recusa nomes de host externos (proteção contra DNS rebinding).
        if self.headers.get("Host", "") not in self.allowed_hosts:
            self.send_error_json(HTTPStatus.FORBIDDEN, "host não permitido")
            return
        url = urlsplit(self.path)
        query = parse_qs(url.query)
        if url.path == "/api/catalog":
            self.serve_catalog()
        elif url.path == "/api/file":
            self.serve_artifact(query)
        elif url.path == "/":
            self.serve_app("index.html")
        elif url.path.startswith("/app/"):
            self.serve_app(url.path.removeprefix("/app/"))
        else:
            self.send_error_json(HTTPStatus.NOT_FOUND, "rota inexistente")

    def serve_catalog(self) -> None:
        sources = []
        for index, source in enumerate(self.sources):
            entry = {"id": index, "label": source.label, "path": str(source.root)}
            if source.root.is_dir():
                entry.update(discover(source.root))
            else:
                entry.update(
                    packages=[], campaigns=[], problems=["diretório inexistente"]
                )
            sources.append(entry)
        self.send_json(HTTPStatus.OK, {"sources": sources})

    def serve_artifact(self, query: dict[str, list[str]]) -> None:
        try:
            source = self.sources[int(query.get("source", [""])[0])]
        except (ValueError, IndexError):
            self.send_error_json(HTTPStatus.BAD_REQUEST, "fonte inválida")
            return
        relative = query.get("path", [None])[0]
        path = resolve_inside(source.root, relative)
        if path is None or path == source.root:
            self.send_error_json(HTTPStatus.FORBIDDEN, "caminho fora da raiz")
            return
        content_type = ARTIFACT_TYPES.get(path.suffix.lower())
        if content_type is None:
            self.send_error_json(HTTPStatus.FORBIDDEN, "tipo de arquivo não lido")
            return
        self.send_file(path, content_type)

    def serve_app(self, relative: str) -> None:
        path = resolve_inside(APP_DIR, relative)
        content_type = APP_TYPES.get(path.suffix.lower()) if path else None
        if path is None or content_type is None:
            self.send_error_json(HTTPStatus.NOT_FOUND, "arquivo inexistente")
            return
        self.send_file(path, content_type)

    def send_file(self, path: Path, content_type: str) -> None:
        if not path.is_file():
            self.send_error_json(HTTPStatus.NOT_FOUND, "arquivo inexistente")
            return
        if path.stat().st_size > MAX_FILE_BYTES:
            self.send_error_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "arquivo grande demais"
            )
            return
        self.send_bytes(HTTPStatus.OK, path.read_bytes(), content_type)


def build_sources(args: argparse.Namespace) -> list[Source]:
    repo = Path(args.repo).expanduser().resolve()
    sources = [Source("experiments/ do repositório", repo / "experiments")]
    if args.include_output:
        sources.append(
            Source("output/experiments/ (local)", repo / "output" / "experiments")
        )
    for extra in args.root:
        path = Path(extra).expanduser().resolve()
        sources.append(Source(f"raiz extra: {path.name}", path))
    return [Source(s.label, s.root.resolve()) for s in sources]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo",
        default=str(DEFAULT_REPO),
        help="raiz do repositório api-fuzzer (padrão: o diretório acima de viewer/)",
    )
    parser.add_argument(
        "--include-output",
        action="store_true",
        help="também procura em <repo>/output/experiments",
    )
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        help="diretório extra a procurar (repetível), p.ex. a saída de uma run do CLI",
    )
    parser.add_argument("--port", type=int, default=8765)
    return parser.parse_args(argv)


class ViewerServer(ThreadingHTTPServer):
    # A fila padrão (5) estoura quando o navegador abre os seis arquivos de uma
    # campanha em paralelo, e o pedido excedente volta como "Failed to fetch".
    request_queue_size = 64
    daemon_threads = True


def make_server(sources: list[Source], port: int) -> ThreadingHTTPServer:
    handler = type("Handler", (ViewerHandler,), {"sources": sources})
    server = ViewerServer(("127.0.0.1", port), handler)
    bound = server.server_address[1]
    handler.allowed_hosts = {f"127.0.0.1:{bound}", f"localhost:{bound}"}
    return server


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    sources = build_sources(args)
    server = make_server(sources, args.port)
    for source in sources:
        state = "" if source.root.is_dir() else "  (inexistente)"
        print(f"fonte: {source.root}{state}")
    print(f"abra http://127.0.0.1:{server.server_address[1]}/  (Ctrl+C encerra)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
