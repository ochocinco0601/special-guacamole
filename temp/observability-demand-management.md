# Observability Demand Management

The practice of taking incoming observability demand — requests that almost always arrive as solutions ("build me X") — and converting it into well-formed work: name the kind of request, recover what the requestor actually needs, check whether it's answerable yet, and decide what to do. This is **Demand Management** (ITIL 4) at the front of the observability practice, doing two established moves in sequence: recover the need behind the asked-for solution (Jobs to Be Done; requirements elicitation), then classify and route it.

The work is the same whatever the domain; observability is the worked instance here. Nothing in the method is observability-specific — a second-domain example shows the same walk on a product backlog. Treat the observability content as one instantiation, not the method.

This is a current baseline, not fixed doctrine. It's meant to be run the same way by every co-owner; where two of us disposition the same item differently, that disagreement is the signal that sharpens it.

This document has two parts. **Part 1 — the practice** is the walk you run on each request (the human surface). **Part 2 — the reference** is the *Observability Question Taxonomy*, the map you reason against when you place a request. Part 1 is what you do; Part 2 is what you consult.

---

# Part 1 — The practice

## What's actually going on

**Most requests name a solution, not the need.** "Build me X" means "I can't find out or do something." The build is their best guess; the need underneath is what matters — and the same holds for a request to fix or tune something.
> *In observability:* "build me a dashboard" = "I can't find out something I need to know."

**One request usually hides several needs.** What looks like one item is often three bundled together, each a different piece of work with a different answer. Treat them as one and you build a single thing that does three jobs poorly, or pick one and miss the rest.
> *In observability:* an SLO (service-level objective) repository request can be three needs — do we have SLOs, are we meeting them, can leadership see the picture across services.

**Some needs aren't answerable yet — and the reason usually isn't missing tooling.** Something has to exist first: a definition, a registry, a map, a documented practice. That prerequisite is the real first step; the build comes after.
> *In observability:* you can't report on SLOs nobody has defined, or map a blast radius nobody has mapped. The definition or the dependency map comes first.

**Surface signals can mislead — absence of symptoms isn't proof the outcome is right.** A request that doesn't look like yours can still be yours; check the real outcome, not the surface. Treat "not ours" as a conclusion that needs evidence, not a first reaction to unfamiliar wording.
> *In observability:* everything can be green — APIs returning 200, servers up, no alerts — while the wrong customers have access or the wrong transactions process. When a request doesn't look like observability, ask whether anyone would know if the system produced the wrong result.

**Repeated demand is a signal.** Several people asking for the same thing means either the answer exists but isn't findable, or it's a common need nobody has solved. Either way, check before building.

---

## Step 1 — What kind of request is it?

Name this first; it decides everything after. Most demand is one of these:

- **Build an artifact** — the common case. Treat the build as a guess and look for the need it's really trying to serve.
- **Fix or tune what exists** ("retune these alerts," "tighten these thresholds") — still has a need inside it: how would we know it's actually working?
- **Build a capability** — a generator that turns out artifacts on its own, not a single artifact. A much bigger decision; don't triage it like one item.
- **Carry out a mandate** — the decision is already made upstream. The work is breaking it into items, not reopening it.
- **A well-formed need** — the requestor did the thinking. You're ahead; go straight to whether it's answerable.
- **Out of scope** — it's about how the intake or the team runs, not about the thing you're here to serve. Different queue.

Across all kinds: when a request is worded as a fix, or doesn't look like it belongs to you, assume there's a real need in it until you've looked.

---

## Step 2 — Recover the need(s)

With the kind in hand, work these for anything that hides a need. There's usually more than one — recover the set, not a single answer.

