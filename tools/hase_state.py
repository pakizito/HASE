#!/usr/bin/env python3
"""Encode, decode, and validate the HASE state byte and frame.

Examples:
    python tools/hase_state.py decode 0x4D
    python tools/hase_state.py encode architecture defensive performance idioms
    python tools/hase_state.py check frame.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

BITS: tuple[tuple[int, str, str], ...] = (
    (0x80, "security", "security/privacy"),
    (0x40, "idioms", "idiomatic alignment"),
    (0x20, "verification", "tests/evidence"),
    (0x10, "observability", "logs/metrics/traces"),
    (0x08, "performance", "performance/resources"),
    (0x04, "defensive", "defensive design"),
    (0x02, "state", "state/lifecycle"),
    (0x01, "architecture", "architecture/boundaries"),
)
ALIASES = {
    "a": "architecture", "arch": "architecture", "architecture": "architecture",
    "s": "state", "lifecycle": "state", "state": "state",
    "d": "defensive", "defense": "defensive", "defensive": "defensive",
    "p": "performance", "perf": "performance", "performance": "performance",
    "o": "observability", "observability": "observability",
    "v": "verification", "verify": "verification", "verification": "verification",
    "i": "idioms", "idiom": "idioms", "idioms": "idioms", "idiomatic": "idioms",
    "x": "security", "security": "security", "privacy": "security",
}
STATE_RE = re.compile(r"\[STATE:\s*(0x[0-9a-fA-F]{2})\s*\]")
PLAN_RE = re.compile(r"\[PLAN:\s*[^\]]+\]")
SUMMARY_RE = re.compile(r"\[SUMMARY:\s*[^\]]+\]")


@dataclass(frozen=True)
class Frame:
    state: int
    plan: str
    summary: str

    @property
    def bits(self) -> tuple[str, ...]:
        return tuple(name for mask, name, _ in BITS if self.state & mask)


def decode(value: str | int) -> int:
    if isinstance(value, int):
        state = value
    else:
        text = value.strip().lower()
        if text.startswith("0x"):
            text = text[2:]
        if len(text) != 2:
            raise ValueError("state must be two hexadecimal digits, e.g. 0x4D")
        try:
            state = int(text, 16)
        except ValueError as error:
            raise ValueError(f"invalid hexadecimal state: {value!r}") from error
    if not 0 <= state <= 0xFF:
        raise ValueError("state must be between 0x00 and 0xFF")
    return state


def encode(names: list[str]) -> int:
    selected: set[str] = set()
    for raw in names:
        for part in raw.replace(",", " ").split():
            key = part.strip().lower()
            if key not in ALIASES:
                raise ValueError(f"unknown lens: {part!r}")
            selected.add(ALIASES[key])
    if not selected:
        raise ValueError("select at least one lens")
    state = 0
    for mask, name, _ in BITS:
        if name in selected:
            state |= mask
    return state


def describe(state: int) -> str:
    names = [f"{name} ({label})" for mask, name, label in BITS if state & mask]
    return f"0x{state:02X} = " + (", ".join(names) if names else "no lenses")


def parse_frame(text: str) -> Frame:
    state_match = STATE_RE.search(text)
    plan_match = PLAN_RE.search(text)
    summary_match = SUMMARY_RE.search(text)
    missing = []
    if state_match is None:
        missing.append("[STATE: 0xNN]")
    if plan_match is None:
        missing.append("[PLAN: ...]")
    if summary_match is None:
        missing.append("[SUMMARY: ...]")
    if missing:
        raise ValueError("missing frame line(s): " + ", ".join(missing))
    assert state_match is not None and plan_match is not None and summary_match is not None
    return Frame(
        state=decode(state_match.group(1)),
        plan=plan_match.group(0),
        summary=summary_match.group(0),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_decode = sub.add_parser("decode", help="decode a hex state")
    p_decode.add_argument("state")

    p_encode = sub.add_parser("encode", help="encode lens names")
    p_encode.add_argument("lenses", nargs="+")

    p_check = sub.add_parser("check", help="validate a frame from a file or stdin")
    p_check.add_argument("path", nargs="?", default="-")

    args = parser.parse_args(argv)
    try:
        if args.command == "decode":
            state = decode(args.state)
            print(describe(state))
            return 0
        if args.command == "encode":
            state = encode(args.lenses)
            print(f"0x{state:02X}")
            return 0
        if args.command == "check":
            if args.path == "-":
                text = sys.stdin.read()
            else:
                text = Path(args.path).read_text(encoding="utf-8")
            frame = parse_frame(text)
            if frame.state == 0:
                raise ValueError("0x00 means no lens applies; skip the frame instead")
            print(f"ok {describe(frame.state)}")
            print(frame.plan)
            print(frame.summary)
            return 0
    except (OSError, ValueError) as error:
        print(f"hase_state: error: {error}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
