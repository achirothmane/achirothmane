# Fast Hard-Fork Product Base — Source-backed selection

**Date:** 2026-10-10
**Decision type:** technical acceleration / self-use-first foundation; **NOT a commercial launch, approved expenditure, new runnable Dot mission, or proof of paid demand**.
**Selection:** [dgtlmoon/changedetection.io](https://github.com/dgtlmoon/changedetection.io) at upstream release **0.60.8 (2026-09-28)**, Apache-2.0.
**Proposed independent downstream name:** `market-signal-engine`, only if/when an actual fork exists. This proposal does not create a GitHub fork.

## Why this one, after independent comparison

The instruction was to **reuse a substantial, current working product** rather than produce a slow stack of new primitives. Prioritization factors: working UI, maintained code, built-in collection/notifications, API contracts, permissive license, use by a sole operator, and compatibility with our broad research/data/marketing portfolio.

| Candidate | First-party evidence as checked 2026-10-10 | Barrier to immediate reuse | Decision |
| --- | --- | --- | --- |
| [changedetection.io](https://github.com/dgtlmoon/changedetection.io) | Apache-2.0, GitHub release `0.60.8` dated 2026-09-28, active code 2026-10-09; Docker/Python deployment, full watch management/UI, conditional CSS/XPath/JSONPath/jq extraction, notification history and REST API | Running service and optional browser infrastructure; paid hosted/proprietary features must **not** be assumed in fork | **SELECT technical foundation**, commercial `NEEDS_EVIDENCE` |
| [DataRecce/recce](https://github.com/DataRecce/recce) | Apache-2.0, `v1.68.0` dated 2026-10-07, data diff/lineage + complete UI | dbt-first; more specific than our broad web-source intelligence use; competes with its original paid cloud | Excellent alternative when a real dbt-first buyer appears |
| [docling-project/docling](https://github.com/docling-project/docling) | MIT, `v2.137.0` dated 2026-10-09, substantial document extraction engine | library/pipeline, not the finished buyer-facing product; local heavy extraction/runtime concerns | Prefer upstream library ingestion into Data Engine if an actual document use case arises |
| [erezsh/reladiff](https://github.com/erezsh/reladiff) | Cross-database comparison engine; latest release `v0.6.0` 2025-03-04 and last GitHub code push recorded 2025-08-18 | older maintenance signal; not a complete commercial UX | Not preferred for fastest CURRENT product fork |
| [datafold/data-diff](https://github.com/datafold/data-diff) | MIT, but original source archived 2024-05-17 | upstream development stopped | Reject as contemporary foundation |

**Why not automatically pick the biggest repository?** Source popularity and code size do not establish user demand or a defensible business. Docling's engine is impressive but it requires additional UX/output/product distribution; Recce requires a dbt context. changedetection has an operational UI and notifications already.

## Broad owned-use product concept (NOT yet a commercial differentiation claim)

`Market Signal Engine`: watch permitted public supplier, product, licensing, pricing, documentation and market pages that matter to *our own decisions*. Create a growing, source-linked history of material changes rather than manually rechecking websites. This serves Portfolio research, content research, price/vendor observation and buyer discovery without imposing an early market niche.

**Existing upstream features we must NOT rebuild:**
- page fetch, browser-backed dynamic page support, UI for watches, snapshots and diff history;
- filters / selectors for HTML and JSON responses;
- schedules, alerting integrations, webhook/API, and backup/installation paths;
- core documentation and test harness.

**Potential proprietary value to validate, not promise:** join upstream change events to existing Data Engine's evidence/profile/conflict capabilities; compare contradictory changes across independent sources; produce dated claims with a `KNOWN / UNKNOWN / CONFLICTING` status plus immutable evidence references. Competitors already offer AI summaries, API integrations, page diffs, important-change classification, and pricing monitoring. We are **not** distinct for adding “AI”, email alerts, or a dashboard.

**No automatic cross-repository dependency:** prove a watch/event evidence contract and a real consumer before adding Data Engine/Marketing OS/Dots as mandatory services.

## Competitive Freshness Gate — explicit commercial boundary

- **Current paid alternatives/spend:** [Visualping prices](https://visualping.io/pricing) show active monthly subscriptions, including a free tier and $14 monthly Personal 1K. The [changedetection.io upstream](https://github.com/dgtlmoon/changedetection.io) itself advertises a hosted $8.99/month offer. Existing paid spend proves a category, **not demand for our derivative**.
- **Strong baseline rivals:** changedetection.io upstream, Visualping, Distill, price-monitoring / competitive-intelligence vendors. Some already have AI intent filters and summaries.
- **Commodity overlap:** alerting, AI summarization, webhook integrations and generic page diffing **already exist**; fork of these alone is **not a commercial product**.
- **Potential distinction:** independent multi-source factual conflict custody and auditable verified change *decisions* with lower false-action rate; this is a hypothesis until compared empirically to existing upstream and competitors.
- **Buyer willingness to pay for incremental difference:** `UNKNOWN`.
- **Accessible free distribution and feasible support economics:** `UNKNOWN`.
- **Commercial disposition:** `NEEDS_EVIDENCE`; do not open a store, advertise or assert recurring sales merely from the fork. See [Competitive Freshness Gate](../COMPETITIVE-FRESHNESS-GATE.md).

## Fork path: shortest implementation (no proprietary feature copying)

1. User opens **https://github.com/dgtlmoon/changedetection.io/fork** and selects owner `achirothmane`. Desired repo `market-signal-engine`. This is required because the installed GitHub connector offers no `create_fork`; neither a generated README nor an imported source snapshot is a true GitHub fork with ancestry.
2. Fork the full upstream history (not default-branch-only if preserving lineage is desired), use default `master` unless explicitly changed, preserve Apache-2.0 `LICENSE`, third-party notices, attribution, upstream remote and commit history. Record exact upstream source commit/tag `0.60.8` in a fork-specific README *after the fork exists*.
3. Verify **the unmodified fork first** with upstream test workflow and Docker/Python smoke startup on supported CI or owned machine, keeping artifact logs and the exact SHA. No marketing rebrand before this baseline.
4. Prove single-watch HTML and JSON/API change monitoring and a real notification with synthetic self-owned/authorized fixtures. Falsify noise/duplicate/timeout/blocked/consent conditions. Track CPU/RAM/runtime, hosting and browser costs.
5. Only after baseline PASS, add one tiny independently tested `change -> provenance evidence envelope` export **with no new infrastructure**, keeping upstream monitoring intact; verify Data Engine consumes it if and only if there is a real user.
6. Do not launch a hosted service or incur spend. A paid subscription/service requires supported deployment, security review, acceptable acquisition costs, source/site rights, support model, independently established paid buyer advantage and separate human approval.

## Explicit runtime/financial constraints

The owner currently has an Android tablet, limited/no startup cash and no verified continuously available server. GitHub Actions can smoke-test or exercise fixtures within plan quotas, but is **not** a guaranteed free always-on hosting service. Browser rendering, proxies and 24/7 monitoring may incur nonzero costs. The original upstream's managed service and hosted-only features are not included just because the public repo is forked.

This technical selection is **not** an automatic NOW/READY priority change or authorization for Dots to execute, publish, purchase, email prospects, collect customer data, or run background services.

## Evidence and promotion

- **Technical PASS:** actual fork lineage, license audit, reproducible upstream baseline, bounded monitored event and measured resource cost.
- **Commercial PASS only after:** independently observed buyer pain relative to already-paid alternatives, willingness to pay for verifiable incremental outcome, zero-upfront channel and concrete costed delivery. Otherwise `COMMERCIAL_HOLD`.
- **Stop rule:** if the upstream already offers the full proposed differentiation, or support/hosting obligations exceed attainable revenue, retain for self-use only rather than pretending to build a new SaaS.

## Direct sources

- Upstream [GitHub](https://github.com/dgtlmoon/changedetection.io), [REST OpenAPI spec](https://github.com/dgtlmoon/changedetection.io/blob/master/docs/api-spec.yaml), and [license](https://github.com/dgtlmoon/changedetection.io/blob/master/LICENSE).
- [Recce releases](https://github.com/DataRecce/recce/releases), [Docling releases](https://github.com/docling-project/docling/releases), [Reladiff releases](https://github.com/erezsh/reladiff/releases).
- [Datafold open-source sunset announcement](https://www.datafold.com/blog/sunsetting-open-source-data-diff/).
- [Visualping pricing](https://visualping.io/pricing).

