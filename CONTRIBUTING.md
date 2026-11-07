# Contributing to HASE

HASE is one file. The contract is [`HASE.md`](HASE.md). Keep it that way.

## Source of truth

Edit `HASE.md` only.

Do not add:

- generated adapter files;
- a context graph, cache, or index;
- a second instruction file;
- a required reference document;
- a runtime dependency.

If a rule needs more detail, write it in `HASE.md`. If it does not fit, it is not a HASE rule.

## Before you change the contract

Ask one question: does this change an engineering decision or prevent a repeated failure?

If the answer is no, do not add it. If the answer is yes, keep the rule short and testable.

## Validate

```powershell
python -m unittest discover -s tests -t . -v
```

The tests check the one-file contract, the HASE-STE rules, and the size limit.

## What belongs here

- A rule that changes a real decision or prevents a repeated failure.
- A missing mode, check, or safety boundary with a clear use case.
- A smaller way to express the same rule.

Avoid:

- a rule for every possible mistake;
- repeated guidance in several sections;
- language-specific advice without evidence;
- dependencies, hooks, background jobs, or network calls;
- claims that HASE guarantees correctness, security, or token savings.

## Pull request checklist

- [ ] `HASE.md` is the only instruction file changed.
- [ ] No adapters, graph, cache, or second instruction file added.
- [ ] Tests pass.
- [ ] The file is still under 10 KB.
- [ ] No secrets, personal data, or credentials.
- [ ] Security, data, and verification rules are not weaker.
- [ ] A material decision is recorded in `docs/adr/`.

## Decision records

Copy `docs/adr/0000-template.md`, number it sequentially, and state the context, decision, alternatives, and consequences.

## Security

Do not open a public issue for a vulnerability. See [`SECURITY.md`](SECURITY.md).
