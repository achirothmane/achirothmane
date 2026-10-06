# Portfolio Contracts

These files describe **real cross-project relationships** only.

They do not replace repository-local APIs, schemas, or protocol specifications. Their job is to tell the portfolio operating layer — and later a Dot/agent — which projects actually exchange capability, evidence, decisions, or validation.

## Rules

- No contract from thematic similarity.
- No hard dependency unless one project truly cannot satisfy its role without the other.
- A producer does not automatically become a runtime dependency.
- Ownership stays with the project that owns the capability or evidence.
- Implementation-level schemas remain in the owning repositories.
- If evidence is insufficient, keep the relationship out of this directory.

## Active chain

```text
Workflow Failure Lab
   │ evidence feed (non-hard dependency)
   ▼
CI Retry Gate Engine
   │ engine dependency + integration contract
   ▼
CI Retry Gate Consumer E2E
```
