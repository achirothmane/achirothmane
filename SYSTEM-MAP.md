# System Map

> Canonical portfolio map for long-running projects, shared capabilities, real dependencies, and future agent/Dot operation.

**Owner:** achirothmane  
**Status:** ACTIVE  
**Last structural review:** 2026-10-06

---

## 1. Purpose

This file is the top-level operating map for the portfolio.

It exists to answer, for every project:

- What does it own?
- What does it produce?
- What does it consume?
- What other project does it genuinely depend on?
- What is its current state?
- What is the next gate?
- What evidence justifies promoting it, composing it, publishing it, or stopping it?

The map must not manufacture architecture.

> **Projects are connected only when a real flow of data, capability, decision, evidence, or distribution exists between them.**

No shared owner is enough. No thematic similarity is enough. No future possibility is enough.

---

## 2. Portfolio operating model

```text
                         SYSTEM MAP
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
   Shared Capabilities   Products/Engines   Independent Labs
          │                  │                  │
          └──────── real contracts only ───────┘
                             │
                    Evidence / State / Gates
                             │
                 Distribution / Revenue Layer
                             │
                    Human decision authority
                             │
                 Future Portfolio Dot / Agent
```

### Future Dot role

A future portfolio Dot should consume this map as its primary navigation layer.

It may:

- inspect project state;
- follow declared dependencies;
- identify stale or missing evidence;
- propose the next gate;
- coordinate work across repositories;
- surface conflicts between projects;
- call execution tools when authorized.

It must **not** infer undeclared dependencies or silently collapse repositories into one platform.

---

## 3. Relationship vocabulary

Only these relationship types should be used unless a new type proves necessary:

| Relation | Meaning |
|---|---|
| `PRODUCES` | Creates data, evidence, artifacts, or capabilities consumed elsewhere |
| `CONSUMES` | Uses an output owned elsewhere |
| `DEPENDS_ON` | Cannot satisfy its contract without another project/capability |
| `VALIDATES` | Tests or falsifies claims made by another project |
| `DISTRIBUTES` | Delivers another asset to users/channels |
| `COMPOSES_WITH` | Optional composition; neither side loses independent ownership |
| `SUPERSEDES` | Replaces an older implementation or direction |
| `ARCHIVES` | Preserves evidence/history without active expansion |

---

## 4. Shared capability layer

These are the strongest candidates for reusable portfolio primitives.

### Data Engine — `achirothmane/data-engine`

**Role:** trustworthy data capability layer.  
**Owns:** ingestion-derived knowledge processing, profiling, cleaning, schema inference, reconciliation, indexing/learning boundaries.  
**Doctrine:** build the capability and its boundary together.  
**Boundary states:** KNOWN / ACCEPTED, UNKNOWN, AMBIGUOUS, CONFLICTING, REFUSED / UNSUPPORTED.  
**Produces:** trusted structured knowledge + provenance + decision evidence.  
**Potential consumers:** Marketing Automation Suite, Intelligence Layer, analytics products, future media/research systems.  
**Current state:** ACTIVE / foundational.  
**Next gate:** prove capability contracts and explicit failure boundaries on inherited + new capabilities.

### Workflow Failure Lab — `achirothmane/workflow-failure-lab`

**Role:** reliability/failure experimentation asset.  
**Owns:** workflow failure corpus, retry behavior experiments, reproducible CI failure knowledge.  
**Produces:** failure evidence and test cases.  
**Composes with:** CI Retry Gate assets and future DevEx/reliability products.  
**Current state:** ACTIVE.

### CI Retry Gate Engine — `achirothmane/ci-retry-gate-engine`

**Role:** retry decision capability.  
**Owns:** evidence-based retry logic for CI failure classes.  
**Produces:** retry/no-retry decisions and causal evidence.  
**Validated by:** consumer E2E + Workflow Failure Lab.  
**Current state:** PRIVATE / validation asset.

### CI Retry Gate Consumer E2E — `achirothmane/ci-retry-gate-consumer-e2e`

**Role:** adoption/integration proof harness.  
**Validates:** CI Retry Gate integration path and trust boundary.  
**Current state:** PRIVATE / evidence asset.

### EASL — `achirothmane/easl`

**Role:** assumption/evidence state semantics.  
**Owns:** assumption lifecycle, temporal validity, contradiction/invalidation semantics.  
**Current state:** ACTIVE research/engineering primitive.  
**Constraint:** do not force downstream products to depend on it without demonstrated value.

### Assumption Gate — `achirothmane/assumption-gate-`

**Role:** executable assumption admission primitive.  
**Consumes:** assumption/evidence state.  
**Produces:** allow / deny / unknown-style gate decisions.  
**Current state:** ACTIVE primitive.

