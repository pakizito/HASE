# HASE engineering playbook

Extended reference for HASE v9. Load only the section the task needs. The compact contract is in [`../HASE.md`](../HASE.md).

## GRILL protocol

Use GRILL when the user asks for it, when a high-impact requirement is genuinely ambiguous, or before a large T2 build with unresolved product choices. Do not turn ordinary work into an interview.

### Quiet by default

1. Inspect the repository, tests, docs, and prior decisions first.
2. Build a decision tree: each decision that changes the design becomes a node; each dependent choice becomes a child.
3. Resolve every node you can from evidence, conventions, or a sensible default.
4. Keep a frontier of unresolved nodes. Ask only about nodes that are both unresolved and blocking.
5. If a safe default exists, take it, record it as an assumption, and proceed.
6. Do not ask for permission for reversible local work. Do not ask a question merely because a choice exists.

### Question rule

Ask when the answer changes one of:

- observable behaviour or public contract;
- data shape, retention, deletion, or migration;
- security, privacy, or authorisation;
- cost, latency, or operational risk above the agreed budget;
- an irreversible action or external side effect.

If none apply, decide and state the assumption.

### Question format

One question at a time:

```text
Q: <one decision that changes the design>
Recommended: <option> — <reason>
Trade-off: <what gets worse or what is deferred>
Reply: accept / change to ... / unknown / skip / summary / stop
```

Question budget: at most three blocking questions per task. If more remain, group low-impact choices into a defaults note and proceed; schedule an explicit GRILL session only for genuine high-impact forks.

### Decision ledger

Track:

- goal and users;
- success criteria;
- scope and non-goals;
- constraints;
- decisions and status;
- assumptions;
- risks and failure modes;
- open questions.

### Convergence

Stop when the frontier has no blocking nodes and the next implementation step is unambiguous, or when the user says `stop` or `summary`. A GRILL session ends with a decision brief. Do not implement until the user confirms shared understanding for an explicit GRILL session.

### Stress tests

- Pre-mortem: assume the change failed; why?
- Second-order effects: what does this make harder next?
- Reversal cost: how expensive is undoing this?
- Evidence gap: what would make the plan wrong?
- Abuse case: who benefits from breaking it?
- Operability: who gets paged, and what do they see?

## PLAN

For T1/T2 work where the approach is not obvious:

- goal and acceptance criteria;
- assumptions and non-goals;
- affected interfaces, data, and trust boundaries;
- failure modes and rollback;
- test and verification plan;
- one recommended approach with the main alternative.

For T2, include a threat model: assets, actors, entry points, trust boundaries, mitigations, residual risk.

## REVIEW severity

- **P0:** active data loss, security breach, outage, or unsafe production behaviour. Block.
- **P1:** correctness, contract, or security failure likely to affect users. Block until resolved or explicitly accepted.
- **P2:** important maintainability, performance, or edge-case issue. Fix before merge when practical.
- **P3:** minor improvement or style preference. Optional; do not flood the review.

## Architecture and design

- Keep domain logic independent of transport, storage, and vendor SDKs.
- Prefer explicit interfaces over hidden global state.
- Introduce an abstraction only when there is a real second use case or a boundary that needs testing.
- Make dependencies point inward. Avoid cycles.
- Design for failure: timeouts, cancellation, retries with jitter, idempotency, bounded queues.
- Separate read and write paths when their scaling or consistency needs differ.

## State, concurrency, and resources

- Define ownership and lifetime for every resource.
- Release files, sockets, locks, transactions, and background tasks deterministically.
- Make state transitions atomic or explicitly synchronised.
- Assume duplicate delivery and concurrent requests unless the system proves otherwise.
- Bound memory, concurrency, retries, and payload sizes.
- Make cancellation propagate; do not leave orphaned work.

## Errors and resilience

