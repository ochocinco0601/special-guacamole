# Core Style Guide for Impactful Content – With Reusable Structural Examples
**Version:** 1.0  
**Last Updated:** 2025-08-08  

* **Plain, Direct Language:** Favor content that is clear, factual, and free of fluff. Replace abstract or vague terms with concrete examples the audience can immediately understand. Prefer short, active sentences that state facts directly. Avoid layered subordinate clauses that dilute clarity.  
  *Structural Example:* “Replace ‘optimize operational synergy’ with ‘reduce customer wait times.’” *(Follow the style of replacing an abstract term with a concrete, measurable example. Do not copy the topic.)*  
  `LLM Execution Note:` Always default to short, active sentences. If an abstract term is used, replace or pair it with a concrete, domain-relevant example.  

* **Strategic Use of Industry Terminology:** Use industry terms, like `Product Owner` or `functional requirements`, when they add precision and align with shared understanding. Avoid using them when they introduce ambiguity. On first use, pair the term with a brief definition or example to prevent misinterpretation.  
  *Structural Example:* “The `Service Owner` (the person accountable for its operation) approves changes before deployment.” *(Follow the style of pairing the term with a short, in-line definition. Do not copy the topic.)*  
  `LLM Execution Note:` When an industry term is introduced, add “(meaning: …)” or a short clarifying phrase the first time it appears in the output.  

* **Contrast-Driven Messaging:** Introduce new concepts by highlighting the difference between the traditional approach and the improved approach. Lead with contrast to create a mental anchor, then expand into specifics. Avoid burying contrasts mid-paragraph where they lose impact.  
  *Structural Example:* “Old: Manual report generation. New: Automated daily summary.” *(Follow the style of presenting an Old vs. New comparison before expanding. Do not copy the topic.)*  
  `LLM Execution Note:` When explaining a new idea, start with an “Old vs. New” sentence pair before expanding.  

* **Diagnostic and Revealing Content:** Use questions that expose unseen gaps in understanding, such as “how do you know the service is doing what it’s supposed to do?” Immediately follow a diagnostic question with a brief statement that frames the significance of the revealed gap.  
  *Structural Example:* “How do you know the process is running on time? This matters because late steps create cascading delays.” *(Follow the style of a diagnostic question plus immediate relevance statement. Do not copy the topic.)*  
  `LLM Execution Note:` After every diagnostic-style question, add one follow-up sentence beginning with “This matters because…”  

* **Structure That Guides:** Treat structure as a thinking tool, not just a container. Use progressive disclosure: start with a high-level principle, then progressively narrow to detail and measurable criteria. Organize content so the reader is led toward the intended conclusion.  
  *Structural Example:* “Principle: Processes must be predictable. Explanation: Predictable processes reduce waste. Example: Standardized meeting times. Measurement: Fewer schedule conflicts.” *(Follow the sequence: Principle → Explanation → Example → Measurement. Do not copy the topic.)*  
  `LLM Execution Note:` Structure outputs in a top-down order: Principle → Explanation → Example → Measurement/Criteria. Avoid skipping levels.  

* **Premise + Justification Structure:** Present reasoning as paired statements — a bold, concise premise followed by an italicized justification. Each pair should be self-contained so it can be reused independently. This structure creates a stepwise, self-evident logic arc that is easy to scan, hard to dispute, and ideal for reusable frameworks.  
  *Reusable Example:*  
  1. **Quality depends on verification.**  
     *Without verification, you can’t be certain work meets expectations.*  
  2. **Verification depends on clear criteria.**  
     *If the criteria aren’t defined, verification is subjective.*  
  *(Follow the style of premise + justification pairs. Do not copy the topic.)*  
  `LLM Execution Note:` When presenting reasoning, output in numbered premise + justification pairs. Each premise must be a standalone truth; each justification must connect it to an operational or business reality.  


# BOS-Specific Example Module – Parallel to Core Style Guide
**Version:** 1.0  
**Last Updated:** 2025-08-08  

**Domain Anchor:**  
**Business Observability System (BOS)** – A structured methodology for connecting technical monitoring to business outcomes, ensuring services are doing what the business needs them to do by defining, instrumenting, and validating business goals.  

---

* **Plain, Direct Language:** Favor content that is clear, factual, and free of fluff. Replace abstract or vague terms with BOS-relevant, concrete examples the audience can immediately understand. Prefer short, active sentences that state facts directly.  
  *BOS Example:* “Replace ‘improve operational alignment’ with ‘ensure the loan funding service completes by 8 AM each day.’”  

* **Strategic Use of Industry Terminology:** Use BOS-relevant terms, like `Product Owner`, `functional requirements`, or `ServiceNow incident`, when they add precision and align with shared understanding. Avoid using them when they introduce ambiguity. On first use, pair the term with a brief BOS context definition.  
  *BOS Example:* “The `Service Owner` (the person accountable for the loan funding service’s performance) reviews SLIs weekly.”  

* **Contrast-Driven Messaging:** Introduce BOS concepts by highlighting the difference between the traditional monitoring approach and the BOS-enabled approach. Lead with contrast to create a mental anchor, then expand into specifics.  
  *BOS Example:* “Old: Dashboard shows all systems green. New: Dashboard shows loan funding service missed its daily transaction volume target.”  

* **Diagnostic and Revealing Content:** Use questions that expose unseen gaps in BOS-related understanding, followed by a brief statement on why the gap matters.  
  *BOS Example:* “How do you know the home loan underwriting service is processing the expected volume? This matters because undetected slowdowns delay funding and impact customer deadlines.”  

* **Structure That Guides:** Treat BOS structure as a thinking tool. Use progressive disclosure: start with a high-level BOS principle, then progressively narrow to detail and measurable criteria.  
  *BOS Example:* “Principle: Loan funding readiness must be known at the start of day. Explanation: Readiness ensures same-day closings. Example: Funding dashboard shows transactions processed vs. target. Measurement: 100% of expected transactions completed by 8 AM.”  

* **Premise + Justification Structure:** Present BOS reasoning as paired statements — a bold, concise premise followed by an italicized justification. Each pair should be self-contained so it can be reused independently.  
  *BOS Example:*  
  1. **Readiness requires transaction completion.**  
     *If transactions are not processed on time, the service cannot support same-day closings.*  
  2. **Transaction completion requires real-time monitoring.**  
     *Without real-time visibility, delays are detected too late to mitigate.*  
