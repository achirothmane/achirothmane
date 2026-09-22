<div align="center">

# Othmane Achir

### Evidence-Gated Systems

**Verification & control infrastructure for AI, automation, and high-consequence software.**

**Evidence before action.**

`OBSERVE → VERIFY → AUTHORIZE → ACT`  
`INSUFFICIENT EVIDENCE → UNKNOWN / BLOCK / ESCALATE`

</div>

---

## What I build

I build developer infrastructure for a recurring failure mode:

> **A system should not act just because a signal looks plausible. It should act only when the evidence is strong enough to authorize the next step.**

Across CI, AI agents, databases, legal AI, and software modernization, the design pattern stays the same:

```text
Input / event / proposed action
             │
             ▼
      Evidence collection
             │
             ▼
        Verification
        ┌────┴────┐
        │         │
   sufficient   insufficient
        │         │
        ▼         ▼
 Authority /    UNKNOWN
    policy      BLOCK / ESCALATE
        │
        ▼
   Decision gate
   ┌────┼────┐
   ▼    ▼    ▼
 ALLOW BLOCK HUMAN
        │
        ▼
    Execution
        │
        ▼
 Outcome verification
        │
        ▼
   Audit / replay
```

---

## Selected systems

| Project | What it gates |
|---|---|
| **[CI Retry Gate](https://github.com/othy19904-eng/workflow-failure-lab)** | Prevents blind CI reruns. Uses provenance, causal evidence, side-effect checks, retry limits, and explicit authority before a failed job is retried. |
| **[Consequence Boundary Completeness](https://github.com/othy19904-eng/agent-action-guard)** | Looks for modeled paths that let an AI agent reach a real consequence while bypassing the approval or policy boundary that was supposed to control it. |
| **[PostgreSQL Change Safety](https://github.com/othy19904-eng/postgres-change-safety)** | Detects workload regressions after PostgreSQL changes and requires repeated causal evidence before attributing a slowdown to a specific factor. |
| **[Legal Authority Diff](https://github.com/othy19904-eng/legal-authority-diff)** | Differential regression testing for legal-AI authority, citations, and claim support — with `UNKNOWN` and `WORLD_CHANGE` kept separate from model regressions. |
| **[Private Code Modernization Factory](https://github.com/othy19904-eng/private-code-modernization-factory)** | Evidence-first modernization: strengthen repository evidence, constrain patch proposals, verify before/after behavior, and escalate when automation is not justified. |

---

## Engineering principles

- **Explicit uncertainty** — `UNKNOWN` is a valid engineering outcome, not a failure to hide.
- **Fail closed on high-consequence actions** — insufficient evidence should not silently become permission.
- **Differential and causal verification** — prefer before/after evidence and controlled experiments over plausible explanations.
- **Read-only first** — observe and prove value before enabling mutation, reruns, quarantine, merge, deploy, or other write authority.
- **Auditable decisions** — important actions should carry the evidence and reasoning needed to inspect or replay the decision later.

---

## Current technical focus

`Python` · `GitHub Actions` · `CI/CD` · `PostgreSQL` · `AI Agents` · `LLM Evaluation` · `Automation` · `Verification` · `Developer Infrastructure`

I am turning this portfolio thesis into independently useful tools rather than one large platform. Shared infrastructure only earns the right to exist when multiple real projects prove they need the same evidence, policy, decision-gate, provenance, and replay primitives.

---

<div align="center">

### Evidence before action.

**Build → test → falsify → strengthen the evidence → automate only what has earned authority.**

</div>
