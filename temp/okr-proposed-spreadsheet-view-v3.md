# Chad's Proposed OKR Spreadsheet View

**Purpose:** Exact cell-level representation of proposed changes mapped to the team's actual spreadsheet columns. Ready to transfer to WF spreadsheet.
**Date:** 2026-03-03

---

## Key Terms Used in This Document

**BOS (Business Observability):** A framework that adds business context to technical monitoring. Traditional monitoring answers "what's broken?" BOS adds "what does it mean for the business?" — who is affected, what are they experiencing, and what's the financial or customer impact.

**BOS Progression Pipeline:** The four stages a service goes through to become business-observable. Used throughout this document to define what "onboarded" means and to set adoption targets.

| Stage | Name | What It Means | A service is at this stage when... |
|-------|------|--------------|-----------------------------------|
| 1 | Identified | The service has been selected for BOS onboarding | An L3 lead has named it as a critical flow and it appears on a documented list |
| 2 | Contextualized | A Product Owner has defined what "healthy" and "broken" look like in business terms | Business success criteria exist: who the stakeholders are, what they expect, what impact looks like when it fails |
| 3 | Instrumented | Business health signals are built and live in production | Dashboards or alerts exist that show business health (not just system health) and they are actively receiving data |
| 4 | Operationalized | Teams use business health signals during incidents and operational decisions | Signals have been referenced during at least one real incident or are included in regular operational reviews |

**BOS Tracking System:** Where pipeline stage progress is recorded. This is currently tracked via Jira using the `CT-HLT-OKR-Stability-Observability` label. Each service's pipeline stage is updated as onboarding work progresses.

**PO-defined:** Business context defined by the Product Owner or L3 lead who understands the service's business purpose — not by the platform or SRE team. The people closest to the business define what matters; the technical teams build the monitoring to match.

---

## Current State (V3 Spreadsheet — What Exists Today)

| Row | Objective (A) | Outcomes (B) | Key Results (C) | 2026 Strategic Measures (D) | Measurement Methodology & Data Source (E) | Assigned (F) |
|-----|--------------|-------------|-----------------|---------------------------|------------------------------------------|-------------|
| 11 | Ensure Operational Stability that delivers a consistent customer experience | 1) Reduce Incident Impact and Improve Recovery; 2) Strengthen Observability and Alert Hygiene; 3) Establish Business Observability Capability | Deliver a generic, reusable business observability framework | Deliver BOS framework with business health signal model, impact quantification methodology, and dashboard templates by Q2 | *(empty)* | Chad |
| 12 | | | | Define business success criteria structure for critical services by Q2 | *(empty)* | Chad |
| 13 | | | | Establish SLO mapping methodology appropriate for organizational maturity level by Q2 | *(empty)* | Chad |
| 14 | | | | Reduce time-to-business-impact identification to ≤15 minutes for onboarded services by Q4 | *(empty)* | Chad |
| 15 | | | L3 leads identify critical flows from their product areas and team instruments them through the framework | Each L3 lead identifies top 3 critical customer journeys/flows for their product area by Q2 | *(empty)* | L3 Leads |
| 16 | | | | Instrument ≥50 identified flows with business health and impact signals visible in observability platform by Q4 | *(empty)* | Chad + L3 Leads |
| 17 | | | | Onboard ≥20 product teams to BOS by Q4 | *(empty)* | Chad |
| 18 | | | | Visualize SLA adherence for critical applications via Grafana/observability platform with ≥99.9% adherence visible by Q4 | *(empty)* | Chad |

---

## Proposed State (Transfer-Ready)

