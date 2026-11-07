# HASE-STE

HASE-STE is a controlled style for HASE instructions and handoffs. It uses selected principles from **ASD-STE100 Simplified Technical English**. It is not the full standard, and it is not certified.

## What ASD-STE100 is

ASD-STE100 is a controlled natural language for technical documentation. Issue 9 was published in January 2025. It has two parts:

- 53 writing rules in 9 sections.
- A controlled dictionary of about 900 approved words.

ASD owns the standard. ASD-STE100 is a copyright and trademark of ASD, Brussels, Belgium. HASE is not affiliated with ASD or the STEMG. You can request the official copy from [asd-ste100.org](https://www.asd-ste100.org/). Do not copy the standard into HASE.

## What HASE takes from it

HASE uses a small, practical subset:

- Write short sentences.
- Write one instruction in one sentence.
- Use the imperative for actions.
- Use the active voice.
- Use one term for one concept.
- Put conditions first.
- Do not omit articles, subjects, or verbs.
- Keep noun clusters to three words or fewer.
- Do not use contractions, semicolons, or Latin abbreviations.
- Use one topic per paragraph.
- Use a vertical list for a sequence or a set of options.

HASE does not use the full STE dictionary. HASE uses project terms as technical nouns. Examples: `agent`, `user`, `repository`, `change`, `test`, `risk`, `frame`, `summary`, `state byte`, `playbook`.

## Sentence limits

- An instruction has a maximum of 20 words.
- A description has a maximum of 25 words.
- A note has a maximum of 25 words.
- A paragraph has a maximum of six sentences.

These limits are ceilings. Do not cut facts to obey them. If a sentence is too long, split it or use a list.

## HASE glossary

Use these terms with one meaning:

- **agent** — the AI system that reads HASE and changes the repository.
- **user** — the person who gives the task and approves irreversible actions.
- **repository** — the project files and history.
- **change** — one focused edit or patch.
- **test** — a check that gives evidence.
- **risk** — a possible failure, cost, or harmful outcome.
- **frame** — the `[STATE]`, `[PLAN]`, and `[SUMMARY]` header.
- **summary** — the one-line human and machine handoff.
- **state byte** — the two-digit hex value in the frame.
- **playbook** — the optional detailed reference in `docs/playbook.md`.

Do not use synonyms for these terms. Do not use `codebase` for `repository`. Do not use `assistant` for `agent`. Do not use `verification` when you mean `test`.

## Examples

Non-HASE:

> It is important to note that the implementation of the authentication flow should be carefully reviewed by the team before any changes are made to production.

HASE-STE:

> Review the authentication flow before you change production.

Non-HASE:

> The system will be able to provide an indication of whether or not the operation has completed successfully.

HASE-STE:

> The system reports when the operation completes.

## Meaning first

Do not change a technical fact to obey the style. Do not remove a qualifier, an object, or a condition. If a short sentence is false, write a longer correct sentence.

Examples:

- Keep `can` when the claim is conditional.
- Keep `may` when the risk is possible.
- Keep a named actor when the actor is known.
- Do not invent an actor when the source does not name one.

## Token effect

Short sentences and one term per concept reduce ambiguity. They often reduce rework and output length. They do not guarantee a token reduction. Measure the result. Do not remove evidence to save tokens.

## Limits

- HASE-STE is not a certified ASD-STE100 document.
- HASE does not include the STE dictionary.
- Code identifiers, API names, and project terms can violate STE spelling or word rules. Keep them exact.
- The full standard is the authority for aerospace or contractual STE work.

## Sources

- https://www.asd-ste100.org/
- https://www.asd-ste100.org/about_STE.html
- https://www.asd-ste100.org/STE_downloads.html
- ASD-STE100 Issue 9, January 2025 (official copy on request)
