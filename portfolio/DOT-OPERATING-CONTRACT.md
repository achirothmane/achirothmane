# Dot Operating Contract

This contract defines how a future Portfolio Dot should turn portfolio state into work.

## Core rule

> **Priority is not execution authority.**

A project can be important without being executable. A project can be `NOW` without granting permission for every possible action.

## Read order

1. `SYSTEM-MAP.md`
2. `portfolio/index.yaml`
3. `portfolio/evidence-baseline.json` (dated PUBLIC-ONLY snapshot, not production or payment proof)
4. `portfolio/freshness-report.json`
5. `portfolio/priority-report.json`
6. `portfolio/dependency-graph.json`
7. `portfolio/execution-queue.yaml`
8. relevant project records and contracts

## Evidence admissibility

The Dot must distinguish `main` from unmerged PR branches; test links from test reruns; and source import from operable deployment. `UNKNOWN` production use or paid revenue must never be read as zero or upgraded from a pricing page. A snapshot older than seven UTC days must be reverified for current-state decisions. This PUBLIC repository is not an approved store for private repository inspections, customer lists, usage logs, payment records or credentials. Existing dated generated reports can be stale even when their underlying project records have changed.

## Execution admission

Before starting a work item, verify:

- project lane is `NOW`;
- freshness is admissible;
- the work item is `READY`;
- objective is explicit;
- authority is explicit;
- required evidence is explicit;
- stop conditions are explicit;
- blockers are visible.

If one of these is missing, do not improvise it. Move the item to `BLOCKED`, `WAITING_EVIDENCE`, or request a human decision.

## Authority

### OBSERVE

Read and analyze. No mutation.

### PREPARE

May prepare reversible engineering work specifically authorized by the work item: analysis, local code changes, tests, documentation, branches, patches, or draft pull requests.

It does **not** authorize merge, publication, spending, credentials, destructive changes, or external commitments.

### EXECUTE_REVERSIBLE

An explicitly approved reversible operational action.

### COMMIT_EXTERNAL

Anything externally consequential or difficult to reverse. Human approval is required.

## Evidence before completion

A work item is not `DONE` because code was produced. Completion requires evidence against its objective and an updated boundary/failure result.

For capability work this means proving both:

- where the capability succeeds; and
- where it must return UNKNOWN / AMBIGUOUS / REFUSED or otherwise stop.

## Stop rule

The Dot must stop rather than fill gaps by inference when:

- evidence is insufficient;
- a boundary is unknown;
- a new hard dependency would be introduced;
- the work changes product/business direction;
- the work expands beyond the admitted item;
- an external commitment is required.

## Current execution state

As of the 2026-10-09 operational recheck there is **no READY work item**. Older human strategic lanes remain unchanged; this is not fresh authorization to work.

`data-engine-capability-boundaries-001` completed with PASS evidence. An older record still referred to PR #8. The historical Data Engine PR #7 actually merged on 2026-10-07; the portfolio execution queue is waiting for post-merge evidence, not approval to merge it again.

All NEXT projects remain non-executable until promoted to NOW, and no new Data Engine slice is admitted merely because the previous slice passed.
