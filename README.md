# HASE v8.0

### A deliberate engineering contract for AI-assisted software development.

HASE is a portable instruction set for coding agents. It gives an agent a repeatable way to understand a repository, ask better questions, make focused changes, verify the result, and hand work back with evidence.

It is plain text. No runtime, hosted service, or mandatory setup. Use one adapter file, or use the optional local tools when they earn their keep.

> **Guidance, not magic:** HASE improves process discipline. It does not guarantee correctness, security, or a particular token reduction. Results still depend on the model, editor tools, repository state, and human review.

## What changed in v8

v7 was a compact lens checklist. v8 is an engineering contract that scales from a typo to a production incident.

- **Canonical source:** `HASE.md` is the single source of truth. All adapter files are generated from it, so they cannot drift.
- **Proportional process:** tasks are classified as T0–T3. A typo does not get a threat model; authentication and migrations do.
- **GRILL mode:** a decision interview inspired by [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me). One consequential question at a time, each with a recommended answer and trade-off.
- **Explicit modes:** GRILL, PLAN, BUILD, DEBUG, REVIEW, and SHIP.
- **Definition of Done:** tests, types, security, data, observability, docs, and rollback are checked before work is called complete.
- **Stronger engineering standards:** security, privacy, concurrency, APIs, accessibility, AI/LLM safety, supply chain, Git, release, and observability.
- **Evidence-based handoff:** “done” requires the command or observation that proves it.
- **Optional compact mode:** the eight-bit state token is still available, but it is no longer mandatory output.
- **Maintainable repository:** generated adapters, a drift check, unit tests, and CI.

Memory schema remains **v7-compatible**; HASE’s contract version and the memory format version are independent.

## Choose a mode

| Mode | Use it for | Output |
| --- | --- | --- |
| **GRILL** | Vague or high-impact plans; “grill me” | One question at a time, recommendation, trade-off, decision ledger |
| **PLAN** | T1/T2 work where the approach is not obvious | Goal, assumptions, interfaces, risks, acceptance criteria, test plan |
| **BUILD** | Implementing an agreed change | Focused patch, tests, verification |
| **DEBUG** | A defect or failing test | Reproduction, root cause, minimal fix, regression test |
| **REVIEW** | A diff, PR, or design | Findings by severity with file/line evidence |
| **SHIP** | Release or production change | Verification, migration/rollback, observability, release notes |

## Task tiers

| Tier | Examples | Minimum process |
| --- | --- | --- |
| **T0** | Typo, comment, link, isolated copy change | Inspect, edit, validate the affected file |
| **T1** | Bug fix, feature, refactor, local API change | Assumptions, tests, relevant checks, diff review |
| **T2** | Auth, payments, PII, destructive migration, public contract, AI safety | Plan, threat model, rollback, approval before irreversible steps |
| **T3** | Outage, data loss, exploit, leaked credential | Stabilise, preserve evidence, avoid opportunistic refactors |

When unsure, escalate one tier.

## Install one adapter

Choose **one** native instruction file and copy it to the matching path in your project. Do not install every variant in the same repository.

| IDE / agent | Instruction file |
| --- | --- |
| Codex / AGENTS.md-compatible agents | [`AGENTS.md`](AGENTS.md) |
| GitHub Copilot | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) |
| Cursor | [`.cursor/rules/hase.mdc`](.cursor/rules/hase.mdc) |
| Claude Code | [`CLAUDE.md`](CLAUDE.md) |
| Windsurf | [`.windsurfrules`](.windsurfrules) |
| Cline / Roo Code | [`.clinerules`](.clinerules) |
| Antigravity | [`.agents/rules/hase.md`](.agents/rules/hase.md) |
| Gemini | [`GEMINI.md`](GEMINI.md) |
| Aider | [`CONVENTIONS.md`](CONVENTIONS.md) |

Each adapter is self-contained. The generated marker at the top is provenance: when contributing to HASE, edit [`HASE.md`](HASE.md) and run the renderer. A copied adapter may be adapted for its target project.