| Row | Objective (A) | Outcomes (B) | Key Results (C) | 2026 Strategic Measures (D) | Measurement Methodology & Data Source (E) | Assigned (F) |
|-----|--------------|-------------|-----------------|---------------------------|------------------------------------------|-------------|
| 11 | Ensure Operational Stability that delivers a consistent customer experience | Reduce Incident Impact and Improve Recovery | Reduce time-to-business-impact identification to ≤15 minutes for onboarded services by Q4 | Deliver BOS framework with business health signal model, impact quantification methodology, and dashboard templates by Q2 | 1) Track in Jira under CT-HLT-OKR-Stability-Observability label; 2) Acceptance criteria: signal model reviewed/approved, impact quantification methodology reviewed/approved, dashboard templates reviewed/approved | Chad |
| 12 | | | | Define business success criteria structure for critical services by Q2 | 1) Criteria template published and available; 2) ≥N services have PO-completed business success criteria using the template; 3) Source: BOS onboarding artifacts in Jira | Chad |
| 13 | | | | Establish SLO mapping methodology appropriate for organizational maturity level by Q2 | 1) Methodology document published; 2) Validated by applying it to ≥1 real service end-to-end; 3) Track in Jira under CT-HLT-OKR-Stability-Observability label | Chad |
| 14 | | Strengthen Observability and Establish Business Observability Capability | ≥20 product teams onboarded to BOS with ≥1 service at Stage 3 (Instrumented) and a combined ≥50 critical flows instrumented by Q4 | Each L3 lead identifies top 3 critical customer journeys/flows for their product area by Q2 | 1) Documented list per L3 lead with PO acknowledgment; 2) Source: BOS onboarding artifacts in Jira; 3) Quarterly review to confirm lists are current | L3 Leads |
| 15 | | | | Instrument identified flows with PO-defined business health and impact signals visible in observability platform by Q4 | 1) Count of flows at Stage 3 or above with PO-defined business context completed; 2) Signal types per flow determined by PO business context (may include SLA adherence, transaction health, customer impact, error rates); 3) Source: Jira tracking under CT-HLT-OKR-Stability-Observability; 4) Quarterly targets: Q1: 12, Q2: 25, Q3: 37, Q4: 50 | Chad + L3 Leads |
| 16 | | | | Onboard product teams to BOS with ≥1 service at Stage 3 (business health signals live in production) by Q4 | 1) Count of distinct product teams with ≥1 service at Stage 3+; 2) Source: Jira tracking under CT-HLT-OKR-Stability-Observability; 3) Quarterly targets: Q1: 3, Q2: 8, Q3: 15, Q4: 20 | Chad |

---

## What Changed — Row by Row

| Row | Current (V3) | Proposed | What Changed and Why |
|-----|-------------|----------|---------------------|
| 11 | Outcome B: three outcomes listed; KR C: "Deliver a generic, reusable business observability framework"; Measure D: same as KR; Methodology E: empty | Outcome B: "Reduce Incident Impact and Improve Recovery"; KR C: "Reduce time-to-business-impact to ≤15 min"; Measure D: unchanged; Methodology E: filled | 1) Outcomes reduced from three to two — "Strengthen Observability" and "Establish BOS Capability" merged because they describe the same thing; 2) KR changed from activity ("deliver framework") to measurable target ("reduce time-to-impact to ≤15 min"); 3) Methodology filled with Jira tracking and acceptance criteria |
| 12 | Measure D: unchanged; Methodology E: empty | Measure D: unchanged; Methodology E: filled | Methodology filled: criteria template published, PO-completed criteria count, Jira source |
| 13 | Measure D: unchanged; Methodology E: empty | Measure D: unchanged; Methodology E: filled | Methodology filled: methodology published, validated against ≥1 real service, Jira tracking |
| 14 | Was Row 14 under old KR1 with Measure D: "Reduce time-to-business-impact to ≤15 min"; Methodology E: empty | Now first row of KR2 with Outcome B: "Strengthen Observability and Establish BOS Capability"; KR C: "≥20 teams onboarded + ≥50 flows instrumented"; Measure D: "L3 leads identify top 3 flows by Q2"; Methodology E: filled | 1) Row 14's old Measure D content ("reduce to ≤15 min") moved up to be KR1 in Column C on Row 11; 2) This row now carries KR2 (adoption target); 3) Measure D is the gating input — L3 leads pick the flows before anything else happens; 4) Methodology filled with documented list and PO acknowledgment |
| 15 | Was Row 16 with Measure D: "Instrument ≥50 flows"; Methodology E: empty | Measure D: "Instrument identified flows with PO-defined signals"; Methodology E: filled | 1) Added "PO-defined" to clarify that signal types are determined by the business owner, not the platform team; 2) SLA adherence (previously standalone Row 18) integrated as one signal type among many; 3) Methodology filled with Stage 3 count, Jira source, quarterly targets 12/25/37/50 |
| 16 | Was Row 17 with Measure D: "Onboard ≥20 product teams to BOS"; Methodology E: empty | Measure D: "Onboard product teams with ≥1 service at Stage 3"; Methodology E: filled | 1) "Onboarded" now defined — ≥1 service at Stage 3 (signals live in production), not just "attended a session"; 2) Methodology filled with team count, Jira source, quarterly targets 3/8/15/20 |
| 17 | Was Row 18 with Measure D: "Visualize SLA adherence with ≥99.9% adherence visible" | Removed | SLA adherence integrated into Row 15 as one signal type. The ≥99.9% target is system reliability — BOS makes it visible, doesn't make it happen. Already tracked in Home Lending KPI tracker. |
| 18 | N/A | Removed | See Row 17 above. |

