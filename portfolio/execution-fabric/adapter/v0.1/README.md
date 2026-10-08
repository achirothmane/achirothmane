# Execution Fabric Adapter v0.1

This adapter is the smallest shared execution layer proven by both Data Engine and PostgreSQL Change Safety.

It deliberately owns **transport and runtime mechanics only**:

```text
consumer checkout
      │
      │ project-local flow + semantic assertions
      ▼
Execution Fabric Adapter
      │
      ├─ download Kestra OSS
      ├─ start isolated local runtime
      ├─ create flow
      ├─ execute flow
      ├─ retrieve task outputs
      ├─ validate minimum execution envelope
      └─ prove checkout stayed clean
      │
      ▼
Kestra OSS Process Runner
```

The adapter does not decide whether data is publishable, whether a PostgreSQL regression is real, or what evidence is sufficient. Those decisions remain inside the owning project.

Consumers may vendor this exact file to avoid creating a hard dependency on the portfolio repository. A hard fork of Kestra remains unjustified until a concrete recurring upstream divergence is proven.
