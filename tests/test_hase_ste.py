import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASE = ROOT / "HASE.md"


def prose_lines(text: str):
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line


class HaseContractTests(unittest.TestCase):
    def setUp(self):
        self.text = HASE.read_text(encoding="utf-8")

    def test_contract_is_one_self_contained_file(self):
        self.assertIn("one self-contained file", self.text)
        for required in ("HASE-STE", "ASD-STE100", "Schema v7", ".hase/memory.json"):
            self.assertIn(required, self.text)

    def test_no_external_instruction_dependency(self):
        for banned in ("docs/playbook.md", "docs/ste.md", "docs/hase-frame.md", "tools/context_graph.py", "tools/hase_state.py"):
            self.assertNotIn(banned, self.text)

    def test_graph_is_removed(self):
        self.assertIn("Do not build a context graph", self.text)
        self.assertIn("Do not build a graph", self.text)

    def test_no_generated_instruction_files(self):
        generated = [
            "AGENTS.md",
            "CLAUDE.md",
            "GEMINI.md",
            "CONVENTIONS.md",
            ".windsurfrules",
            ".clinerules",
            ".github/copilot-instructions.md",
            ".cursor/rules/hase.mdc",
            ".agents/rules/hase.md",
        ]
        found = [name for name in generated if (ROOT / name).exists()]
        self.assertEqual(found, [], "HASE must stay one instruction file")

    def test_contract_prose_has_no_semicolons(self):
        offenders = [line for line in prose_lines(self.text) if ";" in line]
        self.assertEqual(offenders, [], "HASE-STE forbids semicolons in prose")

    def test_contract_has_no_latin_abbreviations(self):
        offenders = [
            line
            for line in prose_lines(self.text)
            if re.search(r"\b(e\.g\.|i\.e\.|etc\.|vs\.)", line, re.IGNORECASE)
        ]
        self.assertEqual(offenders, [], "HASE-STE forbids Latin abbreviations")

    def test_contract_stays_under_size_limit(self):
        self.assertLess(HASE.stat().st_size, 10_000, "HASE.md exceeds 10 KB")


if __name__ == "__main__":
    unittest.main()
