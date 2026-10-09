# First real Portfolio D2 context — scoped, non-paid S1

This is an **actual source-backed sealed Portfolio context**, not a synthetic READY work item. The only admitted task is `dots-runtime-evidence-observe-006`, granted `OBSERVE` by the 2026-10-09 central human decision.

Run offline:

```sh
python -m pip install -r portfolio/requirements.txt
python -m unittest discover -s portfolio/tests -p test_export_dots_context.py -v
python portfolio/scripts/export_dots_context.py --as-of 2026-10-09 --output /tmp/real-dots-public-context.json
```

The emitted JSON follows the **Go `portfoliocontext.Parse` D2 schema**, including the canonical JSON SHA-256 digest and source-file identity/digests. Source paths refer only to files in the public portfolio; the `ReasoningView` projection is restricted to public audited project IDs, strips non-public graph nodes, excludes raw repository and other project records, and includes exactly one OBSERVE work item. Only an ephemeral file outside the public repository may store the raw context.

`state=EXECUTABLE` is an existing D2 schema term: **eligible for a typed D3 decision**, NOT permission to execute tools/effects, send messages, merge, or spend. If the queue ceases to be exactly one approved OBSERVE task, if sources expire, if the reference digest changes, or if private projects would appear in the projection, the exporter exits without creating an executable context.

The complete evidence chain must be measured separately:

1. **Real Portfolio sources -> ephemeral Go D2 snapshot:** this exporter and its unit tests, audited for source binding.
2. **Go D2 Parse -> D3 Validate -> D4 Temporal and PostgreSQL -> inert committed record:** a dedicated runtime integration test is required and must use the exact checked-out Portfolio commit, not a hand-constructed fixture.
3. **Independent GitHub and human ground-truth comparison:** validate whether the resulting one read-only next-gate proposal is defensible. The local deterministic reasoner tests durable plumbing, **not** intelligent reasoning.
4. **D5 live reasoning:** a separate consented, potentially paid provider run. Not permitted by this test and not measured.

Policy oracle S0 and S1 trace validator remain separate from the Go D2 digest. None of these files are a proof of paid provider output, business adoption, or autonomous management.
