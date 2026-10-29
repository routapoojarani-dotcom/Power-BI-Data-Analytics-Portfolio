# Security Guide

This is an educational application using fictional data. It demonstrates safe defaults but is not
a production security boundary.

## Threat model

Tools make an agent useful and risky: they can reach data or perform actions. Treat model output as
untrusted input and tool output as untrusted data. A prompt cannot grant itself permission.

## Controls included

- Credentials are environment variables represented as `SecretStr`; `.env` is ignored.
- Azure secrets are used server-side and never placed in Jinja templates or JavaScript.
- The calculator parses an AST and rejects names, calls, imports, shell commands, and large powers.
- Sample employee/order tools are read-only and validate identifiers.
- Knowledge files are read from one fixed directory; users cannot provide file paths.
- User message and HTTP body sizes are limited.
- Agent iterations, tool calls, and graph recursion are bounded.
- Browser session cookies are signed, HTTP-only, and `SameSite=Lax`.
- Public activity contains protocol events, not hidden reasoning or system prompts.
- The destructive checkpoint cleanup script only deletes within `data/checkpoints` and requires
  confirmation unless `--yes` is supplied.

## Before production

1. Add authentication and per-user/tenant authorization.
2. Authorize every tool invocation against the current user—do not rely on the model.
3. Replace the development session/checkpointer setup with shared, encrypted stores.
4. Add CSRF protection to form routes and strong API authentication.
5. Enforce HTTPS, `Secure` cookies, trusted hosts, proxy headers, and secret rotation.
6. Add rate limits, request timeouts, retries with backoff, circuit breakers, and quotas.
7. Redact personal data and secrets from prompts, tool observations, logs, traces, and errors.
8. Give each tool the minimum network, filesystem, and database permissions it needs.
9. Require durable human approval for payments, deletion, messages, and record changes.
10. Make side effects idempotent and attach approval identity, timestamp, scope, and expiry.
11. Test prompt injection: retrieved documents may contain malicious instructions.
12. Add dependency, secret, SAST, DAST, and container/image scanning.
13. Define retention/deletion rules for conversations and checkpoints.
14. Evaluate tool selection, argument correctness, groundedness, refusal, and loop behavior.

## Human approval is not a button alone

Production approval must be bound to an authenticated reviewer and the exact proposed action. If
the amount, recipient, order, or payload changes after approval, require a new approval. Log the
decision without logging sensitive content unnecessarily.

## Reporting a vulnerability

Do not open a public issue containing credentials, customer data, or exploit details. Contact the
repository owner privately and include the affected version, impact, and a minimal safe reproduction.

