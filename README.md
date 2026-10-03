# HASE v7.0

### Make AI-assisted engineering more deliberate, reviewable, and context-aware.

HASE is a small, portable instruction set for coding agents. It gives agents a repeatable way to consider architecture, explain their approach, make focused changes, and verify the result—without requiring another agent runtime or hosted service.

HASE is designed to be useful from one IDE-specific instruction file. Optional project memory and a local Python context map can be added when they earn their keep; neither is required to start.

> **Guidance, not magic:** HASE helps agents follow a consistent process, but does not guarantee correctness or a particular reduction in tokens. Results still depend on the model, editor tools, and available workspace access.

## What HASE adds

| | |
| --- | --- |
| **Eight engineering lenses** | A compact bitmask reminds agents to consider architecture, state, defensive design, performance, observability, verification, idioms, and security. |
| **Clear response contract** | `[STATE]`, `[PLAN]`, and optional `[MEM]` make the selected review lenses, implementation approach, and durable findings easy to inspect. |
| **Focused code navigation** | Instructions prefer IDE symbols and targeted inspection. For Python, an optional local AST tool builds a compact module/import map on demand. |
| **Memory only when useful** | A documented JSON format preserves verified project facts without requiring an empty setup file or task log. |
| **No external dependency** | The instructions are plain files. The optional graph tool uses only Python’s standard library and makes no network or MCP calls. |

### The eight lenses

| Bit | Engineering lens | Consider |
| --- | --- | --- |
| `0x01` | Architecture | Boundaries, separation of concerns, loose coupling |
| `0x02` | State & lifecycle | Concurrency, immutability, cleanup, atomic changes |
| `0x04` | Defensive design | Validation, boundaries, explicit failure paths |
| `0x08` | Performance | Complexity, allocations, resource use |
| `0x10` | Observability | Logs, telemetry, useful error context |
| `0x20` | Verification | Testability, behavior checks, relevant validation |
| `0x40` | Idiomatic alignment | Language and ecosystem conventions |
| `0x80` | Security | Trust boundaries, secrets, least privilege |

For example, architecture + defensive design + performance + idiomatic alignment gives $0x01 \mathbin{|} 0x04 \mathbin{|} 0x08 \mathbin{|} 0x40 = 0x4D$.

A HASE-style response is compact and reviewable:

```text
[STATE: 0x4D]
[PLAN: Validate inputs | Fail early and clearly | Invalid data -> Reject before processing]
[MEM: API | Verified project constraint worth preserving]
```

## Add HASE to your editor

Choose **one** native instruction file and copy it to the matching path in your repository. Each file is self-contained; do not install every variant in the same project.

| IDE / agent | Instruction file |
| --- | --- |
| GitHub Copilot | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) |
| Cursor | [`.cursor/rules/hase.mdc`](.cursor/rules/hase.mdc) |
| Claude Code | [`CLAUDE.md`](CLAUDE.md) |
| Windsurf | [`.windsurfrules`](.windsurfrules) |
| Cline / Roo Code | [`.clinerules`](.clinerules) |
| Antigravity | [`.agents/rules/hase.md`](.agents/rules/hase.md) |
| Gemini | [`GEMINI.md`](GEMINI.md) |
| Aider | [`CONVENTIONS.md`](CONVENTIONS.md) |

The instruction file contains the HASE protocol, optional graph instructions, overwrite safeguards, and the complete memory schema and validation rules.

## Optional: build a Python context map

For cross-file Python work, explicitly run the graph tool from the target repository root:

```powershell
python tools/context_graph.py --root .
```

You can narrow the scan to one or more source roots:

```powershell
python tools/context_graph.py --root . --source src --source tests
```

To add this feature to another repository, copy [`tools/context_graph.py`](tools/context_graph.py) into its `tools/` directory. It requires Python 3.10 or later and uses only the standard library. It parses Python files with `ast`—it does not import or execute project code—and writes a deterministic, compact `.hase/context.md` map of top-level symbols and observed imports. Imports are syntax-level clues, not proof of runtime dependencies; external and out-of-scope imports are labeled accordingly.

The scanner skips common VCS, environment, cache, build, and dependency directories, but includes other hidden source directories. It fails instead of silently truncating above 400 Python files or 30,000 output characters. Use `python tools/context_graph.py --help` for options. The tool refuses to overwrite unmarked, hand-written context; inspect it before explicitly passing `--force`.

HASE’s `.gitignore` keeps its generated map local. In another repository, choose whether to commit `.hase/context.md` for teammates or add it to `.gitignore` for local-only use. Regenerate after meaningful Python structure or import changes. Treat the map as a cache: verify relevant source before relying on it. For other languages, use the IDE’s symbols/references and targeted inspection instead.

## Optional: preserve project memory

When useful facts accumulate, an agent may create `.hase/memory.json`. It is separate from the generated context map and is not created during setup. The IDE instructions define how to validate, update, and preserve this v7 JSON structure:

```json
{
  "version": "7.0",
  "updated_at": "2026-10-03T12:00:00Z",
  "findings": [
    {
      "id": "f-001",
      "topic": "API",
      "fact": "Access tokens expire after 15 minutes.",
      "files": ["src/auth.py"],
      "recorded_at": "2026-10-03T12:00:00Z"
    }
  ],
  "invariants": ["Pure logic stays decoupled from infrastructure I/O"]
}
```

Keep entries verified, durable, concise, and useful to future decisions. Preserve unrelated entries; exclude guesses, secrets, duplicates, and task history. Memory updates require workspace write access.

## Design principles

- **Explicit opt-in:** no startup hooks, background scans, or automatic graph writes.
- **Local by design:** graph generation requires no MCP, network access, package installation, or third-party service.
- **Source remains authoritative:** generated context and model-maintained memory can be stale; inspect the relevant code.
- **Start small:** add one instruction file first; enable Python context and memory only if they help your workflow.

Licensed under [MIT](LICENSE).