1. **What do they need to find out or do?** This is the core move. Don't accept the named thing — ask what they'd *do* with it, or what goes wrong without it, and keep laddering. **You've reached the need when you can name two things: the decision it informs, and the uncertainty it resolves.** If you can't name a decision the answer would change, you haven't laddered far enough — or there's no real need under the request (a dashboard nobody acts on). This is value-of-information applied to intake (Hubbard's *clarification chain*): a thing is worth building only when it reduces an uncertainty that bears on a decision.

   *The thinking, in motion (observability):*
   - "Build me a dashboard."
   - *What would you watch on it?* — "Whether last night's batch finished."
   - *And when it hasn't?* — "We scramble to find out before customers feel it."
   - The need, named as the pair — **decision:** act now, before customers feel it, or not; **uncertainty:** did last night's batch fail. And *when* the decision gets made picks the delivery form: in the moment → an **alert** (push); periodic review → a report; on demand → a dashboard (pull); known and recurring → a runbook. The dashboard they asked for fits none of those — an alert does. That only came into view by laddering past the asked-for solution to the decision underneath.

2. **Is that answerable now, or must something exist first?** If a definition, a registry, a map, or a documented practice has to exist before the need can be met, that prerequisite is the real first step.

3. **Does the answer already exist somewhere?**

When someone already built something, two more:

4. **Does it serve the real need — at the right level, for the right audience?**

5. **Is it sustainable — does it trace to a real source, and could someone else keep it true?**

These last two are independent. Something can be well-built and serve the wrong need, or serve the right need with nothing underneath to keep it true. Check both.
> *In observability:* (4) does it answer what a business person would ask ("are customers completing checkout?"), not only what a technical person would ask ("is the API returning 200s?"). (5) do its inputs trace to a stakeholder expectation, or are they infrastructure-derived — a threshold set from a historical median answers "is it behaving as usual?", not "is it meeting what stakeholders need?"

When you can't tell from the request alone — whether there's a real need in it, or which one — flag it and get the context. A forced call on a request you don't understand is worse than an honest "I need more here."

Once you have the need(s), each one decomposes into the specific, answerable **questions** that serve it — that decomposition, and the map you place those questions on, is Part 2.

---

## Step 3 — Where it lands

Every item ends in one of these:

- **It already exists.** Point them to it.
- **They need the practice, not a build.** Give them the documented way to do it.
- **It isn't answerable yet.** The real first step is the prerequisite that has to exist before anything can be built on it — not the build.
- **They built something.** Assess it on the two axes: does it serve the real need, and could someone else keep it running?
- **Real gap, and it's ours.** Build it.
- **Real gap, but another team builds it.** Specify what's needed and hand off the build — but the ownership stays with you. Handing off the build isn't handing off the responsibility for the whole picture.
- **It's a capability, not an artifact.** That's a strategic decision in its own right — escalate it as one; don't slot it in as a single build.

> *In observability:* "it already exists" usually means another platform in the federation already covers it — check there first (e.g., holistic views, anomaly detection, log/dashboard tooling) before standing up something new.

## A worked instance — observability

*"Build a centralized SLO repository."*

- **Kind?** Build an artifact — treat it as a guess and look for the needs under it.
- **What do they need?** More than one thing: do our services even have SLOs, are we meeting the ones we have, can leadership see the picture across services. Three needs wearing one request.
- **Answerable yet?** The first two aren't. You can't report on SLOs nobody has defined, and defining them is stakeholder work, not a tooling task — so that comes first.
- **Does it already exist?** Check the platform federation for a registry or this reporting before building.
- **Built already?** No, so the last two questions don't apply.

**Where it lands:** first get the SLOs defined — nothing can report on them until then — then build or point to a registry once there's something to put in it. What it is *not* is a single "build the repository" ticket; that ships an empty shell.

## The same instrument, a different domain

*"Add a CSV export button."* (a product backlog, not observability)

- **Kind?** Build an artifact — the button is the guess.
- **What do they need?** To get their data into their own tools — which might be an API or a scheduled feed, not a button.
- **Answerable yet?** Maybe not: if the data model doesn't expose those fields, that comes first.
- **Does it already exist?** There may be an export elsewhere in the product.
- **Repeated?** If five teams want export, that's a platform capability, not five buttons.
- **Where it lands:** redirect (it exists) · enable (here's the API) · elicit (what data, for what) · build · or specify (the data team owns the pipeline, you keep the requirement).

Same walk, no observability content. The method is the instance-free part; observability supplies the vocabulary, not the structure.

---

## AI prompt for batch triage

Paste items into your AI assistant. (Swap the domain cue in line 1 for a different queue.)

```
I have intake items to triage. They arrive as solutions ("build/fix X"), not as needs.
For each one:

1. What can't they find out or do today? The request names something to build or fix —
   what would they be able to accomplish once it exists? There's usually more than one
   need hiding in a request. If it doesn't look like it belongs to this team, ask: would
   anyone know if the underlying outcome were wrong?

2. Can we meet those needs now, or does something have to exist first (a definition,
   registry, map, or documented practice)?

3. Might this already exist somewhere?

Flag anything where the answer depends on context you don't have.

Items:
```

---

# Part 2 — The reference: Observability Question Taxonomy

The map Part 1 reasons against. It defines the **space of abstract question types** that observability should answer for any service at any enterprise. Recovered needs decompose into questions that classify into cells; existing solutions are assessed by which cells they cover; practice gaps surface as cells no solution addresses.

Each cell is generated by a semantic chain — `standard × altitude × operational-mode → question type → widget form` — and carries its prior-art source inline, so the reasoning behind a cell is visible, not just the result.

**What it is not:** it does not enumerate service-specific questions (those are instantiations of a cell), and it is not itself a tool to build — it is the map a triager reasons against.

**Confidence legend:** **proven** = validated against real triage walks · **derived** = generated from named prior art, structurally sound but not yet walk-validated.

## The three layers

The taxonomy is the middle layer of a larger structure. A request never lands directly on a cell; it is routed across layers first.

```
Layer A — The practice (Part 1)     what the human experiences (the requestor conversation)
                                    "what are you really trying to find out or do, and why?"
Layer B — Question taxonomy         the live-inquiry space (mode × altitude) — what you can find out NOW
                                    from telemetry about current state
Layer C — Standing knowledge        the documented substrate B consults and A is often really asking for
            ├─ Model of reality:  dependency map / CMDB / service catalog / architecture
            └─ Documented practice: handbook / runbook library / how-to guide
```

- **Layer A** is Part 1 — the human surface, where the *need* is recovered (Step 2). It speaks the requestor's language; it talks in needs, never in cells.
- **Layer B** is this taxonomy — where the recovered need is decomposed into *questions* and each is placed. Both axes describe a *moment of inquiry* — when you ask, whose view answers. Everything in B is answered from live telemetry about current state; B is a **runtime** map. A and B are consecutive, not alternatives: A recovers the need, B turns it into placeable questions; one without the other either can't act or builds the wrong thing.
- **Layer C** is the standing, documented substrate that persists whether or not anyone is asking right now. The taxonomy *consumes* it — blast radius and impact propagation both read dependency relationships — but has no representation for *building or maintaining* it. In a large estate, building and maintaining Layer C is much of the work.

## From need to placed question

A recovered need (Part 1, Step 2) is not yet placeable — it has to be decomposed into the answerable units that serve it. A need is a **(decision, uncertainty) pair**; a *question* is a specific formulation whose answer, from telemetry, reduces that uncertainty enough to decide. One need usually yields *several* questions, frequently at different altitudes.

Take the batch need from Part 1 — *"know a batch failed in time to act before customers feel it."* It decomposes into "did the batch complete on time?" (Mode 1 · Step 0 · Business, best delivered as an **alert**), "which job failed?" (Step 1 · Technology), and "what customer process is at risk?" (Step 2 · Business). Recover the need first — it catches wrong-altitude and wrong-delivery-form answers; then place each question.

To place a question, pin it on:

- **When are they asking?** — incident · routine check · after a change · planning growth · proving compliance · watching a trend · checking coverage · cost · toil · is-the-alerting-any-good (the modes, below)
- **Whose view answers it?** — business outcome · business process · application · infrastructure · capability/leadership (the altitudes, below)
- **Where in the event?** — the alert fires → you comprehend → you respond (most real requests are about the alert firing well)
- **What shape?** — one service or thousands? a step in a journey (order matters)? batch job or container?

A **build** request is neither a question nor a standing-knowledge need — it is a construct that serves a set of both. Decompose it first into the questions it will answer (→ the map below) and the foundation it needs (→ Layer C), then place each element. This is why the dominant request type (*build-me-X*) can't be placed directly: the single most important skill is **recovering the buried question from solution language**, including from requests worded as fixes or that don't look like observability at all. The default is *"what observability question is implied?"*, not *"is this even observability?"* — true out-of-domain requires positive evidence, not a vocabulary mismatch.

## Axis 1 — Operational modes (rows): *when and why* a question is asked

Each mode is a distinct *occasion of asking* — the same subject generates different questions in different modes.

| # | Mode | Governing prior art | The recurring question |
|---|------|--------------------|------------------------|
| 1 | **Incident Triage** | ITIL 4 Incident Management; Google SRE incident response (assess→mitigate→diagnose); OODA | "Something is wrong — what do I do?" (7-step flow) |
| 2 | **Routine Monitoring / Readiness** | Google SRE Ch.6 *Monitoring Distributed Systems* (golden signals, symptom-based); ITIL 4 *Monitor & Event Management* | "Is everything healthy right now / ready for the day?" |
| 3 | **Change Validation** | DORA (change failure rate, time-to-restore); Google SRE *Release Engineering* + *Canary Analysis* | "Did this change degrade anything?" |
| 4 | **Capacity Planning** | Google SRE *capacity planning* (organic/inorganic growth, demand forecasting); SRE Workbook | "Will we have enough? When do we run out?" |
| 5 | **Compliance & Audit** | COSO ERM 2017 (compliance driver); OpenSLO/SLODLC (SLA conformance, error budget as evidence); regulatory obligation | "Can we prove we met our obligations? What's the exposure?" |
| 6 | **Trend Analysis** | Google SRE (error-budget burn, reliability over time); DORA trend; SLODLC; Tufte (small multiples) | "Are we getting better or worse?" |
| 7 | **Coverage & Maturity** | CNCF Observability Maturity Model; DORA capability self-assessment; expectation-to-signal traceability | "What's unmonitored? How mature is our observability?" |
| 8 | **Cost & Efficiency** | FinOps Framework (unit economics); Google SRE efficiency/utilization | "What does this cost? Is resource use efficient?" |
| 9 | **Toil & Operational Burden** | Google SRE Ch.5 *Eliminating Toil*; ISA-18.2/IEC 62682 (alarm rate, alarm flood) | "How much manual burden / alert noise does this generate?" |

## Axis 2 — Altitudes (columns): *whose perspective* answers it

ArchiMate 3.2 layers, each bound to its health-dimension framework. The Serving relationship (Technology → Application → Business) is the blast-radius / impact-propagation chain.

| Altitude | ArchiMate | Subject terms | Health framework | Typical consumer |
|----------|-----------|---------------|------------------|------------------|
| **Business** | `archimate:Business` | business process, business service | **APQC** Process Performance (effectiveness, efficiency, adaptability) | product owner, business owner, compliance officer |
| **Application** | `archimate:Application` | application service, API, component | **Golden Signals** (Latency, Traffic, Errors, Saturation) / RED | developer, app owner |
| **Technology** | `archimate:Technology` | node, server, cluster, database | **USE** (Utilization, Saturation, Errors) | platform / SRE |

A higher altitude exists in Motivation space (`archimate:Driver`/`Outcome`) — this is where **impact** lives (COSO drivers are business-risk categories). It is not a separate column; it sits above Business and is reached by the impact and blast-radius traversals. A **Strategy** altitude (ArchiMate Strategy layer: Capability, Value Stream) sits above that, for division-level capability/maturity questions.

## Widget-form vocabulary

| Form | Prior art |
|------|-----------|
| Status indicator (tile/traffic light) | Nagios two-threshold (1999) |
| Gauge (value vs target) | OpenSLO `objective.target` |
| Impact statement | COSO + composed |
| Trend line | Prometheus range vector + Grafana |
| Comparison / small multiples | Tufte |
| Dependency graph (topology) | ArchiMate Serving / Composition |
| List / decomposition | ArchiMate Composition |
| Contact card | vCard (RFC 6350) + ITIL RACI |
| Runbook procedure | ISA-18.2 ARR |
| Forecast / headroom | capacity-planning projection |
| Coverage matrix | expectation-to-signal mapping |

---

## The matrix

### Mode 1 — Incident Triage (ITIL 4 Incident Management) — 7 steps × 3 altitudes

| Step (ITIL phase) | Business (APQC) | Application (Golden Signals) | Technology (USE) |
|---|---|---|---|
| **0 — Health** ("is it healthy?") *Detection* | "Is this process meeting performance expectations?" → status indicator · **proven** | "Is this service healthy on its golden signals?" → status indicator · **proven** | "Is this node healthy on USE?" → status indicator · **proven** |
| **1 — Scope** ("what specifically?") *Triage* | "Which child process/service is unhealthy?" → decomposition list (Composition) · **proven** | "Which component/endpoint is unhealthy?" → list · **derived** | "Which instance/node is unhealthy?" → list · **derived** |
| **2 — Impact** ("what's the business impact?") *Prioritization* | "What business outcome is at risk, and how much?" → impact statement (COSO driver) · **proven** | impact at app altitude — realized only by Serving-propagation to business | impact at tech altitude — same; not an independent cell |
| **3 — Cause** ("why is it red?") *Diagnosis* | "Which underlying requirement/outcome failed?" → analytical breakdown (Realization) · **proven** | "Which golden signal degraded, and where?" → analytical · **proven** | "Which USE dimension is saturating/erroring?" → analytical · **derived** |
| **4 — Blast radius** ("what else is affected?") *Propagation* | "Which other business processes depend on this?" → dependency graph (Serving up) · **proven** | "Which app services depend on this one?" → dependency graph · **derived** | "Which app services run on this node?" → dependency graph · **derived** |
| **5 — Ownership** ("who do I call?") *Escalation* | "Who owns this process?" → contact card (vCard+RACI) · **proven** | "Who owns this service?" → contact card · **derived** | "Who owns this infrastructure?" → contact card · **derived** |
| **6 — Runbook** ("what's the fix?") *Resolution* | "What's the recovery procedure?" → runbook (ISA-18.2 ARR) · **proven** | "What's the service runbook?" → runbook · **derived** | "What's the node runbook?" → runbook · **derived** |

### Modes 2–9 — Industry-scope modes — all derived

**Mode 2 — Routine Monitoring / Readiness** (SRE Ch.6; ITIL Monitor & Event Mgmt)

| Business | Application | Technology |
|---|---|---|
| "Is the portfolio ready for business today?" → worst-child rollup · **proven** | "Are all services in this portfolio healthy?" → rollup · **derived** | "Are all nodes/clusters healthy?" → rollup · **derived** |

**Mode 3 — Change Validation** (DORA change-failure-rate / MTTR; SRE canary)

| Business | Application | Technology |
|---|---|---|
| "Did this release change the business-outcome rate?" → before/after comparison · **derived** | "Did this deploy shift golden signals vs baseline (canary)?" → comparison · **derived** | "Did this change shift resource utilization?" → comparison · **derived** |

**Mode 4 — Capacity Planning** (SRE demand forecasting)

| Business | Application | Technology |
|---|---|---|
| "Will process throughput meet forecasted demand?" → forecast · **derived** | "Will the service handle projected traffic?" → forecast (Traffic/Saturation trend) · **derived** | "When will this resource saturate at current growth?" → headroom/burn-down · **derived** |

**Mode 5 — Compliance & Audit** (COSO compliance; OpenSLO conformance) — strongest at Business; app/tech is SLA-conformance proxy

| Business | Application | Technology |
|---|---|---|
| "Did we meet regulatory/SLA obligations this period?" → conformance report · **derived** | "Did the service meet its SLA / error budget?" → budget gauge · **derived** | "Did infrastructure meet availability commitments?" → conformance report · **derived** |

**Mode 6 — Trend Analysis** (SRE error-budget trend; DORA trend; Tufte)

| Business | Application | Technology |
|---|---|---|
| "How has the outcome trended / compared across cohorts?" → trend / small multiples · **proven** | "How have golden signals / error budget trended?" → trend line · **derived** | "How has utilization trended?" → trend line · **derived** |

**Mode 7 — Coverage & Maturity** (CNCF Maturity Model; DORA capability; expectation-to-signal traceability)

| Business | Application | Technology |
|---|---|---|
| "Which business expectations have no signal coverage?" → coverage matrix · **derived** | "Which services have no SLO defined?" → coverage matrix · **derived** | "Which nodes have no instrumentation?" → coverage matrix · **derived** |

**Mode 8 — Cost & Efficiency** (FinOps Framework — an *adjacent* discipline to the core observability stack)

| Business | Application | Technology |
|---|---|---|
| "What is cost-per-transaction / cost-to-serve?" → cost trend · **derived** | "What is the service's resource cost / efficiency?" → cost gauge · **derived** | "What is infra cost vs utilization efficiency?" → cost/utilization · **derived** |

**Mode 9 — Toil & Operational Burden** (SRE Ch.5 Eliminating Toil; ISA-18.2 alarm rate)

| Business | Application | Technology |
|---|---|---|
| "How much manual intervention does this process require?" → rate/trend · **derived** | "What is the alert volume / on-call burden?" → rate/trend · **derived** | "What is the alarm-flood rate / noise?" → rate · **derived** |

---

## Cross-consistency notes

Not all mode × altitude cells are independent, equally valid configurations:

1. **Step 2 (Impact) at Application/Technology — conditional.** Impact is a Motivation-altitude concept (COSO drivers are business-risk categories). At app/tech altitude, "impact" exists only by Serving-propagation upward to business — it is the blast-radius traversal (Step 4) viewed from impact's angle, not an independent cell.
2. **Mode 5 (Compliance) at Application/Technology — proxy only.** Regulatory obligations are business obligations. App/tech compliance reduces to SLA/error-budget conformance — valid but derivative of the business-altitude obligation.
3. **Mode 8 (Cost) — adjacent-discipline grounding.** FinOps is a named, published framework but sits *adjacent* to observability, not inside the core SRE/ITIL/DORA stack. The cells are real; their prior art is borrowed from financial operations.

---

## Layer C — two faces

**Face 1 — Model of reality** ("what exists and what depends on what"): ITIL 4 Service Configuration Management (CMDB); ISO/IEC/IEEE 42010 architecture description; the C4 model; ITIL 4 Service Catalogue Management. Dependency mapping lives here.

**Face 2 — Documented practice** ("how to do it / what to do"): DORA documentation-quality capability (documentation is a *measured* predictor of performance, not an afterthought); ITIL 4 Knowledge Management (the handbook, the known-error database); Google SRE service docs + postmortems; ISA-18.2 ARR as a maintained runbook library. In DIKW terms, B is the *information* layer (answers); C-Face-2 is the *knowledge* layer (reusable, documented understanding).

A standing model only works if it is **owned, versioned, single-source, and kept current** — or it rots into the stale page nobody believes mid-incident.

## The delivery-form axis

The "widget form" column quietly assumed every answer is a live dashboard panel. The same question's answer is delivered in multiple forms:

`dashboard (pull) · alert (push) · report (periodic) · runbook (procedure) · documentation (reference)`

Which form follows from **when the decision is made**: in the moment → alert (push); periodic review → report; on-demand investigation → dashboard (pull); known and recurring → runbook; reference for a standing decision → documentation. The form is a consequence of the decision's timing, not a taste choice.

**Documentation is the delivery form that bridges B up to C-Face-2.** "Guidance for how to monitor a business workflow" has no runtime cell because it isn't a runtime question — it's a Layer-C artifact delivered as documentation.

---

## The detection / alerting phase

An observability event has three temporal phases:

1. **Detection / Alerting** — signal → event → filter → correlate → dedup → incident
2. **Comprehension** — the 7-step Mode-1 flow this taxonomy models
3. **Response** — runbook → mitigate → resolve → postmortem

The taxonomy models a person who *decides to look*. In real operations the flow starts earlier, at **Step −1: an alert fired and paged someone** — the system decides to tell the human. This phase is the highest-volume, highest-pain part of operations (alert fatigue, noise, false positives, missed detection, alarm storms), and at scale it becomes a **correlation** problem.

Prior art for this phase, often under-applied: ISA-18.2's *primary* subject is alarm management (rate, flood, priority, suppression, stale/chattering alarms); ITIL **Monitoring & Event Management** (the event/alert lifecycle) is distinct from Incident Management (the Mode-1 triage flow); Google SRE "Practical Alerting" and multi-window multi-burn-rate SLO alerting; AIOps / event correlation. The incident itself is a **live standing-state object** (lifecycle open→triaged→escalated→resolved→closed, severity, timeline, assignee, postmortem).

---

## Why scale changes everything

The mode × altitude matrix is the **comprehension kernel** — correct and proven at a single service. At thousands of services the cross-cutting dimensions that look like additions become load-bearing, and the single-subject matrix becomes one view among them:

- **Layer C** — mandatory at scale (nobody holds thousands of services in their head); skippable at n=1.
- **Detection at scale** — "set a threshold" becomes "correlate the storm."
- **Platform federation** — exists *because* no single tool covers the estate.
- **Coverage & Maturity (Mode 7)** — trivial at n=1, the governing question at scale.
- **Scale / cardinality** — portfolio rollup, fleet triage, cross-line comparison, hierarchy aggregation.
- **Heterogeneity** — batch jobs, containers, vendor-integrated services, real-time payments — different observability shapes through one instrument.

The instrument's real job is at scale. The cross-cutting dimensions are not edge cases — they are the enterprise skeleton, and the mode × altitude matrix is one rib.

---

## Status

- **Proven (walked):** Mode 1 (Incident Triage), validated against real incident-triage walks — Business strong, Application moderate, Technology thin.
- **Derived, not walked:** Modes 2–9. The semantic chain holds; no walk validation yet.
- **The practice flow (recover → place → decide):** tested and repaired — the decompose-the-build step was added after build requests broke an original one-request-one-placement assumption; it held under independent classification with two named ambiguity points — observability-or-not when the text is indeterminate, and build-vs-mandate at the boundary.

This is a baseline, not a finished artifact — it evolves through use. The riskiest standing claim is that modes parameterize cleanly across all three altitudes; the cross-consistency notes show several cells are conditional rather than independent.
