# 0004 — Adopt HASE-STE

- **Status:** Accepted
- **Date:** 2026-10-25
- **Deciders:** HASE maintainers

## Context

HASE v9.2 was shorter than v9.1, but many instructions still used long sentences and mixed terms. Long instructions cost tokens. They also increase ambiguity, especially when another agent parses the result.

ASD-STE100 is a controlled natural language for technical documentation. Issue 9, January 2025, has 53 writing rules and a controlled dictionary of about 900 words. It is owned by ASD. A full implementation would need the dictionary and certification. That is too heavy for a portable agent file.

## Decision

Add a small style layer called HASE-STE:

- short sentences;
- one instruction per sentence;
- imperative and active voice;
- one term for one concept;
- conditions first;
- no omitted articles, subjects, or verbs;
- no contractions, semicolons, or Latin abbreviations;
- three-word maximum for noun clusters;
- a small glossary for HASE terms.

HASE-STE is not certified ASD-STE100. HASE does not copy the standard or its dictionary. It uses selected principles and cites the official source.

## Consequences

**Positive**

- Shorter, clearer instructions.
- More predictable output for humans and agents.
- Fewer synonyms and less ambiguity.
- A smaller default core: about 8.9 KB.

**Negative**

- HASE cannot claim ASD-STE100 compliance.
- Some technical names and code identifiers do not follow STE.
- The style requires review; it is not a mechanical word replacement.
- The 20/25-word limits can split complex ideas and add structure.

## Alternatives considered

- **Adopt the full ASD-STE100 dictionary.** Rejected: too large for a one-file agent contract and not licensed for embedding.
- **Use plain terse English.** Rejected: shorter, but less consistent and easier to misread.
- **Use JSON for all output.** Rejected: too rigid for human readers and code review.

## Follow-up

- Review HASE examples for sentence length and term consistency.
- Keep code identifiers and official API names exact.
- Do not add a compliance claim without a licensed review.
