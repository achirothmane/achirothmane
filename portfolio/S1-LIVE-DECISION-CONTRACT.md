# Dots S1 — Live decision evidence ingress (no autonomous execution)

**Operational result at 2026-10-09:** `BLOCKED_NO_READY_WORK`. Dots has no admitted READY work item, the D4 and D5 runtime pull requests are not merged to `main`, and **no paid OpenAI provider call is authorized**. These are legitimate blockers, not reasons to create an artificial READY task.

## Two different SHA-256 domains

- `portfolio_source_digest`: SHA-256 over an exact ordered set of Portfolio source **bytes** as specified in `portfolio/scripts/shadow_management.py`. Its matching baseline is `shadow-reference.json`.
- `runtime_snapshot_digest`: the **different** SHA-256 on the Go D2 sealed Portfolio Context JSON, validated by `portfoliocontext.Parse` and used in D3/D4/D5.

These two digests are deliberately never assumed equal. A real bridge must bind both to verifiable source-identities and the *same eligible work item*; a claimed string in a file is not cryptographic provenance.

## Why S1 remains blocked today

The actual D5 adapter on `governed-agent-runtime` draft PR #29 explicitly rejects a `ReasoningView` with no runnable items. The D3 validator also requires an admitted work item in the snapshot, and D4 durable commitment belongs to its separate unmerged draft PR #28. The central queue and handoff currently declare zero runnable items. The correct action is **no call**, not a synthetic work item injected into our real queue.

## S1 bridge

`python portfolio/scripts/shadow_live_gate.py --as-of 2026-10-09 --check-reference`

Outputs a safe, public-only machine-readable preflight in `portfolio/s1-readiness.json`, with no project-by-project private information or model/provider metadata.

Optional offline trace review:

`python portfolio/scripts/shadow_live_gate.py --trace /local/private/path/dots-trace.json`

The trace must contain the exact schema fields `origin`, `portfolio_source_digest`, `runtime_snapshot_digest`, `provider_kind`, `decision` (D3 structured decision), and `provider_receipt`. A trace claiming `paid_call=true` is not independent proof; even if the JSON is perfectly formed the maximum state is `PENDING_INDEPENDENT_ORIGIN_ATTESTATION`, never VERIFIED.

No untrusted trace, private source binding, model rationale, credential, paid receipt or private project name may be committed into this public portfolio repository.

## Gates to enter real live S1

1. Inspect and separately validate the stacked runtime PRs (#25, #28, #29) against the current `main` code; finish any required integration tests and explicitly decide whether to merge them. There is **no automatic merge** from this contract.
2. Admit **one genuine, bounded, read-only objective**, with verifiable NOW lane, freshness, evidence and stop conditions, only with explicit human priority authorization. Never manufacture runnable work merely to make a demo pass.
3. Produce the D2 sealed context, confirm the same source binding in the central Portfolio preflight, and test the D3/D4 path with a non-paid/local reasoner.
4. After separately authorizing any provider costs, run at most the human-approved provider smoke with `ALLOW_PAID_MODEL_TEST=1`; retain receipts privately, bind them to the actual provider run and source commits. Never publish credentials or private context.
5. Obtain an **independent** audit of provider and durable decision provenance (not merely the self-reported trace file), then compare actual candidate decisions with the S0 policy oracle and prospectively human-labeled outcomes.

Until those gates pass, `actual_dots_trace_count=0`, `decision_quality=NOT_MEASURED`, `runtime_validated=false` and `live_model_authorized=false`. This is S1 **preflight infrastructure**, not an S1 live-model PASS.

## Falsification

`python -m unittest discover -s portfolio/tests -p 'test_shadow*.py' -v`

Synthetic fixtures demonstrate that false READY work, NEXT-to-NOW promotion, forged live-provider JSON, execution requests, authority escalation, stale evidence and mismatched digests do **not** become authenticated live Dots decisions.
