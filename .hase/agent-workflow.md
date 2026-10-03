# HASE Agent-Managed Context & Memory Workflow

HASE has no runtime, CLI, build step, or code-generation dependency. The graph and memory features are maintained by the coding agent through the editor and workspace tools already available in the host environment. Updating either file requires workspace write access; without it, the agent can only present a proposed change.

## Codebase context graph

### At task start

1. Read `.hase/context.md` when it exists; use it to narrow exploration, not as a substitute for checking source files.
2. Read `.hase/memory.json` before changing code or project rules. Treat source files as authoritative if the graph or ledger conflicts with them.
3. If the graph is missing or clearly stale, inspect the relevant workspace before editing and update the graph with the available file-navigation, search, symbol, definition, reference, and call-hierarchy capabilities.

If there are no implementation changes yet, retain the previous graph; when initializing a missing graph, index project instructions, templates, configuration, and tests rather than inventing source-code symbols.

### Build or refresh

Maintain `.hase/context.md` as concise Markdown. Include the update date and coverage/limitations, then record relevant module paths, important imports/dependencies, public symbols and signatures, class relationships, and test/config entry points. Include line ranges when they can be verified; treat them as navigation hints because edits can make them stale.

Prefer language-server or editor symbol data when available. Otherwise inspect source files and create a best-effort index. Do not claim a complete AST, exact dependency graph, or full repository coverage unless the available tooling actually established it. Exclude generated, vendored, hidden, and ignored directories. For large repositories, index the relevant subset and state that scope rather than inventing completeness. Keep entries compact and paths consistently sorted.

Refresh the graph after adding, deleting, renaming, or moving modules, or after changing public signatures, imports, or class relationships. Do not rewrite it for ordinary implementation edits that do not affect structure. Confirm source text before relying on recorded line numbers.

### Suggested graph layout

```markdown
# CODEBASE CONTEXT GRAPH
*Agent-maintained | Updated: YYYY-MM-DD | Coverage: ...*

## Module and dependency topology
- `src/example.ts` -> [`src/models.ts`, `@/shared/logger`]

## Symbol hierarchy
### `src/example.ts`
- `class ExampleService` implements `ExamplePort`
- `function runExample(input: Input): Result` [L20-L42]

## Tests and configuration
- `tests/example.test.ts` -> tests `ExampleService`
```

Use only sections that apply to the repository. For documentation-only repositories, index the key documents and their roles instead of inventing code symbols.

When machine-readable graph output is explicitly requested, maintain `graph.json` with this best-effort, language-neutral shape. Omit unknown values instead of fabricating them:

```json
{
  "root": "workspace-relative root",
  "total_files": 1,
  "generated_at": "ISO-8601 UTC timestamp",
  "files": [
    {
      "file": "src/example.ts",
      "lines": 42,
      "imports": ["./models"],
      "symbols": [
        {"kind": "class", "name": "ExampleService", "signature": "ExampleService implements ExamplePort", "line_start": 10, "line_end": 30}
      ]
    }
  ],
  "dependencies": {"src/example.ts": ["./models"]}
}
```

Use workspace-relative forward-slash paths, sort file and dependency entries, and keep `total_files` consistent with `files`. This is an editor-derived index, not a parser-produced AST.

## Persistent memory ledger

Use `.hase/memory.json` with the existing schema:

```json
{
  "version": "7.0",
  "updated_at": "ISO-8601 UTC timestamp",
  "findings": [
    {
      "id": "f-001",
      "topic": "Area",
      "fact": "Verified finding or constraint",
      "files": ["path/to/file"],
      "recorded_at": "ISO-8601 UTC timestamp"
    }
  ],
  "invariants": ["Project-wide rule"]
}
```

Read and validate the existing JSON before editing. Preserve existing findings and invariants; append only durable, non-obvious information that will help future work. Use a unique sequential finding ID, include relevant paths, update UTC timestamps, and avoid duplicate invariants. Never silently replace malformed or unreadable memory with an empty ledger. Do not clear or remove entries unless explicitly requested. If the ledger is missing, initialize it with the schema above.

When a new durable discovery is recorded, include `[MEM: Topic | Finding]` in the task response and persist that finding in the ledger. Do not store secrets or transient implementation details.

## Agent-operated HASE features

- **Calculate a state:** bitwise-OR selected plane values; report the byte, decimal value, binary value, and active planes. Accept only values in the byte range `0..255` and known plane flags/slugs.
- **Explain a state:** accept decimal or hexadecimal byte input; report active/inactive planes and whether tests are mandated. Reject values outside `0..255` rather than silently wrapping them.
- **Verify output:** inspect the first non-empty line for `[STATE: 0xNN]`; require a second line with exactly three non-empty `[PLAN: Approach | Rationale | Risk -> Mitigation]` segments and `->` in the third; allow one optional `[MEM: Topic | Finding]` line next. Check the remaining content for placeholders and, when bit `0x20` is active, require actual companion test code or tests in the changed project. Report specific issues; do not claim static proof from keyword matches alone.
- **Sync context and memory:** inspect/refresh the graph as needed and validate that the ledger exists and is valid JSON; preserve user data.
- **List, add, or clear memory:** inspect and summarize the ledger, append durable findings/invariants, or clear only on explicit request.
- **Initialize another workspace:** install the selected HASE instruction files and this workflow document using workspace file operations; create `.hase/context.md` and `.hase/memory.json` only when absent. Preserve existing user files and data; ask before overwriting or replacing them.

These operations are agent-guided, not deterministic commands. Their completeness depends on the host agent's access to workspace files and language services. Do not ask the user to install Python or run a HASE script.
