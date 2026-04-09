# UX & Interaction Design — Professional Disciplines

Expert perspectives for user interface design, usability, and interaction patterns.

---

## Don Norman — Interaction Design Principles

**Source:** *The Design of Everyday Things* (1988, revised 2013); *Emotional Design* (2004)

### Core Principles — Six Fundamentals
1. **Affordances** — properties that show what actions are possible
2. **Signifiers** — signals that indicate where/how to act
3. **Constraints** — restrictions that prevent incorrect actions
4. **Mappings** — layout of controls matches spatial layout of results
5. **Feedback** — communicating results of an action back to the user
6. **Conceptual models** — the mental image the user forms about how something works

### Three Levels of Emotional Design
1. **Visceral** — immediate sensory/aesthetic reaction
2. **Behavioral** — experience during use (function, usability, performance)
3. **Reflective** — conscious thought about the product (meaning, self-image)

### Application Checklist
- [ ] Can the user tell what actions are possible without instructions? (affordances + signifiers)
- [ ] Does the interface prevent errors before they happen? (constraints)
- [ ] Does every action produce visible feedback?
- [ ] Does the layout of controls match the user's mental model? (mappings)

---

## Jakob Nielsen — 10 Usability Heuristics

**Source:** *Usability Engineering* (1993); heuristics paper with Rolf Molich (1990, revised 1994)

### The 10 Heuristics
1. **Visibility of system status** — keep users informed about what's happening
2. **Match between system and real world** — use the user's language, not system language
3. **User control and freedom** — support undo and redo; provide emergency exits
4. **Consistency and standards** — don't make users wonder whether different words/actions mean the same thing
5. **Error prevention** — design to prevent errors, not just report them
6. **Recognition rather than recall** — make options visible; minimize memory load
7. **Flexibility and efficiency of use** — accelerators for experts, simplicity for novices
8. **Aesthetic and minimalist design** — every extra unit of information competes with relevant information
9. **Help users recognize, diagnose, and recover from errors** — express errors in plain language with solutions
10. **Help and documentation** — provide help that's searchable and task-focused

