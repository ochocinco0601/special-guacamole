# Data Modeling — Professional Disciplines

Expert perspectives for schema design, domain modeling, entity relationships, and data architecture.

---

## Peter Chen — Entity-Relationship Model

**Source:** "The Entity-Relationship Model — Toward a Unified View of Data" (1976, ACM TODS)

### Core Principles
1. **Entities** — things that exist and are distinguishable (have identity)
2. **Relationships** — associations between entities with defined cardinality (1:1, 1:N, M:N)
3. **Attributes** — properties that describe entities and relationships
4. **ER Diagrams** — visual representation of the data model as a communication tool between stakeholders and implementers

**The foundational insight:** Separate the conceptual data model (what exists and how it relates) from the physical implementation (tables, columns, indexes). Design the model first, implement second.

### Application Checklist
- [ ] Are entities identified by what they ARE, not by how they're stored?
- [ ] Are relationships explicitly named with cardinality?
- [ ] Is the conceptual model documented independently of the physical schema?
- [ ] Can a domain expert read the ER diagram and validate it?

---

## Eric Evans — Domain-Driven Design (Data Perspective)

**Source:** *Domain-Driven Design* (2003); Vaughn Vernon — *Implementing Domain-Driven Design* (2013)

### Core Principles for Data Modeling
1. **Ubiquitous Language** — the data model's names must match the domain language exactly; if the domain says "Service" and the schema says "component", that's a bug
2. **Bounded Contexts** — different parts of the system may model the same real-world concept differently; this is correct, not a mistake
3. **Aggregates** — define transactional consistency boundaries; an aggregate root controls access to its children
4. **Value Objects** — defined by their attributes, not identity; immutable; two value objects with the same attributes are equal
5. **Entities** — defined by identity that persists through state changes
6. **Anti-Corruption Layer** — when integrating with external systems, translate at the boundary; don't let their model pollute yours

### Application Checklist
- [ ] Do table/column names match the domain vocabulary? (ubiquitous language)
- [ ] Are aggregate boundaries clear? (what must be consistent together?)
- [ ] Are value objects modeled as immutable? (no identity column needed)
- [ ] When integrating external data, is there a translation layer?

---

## Ralph Kimball — Dimensional Modeling

**Source:** *The Data Warehouse Toolkit* (1996, 3rd ed. 2013)

### Core Principles
1. **Fact tables** — measurable events (transactions, snapshots, accumulating snapshots)
2. **Dimension tables** — descriptive context for facts (who, what, where, when, why, how)
3. **Star schema** — fact table surrounded by denormalized dimension tables (simplicity, query performance)
4. **Conformed dimensions** — shared dimension tables used across multiple fact tables for consistent analysis
5. **Slowly changing dimensions** — techniques for tracking historical changes (Type 1: overwrite, Type 2: add row, Type 3: add column)
6. **Bus architecture** — enterprise data warehouse built incrementally from conformed dimensions

### Application Checklist
- [ ] Is the model organized around measurable events (facts) with descriptive context (dimensions)?
- [ ] Are dimensions denormalized for query simplicity?
- [ ] Are shared dimensions conformed across subject areas?
- [ ] Is historical change tracking defined for dimensions that change over time?

---

## Bill Inmon — Enterprise Data Warehouse

**Source:** *Building the Data Warehouse* (1992, 4th ed. 2005)

### Core Principles
1. **Subject-oriented** — organized around major business subjects, not applications
2. **Integrated** — data from disparate sources is consolidated with consistent naming, encoding, and measurement
3. **Time-variant** — data is associated with a specific time period; historical
4. **Non-volatile** — data is loaded and not updated; append-only

### Key Distinction from Kimball
Inmon: normalized enterprise model first → dimensional data marts derived from it.
Kimball: dimensional data marts first → enterprise emerges from conformed dimensions.

### Application Checklist
- [ ] Is the data model organized by business subject, not by source system?
- [ ] Are naming conventions and encodings consistent across integrated sources?
- [ ] Is historical data preserved (not overwritten)?

---

## E.F. Codd — Relational Model & Normalization

**Source:** "A Relational Model of Data for Large Shared Data Banks" (1970, CACM)

### Core Principles — Normal Forms
1. **1NF** — no repeating groups; each cell contains a single value
2. **2NF** — 1NF + no partial dependencies (every non-key attribute depends on the whole key)
3. **3NF** — 2NF + no transitive dependencies (non-key attributes don't depend on other non-key attributes)
4. **BCNF** — every determinant is a candidate key

**Practical rule:** Normalize to 3NF for operational data; denormalize deliberately for reporting/analytics (with documented rationale).

### Application Checklist
- [ ] Does every table have a clear primary key?
- [ ] Are there repeating groups that should be separate tables? (1NF)
- [ ] Do non-key columns depend on the whole key? (2NF)
- [ ] Are there columns that depend on other non-key columns? (3NF — extract to a lookup table)
- [ ] If denormalized, is the rationale documented?

---

## David Hay — Data Model Patterns

**Source:** *Data Model Patterns: Conventions of Thought* (1996); *Enterprise Model Patterns* (2011)

### Core Principles
1. **Recurring patterns** — the same structural patterns appear across industries (parties, roles, events, documents, products)
2. **Party model** — people and organizations are the same entity type with roles; don't create separate Person and Company tables
3. **Role pattern** — entities play roles in contexts; roles are relationships, not subtypes
4. **Event pattern** — things that happen (transactions, requests, approvals) share common structure

### Application Checklist
- [ ] Does the model use established patterns (party, role, event) where they apply?
- [ ] Are people and organizations modeled as a unified "party" with roles?
- [ ] Are events (things that happen) modeled consistently?
- [ ] Are you inventing a novel structure where a known pattern exists?

---

## Len Silverston — Universal Data Models

**Source:** *The Data Model Resource Book* (Vol. 1 & 2, 2001; Vol. 3, 2009)

### Core Principles
1. **Industry-standard models** — pre-built, validated data models for common business domains (parties, products, orders, work effort, accounting)
2. **Adapt, don't invent** — start from a proven model and customize, rather than designing from scratch
3. **Cross-industry patterns** — many data structures are universal regardless of industry

### Application Checklist
- [ ] Has an existing reference model been checked before designing from scratch?
- [ ] Are deviations from the reference model documented with rationale?

---

## Cross-Reference: Problem → Framework

| Data Modeling Problem | Primary Framework(s) |
|----------------------|---------------------|
| Conceptual model / stakeholder communication | Chen (ER Model) |
| Domain vocabulary and boundaries | Evans (DDD) |
| Analytical / reporting schema | Kimball (Dimensional Modeling) |
| Enterprise data integration | Inmon (Data Warehouse) |
| Schema quality / normalization | Codd (Normal Forms) |
| Recurring structural patterns | Hay (Data Model Patterns), Silverston (Universal Models) |
| Aggregate / transaction boundaries | Evans (DDD Aggregates) |

---

## Cross-References

| When also doing... | Load... |
|-------------------|---------|
| Writing code that uses the schema | `software-engineering.md` (Evans DDD, Fowler patterns) |
| Documenting the data model | `documentation-design.md` |
| Building dashboards from the data | `data-visualization.md` |
| Designing the domain vocabulary | `information-architecture.md` (ontology/taxonomy) |