```powershell
python tools/render_adapters.py
python tools/render_adapters.py --check
```

## GRILL mode

Use it when the user says “grill me”, when requirements are fuzzy, or before a large high-risk build.

The agent asks one question at a time, recommends an answer, names the trade-off, and waits. It investigates facts in the repository instead of asking the user to repeat them. It maintains a decision tree and only asks questions whose prerequisites are settled.

```text
Q: Should the first release support shared family accounts, or one owner per profile?
Recommended: One owner — smaller permission model and clearer consent boundary.
Trade-off: Families with multiple caregivers wait for the second release.
Reply: accept / change to ... / unknown / skip / summary / stop
```

GRILL ends with a decision brief. It does not start coding until the user confirms shared understanding. A template is in [`docs/decision-brief-template.md`](docs/decision-brief-template.md).

## Templates

- [`docs/decision-brief-template.md`](docs/decision-brief-template.md) — the output of a GRILL session.
- [`docs/threat-model-template.md`](docs/threat-model-template.md) — T2 security and trust-boundary review.
- [`docs/adr/0000-template.md`](docs/adr/0000-template.md) — durable architecture decision record.

## Optional: Python context map

For cross-file Python work:

```powershell
python tools/context_graph.py --root .
python tools/context_graph.py --root . --source src --source tests
```

The tool requires Python 3.10 or later, uses only the standard library, parses with `ast`, does not import project code, and writes `.hase/context.md`. It skips VCS, virtual environments, caches, editor state, package managers, and common build outputs. It fails instead of silently truncating above 400 Python files or 30,000 output characters. It refuses to overwrite handwritten context without `--force`.

Treat the map as a cache. Verify the relevant source before relying on it. For other languages, use IDE symbols and targeted inspection.

## Optional: project memory

Memory is for verified, durable facts that change future decisions, not task history. It is separate from the generated context map and is not created during setup.

```json
{
  "version": "7.0",
  "updated_at": "2026-10-24T12:00:00Z",
  "findings": [
    {
      "id": "f-001",
      "topic": "API",
      "fact": "Access tokens expire after 15 minutes.",
      "files": ["src/auth.py"],
      "recorded_at": "2026-10-24T12:00:00Z"
    }
  ],
  "invariants": ["Pure logic stays decoupled from infrastructure I/O"]
}
```

Keep entries verified, durable, concise, and useful. Preserve unrelated entries. Exclude guesses, secrets, personal data, duplicates, and task logs. Durable architecture decisions belong in `docs/adr/`, not in memory.

## Repository maintenance

```powershell
python -m unittest discover -s tests -t . -v
python tools/render_adapters.py --check
python tools/context_graph.py --root . --source tools --source tests
```

CI runs the test suite and the adapter drift check on every push and pull request. The repository uses UTF-8, LF line endings, and a two-space Markdown indent; see `.editorconfig` and `.gitattributes`.

## Design principles

- **Explicit opt-in:** no hooks, background scans, or automatic writes.
- **Local by default:** no MCP, network access, package installation, or third-party service required.
- **Source remains authoritative:** generated context and memory can be stale; inspect the code.
- **Proportional ceremony:** use the lightest process that still makes the change safe and reviewable.
- **One source of truth:** edit `HASE.md`, not the generated adapters.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the source-of-truth workflow and pull-request checklist. Report vulnerabilities through the process in [`SECURITY.md`](SECURITY.md). Material contract changes belong in [`CHANGELOG.md`](CHANGELOG.md) and [`docs/adr/`](docs/adr/).

## Inspirations

- [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) by Matt Pocock (MIT): the one-question-at-a-time decision interview, recommended answers, and “facts are the agent’s job; decisions are the user’s.”
- [grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-with-docs) (MIT): shared domain language and ADRs as durable decision records.
- The original HASE v7 lens model: architecture, state, defensive design, performance, observability, verification, idioms, and security.

HASE is not affiliated with those projects. The GRILL implementation here is a compact adaptation, not a copy.

Licensed under [MIT](LICENSE).
