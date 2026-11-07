# 0005 — One file, no context graph

- **Status:** Accepted
- **Date:** 2026-11-07
- **Deciders:** HASE maintainers

## Context

HASE v9 depended on generated adapters, a state validator, a polyglot context graph, and a detailed playbook. The graph did not earn its cost. It added a tool run, a cache file, and a maintenance surface. It also encouraged agents to inspect a map before they read the few files that mattered.

The product goal is one instruction file that a developer can copy into a repository. Extra instruction files and tools weaken that goal.

## Decision

HASE v10 is one self-contained file: `HASE.md`.

- Remove the context graph, its cache, its tests, and its documentation.
- Remove generated adapters, the adapter renderer, and the state validator.
- Remove the external playbook, STE reference, frame reference, and templates. Keep the rules inside `HASE.md`.
- Replace the graph with a read order and a stop rule: read the smallest surface, then stop when the change and test path are clear.
- Keep the frame, GRILL, memory protocol, checks, and safety rules.
- Keep `.hase/memory.json` as optional local data. It is not an instruction file.

## Consequences

**Positive**

- One file to copy, review, and version.
- Fewer steps and less context spent on tooling.
- No stale graph or adapter drift.
- The agent reads code and tests, not a proxy for them.

**Negative**

- No structural map for very large repositories.
- No validator for the frame.
- No pre-generated files for tools that need a specific filename.
- Detailed standards now live in a compact form instead of a long playbook.

## Alternatives considered

- **Embed a growing graph in `HASE.md`.** Rejected. A static file cannot grow per repository, and a generated section would make the file stale.
- **Keep the graph as an optional tool.** Rejected. Optional tooling still costs steps and invites the same failure.
- **Keep adapters as copies.** Rejected. A rename is enough, and copies drift.
- **Keep the playbook as an optional reference.** Rejected. It makes the one-file claim conditional.

## Follow-up

Use a repository-specific index only if a measured problem shows that targeted reading is insufficient. Do not add it to HASE by default.
