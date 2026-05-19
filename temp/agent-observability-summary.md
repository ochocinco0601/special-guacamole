# AI Agent Observability: Arize AI & ServiceNow AI Control Tower

> **May 2026** | Full technical detail: [agent-observability-technical-briefing.md](agent-observability-technical-briefing.md)

---

## The Problem

AI agents call multiple tools across multiple systems and make judgment calls between input and output. Current observability logs what went in and what came out — not what the agent *did* in between. Two products address this at different altitudes.

---

## Arize AI — Agent Execution Observability

Traces every LLM call, tool invocation, and agent-to-agent interaction as OpenTelemetry spans. Open source component (Phoenix, Elastic License 2.0) and enterprise SaaS (AX — SOC 2, PCI DSS 4.0, HIPAA).

| Capability | Detail |
|------------|--------|
| **Workflow visualization** | Interactive flowcharts of multi-agent orchestration (Agent Graph & Path, June 2025) |
| **MCP tracing** | Stitches traces across MCP client-server boundaries (April 2025). Both sides must be instrumented. |
| **Output evaluation** | LLM-as-judge: hallucination, relevance, drift detection, toxicity |
| **Cost tracking** | Per-span, per-model, across 60+ providers |

**Does not do:** Governance, kill switch, CMDB/service catalog, incident management, cross-domain APM correlation, business process context. Observes only — cannot intervene.

**Practical note:** Agent Graph and MCP tracing are relatively recent features. Enterprises deploying Arize through a wrapper platform may have basic logging enabled but not these capabilities — worth checking before pursuing new procurement.

---

## ServiceNow AI Control Tower — Agent Fleet Governance

Centralized governance anchored to the CMDB. Expanded at Knowledge 2026 (May 5) with Traceloop (LLM tracing, $60-80M acquisition) and Veza (identity/permission mapping, 30B+ permissions). GA August 2026 — Innovation Lab today.

| Capability | Detail |
|------------|--------|
| **Discover** | Agent inventory via 30 connectors (AWS, GCP, Azure, SAP, Oracle, Workday). Agents registered as CMDB configuration items. |
| **Observe** | Runtime tracing via Traceloop (OpenLLMetry — open source, Apache 2.0, auto-instruments 30+ LLM frameworks). Same OTel foundation as Arize. |
| **Govern** | Risk frameworks aligned to NIST and EU AI Act. Fairness audits, regulatory mapping. |
| **Secure** | Kill switch — revokes agent permissions across all connected systems via Veza. Auto-generates P1 incident with blast radius and audit trail. Can be automated or human-approved. |
| **Measure** | Token consumption and cost attribution across providers. ROI methodology still maturing. |

**Kill switch limitation:** Works on supported platforms (ServiceNow + 30 connectors). Agents on unsupported runtimes or custom containers are not covered.

**Entitlement distinction:** Included in all ServiceNow AI tiers for **ServiceNow-native** workflows. Governing agents on **external platforms** (AWS, Azure, GCP, internal LLM platforms) requires an additional enterprise-wide purchase.

---

## Side by Side

| | Arize | AI Control Tower |
|---|---|---|
| **Core question** | "Did this agent produce reliable output?" | "Are agents operating within policy?" |
| **Target user** | Engineers | CIO / CISO / IT governance |
| **Traces execution** | Deep, span-level | Yes, via Traceloop (same OTel) |
| **Evaluates quality** | LLM-as-judge, drift detection | Quality evaluators, drift alerts |
| **Agent inventory** | No | CMDB-anchored, 30 connectors |
| **Can stop an agent** | No | Kill switch + blast radius |
| **Incident management** | PagerDuty alerts | Native ServiceNow P1 with audit trail |
| **Open source** | Phoenix (ELv2) | OpenLLMetry (Apache 2.0) |
| **Status** | Production | GA August 2026 |

**Complementary, not competing.** Arize goes deep on individual agent behavior. AI Control Tower goes wide on fleet governance. Both use OTel for tracing.

---

## What Neither Does

Neither answers: **"Is the business process this agent serves actually working?"** Both trace the agent. Neither traces through to business results. Complete agent observability requires agent tracing + agent governance + traditional APM + business process monitoring + a correlation layer. No single product does this today.

---

## ITSM AI Agents — Related

ServiceNow's ITSM team is separately building AI agents for incident and change management:

- **Incident investigation** — 5 skills: change correlation (with confidence scoring), KB lookup, similar incidents, reassignment, catalog items. Natural language interaction.
- **Change quality** — evaluates implementation plans and backup instructions.

These don't solve the observability gap but directly address incident response — fewer people on the call, faster resolution. Shipping this year.

---

## References

- [Knowledge 2026 Day 1 Keynote](https://www.youtube.com/watch?v=jeo2V1w-Peg) — kill switch demo
- [Knowledge 2026 Day 2 Keynote](https://www.youtube.com/watch?v=q8kaVEkTWho) — product depth
- [AI Control Tower Demo](https://www.youtube.com/watch?v=ss9eUlaM8So) — standalone walkthrough
- [AI Control Tower Demo Playlist](https://www.youtube.com/playlist?list=PLrveurE10abZnNPEc9V5k-lZTTHHELEBz)
- [OpenInference Spec](https://arize-ai.github.io/openinference/spec/semantic_conventions.html)
- [OpenLLMetry](https://github.com/traceloop/openllmetry)
- [Gemini deep research](https://gemini.google.com/app/6c0a183537a8065b)
