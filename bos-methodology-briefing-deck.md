# Business Observability — Methodology, Framework, Factory

**Briefing for the CT Platform Observability Pillar**
**Audience:** PE peers, lead engineers, Director (sponsor)
**Duration:** 30–45 min + Q&A
**Form:** Slides stand alone as takeaway

---

## BLUF

Observability is one capability across a lifecycle of five stages — Define, Implement, Enforce, Observe, Respond — and the pillar owns the full chain. Business Observability (BOS) is the named discipline for the **Define** stage: it captures business context as a structured Service Profile (four PO questions → five templates → one system of record per service) and feeds that profile into a factory that produces five operational artifact types automatically — stories, dashboards, alerts, playbooks, documentation. ULMS dashboards are the **Observe**-stage surface where the Dashboard Factory's output renders. The pillar's work across the lifecycle is structurally one integrated capability, not separate efforts being aligned.

---

## SLIDE 1 — TITLE

# Business Observability
### Methodology, Framework, and Factory

How the CT Platform Observability Pillar operationalizes observability as one integrated capability across the lifecycle

*Presented to the PE Observability Pillar · [DATE]*

---

## SLIDE 2 — BLUF

# What this pillar operationalizes

**Observability is one capability across a lifecycle. The pillar owns the full chain.**

- **Business Observability (BOS)** is the named discipline for the **Define** stage — capturing business context as a structured system of record
- **The framework** is the structured artifact — one Service Profile per service, contributed by three roles (PO, Developer, Platform/SRE)
- **The factory** is the production mechanism — 1 structured input produces 5+ operational artifacts (stories, dashboards, alerts, playbooks, documentation) automatically
- **The pillar's work at upstream stages flows through the factory** to every downstream stage — including Observe, where ULMS dashboards render

*The rest of the deck walks the methodology, the Credit Check example end-to-end, and the factory operating across the lifecycle.*

---

## SLIDE 3 — THE SPINE: THE OBSERVABILITY LIFECYCLE

# Observability is five stages, not one activity

| Stage | Question it answers | Primary owner |
|---|---|---|
| **Define** | What does "healthy" mean in business terms? | Product Owner |
| **Implement** | How do we instrument the signals? | Developer |
| **Enforce** | How do we ensure standards are followed? | Platform / Engineering |
| **Observe** | What views make health visible? | Platform / SRE |
| **Respond** | When something fails, what do we do? | SRE / Ops |

**Each stage has a distinct question, a distinct owner, and distinct output.** None of them is "observability" on its own.

> **VISUAL:** Left-to-right strip — `Define → Implement → Enforce → Observe → Respond` — with owner labels below each stage.

---

## SLIDE 4 — THE DEPENDENCY CHAIN IS STRUCTURAL

# You can't skip stages

- **You can't Observe what you haven't Instrumented.**
- **You can't Instrument what you haven't Defined.**
- **You can't Enforce standards that haven't been Defined.**

Non-linear in practice, but the dependency direction is real.

**Most enterprise observability investment lives at Observe.** The upstream stages — especially **Define** — are largely empty.

This is the structural cause behind recurring questions about standards, consistency, and business context showing up in dashboards.

> **VISUAL:** Same lifecycle strip from Slide 3, with the three dependency constraints shown as back-pointing arrows — Observe depends on Implement, Implement depends on Define, Enforce depends on Define. "Investment concentrates here" overlay at Observe; "structural gap" overlay at Define.

---

## SLIDE 5 — WHERE THE PILLAR'S WORK LIVES TODAY

# One capability, the pillar owns the chain

| Stage | Work in flight |
|---|---|
| **Define** | BOS methodology, framework, system of record, factory inputs |
| **Implement** | [INSERT: pillar-specific instrumentation standards work] |
| **Enforce** | [INSERT: pillar-specific enforcement mechanisms, NFR gates] |
| **Observe** | ULMS dashboards, BOS factory dashboard blueprints, platform rendering surfaces |
| **Respond** | [INSERT: pillar-specific incident response / playbook standards] |

