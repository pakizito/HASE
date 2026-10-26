# HASE v9.1

### A token-optimized engineering contract for AI-assisted software development.

HASE gives coding agents a repeatable way to understand a repository, make focused changes, verify with evidence, and hand work back without flooding the context window.

The default adapter is a compact contract. Detailed standards live in [`docs/playbook.md`](docs/playbook.md) and are loaded only when a task needs them.

> **Guidance, not magic:** HASE improves process discipline. It does not guarantee correctness, security, or a particular token reduction. Results still depend on the model, editor tools, repository state, and human review.

## What changed in v9.1

v9 made the contract compact. v9.1 restores the hex state as an evidence-backed machine frame, not as ceremony.

- **Hex state frame:** T1/T2 code changes and reviews start with `[STATE: 0xNN]` and `[PLAN: ...]`, and end with `[SUMMARY: change | verify: ... | risk: ...]`.
- **Evidence-backed bits:** a set bit must be acted on. Verification needs a test, security needs a boundary check, performance needs a budget.
- **Validator:** `tools/hase_state.py` decodes, encodes, and checks frames.
- **Still compact:** detailed standards remain in `docs/playbook.md`; the default adapter stays under the 11 KB budget.

## What changed in v9

v8 proved the process but grew to about 23 KB per adapter. v9 keeps the useful parts and makes them compact.

- **Token-optimized core:** the canonical contract is now about 10 KB instead of 23 KB. A unit test enforces an 11 KB adapter budget.
- **Progressive disclosure:** detailed security, data, API, frontend, AI, and release guidance moved to `docs/playbook.md`; the adapter points to the relevant reference.
- **Quiet GRILL:** the decision interview remains, but it runs silently by default. The agent resolves facts and sensible defaults itself and asks only when the answer changes behaviour, security, data, cost, or an irreversible action. Hard cap: three blocking questions per task.
- **Polyglot context graph:** `tools/context_graph.py` now inventories any codebase by directory and language. Python also gets symbols and import edges; other languages get a structural map. `--files` is opt-in.
- **Less nagging:** no routine confirmation for plans, reversible local edits, or read-only work. Assumptions are stated in the handoff instead.
- **AGENTS.md:** added for Codex and other AGENTS.md-compatible agents. All nine adapters are generated from `HASE.md`.

Memory schema remains **v7-compatible**; HASE’s contract version and the memory format version are independent.

## Core behaviour

| Area | Rule |
| --- | --- |
| Triage | T0 trivial, T1 normal, T2 high risk, T3 incident. Escalate when unsure. |
| GRILL | Resolve silently; ask only blocking questions; recommend an option with a trade-off. |
| PLAN | Goal, acceptance criteria, constraints, failure modes, rollback, tests. |
| BUILD | Read first, focused patch, tests where practical, run the checks. |
| DEBUG | Reproduce, isolate, fix the cause, add a regression test. |
| REVIEW | P0–P3 findings with file/line evidence; read-only by default. |
| SHIP | Verify, document, and do not deploy without explicit approval. |

## The hex state frame

The frame is a **commitment header**, not a compression of reasoning. It forces the agent to choose the lenses it will act on and gives another agent a stable line to parse. Use it for T1/T2 code changes and reviews; skip it for T0 and ordinary chat.

```text
[STATE: 0x25]
[PLAN: replace parser branch | legacy input -> fixture]
...
[SUMMARY: parser fixed | verify: 27 tests pass | risk: none]
```

Bits, high to low:

| Bit | Lens | Evidence expected |
| --- | --- | --- |
| `0x80` | Security / privacy | Boundary, authz, secret, or data check |
| `0x40` | Idioms | Repository convention followed |
| `0x20` | Verification | Test, command, or observation |
| `0x10` | Observability | Log, metric, trace, or why not needed |
| `0x08` | Performance | Budget, measurement, or complexity argument |
| `0x04` | Defensive design | Input, error, or boundary handling |
| `0x02` | State / lifecycle | Ownership, cleanup, concurrency, atomicity |
| `0x01` | Architecture | Boundary, interface, or dependency direction |

Set only bits you act on. `0x00` means no lens applies: skip the frame instead of emitting a meaningless one.

The full specification and evidence rules are in [`docs/hase-frame.md`](docs/hase-frame.md). Validate a frame with:

