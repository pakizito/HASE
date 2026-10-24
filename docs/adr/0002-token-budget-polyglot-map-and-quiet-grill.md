# 0002 — Token budget, polyglot map, and quiet GRILL

- **Status:** Accepted
- **Date:** 2026-10-24
- **Deciders:** HASE maintainers

## Context

HASE v8 improved process quality but produced a roughly 23 KB adapter. That is expensive for a tool whose purpose is to optimise token use. It also made two assumptions that did not survive use:

1. The context graph only worked for Python repositories.
2. GRILL risked turning every uncertainty into a question, which adds friction instead of reducing it.

The desired behaviour is a compact default contract, a repository map that works for any codebase, and a decision interview that stays quiet unless a choice is genuinely blocking.

## Decision

Adopt HASE v9 with:

- a roughly 10 KB compact core, enforced by an 11 KB adapter-size test;
- detailed standards moved to `docs/playbook.md` and loaded only when needed;
- a polyglot context map that inventories any codebase by directory and language, adds Python symbols/imports, reports Python parse errors without discarding the inventory, and makes a full file listing opt-in;
- quiet GRILL: resolve facts and sensible defaults first, ask only when the answer changes behaviour, security, data, cost, or an irreversible action, with a three-question blocking budget;
- `AGENTS.md` as the ninth generated adapter.

## Consequences

**Positive**

- The default context cost is roughly halved.
- The map is useful in mixed-language and non-Python repositories.
- GRILL remains available without making the user answer routine questions.
- Detailed guidance is still available through progressive disclosure.

**Negative**

- Non-Python dependency edges are not semantically parsed; the map is structural, not a full call graph.
- The compact core relies on the agent loading the playbook when a task needs deeper standards.
- The 11 KB test caps future additions and may force a deliberate split.

## Alternatives considered

- **Keep the v8 contract and rely on model context windows.** Rejected: it contradicts the token-optimizer goal.
- **Make every adapter a link to `HASE.md`.** Rejected: many IDE agents do not load linked files reliably.
- **Add tree-sitter or language servers for every language.** Rejected for the default: dependencies and installation complexity outweigh the benefit. Python AST remains the semantic path; other languages are inventoried structurally.
- **Remove GRILL.** Rejected: the approach is useful; the problem was frequency, not existence.

## Follow-up

- Measure whether the compact core changes task quality in real repositories.
- Add language-specific semantic parsing only if a repeated need is demonstrated.
- Revisit the question budget after several GRILL sessions.
