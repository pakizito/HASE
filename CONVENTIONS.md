# HASE v7.0 ARCHITECTURAL CONVENTIONS FOR AIDER
Universal AI Developer Co-Pilot · Optimized for Metered & Low-Parameter LLMs

## 1. Architectural Bitmask Mandate
Before editing code, mentally audit the task against the HASE v7.0 8-plane cognitive matrix:
- 0x01 (1): Macro-Architecture (SOLID, modular boundaries, loose coupling)
- 0x02 (2): State & Lifecycle (Concurrency safety, immutability, deterministic cleanup via RAII/defer)
- 0x04 (4): Defensive Design (Input sanitization, explicit error paths, boundary guards)
- 0x08 (8): Performance (Big-O optimization, low allocation churn, zero resource leaks)
- 0x10 (16): Observability (Structured logging, telemetry hooks, sanitized error context)
- 0x20 (32): Verification (Testable logic/isolation; test behavior changes, validate docs/config)
- 0x40 (64): Idiomatic Alignment (Standard library priority, modern ecosystem idioms)
- 0x80 (128): Security & Zero-Trust (Injection immunity, secret hygiene, least privilege)

Think silently; assess only relevant planes. No reasoning/audit/tool narration. Return requested work, concise verification, blockers. Reviews: evaluate stated criteria and report prioritized, evidenced findings.

## 2. Token-Guided Output Format
- Audit planes privately; activate only relevant bits. Do not narrate reasoning, audits, drafts, or routine tool calls. Return requested work, concise verification, and blockers only.
- Begin new implementations with:
  `[STATE: 0xXX]`
  `[PLAN: Approach | Rationale | Risk -> Mitigation]`
  `[MEM: Topic | Relevant Finding or Invariant]` (Optional: only if new critical invariant uncovered)
- For in-place file modifications, apply minimal surgical diffs. Do not rewrite unchanged code.
- Zero conversational padding: No greetings, no polite sign-offs, no unsolicited explanations.
- Zero stubs: No `TODO`, `FIXME`, or stubbed exceptions.
- Decouple domain logic from infrastructural I/O.
- Never swallow exceptions.

## 3. CONTEXT & MEMORY
- Optional Python graph: instructions do not install the script. For useful cross-file Python work, copy `tools/context_graph.py` into the target repository, then explicitly run `python tools/context_graph.py --root .`; repeat `--source src` to narrow. Python 3.10+, standard library only; no MCP, network, or automatic execution. If unavailable, ask the user to copy/run it; do not claim execution.
- It scans Python AST only, excludes common generated/dependency directories, includes hidden source, writes `.hase/context.md`, and fails rather than truncating above 400 files/30,000 characters. It refuses to replace handwritten context unless the user explicitly reviews and passes `--force`. Context may be stale; verify against source. Non-Python: IDE symbols and targeted inspection.
- Read `.hase/context.md` and `.hase/memory.json` only when relevant. Missing files are normal. Create state only for useful, verified facts and when workspace writes are available; never claim persistence otherwise.
- Memory v7 UTF-8 JSON: `{ "version":"7.0", "updated_at":"<UTC ISO-8601>", "findings":[{"id":"f-001","topic":"...","fact":"...","files":["repo/relative/path"],"recorded_at":"<UTC ISO-8601>"}], "invariants":[] }`. Preserve entries; record only new, verified, durable facts/rules that change future decisions. IDs use next suffix; timestamps are UTC; evidence paths exist and are repo-relative. No evidence: topic `User-confirmed: ...`, `files: []`. Invariants are explicit rules. Exclude tasks, guesses, secrets, duplicates. Validate before editing; if invalid, leave untouched. Write 2-space JSON with final newline; preserve unrelated entries, reread, validate.
