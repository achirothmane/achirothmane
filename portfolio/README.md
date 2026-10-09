# Portfolio State

This directory is the machine-readable operating state for the portfolio.

Human-facing architecture lives in [SYSTEM-MAP.md](../SYSTEM-MAP.md).  
Machine-facing project state lives in [index.yaml](./index.yaml) and `projects/*.yaml`.

## Agent / Dot read order

1. Read `SYSTEM-MAP.md`.
2. Read `portfolio/index.yaml`.
3. Read `portfolio/evidence-baseline.json` for a public-only, dated audit snapshot. Only default-branch evidence counts as merged; PR work is not main. No deployment, use or revenue may be inferred.
4. Read `portfolio/freshness-report.json`; STALE or UNKNOWN state must be reverified before material use.
5. Read `portfolio/priority-report.json` to determine NOW / NEXT / WATCH / PARKED / REVERIFY / CLOSED.
6. Read `portfolio/execution-queue.yaml`; only READY items with explicit authority are executable.
7. Read `portfolio/dependency-graph.json` for the verified cross-project graph.
8. Read `portfolio/shadow-reference.json` as a PUBLIC-only policy baseline, not a Dots model success score.
9. Read the relevant project records, contracts, priority directives, and execution policy.
10. Follow only declared dependencies and contracts.
11. Treat `UNKNOWN` as unknown. Never fill it from assumption.
12. Remember that FRESH does not mean COMPLETE, ACTIVE does not mean NOW, and NOW does not equal execution authority.
13. Keep technical status separate from commercial status.
14. Escalate portfolio-level conflicts or irreversible choices to human authority.

## Project record fields

Each project record uses:

- `id`
- `repository`
- `role`
- `status`
- `owner_of`
- `produces`
- `consumes`
- `dependencies`
- `contracts`
- `current_state`
- `next_gate`
- `blockers`
- `evidence`
- `distribution`
- `economic_role`
- `last_verified`

## Truth rule

> Unknown is preferable to invented coherence.

A relationship is promoted into the graph only after a real flow of data, capability, evidence, decision, or distribution is demonstrated.


## Dependency graph generation

The human view is `portfolio/DEPENDENCY-GRAPH.md`; the machine view is `portfolio/dependency-graph.json`.

Regenerate both from the YAML sources with:

`python portfolio/scripts/generate_dependency_graph.py`

The generator also rejects a project-level hard dependency unless a registered contract declares the same dependency explicitly.


## Freshness layer

Policy: `portfolio/freshness-policy.yaml`  
Human report: `portfolio/FRESHNESS-REPORT.md`  
Machine report: `portfolio/freshness-report.json`

Regenerate with:

`python portfolio/scripts/generate_freshness_report.py`

Use `--as-of YYYY-MM-DD` to evaluate the portfolio at a specific UTC date.

A state may be FRESH and still INCOMPLETE. Freshness controls whether the record is current enough to use; completeness tracks unresolved `UNKNOWN` values.


## Priority / next-action layer

Policy: `portfolio/priority-policy.yaml`  
Human directives: `portfolio/priority-directives.yaml`  
Human report: `portfolio/PRIORITY-REPORT.md`  
Machine report: `portfolio/priority-report.json`

Regenerate with:

`python portfolio/scripts/generate_priority_report.py`

The priority system is deliberately non-numeric. It uses gates and explicit human directives rather than a hidden score.

**ACTIVE does not imply NOW.** NOW has a WIP cap and requires explicit promotion or strong economic evidence.


## Execution / Dot handoff layer

Execution policy: `portfolio/execution-policy.yaml`  
Admitted work queue: `portfolio/execution-queue.yaml`  
Dot operating contract: `portfolio/DOT-OPERATING-CONTRACT.md`  
Handoff manifest: `portfolio/dot-handoff.yaml`

The key invariant is:

> **Priority does not equal execution authority.**

A work item must be READY and carry explicit authority plus evidence and stop conditions before a Dot may execute it.

Current execution state (operational check 2026-10-09):

- one bounded OBSERVE-only public-context task is READY, under 2026-10-09 human authority;
- `data-engine-capability-boundaries-001` is DONE / PASS (scoped);
- Data Engine PR #7 has already merged into main; the legacy queue entry now waits for post-merge evidence, **not** a second merge decision.
- Dots requires updated generated priority/freshness reports before executing consequential work.


## Public evidence baseline (9 October 2026)

Source: `portfolio/evidence-baseline.json` (curated **public repositories only**); displayed as a generated table in `SYSTEM-MAP.md`.

Validate and check that the human map matches JSON:

`python portfolio/scripts/check_evidence_baseline.py`

Refresh only the marked public table after explicitly re-verifying GitHub evidence:

`python portfolio/scripts/check_evidence_baseline.py --write`

To reject a snapshot older than seven UTC days:

`python portfolio/scripts/check_evidence_baseline.py --fail-on-stale`

This is an **offline audit snapshot**, not a live GitHub poll, CI rerun, sales ledger, production deployment proof, or evidence for private repositories. The verifier rejects new nonpublic repositories and unsupported paid/deployed claims. Existing private-repository references in historical public files should not be supplemented with further confidential metadata. Operational records must be rechecked against current GitHub state before consequential actions.

The freshness and dependency reports predate the new project records and must be regenerated before treating their project counts or freshness statuses as current. Regeneration should not imply independent technical or commercial proof.


## Dots shadow-management policy oracle

See [SHADOW-MANAGEMENT.md](./SHADOW-MANAGEMENT.md) and the dated [shadow reference](./shadow-reference.json). The read-only oracle compares proposed decisions with snapshot-bound explicit policy and redacts proposals outside the approved public scope. The reference is deterministic, not an AI model, and the live Dots decision-quality score remains **NOT_MEASURED**.

`python portfolio/scripts/shadow_management.py --as-of 2026-10-09 --check-reference`

`python -m unittest discover -s portfolio/tests -p 'test_shadow_*.py' -v`

The historical note above about reports predating the October 9 update is superseded: the six reports were regenerated and verified in PR #2. Recency and completeness must still be checked before any material decision.


## S1 live decision provenance preflight

See [S1-LIVE-DECISION-CONTRACT.md](./S1-LIVE-DECISION-CONTRACT.md) and the current [S1 readiness](./s1-readiness.json).

`python portfolio/scripts/shadow_live_gate.py --as-of 2026-10-09 --check-reference`

Current state: **one genuine OBSERVE-only task admitted for public evidence review**, but zero actual model-generated Dots decisions and zero paid provider calls. Runtime D4/D5 have merged, with mock-provider integration verified. S1 still cannot authenticate paid provider evidence from an ordinary file and does not authorize provider costs.

## Dots D2 context export

See [REAL-DOTS-CONTEXT.md](./REAL-DOTS-CONTEXT.md). Run `python portfolio/scripts/export_dots_context.py --output /tmp/real-dots-context.json` to prepare the source-bound read-only D2 context. This is a local snapshot step, not a model call or operational execution.
