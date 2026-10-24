from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.context_graph import (
    DEFAULT_MAX_FILES,
    DEFAULT_MAX_OUTPUT_CHARS,
    GENERATOR_MARKER,
    GraphError,
    build_repository,
    main,
    render_repository_map,
    write_graph,
)


class ContextGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_source(self, relative_path: str, content: str) -> Path:
        path = self.project_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def render(self, source_roots=None, include_files=False, include_external=False):
        repository = build_repository(self.project_root, source_roots)
        return repository, render_repository_map(
            repository,
            include_files=include_files,
            include_external_imports=include_external,
        )

    def test_polyglot_inventory_includes_languages_and_directories(self) -> None:
        self.write_source(
            "src/app.py",
            "class Service:\n    def call(self):\n        return True\n\ndef run():\n    return Service()\n",
        )
        self.write_source("web/app.ts", "export const run = () => true;\n")
        self.write_source("cmd/main.go", "package main\n")
        self.write_source("Dockerfile", "FROM scratch\n")
        self.write_source("README.md", "# Not code\n")

        repository, markdown = self.render()

        self.assertEqual([item.path for item in repository.files], ["Dockerfile", "cmd/main.go", "src/app.py", "web/app.ts"])
        self.assertIn("Files: 4", markdown)
        self.assertIn("- Python: 1 files", markdown)
        self.assertIn("- TypeScript: 1 files", markdown)
        self.assertIn("- Go: 1 files", markdown)
        self.assertIn("- Docker: 1 files", markdown)
        self.assertIn("`src/`: 1 files (Python 1)", markdown)
        self.assertIn("`web/`: 1 files (TypeScript 1)", markdown)
        self.assertIn("class Service L1-L3 (call)", markdown)
        self.assertIn("function run L5-L6", markdown)

    def test_non_python_repository_still_produces_a_structural_map(self) -> None:
        self.write_source("src/app.ts", "export const start = () => true;\n")
        self.write_source("src/util.ts", "export const value = 1;\n")

        repository, markdown = self.render()

        self.assertEqual(len(repository.files), 2)
        self.assertEqual(repository.modules, ())
        self.assertIn("## Python Modules", markdown)
        self.assertIn("None detected; structural inventory only.", markdown)
        self.assertIn("Other languages are a structural inventory", markdown)

    def test_python_symbols_and_imports_resolve(self) -> None:
        self.write_source("app/__init__.py", "from .service import run\n")
        self.write_source(
            "app/service.py",
            "import json\nfrom .util import helper\n\nclass Service:\n    def call(self):\n        return helper()\n\nasync def run(value: str) -> str:\n    return value\n",
        )
        self.write_source("app/util.py", "def helper():\n    return 1\n")

        _, markdown = self.render()
        self.assertIn("`app/service.py` `app.service`: class Service L4-L6 (call); async function run L8-L9", markdown)
        self.assertIn("`app/service.py` -> `app.util` [in-scope: `app/util.py`]", markdown)
        self.assertIn("`app/__init__.py` -> `app.service` [in-scope: `app/service.py`]", markdown)
        self.assertNotIn("`app/service.py` -> `json`", markdown)
        self.assertIn("external/out-of-scope imports omitted", markdown)

        _, full = self.render(include_external=True)
        self.assertIn("`app/service.py` -> `json` [external/outside scope]", full)

    def test_absolute_from_imports_resolve_and_leave_external_unresolved(self) -> None:
        self.write_source("pkg/__init__.py", "value = 1\n")
        self.write_source("pkg/api.py", "from pkg import value\nfrom json import loads\n")
        _, markdown = self.render()
        self.assertIn("`pkg/api.py` -> `pkg` [in-scope: `pkg/__init__.py`]", markdown)
        self.assertNotIn("`pkg/api.py` -> `json`", markdown)

        _, full = self.render(include_external=True)
        self.assertIn("`pkg/api.py` -> `json` [external/outside scope]", full)

    def test_relative_imports_resolve_from_package_and_module(self) -> None:
        self.write_source("pkg/__init__.py", "from .api import run\n")
        self.write_source("pkg/api.py", "from .service import Service\n")
        self.write_source("pkg/service.py", "class Service:\n    pass\n")
        _, markdown = self.render()
        self.assertIn("`pkg/__init__.py` -> `pkg.api` [in-scope: `pkg/api.py`]", markdown)
        self.assertIn("`pkg/api.py` -> `pkg.service` [in-scope: `pkg/service.py`]", markdown)

    def test_explicit_source_roots_are_respected(self) -> None:
        self.write_source("src/pkg/app.py", "import pkg.helper\n")
        self.write_source("src/pkg/helper.py", "value = 1\n")
        self.write_source("tests/test_app.py", "from pkg.app import run\n")

        repository, markdown = self.render([Path("src")])

        self.assertEqual([item.path for item in repository.files], ["src/pkg/app.py", "src/pkg/helper.py"])
        self.assertIn("Source roots: `src`", markdown)
        self.assertNotIn("tests/test_app.py", markdown)

    def test_hidden_source_directories_are_included(self) -> None:
        self.write_source(".hidden/module.py", "def f():\n    return 1\n")
        repository, _ = self.render()
        self.assertEqual([item.path for item in repository.files], [".hidden/module.py"])

    def test_generated_and_dependency_directories_are_excluded(self) -> None:
        for directory in (".venv/lib", "node_modules", ".git", ".hase"):
            self.write_source(f"{directory}/ignored.py", "invalid python ???\n")
        self.write_source("src/kept.py", "value = 1\n")
        repository, _ = self.render()
        self.assertEqual([item.path for item in repository.files], ["src/kept.py"])

    def test_editor_and_foreign_build_directories_are_excluded(self) -> None:
        for directory in (".idea", ".vscode", ".next", ".svelte-kit", "coverage"):
            self.write_source(f"{directory}/ignored.py", "invalid python ???\n")
        self.write_source("src/kept.py", "value = 1\n")
        repository, _ = self.render()
        self.assertEqual([item.path for item in repository.files], ["src/kept.py"])

    def test_file_limit_fails_instead_of_truncating(self) -> None:
        self.write_source("a.py", "value = 1\n")
        self.write_source("b.py", "value = 2\n")
        with self.assertRaisesRegex(GraphError, r"code file limit exceeded \(1\)"):
            build_repository(self.project_root, max_files=1)

    def test_no_code_files_is_an_actionable_error(self) -> None:
        with self.assertRaisesRegex(GraphError, "no recognized code files"):
            build_repository(self.project_root)

    def test_python_syntax_error_is_reported_without_losing_inventory(self) -> None:
        self.write_source("src/broken.py", "def nope(:\n")
        repository, markdown = self.render()
        self.assertEqual(len(repository.files), 1)
        self.assertEqual(len(repository.modules), 1)
        self.assertIn("## Python Parse Errors", markdown)
        self.assertIn("broken.py", markdown)
        self.assertIn("line 1", markdown)

    def test_ambiguous_module_name_is_reported_not_fatal(self) -> None:
        self.write_source("one/shared.py", "value = 1\n")
        self.write_source("two/shared.py", "value = 2\n")
        repository, markdown = self.render([Path("one"), Path("two")])
        self.assertIn("shared", repository.ambiguous)
        self.assertIn("## Ambiguous Python Modules", markdown)
        self.assertIn("`shared` appears more than once", markdown)

    def test_symbols_and_external_imports_are_bounded(self) -> None:
        methods = "\n".join(f"    def method_{index}(self):\n        return {index}" for index in range(8))
        self.write_source("src/app.py", f"import os\n\nclass Big:\n{methods}\n")
        _, markdown = self.render()
        self.assertIn("+2 more", markdown)
        self.assertNotIn("`src/app.py` -> `os`", markdown)
        self.assertIn("external/out-of-scope imports omitted", markdown)

    def test_output_budget_fails_instead_of_truncating(self) -> None:
        self.write_source("src/app.py", "def application_entry_point():\n    return True\n")
        repository = build_repository(self.project_root)
        with self.assertRaisesRegex(GraphError, "map exceeds --max-output-chars"):
            render_repository_map(repository, max_chars=32)

    def test_files_flag_includes_the_file_listing(self) -> None:
        self.write_source("src/app.py", "value = 1\n")
        _, markdown = self.render(include_files=True)
        self.assertIn("## Files", markdown)
        self.assertIn("`src/app.py` (Python)", markdown)

    def test_existing_handwritten_context_requires_explicit_force(self) -> None:
        destination = self.project_root / ".hase" / "context.md"
        destination.parent.mkdir()
        destination.write_text("handwritten context\n", encoding="utf-8")

        with self.assertRaisesRegex(GraphError, "refusing to replace handwritten"):
            write_graph(self.project_root, GENERATOR_MARKER + "\n# new\n")

        destination, changed = write_graph(self.project_root, GENERATOR_MARKER + "\n# new\n", force=True)
        self.assertTrue(changed)
        self.assertEqual(destination.read_text(encoding="utf-8"), GENERATOR_MARKER + "\n# new\n")

    def test_generated_context_is_idempotent(self) -> None:
        self.write_source("src/app.py", "def start():\n    return True\n")
        repository = build_repository(self.project_root)
        content = render_repository_map(repository)

        destination, created = write_graph(self.project_root, content)
        self.assertTrue(created)
        destination, changed = write_graph(self.project_root, content)
        self.assertFalse(changed)
        self.assertEqual(destination.read_text(encoding="utf-8"), content)

    def test_cli_writes_generated_map_and_reports_counts(self) -> None:
        self.write_source("src/app.py", "def start():\n    return True\n")
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            status = main(["--root", str(self.project_root)])
        self.assertEqual(status, 0)
        self.assertIn("updated", stdout.getvalue())
        self.assertIn("1 files", stdout.getvalue())
        self.assertTrue((self.project_root / ".hase" / "context.md").exists())

    def test_cli_rejects_user_context_and_supports_force(self) -> None:
        self.write_source("src/app.py", "def start():\n    return True\n")
        destination = self.project_root / ".hase" / "context.md"
        destination.parent.mkdir()
        destination.write_text("user notes\n", encoding="utf-8")

        with patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(main(["--root", str(self.project_root)]), 2)
        with patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(main(["--root", str(self.project_root), "--force"]), 0)
        self.assertIn(GENERATOR_MARKER, destination.read_text(encoding="utf-8"))

    def test_cli_files_flag_and_bounded_defaults(self) -> None:
        self.write_source("src/app.ts", "export const start = () => true;\n")
        with patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(main(["--root", str(self.project_root), "--files"]), 0)
        content = (self.project_root / ".hase" / "context.md").read_text(encoding="utf-8")
        self.assertIn("## Files", content)
        self.assertEqual(DEFAULT_MAX_FILES, 2_000)
        self.assertEqual(DEFAULT_MAX_OUTPUT_CHARS, 30_000)

    def test_cli_all_imports_includes_external_edges(self) -> None:
        self.write_source("src/app.py", "import os\n")
        with patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(main(["--root", str(self.project_root), "--all-imports"]), 0)
        content = (self.project_root / ".hase" / "context.md").read_text(encoding="utf-8")
        self.assertIn("`src/app.py` -> `os` [external/outside scope]", content)


if __name__ == "__main__":
    unittest.main()
