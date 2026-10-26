from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from tools.hase_state import BITS, decode, describe, encode, main, parse_frame


class HaseStateTests(unittest.TestCase):
    def test_decode_example(self) -> None:
        self.assertEqual(decode("0x4D"), 0x4D)
        self.assertEqual(
            describe(0x4D),
            "0x4D = idioms (idiomatic alignment), performance (performance/resources), defensive (defensive design), architecture (architecture/boundaries)",
        )

    def test_encode_is_case_and_alias_friendly(self) -> None:
        self.assertEqual(encode(["A", "defense", "PERF", "idioms"]), 0x4D)
        self.assertEqual(encode(["architecture,defensive,performance,idiomatic"]), 0x4D)

    def test_round_trip(self) -> None:
        for state in range(256):
            names = [name for mask, name, _ in BITS if state & mask]
            if names:
                self.assertEqual(encode(names), state)

    def test_invalid_state_and_lens(self) -> None:
        for value in ("0x100", "GG", "4", "0x4"):
            with self.assertRaises(ValueError):
                decode(value)
        with self.assertRaisesRegex(ValueError, "unknown lens"):
            encode(["architecture", "nonsense"])
        with self.assertRaisesRegex(ValueError, "at least one lens"):
            encode([])

    def test_parse_frame_and_cli_check(self) -> None:
        frame = parse_frame(
            "[STATE: 0x25]\n"
            "[PLAN: replace parser | legacy input -> fixture]\n"
            "[SUMMARY: parser fixed | verify: 27 tests pass | risk: none]\n"
        )
        self.assertEqual(frame.state, 0x25)
        self.assertEqual(frame.bits, ("verification", "defensive", "architecture"))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "frame.txt"
            path.write_text(
                "[STATE: 0x25]\n[PLAN: replace parser | risk -> fixture]\n[SUMMARY: fixed | verify: tests | risk: none]\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(main(["check", str(path)]), 0)
            self.assertIn("ok 0x25", stdout.getvalue())

    def test_cli_rejects_missing_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "frame.txt"
            path.write_text("[STATE: 0x01]\n[PLAN: test]\n", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(main(["check", str(path)]), 2)
            self.assertIn("[SUMMARY: ...]", stderr.getvalue())

    def test_cli_rejects_zero_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "frame.txt"
            path.write_text(
                "[STATE: 0x00]\n[PLAN: no lens]\n[SUMMARY: skip | verify: none | risk: none]\n",
                encoding="utf-8",
            )
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(main(["check", str(path)]), 2)
            self.assertIn("skip the frame", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