**BOS at Define and ULMS at Observe are stages of the same pipeline.** The factory is the mechanism that makes Define output flow through to Observe (and to every other downstream stage) consistently.

No competitive axis exists. The pillar owns both ends and what connects them.

---

## SLIDE 6 — THE CORE PREMISE

# BOS makes implicit requirements explicit

Product Owners write functional requirements for their services.

**Business health requirements — what "healthy" means, what the thresholds are, who's impacted when it degrades — are implicit in that work.**

Business Observability is the discipline of making those implicit requirements **explicit** — structured, measurable, traceable.

**This is not new work.** The knowledge already exists — in POs' heads, Jira tickets, design conversations, incident postmortems. BOS structures it so it can be measured, monitored, and acted on at scale.

---

## SLIDE 7 — THE FOUR-LAYER MODEL

# Every signal answers one question at one layer

| Layer | Name | Question | Who has it today |
|---|---|---|---|
| **1** | System | Is it up? | Traditional monitoring |
| **2** | Process | Is it correct? | Traditional monitoring |
| **3** | **Business Health** | **Is the expectation being met?** | **BOS adds this** |
| **4** | **Business Impact** | **How bad when we fail?** | **BOS adds this** |

**Layers 1–2 are standard observability. Layers 3–4 are what BOS adds.**

A service can be green at Layers 1–2 while failing at Layer 3 — the **"Green But Failing"** pattern.

**Concrete anchor — Credit Check service (Home Lending):**
- **L1:** Bureau Connection Health = 95% (target ≥ 95%) ✓
- **L2:** Credit Check Response Time < 5 seconds ✓
- **L3:** Credit Check Success Rate = 89% (target ≥ 85%) ✓
- **L4:** Customers Blocked = 127, Loan Revenue at Risk = [$X], FCRA Timing Violations = Y

---

## SLIDE 8 — WHY ALL FOUR LAYERS MATTER

# Mechanism health ≠ outcome success

**The dangerous state:** Layers 1 and 2 green (system up, process correct), Layer 3 red (business outcome not achieved). Traditional monitoring reports "everything is fine" while customers cannot complete their transaction.

**Layer 4 says "so what?"** — quantifying the consequence when Layer 3 misses. Not every Layer 3 miss is equal. A Credit Check success rate drop at 2am affecting 30 customers is materially different from a 2pm drop affecting 2,000 customers and $500K of loan revenue.

**Cross-layer combinations are the real decision surface.** A Layer 3 miss combined with a Layer 4 severity is what triggers meaningful action — not a Layer 1 threshold alone.

---

## SLIDE 9 — SEMANTIC FLOW

# The traceable chain from business intent to action

```
[Stakeholder] → [Expectation] → [KPI target + formula]
                                       │
                                       ▼
                         [Business Health Signal (L3)]
                         supported by [L2 Process + L1 System]
                                       │ if deviation
                                       ▼
                         [Business Impact Signal (L4): category + magnitude]
                                       │
                                       ▼
                              [Alert] → [Owner + Next Action]
```

- A **stakeholder** has an **expectation** about a service
- The expectation becomes a **KPI target with formula** — the measurable definition of "healthy"
- **L3 signals** measure whether the expectation is met, **supported by** L2 and L1
- **L4 signals** fire only when L3 deviates — quantifying consequence
- Alerts carry full context to the **owner** with a defined **next action**

**If a metric cannot trace back through this chain to a stakeholder expectation, it is noise — not signal.**

---

## SLIDE 10 — THE SERVICE PROFILE FRAMEWORK

# Four PO questions → five templates → one system of record

The PO answers **four questions** (the conceptual interface):

1. **What does the service do?**
2. **Who depends on it?**
3. **What does "working" look like?** (business health definitions)
4. **What happens when it fails?** (impact quantification)

These answers become **five structured templates:**

