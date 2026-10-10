<div align="center">

<img src="./assets/ai-native-futuristic.svg" width="100%" alt="AI-Native Engineering — systems, evidence, and reliability" />

### Independent software & systems builder

**Data systems · distributed execution · workflow reliability · AI-native engineering**

[LinkedIn](https://www.linkedin.com/in/othmane-achir-2733a540b/) · [System map](./SYSTEM-MAP.md) · [Public evidence baseline](./portfolio/evidence-baseline.json)

</div>

---

I build software systems and investigate how they behave under failure, concurrency, and incomplete information. This profile is a curated engineering record: **implemented capabilities, reproducible evidence where available, and explicit limits**. It does not equate a passing CI run with production deployment, third-party adoption, or commercial success.

## Selected systems

### [Marketing OS](https://github.com/achirothmane/marketing-os) — event-driven marketing infrastructure

A Mautic-based system exploring durable event processing, identity and consent, and operational recovery.

- **Implemented/tested scope:** Mautic 7.2.1 source integration with MariaDB-backed, bounded source-to-queue-to-inbox execution; explicit crash/replay cases documented in [integration CI](https://github.com/achirothmane/marketing-os/actions/runs/38049177697) and [project status](https://github.com/achirothmane/marketing-os/blob/main/docs/marketing-os/project-status.json).
- **Boundary:** these tests do not establish a deployed production service, authorized marketing sends, or external customer use.

### [ReleaseGuard for n8n](https://github.com/achirothmane/releaseguard-n8n) — measured workflow rollout and rollback

Canary routing and release decisions for a **bounded class of synchronous, read-only JSON workflows**, with explicit evidence for PROMOTE, HOLD, and ROLLBACK.

- **Implemented/tested scope:** HTTP and PostgreSQL integration, concurrency and lost-observation scenarios, and n8n webhook compatibility; see the [executed-validation record](https://github.com/achirothmane/releaseguard-n8n/blob/main/docs/validation.md).
- **Boundary:** no claim of universal production safety, long-running high-availability operation, or paid adoption.

### [Data Engine](https://github.com/achirothmane/data-engine) — source-aware data acquisition and provenance

A Go-based data system that plans source selection against cost, freshness and rights constraints, retains acquired evidence, and produces datasets with lineage and quality information.

- **Implemented/documented scope:** `discover` and `auto` command paths, acquisition manifests, provenance outputs and a read-only `data.profile` capability over MCP; see [implementation and usage](https://github.com/achirothmane/data-engine/blob/main/README.md).
- **Boundary:** these are repository-documented capabilities, not an independent certification of correctness or a claim of autonomous open-web discovery.

### [AI-Native Agent Runtime](https://github.com/achirothmane/governed-agent-runtime) — durable agents and tool execution

A runtime exploring Temporal-backed execution, persisted runs and events, MCP capability binding, and bounded tool invocation.

- **Implementation record:** [runtime README and capability history](https://github.com/achirothmane/governed-agent-runtime/blob/main/README.md).
- **Boundary:** the architecture and component work should not be presented as proof of an autonomously operating production company or a commercially validated agent platform.

## Engineering disciplines

**Languages and systems:** Go · Python · TypeScript · Rust · SQL · PostgreSQL · Linux · distributed workflows.

**Methods:** explicit contracts, integration and failure-path testing, provenance, state machines, concurrency reasoning, and formal-methods study (including TLA+).

I distinguish four claims: **documented design**, **implemented code**, **reproduced test evidence**, and **deployed/used system**. None automatically establishes the next. Competitive differentiation and commercial adoption require separate external evidence.

## Additional work

The broader portfolio includes CI reliability experiments, PostgreSQL change analysis, software modernization, game development, and research prototypes. They are deliberately not presented here as equally mature products.

Browse the [system map](./SYSTEM-MAP.md) for the wider project index and the [evidence baseline](./portfolio/evidence-baseline.json) for a dated public-only snapshot.

---

<sub>Independent engineering work. Scope and verification claims are intentionally narrower than long-term product ambitions.</sub>