- Fail fast on programmer errors; fail gracefully on expected operational errors.
- Preserve context when wrapping exceptions; do not discard the cause.
- Never expose secrets, tokens, personal data, or internal paths in user-facing errors.
- Retry only idempotent operations, with a cap and backoff. Do not retry validation failures.
- Use one documented error shape for APIs.
- Distinguish user error, dependency failure, and internal defect.

## Data and privacy

- Treat schemas and migrations as production code. Include forward and rollback plans.
- Preserve backward compatibility unless a breaking change is explicitly approved.
- Minimise collected data and retention. Classify PII and sensitive fields.
- Define export and deletion paths for personal data, including derived indexes, caches, and backups. Verify deletion rather than assuming it.
- Use transactions for multi-step invariants. Test migration and rollback paths.
- Do not log payloads by default. Redact at the logging boundary.
- Define who can read, export, correct, and delete data.

## Security

- Authenticate, then authorise every request at the resource boundary. Do not trust client-side checks.
- Validate and normalise input at the boundary; encode output for its context.
- Use parameterised queries and safe deserialisation. Avoid `eval`, unsafe YAML, and shell interpolation.
- Keep secrets out of source, logs, prompts, fixtures, and error messages.
- Pin and review dependencies; check licences and known vulnerabilities before adding them.
- Treat SSRF, path traversal, prompt injection, and file uploads as real attack surfaces.
- For high-risk changes, document the threat model and residual risk.
- Apply least privilege to service accounts, tokens, and model tools.

## Performance

- State an explicit budget for latency, throughput, memory, or cost when it matters.
- Measure before optimising. Prefer algorithmic improvements over micro-optimisations.
- Watch for N+1 queries, unbounded result sets, repeated serialisation, and cache invalidation bugs.
- Do not add a cache without defining scope, eviction, and invalidation.
- Test at realistic data volume, not only with a toy fixture.

## Observability

- Emit structured logs with correlation IDs and actionable context.
- Record metrics for rate, error, duration, saturation, and business-critical outcomes.
- Trace across service and model boundaries where the platform supports it.
- Never log credentials or raw personal data.
- Make failures diagnosable without reproducing them locally.

## Testing

- Test behaviour and contracts, not private implementation details.
- Cover the happy path, boundary conditions, invalid input, and failure paths.
- Prefer deterministic tests. Avoid sleeps and real network calls in unit tests.
- Use integration tests for boundaries you do not own; use contract tests for APIs.
- A bug fix needs a regression test. A new feature needs acceptance coverage.
- Do not mock the thing you are supposed to be testing.
- Test the migration and rollback path when data changes.

## APIs

- Version public APIs and document compatibility guarantees.
- Use consistent naming, pagination, filtering, idempotency keys, and error formats.
- Validate request bodies and reject unknown or oversized input deliberately.
- Document authentication, rate limits, retries, and example responses.
- Treat generated clients and schemas as contracts; regenerate and test them together.
- Make destructive endpoints explicit and idempotent where possible.

## Frontend and accessibility

- Prefer semantic HTML and native controls.
- Every interactive element must be keyboard reachable and have a visible focus state.
- Label controls; preserve heading order; provide alt text for meaningful images.
- Design loading, empty, error, and offline states, not just the happy path.
- Check responsive layouts and colour contrast. Do not encode meaning in colour alone.
- Externalise user-facing strings when the product supports multiple locales.
- Respect reduced-motion and user preferences where relevant.

## AI and LLM features

- Treat model output as untrusted input.
- Ground factual claims in retrieved evidence; cite sources when the interface exposes them.
- Separate system instructions, user content, and retrieved documents; defend against prompt injection.
- Version prompts, models, tools, and evaluation datasets. Record what changed and why.
- Define evals before tuning. Include regression cases for safety, refusal, grounding, and format.
- Set cost, latency, and token budgets. Fail closed on missing consent or missing evidence.
- Provide human review for consequential actions. Never let a model perform irreversible operations without explicit authorisation.
- Do not send personal or confidential data to a provider without a documented basis and a data-processing agreement.
- Log model version and prompt version with outcomes where privacy permits.