| Template | Contents |
|---|---|
| **Services** | Identity, owner, tier, business domain, technical owner |
| **SLI Definitions** | Signals per layer (L1/L2/L3/L4), what each tells us, formulas |
| **SLO Configurations** | Targets, thresholds, alert/page levels |
| **Impact Assessments** | L4 signals — customer, financial, compliance, operational |
| **Operational Metadata** | Dashboards, runbooks, alert routing, on-call |

**Together these are the Service Profile — the system of record for a service's business context.**

---

## SLIDE 11 — THREE PERSONAS

# Three roles contribute; no role owns the whole profile

| Persona | Contributes | Lifecycle stage |
|---|---|---|
| **Product Owner** | Business context, stakeholders, expectations, impact definitions | **Define** |
| **Developer** | Signal implementations, instrumentation, data sources | **Implement** |
| **Platform / SRE** | Alerts, dashboards, playbooks, operational config | **Observe + Respond** |

**No single role owns the whole profile.**
- The PO can't define instrumentation without the Developer
- The Developer can't choose what to measure without the PO's business health definitions
- Platform/SRE can't build meaningful operational surfaces without either

**The pillar's co-leading structure mirrors this** — different PE leads and lead engineers plug in at different lifecycle stages.

---

## SLIDE 12 — CONCRETE ANCHOR: CREDIT CHECK END-TO-END

# What a Service Profile looks like (excerpt)

**Service:** Credit Check Service — Home Lending

**Stakeholders and expectations:**

| Stakeholder | Expectation | Impact category | Priority |
|---|---|---|---|
| Loan Applicants | Credit checks return valid scores within acceptable timeframe | Customer Experience | HIGH |
| Home Lending | Credit checks complete successfully without failures | Financial | HIGH |
| Regulatory Body | Credit checks meet FCRA 30-day timing requirements | Legal / Risk | HIGH |
| Loan Processors | Credit checks complete without manual intervention | Operational | MEDIUM |

**Signals across all four layers:**
- **L1:** Bureau Connection Health (≥ 95%)
- **L2:** Credit Check Response Time (< 5 seconds)
- **L3:** Credit Check Success Rate (≥ 85%), Credit Score Retrieval %, Valid Score Return Rate
- **L4:** Customers Blocked, Loan Revenue at Risk, FCRA Timing Violations, Manual Interventions Required

**That's the structured input. Now watch what it produces.**

---

## SLIDE 13 — THE FACTORY MULTIPLIER

# 1 structured input → 5+ operational artifacts

The Service Profile is not the output. **It's the input to five parallel production lines.**

```
                        Service Profile
                       (structured input)
                              │
          ┌────────┬──────────┼──────────┬────────┐
          ▼        ▼          ▼          ▼        ▼
      Story    Dashboard    Alert    Playbook   Documentation
      Factory   Factory    Factory   Factory    Factory
          │        │          │          │        │
      Jira     Grafana    Monitoring  Incident  Service catalog
      stories   / ULMS     rules +    response  entries +
      with BDD  blueprints  escalation  docs     ownership
      ACs      (layered)    paths
```

**Design targets** (scaling projection, not observed outcome):
- 1 PO action → **5+** automated artifact types per service
- **10+** team hours saved per service vs. hand-crafting equivalents
- At the pillar's 100+ service target: **1000+** hours saved annually
- Consistency: every service gets the same artifact types at the same quality

---

## SLIDE 14 — THE FIVE FACTORIES

# Each factory produces a specific operational artifact

| Factory | Consumes | Produces | Consumer |
|---|---|---|---|
| **Story** | Service profile | Jira user stories with BDD acceptance criteria | Development teams |
| **Dashboard** | Service profile | Grafana / ULMS dashboard blueprints (layered L1–L4) | SRE, operations, business |
| **Alert** | Service profile | Monitoring rules + escalation paths + owner routing | On-call, incident response |
| **Playbook** | Service profile | Incident response documentation keyed to signal failures | SRE during incidents |
| **Documentation** | Service profile | Service catalog entries + ownership records | Enterprise search, onboarding |

