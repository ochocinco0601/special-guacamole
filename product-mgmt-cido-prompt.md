# 📦 prompt-cido-problem.md  
Modular, LLM-ready prompt for defining structured problem statements using the CIDO framework (Context, Issue, Downside, Opportunity).  
Designed for use in upstream discovery for BOS Factory and complex initiatives.

---

## 📘 OVERVIEW

This prompt helps clarify **why a product, feature, or system improvement matters** — before defining what to build.  
It generates a structured **CIDO-framed problem statement** that aligns stakeholders, prevents misalignment, and links downstream work (like flows, specs, signals) to meaningful business goals.

Use it to:
- Validate the “why” before the “what”
- Anchor observability, KPI, or dashboard design in real outcomes
- Make proposals more credible and traceable

---

## 🛠️ HOW TO USE THIS PROMPT

Paste this full prompt into an LLM. Then choose how you'd like to proceed:

- ✅ **One-Shot Mode**: Provide all relevant background and have the LLM generate the full CIDO output.  
- 🧭 **Guided Mode**: Let the LLM walk you through each of the four CIDO components with targeted questions.

Use flags for ambiguity:
- `Assumption:` → Reasonable default filled in by LLM  
- `Unclear:` → Input required or needs SME follow-up

---

## 📄 Output Table

| Section | Description |
|---------|-------------|
| **Context** | _The situation, environment, or background framing the problem. What system, business unit, or operational reality does this exist within?_ |
| **Issue** | _The specific problem, friction point, failure mode, or gap. Avoid jumping to solutions — describe what’s broken or insufficient._ |
| **Downside** | _The risk or consequence if the issue is not addressed. What gets worse, goes wrong, or loses value?_ |
| **Opportunity** | _The potential benefit or value of solving this. Who gains what — and how might this tie to strategy, metrics, or improved outcomes?_ |

---

## 📚 Reference Sections

---

### 📘 Reference A: What Makes a “Good” CIDO Statement?

A high-quality CIDO has these traits:
- **Context** is specific, not vague (e.g., “in our loan doc processing queue” vs “in the business”)
- **Issue** describes the problem *without* jumping to “we should do X”
- **Downside** is credible and relevant to a real stakeholder or system (e.g., SLA breach, compliance miss, poor UX, Ops burden)
- **Opportunity** ties to outcomes or capabilities that matter (e.g., faster decisions, reduced rework, increased clarity, enabled signals)

CIDO is not about fancy wording — it’s about traceable logic.

---

### 📘 Reference B: Examples of CIDO Statements

#### Example 1: Observability Gap

| Section | Description |
|---------|-------------|
| **Context** | Home Lending document delivery process includes multiple system handoffs with asynchronous APIs. |
| **Issue** | There is no signal when a document generation request silently fails or stalls in the print vendor queue. |
| **Downside** | If documents are not mailed within 3 days, we risk regulatory SLA breaches and customer dissatisfaction. |
| **Opportunity** | Adding an observable handoff signal allows proactive alerting, SLA compliance, and higher confidence in downstream status dashboards. |

#### Example 2: Operational Bottleneck

| Section | Description |
|---------|-------------|
| **Context** | Internal analysts must reconcile trade confirmations daily in our capital markets workflow. |
| **Issue** | The current reconciliation UI doesn’t show root cause of mismatches, increasing manual review time. |
| **Downside** | This creates delay risk in trade settlement, with potential reputational and financial exposure. |
| **Opportunity** | Enhancing UI with automated mismatch classification could reduce analyst effort and settlement delay risk. |

---

### 📘 Reference C: Guided Mode – Suggested Questions

To use this prompt interactively, ask the following:

1. **Context:**  
   - What system, team, or workflow does this take place in?  
   - What’s happening around the issue that helps us understand its environment?

2. **Issue:**  
   - What is the specific problem, inefficiency, or gap?  
   - Is anything broken, missing, or invisible?

3. **Downside:**  
   - If nothing changes, what gets worse or goes wrong?  
   - Who is impacted, and how?

4. **Opportunity:**  
   - What value could be created by solving this?  
   - Could it improve customer experience, reduce risk, save time, or surface better signals?

---

## ✅ Next Steps

After generating your CIDO statement:
- Review with stakeholders to validate shared understanding  
- Feed into `prompt-process-flow` to structure the flow  
- Use `Downside` and `Opportunity` to flag KPIs or SLA relevance  
- Use `Issue` to inform scope boundaries in `prompt-feature-spec`

---


---

### 📘 Reference D: CIDO-Lite (Quick Framing Format)

Use this when you need a fast, lightweight version of CIDO for early discussions, idea review, or stakeholder check-ins.

| Field | Prompt |
|-------|--------|
| **What’s happening?** | (Give a quick description of the system, process, or environment) |
| **What’s the problem?** | (Describe the specific issue or failure mode) |
| **Why does it matter?** | (Describe the risk or pain if nothing changes) |
| **What’s possible if we fix it?** | (Briefly name the value, impact, or capability unlocked) |

#### 🔄 Example (same scenario as earlier)

- **What’s happening?**  
  Document delivery system relies on third-party print vendor.

- **What’s the problem?**  
  No alert is triggered when delivery confirmation is missing.

- **Why does it matter?**  
  We risk SLA violations and compliance fines.

- **What’s possible if we fix it?**  
  Add a missing signal + alert, protect SLA and customer trust.

Use CIDO-Lite in hallway conversations, idea grooming, or early-stage problem surfacing. You can always convert it to full CIDO later.

---


