# HASE frame v1

A compact, parseable header for agent-to-agent work with a human-readable summary.

## Why it exists

The hex byte is not a compression of reasoning. It is a **commitment header**: before touching code, the agent chooses the engineering lenses that actually apply. That makes the trade-offs visible, prevents silent scope drift, and gives another agent a stable field to parse.

It replaces narration, not thinking. A frame that is emitted as ritual is worse than no frame.

## Scope

Use the frame for:

- T1/T2 code changes;
- reviews where another agent or a human will consume the result;
- handoffs where the summary must be machine-readable.

Do **not** use it for:

- ordinary chat;
- T0 edits;
- a direct answer that is shorter than the frame itself.

## Grammar

The frame has three required lines. Code or prose may sit between the plan and the summary.

```text
[STATE: 0xNN]
[PLAN: approach | risk -> mitigation]
...
[SUMMARY: change | verify: command or observation | risk: residual]
```

- `0xNN` is exactly two hexadecimal digits, `00`–`FF`; case-insensitive.
- `PLAN` is one line. It names the approach, the primary risk, and the mitigation.
- `SUMMARY` is one line. It is the human-facing handoff and the machine-facing result.
- Do not put hidden chain-of-thought in any field.

## Bits

High bit first. Set only the lenses the agent will actually act on.

| Bit | Name | Required evidence |
| --- | --- | --- |
| `0x80` | Security / privacy | A trust-boundary check, authz check, secret review, or explicit "not applicable" |
| `0x40` | Idioms | The repository convention or language idiom followed |
| `0x20` | Verification | A test, command, or observation that supports the claim |
| `0x10` | Observability | A log, metric, trace, or a reason it is not needed |
| `0x08` | Performance | A budget, measurement, or complexity argument |
| `0x04` | Defensive design | Input validation, error path, or boundary handling |
| `0x02` | State / lifecycle | Ownership, cleanup, cancellation, concurrency, or atomicity decision |
| `0x01` | Architecture | The boundary, interface, or dependency direction touched |

Examples:

- `0x25` = `0x20` verification + `0x04` defensive + `0x01` architecture.
- `0x8C` = `0x80` security + `0x08` performance + `0x04` defensive.
- `0x00` means no lens was selected. If that is true, skip the frame instead of emitting a meaningless one.

## Evidence rule

An unbacked bit is a false claim. Before setting a bit, answer the question in the evidence column. If the answer is "not applicable", clear the bit. If the answer is "I will check", make the check part of `PLAN` and report it in `SUMMARY`.

Examples:

```text
[STATE: 0x25]
[PLAN: replace parser branch | legacy input -> fixture]
...
[SUMMARY: parser fixed | verify: 27 tests pass | risk: none]
```

```text
[STATE: 0x8C]
[PLAN: add upload endpoint | path traversal -> normalise + reject | 50 MB cap]
...
[SUMMARY: upload added | verify: authz + traversal tests pass | risk: storage quota]
```

## Machine-to-machine use

A parser should read the first matching `[STATE: ...]`, the `[PLAN: ...]` line, and the `[SUMMARY: ...]` line. It should ignore prose and code between them. This keeps the contract stable without forcing the entire answer into a rigid format.

```powershell
python tools/hase_state.py decode 0x25
python tools/hase_state.py encode architecture defensive verification
python tools/hase_state.py check frame.txt
```

The checker validates syntax and required lines. It cannot prove that the evidence is true; that remains the reviewer's job.

## Token economics

- Frame overhead is roughly 20–40 tokens per task.
- It is worth it only when it changes a decision, makes a risk explicit, or lets another agent parse the result.
- It is not worth it for T0 changes, casual chat, or a one-line answer.
- The savings come from replacing narration with one plan and one summary, not from the hex digits themselves.

## Failure modes

- **Ritual:** emitting all eight bits every time. Fix: select only acted-on lenses.
- **False evidence:** setting verification without a test. Fix: check the evidence column.
- **Hidden reasoning:** using the frame as a substitute for showing the decision. Fix: keep the plan concrete.
- **Overuse:** framing a typo. Fix: T0 skips the frame.
- **Parser drift:** changing field order. Fix: keep `STATE`, `PLAN`, `SUMMARY` stable; extend with optional fields only.