**Each factory is a defined transformation.** Same input, different output, governed separately. A Dashboard Factory change doesn't affect the Alert Factory's output.

**Factories are independent production lines. The Service Profile is the shared upstream contract.**

---

## SLIDE 15 — FACTORY INTEGRATES WITH THE LIFECYCLE

# One Define-stage effort → consistent output at every downstream stage

```
DEFINE                            IMPLEMENT   ENFORCE   OBSERVE          RESPOND
   │                                  │          │         │                │
Service Profile                       │          │         │                │
(structured)                          │          │         │                │
   │                                  │          │         │                │
   ├── Story Factory ───────────────▶ │          │         │                │
   │                              feeds dev      │         │                │
   │                              backlog        │         │                │
   │                                             │         │                │
   ├── Documentation Factory ─────────────────▶ │         │                │
   │                                          standards    │                │
   │                                          reference    │                │
   │                                                       │                │
   ├── Dashboard Factory ─────────────────────────────▶   │                │
   │                                                    ULMS + platform     │
   │                                                    surfaces render     │
   │                                                    these               │
   │                                                                        │
   ├── Alert Factory ──────────────────────────────────────────────────▶   │
   │                                                                      on-call
   │                                                                      routing
   │                                                                        │
   └── Playbook Factory ───────────────────────────────────────────────▶   │
                                                                       response
                                                                       docs
```

**The factory is the leverage.** One structured Define-stage artifact produces correct, consistent output at every downstream stage — no per-stage recreation.

---

## SLIDE 16 — ULMS IS OBSERVE-STAGE OUTPUT

# Dashboard Factory consumers — the artisanal path vs. the factory path

**The artisanal path (where most enterprise dashboarding lives today):**
Platform team hand-crafts a dashboard per service. Business context lives in the dashboard creator's head. Quality varies by who built it. Scales to ~50 services before visual consistency and content fidelity degrade.

**The factory path:**
Dashboard Factory consumes the Service Profile. Produces a Grafana / ULMS blueprint with business context baked in — layered panels (L1/L2/L3/L4), stakeholder-labeled, impact-quantified, consistent across every service.

**The pillar's commitment:** make the Dashboard Factory produce ULMS-quality output from the Service Profile, automatically, for every onboarded service.

**This is integration.** ULMS is not separate from BOS. ULMS is the **Observe-stage surface** where Dashboard Factory output renders. The pillar owns the factory and the surface.

---

## SLIDE 17 — PILLAR OKRs BY LIFECYCLE STAGE

# What the pillar commits to, mapped to where it lives

*[User to fill exact OKR statements — structural slots below show where each OKR lands on the lifecycle.]*

| Lifecycle Stage | Pillar OKR(s) operationalized here |
|---|---|
| **Define** | [INSERT: e.g., "N services onboarded with structured Service Profiles by EOY"] |
| **Implement** | [INSERT: e.g., "signal instrumentation standards adopted in M repos"] |
| **Enforce** | [INSERT: e.g., "NFR gate on Service Profile completeness before production"] |
| **Observe** | [INSERT: e.g., "P services with factory-rendered ULMS dashboards in production"] |
| **Respond** | [INSERT: e.g., "factory-produced playbooks covering Q incident classes"] |

**If** the pillar owns the integrated capability, **then** the OKRs must span the lifecycle — not concentrate at any single stage.

**The factory is the compounding lever.** Upstream OKRs at Define produce downstream artifacts at scale without additional per-stage effort.

---

## SLIDE 18 — WHAT CO-LEADING LOOKS LIKE

# Where pillar members plug in

The lifecycle is the map. Different PEs and lead engineers co-lead different stretches.

**Co-lead territories across the lifecycle:**