### Token Governance Protocol — `achirothmane/token-governance-protocol`

**Role:** budget/consumption governance primitive.  
**Owns:** reservation semantics, budget model, exhaustion policy.  
**Current state:** ACTIVE primitive.

---

## 5. Product and engine layer

### Marketing Automation Suite — repository pending

**Role:** broad self-use-first marketing operations system.  
**Consumes:** trusted data/knowledge when useful.  
**Potential producer:** campaign events, audience behavior, channel performance, operational feedback.  
**Constraint:** do not narrow to a niche early.  
**Current state:** PLANNED / architecture evolving.  
**Future relationship:** likely `CONSUMES data-engine` only after a real integration contract exists.

### Intelligence Layer — repository pending

**Role:** cross-system reasoning/analysis capability.  
**Current state:** PLANNED.  
**Constraint:** do not create as a vague AI umbrella; it must own concrete capabilities and boundaries.

### Revenue Engine — deferred

**Role:** monetization/revenue operations layer.  
**Current state:** DEFERRED by design.  
**Entry condition:** only after upstream data + marketing capabilities are useful to us and produce real operational evidence.

### PostgreSQL Change Safety — `achirothmane/postgres-change-safety`

**Role:** database change reliability product/asset.  
**Owns:** observation and regression evidence around PostgreSQL changes.  
**Current state:** ACTIVE.

### Conversion Truth Auditor — `achirothmane/conversion-truth-auditor`

**Role:** conversion measurement verification.  
**Owns:** journey/signal verification experiments.  
**Current state:** ACTIVE / product exploration.

### ConversionGuard — `achirothmane/conversionguard`

**Role:** conversion integrity capability/product line.  
**Current state:** ACTIVE / evaluate overlap with Conversion Truth Auditor before composition.

### Atlassian Revenue Integrity — `achirothmane/atlassian-revenue-integrity`

**Role:** revenue/integrity product in Atlassian ecosystem.  
**Current state:** PRODUCT ASSET.

### FlowMeter for Jira Forge — `achirothmane/flowmeter-for-jira-forge`

**Role:** Jira/Forge product asset.  
**Current state:** PRIVATE / prior marketplace learning.

### ReleaseGuard n8n — `achirothmane/releaseguard-n8n`

**Role:** workflow/release evidence product.  
**Current state:** ACTIVE product asset.

### Private Code Modernization Factory — `achirothmane/private-code-modernization-factory`

**Role:** AI-assisted modernization with verification loop.  
**Current state:** RETEST / needs stronger verification and onboarding evidence.

### Firebase Auth Email Canary — `achirothmane/firebase-auth-email-canary`

**Role:** auth-email delivery reliability monitor.  
**Current state:** ACTIVE small reliability asset.

### AI Deployer — `achirothmane/ai-deployer`

**Role:** deployment/operation experiments for AI-enabled software.  
**Current state:** ACTIVE learning/build asset.

### Smart Fuel Morocco — `achirothmane/smart-fuel-morocco`

**Role:** consumer fuel-price/product experiment.  
**Current state:** PRIVATE product asset.

### Creator Docs — `achirothmane/creator-docs`

**Role:** documentation/content product asset.  
**Current state:** ACTIVE repository; composition not yet declared.

---

## 6. Governance / verification lineage

These repositories remain valuable as engineering evidence, primitives, or historical lineage, but are **not automatically a commercial platform**.

### Aegis-EGE — `achirothmane/aegis-ege`

**Commercial state:** CLOSED / DEAD as a standalone commercial platform.  
**Preserve:** falsification evidence, reusable primitives, historical engineering proof.  
**Do not:** revive generic agent-control/IAM/orchestration positioning under a new name.  
**Allowed:** extract independently valuable capabilities only when another project proves the need.

### Governed Agent Runtime — `achirothmane/governed-agent-runtime`
### Agent Action Guard — `achirothmane/agent-action-guard`
### Agent Model Gate — `achirothmane/agent-model-gate`
### Legal Authority Diff — `achirothmane/legal-authority-diff`

**Portfolio treatment:** verification/governance lineage.  
**Default relation:** none.  
**Promotion rule:** only re-enter the active capability graph when a current product has a concrete dependency and measurable benefit.

---

## 7. Games and interactive systems

These are independent product lines. Shared ownership does not imply dependency on the software/AI portfolio.

### Mini Foot — `achirothmane/mini-foot`

**Role:** mobile 4v4 football game.  
**Core engineering:** deterministic simulation, fixed tick, clean identity/control separation.  
**Primary KPI:** Rematch Rate.  
**Current state:** PRIVATE / active game project.

### Air Combat — `achirothmane/air-combat`

