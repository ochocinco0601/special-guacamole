# PE Pillar — Business Observability Deck Brief

**Purpose:** Content source for Claude design to produce a slide deck for the CT Observability & Business Context pillar PEs.

**Audience:** PEs in the pillar — Bobby Parikh, Vanita Adulkar, Balla Durga Shanker, Srikanth Kari (Jason and Rajan as sponsors). Observability-fluent peers, not customers being sold to.

**Stance:** Peer-to-peer co-design. They are co-owners of this pillar. The deck invites engagement, it does not sell the concept.

**Spine:** Show the input → show the output → show the plumbing → show the gaps. Practicality over concept throughout.

**Running example:** Credit Check Service carries the whole deck. Same service shown at input, output, dashboard, dev task, platform task, handoff. By the end they have seen one service produced end-to-end.

---

## Deck Calibration (paste into Claude design context prompt)

**Tone guards:**
- Do not lead with architecture (four-layer model, factory model, semantic flow). Land these mid-deck if at all.
- Do not teach observability fundamentals — audience has them.
- Never claim enterprise scale without the n=1 entry point in the same breath.
- Use audience vocabulary: SLIs, SLOs, alerts, dashboards, runbooks, incident response, error budgets. Avoid "telemetry" in the abstract.
- Prefer showing artifacts over explaining concepts. Every slide answers "what is this thing, concretely?" not "why does this matter?"

**Recurring formulation (weave into 2–3 slides):** *"We are reconstructing meaning during every incident."*

**Visual language:**
- Tables over prose where possible — PEs read tables fast.
- Monospace for query/config snippets.
- The existing asset `dashboard-template-credit-check.png` drops into Slide 4.
- Side-by-side "before/after" on Slide 3 alert comparison.

---

## Slide 1 — Title

**Title:** Business Observability: What We're Building and What We Need to Co-Design

**Subtitle:** Observability & Business Context Pillar · CT PE Group · [date]

**Footer:** Chad Johnson · Consumer Technology Platform

**Notes:** Minimal opener. Real opening is Slide 2. Keep aesthetic consistent with pillar OKR slide set if possible.

---

## Slide 2 — The Unit We're Onboarding

**Headline:** Credit Check Service — what a completed business observability capture looks like.

**Body:** One filled-out service profile, shown as the PO produces it. Real field values.

**Service Identity:**

| Field | Value |
|---|---|
| Service Name | Credit Check Service |
| Service ID | `HOME_ORIG_CREDIT_CHECK` |
| Description | Validate borrower creditworthiness for loan approval decisions |
| Tier | Tier 2 |
| Product Line | Home Lending |
| Business Domain | Home Lending |
| Functional Category | Credit Assessment |
| Org Product | Home Originations Platform |
| Technical Owner | robert.kim@example.com |

**Stakeholder Expectations:**

| Impact Category | Stakeholder | Priority | Expectation | Impact if unmet |
|---|---|---|---|---|
| Customer Experience | Loan Applicants | High | Credit checks return valid scores within acceptable timeframe | Applicants unable to proceed |
| Financial | Home Lending | High | Credit checks complete successfully | Lost loan origination revenue |
| Legal & Compliance | Regulatory Body | High | Meet FCRA 30-day timing requirements | Regulatory violation risk |
| Operational | Loan Processors | Medium | Complete without manual intervention | Manual workarounds reduce capacity |

**Callout:** *"This table doesn't exist today for most services. The information lives in people's heads — and when they leave, it leaves with them."*

**Speaker note:** Don't explain the concept first. Show the artifact. Let PEs read it. One sentence of setup: "This is the structured capture a PO produces for one service. Here is Credit Check fully completed." Let the table speak.

---

## Slide 3 — The Alert, Before and After

**Headline:** Same signal. Same tooling. Business context attached.

**Body — side by side, identical formatting for direct comparison:**

**Today:**
```
[CRITICAL] Credit Check Service
Response time > 500ms threshold exceeded
Duration: 4 minutes
Dashboard: grafana.../credit-check
```

**With business observability:**
```
[CRITICAL] Credit Check Service — Applicant impact active
Signal: Credit Check Success Rate at 62% (SLO 85%)
Customers affected: ~1,200 applicants blocked
Revenue at risk: loan origination pipeline delayed
Compliance: FCRA 30-day timing exposure if >6h
Notify: Home Lending VP (customer threshold)
Dashboard: grafana.../credit-check-bos
Runbook: wiki.../credit-check-degradation
```

