# Professional Disciplines Catalog

Master index mapping work types to established professional disciplines. Ensures consistent, deterministic expert perspective application.

## Work Type → Disciplines

| Work Type | Discipline File | Key Frameworks |
|-----------|----------------|----------------|
| Documentation | `references/documentation-design.md` | Diataxis, Information Mapping, Minimalism, EPPO, DQTI, Docs as Code |
| Data Visualization | `references/data-visualization.md` | Tufte, Few, Bertin, Cleveland & McGill, Cairo, Knaflic, Ware, Brewer |
| Content Design | `references/content-design.md` | Richards, Halvorson, Kissane, McGovern, Hane/Atherton, Plain Language |
| Information Architecture | `references/information-architecture.md` | Morville/Rosenfeld, Wurman LATCH, Klyn, Covert, Resmini/Rosati |
| UX / Interaction Design | `references/ux-interaction-design.md` | Norman, Nielsen, Krug, Shneiderman, Garrett, Gestalt, Cognitive Load |
| Software Engineering | `references/software-engineering.md` | Martin (SOLID/Clean), Fowler, Beck (TDD), Evans (DDD), GoF, Metz, Humble/Farley (CD), DORA |
| Data Modeling | `references/data-modeling.md` | Chen (ER), Evans (DDD), Kimball, Inmon, Codd, Hay, Silverston |
| Writing Craft | `references/writing-craft.md` | Gopen & Swan, Williams, McEnerney, Pinker, Zinsser |
| Persuasive Communication | Daniel Pink | 7 persuasion principles |
| Communication Style (motivating action) | Nate B Jones | Framework building, provocative reframing, concrete-before-abstract, escalating altitude |
| Communication Style (building conviction) | Dave Farley (style) | Logical chains, theory grounding, career evidence, precise problem statements, calm authority |
| chad-bot | `/chad-bot` skill | Field-tested communication methodology. Progressive disclosure + objection handling, audience-specific architectures, formulations, PE heuristics. Invoke as separate skill. |
| Systems Thinking | Meadows, Senge | See `/systems-analysis` skill |
| Engineering Discipline | Dave Farley | Learning + complexity management |
| Value / Strategy / Positioning | Porter, Goldratt (TOC), Christensen (JTBD), Rumelt | See `/value-analysis` skill |

## Co-Application Patterns

Common work scenarios that require multiple discipline sets:

| Scenario | Disciplines to Load |
|----------|-------------------|
| Confluence page creation | Content Design + Information Architecture + Documentation |
| Dashboard development | Data Visualization + UX/Interaction Design |
| Dashboard generator code | Software Engineering + Data Visualization |
| Onboarding screen design | UX/Interaction Design + Content Design + Documentation |
| Stakeholder deliverable | Persuasive Communication + Communication Style + Documentation + Content Design + chad-bot |
| Presentation / talk prep | Communication Style + Persuasive Communication + Content Design + chad-bot |
| Meeting prep | chad-bot + Persuasive Communication + Communication Style |
| Domain content / Confluence | chad-bot + Content Design + Documentation |
| Walkthrough / enablement design | chad-bot + UX/Interaction Design + Content Design |
| Repository restructuring | Information Architecture |
| Interactive HTML artifact | UX/Interaction Design + Documentation |
| Schema design / migration | Data Modeling + Software Engineering |
| Skill / protocol creation | Software Engineering + Documentation |
| Pipeline / build tooling | Software Engineering |
| Methodology artifacts | Documentation + Content Design + Data Modeling |
| Data model documentation | Data Modeling + Documentation + Data Visualization |
| Visualization prompt (stakeholder) | chad-bot + Data Visualization + Communication Style |
| Visualization prompt (technical) | Data Visualization |
| AI strategy / value positioning | Value Reasoning + Systems Thinking |
| External knowledge extraction | Relevant domain disciplines |
| Stakeholder value communication | Value Reasoning + Persuasive Communication + Communication Style |
| Domain value articulation | Value Reasoning + chad-bot |

## Catalog Maintenance

This catalog grows when work reveals missing professional perspectives. The pattern:
1. "I should have thought of that" → identify the discipline
2. Verify it's established (published, peer-validated)
3. Add to relevant discipline file
4. Update this index
