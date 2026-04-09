# Software Engineering — Professional Disciplines

Expert perspectives for code design, architecture, testing, refactoring, and deployment.

*Note: Dave Farley's two-competency framework (optimize for learning, manage complexity) is foundational. This file provides the broader landscape of engineering disciplines beyond that framework.*

---

## Robert C. Martin — SOLID Principles & Clean Code

**Source:** *Clean Code* (2008); *Clean Architecture* (2017); *Agile Software Development: Principles, Patterns, and Practices* (2002)

### Core Principles — SOLID
1. **Single Responsibility** — a class/module has one reason to change
2. **Open/Closed** — open for extension, closed for modification
3. **Liskov Substitution** — subtypes must be substitutable for their base types
4. **Interface Segregation** — no client should depend on methods it doesn't use
5. **Dependency Inversion** — depend on abstractions, not concretions

### Clean Code Principles
- Functions should do one thing, do it well, do it only
- Names should reveal intent
- Comments are a failure to express intent in code
- The Boy Scout Rule: leave the code cleaner than you found it

### Application Checklist
- [ ] Does each module/function have a single, nameable responsibility?
- [ ] Can this be extended without modifying existing code?
- [ ] Are dependencies on abstractions, not concrete implementations?
- [ ] Do names reveal intent without needing comments to explain?

---

## Martin Fowler — Refactoring & Enterprise Patterns

**Source:** *Refactoring* (1999, 2nd ed. 2018); *Patterns of Enterprise Application Architecture* (2002)

### Core Principles — Refactoring
1. **Refactoring** — changing internal structure without changing external behavior
2. **Code smells** — indicators that code needs restructuring (long method, large class, feature envy, data clumps, primitive obsession)
3. **Two hats** — you're either adding function or refactoring; never both at once
4. **Small steps** — refactor in small, verified increments

### Key Enterprise Patterns
- **Repository** — mediates between domain and data mapping layers
- **Unit of Work** — maintains list of objects affected by a transaction
- **Data Mapper** — moves data between objects and database, keeping them independent
- **Domain Model** — object model of the domain incorporating behavior and data

### Application Checklist
- [ ] Are you wearing one hat? (adding function OR refactoring, not both)
- [ ] Can you name the code smell? (if it feels wrong, it has a name)
- [ ] Is each refactoring step small enough to verify independently?
- [ ] Does the architecture separate domain logic from infrastructure?

---

## Kent Beck — Test-Driven Development & Extreme Programming

**Source:** *Test-Driven Development: By Example* (2002); *Extreme Programming Explained* (1999, 2nd ed. 2004)

### Core Principles — TDD Cycle
1. **Red** — write a failing test
2. **Green** — write the simplest code that makes the test pass
3. **Refactor** — clean up while keeping tests green

### XP Values
Communication, Simplicity, Feedback, Courage, Respect — do the simplest thing that works, get feedback fast, make the hard changes.

### Application Checklist
- [ ] Is there a test before there's implementation?
- [ ] Is the implementation the simplest thing that passes the test?
- [ ] Are you refactoring after green, not skipping it?
- [ ] Is YAGNI being respected? (You Aren't Gonna Need It)

---

## Eric Evans — Domain-Driven Design

**Source:** *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003)

### Core Principles
1. **Ubiquitous Language** — shared, rigorous language between developers and domain experts
2. **Bounded Context** — explicit boundaries within which a model applies
3. **Aggregates** — cluster of domain objects treated as a unit; root entity + consistency boundary
4. **Entities vs Value Objects** — entities defined by identity; value objects by attributes (immutable)
5. **Domain Events** — something that happened that domain experts care about
6. **Context Mapping** — relationships between bounded contexts (shared kernel, customer/supplier, anti-corruption layer)

### Application Checklist
- [ ] Is the code using the same language as the domain?
- [ ] Are model boundaries explicit?
- [ ] Is domain logic in the domain layer, not scattered across infrastructure?

---

## Gang of Four — Design Patterns

**Source:** Gamma, Helm, Johnson, Vlissides — *Design Patterns: Elements of Reusable Object-Oriented Software* (1994)

