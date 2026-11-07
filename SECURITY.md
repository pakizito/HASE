# Security policy

## Supported versions

HASE is a plain-text instruction file. Security fixes apply to the current major version, currently **10.x**.

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue, discussion, or pull request.

Use GitHub's private vulnerability reporting for this repository:

1. Open the repository's **Security** tab.
2. Choose **Report a vulnerability**.
3. Include the affected section, version, impact, and a minimal reproduction.

If private reporting is unavailable, open a public issue that asks the maintainer to establish a private channel. Do not include exploit details, secrets, or personal data.

## Scope

Relevant reports include:

- instructions that could cause an agent to perform destructive or unauthorised actions;
- secret leakage in examples, memory, or generated output;
- a rule that weakens auth, data, or verification boundaries;
- unsafe handling of `.hase/memory.json`.

HASE cannot enforce its own rules. A model that ignores the contract is a product limitation, not a vulnerability by itself.

## Handling secrets

Never include credentials, tokens, private keys, customer data, or production configuration in an issue, test, or example. Redact them before reporting.
