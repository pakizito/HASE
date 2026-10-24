# Security policy

## Supported versions

HASE is a set of plain-text instructions and local developer tools. Security fixes are applied to the current major version, currently **8.x**.

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue, discussion, or pull request.

Use GitHub's private vulnerability reporting for this repository:

1. Open the repository's **Security** tab.
2. Choose **Report a vulnerability**.
3. Include the affected file, version, impact, and a minimal reproduction or proof of concept.

If private reporting is unavailable, open a public issue that asks the maintainer to establish a private channel, without including exploit details, secrets, or personal data.

## Scope

Relevant reports include:

- unexpected command execution, network access, or filesystem writes by the local tools;
- path traversal or unsafe overwrite behaviour in `tools/context_graph.py` or `tools/render_adapters.py`;
- secret leakage in generated files or logs;
- instructions that could cause an agent to perform destructive or unauthorised actions.

HASE cannot enforce its own rules. A model that ignores the contract is a product limitation, not a vulnerability by itself, unless the tooling makes the unsafe outcome materially easier.

## Handling secrets

Never include credentials, tokens, private keys, customer data, or production configuration in an issue, test fixture, or example. Redact them before reporting.
