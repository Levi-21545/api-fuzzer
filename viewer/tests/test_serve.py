"""Testes do servidor: descoberta, confinamento às raízes e somente leitura."""

from __future__ import annotations

import http.client
import json
import os
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import serve  # noqa: E402


def write(path: Path, text: str = "{}") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class DiscoverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_finds_packages_and_loose_campaigns(self) -> None:
        write(self.root / "pkg" / "final-analysis.json")
        write(self.root / "pkg" / "provenance-index.json")
        write(self.root / "pkg" / "api" / "run-1" / "run_manifest.json")
        write(self.root / "set" / "api" / "run-2" / "run_manifest.json")
        write(self.root / "legacy" / "run-3" / "data" / "execution_plan.json", "[]")
        write(self.root / ".hidden" / "run-4" / "run_manifest.json")
        write(self.root / "notes" / "readme.md", "x")

        found = serve.discover(self.root)

        self.assertEqual(found["packages"], ["pkg"])
        self.assertEqual(found["campaigns"], ["legacy/run-3", "set/api/run-2"])

    def test_root_itself_can_be_a_campaign(self) -> None:
        write(self.root / "run_manifest.json")
        self.assertEqual(serve.discover(self.root)["campaigns"], [""])

    def test_does_not_follow_directory_symlinks(self) -> None:
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        write(Path(outside.name) / "run" / "run_manifest.json")
        os.symlink(outside.name, self.root / "link")
        self.assertEqual(serve.discover(self.root)["campaigns"], [])


class ResolveInsideTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        write(self.root / "a" / "b.json")
        write(self.root / ".env", "SECRET=1")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_accepts_paths_inside(self) -> None:
        self.assertEqual(
            serve.resolve_inside(self.root, "a/b.json"), self.root / "a" / "b.json"
        )

    def test_rejects_escape_and_hidden(self) -> None:
        for relative in [
            "../x",
            "a/../../x",
            "/etc/passwd",
            ".env",
            "a/.git/config",
            "a//b.json",
            "a\\b.json",
            None,
        ]:
            with self.subTest(relative=relative):
                self.assertIsNone(serve.resolve_inside(self.root, relative))

    def test_rejects_symlink_out_of_root_or_to_hidden_file(self) -> None:
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        write(Path(outside.name) / "secret.json")
        os.symlink(Path(outside.name) / "secret.json", self.root / "out.json")
        os.symlink(self.root / ".env", self.root / "env.json")
        self.assertIsNone(serve.resolve_inside(self.root, "out.json"))
        self.assertIsNone(serve.resolve_inside(self.root, "env.json"))


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name).resolve()
        write(root / "pkg" / "final-analysis.json", '{"api": {}}')
        write(root / "pkg" / "provenance-index.json")
        write(root / "pkg" / "results.md", "<script>alert(1)</script>")
        write(root / "pkg" / "api" / "run" / "data" / "bootstrap.log", "token=abc")
        write(root / ".env", "SECRET=1")
        cls.root = root
        cls.server = serve.make_server(
            [serve.Source("teste", root), serve.Source("ausente", root / "nope")], 0
        )
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmp.cleanup()

    def request(self, method: str, path: str, host: str | None = None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        headers = {"Host": host or f"127.0.0.1:{self.port}"}
        connection.request(method, path, headers=headers)
        response = connection.getresponse()
        body = response.read()
        connection.close()
        return response, body

    def test_catalog_lists_sources(self) -> None:
        response, body = self.request("GET", "/api/catalog")
        self.assertEqual(response.status, 200)
        sources = json.loads(body)["sources"]
        self.assertEqual(sources[0]["packages"], ["pkg"])
        self.assertEqual(sources[1]["problems"], ["diretório inexistente"])

    def test_serves_artifact_as_plain_text_with_csp(self) -> None:
        response, body = self.request("GET", "/api/file?source=0&path=pkg/results.md")
        self.assertEqual(response.status, 200)
        self.assertEqual(
            response.getheader("Content-Type"), "text/plain; charset=utf-8"
        )
        self.assertEqual(response.getheader("X-Content-Type-Options"), "nosniff")
        self.assertIn(
            "default-src 'self'", response.getheader("Content-Security-Policy")
        )
        self.assertEqual(body, b"<script>alert(1)</script>")

    def test_refuses_paths_outside_types_and_hidden(self) -> None:
        cases = {
            "/api/file?source=0&path=../etc/passwd": 403,
            "/api/file?source=0&path=.env": 403,
            "/api/file?source=0&path=pkg/api/run/data/bootstrap.log": 403,
            "/api/file?source=0&path=": 403,
            "/api/file?source=9&path=pkg/results.md": 400,
            "/api/file?source=0&path=pkg/missing.json": 404,
            "/app/../serve.py": 404,
            "/outra": 404,
        }
        for path, status in cases.items():
            with self.subTest(path=path):
                self.assertEqual(self.request("GET", path)[0].status, status)

    def test_only_get_is_allowed(self) -> None:
        for method in ["POST", "PUT", "PATCH", "DELETE", "OPTIONS"]:
            with self.subTest(method=method):
                self.assertEqual(
                    self.request(method, "/api/file?source=0&path=pkg/results.md")[
                        0
                    ].status,
                    405,
                )

    def test_rejects_foreign_host_header(self) -> None:
        self.assertEqual(
            self.request("GET", "/api/catalog", host="evil.example:80")[0].status, 403
        )

    def test_serves_app(self) -> None:
        response, body = self.request("GET", "/")
        self.assertEqual(response.status, 200)
        self.assertIn(b'<main id="main"', body)
        self.assertEqual(
            self.request("GET", "/app/js/model.js")[0].getheader("Content-Type"),
            "text/javascript; charset=utf-8",
        )


if __name__ == "__main__":
    unittest.main()
