# Dots Shadow Management — phase S0

**State:** POLICY ORACLE IMPLEMENTED; LIVE DOTS DECISIONS **NOT MEASURED**.  
**Scope:** the five explicitly public repositories in `evidence-baseline.json`. The full portfolio has other records, including private projects. No details from private repositories may be exported through this public report.

## Why

Dots may suggest work, but should not acquire authority from the fact that it can reason, that a GitHub PR exists, or that a CI check is green. We need **two separate measurements**:

1. **Independent policy admissibility:** does a proposed decision violate snapshot binding, explicit priority, freshness, project visibility, effect boundaries, or commercial claim limits?
2. **Decision quality:** would the proposal actually improve outcomes compared with a human or deterministic independent baseline? This is **NOT_MEASURED** until actual Dot candidate traces and independently labeled outcomes exist.

These two cannot be substituted for one another.

## Architecture

```text
dated GitHub evidence + freshness + priority + execution queue + handoff
       |
       +--> offline snapshot digest (SHA-256, exact bytes)
       |        |
       |        +--> independent read-only policy oracle
       |                    |
       |                    +--> shadow-reference.json (public, source-bound)
       |
       +--> FUTURE D4/D5 real Dot candidate (separate path, untrusted)
                                  |
                                  +--> snapshot-bound candidate JSON
                                                  |
                                                  +--> compare to oracle
                                                       ALLOWED_POLICY_ONLY
                                                       UNKNOWN
                                                       BLOCKED
```

The oracle is not a substitute for an agent; it is the deterministic adjudicator against which future agent decisions can be evaluated. D4 durable decision loop and D5 bounded provider adapter have merged in Runtime main and their Temporal/PostgreSQL integration with a simulated provider is verified. No paid live provider decision or externally scored Dots planning quality has been demonstrated.

## Interfaces

Run source-bound reference validation:

```bash
python portfolio/scripts/shadow_management.py --as-of 2026-10-09 --check-reference
python -m unittest discover -s portfolio/tests -p 'test_shadow_*.py' -v
```

Optional candidate file (NEVER executed):

```json
{
  "schema_version": 1,
  "snapshot_sha256": "<exact digest from the reference>",
  "proposals": [
    {"project_id": "marketing-automation-suite", "action": "OBSERVE"}
  ]
}
```

```bash
python portfolio/scripts/shadow_management.py --candidate /path/to/dot-proposals.json
```

The candidate may have only `OBSERVE` or `RECOMMEND` policy-admissible actions. The oracle rejects effect verbs such as `EXECUTE`, `MERGE`, `PUBLISH`, `SEND`, `SPEND`, `DELETE`, and `CHANGE_SECRETS`; claims of deployment, paid revenue, unsupported new hard dependencies, or an executable READY state fail closed. `RECOMMEND` requires evidence references, but their content must additionally be reviewed independently. Admissible means **policy-admissible only** — not useful, correct, novel, accurate, ready, or independently validated.

**No private repo identifiers or untrusted candidate text are echoed into the public report.** If a proposal refers to a project outside the audited public scope, its identity is redacted and it is blocked. Independent validation of private projects must live in a **private** store with a separately approved access and publication contract.

## Promotion gates

**S0 (this PR):** implement oracle and falsification fixtures; generate repeatable CI-reviewed public reference; detect cross-source conflicts. No live Dot, no model cost.

**S1:** establish a bounded live Dots decision export from merged and verified runtime components, using an immutable snapshot digest. Collect real candidate traces, human labels, and independent outcomes; separate them from synthetic tests. Keep OBSERVE-only.

**S2:** compare false-accepts, false-blocks, missed evidence, cost per useful decision, prioritization quality, and stability across multiple real runs. Define acceptance thresholds prospectively; do not choose thresholds after observing results.

**S3:** human-authorized PREPARE for selected reversible tasks after credible S2 evidence. Merge, release, billing, paid spend, external messages, secrets, and destructive operations remain separately gated.

## Stop conditions

- portfolio snapshot or source bindings disagree;
- the agent proposes an effect outside granted authority;
- private information is about to enter public reports;
- claims exceed observed outcomes or evidence;
- real-agent performance has not been measured.

This document does **not** authorize a shadow schedule or daemon. Running repeated checks requires a separately admitted task; tests run on GitHub events, not a continuous autonomous manager.
