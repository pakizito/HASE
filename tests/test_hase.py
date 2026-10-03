#!/usr/bin/env python3
"""
Unit tests for HASE v7.0 toolkit & verification engine.
"""

import unittest
from pathlib import Path
import sys

# Ensure tools module can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from hase import calc_state, explain_state, format_hex_byte, parse_state_int, verify_output, install_rules


class TestHaseCore(unittest.TestCase):
    def test_format_hex_byte(self):
        self.assertEqual(format_hex_byte(0), "0x00")
        self.assertEqual(format_hex_byte(1), "0x01")
        self.assertEqual(format_hex_byte(77), "0x4D")
        self.assertEqual(format_hex_byte(255), "0xFF")

    def test_calc_state(self):
        # 1 (arch) + 4 (fault) + 8 (perf) + 64 (idiom) = 77 (0x4D)
        self.assertEqual(calc_state([0x01, 0x04, 0x08, 0x40]), 0x4D)
        # All planes: 1+2+4+8+16+32+64+128 = 255 (0xFF)
        self.assertEqual(calc_state([1, 2, 4, 8, 16, 32, 64, 128]), 0xFF)
        # Empty
        self.assertEqual(calc_state([]), 0x00)

    def test_explain_state(self):
        res = explain_state(0x4D)
        self.assertEqual(res["hex"], "0x4D")
        self.assertEqual(res["val"], 77)
        self.assertFalse(res["requires_tests"])
        active_slugs = [p["slug"] for p in res["active"]]
        self.assertEqual(active_slugs, ["arch", "fault", "perf", "idiom"])

        # State with testing enabled (0x20)
        res_test = explain_state(0x20)
        self.assertTrue(res_test["requires_tests"])

    def test_parse_state_int(self):
        self.assertEqual(parse_state_int("0x4D"), 77)
        self.assertEqual(parse_state_int("77"), 77)
        self.assertEqual(parse_state_int("0xFF"), 255)
        self.assertEqual(parse_state_int("0"), 0)

    def test_verify_output_success(self):
        sample = """[STATE: 0x4D]
[PLAN: Exponential-backoff loop | Resilient network handling | Thread exhaustion -> Bounded retry limits]
def fetch(url: str):
    pass
"""
        valid, issues = verify_output(sample)
        self.assertTrue(valid)
        self.assertEqual(issues, [])

    def test_verify_output_missing_state(self):
        sample = """def fetch(url: str):
    pass
"""
        valid, issues = verify_output(sample)
        self.assertFalse(valid)
        self.assertTrue(any("Line 1 must be formatted" in i for i in issues))

    def test_verify_output_invalid_plan(self):
        sample = """[STATE: 0x4D]
[PLAN: Just use requests]
def fetch(url: str):
    pass
"""
        valid, issues = verify_output(sample)
        self.assertFalse(valid)
        self.assertTrue(any("must have exactly 3 pipe-separated segments" in i for i in issues))

    def test_verify_output_forbidden_stub(self):
        sample = """[STATE: 0x4D]
[PLAN: Exponential-backoff loop | Resilient network handling | Thread exhaustion -> Bounded retry limits]
def fetch(url: str):
    TODO: finish this
"""
        valid, issues = verify_output(sample)
        self.assertFalse(valid)
        self.assertTrue(any("Forbidden placeholder/stub detected" in i for i in issues))

    def test_verify_output_testability_mandate(self):
        # 0x20 active without test block
        sample_no_test = """[STATE: 0x20]
[PLAN: Pure function design | Test isolation | State drift -> Pure functions]
def add(a, b):
    return a + b
"""
        valid, issues = verify_output(sample_no_test)
        self.assertFalse(valid)
        self.assertTrue(any("companion test blocks or assertions were detected" in i.lower() for i in issues))

        # 0x20 active WITH test block
        sample_with_test = """[STATE: 0x20]
[PLAN: Pure function design | Test isolation | State drift -> Pure functions]
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
"""
        valid, issues = verify_output(sample_with_test)
        self.assertTrue(valid)
        self.assertEqual(issues, [])

    def test_verify_output_with_memory_tag(self):
        sample = """[STATE: 0x4D]
[PLAN: Exponential-backoff loop | Resilient network handling | Thread exhaustion -> Bounded retry limits]
[MEM: Network | Retry backoff multiplier set to 2.0]
def fetch(url: str):
    pass
"""
        valid, issues = verify_output(sample)
        self.assertTrue(valid)
        self.assertEqual(issues, [])

    def test_ast_graph_and_export(self):
        import tempfile
        from hase import build_ast_graph, export_compact_graph
        with tempfile.TemporaryDirectory() as tmp_dir:
            p = Path(tmp_dir) / "demo.py"
            p.write_text("import os\n\nclass Demo:\n    def run(self, x: int) -> bool:\n        return True\n", encoding="utf-8")
            graph = build_ast_graph(Path(tmp_dir))
            self.assertEqual(graph["total_files"], 1)
            self.assertEqual(graph["files"][0]["file"], "demo.py")
            self.assertEqual(graph["files"][0]["classes"][0]["name"], "Demo")
            out = export_compact_graph(graph)
            self.assertIn("class Demo", out)
            self.assertIn("demo.py", out)

    def test_memory_ledger_operations(self):
        import tempfile
        from hase import add_memory_finding, add_memory_invariant, load_memory, clear_memory
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            f = add_memory_finding(workspace, "Auth", "Token expiry is 15m", ["auth.py"])
            self.assertEqual(f["topic"], "Auth")
            inv = add_memory_invariant(workspace, "Never mutate frozen dataclasses")
            self.assertEqual(inv, "Never mutate frozen dataclasses")

            mem = load_memory(workspace)
            self.assertEqual(len(mem["findings"]), 1)
            self.assertEqual(len(mem["invariants"]), 1)

            clear_memory(workspace)
            mem_cleared = load_memory(workspace)
            self.assertEqual(len(mem_cleared["findings"]), 0)

    def test_sync_command_flow(self):
        import tempfile
        from hase import build_ast_graph, export_compact_graph, load_memory, save_memory
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir)
            p = workspace / "service.py"
            p.write_text("class Service:\n    def execute(self):\n        pass\n", encoding="utf-8")
            hase_dir = workspace / ".hase"
            hase_dir.mkdir(parents=True, exist_ok=True)
            mem = load_memory(workspace)
            save_memory(workspace, mem)
            graph = build_ast_graph(workspace)
            (hase_dir / "context.md").write_text(export_compact_graph(graph), encoding="utf-8")

            self.assertTrue((hase_dir / "context.md").exists())
            self.assertTrue((hase_dir / "memory.json").exists())
            self.assertIn("class Service", (hase_dir / "context.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