| Territory | Stage | Substance |
|---|---|---|
| Define methodology | Define | Framework, vocabulary, "what counts as a service" discipline |
| Service onboarding | Define | IC enablement, JPA, reference examples, extraction quality feedback |
| Factory pipelines | Define → downstream | Five production lines, schema governance, integration contracts |
| Dashboard rendering | Observe | ULMS integration, templatization, layered dashboard design |
| Instrumentation standards | Implement | Developer contracts, signal library, data source conventions |
| Enforcement mechanisms | Enforce | NFR gates, fitness functions, drift detection |
| Response tooling | Respond | Playbook generation, incident response integration |

**The weekly pillar meeting is where cross-stage decisions happen.** Co-leading means showing up with substance on at least one territory.

---

## SLIDE 19 — KEY POINTS RECAPPED

# What you're leaving with

- **The lifecycle is the pillar's territory.** Observability is one capability across five stages — Define, Implement, Enforce, Observe, Respond.
- **BOS is the named discipline for Define.** The Four-Layer Model names what to measure; the Semantic Flow makes every signal traceable to a stakeholder expectation.
- **The framework is the Service Profile** — four PO questions → five structured templates → one system of record per service.
- **The factory is the production mechanism.** One structured input produces five+ operational artifacts — stories, dashboards, alerts, playbooks, documentation — automatically.
- **ULMS is the Observe-stage surface.** The Dashboard Factory produces blueprints; ULMS and platform tools render them. Same pipeline, different stages.
- **The pillar owns the chain.** OKRs span the lifecycle. Co-leading means owning a stretch of it.

**The work now:** operationalize the factory across stages, scale service onboarding, make each stage's output consistently factory-produced rather than artisanal.

---

## SLIDE 20 — OPEN QUESTIONS FOR DISCUSSION

# Discussion prompts

1. **Co-lead territories.** Which stretch of the lifecycle do you see yourself owning?
2. **Current vulnerability.** Where is our pillar work most at risk — Define scale, factory output quality, or enforcement coverage?
3. **Cadence.** What's the right rhythm between service onboarding iterations and factory iteration?
4. **PO engagement.** How do we surface Define-stage work that needs PO involvement beyond the pillar?
5. **Sponsor touchpoints.** What belongs on the sponsor-brief queue vs. staying inside the pillar?

**For deeper reference (after this session):**
- Credit Check service profile walkthrough — end-to-end example with extraction output, rendered Confluence page, review flow
- Onboarding pipeline system map — how the factory operates M0→M5 inside WF Copilot today, with gap markers for what's deployed vs. designed-not-built

---

## Self-Evaluation Scorecard

**Type:** Information Brief (per FM 6-0) — methodology substance shared at the pillar's working altitude, standalone slides, no decision requested.

**Frame:** Integration (observability lifecycle as spine); NOT convergence. Per memory `feedback_bos-ulms-integration-frame.md`.

| # | Criterion | Pass/Fail | Evidence |
|---|---|---|---|
| 1 | BLUF | **Pass** | Slide 2 is the full BLUF; each major section opens with a one-line lede |
| 2 | Consumer-oriented | **Pass** | Structured around audience walk-away capability (co-lead-capable methodology depth for peers; integrated-capability mental model for Director) |
| 3 | Fact-judgment separation | **Pass** | Credit Check signals are facts (from reference example); factory multiplier numbers flagged as "design targets, scaling projection, not observed outcome" on Slide 13 |
| 4 | Uncertainty expressed | **Pass** | Factory multiplier tagged as design targets. Slide 5 and 17 use `[INSERT: ...]` slots for pillar-specific content Claude cannot author. Slide 20 labels open questions as genuine discussion prompts. |
| 5 | Alternatives considered | **Partial** | Implicit: the "artisanal path vs. factory path" on Slide 16 and "investment at Observe" critique on Slide 4 name the alternatives BOS addresses. Not an explicit alternatives-considered treatment — acceptable for an information brief; explicit comparison belongs in a decision brief. |
| 6 | Assumptions stated | **Pass** | Slide 13 states factory projections assume structured input; Slide 11 states no role owns the profile alone; Slide 17 states OKR cascade assumes pillar owns the integrated capability. |
| 7 | Risks and failure modes | **Pass** | "Green But Failing" (Slide 8) is the core failure mode BOS addresses. Slide 4 names the failure mode of investment concentrated at Observe. Slide 16 names the artisanal-path scale wall. |
| 8 | Actionable with clear ask | **Pass** | Slide 18 names co-lead territories. Slide 20 carries five discussion prompts. Teaching decks don't have decision asks — the lift is discussion and co-lead identification. |
| 9 | Logical structure | **Pass** | Lifecycle (spine) → methodology → framework → factory → integration → OKRs → co-leading → close. Dependency order preserved; recap restates BLUF. |
| 10 | Prioritized | **Pass** | BLUF first; lifecycle (highest level of abstraction) before methodology (the discipline) before framework (the artifact) before factory (the mechanism). Pillar-specific content (OKRs, co-leading) after the shared foundation. |

