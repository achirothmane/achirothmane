# Portfolio State

This directory is the machine-readable operating state for the portfolio.

Human-facing architecture lives in [SYSTEM-MAP.md](../SYSTEM-MAP.md).  
Machine-facing project state lives in [index.yaml](./index.yaml) and `projects/*.yaml`.

## Agent / Dot read order

1. Read `SYSTEM-MAP.md`.
2. Read `portfolio/index.yaml`.
3. Read `portfolio/freshness-report.json`; STALE or UNKNOWN state must be reverified before material use.
4. Read `portfolio/priority-report.json` to determine NOW / NEXT / WATCH / PARKED / REVERIFY / CLOSED.
5. Read `portfolio/dependency-graph.json` for the verified cross-project graph.
6. Read the relevant project records, contracts, and priority directives.
7. Follow only declared dependencies and contracts.
8. Treat `UNKNOWN` as unknown. Never fill it from assumption.
9. Remember that FRESH does not mean COMPLETE and ACTIVE does not mean NOW.
10. Keep technical status separate from commercial status.
11. Escalate portfolio-level conflicts or irreversible choices to human authority.

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
