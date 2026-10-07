# Kestra -> Data Engine bounded spike

**Status:** READY_TO_RUN — not PASS.

This spike tests whether Kestra OSS can act as a neutral execution fabric around the
converged Data Engine without becoming a semantic authority or a product dependency.

## Pinned facts

- Data Engine `main` converged via PR #7 on 2026-10-07.
- Converged main merge commit: `154b92d4c464a2e0a8646ba1709d16f7ecba7c76`.
- Candidate orchestrator: Kestra OSS.
- Intended local runner: open-source Process Task Runner.
- No Enterprise-only capability is part of this spike.

## Contract

Kestra may:

1. start the Data Engine process;
2. observe process exit;
3. persist logs and emitted artifacts;
4. hash observed artifacts;
5. report execution state.

Kestra may **not**:

- rewrite pinned evidence;
- reinterpret field decisions;
- turn `publishable=false` into success;
- resolve `UNKNOWN` or `CONFLICTING`;
- become a second truth store.

The execution record intentionally contains two separate ideas:

- `orchestration_state`: whether the process outcome and required artifacts are known.
- `data_publishable`: Data Engine's own quality decision.

A run can therefore be `KNOWN_SUCCESS` at the orchestration layer while
`data_publishable=false`. That is valid and must not be collapsed.

## Run

Start Kestra OSS with a Process-capable environment and import `flow.yml`.

Provide `data_engine_root` as the absolute path to an existing checkout of
`achirothmane/data-engine` on the converged `main` commit.

The flow executes the existing real H200 fixture:

`go run ./cmd/dataengine auto`

and captures:

- `result.json`
- `quality.json`
- `provenance.jsonl`
- `dataset.csv`
- source plan
- acquisition manifest
- stdout/stderr
- `execution-record.json`

## PASS gate

This spike becomes PASS only when a real Kestra execution shows:

- Data Engine process exit is observed;
- all four required semantic artifacts are present;
- hashes are recorded;
- `data_publishable` exactly matches Data Engine's quality artifact;
- the input checkout remains unchanged except for no repository-owned files;
- no Enterprise feature is required.

Until that evidence exists, the state remains READY_TO_RUN.

## Hard-fork gate

Even after PASS, Kestra is **not** forked automatically. A hard fork requires repeated
internal use plus a concrete architectural divergence that is cheaper to own than to
maintain as external glue.
