# CODEBASE CONTEXT GRAPH
*Updated: 2026-10-03 | Code/test: FULL 0/0 | Docs/config: FULL 18/18 tracked files (license separate); excluded: VCS metadata.*

## Project
- Documentation/configuration-only prompt protocol; no executable, runtime, tests, build, or lint commands.
- `.hase/agent-workflow.md` -> 500-token graph budget; silent execution; selective navigation, structural refresh, curated memory.
- `.hase/memory.json` -> durable findings and invariants.
- `README.md` defines the 8-plane matrix, output modes, and token-lean agent-operated features.

## Instructions and templates
- `.github/copilot-instructions.md`, `.cursor/rules/hase.mdc`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.agents/rules/hase.md`, `.sourcegraph/hase.rule.md`, `CLAUDE.md`, `CONVENTIONS.md`, `GEMINI.md` -> tool-specific rules; all defer graph/memory updates to `.hase/agent-workflow.md`.
- `templates/hase-system-prompt.md`, `templates/hase-system-prompt.txt`, `templates/hase-compact.txt` -> standalone full/compact prompt variants; graph/memory behavior follows `.hase/agent-workflow.md`.
- `.gitignore` -> OS-generated and IDE exclusions; no environment/cache ignores remain.
- `.hase/context.md` -> this navigation index; `.hase/memory.json` -> findings and invariants.

## Limitations
- Workspace contains no executable, automated test suite, language-source files, virtual environment, or cache artifacts; graph/memory updates use host workspace file access.
- Graph is intentionally token-lean: use relevant entries and inspect source on demand; routine edits do not trigger a full rebuild.
