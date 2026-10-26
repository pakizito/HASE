# 0003 — Evidence-backed hex frame

- **Status:** Accepted
- **Date:** 2026-10-25
- **Deciders:** HASE maintainers

## Context

HASE v7 made the eight-bit state token mandatory. It was compact and distinctive, but it often became ritual: an agent emitted bits it never acted on, and the byte did not by itself improve reasoning or save tokens. HASE v9 removed the mandatory frame, which also removed the useful part: a stable, compact header that forces an agent to commit to a few engineering lenses before touching code.

The goal is not to compress reasoning into one byte. The goal is to make the agent's commitments inspectable, give another agent a parseable contract, and give a human a one-line summary.

## Decision

Restore the hex state as a scoped frame:

- Required for T1/T2 code changes and reviews; skipped for T0 and ordinary chat.
- `[STATE: 0xNN]`, `[PLAN: ...]`, `[SUMMARY: change | verify: ... | risk: ...]`.
- Each set bit must be backed by an action or observation. Verification requires a test, security a boundary check, performance a budget.
- `tools/hase_state.py` validates and encodes/decodes frames.
- `docs/hase-frame.md` defines the grammar and evidence rules.
- The adapter remains under the 11 KB budget.

## Consequences

**Positive**

- The bitmask has a concrete job again: committing to lenses and evidence.
- Agent-to-agent consumers have stable first and last lines to parse.
- Humans get a compact summary instead of narrated reasoning.
- Misuse is visible: an unbacked bit is a review finding.

**Negative**

- The frame adds roughly 20–40 tokens per task.
- It can still become ritual if used on trivial work.
- A validator can check syntax, not whether the evidence is truthful.
- Another format to maintain and teach.

## Alternatives considered

- **Mandatory on every response.** Rejected: it is noise for chat and T0, and encourages empty bits.
- **No frame at all.** Rejected: it loses a useful compact commitment and makes machine parsing rely on prose.
- **Full JSON state object.** Rejected for the default: too many tokens for the same information.
- **Only a human summary.** Rejected: not stable enough for agent-to-agent parsing.

## Follow-up

- Observe whether the frame reduces narration in real tasks.
- Add a review check for set bits without corresponding evidence if the pattern persists.
- Keep the grammar stable; add optional fields only by versioned extension.
