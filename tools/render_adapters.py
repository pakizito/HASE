"""Render the self-contained HASE adapter files from HASE.md."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


MARKER = "<!-- Generated from HASE.md by tools/render_adapters.py. In the HASE repository, edit HASE.md and regenerate; a copied adapter may be adapted for its target project. -->"


@dataclass(frozen=True)
class Target:
    path: str
    title: str
    frontmatter: str = ""


TARGETS: tuple[Target, ...] = (
    Target("AGENTS.md", "HASE v8.0 — AGENTS.md / Codex"),
    Target("CLAUDE.md", "HASE v8.0 — Claude Code"),
    Target("GEMINI.md", "HASE v8.0 — Gemini"),
    Target(".github/copilot-instructions.md", "HASE v8.0 — GitHub Copilot"),
    Target(
        ".cursor/rules/hase.mdc",
        "HASE v8.0 — Cursor",
        """---
description: HASE v8 engineering contract for Cursor
globs: "**/*"
alwaysApply: true
---""",
    ),
    Target(".windsurfrules", "HASE v8.0 — Windsurf"),
    Target(".clinerules", "HASE v8.0 — Cline / Roo Code"),
    Target(".agents/rules/hase.md", "HASE v8.0 — Antigravity & Agentic Systems"),
    Target("CONVENTIONS.md", "HASE v8.0 — Aider"),
)


def canonical_body(canonical_text: str) -> str:
    """Return the canonical instructions without the source H1."""
    lines = canonical_text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("HASE.md must start with an H1 title")
    body = "\n".join(lines[1:]).lstrip("\n")
    if not body.strip():
        raise ValueError("HASE.md must contain instructions after the H1 title")
    return body.rstrip("\n") + "\n"


def compose(canonical_text: str, target: Target) -> str:
    """Compose one adapter with a target-specific header and canonical body."""
    parts: list[str] = []
    if target.frontmatter:
        parts.append(target.frontmatter.strip())
    parts.append(MARKER)
    parts.append(f"# {target.title}")
    parts.append(canonical_body(canonical_text))
    return "\n\n".join(parts)


def render_all(root: Path) -> dict[str, str]:
    """Return every generated adapter keyed by repository-relative path."""
    canonical = (root / "HASE.md").read_text(encoding="utf-8")
    return {target.path: compose(canonical, target) for target in TARGETS}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root containing HASE.md (default: parent of tools/)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if any adapter is missing or differs from HASE.md",
    )
    args = parser.parse_args(argv)

    try:
        rendered = render_all(args.root)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if args.check:
        stale = []
        for relative, expected in rendered.items():
            path = args.root / relative
            if not path.exists() or path.read_bytes() != expected.encode("utf-8"):
                stale.append(relative)
        if stale:
            print("out of date: " + ", ".join(stale), file=sys.stderr)
            print("run: python tools/render_adapters.py", file=sys.stderr)
            return 1
        print(f"{len(rendered)} adapters are up to date")
        return 0

    for relative, content in rendered.items():
        path = args.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))
    print(f"wrote {len(rendered)} adapters from HASE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
