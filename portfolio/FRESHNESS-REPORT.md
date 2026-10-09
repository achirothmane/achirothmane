# Freshness Report

> Generated from project `last_verified` values and `portfolio/freshness-policy.yaml`.
> Freshness measures recency, not truth completeness.

**As of:** 2026-10-09  
**Projects:** 40  
**FRESH:** 40  
**AGING:** 0  
**STALE:** 0  
**UNKNOWN freshness:** 0  
**Incomplete records (contain UNKNOWN values):** 24

## Action semantics

| Freshness | Meaning | Material action |
|---|---|---|
| FRESH | recently verified for its policy class | normal gates apply |
| AGING | still usable, but current-state-sensitive decisions should reverify | verify when material |
| STALE | verification age exceeded | reverify first |
| UNKNOWN | no usable verification date | reverify first |

## Projects

| Project | Status | Class | Freshness | Age | Completeness |
|---|---|---|---|---:|---|
| `aegis-ege` | CLOSED_COMMERCIAL | dormant | **FRESH** | 3 | COMPLETE |
| `agent-action-guard` | HOLD | dormant | **FRESH** | 3 | INCOMPLETE |
| `agent-deal-exchange` | ACTIVE | active | **FRESH** | 0 | COMPLETE |
| `agent-model-gate` | HOLD | dormant | **FRESH** | 3 | INCOMPLETE |
| `ai-deployer` | ACTIVE | active | **FRESH** | 3 | INCOMPLETE |
| `air-combat` | PRIVATE | review | **FRESH** | 3 | INCOMPLETE |
| `assumption-gate` | ACTIVE | active | **FRESH** | 3 | INCOMPLETE |
| `atlassian-revenue-integrity` | ACTIVE | active | **FRESH** | 3 | INCOMPLETE |
| `caddy` | FORK_INDEPENDENT | dormant | **FRESH** | 3 | INCOMPLETE |
| `ci-retry-gate-consumer-e2e` | ACTIVE_PRIVATE | active | **FRESH** | 3 | COMPLETE |
| `ci-retry-gate-engine` | ACTIVE_PRIVATE | active | **FRESH** | 3 | COMPLETE |
| `claude-mem` | EVALUATE | review | **FRESH** | 3 | INCOMPLETE |
| `conversion-truth-auditor` | ACTIVE | active | **FRESH** | 3 | COMPLETE |
| `conversionguard` | ACTIVE | active | **FRESH** | 3 | INCOMPLETE |
| `creator-docs` | ACTIVE | active | **FRESH** | 3 | INCOMPLETE |
| `creature-isles` | PRIVATE | review | **FRESH** | 3 | INCOMPLETE |
| `data-engine` | ACTIVE | active | **FRESH** | 0 | COMPLETE |
| `e2e` | EVALUATE | review | **FRESH** | 3 | INCOMPLETE |
| `easl` | ACTIVE | active | **FRESH** | 3 | COMPLETE |
| `esp32-c3-adblock` | INDEPENDENT | dormant | **FRESH** | 3 | INCOMPLETE |
| `firebase-auth-email-canary` | ACTIVE | active | **FRESH** | 3 | COMPLETE |
| `flowmeter-for-jira-forge` | PRIVATE_RETEST | review | **FRESH** | 3 | INCOMPLETE |
| `future-morocco-lab` | PRIVATE | review | **FRESH** | 3 | INCOMPLETE |
| `geophires-x` | INDEPENDENT | dormant | **FRESH** | 3 | INCOMPLETE |
| `github-test-reporter` | EVALUATE | review | **FRESH** | 0 | COMPLETE |
| `governed-agent-runtime` | ACTIVE | active | **FRESH** | 0 | COMPLETE |
| `grok-build` | EVALUATE | review | **FRESH** | 3 | INCOMPLETE |
| `intelligence-layer` | PLANNED | planned | **FRESH** | 3 | INCOMPLETE |
| `legal-authority-diff` | HOLD | dormant | **FRESH** | 3 | INCOMPLETE |
| `marketing-automation-suite` | ACTIVE | active | **FRESH** | 0 | COMPLETE |
| `mini-foot` | ACTIVE_PRIVATE | active | **FRESH** | 3 | COMPLETE |
| `postgres-change-safety` | ACTIVE | active | **FRESH** | 3 | COMPLETE |
| `private-code-modernization-factory` | RETEST | review | **FRESH** | 3 | COMPLETE |
| `releaseguard-n8n` | ACTIVE | active | **FRESH** | 3 | INCOMPLETE |
| `revenue-engine` | DEFERRED | dormant | **FRESH** | 3 | INCOMPLETE |
| `smart-fuel-morocco` | PRIVATE | review | **FRESH** | 3 | INCOMPLETE |
| `stremio-web` | FORK_INDEPENDENT | dormant | **FRESH** | 3 | INCOMPLETE |
| `token-governance-protocol` | ACTIVE | active | **FRESH** | 3 | COMPLETE |
| `window-worlds-lab` | PRIVATE | review | **FRESH** | 3 | INCOMPLETE |
| `workflow-failure-lab` | ACTIVE | active | **FRESH** | 3 | COMPLETE |

## Dependency freshness risks

No registered hard dependency currently points to STALE or UNKNOWN upstream state.

## Invariant

> A stale record is not automatically false; it is **inadmissible as current-state evidence** until reverified when a material decision depends on it.

A FRESH record may still be incomplete. `UNKNOWN` values remain unknown even when the record itself is fresh.
