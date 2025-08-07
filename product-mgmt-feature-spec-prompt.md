# 📦 prompt-feature-spec-v2.3.md
**Reusable, modular prompt for documenting a feature, capability, or system function at scale. Designed for large initiatives like BOS Factory.**

---

## 📘 OVERVIEW

This prompt generates a complete 12-section **feature specification** for a complex feature, system capability, or cross-functional initiative.

It supports:
- **Large-scale systems** (e.g., observability platforms, orchestration layers)
- **Business-impacting features** (e.g., compliance validation, risk scoring)
- **Reusable system components** (e.g., signal mappers, traceability tools)

The output is structured, audit-friendly, and supports traceability, downstream implementation, and stakeholder alignment.

---

## 🛠️ HOW TO USE THIS PROMPT

Paste this full prompt into your LLM.

Then choose one of two modes:

### ✅ One-Shot Generation:
> “You have the context. Generate the full 12-section feature spec in one go.”

### 🧭 Guided Mode (recommended for iterative work):
Start with:
> “Let’s work through this one section at a time. Ask me questions to gather the needed context.”

### 🔖 Interactive Flags:
If anything is unclear or missing, the LLM will use inline flags:
- `Assumption:` → model is inferring based on context
- `Unclear:` → ambiguity or risk noted

---

## 🧩 PRIMARY PROMPT (What the LLM Executes)

You have full access to the product documentation, design artifacts, and business context for **[Product Name or Initiative]**.  
Act as a **senior product manager** and generate a comprehensive feature specification for a **complex feature, system capability, or cross-team initiative** named **[Feature or Capability Name]**.

If any required information is missing or unclear:
- Use inline flags (`Assumption:` / `Unclear:`) as described below
- Do **not leave any sections blank** — offer your best guess or placeholder

Optionally, specify a `Step Type` or `System Type` to tailor output focus (see Reference A).

---

### 📄 Deliverable: 12-Section Feature Specification

1. **Feature Title**  
2. **Executive Summary**  
3. **Problem Statement**  
4. **Goals and Success Metrics**  
5. **Scope (In/Out)**  
6. **Solution Overview** *(include assumptions or open questions)*  
7. **Feature Breakdown** *(break into modular units if applicable)*  
8. **Acceptance Criteria** *(in GIVEN–WHEN–THEN format)*  
9. **Dependencies and Risks**  
10. **Test Scenarios**  
11. **Rollout Plan**  
12. **Sustainability and Monitoring**

---

## 📚 Reference Sections

---

### 📘 Reference A: Step Type & System Type (Optional Classifications)

Use these tags to guide assumptions around KPIs, observability, and testing focus.

#### Step Type
- `Execution` — performs a business action
- `Validation` — checks correctness or policy
- `Fulfillment` — completes a transaction or handoff
- `Orchestration` — coordinates other components

#### System Type
- `API Service` — backend logic, request/response
- `UI Frontend` — user-facing interface
- `Workflow Orchestrator` — controls step sequencing
- `Data Pipeline` — ingestion, transformation, storage
- `Monitoring Component` — logs, metrics, signals

---

### 📘 Reference B: Assumption & Unclear Flagging

| Tag | When to Use | Format Example |
|-----|-------------|----------------|
| `Assumption:` | You are inferring a missing value based on context | *Assumption: The nightly batch is triggered by a control system upstream.* |
| `Unclear:` | The documentation or ownership is ambiguous | *Unclear: System B's retry behavior is not clearly documented.* |

> ✅ Place flags inline where the assumption occurs, not as footnotes.

---

## ✅ Next Steps

After generating or reviewing the spec, you can:
- Extract sub-prompts (e.g., dashboard mockups, template validations)
- Generate traceability tables
- Draft rollout comms or change tickets

This feature spec becomes your **source of truth** for aligning Product, Dev, SRE, and Business.

---


