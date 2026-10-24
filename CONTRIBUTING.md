# Contributing to HASE

HASE is intentionally small and portable. Changes should improve agent behaviour without turning the project into a framework.

## Source of truth

Edit [`HASE.md`](HASE.md). The adapter files are generated and must not be edited by hand:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.github/copilot-instructions.md`
- `.cursor/rules/hase.mdc`
- `.windsurfrules`
- `.clinerules`
- `.agents/rules/hase.md`
- `CONVENTIONS.md`

After changing `HASE.md`:

```powershell
python tools/render_adapters.py
python -m unittest discover -s tests -t . -v
python tools/render_adapters.py --check
```

## What belongs here

- A rule that changes a real engineering decision or prevents a repeated failure.
- A missing mode, checklist, or safety boundary with a clear use case.
- Tooling that stays local, standard-library-only, and opt-in.
- Tests for behaviour, not snapshots of prose.

Avoid:

- adding a rule for every possible mistake;
- duplicating the same guidance in several sections;
- language-specific advice without evidence that it generalises;
- dependencies, background hooks, or network calls;
- claims that HASE guarantees correctness, security, or token savings.

## Pull request checklist

- [ ] `HASE.md` is the only instruction source changed.
- [ ] Adapters were regenerated and `--check` passes.
- [ ] Tests pass.
- [ ] New behaviour has a test or a clear reason why it cannot be tested.
- [ ] No secrets, personal data, or credentials are included.
- [ ] The change does not weaken the security, data, or verification rules.
- [ ] The README or an ADR is updated when the contract changes materially.

## Decision records

Material changes to the contract belong in `docs/adr/`. Copy `docs/adr/0000-template.md`, number it sequentially, and state the alternatives and consequences.

## Reporting security issues

Do not open a public issue for a vulnerability. See [`SECURITY.md`](SECURITY.md).
