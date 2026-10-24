# 0001 — Adopt HASE v8 as a risk-proportional engineering contract

- **Status:** Accepted
- **Date:** 2026-10-24
- **Deciders:** HASE maintainers

## Context

HASE v7 provided eight engineering lenses, an optional Python context map, and a small memory schema. It was portable and cheap to adopt, but it had four structural problems:

1. Eight near-identical adapter files were maintained by hand, which produced drift and encoding defects.
2. The response contract optimised for brevity at the expense of required clarification, verification, and handoff.
3. It treated every task with the same process, whether the change was a typo or an authentication boundary.
4. It had no discovery mode, no definition of done, and little guidance on security, data, APIs, accessibility, AI safety, release, or incident response.

The `grill-me` approach demonstrated a useful discipline: discover facts, ask one consequential decision at a time, recommend an answer, and do not implement until shared understanding is reached.

## Decision

Adopt HASE v8 with:

- `HASE.md` as the canonical contract and generated adapters;
- task tiers T0–T3 for proportional process;
- GRILL, PLAN, BUILD, DEBUG, REVIEW, and SHIP modes;
- a mandatory evidence-based handoff;
- an explicit Definition of Done;
- expanded engineering standards, including security, data, APIs, accessibility, AI/LLM safety, supply chain, Git, and release;
- an optional compact response mode that preserves the original bitmask without making it mandatory;
- repository tests, adapter drift checks, and CI.

The memory schema remains at `7.0` so existing `.hase/memory.json` files remain valid.

## Consequences

**Positive**

- One source of truth removes adapter drift.
- The process now scales with risk instead of applying maximum ceremony everywhere.
- GRILL reduces the chance of building the wrong thing.
- The handoff and Definition of Done make “done” inspectable.
- CI catches generated-file drift and regressions in the local tools.

**Negative**

- The canonical instruction is materially longer than v7 and consumes more context.
- Contributors must edit `HASE.md` and regenerate adapters rather than editing an adapter directly.
- The contract asks for more judgement; it cannot mechanically enforce security or correctness.
- The optional compact mode still depends on the model following a private checklist.

## Alternatives considered

- **Keep v7 and patch individual adapters.** Rejected because it preserves the drift and encoding failure mode.
- **Make every mode mandatory.** Rejected because it adds friction to trivial work and encourages performative ceremony.
- **Move all detail into reference files.** Rejected for the default adapter because IDE agents may not load linked files reliably. Detailed procedures remain in the contract; optional tools stay separate.
- **Bump the memory schema.** Rejected because it would break existing files without adding enough value.

## Follow-up

- Validate the contract against real repositories and remove rules that prove to be noise.
- Add language- or platform-specific checklists only when a repeated need is demonstrated.
- Review the GRILL protocol after several sessions and tighten the convergence criteria.
