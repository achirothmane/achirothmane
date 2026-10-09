# Dots S1 — Live decision evidence ingress (no autonomous execution)

**Operational result at 2026-10-09:** `READY_FOR_SEPARATE_RUNTIME_ATTESTATION` is the *preflight* result only. The owner authorized precisely one real public GitHub readiness-evidence observation with `OBSERVE` authority. D4 and D5 are now merged in Runtime main and their Temporal/PostgreSQL mock-provider integration passes. **No paid OpenAI provider call is authorized; no actual model-generated Dot decision has been independently authenticated.**

## Two different SHA-256 domains

- `portfolio_source_digest`: SHA-256 over an exact ordered set of Portfolio source **bytes** as specified in `portfolio/scripts/shadow_management.py`. Its matching baseline is `shadow-reference.json`.
- `runtime_snapshot_digest`: the **different** SHA-256 on the Go D2 sealed Portfolio Context JSON, validated by `portfoliocontext.Parse` and used in D3/D4/D5.

These two digests are deliberately never assumed equal. A real bridge must bind both to verifiable source-identities and the *same eligible work item*; a claimed string in a file is not cryptographic provenance.

## Why S1 live-model measurement remains blocked today

D5 and D4 are now merged into Runtime main. The central queue has one owner-authorized `OBSERVE` task, `dots-runtime-evidence-observe-006`, to propose an evidence-request next gate from the sealed public Portfolio projection. Dots has no live GitHub read tool inside D5; a human must independently inspect current PR and CI evidence. D5 cannot be used with a paid model without separate cost approval. The current preflight is not the D2 sealed context, and it is not a production decision.

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

Until those gates pass, `actual_dots_trace_count=0`, `decision_quality=NOT_MEASURED`, `runtime_validated=false` and `live_model_authorized=false`. Admission of the OBSERVE task permits analysis only, not tool execution, API spend or a claim of S1 live-model PASS.

## Falsification

`python -m unittest discover -s portfolio/tests -p 'test_shadow*.py' -v`

Synthetic fixtures demonstrate that false READY work, NEXT-to-NOW promotion, forged live-provider JSON, execution requests, authority escalation, stale evidence and mismatched digests do **not** become authenticated live Dots decisions.
