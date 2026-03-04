# Stability OKR Talking Points — HLT Platform Ops Team Meeting

**Date:** 2026-03-04
**Context:** 2-3 minute section covering Stability OKRs at team meeting
**Approach:** "Last year we experienced X → here's what we're doing about it → here's where we're headed"

---

## KR1/KR2 — Business Observability

"Last year we saw issues with the funding service around wire transfers — and one of the things that was hard to answer quickly in those moments was 'what's the business impact?' How many wires are affected, who's waiting, what's the downstream exposure. That's what business observability is solving for — getting that answer within 15 minutes.

To get there, Product Owners document what matters about their services — who's affected, what they expect, what 'broken' means in business terms — and then we instrument those flows with health signals. The framework to do that is being delivered Q2.

We have hundreds of business apps, 30-plus start-of-day flows. The obstacle isn't figuring out which ones matter — they all matter. It's just getting started. Once we get the first few through the pipeline, the pattern repeats."

## KR3 — Change Management

"Last year one of the challenges was the volume and variety of change reviews — different types of changes across a large portfolio, and keeping up with all of them. Natraj has built an analytics dashboard that gives us visibility into incident themes, change causes, and categorization — that's how we identify where the opportunities are. Change success rate is running above goal at 99.8%. The direction is using GenAI to help standardize and scale those reviews, and drive down emergency and unsuccessful changes by 50% year-over-year."

## KR4 — Postmortem & RCA

"Last year, tracking problems and root causes meant someone going into ServiceNow and manually stitching it together. Same way we want dashboards showing the health of a service and its alerts, we need that visibility into problem management — tracking problems, root causes, and whether fixes are actually preventing recurrence. This year is about building on that effort — centralizing the process and getting that picture without the manual work."
