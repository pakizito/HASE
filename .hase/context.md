# CODEBASE CONTEXT GRAPH
*Agent-maintained | Updated: 2026-10-03 | Coverage: HASE documentation, instruction files, prompt templates, and workspace ledger; source tooling and automated HASE tests were removed.*

## Project structure
- `README.md` -> Protocol description, eight-plane matrix, integrations, examples, and agent-operated feature guide.
- `CLAUDE.md`, `CONVENTIONS.md`, `GEMINI.md` -> Claude, Aider, and Gemini/Antigravity project instructions.
- `.github/copilot-instructions.md`, `.cursor/rules/hase.mdc`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.agents/rules/hase.md`, `.sourcegraph/hase.rule.md` -> Agent-specific instructions; all delegate context/memory behavior to `.hase/agent-workflow.md`.
- `.hase/agent-workflow.md` -> Shared Python-free graph and persistent-memory procedures.
- `.hase/memory.json` -> Durable project findings and invariants.
- `templates/hase-system-prompt.md`, `templates/hase-system-prompt.txt`, `templates/hase-compact.txt` -> Long and compact prompt variants.
- `LICENSE` -> MIT license.

## Workflow relationships
- Workspace-specific instructions use `.hase/agent-workflow.md` as the shared source of truth for graph refresh and ledger edits.
- `.hase/context.md` is an agent-maintained, best-effort navigation index, not a parser-generated AST.
- Graph and memory operations require the host agent's workspace-file access; HASE has no executable, runtime, CLI, or automated test runner.
