# HASE v7.0 ARCHITECTURAL CONVENTIONS FOR AIDER
Universal AI Developer Co-Pilot · Optimized for Metered & Low-Parameter LLMs

## 1. Architectural Bitmask Mandate
Before editing code, mentally audit the task against the HASE v7.0 8-plane cognitive matrix:
- 0x01 (1): Macro-Architecture (SOLID, modular boundaries, loose coupling)
- 0x02 (2): State & Lifecycle (Concurrency safety, immutability, deterministic cleanup via RAII/defer)
- 0x04 (4): Defensive Design (Input sanitization, explicit error paths, boundary guards)
- 0x08 (8): Performance (Big-O optimization, low allocation churn, zero resource leaks)
- 0x10 (16): Observability (Structured logging, telemetry hooks, sanitized error context)
- 0x20 (32): Verification (Pure logic isolation; companion unit tests required when active)
- 0x40 (64): Idiomatic Alignment (Standard library priority, modern ecosystem idioms)
- 0x80 (128): Security & Zero-Trust (Injection immunity, secret hygiene, least privilege)

## 2. Token-Guided Output Format
- Begin new implementations with:
  `[STATE: 0xXX]`
  `[PLAN: Approach | Rationale | Risk -> Mitigation]`
  `[MEM: Topic | Relevant Finding or Invariant]` (Optional: only if new critical invariant uncovered)
- For in-place file modifications, apply minimal surgical diffs. Do not rewrite unchanged code.
- Zero conversational padding: No greetings, no polite sign-offs, no unsolicited explanations.
- Zero stubs: No `TODO`, `FIXME`, or stubbed exceptions.
- Decouple domain logic from infrastructural I/O.
- Never swallow exceptions.

## 3. Context Engine & Working Memory
Follow `.hase/agent-workflow.md` for agent-managed context graph and memory operations. Consult `.hase/context.md` and `.hase/memory.json` before exploration or edits, refresh the graph after structural changes, and preserve existing ledger entries. No Python runtime or HASE CLI is required.
