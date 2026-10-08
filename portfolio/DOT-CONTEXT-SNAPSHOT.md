# Portfolio Context Snapshot v0.1

Status: **candidate until CI proof passes**

Dots must not reason directly over arbitrary repository files.

Before selecting or executing a work item, the Portfolio repo builds one deterministic snapshot from explicit machine-readable sources.

## Source boundary

The snapshot binds SHA-256 for:

- `SYSTEM-MAP.md`;
- `portfolio/index.yaml`;
- freshness, priority, dependency, execution-policy, execution-queue, and handoff state;
- the Dot operating contract;
- every project record registered in the index;
- every verified contract registered in the index.

The source files remain the authority. The snapshot is only a compact, digest-bound projection.

## Projection

v0.1 exposes only what Dots needs for admission:

- structural review date;
- NOW projects;
- freshness/completeness for NOW projects;
- READY runnable items with objective, authority, evidence gate, and stop conditions;
- verified contract edges;
- human-final authority actions;
- WIP counts and execution principle.

It does not copy full project descriptions, evidence corpora, or arbitrary repository content.

## Executability

The snapshot is `EXECUTABLE` only when all admission sources agree.

It becomes `NON_EXECUTABLE` when freshness / priority / dependency dates disagree, a NOW project has stale or UNKNOWN freshness, a hard dependency has a freshness risk, runnable count disagrees with READY items, a READY project is not NOW, required admission fields are missing, human-final authority is absent, or WIP caps are exceeded.

A missing required source raises a hard error and produces no usable snapshot.

## Determinism

The snapshot contains no wall-clock generation timestamp.

Its digest is SHA-256 over canonical JSON containing the compact projection, fail-closed state/reasons, and source paths with SHA-256 bindings.

Therefore: same sources -> same digest; any bound source change -> different digest.

## Dots boundary

A later Dots reasoning activity may consume this snapshot as one admitted context object.

It must not reopen arbitrary files to fill gaps, infer undeclared dependencies, silently promote projects, execute when state is `NON_EXECUTABLE`, treat priority as execution authority, or bypass human-final actions.

D2 proves the context boundary. It does not yet add a model-provider reasoner.
