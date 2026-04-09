# Documentation Design — Professional Disciplines

Expert perspectives for creating, structuring, and evaluating documentation.

---

## Daniele Procida — Diataxis

**Source:** diataxis.fr (open framework); adopted by Django, Canonical, Cloudflare

### Core Framework — Four Types (Do Not Mix)

| Type | Orientation | Reader Mode | Key Rule |
|------|------------|-------------|----------|
| **Tutorial** | Learning | Following | Take reader through steps to complete a project. Learning by doing. |
| **How-To** | Task | Working | Solve a specific problem. Assume competence. No teaching. |
| **Reference** | Information | Working | Describe the machinery. Austere, accurate, complete. |
| **Explanation** | Understanding | Learning | Clarify and illuminate. Discuss alternatives, history, context. |

### Application Checklist
- [ ] Is this document clearly one type, or does it mix types?
- [ ] Does the reader mode match the content? (doing vs understanding)
- [ ] Are all four types covered across the documentation set?

---

## Robert Horn — Information Mapping

**Source:** IEEE (1993); Information Mapping methodology (1960s-1970s)

### Core Principles — Seven Rules of Structured Writing
1. **Chunking** — group information into small blocks (max ~7±2 sentences)
2. **Relevance** — each block contains ONLY information related to its single point
3. **Labeling** — every block gets a short descriptive label (3-5 words)
4. **Consistency** — similar information types get similar structure and formatting
5. **Integrated graphics** — illustrations accompany text where they aid understanding
6. **Accessible detail** — provide multiple levels of detail the reader can navigate
7. **Hierarchy of chunking** — blocks into maps, maps into sections, labels at each level

### Application Checklist
- [ ] Is every section chunked into scannable blocks with labels?
- [ ] Does each block contain exactly one main point?
- [ ] Are similar information types structured consistently throughout?
- [ ] Can a reader navigate to the level of detail they need?

---

## John Carroll — Minimalism

**Source:** *The Nurnberg Funnel* (MIT Press, 1990)

### Core Principles
1. **Action-oriented** — get users doing real tasks immediately; don't front-load concepts
2. **Anchor in the task domain** — frame everything in terms of what the user is trying to accomplish, not product features
3. **Support error recovery** — errors are teachable moments; help users recognize and recover, don't try to prevent all errors
4. **Support multiple reading strategies** — people scan, skip, and jump; support reading-to-do, reading-to-study, and reading-to-locate

**Foundational insight:** The people who most need documentation are the least likely to use it. Accommodate this behavior.

### Application Checklist
- [ ] Does the reader do something within the first few paragraphs?
- [ ] Is content framed around user tasks, not product features?
- [ ] Are error recovery paths included (not just happy paths)?
- [ ] Can a reader skip ahead and still orient themselves?

---

## Mark Baker — Every Page is Page One (EPPO)

**Source:** *Every Page is Page One* (XML Press, 2013)

### Core Principles — Seven EPPO Requirements
1. **Self-contained** — each topic has everything needed for its purpose
2. **Specific purpose** — one clear, bounded purpose per topic
3. **Conforms to a type** — topic types are subject-specific, not generic
4. **Establishes context** — reader can arrive from anywhere and quickly orient
5. **Assumes qualified reader** — don't explain prerequisites inline; link to them
6. **Stays on one level** — don't dive into sub-topics or rise to overviews within a topic
7. **Links richly** — topics connect along lines of subject affinity

### Application Checklist
- [ ] Could a reader arrive at this page from search and understand where they are?
- [ ] Does the topic have one clear purpose (not a general dump)?
- [ ] Are prerequisites linked rather than explained inline?
- [ ] Does it stay on one level (no diving or climbing)?

---

## IBM — Developing Quality Technical Information (DQTI)

**Source:** Carey et al., *Developing Quality Technical Information* (IBM Press, 3rd ed. 2014)

### Core Framework — Nine Quality Characteristics

**Easy to Use:** task orientation, accuracy, completeness
**Easy to Understand:** clarity, concreteness, style
**Easy to Find:** organization, retrievability, visual effectiveness

### Application Checklist
- [ ] Is content organized around user tasks, not product structure? (task orientation)
- [ ] Is every statement correct and current? (accuracy)
- [ ] Is meaning unambiguous on first reading? (clarity)
- [ ] Are examples concrete and specific, not abstract? (concreteness)
- [ ] Can users find specific information through TOC/search/cross-references? (retrievability)
- [ ] Does layout guide the eye and signal structure? (visual effectiveness)

---

## Anne Gentle — Docs as Code

**Source:** *Docs Like Code* (2017); docslikecode.com

### Core Principles
1. **Version control** — docs live in Git alongside code
2. **Plain text source** — Markdown, AsciiDoc, or reStructuredText
3. **Pull request reviews** — documentation changes go through code review
4. **Automated testing** — link checking, style linting in CI/CD
5. **Continuous deployment** — docs build and publish automatically on merge

**Key insight:** The biggest documentation problem isn't writing quality — it's that docs are perpetually out of date because the update workflow is separate from the development workflow.

### Application Checklist
- [ ] Is documentation in version control?
- [ ] Can engineers contribute directly using tools they already know?
- [ ] Are broken links and style issues caught automatically?
- [ ] Does publishing happen automatically on merge?

---

## Ferri-Benedetti — Seven-Action Documentation Model

*Emerging framework — blog-sourced (2025), not yet peer-validated through publication. Useful as a Diataxis complement but does not have the establishment credentials of other entries in this catalog.*

**Source:** passo.uno/seven-action-model/ (2025)

### Core Framework — Seven User Actions
1. **Appraise** — evaluate whether this product is right for them
2. **Understand** — build a mental model of how the system works
3. **Explore** — discover capabilities and possibilities
4. **Practice** — build skill through guided practice
5. **Remember** — look up specific details they once knew
6. **Develop** — build on top of or integrate with the system
7. **Troubleshoot** — diagnose and fix problems

**Complement to Diataxis:** Descriptive (what user needs exist) rather than prescriptive (what document types to create). A single document can serve multiple actions.

### Application Checklist
- [ ] Which of the seven user actions does this documentation serve?
- [ ] Are any actions underserved across the documentation set?
- [ ] Has the "Appraise" action been considered? (often missing — users need to evaluate before committing)

---

## Cross-Reference: Problem → Framework

| Documentation Problem | Primary Framework(s) |
|----------------------|---------------------|
| What types of docs to write? | Diataxis, Seven-Action Model |
| How to structure each document? | Information Mapping, DQTI |
| How to write clearly? | Plain Language (see `content-design.md`), DQTI |
| How to design individual topics? | EPPO, Minimalism |
| How to organize the whole doc set? | IA (see `information-architecture.md`), Diataxis |
| How to keep docs current? | Docs as Code |
| How to evaluate documentation quality? | DQTI (nine characteristics as rubric) |

---

## Cross-References

| When also doing... | Load... |
|-------------------|---------|
| Organizing the doc set's navigation/taxonomy | `information-architecture.md` |
| Writing content for specific audiences | `content-design.md` |
| Building documentation UI/reader experience | `ux-interaction-design.md` |
| Including data displays in documentation | `data-visualization.md` |