### Application Checklist
- [ ] Does the user always know what state the system is in? (#1)
- [ ] Does the interface use the user's vocabulary, not technical terms? (#2)
- [ ] Can the user undo any action? (#3)
- [ ] Are similar things presented consistently? (#4)
- [ ] Do error messages tell the user what to do, not just what went wrong? (#9)

---

## Steve Krug — Don't Make Me Think

**Source:** *Don't Make Me Think* (2000, 3rd ed. 2014)

### Core Principles
1. **Self-evident design** — the page should be self-explanatory at a glance
2. **Users scan, they don't read** — design for scanning behavior
3. **Users satisfice** — they choose the first reasonable option, not the best
4. **Users muddle through** — they don't figure out how things work, they guess

### Application Checklist
- [ ] Can someone understand what this page does in 5 seconds?
- [ ] Is the visual hierarchy clear (what's most important is most prominent)?
- [ ] Are clickable things obviously clickable?
- [ ] Could any text be cut in half and still work?

---

## Ben Shneiderman — 8 Golden Rules

**Source:** *Designing the User Interface* (1st ed. 1986, 6th ed. 2016)

### The 8 Golden Rules
1. **Strive for consistency** — same actions, same results, same terminology
2. **Enable frequent users to use shortcuts** — abbreviations, hotkeys, macros
3. **Offer informative feedback** — every action should produce a visible response
4. **Design dialogs to yield closure** — group actions into beginning/middle/end
5. **Offer error prevention and simple error handling** — prevent errors; when they occur, offer constructive guidance
6. **Permit easy reversal of actions** — undo reduces anxiety and encourages exploration
7. **Support internal locus of control** — users feel in charge, not controlled by the system
8. **Reduce short-term memory load** — don't require users to remember information across screens

### Application Checklist
- [ ] Do multi-step processes have clear beginning/middle/end? (#4)
- [ ] Can the user reverse any action easily? (#6)
- [ ] Does the user feel in control of the experience? (#7)
- [ ] Is information carried forward between steps (not requiring user to remember)? (#8)

---

## Jesse James Garrett — Five Planes of UX

**Source:** *The Elements of User Experience* (2002, 2nd ed. 2010)

### The Five Planes (abstract → concrete)
1. **Strategy** — user needs + business objectives
2. **Scope** — functional specifications + content requirements
3. **Structure** — interaction design + information architecture
4. **Skeleton** — interface design + navigation design + information design
5. **Surface** — visual design (sensory experience)

Each plane depends on the one below it. Strategy is foundation; surface is final expression.

### Application Checklist
- [ ] Is the strategy clear before designing the surface? (don't start with visual design)
- [ ] Are scope decisions driven by strategy, not feature wishlists?
- [ ] Is the structure (IA + interaction patterns) resolved before skeleton (layout)?

---

## Gestalt Principles of Perception

**Source:** Wertheimer, Koffka, Kohler (1920s, Berlin School)

### Core Principles
1. **Proximity** — elements near each other are perceived as a group
2. **Similarity** — elements sharing visual characteristics are perceived as related
3. **Closure** — the mind completes incomplete shapes
4. **Continuity** — elements on a line/curve are perceived as related
5. **Figure/Ground** — perception separates foreground from background
6. **Common region** — elements within a boundary are perceived as grouped

### Application Checklist
- [ ] Are related elements visually grouped through proximity or common region?
- [ ] Do similar elements share visual treatment (color, shape, size)?
- [ ] Is the foreground/background relationship clear?
- [ ] Are visual groupings communicating actual semantic relationships?

---

## Cognitive Load Theory

**Source:** John Sweller (1988), educational psychology

### Three Types
1. **Intrinsic** — inherent complexity of the task (irreducible)
2. **Extraneous** — imposed by bad design (unnecessary processing, distracting elements)
3. **Germane** — effort devoted to building understanding (the "good" load)

**Design objective:** Minimize extraneous load, manage intrinsic load through chunking and progressive disclosure, maximize germane load.

### Application Checklist
- [ ] Is the user overwhelmed? Which type of load is the problem?
- [ ] Can extraneous elements be removed without losing function?
- [ ] Is complex information chunked into manageable pieces?
- [ ] Is progressive disclosure used (show only what's needed at each step)?

---

## Key Perceptual Laws

### Fitts's Law (Paul Fitts, 1954)
Time to acquire a target = f(distance to target, size of target). **Make important targets large and close.**

### Hick's Law (Hick & Hyman, 1952)
Decision time increases logarithmically with the number of choices. **Reduce options; use progressive disclosure.**

### Miller's Law (George Miller, 1956)
Working memory holds 7±2 items. The point is **chunking** — group items into meaningful units.

### Tesler's Law (Larry Tesler, 1980s)
Every system has irreducible complexity. It can only be moved — **the system should absorb complexity, not the user.**

### Application Checklist
- [ ] Are important interactive targets large enough and close to related elements? (Fitts)
- [ ] Are choices kept manageable at each decision point? (Hick)
- [ ] Is information chunked into groups of 5-9? (Miller)
- [ ] Is unavoidable complexity handled by the system, not pushed to the user? (Tesler)

---

## Dieter Rams — 10 Principles of Good Design

**Source:** Articulated late 1970s (industrial design, Braun)

### Core Principles
Good design is: innovative, useful, aesthetic, understandable, unobtrusive, honest, long-lasting, thorough to the last detail, environmentally friendly, and **as little design as possible** ("Less, but better").

### Application Checklist
- [ ] Is the design honest about what it does? (no misleading affordances)
- [ ] Is the design unobtrusive? (doesn't dominate the content)
- [ ] Could any design element be removed? ("as little design as possible")

---

## Aarron Walter — Hierarchy of User Needs

**Source:** *Designing for Emotion* (2011, A Book Apart)

### The Hierarchy (bottom → top, Maslow-adapted)
1. **Functional** — it works
2. **Reliable** — it works consistently
3. **Usable** — it's easy to use
4. **Pleasurable** — it creates positive emotional response

Each level must be satisfied before the next matters.

### Application Checklist
- [ ] Is the product reliably functional before adding delight?
- [ ] Are you trying to be pleasurable when you're not yet usable?

---

## Cross-Reference: Problem → Framework

| UX/Interaction Problem | Primary Framework(s) |
|-----------------------|---------------------|
| Users can't figure out what to do | Norman (affordances, signifiers), Krug (self-evident design) |
| Users make errors | Norman (constraints), Nielsen (#5 error prevention, #9 error recovery), Shneiderman (#5) |
| Interface feels overwhelming | Cognitive Load (reduce extraneous), Hick's Law (fewer choices), Nielsen (#8 minimalist design) |
| Multi-step flow feels broken | Shneiderman (#4 closure, #8 memory load), Garrett (structure plane) |
| Users don't notice important elements | Gestalt (proximity, similarity), Ware (preattentive processing), Fitts's Law (target size) |
| Design lacks strategic grounding | Garrett (five planes — start from strategy), Walter (hierarchy of needs) |
| Visual design feels cluttered | Rams ("as little design as possible"), Nielsen (#8), Gestalt (figure/ground) |
| Evaluating overall usability | Nielsen (10 heuristics as evaluation framework), Shneiderman (8 golden rules) |

---

## Cross-References

| When also doing... | Load... |
|-------------------|---------|
| Organizing content/navigation | `information-architecture.md` |
| Displaying data | `data-visualization.md` |
| Writing UI text/labels/messages | `content-design.md` (Podmajersky — UX Writing) |
| Building documentation UI | `documentation-design.md` |
