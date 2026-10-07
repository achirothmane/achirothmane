# Kestra -> Data Engine bounded spike

**Status:** PASS_BOUNDED_SPIKE.

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

The gate passed in GitHub Actions run `37583709577`.

Verified evidence:

- normal Data Engine test job: `success`;
- Kestra spike job: `success`;
- Kestra execution: `2UkqKuYaKbeZuU7YdKC4p0`;
- `orchestration_state=KNOWN_SUCCESS`;
- Data Engine exit code: `0`;
- `data_publishable=true`;
- entities: `3`, coverage: `1.0`, conflicts: `0`, unknown cells: `0`;
- evidence authority: `data-engine`;
- orchestrator evidence mutation: `false`;
- GitHub Actions evidence artifact: `11465352137`.

Artifact SHA-256:

- `dataset.csv`: `24417a0ce98888e93a2ff425fab88848fa9f29de76eb0e2837ec0a39aec9b9fa`
- `provenance.jsonl`: `fc968acdf74fa2c632966a8dab7a84b460a1eabcac098226c81cfeb8c96a95db`
- `quality.json`: `08d8ac2cbf22580a3be33878b2e3c8df0d464b89ae7282e7caf0f6fffc556b35`
- `result.json`: `32c5f58426f9f9da5042b9c05c2fa085eb44057ef9978375cfab2a4dc8efb412`

The spike also exposed three operational facts that are now part of the harness: Kestra
2.0.5 uses JDK 25 in this standalone path, local API calls are authenticated, and task
outputs are read from the Kestra 2.0 task-output API rather than assumed to be inline
inside the synchronous execution response.

## Hard-fork gate

PASS proves that Kestra is a viable Execution Fabric upstream; it does **not** prove
that we should own a fork.

A hard fork still requires:

1. a second distinct real portfolio workflow;
2. repeated internal usefulness;
3. measurable reduction in manual/project-specific glue;
4. a concrete architectural divergence;
5. evidence that maintaining the divergence is cheaper than staying upstream-compatible.

Until those conditions are met, Kestra remains a proven upstream candidate rather than
a new owned repository.
