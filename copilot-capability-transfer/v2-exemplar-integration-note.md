# V2 Exemplar Integration Note

## What's included

`ledger-writer-v2-exemplar.yaml` — a completed SUD for a non-trivial
financial service (Bank of Anthos ledger-writer), produced by walking the
v2 motivation chain instrument. Transfer this file alongside this note.

## Why this exists

The v1 bos-onboard skill treats the exemplar as an architectural dependency.
The agent reads the exemplar before producing any output and matches its
structure exactly. The exemplar IS the output contract — it shows what
a completed SUD looks like, which is a different problem than what questions
to ask (the instrument handles that).

When the v2 instrument was introduced, this exemplar reference was dropped.
The v2 skill relied on the instrument's structural metadata (repeat_per,
chain, group) to communicate output shape. In practice, showing a completed
example is more reliable than describing structure through metadata —
particularly for less capable models. This is basic worked-example effect
(Sweller's cognitive load theory): pattern-matching from a concrete example
reduces the agent's inference burden.

## What the exemplar demonstrates

The ledger-writer exercises the full v2 schema expansion:

- **4 stakeholder motivation chains** with distinct drivers and impact categories
  (customer_experience, legal_risk, financial, operational)
- **All 3 APQC dimensions** on Business Health signals (Effectiveness,
  Efficiency, Adaptability)
- **16 signals across 4 layers** — Business Health, Business Impact, Process,
  System
- **needs[]** — GQM Goals with SEI QA scenarios, Meyer DbC preconditions,
  composite health formulas, and need-level impacts
- **need_signals[]** — Goal-Metric links with outcome/diagnostic roles
- **need_stakeholders[]** and **need_expectations[]** — full RTM traceability
- **service.process_participations[]** — ArchiMate process participation
- **Causal links** from Process signals to Business Health signals
- **Golden Signal and USE dimensions** on Process and System signals
- Deprecated v1 fields maintained for backward compatibility

The previous exemplar (checkout or pitstop) demonstrated the pipeline
mechanics on a trivial service. This exemplar demonstrates what a real
v2 SUD looks like — multi-stakeholder, multi-chain, with the regulatory
and financial complexity that banking services actually have.

## What to do with it

The bos-onboard skill in this environment should reference this exemplar
the way the v1 skill referenced its exemplar — as an output contract the
agent reads before producing any SUD. The specific integration depends on
how the skill is currently structured here, which may have evolved since
the original transfer. The key behavior to establish:

1. The agent reads the exemplar before producing output
2. The agent's output matches the exemplar's structure (field names, nesting,
   v2 additions)
3. The exemplar is the format reference, the instrument is the question
   reference — these are complementary, not redundant

The exemplar file should live with the skill's reference materials, not
in the pipeline's golden-fixture directory. It serves the agent (output
contract), not the pipeline (validation fixture).
