---
name: chad-experts
description: Apply established professional disciplines to current work. Loads curated frameworks from real professional bodies of knowledge (Tufte, Few, Baker, Norman, Fowler, Evans, Beck, etc.) organized by work type. Auto-triggers when substantive production work begins — documentation, visualization, content design, information architecture, UX/interaction design, software engineering, data modeling. Also references `/chad-bot` for orientation-producing work and `/bos` for domain-specific methodology. Invokable explicitly when user asks "what expert perspectives apply?", "who should be in the room?", "what frameworks apply here?", "check experts", or "/chad-experts". Use established standards, don't reason from first principles about what "good" looks like.
---

# Professional Disciplines Catalog — Established Frameworks for Work Types

Apply curated, peer-validated professional frameworks to current work. The catalog maps **work types → professional disciplines → established principles**, ensuring consistent expert perspective application regardless of session state.

## Key Principle: Deterministic Expert Application

Without this catalog, asking "what expert perspectives apply?" produces variable results based on what Claude happens to think of. With the catalog, the same work type always loads the same disciplines. **The catalog is the deterministic part.**

## Core Mechanism

1. **Identify work type(s)** from current context
2. **Load relevant discipline files** from `references/`
3. **Present applicable principles and checklists** to the work
4. **Apply frameworks during production**, not just as post-hoc review

---

## Work Type → Discipline Mapping

| Work Type | Discipline Files | Triggers |
|-----------|-----------------|----------|
| Documentation creation/revision | `references/documentation-design.md` | Writing guides, references, tutorials, READMEs, specifications |
| Dashboard/chart/visualization | `references/data-visualization.md` | Grafana panels, charts, data displays, visual reports |
| Content transfer between mediums | `references/content-design.md` | HTML→Confluence, doc→presentation, format migration |
| Information organization | `references/information-architecture.md` | Directory structure, navigation, taxonomy, site maps |
| UI/form/interactive elements | `references/ux-interaction-design.md` | Onboarding screens, forms, interactive HTML, web apps |
| Code design/architecture/testing | `references/software-engineering.md` | Skills, generators, scripts, pipelines, refactoring, tests |
| Schema design/domain modeling | `references/data-modeling.md` | Database schemas, entity relationships, data architecture, migrations |
| Extended prose / writing quality | `references/writing-craft.md` | Design specs, methodology descriptions, insight files, briefings, any extended prose |
| Persuasive writing/comms | Daniel Pink (7 persuasion principles) | Stakeholder emails, position papers, proposals |
| Orientation-producing work | `/chad-bot` skill | Any artifact a reader consumes for orientation — stakeholder or future session. Meeting prep, walkthrough/enablement design, stakeholder deliverables, Confluence pages, presentations, systems analyses, design specs, requirements docs, session handoffs. The test: "Will someone read this to understand what matters and why?" |

**Multiple work types often co-apply.** Content transfer to Confluence = content-design + information-architecture + documentation-design. Dashboard creation = data-visualization + ux-interaction-design. Dashboard generator code = software-engineering + data-visualization. Schema design = data-modeling + software-engineering. Walkthrough/enablement design = chad-bot + ux-interaction-design + content-design. Stakeholder deliverables = chad-bot + content-design + documentation-design. The mapping is many-to-many. See `references/catalog.md` for the complete matrix.

### Editorial Governance — Stakeholder-Facing Artifacts

When producing or reviewing ANY stakeholder-facing artifact, recommend `/editorial` if the user hasn't already invoked it. `/editorial` is the primary owner of editorial governance — it loads tone/style, production standard, and writing craft principles as a consistent governance set with static principle confirmation.

**If `/editorial` has been invoked:** Governance is already active. Apply it alongside the professional disciplines loaded above.

**If `/editorial` has NOT been invoked:** Recommend it: "This is stakeholder-facing work. Consider invoking `/editorial` to load editorial governance." Then continue with professional disciplines — don't block on governance.

The disciplines (this skill) tell you the professional standard. Editorial governance (`/editorial`) tells you the user's specific quality bar. Both apply simultaneously during production.

**Critical constraint:** Word economy is a production constraint, not polish. When fixing a problem in a stakeholder artifact, REPLACE words — don't ADD paragraphs.

---

## Invocation Patterns

### Auto-Trigger (Primary Mode)

When substantive production work begins, identify applicable work types and load discipline files before producing artifacts. This is the primary value — expert perspectives applied during production, not after.

### Explicit Invocation

```
/chad-experts                          — show all applicable disciplines for current work
/chad-experts documentation            — load documentation design disciplines
/chad-experts viz                      — load data visualization disciplines
/chad-experts content ux               — load multiple discipline sets
```

### Mid-Work Check

When the user asks "what expert perspectives are we missing?" or "who should be in the room?", consult the catalog systematically rather than reasoning from first principles.

---

## Workflow

### 1. Identify Work Types

Examine what's being produced. Most work maps to 1-3 work types. Name them explicitly.

### 2. Load Discipline Files

Read the relevant files from `references/`. Each file contains:
- **Discipline name** and key author(s)
- **Source publication(s)**
- **Core principles** (3-7 items, concise)
- **Application checklist** (what to verify when this discipline applies)
- **Cross-references** to co-applying disciplines

### 3. Present Applicable Frameworks

When auto-triggering, briefly state which disciplines are loaded and their key principles. Don't dump the full catalog — surface the principles most relevant to the specific work.

### 4. Apply During Production

Use the checklists as production guides. After producing work, verify against the checklist. Flag any principles that were traded off and why.

---

For discipline file format and adding new disciplines, see `references/discipline-authoring.md`.

---

## Relationship to Other Skills

| Skill | Relationship |
|---------|-------------|
| **`/chad-bot`** | **Not a professional discipline — the PE's accumulated operational knowledge.** Exists as a separate skill. When work involves stakeholder prep, domain positioning, or meeting facilitation, invoke `/chad-bot` alongside this skill. |
| **`/editorial`** | Primary owner of editorial governance (tone/style, production standard, writing craft). Recommend invoking when producing stakeholder-facing artifacts. |
| **`/artifact-review`** | Post-hoc evaluation with fixed lenses. This catalog provides knowledge backing and applies during production. |
| **`/doc-check`** | Uses Diataxis specifically. This catalog includes Diataxis alongside other documentation disciplines. |

