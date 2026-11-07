import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prose_lines(text: str):
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line


class HaseSteTests(unittest.TestCase):
    def test_contract_names_the_style_and_the_source(self):
        text = (ROOT / "HASE.md").read_text(encoding="utf-8")
        self.assertIn("HASE-STE", text)
        self.assertIn("ASD-STE100", text)
        self.assertIn("docs/ste.md", text)

    def test_reference_exists_and_does_not_claim_certification(self):
        text = (ROOT / "docs" / "ste.md").read_text(encoding="utf-8").lower()
        self.assertIn("not certified", text)
        self.assertIn("asd-ste100", text)

    def test_contract_prose_has_no_semicolons(self):
        text = (ROOT / "HASE.md").read_text(encoding="utf-8")
        offenders = [line for line in prose_lines(text) if ";" in line]
        self.assertEqual(offenders, [], "HASE-STE forbids semicolons in prose")

    def test_contract_has_no_latin_abbreviations(self):
        text = (ROOT / "HASE.md").read_text(encoding="utf-8")
        offenders = [
            line
            for line in prose_lines(text)
            if re.search(r"\b(e\.g\.|i\.e\.|etc\.|vs\.)", line, re.IGNORECASE)
        ]
        self.assertEqual(offenders, [], "HASE-STE forbids Latin abbreviations")


if __name__ == "__main__":
    unittest.main()
