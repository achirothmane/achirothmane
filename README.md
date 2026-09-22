<div align="center">

<img src="./assets/evidence-gated-systems.svg" alt="Othmane Achir — Evidence-Gated Systems" width="100%" />

<br/>

### Verification & control infrastructure for AI, automation, and high-consequence software

I build systems that decide **when there is enough evidence to act — and when the correct answer is UNKNOWN.**

[![CI Retry Gate](https://img.shields.io/badge/CI_Retry_Gate-evidence--gated-238636?style=for-the-badge)](https://github.com/achirothmane/workflow-failure-lab)
[![Agent Action Guard](https://img.shields.io/badge/Agent_Action_Guard-control_plane-1f6feb?style=for-the-badge)](https://github.com/achirothmane/agent-action-guard)
[![PostgreSQL Change Safety](https://img.shields.io/badge/PostgreSQL_Change_Safety-causal_verification-6f42c1?style=for-the-badge)](https://github.com/achirothmane/postgres-change-safety)

</div>

---

## Selected systems

<table>
<tr>
<td width="50%" valign="top">

### [CI Retry Gate](https://github.com/achirothmane/workflow-failure-lab)

**Do not retry a failed CI job just because it failed.**

Uses provenance, causal evidence, side-effect checks, retry limits, and explicit authority before granting a rerun.

`failure → evidence → decision → retry / block`

</td>
<td width="50%" valign="top">

### [Consequence Boundary Completeness](https://github.com/achirothmane/agent-action-guard)

**Find paths that bypass an AI agent's intended approval boundary.**

Models routes from agent capabilities to real consequences and reports certain bypasses, covered paths, or unresolved evidence.

`agent → path analysis → boundary → allow / counterexample / unknown`

</td>
</tr>

<tr>
<td width="50%" valign="top">

### [PostgreSQL Change Safety](https://github.com/achirothmane/postgres-change-safety)

**Do not blame a PostgreSQL change for a regression without causal evidence.**

Compares workload windows, fingerprints SQL across versions, runs controlled experiments, analyzes plan variants, and preserves `UNKNOWN` when confounders remain.

`before/after → regression → causal isolation → evidence strength`

</td>
<td width="50%" valign="top">

### [Legal Authority Diff](https://github.com/achirothmane/legal-authority-diff)

**A citation is not enough; the supporting authority can regress.**

Differential testing for legal-AI citations, authority strength, treatment, and proposition support, while separating model regression from world change.

`baseline → candidate → authority diff → block / unchanged / world change`

</td>
</tr>

<tr>
<td colspan="2" valign="top">

### [Private Code Modernization Factory](https://github.com/achirothmane/private-code-modernization-factory)

**Do not let a plausible patch become an authorized modernization.**

Strengthens repository evidence, constrains patch proposals, performs differential verification, and escalates when deterministic automation is not justified.

`repository → evidence → proposal → verification → human / automation`

</td>
</tr>
</table>

---

## The engineering thesis

A recurring failure pattern appears across AI agents, CI systems, databases, legal AI, and software automation:

> **Plausibility is not authority. A system should act only when the evidence required for that action has actually been established.**

The architecture I keep returning to is:

```text
Input / Event / Proposed Action
              │
              ▼
      Evidence Collection
              │
              ▼
         Verification
        ┌─────┴─────┐
        │           │
   sufficient   insufficient
        │           │
        ▼           ▼
Authority/Policy   UNKNOWN
        │        BLOCK / ESCALATE
        ▼
    Decision Gate
     ┌───┼───┐
     ▼   ▼   ▼
   ALLOW BLOCK HUMAN
        │
        ▼
     Execution
        │
        ▼
 Outcome Verification
        │
        ▼
   Audit / Replay
```

---

## Design rules I care about

<table>
<tr>
<td width="33%" valign="top"><b>Explicit uncertainty</b><br/><br/><code>UNKNOWN</code> is a valid engineering outcome. It is safer than inventing certainty from weak evidence.</td>
<td width="33%" valign="top"><b>Fail closed</b><br/><br/>High-consequence actions do not silently inherit permission when evidence is incomplete.</td>
<td width="33%" valign="top"><b>Read-only first</b><br/><br/>Observe and prove value before enabling mutation, reruns, quarantine, merge, deploy, or other write authority.</td>
</tr>
<tr>
<td width="33%" valign="top"><b>Differential verification</b><br/><br/>Prefer controlled before/after evidence over plausible explanations.</td>
<td width="33%" valign="top"><b>Causal isolation</b><br/><br/>When attribution matters, test competing explanations instead of treating correlation as cause.</td>
<td width="33%" valign="top"><b>Audit & replay</b><br/><br/>Important decisions should retain enough evidence to inspect and reproduce how authority was granted.</td>
</tr>
</table>

---

## Technical focus

<div align="center">

![Python](https://img.shields.io/badge/Python-0D1117?style=flat-square&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-0D1117?style=flat-square&logo=githubactions&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-0D1117?style=flat-square&logo=postgresql&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-0D1117?style=flat-square)
![AI Agents](https://img.shields.io/badge/AI_Agents-0D1117?style=flat-square)
![LLM Evaluation](https://img.shields.io/badge/LLM_Evaluation-0D1117?style=flat-square)
![Verification](https://img.shields.io/badge/Verification-0D1117?style=flat-square)
![Developer Infrastructure](https://img.shields.io/badge/Developer_Infrastructure-0D1117?style=flat-square)

</div>

---

<div align="center">

### Evidence before action.

**Build → test → falsify → strengthen the evidence → automate only what has earned authority.**

<sub>Independent tools first. Shared platform only when repeated real-world usage proves the same primitives belong together.</sub>

</div>
