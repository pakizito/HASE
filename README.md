# HASE v10.1

### One self-contained instruction file for AI-assisted software development.

HASE gives a coding agent a short, repeatable way to understand a repository, make a focused change, verify it, and hand it back without flooding the context window.

`HASE.md` is the product. It is plain Markdown. It needs no graph tool, no cache, no adapters, and no second instruction file.

## Install for any IDE

Copy [`HASE.md`](HASE.md) into your project under the filename your agent reads. Use one copy per repository.

| IDE or agent | Instruction file | Note |
| --- | --- | --- |
| Codex and AGENTS.md-compatible agents | `AGENTS.md` | Most portable option. |
| Claude Code | `CLAUDE.md` | Plain Markdown. |
| Gemini | `GEMINI.md` | Plain Markdown. |
| GitHub Copilot | `.github/copilot-instructions.md` | Plain Markdown. |
| Cursor | `.cursor/rules/hase.mdc` | Add the frontmatter below. |
| Windsurf | `.windsurfrules` | Plain text. |
| Cline and Roo Code | `.clinerules` | Plain text. |
| Aider | `CONVENTIONS.md` | Plain Markdown. |
| Antigravity | `.agents/rules/hase.md` | Plain Markdown. |
| Continue | `.continue/rules/hase.md` | Plain Markdown. |
| Amazon Q Developer | `.amazonq/rules/hase.md` | Plain Markdown. |
| Tabnine | `.tabnine/guidelines/hase.md` | Plain Markdown. |
| Zed | `AGENTS.md` | Uses the AGENTS.md convention. |
| Other agents | Filename the agent reads | HASE is vendor-neutral Markdown. |

For Cursor, put this frontmatter above the HASE title:

```yaml
---
description: HASE engineering contract
globs: ["**/*"]
alwaysApply: true
---
```

Do not install several copies in the same repository. If your agent supports `AGENTS.md`, use it first.

## What is in the file

- Priorities and token discipline.
- HASE-STE: short sentences, active voice, one term for one concept.
- A read order from C0 to C2.
- Triage from T0 to T3.
- The `[STATE]`, `[PLAN]`, and `[SUMMARY]` frame.
- GRILL, PLAN, BUILD, DEBUG, REVIEW, and SHIP modes.
- Core checks for architecture, security, data, runtime, AI, and supply chain.
- Definition of done, stop conditions, and anti-patterns.
- Optional local memory in `.hase/memory.json`.

## Why the context graph is gone

The graph added a tool run, a cache file, and another thing to keep true. It did not save enough reading to pay for those steps. HASE now uses a simpler rule:

1. Read the smallest surface.
2. Stop when the change and test path are clear.
3. Use search and IDE symbols when the code is not enough.

Do not create a graph. If an old `.hase/context.md` exists, ignore it. Code and tests are the source of truth.

## Memory

Memory is optional data, not a second instruction file. It stores only verified, durable facts.

```json
{
  "version": "7.0",
  "findings": [
    {
      "id": "f-001",
      "topic": "API",
      "fact": "Access tokens expire after 15 minutes.",
      "files": ["src/auth.py"]
    }
  ]
}
```

Keep entries small. Use repository-relative evidence. Do not store secrets, personal data, guesses, or task history. If memory conflicts with code, code wins. Put durable decisions in `docs/adr/`.

## The frame

Use the frame for T1 and T2 code changes and reviews. Skip it for T0 and ordinary chat.

```text
[STATE: 0x25]
[PLAN: replace parser branch | legacy input -> fixture]
...
[SUMMARY: parser fixed | verify: 27 tests pass | risk: none]
```

Bits, high to low: `80` security, `40` idioms, `20` verification, `10` observability, `08` performance, `04` defensive design, `02` state/lifecycle, `01` architecture.

Set only bits that you act on. Every set bit needs evidence. The byte is a commitment header, not a compression of reasoning.

## Maintain

Edit `HASE.md` only. Do not add generated instruction files, a context graph, or a second instruction source.

```powershell
python -m unittest discover -s tests -t . -v
```

Material decisions belong in `docs/adr/`. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before a change.

## Status

HASE version: **10.1.0**. Memory schema: **7.0**.

HASE improves process discipline. It does not guarantee correctness, security, or a specific token reduction. Results depend on the model, tools, repository, and review.

## License

See [`LICENSE`](LICENSE). Report security issues through [`SECURITY.md`](SECURITY.md).
