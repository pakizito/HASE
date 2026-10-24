# Threat model template

Use for T2 changes: authentication, authorisation, payments, personal data, public APIs, destructive migrations, AI safety controls, or anything crossing a trust boundary.

## System and change

- **System:**
- **Change:**
- **Owner:**
- **Date:**

## Assets

What is worth protecting? Data, money, availability, reputation, model integrity, audit evidence.

## Actors

Who or what can interact? Anonymous users, authenticated users, administrators, services, operators, attackers, insiders, automated agents.

## Entry points

APIs, UI forms, webhooks, queues, file uploads, model prompts, admin tools, scheduled jobs, dependencies.

## Trust boundaries

Where does data or authority cross from one trust level to another? Browser to API, API to database, service to provider, model to tool.

## Threats

| Threat | Path | Impact | Existing control | Residual risk |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Consider: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege, injection, SSRF, path traversal, unsafe deserialisation, prompt injection, supply-chain compromise.

## Mitigations

- <control, where it lives, and how it is tested>

## Verification

- [ ] Authorisation tests cover allowed and denied paths.
- [ ] Input validation and output encoding are tested.
- [ ] Secrets are not present in source, logs, fixtures, or error messages.
- [ ] Dependency and licence checks are complete.
- [ ] Abuse, rate-limit, and failure paths are tested.
- [ ] Residual risk is accepted by the appropriate owner.

## Residual risk and sign-off

- **Accepted risk:**
- **Approver:**
- **Review date:**
