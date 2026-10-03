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
    build_graph,
    main,
    render_graph,
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

    def test_builds_sorted_top_level_symbols_and_import_edges(self) -> None:
        self.write_source(
            "app/__init__.py",
            "from .service import run\n",
        )
        self.write_source(
            "app/service.py",
            "import json\nfrom .util import helper\n\nclass Service:\n    def call(self):\n        return helper()\n\nasync def run(value: str) -> str:\n    return value\n",
        )
        self.write_source("app/util.py", "def helper():\n    return 1\n")
        self.write_source("other/not-importable.py", "value = 1\n")

        modules = build_graph(self.project_root)

        self.assertEqual(
            [module.path for module in modules],
            ["app/__init__.py", "app/service.py", "app/util.py", "other/not-importable.py"],
        )
        service = next(module for module in modules if module.path == "app/service.py")
        self.assertEqual(
            service.symbols,
            ("class Service L4-L6 (call)", "async function run L8-L9"),
        )

        markdown = render_graph(self.project_root, None, modules)
        self.assertIn(GENERATOR_MARKER, markdown)
        self.assertIn("`app/service.py` -> `app.util` [in-scope: `app/util.py` (app/util.py)]", markdown)
        self.assertIn("`app/service.py` -> `json` [external/outside scope]", markdown)
        self.assertIn("`app/__init__.py` -> `app.service` [in-scope: `app/service.py` (app/service.py)]", markdown)
        self.assertIn("`other/not-importable.py` (not import-resolvable)", markdown)

    def test_absolute_from_imports_resolve_and_leave_external_unresolved(self) -> None:
        self.write_source("pkg/__init__.py", "value = 1\n")
        self.write_source("pkg/api.py", "from pkg import value\nfrom json import loads\n")
        modules = build_graph(self.project_root)
        markdown = render_graph(self.project_root, None, modules)
        self.assertIn("`pkg/api.py` -> `pkg` [in-scope: `pkg/__init__.py` (pkg/__init__.py)]", markdown)
        self.assertIn("`pkg/api.py` -> `json` [external/outside scope]", markdown)

    def test_relative_imports_resolve_from_package_and_module(self) -> None:
        self.write_source("pkg/__init__.py", "from .api import run\n")
        self.write_source("pkg/api.py", "from .service import Service\n")
        self.write_source("pkg/service.py", "class Service:\n    pass\n")

        modules = build_graph(self.project_root)
        markdown = render_graph(self.project_root, None, modules)

        self.assertIn("`pkg/__init__.py` -> `pkg.api` [in-scope: `pkg/api.py` (pkg/api.py)]", markdown)
        self.assertIn("`pkg/api.py` -> `pkg.service` [in-scope: `pkg/service.py` (pkg/service.py)]", markdown)

    def test_explicit_source_roots_are_respected(self) -> None:
        self.write_source("src/pkg/app.py", "import pkg.helper\n")
        self.write_source("src/pkg/helper.py", "value = 1\n")
        self.write_source("tests/test_app.py", "from pkg.app import run\n")

        modules = build_graph(self.project_root, [Path("src")])
        self.assertEqual([module.path for module in modules], ["src/pkg/app.py", "src/pkg/helper.py"])
        markdown = render_graph(self.project_root, [Path("src")], modules)
        self.assertIn("Source roots: `src`", markdown)

    def test_hidden_source_directories_are_included(self) -> None:
        self.write_source(".hidden/module.py", "def f():\n    return 1\n")
        modules = build_graph(self.project_root)
        self.assertEqual([module.path for module in modules], [".hidden/module.py"])

    def test_generated_and_dependency_directories_are_excluded(self) -> None:
        self.write_source(".venv/lib/ignored.py", "invalid python ???\n")
        self.write_source("node_modules/ignored.py", "invalid python ???\n")
        self.write_source(".git/ignored.py", "invalid python ???\n")
        self.write_source("src/kept.py", "value = 1\n")
        modules = build_graph(self.project_root)
        self.assertEqual([module.path for module in modules], ["src/kept.py"])

    def test_file_limit_fails_instead_of_truncating(self) -> None:
        self.write_source("a.py", "value = 1\n")
        self.write_source("b.py", "value = 2\n")
        with self.assertRaisesRegex(GraphError, r"file limit exceeded \(1\)"): 
            build_graph(self.project_root, max_files=1)

    def test_no_python_files_is_an_actionable_error(self) -> None:
        with self.assertRaisesRegex(GraphError, "no Python files found"):
            build_graph(self.project_root)

    def test_syntax_error_includes_file_and_line(self) -> None:
        self.write_source("src/broken.py", "def nope(:\n")
        with self.assertRaisesRegex(GraphError, "broken.py.*line 1"):
            build_graph(self.project_root)

    def test_ambiguous_module_name_fails_explicitly(self) -> None:
        self.write_source("one/shared.py", "value = 1\n")
        self.write_source("two/shared.py", "value = 2\n")
        with self.assertRaisesRegex(GraphError, "ambiguous module 'shared'"):  
            build_graph(self.project_root, [Path("one"), Path("two")])

    def test_output_budget_fails_instead_of_truncating(self) -> None:
        self.write_source("src/app.py", "def application_entry_point():\n    return True\n")
        modules = build_graph(self.project_root)
        with self.assertRaisesRegex(GraphError, "map exceeds --max-output-chars"):
            render_graph(self.project_root, None, modules, max_chars=32)

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
        modules = build_graph(self.project_root)
        content = render_graph(self.project_root, None, modules)

        destination, created = write_graph(self.project_root, content)
        self.assertTrue(created)
        destination, changed = write_graph(self.project_root, content)
        self.assertFalse(changed)
        self.assertEqual(destination.read_text(encoding="utf-8"), content)

    def test_cli_writes_generated_map_and_requires_root(self) -> None:
        self.write_source("src/app.py", "def start():\n    return True\n")
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            status = main(["--root", str(self.project_root)])
        self.assertEqual(status, 0)
        self.assertIn("updated", stdout.getvalue())
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

    def test_cli_defaults_are_bounded(self) -> None:
        self.assertEqual(DEFAULT_MAX_FILES, 400)
        self.assertEqual(DEFAULT_MAX_OUTPUT_CHARS, 30_000)


if __name__ == "__main__":
    unittest.main()