```powershell
python tools/hase_state.py decode 0x25
python tools/hase_state.py encode architecture defensive verification
python tools/hase_state.py check frame.txt
```

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

Each adapter is self-contained for normal work. The generated marker is provenance: when contributing to HASE, edit [`HASE.md`](HASE.md) and run the renderer. A copied adapter may be adapted for its target project; the detailed playbook is optional reference, not a runtime dependency.

```powershell
python tools/render_adapters.py
python tools/render_adapters.py --check
```

## GRILL without nagging

Use GRILL when the user says “grill me”, when a high-impact requirement is genuinely ambiguous, or before a large T2 build.

The agent first resolves everything it can from the repository, conventions, and sensible defaults. It asks only when the answer changes one of:

- observable behaviour or a public contract;
- data shape, retention, deletion, or migration;
- security, privacy, or authorisation;
- cost, latency, or operational risk above budget;
- an irreversible action or external side effect.

Questions are one at a time, with a recommendation and trade-off:

```text
Q: Should the first release support shared family accounts, or one owner per profile?
Recommended: One owner — smaller permission model and clearer consent boundary.
Trade-off: Families with multiple caregivers wait for the second release.
Reply: accept / change to ... / unknown / skip / summary / stop
```

If no blocking doubt exists, there is no question. The agent states its assumptions and proceeds. The full protocol is in [`docs/playbook.md`](docs/playbook.md#grill-protocol).

## Polyglot context graph

For any codebase:

```powershell
python tools/context_graph.py --root .
python tools/context_graph.py --root . --source src --source tests
python tools/context_graph.py --root . --files
```

The default output is a compact summary: languages, directory counts, Python modules and import edges. Other languages are inventoried structurally; HASE does not pretend a regex is a parser. `--files` adds the full code-file listing only when needed; `--all-imports` includes external Python imports. Module names are relative to the selected source roots; use `--root .` for cross-root imports.

The tool requires Python 3.10 or later, uses only the standard library, does not import project code, and writes `.hase/context.md`. It skips VCS, virtual environments, caches, editor state, package managers, generated context, and common build outputs. It fails instead of silently truncating above 2,000 code files or 30,000 output characters. It refuses to overwrite handwritten context without `--force`.

Treat the map as a cache. Verify the source before relying on it.

## Optional project memory

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

## Templates and reference

- [`docs/playbook.md`](docs/playbook.md) — detailed standards and full GRILL protocol.
- [`docs/hase-frame.md`](docs/hase-frame.md) — full state-frame grammar, bit evidence, and parser contract.
- [`docs/decision-brief-template.md`](docs/decision-brief-template.md) — output of a GRILL session.
- [`docs/threat-model-template.md`](docs/threat-model-template.md) — T2 security and trust-boundary review.
- [`docs/adr/0000-template.md`](docs/adr/0000-template.md) — durable architecture decision record.

## Repository maintenance

```powershell
python -m unittest discover -s tests -t . -v
python tools/render_adapters.py --check
python tools/context_graph.py --root .
python tools/hase_state.py decode 0x25
```

CI runs the test suite and the adapter drift check on every push and pull request. The repository uses UTF-8, LF line endings, and a two-space Markdown indent; see `.editorconfig` and `.gitattributes`.

## Design principles

- **Explicit opt-in:** no hooks, background scans, or automatic writes.
- **Local by default:** no MCP, network access, package installation, or third-party service required.
- **Source remains authoritative:** generated context and memory can be stale; inspect the code.
- **Proportional ceremony:** use the lightest process that still makes the change safe and reviewable.
- **One source of truth:** edit `HASE.md`, not the generated adapters.
- **Token discipline:** the default adapter is compact; detail is opt-in.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the source-of-truth workflow and pull-request checklist. Report vulnerabilities through the process in [`SECURITY.md`](SECURITY.md). Material contract changes belong in [`CHANGELOG.md`](CHANGELOG.md) and [`docs/adr/`](docs/adr/).

## Inspirations

- [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) by Matt Pocock (MIT): the one-question-at-a-time decision interview, recommended answers, and “facts are the agent’s job; decisions are the user’s.”
- [grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-with-docs) (MIT): shared domain language and ADRs as durable decision records.
- The original HASE v7 lens model.

HASE is not affiliated with those projects. The GRILL implementation here is a quiet adaptation, not a copy.

Licensed under [MIT](LICENSE).