### Core Principle
Design patterns are **named, proven solutions to recurring design problems**. The name is as important as the solution — it creates shared vocabulary.

### Key Patterns by Category
- **Creational:** Factory Method, Abstract Factory, Builder, Singleton
- **Structural:** Adapter, Composite, Decorator, Facade, Proxy
- **Behavioral:** Observer, Strategy, Template Method, Command, Iterator

### Application Checklist
- [ ] Is there a named pattern that solves this problem? (don't reinvent)
- [ ] Is the pattern appropriate, or is simpler code sufficient? (don't over-pattern)
- [ ] Can you name the pattern to communicate intent to future readers?

---

## Sandi Metz — Practical Object-Oriented Design

**Source:** *Practical Object-Oriented Design* (POODR, 2012, 2nd ed. 2018); *99 Bottles of OOP* (2018)

### Core Principles
1. **Depend on things that change less often than you do** — fundamental dependency management rule
2. **Composition over inheritance** — prefer composing objects to inheriting
3. **The Flocking Rules** — find most alike things, identify smallest difference, make simplest change
4. **Cost of change** — minimize cost of future change, not initial implementation
5. **Shameless Green** — simplest code that passes tests; refactor when the abstraction emerges

### Application Checklist
- [ ] Do dependencies point toward stability?
- [ ] Is the design optimized for future change, not just current implementation?
- [ ] Are you waiting for the right abstraction to emerge rather than guessing?

---

## Michael Feathers — Working with Legacy Code

**Source:** *Working Effectively with Legacy Code* (2004)

### Core Principles
1. **Legacy code = code without tests**
2. **Change Algorithm:** identify change points → find test points → break dependencies → write tests → make changes
3. **Seams** — places to alter behavior without editing code (object, link, preprocessing seams)
4. **Characterization tests** — document existing behavior, not desired behavior
5. **Sprout and Wrap** — add new code without making legacy worse

### Application Checklist
- [ ] Is modified code covered by tests? If not, write characterization tests first.
- [ ] Can you identify seams for breaking dependencies?

---

## Jez Humble & Dave Farley — Continuous Delivery

**Source:** *Continuous Delivery* (2010)

### Core Principles
1. **Every change should be releasable** — the pipeline validates this
2. **Automate everything** — build, test, deploy, infrastructure
3. **Keep everything in version control** — code, config, infrastructure, docs
4. **Done means released** — not complete until it's in production
5. **Build quality in** — don't inspect after; build it into the process

### Application Checklist
- [ ] Can any commit be released with confidence?
- [ ] Is the build/test/deploy process automated?
- [ ] Is everything in version control?

---

## Gene Kim et al. — DORA Metrics & DevOps

**Source:** *Accelerate* (2018, with Jez Humble & Nicole Forsgren); *The Phoenix Project* (2013)

### Four Key Metrics (DORA)
1. **Deployment Frequency** — how often you deploy to production
2. **Lead Time for Changes** — commit to production
3. **Mean Time to Restore** — time to recover from failure
4. **Change Failure Rate** — % of deployments causing failures

### Three Ways
1. **Flow** — optimize left-to-right (dev → ops → customer)
2. **Feedback** — amplify right-to-left feedback loops
3. **Continual Learning** — experimentation and learning from failure

---

## Heroku — 12-Factor App

**Source:** 12factor.net (Adam Wiggins, 2011) — 12 principles for building software-as-a-service apps.

### Key Factors
1. **Dependencies** — explicitly declare and isolate
2. **Config** — store in the environment, not code
3. **Build, release, run** — strictly separate stages
4. **Processes** — stateless; store nothing in local memory across requests
5. **Dev/prod parity** — minimize divergence between environments
6. **Logs** — treat as event streams, not files

Full list (12 factors) at 12factor.net. Most missed in practice: #3 (build/run separation), #6 (statelessness), #10 (dev/prod parity).

### Application Checklist
- [ ] Are dependencies explicitly declared, not implicit?
- [ ] Is config separated from code?
- [ ] Is the app stateless?

---

## Fred Brooks — The Mythical Man-Month

**Source:** *The Mythical Man-Month* (1975, anniversary ed. 1995)

### Core Principles
1. **Brooks's Law** — adding people to a late project makes it later
2. **No Silver Bullet** — no single technique yields order-of-magnitude productivity improvement
3. **Conceptual integrity** — one coherent design vision beats many uncoordinated ideas
4. **Second-system effect** — tendency to over-engineer the second version
5. **Plan to throw one away** — you will, whether you plan to or not

### Application Checklist
- [ ] Does the system have conceptual integrity?
- [ ] Are you resisting second-system over-engineering?

---

## Simon Brown — C4 Model

**Source:** *Software Architecture for Developers* (2018); c4model.com

### Core Framework — Four Zoom Levels
1. **Context** — system as black box in its environment ("what is this, where does it fit?")
2. **Container** — high-level building blocks: apps, data stores, services ("what are the big pieces?")
3. **Component** — internals within each container: classes, modules ("what's inside each piece?")
4. **Code** — implementation detail: function signatures, algorithms ("how does this part work?")

### Key Design Principles
- Each level tells a complete story — readers can stop at any level with coherent understanding
- Designed for communication, not formal modeling
- Most systems need only Context + Container; Component and Code are selective

### Application Checklist
- [ ] Can you explain the system at Context level in 2-3 sentences?
- [ ] Are Container-level building blocks named with clear responsibilities?
- [ ] Is each zoom level self-contained?

---

## Gernot Starke & Peter Hruschka — arc42

**Source:** arc42.org (open-source architecture documentation template); Starke, *Effective Software Architecture* (2005)

### Key Sections (from 12-section template)
1. **Constraints** — technical, organizational, business constraints
2. **Context and Scope** — system boundary and external interfaces (overlaps C4 Level 1)
3. **Building Block View** — hierarchical decomposition (overlaps C4 Levels 2-3)
4. **Design Decisions** — significant decisions with context, alternatives, rationale
5. **Risks and Technical Debt** — known limitations and consequences

### Key Principles
- **Lean documentation** — select from the template, don't complete every section
- **Design decisions are first-class** — context + rationale matter more than the decision alone
- **Risks are explicit** — document limitations upfront, not in code comments

### Application Checklist
- [ ] Are significant decisions documented with context and alternatives?
- [ ] Are constraints stated explicitly?
- [ ] Are known risks documented?

---

## C4 + arc42 — Combined Application

C4 provides structural zoom levels (HOW to organize the description). arc42 provides reasoning sections (WHY the architecture is this way). Use C4 for structure, arc42 for decisions/constraints/risks. Apply together for architecture documentation, ADRs, system overviews, onboarding docs.

---

## Cross-Reference: Problem → Framework

| Engineering Problem | Primary Framework(s) |
|--------------------|---------------------|
| Code is hard to change | Martin (SOLID), Metz (dependency direction), Fowler (refactoring) |
| Modifying code without tests | Feathers (legacy code change algorithm, characterization tests, seams) |
| Domain logic is scattered / naming is inconsistent | Evans (DDD — ubiquitous language, bounded contexts, domain model) |
| Choosing between design approaches | GoF (named patterns), Beck (simplest thing that works), Brooks (conceptual integrity) |
| Deployment is painful or manual | Humble/Farley (CD pipeline, automate everything), DORA (four key metrics) |
| Over-engineering / second-system symptoms | Brooks (second-system effect), Beck (YAGNI), Metz (shameless green) |
| Architecture decisions need evaluation | Farley advisor (two-competency test: learning + complexity), 12-Factor |
| Need to measure engineering performance | DORA (four key metrics) |
| Need to explain a system | C4 (zoom levels) + arc42 (decisions + constraints) |

---

## Cross-References

| When also doing... | Load... |
|-------------------|---------|
| Data schemas | `data-modeling.md` |
| User interfaces | `ux-interaction-design.md` |
| Technical documentation | `documentation-design.md` + C4/arc42 above |
| Dashboards/visualizations | `data-visualization.md` |
