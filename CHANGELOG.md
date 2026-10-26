## [9.2.0] — 2026-10-25

### Added

- Context ladder: C0/T0 reads target plus nearest test; C1/T1 adds graph, affected files and tests; C2/T2 adds a playbook section, threat model and rollback.
- State byte as a routing key for optional playbook sections.
- One-file install path: copy `HASE.md` as the agent instruction file; adapters are pre-renamed copies.

### Changed

- Compact core reduced to about 9 KB; adapter budget is now 9.5 KB.
- Core checks condensed; detailed standards remain in `docs/playbook.md`.
- Version bumped to 9.2.0.

## [9.1.0] — 2026-10-25

### Added

- Evidence-backed `[STATE: 0xNN]` / `[PLAN: ...]` / `[SUMMARY: ...]` frame for T1/T2 code changes and reviews.
- `tools/hase_state.py` for decoding, encoding, and validating frames.
- `docs/hase-frame.md` with the grammar, bit evidence rules, examples, and token economics.
- ADR 0003 documenting why the hex frame returned and how it is constrained.
- Six state-frame tests.

### Changed

- The hex state is no longer a private optional checklist; it is a scoped machine frame with evidence requirements.
- The frame is skipped for T0 and ordinary chat to protect the token budget.
- The default adapter remains under the 11 KB budget.

## [9.0.0] — 2026-10-24

### Added

- Token-optimized core contract at roughly 10 KB per adapter, with an 11 KB test budget.
- Detailed engineering reference in `docs/playbook.md`, loaded only when needed.
- Polyglot context graph: languages, directory map, Python symbols/imports, optional file listing, and non-fatal Python parse errors.
- Quiet GRILL protocol with a three-question blocking budget and defaults-first behavior.
- `AGENTS.md` adapter.
- ADR 0002 for the v9 architecture.

### Changed

- Detailed standards moved out of the default adapter into progressive-disclosure references.
- GRILL now resolves facts and sensible defaults silently instead of interviewing the user routinely.
- The context graph default limit is now 2,000 code files; `--files` is opt-in.
- Context-graph Python syntax errors and duplicate module names are reported without discarding the rest of the inventory.

### Fixed

- The context graph no longer fails on a non-Python codebase.
- Adapter richness no longer comes at the cost of the default context budget.

# Changelog

All notable changes to HASE are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses semantic versioning for the contract.

## [8.0.0] — 2026-10-24

### Added

- Canonical `HASE.md` contract and generator for all adapter files, including `AGENTS.md`.
- GRILL decision interview with one-question-at-a-time recommendations, a decision tree, and a convergence rule.
- PLAN, BUILD, DEBUG, REVIEW, and SHIP operating modes.
- Task tiers T0–T3 for proportional process.
- Definition of Done and a mandatory evidence-based handoff.
- Engineering standards for security, privacy, data, concurrency, APIs, accessibility, AI/LLM features, supply chain, Git, release, and observability.
- ADR template and the HASE v8 decision record.
- Contributor and security policies.
- CI validation and expanded unit tests.

### Changed

- The eight-bit state token is now an optional compact mode rather than mandatory output.
- The “no post-code summary” rule is replaced by a short verification and risk handoff.
- `pass`, `NotImplementedError`, and `TODO` are allowed only when intentional, documented, and tracked.
- Memory schema remains `7.0` for backward compatibility.
- Context graph excludes editor state and common non-Python build output directories.

### Fixed

- Removed repeated adapter drift, mojibake, and line-ending inconsistencies by generating adapters from one source.
- Added package markers so the documented `unittest discover` command works.
- Normalised UTF-8 and LF through `.editorconfig` and `.gitattributes`.

## [7.0.0]

- Initial public HASE contract with the eight engineering lenses, optional Python context graph, and memory schema.