---

## What Changed — Column by Column

| Column | Change | Rationale |
|--------|--------|-----------|
| Outcomes (B) | Reduced from three to two. "Strengthen Observability and Alert Hygiene" and "Establish Business Observability Capability" merged into "Strengthen Observability and Establish Business Observability Capability." | The two outcomes described the same thing — BOS is the observability strengthening and establishing BOS is establishing the capability. Three outcomes produced three KRs where two were near-identical (flow count and team count measuring the same adoption progress). |
| Key Results (C) | 1) KR1: "Deliver a generic, reusable business observability framework" → "Reduce time-to-business-impact identification to ≤15 minutes for onboarded services by Q4"; 2) KR2: "L3 leads identify critical flows and team instruments them" → "≥20 product teams onboarded with ≥1 service at Stage 3 and ≥50 combined flows instrumented by Q4" | 1) Old KR1 was an activity ("deliver"). New KR1 is a measurable state change. This capability does not exist today — the target establishes a new standard; 2) Old KR2 was activities ("identify" and "instrument"). New KR2 is a combined adoption target with defined acceptance criteria. Team count (≥20) measures breadth. Flow count (≥50) measures depth. Both in one KR because 20 teams × 2-3 flows each ≈ 50 flows — they're coherent, not independent. |
| Strategic Measures (D) | 1) Rows 11-13 text unchanged — Q2 framework deliverables; 2) Row 14 now carries L3 lead identification (gating input for KR2); 3) Row 15 carries instrumentation work with SLA adherence integrated as one signal type; 4) Row 16 carries team onboarding with "onboarded" defined as Stage 3+; 5) Rows 17-18 removed | Column D was mostly correct as work items. Main fixes: define "onboarded" (Row 16), integrate SLA adherence as signal type not standalone measure (Row 15), remove standalone SLA row (Row 17/18). |
| Methodology (E) | All 6 cells filled. Data sources: 1) Jira with CT-HLT-OKR-Stability-Observability label; 2) incident bridge transcripts and postmortem records; 3) BOS onboarding artifacts | Was the largest methodology gap in the V3 spreadsheet. Every other group has methodology defined pointing to live systems. Chad's section was the only group with all cells empty. |
| Row count | 8 rows → 6 rows | Row 17/18 (SLA adherence) absorbed into Row 15 as one signal type. Onboarding target absorbed into KR2. |
| Quarterly milestones | Non-linear: Teams 3/8/15/20, Flows 12/25/37/50 | First quarter is slowest (building the process). Middle quarters accelerate. Linear milestones would create amber status in Q1 for a brand-new capability. |

---

## Open Decisions (Not Yet Resolved)

| Decision | Status | Impact |
|----------|--------|--------|
| **Dhruv / App Dev shared OKR** | Not yet finalized. KR2 instrumentation work may require App Dev to build queries against PO definitions. Previous work (Issue #75, one-pager v2) identified this as a shared OKR with Dhruv's App Dev team. | When finalized, App Dev may need to appear in the Assigned column for Row 15. Currently excluded until partnership is formalized. |
| **Quarterly milestone adjustment** | Current proposal: Teams 3/8/15/20, Flows 12/25/37/50. | Q1 actuals should be reviewed at end of quarter and milestones adjusted if the adoption curve differs from projection. |
