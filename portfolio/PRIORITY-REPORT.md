# Priority / Next-Action Report

> Priority is gate-based, not a technical-activity score.
> ACTIVE does not mean NOW. Human directives and evidence outrank repository activity.

**As of:** 2026-10-09  
**NOW:** 2 / cap 3  
**NEXT:** 4 / cap 6  
**WATCH:** 21  
**PARKED:** 12  
**REVERIFY:** 0  
**CLOSED:** 1

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
| `data-engine` | broad self-use foundational asset that compounds across future systems | PR #7 already merged 2026-10-07; verify current main and individually review outstanding reconciliation PRs against evidence | — | COMPLETE |
| `governed-agent-runtime` | human-authorized single read-only Dots shadow observation; not a general runtime expansion | Use sealed Portfolio context to propose one next evidence-verification gate; separately let a human compare merged PR #25 #28 #29 and CI | create/lost-ACK case blocked by GitHub 403; independent Dots portfolio-management quality unverified; no live paid OpenAI Portfolio Dot reasoning call or human-scored decision yet | COMPLETE |

## NEXT

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `marketing-automation-suite` | broad self-use-first system intended to replace paid tooling before commercial narrowing | repository exists and scoped C4-05B is merged; verify C4-05C safe scheduler, crash recovery and full integration before operational claims | full C4 end-to-end unverified; production deployment and marketing sends unverified | COMPLETE |
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
| `agent-deal-exchange` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | verify Medusa build, two-account authorization, nested licensing and settlement boundaries before adopting upstream as main capability | upstream Medusa functional build not admitted on main; no real transaction or settlement evidence | COMPLETE |
| `ai-deployer` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | identify reusable capability with proven demand | — | INCOMPLETE |
| `air-combat` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | UNKNOWN | — | INCOMPLETE |
| `atlassian-revenue-integrity` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | validate demand and packaging | — | INCOMPLETE |
| `claude-mem` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | determine whether any capability is independently valuable | — | INCOMPLETE |
| `conversionguard` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | determine overlap or composition with conversion-truth-auditor before expansion | — | INCOMPLETE |
| `creator-docs` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | clarify product role before composition | — | INCOMPLETE |
| `creature-isles` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | UNKNOWN | — | INCOMPLETE |
| `e2e` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | identify concrete reusable test capability | — | INCOMPLETE |
| `firebase-auth-email-canary` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | prove recurring operational value | — | COMPLETE |
| `flowmeter-for-jira-forge` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | only retest after readiness evidence | prior marketplace rejection | INCOMPLETE |
| `future-morocco-lab` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | UNKNOWN | — | INCOMPLETE |
| `github-test-reporter` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | prove adapter test correctness and consumer integration; separate inherited upstream features from our differentiators | verified paid use absent from audit | COMPLETE |
| `grok-build` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | clarify owned capability and value | — | INCOMPLETE |
| `smart-fuel-morocco` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | validate retention and monetization | — | INCOMPLETE |
| `window-worlds-lab` | active/reviewable does not imply NOW without explicit promotion or strong economic evidence | UNKNOWN | — | INCOMPLETE |

## PARKED

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `easl` | reusable primitive must not become a required dependency without a real consumer | reactivate only when a concrete downstream consumer proves value | — | COMPLETE |
| `assumption-gate` | reusable primitive awaiting a real consumer | reactivate only for a concrete consumer integration | — | INCOMPLETE |
| `token-governance-protocol` | reusable primitive awaiting a genuine token-budget consumer | reactivate only for a real agent or model execution budget need | — | COMPLETE |
| `intelligence-layer` | do not create a standalone layer until a real second consumer exists | keep reasoning capability inside the consuming system until extraction is justified | — | INCOMPLETE |
| `revenue-engine` | deferred by design until upstream data and marketing capabilities produce real operational evidence | wait for upstream evidence | upstream capabilities not yet mature | INCOMPLETE |
| `agent-action-guard` | status HOLD is parked by policy | concrete consumer required | — | INCOMPLETE |
| `agent-model-gate` | status HOLD is parked by policy | concrete consumer required | — | INCOMPLETE |
| `caddy` | status FORK_INDEPENDENT is parked by policy | define owned delta before portfolio promotion | — | INCOMPLETE |
| `esp32-c3-adblock` | status INDEPENDENT is parked by policy | UNKNOWN | — | INCOMPLETE |
| `geophires-x` | status INDEPENDENT is parked by policy | UNKNOWN | — | INCOMPLETE |
| `legal-authority-diff` | status HOLD is parked by policy | concrete consumer required | — | INCOMPLETE |
| `stremio-web` | status FORK_INDEPENDENT is parked by policy | define owned delta before portfolio promotion | — | INCOMPLETE |

## REVERIFY

_None._

## CLOSED

| Project | Why | Next action | Blockers | Knowledge |
|---|---|---|---|---|
| `aegis-ege` | commercial or project direction is explicitly closed | extract only independently proven reusable capabilities when another project demonstrates the need | — | COMPLETE |

## Invariants

- No project enters NOW because it is technically interesting or recently active.
- STALE or UNKNOWN freshness overrides priority and becomes REVERIFY.
- A blocker remains visible; priority does not erase it.
- Missing economic evidence remains UNKNOWN rather than being inferred from technical evidence.
- Human strategic directives remain authoritative over derived lanes.
