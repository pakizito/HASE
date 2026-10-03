# HASE v7.0

Portable agent instructions, plus an optional local Python context-map generator. No package dependencies, MCP services, network access, or background automation.

## Choose one IDE instruction file

| IDE/agent | Instruction file |
| --- | --- |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/hase.mdc` |
| Claude Code | `CLAUDE.md` |
| Windsurf | `.windsurfrules` |
| Cline / Roo Code | `.clinerules` |
| Antigravity | `.agents/rules/hase.md` |
| Gemini | `GEMINI.md` |
| Aider | `CONVENTIONS.md` |

Each instruction file is standalone. It includes the HASE protocol, optional Python graph command and safety behavior, and the exact v7 memory JSON schema.

## Optional Python context map

From your repository root, explicitly run:

```powershell
python tools/context_graph.py --root .
```

To restrict scanning to source roots:

```powershell
python tools/context_graph.py --root . --source src --source tests
```

Copy `tools/context_graph.py` into the target repository to install the optional program; the IDE instruction file alone does not provide it. The Python 3.10+ standard-library tool parses Python AST only, extracts top-level symbols/imports, and writes generated `.hase/context.md`. It skips common VCS, environment, cache, build, and dependency directories; hidden source directories are included. It fails (never silently truncates) above 400 files or 30,000 output characters. Run `python tools/context_graph.py --help` for options.

The tool does not overwrite existing handwritten context unless `--force` is explicitly supplied. Review existing contents before forcing. Regenerate after meaningful Python structure/import changes. The map is a stale-able index, not source truth; non-Python projects should use IDE symbols and targeted inspection.

## Memory

`.hase/memory.json` is optional and is not created during installation. See your IDE instruction file for the schema and rules for recording only verified, durable facts. Read it only when relevant; preserve existing entries.

HASE has no automatic startup hooks, watchers, services, or external-tool dependencies. The user or agent invokes the graph command explicitly when its output is worth the cost.
