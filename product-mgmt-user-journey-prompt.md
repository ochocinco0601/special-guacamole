# 📦 prompt-process-flow-v1.md  
Modular, LLM-ready prompt to generate clear, traceable **user journeys** or **process flows** during the Discovery & Research phase of product development.  
Designed for complex systems including BOS Factory.

---

## 📘 OVERVIEW

This prompt helps define a **step-by-step sequence** of user behavior or system/business logic for a product, capability, or service.

Use it to create:
- High-quality discovery-phase artifacts
- Inputs to BOS templates, signal mapping, or dashboard planning
- Structured alignment across Product, Engineering, and SRE

---

## 🛠️ HOW TO USE THIS PROMPT

Paste this full prompt into an LLM (e.g., ChatGPT or Claude). Then choose:

---

### 🟦 Mode 1: **User Journey**
Use this mode to document the experience of a human user (e.g., customer, internal analyst, underwriter) as they interact with a product or service.

> Focus on **goals, actions, decisions, emotions, and pain points**.

- Examples:  
  - “Customer applies for a loan and signs disclosures”  
  - “Loan Officer uploads documents and reviews errors”

---

### 🟧 Mode 2: **Process Flow**
Use this mode to document **system-level or business-entity-driven logic**, including multi-system automation, compliance steps, and internal handoffs.

> Focus on **logic, systems, triggers, and business outcomes**.

This includes:
- System-to-system interactions (APIs, queues, retries)
- Automated or SLA-bound steps
- Business-entity–centric flows (e.g., lifecycle of a loan, claim, trade, or document)

---

Then choose how you'd like to proceed:

- ✅ **One-Shot Mode**: "Generate the full output at once."  
- 🧭 **Guided Mode**: "Ask me questions step-by-step."

Use inline flags when input is unclear:
- `Assumption:` → Inferred based on context
- `Unclear:` → Ambiguity or missing SME input

---

## 📄 Output Tables

---

### 🟦 Output Table for User Journey

| Step | Step Name | Goal or Task | User Role | Tool or Interface | Decision or Friction Point | Outcome |
|------|-----------|--------------|-----------|--------------------|-----------------------------|---------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

---

### 🟧 Output Table for Process Flow (with Business Entity)

| Step | Step Name | Description | Actor | System | Business Entity | Trigger / Condition | Outcome |
|------|-----------|-------------|-------|--------|------------------|----------------------|---------|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

---

## 📚 Reference Sections

---

### 📘 Reference A: What Counts as a “Good” Step?

Each step should:
- Have a clear trigger or input
- Perform **one** business or system action
- Be performed by a specific actor (person, service, team)
- Produce a measurable outcome or decision
- Avoid vague phrases like “system does something” or “user reviews”

---

### 📘 Reference B: Actor Types

| Actor Type | Examples |
|------------|----------|
| Human | Customer, Analyst, Loan Officer |
| System | API, Workflow Engine, Scheduler |
| Hybrid | Orchestrator, Notification System |

---

### 📘 Reference C: Common Triggers and Outcomes

| Trigger | Outcome |
|---------|---------|
| User submits form | Data validated |
| File uploaded | Parsing initiated |
| SLA timer expires | Alert triggered |
| Doc sent | Status updated |

---

### 📘 Reference D: Entity-Centric Process Flow (Definition Card)

#### 🧩 What It Is
An **Entity-Centric Process Flow** models the lifecycle of a **business entity** (e.g., loan, trade, document) as it moves through steps — often automated, regulated, or system-driven.

These flows focus on:
- What *must happen* to the entity
- Which systems or teams are involved
- What business outcome or SLA must be satisfied

#### 🧠 When to Use It
Use this when:
- The business cares about **what happens to the entity**, not just the user
- Many steps are **automated** or **compliance-based**
- There’s a clear start → end lifecycle (e.g., Loan Created → Documents Generated → Delivered)

#### 📌 Examples

| Entity | Flow Goal | Sample Steps |
|--------|-----------|--------------|
| Loan | Ensure docs are delivered | Generate → Mail → Confirm |
| Trade | Ensure settlement | Match → Confirm → Settle |
| Case | Ensure resolution | Triage → Review → Close |

#### 📐 Key Fields

| Field | Notes |
|-------|-------|
| `Step Name` | Business logic label |
| `Business Entity` | Object under transformation |
| `Trigger` | What initiates the step |
| `Outcome` | What happens to the entity |

#### 🔧 BOS Alignment
- Feeds directly into BOS Templates  
- Supports Signal Design  
- Enables traceability across Ops, Dev, and Risk

---

### 📘 Reference E: One-Shot Input Examples

#### 🟦 Mode: User Journey

```plaintext
Context:
We are modeling the user journey for a customer applying for a home loan using the public-facing mortgage portal. The goal is to understand what steps the customer takes from login to receiving confirmation that their loan application is submitted.

Details:
- The customer applies on their own.
- They log in, start a new loan, complete sections, upload documents.
- System validates each section.
- Errors are shown in real-time.
- User submits and receives confirmation.

Please model this as a structured user journey.
```

#### 🟧 Mode: Process Flow

```plaintext
Context:
We are modeling the automated process that begins when a loan is marked “Ready for Document Generation.” This supports legal/regulatory compliance.

Details:
- Entity: Loan
- Trigger: Loan marked "Ready for Docs"
- Systems: Doc generator, print/mailer, delivery monitor
- Flow: Generate → Send to vendor → Confirm delivery
- Exception: If no delivery confirmation in 72h, escalate to Ops

Please model this as a system-level process flow.
```

---

### 📘 Reference F: Guided Mode – Suggested Questions

#### 🟦 Mode: User Journey

1. What is the user’s goal or task?
2. What is the first action the user takes?
3. What is the user’s role?
4. What tool or interface do they use?
5. Are there decisions or pain points at this step?
6. What is the expected outcome?
7. (Optional) What systems are triggered?

#### 🟧 Mode: Process Flow

1. What process or system are we modeling?
2. What business entity is involved?
3. What triggers the first step?
4. Who or what system performs the step?
5. What happens to the entity?
6. What is the state change or outcome?
7. What is the next step and its trigger?
8. Are there any failure or escalation paths?

---

## ✅ Next Steps

After generating the flow:
- Use each step as input for a **BOS Observability Template**
- Assign signal types: Business / Process / System
- Define ownership and KPIs
- Design alert routing or dashboard panels per flow segment

---