**Type-specific checks (Information Brief):**
- ✓ Facts organized for awareness (methodology substance at working altitude)
- ✓ Implications made explicit (integration framing, pillar OKR cascade, co-leading)
- ✓ No hidden recommendation — informational register held throughout

**Voice governance checks:**
- ✓ Validate audience's problem first (investment concentrated at Observe — Slide 4)
- ✓ Enabling language, not automatic (Slide 13 factory projections use "produces" deliberately — factory output IS automatic once input exists; not overclaiming)
- ✓ Outside-in framing (lifecycle before methodology; audience's territory before discipline name)
- ✓ No framework name-dropping in slide body ("ICD 203", "Minto", "FM 6-0" absent from deck content)

**Ask-quality anti-patterns avoided:**
- ✓ No competitive axis with ULMS — integration framing holds throughout
- ✓ No "acknowledge their work then introduce ours" scaffolding — per saved memory
- ✓ No methodology-internals-as-deliverable — Four-Layer Model and Semantic Flow taught for application, not as internal reference

**Gaps surfaced for user to close:**
- `[INSERT: ...]` slots on Slides 5 and 17 — pillar-specific work-in-flight and OKR statements
- Slide 12 — if a different concrete service would land better with this audience than Credit Check, substitute. Credit Check is chosen because the reference example is complete and end-to-end documentable.
- Target date / slot — not yet named; affects how recent the "work in flight" content needs to be
- Speaker notes not produced — slides stand alone per user constraint; add rehearsal prompts per slide if helpful before delivery

**Prep substrate consulted (per committee warning "prep, not content"):**
- `copilot-capability-transfer/starter-kit/.github/skills/bos/SKILL.md` — methodology text
- `copilot-capability-transfer/reference-example-credit-check.md` — Credit Check end-to-end
- `documentation/systems-analyses/bos-onboarding-wf-copilot/analysis.md` — factory-at-work system map
- `_threads/committee-2026-04-15-pe-observability-pillar-onboarding.md` — three rounds of prior framing (round 1–2 broader pillar audience)
- `documentation/systems-analyses/2026-04-09-bos-factory-vs-ulms-sourced-analysis.md` — ULMS integration grounding (NOT reproduced in deck)

---

**Length:** 20 slides. At ~1.5–2 min per slide at working pace, covers 30–40 minutes of content; 5–10 minutes Q&A on Slide 20 prompts lands at the 35–45 minute target.

**Next steps:**
1. User fills `[INSERT: ...]` slots (Slides 5, 17)
2. User confirms Credit Check as the concrete anchor or substitutes
3. Decide on speaker notes — deck stands alone as a takeaway; speaker-notes would be rehearsal prompts only
4. Convert markdown to deck format (Google Slides / PowerPoint / Keynote) — each `##` slide maps to one slide; tables preserve as tables; diagram specs in `> **VISUAL:**` blocks need rendering