**Current state:** PRIVATE game project.  
**Relation:** independent until a reusable game capability is proven.

### Creature Isles — `achirothmane/creature-isles`

**Current state:** PRIVATE game project.  
**Relation:** independent until a reusable game capability is proven.

---

## 8. Labs, forks, and exploration assets

These repositories are intentionally not forced into the main product graph.

| Repository | Portfolio role | Default state |
|---|---|---|
| `future-morocco-lab` | private exploration lab | INDEPENDENT |
| `window-worlds-lab` | private exploration lab | INDEPENDENT |
| `GEOPHIRES-X` | external/domain exploration lineage | INDEPENDENT |
| `claude-mem` | memory/tooling exploration | EVALUATE |
| `e2e` | testing/E2E exploration | EVALUATE |
| `esp32-c3-adblock` | embedded/network experiment | INDEPENDENT |
| `stremio-web` | fork/external codebase | FORK / INDEPENDENT |
| `grok-build` | build/exploration asset | EVALUATE |
| `caddy` | fork/external infrastructure codebase | FORK / INDEPENDENT |

---

## 9. Portfolio support / identity

### `achirothmane/achirothmane`

**Role:** portfolio front door.  
**Owns:** public profile, portfolio narrative, this System Map.  
**Does not own:** product code or runtime state.

---

## 10. Current graph

Only relationships with enough evidence to be useful are drawn here.

```text
Workflow Failure Lab
        │ PRODUCES failure evidence
        ▼
CI Retry Gate Engine
        │ VALIDATED_BY
        ▼
CI Retry Gate Consumer E2E


EASL
  │ COMPOSES_WITH
  ▼
Assumption Gate


Data Engine
  │
  ├── future CONSUMER candidate ──> Marketing Automation Suite
  ├── future CONSUMER candidate ──> Intelligence Layer
  └── future knowledge/evidence source ──> products that prove a need


Aegis-EGE + governance lineage
  │
  └── ARCHIVES engineering evidence / extract only proven reusable primitives


Games
  └── independent product graph
```

Dashed/future relationships are **candidates, not dependencies**.

---

## 11. Project record contract

Every project promoted into the active graph should eventually have a machine-readable record with:

```yaml
project:
  id:
  repository:
  role:
  status:
  owner_of:
  produces:
  consumes:
  dependencies:
  contracts:
  current_state:
  next_gate:
  blockers:
  evidence:
  distribution:
  economic_role:
  last_verified:
```

A future automation/Dot should prefer these explicit records over inference.

---

## 12. Gates

### Composition Gate

Connect two projects only if at least one is true:

1. a real output of A is consumed by B;
2. B cannot satisfy its contract without A;
3. A materially validates B;
4. the composition removes duplicated infrastructure without destroying independent boundaries;
5. measured operation shows a recurring shared requirement.

Otherwise keep them separate.

### Promotion Gate

A lab/primitive becomes an active portfolio dependency only when:

- a real consumer exists;
- the contract is explicit;
- failure behavior is known;
- evidence exists that reuse is cheaper/safer/better than duplication;
- ownership remains clear.

### Commercial Gate

Do not confuse engineering admiration with business evidence.

Before positioning a capability as a product, require evidence of:

- broad real demand or existing spend;
- economic consequence;
- usable proof;
- distribution path;
- product packaging;
- willingness to adopt/pay.

### Asset Test

Prefer work whose value compounds through:

- reusable code;
- proprietary operational data;
- failure/evidence corpora;
- validated contracts;
- distribution;
- accumulated usage knowledge;
- reputation/trust;
- automation.

---

## 13. Next structural work

1. ✅ Add `portfolio/projects/*.yaml` machine-readable project records.
2. ✅ Add `portfolio/index.yaml` and an agent/Dot read protocol.
3. ✅ Add verified `contracts/` only for relationships that actually exist.
4. ✅ Add a generated dependency graph from project records and verified contracts.
5. Add `LAST_VERIFIED` freshness checks so stale project state is visible.
6. Automatic CI freshness verification for generated graph remains pending; the connected GitHub write surface currently blocks creation of the workflow file.
7. Let future Dot/agents read the map + records before touching repositories.
8. Keep commercial/product status separate from technical status.
9. Never create a dependency merely to make the portfolio look unified.

---

## 14. North-star architecture

The target is **not one giant repository**.

The target is:

> **A portfolio of independently valuable capabilities and products that can compose through explicit contracts, with one trustworthy operating map above them.**

That gives us:

- independent evolution;
- reusable primitives;
- less duplicated context;
- easier long-running work;
- clearer decisions;
- safer automation;
- a clean handoff surface for a future Portfolio Dot.

