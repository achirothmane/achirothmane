# Priority / Next-Action Report

> Priority is gate-based, not a technical-activity score.
> **ACTIVE does not mean NOW.** Human directives and evidence outrank repository activity.

**As of:** 2026-10-06  
**NOW:** 1 / cap 3  
**NEXT:** 4 / cap 6  
**WATCH:** 19  
**PARKED:** 13  
**REVERIFY:** 0  
**CLOSED:** 1

## Current focus

Only **one project currently consumes a NOW slot**:

- `data-engine` — prove capability contracts and explicit failure boundaries across inherited and new capabilities.

The remaining NOW capacity is intentionally unused. Empty WIP capacity is preferable to promoting projects without enough evidence.

## Lane semantics

| Lane | Meaning |
|---|---|
| NOW | explicit current focus; eligible to consume active build time |
| NEXT | concrete next gate, but not current WIP |
| WATCH | observe / validate / wait for evidence; do not create work merely for activity |
| PARKED | intentionally inactive until a named re-entry condition is met |
| REVERIFY | state is too stale or unknown for material decisions |
| CLOSED | direction is closed; preserve evidence only unless separately extracted |

## NOW

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `data-engine` | broad self-use foundational asset that compounds across future systems | prove capability contracts and explicit failure boundaries on inherited and new capabilities | — | COMPLETE |

## NEXT

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `marketing-automation-suite` | broad self-use-first system; commercial narrowing comes later | establish the repository and first useful general capability after the Data Engine boundary is usable | — | COMPLETE |
| `mini-foot` | active product experiment with a clear retention gate | reach enjoyable playable feel and voluntary rematch evidence | — | COMPLETE |
| `postgres-change-safety` | product asset with a concrete value-validation gate | prove repeatable user value and packaging | — | COMPLETE |
| `private-code-modernization-factory` | retest candidate with explicit verification and onboarding gaps | prove reliable verification and onboarding before expansion | verification confidence; onboarding quality | COMPLETE |

## WATCH

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `ci-retry-gate-engine` | engineering is frozen while waiting for E1 real-exposure evidence | observe for real exposure and E1; do not add features merely to create activity | external action trust boundary | COMPLETE |
| `ci-retry-gate-consumer-e2e` | validation support asset for CI Retry Gate rather than an independent focus | maintain consumer-path proof only when needed for the E1/adoption question | — | COMPLETE |
| `workflow-failure-lab` | evidence-support asset for CI reliability work | add failure evidence only when it answers a live product or integration question | — | COMPLETE |
| `releaseguard-n8n` | prior marketplace learning exists but depth/readiness must be proven before republishing | prove sufficient product depth and readiness rather than adding superficial features | — | INCOMPLETE |
| `conversion-truth-auditor` | commercial value still needs evidence before more engineering | establish differentiated economic value and packaging before new build work | — | COMPLETE |
| `ai-deployer` | ACTIVE does not imply NOW without explicit promotion or strong economic evidence | identify reusable capability with proven demand | — | INCOMPLETE |
| `air-combat` | private project lacks a concrete next gate | UNKNOWN | — | INCOMPLETE |
| `atlassian-revenue-integrity` | ACTIVE does not imply NOW without explicit promotion or strong economic evidence | validate demand and packaging | — | INCOMPLETE |
| `claude-mem` | evaluation asset is not promoted to current focus | determine whether any capability is independently valuable | — | INCOMPLETE |
| `conversionguard` | active overlap question must be resolved before expansion | determine overlap or composition with conversion-truth-auditor before expansion | — | INCOMPLETE |
| `creator-docs` | ACTIVE does not imply NOW without explicit promotion or strong economic evidence | clarify product role before composition | — | INCOMPLETE |
| `creature-isles` | private project lacks a concrete next gate | UNKNOWN | — | INCOMPLETE |
| `e2e` | evaluation asset is not promoted to current focus | identify concrete reusable test capability | — | INCOMPLETE |
| `firebase-auth-email-canary` | ACTIVE does not imply NOW without explicit promotion or strong economic evidence | prove recurring operational value | — | COMPLETE |
| `flowmeter-for-jira-forge` | retest requires readiness evidence after prior marketplace rejection | only retest after readiness evidence | prior marketplace rejection | INCOMPLETE |
| `future-morocco-lab` | private exploration has no concrete next gate | UNKNOWN | — | INCOMPLETE |
| `grok-build` | evaluation asset is not promoted to current focus | clarify owned capability and value | — | INCOMPLETE |
| `smart-fuel-morocco` | private product requires retention and monetization evidence before promotion | validate retention and monetization | — | INCOMPLETE |
| `window-worlds-lab` | private exploration has no concrete next gate | UNKNOWN | — | INCOMPLETE |

## PARKED

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `easl` | reusable primitive must not become a required dependency without a real consumer | reactivate only when a concrete downstream consumer proves value | — | COMPLETE |
| `assumption-gate` | reusable primitive is awaiting a real consumer | reactivate only for a concrete consumer integration | — | COMPLETE |
| `token-governance-protocol` | reusable primitive is awaiting a genuine token-budget consumer | reactivate only for a real agent or model execution budget need | — | COMPLETE |
| `intelligence-layer` | standalone extraction is not justified until a real second consumer exists | keep reasoning capability inside the consuming system until extraction is justified | — | INCOMPLETE |
| `revenue-engine` | deferred until upstream data and marketing capabilities produce real operational evidence | wait for upstream evidence | upstream capabilities not yet mature | INCOMPLETE |
| `agent-action-guard` | status HOLD is parked by policy | concrete consumer required | — | INCOMPLETE |
| `agent-model-gate` | status HOLD is parked by policy | concrete consumer required | — | INCOMPLETE |
| `caddy` | independent fork is not an active portfolio dependency | define owned delta before portfolio promotion | — | INCOMPLETE |
| `esp32-c3-adblock` | independent experiment is not promoted to active focus | UNKNOWN | — | INCOMPLETE |
| `geophires-x` | independent exploration lineage is not promoted to active focus | UNKNOWN | — | INCOMPLETE |
| `governed-agent-runtime` | status HOLD is parked by policy | re-enter active graph only with concrete consumer and measurable benefit | — | INCOMPLETE |
| `legal-authority-diff` | status HOLD is parked by policy | concrete consumer required | — | INCOMPLETE |
| `stremio-web` | independent fork is not an active portfolio dependency | define owned delta before portfolio promotion | — | INCOMPLETE |

## REVERIFY

_None._

## CLOSED

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `aegis-ege` | commercial platform direction is closed | extract only independently proven reusable capabilities when another project demonstrates the need | — | COMPLETE |

## Invariants

- No project enters NOW because it is technically interesting or recently active.
- STALE or UNKNOWN freshness overrides priority and becomes REVERIFY.
- A blocker remains visible; priority does not erase it.
- Missing economic evidence remains UNKNOWN rather than being inferred from technical evidence.
- Human strategic directives remain authoritative over derived lanes.
- WIP caps are limits, not targets: unused slots should remain empty rather than be filled artificially.
