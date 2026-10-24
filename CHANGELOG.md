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