## Dependencies and supply chain

- Prefer the standard library and existing project dependencies.
- Add a dependency only when its value exceeds its maintenance, security, and licence cost.
- Pin versions where reproducibility matters; review lockfile changes.
- Verify package names and sources; do not install from untrusted indexes or paste arbitrary install scripts.
- Run the project's audit tooling when available.
- Check licence compatibility before commercial use.

## Git and release hygiene

- Keep commits focused and messages explanatory.
- Do not commit secrets, generated credentials, large binaries, or local caches.
- Do not rewrite shared history, force-push a protected branch, or delete another contributor's work without explicit approval.
- Review the diff before committing. Include tests and docs with the behaviour change.
- Use feature flags, staged rollouts, or canaries for risky changes when the platform supports them.
- Record what deployed, where, and how to roll it back.

## Documentation

- Update the README when setup, usage, or behaviour changes.
- Record material architecture decisions as ADRs in `docs/adr/`.
- Maintain a short `CONTEXT.md` or glossary when domain terms are ambiguous or overloaded.
- Document operational steps, failure modes, and rollback where an operator will need them.
- Keep examples executable and current. Remove stale instructions rather than adding caveats.

## Definition of done

A change is done only when all applicable items are true:

- [ ] Acceptance criteria are met, not merely approximated.
- [ ] Tests were added or updated and pass; the relevant suite was run.
- [ ] Types, lint, formatting, and build checks pass.
- [ ] Security and privacy impact was reviewed; no secrets or sensitive data leaked.
- [ ] Data migrations, compatibility, and rollback were considered.
- [ ] Observability is adequate for the failure modes introduced.
- [ ] User, API, and operator documentation is updated.
- [ ] The diff contains no unrelated changes, dead code, or unexplained placeholders.
- [ ] The handoff states what changed, what was verified, and what remains risky.

## Stop and ask

Stop before acting when:

- the action is destructive or irreversible (data deletion, production deploy, credential rotation, force push);
- requirements conflict or a high-impact choice is genuinely ambiguous;
- the change touches authentication, payments, personal data, or a public contract without a clear specification;
- you cannot verify an external effect;
- unrelated tests are failing and the cause is unclear;
- the request requires scope creep or a rewrite beyond the stated goal;
- a licence, legal, or compliance question blocks the design;
- you are about to guess at a secret, credential, or production value.

Ask one focused question. Include the recommended option and the consequence of each path.

## Context and memory

### Inspect in this order

1. `git status`, recent commits, and the current diff.
2. Top-level tree, README, build/test configuration, and package manifests.
3. The smallest relevant source files, their tests, and call sites.
4. Existing conventions, generated files, and migration patterns.
5. Only then form a plan.

Prefer targeted search and IDE symbols over reading the whole repository. Do not infer architecture from filenames alone.

### Polyglot context map

```text
python tools/context_graph.py --root .
python tools/context_graph.py --root . --source src --source tests
python tools/context_graph.py --root . --files
python tools/context_graph.py --root . --all-imports
```

The map inventories any codebase by directory and language. Python also gets top-level symbols and import edges. Other languages get a structural map; do not infer semantic dependencies from it. `--files` adds the full code-file listing; `--all-imports` includes external Python imports. Treat `.hase/context.md` as a cache and verify source before relying on it.

### Memory

Memory is for verified, durable facts that change future decisions. It is not a task log. Schema v7 remains compatible:

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

Rules:

- Store only verified facts, explicit user constraints, or durable invariants.
- Use repo-relative evidence paths that exist. If there is no file evidence, use topic `User-confirmed: ...` and an empty `files` array.
- Preserve unrelated entries. Re-read and validate before writing.
- Exclude guesses, secrets, personal data, task history, and duplicates.
- The latest verified fact wins. If two facts conflict, record the resolution.
- Keep the file small; remove stale entries.
- Durable architecture decisions belong in ADRs.
