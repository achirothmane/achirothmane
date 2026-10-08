# Dot Operating Contract

This contract defines how a future Portfolio Dot should turn portfolio state into work.

## Core rule

> **Priority is not execution authority.**

A project can be important without being executable. A project can be `NOW` without granting permission for every possible action.

## Read order

1. `SYSTEM-MAP.md`
2. `portfolio/index.yaml`
3. `portfolio/freshness-report.json`
4. `portfolio/priority-report.json`
5. `portfolio/dependency-graph.json`
6. `portfolio/execution-queue.yaml`
7. relevant project records and contracts

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

As of 2026-10-08 the Portfolio Dot is in **active build**.

`dots-data-reconcile-001` completed with PASS evidence across Data Engine + governed-agent-runtime:

- Data Engine PR #21;
- governed-agent-runtime PR #25;
- Data Engine CI run `37732132716` PASS;
- real reconciliation run `37732132706` PASS;
- governed-agent-runtime CI run `37732121431` PASS;
- cross-repository Dots runtime run `37732132719` PASS;
- `TestDotsDurablyInvokesDataReconcile` PASS.

The current READY item is `dots-portfolio-context-snapshot-002`.

Its purpose is to bind the portfolio's machine-readable state into one immutable, digest-bound context snapshot before Dots performs next-action reasoning. No merge, publication, spend, destructive action, new hard dependency, or business-positioning change is authorized by that READY state.
