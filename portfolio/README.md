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
8. Read the relevant project records, contracts, priority directives, and execution policy.
9. Follow only declared dependencies and contracts.
10. Treat `UNKNOWN` as unknown. Never fill it from assumption.
11. Remember that FRESH does not mean COMPLETE, ACTIVE does not mean NOW, and NOW does not equal execution authority.
12. Keep technical status separate from commercial status.
13. Escalate portfolio-level conflicts or irreversible choices to human authority.

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

Current execution state:

- no READY work item;
- `data-engine-capability-boundaries-001` is DONE / PASS;
- verified draft PR #8 is waiting for human merge authority.


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
