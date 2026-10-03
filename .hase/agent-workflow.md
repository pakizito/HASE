# HASE Agent Workflow

**Aim:** maximize verified work per token. Keep `.hase/context.md` to about 500 tokens by default. No executable/install. Act silently; never narrate reasoning, audits, drafts, or routine tool calls. Report only result, concise verification, blockers. Never claim unverified writes/checks.

## Every task (read only this section first)

1. Read `.hase/context.md` and `.hase/memory.json`; use entries to locate relevant files. Open only targets/direct dependencies. Source/config is authoritative.
2. Do not scan/rebuild the repository for routine work. Refresh graph only after structural changes. Record memory only if every admission check passes; preserve other entries.
3. Reread changed files before claiming success. If writes are unavailable, say so.
4. Load **Graph procedure** only for graph work; **Memory procedure** only for ledger work. For initial setup, read both. Final output: requested artifact/result, material verification, blockers only.

## Graph procedure — `.hase/context.md`

Navigation only—not AST/source dump. Keep smaller than the context needed to inspect the project. Include only likely exploration-savers: stack/entry points, key symbols/module roles, important imports/test mappings, verified commands, relevant instruction/config links. Omit routine/duplicate/easily recovered facts. Aim for ~500 tokens; group large projects as `PARTIAL`. Expand only on request/task-critical need.

Create/refresh only if missing, requested, or scope changes:

1. Enumerate files only for full coverage/broad changes. Identify roots and generated/vendor/build exclusions. Incomplete listing => `PARTIAL`, never guess counts.
2. Verify symbols/imports in source/language services. Resolve internal paths; separate external/unresolved imports. Static imports do not prove runtime flow.
3. Claim `FULL` only if all in-scope code/test and relevant docs/config files were enumerated and checked; else state `PARTIAL` and omissions. Use exact counts and sorted workspace-relative `/` paths. `FULL 0/0` only after confirming none exist.
4. Update affected entries only; reread/check facts/counts. Body-only edits need no refresh.

Entry example: `` `src/auth.ts` — Auth service; exports `Auth.login(User): Promise<Token>`; imports `src/store.ts`, `jsonwebtoken`; tested by `tests/auth.test.ts`. `` Create `.hase/graph.json` only on request.

## Memory procedure — `.hase/memory.json`

Keep verified, non-obvious, durable facts that may change future decisions. No task summaries, TODOs, generic advice, duplicates, secrets, guesses, or transient details.

**Admission—all yes:** verified or user-confirmed; durable/useful; not already captured; concise/safe. Otherwise do not record. Prefer source/docs when lasting.

Schema: `{"version":"7.0","updated_at":"UTC ISO-8601","findings":[{"id":"f-001","topic":"Area","fact":"Verified fact","files":["src/file.ts"],"recorded_at":"UTC ISO-8601"}],"invariants":["Normative rule"]}`.

- Parse/validate first. Missing file: create empty arrays/current UTC; invent nothing. Require v7.0, UTC timestamps, unique `f-NNN` IDs, non-empty topic/fact, workspace-relative evidence paths, unique non-empty invariants. User-confirmed facts without files use `User-confirmed:` and `files: []`.
- Invalid data: do not edit/repair; report the issue and ask. Deduplicate findings by meaning; next ID follows largest numeric suffix (not array length); one factual sentence and sorted relevant paths. Invariants require an explicit rule, repeated architecture, or user confirmation.
- Preserve unrelated entries. Write full JSON (2-space indent, final newline, UTC), reread/validate, confirm old entries remain. Clear only on request. Emit `[MEM]` only for saved, verified new/corrected memory.

**Sync:** only when requested—enumerate scope, verify graph, refresh stale facts, validate ledger, reread files, report scope/counts and limits. Optimize navigation value per token, not apparent completeness.
