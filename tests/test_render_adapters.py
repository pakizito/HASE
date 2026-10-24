from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.render_adapters import MARKER, TARGETS, canonical_body, compose, render_all


class RenderAdaptersTests(unittest.TestCase):
    def test_body_drops_only_the_canonical_h1(self) -> None:
        body = canonical_body("# Canonical\n\n## Section\n\nText.\n")
        self.assertNotIn("Canonical", body)
        self.assertIn("## Section", body)
        self.assertTrue(body.endswith("\n"))

    def test_compose_preserves_frontmatter_and_marker_order(self) -> None:
        target = next(item for item in TARGETS if item.path.endswith(".mdc"))
        rendered = compose("# Canonical\n\nBody.\n", target)
        self.assertTrue(rendered.startswith("---\n"))
        self.assertLess(rendered.index("---", 4), rendered.index(MARKER))
        self.assertLess(rendered.index(MARKER), rendered.index("# HASE v8.0 — Cursor"))
        self.assertTrue(rendered.endswith("\n"))
        self.assertNotIn("\r\n", rendered)

    def test_all_adapters_are_generated_from_canonical_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "HASE.md").write_text("# Canonical\n\nShared rule.\n", encoding="utf-8")
            rendered = render_all(root)

        self.assertEqual(set(rendered), {target.path for target in TARGETS})
        for content in rendered.values():
            self.assertIn(MARKER, content)
            self.assertIn("Shared rule.", content)
            self.assertNotIn("Canonical", content)

    def test_repository_adapters_are_in_sync(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for relative, expected in render_all(root).items():
            path = root / relative
            self.assertTrue(path.exists(), relative)
            self.assertEqual(path.read_bytes(), expected.encode("utf-8"), relative)


if __name__ == "__main__":
    unittest.main()