**Key point:** Both alerts fire on the same underlying signal (request/response data). The enrichment is metadata attached from the structured capture on Slide 2 — no new instrumentation, no new tool.

**Speaker note:** This is the slide that should land. If PEs engage on anything, engage on this. Prompt: *"What's the minimum your runbook expects you to know in the first 60 seconds? Does the enriched version give you that?"*

---

## Slide 4 — The Dashboard, Generated

**Headline:** Generated from the capture, not hand-built per team.

**Body:** Drop in `stakeholder-communications/enterprise-working-group/confluence-site/dashboard-template-credit-check.png` full-width.

**Annotate the image with callouts (Claude design: add 4 numbered callouts):**
1. **Service header** — from Service Identity fields (Slide 2)
2. **Business Health panel** — SLI name + SLO target + current value — from Health Signals
3. **Impact panels (4 categories)** — Customer / Financial / Legal / Operational — from Impact Signals
4. **"Not defined" placeholders** — where the capture is incomplete; visible gaps, not silent ones

**Key point:** The dashboard on screen is produced from the same structured capture shown on Slide 2. No hand-drawing. If the capture changes, the dashboard regenerates.

**Speaker note:** PEs will ask "is this real?" — Honest answer: the template is real, the generator is partial (Grafana panel tools exist; full pipeline doesn't). Flag this; don't oversell. Slide 8 addresses current state directly.

---

## Slide 5 — The Developer's Actual Work

**Headline:** Same SLI work they already do. One new input: the signal spec.

**Body — what PO hands off, what Dev adds:**

| From PO | Dev adds |
|---|---|
| Signal name: `credit-check-success-rate` | `sliType`: ratio vs threshold |
| SLO target: 85% | `goodEventsCriteria_Dev` (query) |
| Time window: 1 hour rolling | `totalEventsCriteria_Dev` (query) |
| Budgeting: Occurrences | `dataSource`: sql / splunk / prometheus |
| "Why 85%": bureau connectivity focus | `queryImplementation` (production query) |

**Concrete query example:**

```sql
-- Good events (Credit Check success)
SELECT COUNT(*) as good_events
FROM credit_check_requests
WHERE status = 'SCORE_RETURNED'
  AND valid_score = TRUE
  AND response_time_ms < 30000
  AND request_time >= NOW() - INTERVAL 1 HOUR;

-- Total events
SELECT COUNT(*) as total_events
FROM credit_check_requests
WHERE request_type = 'CREDIT_CHECK'
  AND request_time >= NOW() - INTERVAL 1 HOUR;
```

**Translation patterns Dev uses (from the field guide):**
- "Successfully" → `status IN ('SCORE_RETURNED') AND error_code IS NULL`
- "Within 30 seconds" → `response_time_ms < 30000`
- "For applicants" → `request_type = 'CREDIT_CHECK' AND applicant_id IS NOT NULL`

**Framing line:** *"Telemetry choices are implementation details. Business defines WHAT success looks like; Dev defines HOW to measure it."*

**Speaker note:** This slide kills the "new work" objection. It's the SLI work they already do — the only new input is the signal spec from PO. If a dev has ever written an SLI query, they have done this.

---

## Slide 6 — The Platform's Actual Work

**Headline:** Alert thresholds, routing, dashboard panels, runbook links. In the tools you already run.

**Body — what Dev hands off, what Platform configures:**

| From Dev | Platform adds |
|---|---|
| `queryImplementation` | `alertingThreshold` (0.2–0.5% above SLO) — 85.3% |
| `dataSource` | `pageThreshold` (0.5–1% below SLO) — 84.0% |
| `dataSourceDetails` | `alertNotificationTargets` — pagerduty + slack |
| — | Dashboard panel (generated from template) |
| — | Runbook link |

**Alert structure:** `[SEVERITY] Service Impact → Business Consequence → Technical Detail`

**Where this lives:**
- Alert rules → existing Splunk / Prometheus
- Escalation routing → existing PagerDuty
- Dashboard → existing Grafana
- Runbook → existing wiki

**No new platform. No new tool. The BOS layer is metadata attached to existing configuration.**

**Speaker note:** This preempts the HealthScope question. BOS defines, platforms render. The capture on Slide 2 drives what Platform configures here — same tools, richer metadata.

---

## Slide 7 — The Handoff

**Headline:** One artifact. Three roles. Explicit boundaries.

**Body — row-by-row field ownership:**

| Field | PO | Dev | Platform |
|---|---|---|---|
| Service identity, tier, owner | ✓ fills | read-only | read-only |
| Stakeholders + expectations | ✓ fills | read-only | read-only |
| Impact definitions (customers, $, regulatory) | ✓ fills | read-only | read-only |
| Health signal name + SLO target + rationale | ✓ fills | read-only | read-only |
| Signal type (ratio/threshold) | — | ✓ fills | read-only |
| Query implementation + data source | — | ✓ fills | read-only |
| Alert thresholds + routing | — | read-only | ✓ fills |
| Dashboard URL + runbook URL | — | read-only | ✓ fills |

**Format:** A single structured record per service — CSV row today, normalizing toward a BOS data model. Lives in: Story Set Workspace (web UI prototype), spreadsheet template, or Jira user story with the four ACs. All three produce the same structured output.

**Constraint:** PO's signal names and targets are **constraints** for Dev, not suggestions. Dev implements what PO defined; changes are a conversation, not a unilateral rewrite.

**Speaker note:** PEs will ask about handoff sequencing. Honest answer: not fully decided. AI pre-populating + all three validating is one model. Strict sequential is another. This is Open Problem #3 on Slide 9.

---

## Slide 8 — Current State: What's Built, What's Paper

**Headline:** Honest inventory.

**Body — three columns:**

**Built and running:**
- Confluence knowledge hub — 4 pages live at `ctj0601.atlassian.net/wiki/spaces/PM/` (Cloud preview; WF Server deployment planned)
- Field guides for all three roles — `documentation/guides/{po,developer,operations}-field-guide.md`
- Credit Check end-to-end capture — `po-role-page.md` with all AC 1.1–1.4 filled
- Credit Check Story Set HTML — `director-deep-dive/credit-check-story-set.html`
- Observability Story Set with PO/Dev/Platform tabs — `director-deep-dive/observability-story-set.html`
- Dashboard template (Credit Check) — rendered screenshot

**Built on paper, not running:**
- Dev practitioner page (drafting next)
- Platform practitioner page (drafting next)
- BOS onboarding simulation HTML (scoped, not built)
- Enterprise data model (domain model exists; normalized schema in progress)
- Factory pipeline end-to-end (Grafana panel generators partial; full pipeline conceptual)

**Unsolved:**
- Adoption mechanism at 500+ app scale (Open Problem #1)
- Integration insertion point into existing team workflows (Open Problem #2)
- Three-role handoff sequencing (Open Problem #3)
- What "done" looks like for one service in operational reality (Open Problem #4)

**Framing line:** *"This is a starting point, not a finished system."*

**Speaker note:** This slide is load-bearing. If Chad omits it, the first question is "where's the working pipeline?" Saying this honestly peer-to-peer builds credibility and makes Slide 9 an honest invitation rather than a deflection.

---

## Slide 9 — What We Need to Co-Design

**Headline:** Four engineering decisions. Framed as technical problems, not philosophy.

**Body — four open problems, each a concrete engineering question:**

**1. Adoption trigger.** CT has 500+ applications. A program-style "onboard 50 by Q3" produces compliance behavior — forms filled, definitions useless. What signal makes a team reach for this on its own?
- *Candidate triggers:* P1 postmortem gap, new SRE onboarding, failed audit, new executive dashboard request
- *Decision needed:* which trigger(s) do we design for? How do we instrument detection?

**2. Integration insertion point.** Existing team workflows — alert authoring, dashboard review, postmortem, SLO review — where does the business-context capture insert with least friction?
- *Candidate insertion points:* alert creation wizard, dashboard template, postmortem template, sprint planning
- *Decision needed:* which workflow owns it? What does the integration contract look like?

**3. Three-role handoff sequencing.** PO → Dev → Platform sequential? All three validate an AI pre-populated draft? Something else?
- *Candidate models:* sequential (strict), concurrent-validate (AI drafts, all refine), Dev-led (implementation drives, PO annotates)
- *Decision needed:* which handoff model, and what data model supports it?

**4. n=1 success criteria.** If this group picked one real service and onboarded it end-to-end, what's convincing?
- *Candidate measures:* time-to-impact-clarity in an incident, dashboard actually used in ops review, fewer "who's affected?" Slack messages during a P1
- *Decision needed:* what do we commit to measuring on the first service?

**Closing line:** *"If this doesn't help one real piece of work better, we shouldn't expect it to work across hundreds."*

**Speaker note:** This is the most important slide. Do not compress it. Do not answer the questions on the slide — leave them open. Passivity is the failure mode. The explicit invitation + genuinely open engineering questions are what prevent "interesting, thanks for sharing." If energy goes to one problem in the room, let it. Deep engagement on one beats surface coverage of four.

---

## Backup slides (appendix — include only if asked)

### B1 — Four-Layer Model

| Layer | What it measures | Who owns |
|---|---|---|
| 1: System | Infrastructure health — CPU, memory, network | Platform |
| 2: Process | Application behavior — queries, errors, latency | Dev |
| 3: Business Health | Is the service meeting stakeholder expectations? | PO defines, Dev implements |
| 4: Business Impact | What's the cost when Layer 3 degrades? | PO defines, Dev implements |

*Traditional observability covers Layers 1–2. BOS adds Layers 3–4.*

### B2 — Factory Model (scaling mechanism)

One structured capture per service drives five production lines:

| Line | Input → Output |
|---|---|
| Story Factory | Capture fields → Jira stories with BDD AC |
| Dashboard Factory | SLI + SLO + Impact → Grafana panels |
| Alert Factory | Dev criteria + thresholds → monitoring rules + escalation |
| Playbook Factory | Failure scenarios + stakeholders → response procedures |
| Documentation Factory | Business purpose + criteria → service catalog |

*Quality argument for PO input ownership: only product teams can produce the quality of business context required. Platform-alone produces static, mediocre output — not from lack of capability, but from structural lack of domain knowledge.*

### B3 — Confluence Knowledge Hub

Four pages live at `ctj0601.atlassian.net/wiki/spaces/PM/`:
1. Landing — Business Observability
2. Problems Business Observability Solves (15 problems + 7 implementation lessons)
3. How It Works (process model, stakeholder expectations, dev/platform work)
4. What Structured Business Context Looks Like (Wire Transfer example)

### B4 — Pushback quick-reference

| If asked | Response |
|---|---|
| "Isn't this just business context, not observability?" | Pillar charter includes "& Business Context." Industry trajectory: Google SRE → SLO-based reliability → customer-centric observability. |
| "How does this relate to HealthScope?" | BOS is methodology, not tooling. Produces artifacts that feed any platform. See Slide 6. |
| "More work for dev?" | Devs already write SLIs. The only new input is the signal spec from PO. See Slide 5. |
| "Won't this rot?" | It produces dashboards + alerts. If definitions are wrong, operations feels it in the next incident. Feedback loop is architectural. |
| "Can't standardize 300+ apps" | Standardizing descriptions, not implementations. See Slide 9 Problem #1. |
| "We already have SLOs" | SLOs are part of this. Difference: start from business expectations and derive signals — not start with metrics and guess if they matter. |

---

## Visual asset inventory (for Claude design)

**Available in repo:**
- `stakeholder-communications/enterprise-working-group/confluence-site/dashboard-template-credit-check.png` — Slide 4 hero image
- `director-deep-dive/credit-check-story-set.html` — renderable example for sidebar / appendix thumbnail
- `director-deep-dive/observability-story-set.html` — PO/Dev/Platform tabbed view

**Suggested visual style:**
- Tables over prose
- Monospace for query/config blocks
- Muted palette (no alarm-reds except in the alert slide)
- Consistent service/stakeholder iconography across slides 2, 4, 7

---

## Source artifacts (for verification)

- Credit Check fields — `stakeholder-communications/enterprise-working-group/confluence-site/po-role-page.md`
- Dev query patterns — `documentation/guides/developer-field-guide.md`
- Platform config patterns — `documentation/guides/operations-field-guide.md`
- Pushback taxonomy — `stakeholder-communications/o11y-pillar-pushback-scenarios.md`
- Stage-by-stage framing — `stakeholder-communications/pe-pillar-kickoff-outline-draft.md`
- Four-layer model + semantic flow — `documentation/principles/` (CLAUDE.md navigation hub)
- Factory model — `documentation/principles/operational-factory-model.md`
- Confluence site pages — `stakeholder-communications/enterprise-working-group/confluence-site/{landing-page,child-01,child-02,child-03}.md`
