# Zelle — Public Research for Business-Observability Requirements

**What this is:** a cited, public-source research report on Zelle, shaped to feed
business-observability requirement identification for a real-time P2P payment
service. It decomposes Zelle into a business-capability flow whose steps,
outcomes, failure modes, and dependencies can be turned into observability
signals — i.e., the substrate for a service-understanding document (SUD). It is
**not** a SUD: a public-only SUD would manufacture `constructed`/`inferred`
content for the Process/System layers that are implementation-specific. This gives
the real public substrate; the onboard run happens later with internal inputs.

**Verification:** the high-value figures below were primary-verified by hand on
2026-06-20 (a separate per-source provenance record carries `method` and
`evidence_strength` for all 18 primary sources).

**Date:** 2026-06-20. **Scope:** public information only.

---

## ⚠️ Method & confidence caveat (read first)

This report was produced by five parallel research agents (transaction flow,
failure modes/incidents, fraud/regulatory, network structure, payment-domain
prior art). **Direct page fetching (`WebFetch`) returned HTTP 403 on essentially
every primary source** (zelle.com, earlywarning.com, consumerfinance.gov,
hsgac.senate.gov, ecfr.gov, theclearinghouse.org, major bank FAQs, news sites)
in this environment. All claims therefore rest on **search-result summaries that
quote those primaries**, not on full-text reads.

Confidence convention used throughout:
- **HIGH** — the same fact surfaced independently across multiple research angles
  and/or multiple outlets. Cross-angle agreement is the main verification here.
- **MEDIUM** — single-summary or secondary-source; plausible but unconfirmed.
- **VERIFY** — specific dollar/count/date figures that should be confirmed
  against the primary document before any external (stakeholder-facing) use.

The figures most worth primary-verifying before you quote them externally:
the CFPB $870M and NY AG $1B loss totals; the Senate reimbursement percentages
(38% fraud / 12% scam); transaction volume/value/user counts; Reg E §1005.11
subsection cites; and RTP/FedNow transaction limits.

**Update 2026-06-20 — manual primary verification complete for the high-value
figures.** The "Group A" figures (all scale numbers, the CFPB $870M / dismissal,
NY AG $1B, Senate 38%/12%/$166M, Warren $440M/47%) were confirmed against
primaries by hand and are marked **[confirmed 2026-06-20]** below. Two
corrections came out of that pass and are applied here: (1) the Reg E "90-day"
timeline is **not** the general extended deadline — it applies only to
new-account, foreign-initiated, and POS-debit transfers (general escalation is 10
business days → 45 days); (2) the 10/45/90 resolution clock and the 60-day
consumer *reporting* window are two different clocks and are now kept distinct.
The Fiserv "60+ applications" figure held up but remains **single-source**
(American Banker) — keep it attributed.

**Update 2026-06-20 (round 2) — supporting sources (B–E) also primary-verified.**
Confirmed: Reg E resolution + liability clocks (1005.11 / 1005.6); RTP settlement
live Feb 25 2021 (BofA + PNC first movers); EWS RFI response filed Sept 19 2025;
EWS = seven banks running Zelle + Paze ($10.8T screened / $3B fraud stopped 2024);
FedNow 24/7/365 RTGS on ISO 20022; UK PSR APP regime live Oct 7 2024 (£85k,
50/50, 5-day). One freshness correction applied below: **Reg CC next-day
availability threshold rose $225 → $275, effective July 1 2025.** Two guards for
future readers: the Fiserv "60+" stays attributed to American Banker (single
outlet); and **Nacha's Same Day ACH per-payment limit is $1M today** — the $10M
figure is future-dated (effective Sept 17 2027), so do not present it as current.

---

## 1. Executive synthesis

1. **The case for business observability on Zelle is provable from public evidence.** Zelle is a
   *directory + messaging layer over other banks' rails* — it moves messages,
   not money. Because it is embedded inside each bank's own app, a bank-core
   fault, a Zelle-network fault, and a shared-processor fault all present
   **identically** to customers, and attribution is only knowable *post-hoc* from
   a spokesperson statement. There is **no public per-step telemetry** separating
   enrollment / directory-resolution / send-auth / settlement / receive-post
   failures. The incident-blindness pain ("dashboards up, can't tell what's
   up/down or where traffic flowed") is the *inherent* observability gap of this
   architecture — not merely one bank's dashboard deficiency. **[HIGH]**

2. **Public Zelle knowledge maps cleanly onto the SUD's top three layers and
   almost nothing below.** Service context (Part 1), Business-Health stakeholder
   chains (Part 2), and Business Impact (Part 2b) can be substantially pre-filled
   from public sources. Process (Part 3) and System (Part 4) signals are
   implementation-specific and route to a participating bank's internal teams.
   This is itself a finding: *the method can pre-stage the "are we observing the
   right things" layer for free; dev partners must supply the lower layers* —
   a clean framing for what to tell dev partners to build.

3. **There is a real-world precedent for an "enforced standard."** Every
   participating institution is bound by the **Zelle Network Participation Rules**,
   maintained and *enforced* by Early Warning Services (EWS), which can itself
   restrict a bad-actor token network-wide. A bank-owned consortium already
   prescribes-and-confirms compliance at network scale. That is the shape of the
   enforcement mechanism enterprise leadership is reaching for, in the exact
   domain of this effort. **[HIGH]**

4. **Payments carry observability primitives the generic SUD doesn't name.** The
   payment domain has a *two-layer success problem* (a payment can succeed at the
   message layer yet fail to reconcile at the ledger/settlement layer), plus
   built-in primitives — UETR (end-to-end trace ID), ISO 20022 `pacs.002` status
   + reason codes (a ready-made error taxonomy), and irrevocability that turns
   duplicate-detection into a *pre-send safety gate*. These are concrete
   candidate additions to the instrument (§7). **[HIGH]**

5. **The protected business outcomes are large and regulator-visible.** Cumulative
   Zelle fraud/scam losses were put at ~$870M (CFPB suit, Dec 2024) and ~$1B (NY
   AG suit, Aug 2025); the three biggest owner banks reportedly reimbursed fraud
   victims ~38% and scam victims ~12% of the time in 2023. Reg E imposes hard
   investigation SLAs (10 business days / 45-day ceiling / provisional credit).
   These are the business-impact magnitudes and SLO provenance the SUD wants. **[HIGH for existence; VERIFY exact figures]**

---

## 2. Zelle at a glance — scale, ownership, governance

| # | Fact | Confidence |
|---|------|-----------|
| 1 | **Owner/operator:** Early Warning Services, LLC (EWS), Scottsdale AZ — a fintech jointly owned by 7 banks: Bank of America, Capital One, JPMorgan Chase, PNC, Truist, U.S. Bank, Wells Fargo | HIGH |
| 2 | **Lineage:** clearXchange (2011, BofA/Wells/JPM) → folded into EWS (2015–16) → relaunched as Zelle (2017) | HIGH |
| 3 | **Scale 2024:** >$1 trillion sent (first $1T year, +27% YoY); 3.6 billion transactions (+25%); 151 million enrolled accounts (+16M) | HIGH (confirmed 2026-06-20) |
| 4 | **Scale 2025:** >$1.2 trillion sent (+20%) on 4.2 billion transactions (~$3.4B/day); second straight $1T year; single-day record >$9B (Aug 2025) | HIGH (confirmed 2026-06-20) |
| 5 | **Network breadth:** 2,300+ participating institutions (~95% community banks/CUs by count); ~80% of U.S. deposit accounts reachable | HIGH / count drifts |
| 6 | **Concentration:** JPMorgan + BofA + Wells facilitated **73%** of volume (2023) — the one independently-compiled figure (Senate PSI) | HIGH |
| 7 | **Settlement:** no rail of its own — historically deferred-net **ACH**; **RTP** (The Clearing House) since Feb 2021; also card rails (Visa Direct / Mastercard Send); per-transaction rail-selection logic is **not public** | HIGH (multi-rail) / MEDIUM (mix) |
| 8 | **Governance:** participants bound by **Zelle Network Participation Rules**, maintained + enforced by EWS; eligibility gated to chartered/insured/regulated U.S. institutions; EWS can restrict a token network-wide | HIGH |
| 9 | **Broader EWS:** also runs Paze (checkout wallet) and a large fraud/identity franchise (National Shared Database, account screening); screened $10.8T in payments in 2024 | HIGH |

---

## 3. The end-to-end flow, decomposed into sub-capabilities

This is the core deliverable: each Zelle sub-capability rendered in the SUD's
field shape — `{what it does · stakeholders & drivers · customer outcome ·
failure modes · candidate Business-Health signal & SLO · provenance ·
dependencies · observable vs black-box}`. These are **candidate** signals derived
from public understanding; an onboard run with internal inputs confirms/replaces them.

The nine sub-capabilities (a candidate answer to SUD q40–q43):

```
1. Enrollment & token registration
2. Token/alias directory resolution
3. Payment initiation & authorization (sender bank)
4. Risk / fraud / sanctions decisioning (inline, blocking)
5. Network routing & messaging (EWS hub)
6. Clearing & settlement (ACH / RTP / card rails)
7. Receiving-bank posting & funds availability
8. Notification & confirmation
9. Dispute / error resolution / reimbursement (post-completion)
```

---

### 3.1 Enrollment & token registration

- **What it does:** a user registers an email and/or U.S. mobile number (the
  alias/token) and links a deposit account; unverified tokens are confirmed via a
  one-time code. Only the user's name, their FI's name, and the token go to the
  directory — never the account number. **[HIGH]**
- **Stakeholders & drivers:** new customer (Customer Experience — "I can start
  using Zelle"); the bank (Regulatory Compliance / Revenue Integrity — weak
  enrollment identity binding is the root the NY AG suit attacks); fraud/risk
  (Service Reliability — account-takeover prevention).
- **Customer outcome (works):** token verified, account linked, ready to transact.
- **Failure modes:** failed enrollment (token not verified, unsupported contact
  info); **weak identity binding enabling account-takeover onboarding of
  fraudsters** (central NY AG allegation); re-enrollment to a new bank / token
  takeover. **[HIGH for the fraud framing]**
- **Candidate Business-Health signal:** Enrollment Completion Rate (APQC
  *Effectiveness*); Enrollment Verification Latency (APQC *Efficiency*).
- **Provenance for an SLO:** account-takeover / identity-binding controls implicate
  Reg E unauthorized-transfer liability (12 CFR 1005.6) and the Zelle Rules
  identity requirements. **[MEDIUM]**
- **Dependencies:** bank identity/auth systems; the EWS directory write path; OTP
  delivery (SMS/email).
- **Observable vs black-box:** enrollment success/latency observable bank-side;
  the directory's token lifecycle, dedupe, and identity-binding internals are
  **EWS black-box**.

### 3.2 Token/alias directory resolution

- **What it does:** at send time, Zelle looks up the recipient token in its
  directory and maps it to the recipient's financial institution (not an exposed
  account number); identifiers are tokenized and routing is encrypted. **[HIGH for
  mapping; MEDIUM for crypto internals]**
- **Stakeholders & drivers:** sender (Customer Experience — "it goes to the right
  person"); recipient; the bank (Revenue Integrity — misroute is irreversible).
- **Customer outcome (works):** token resolves to the correct FI; payment proceeds.
- **Failure modes:** **send-to-wrong-token** (typo'd phone/email) → effectively
  unrecoverable (see 3.6 irrevocability); recipient **not enrolled** → "claim"
  flow (3.7); directory inconsistency across 2,000+ FIs; changed-bank/multi-token
  resolution ambiguity. **[HIGH for wrong-token & not-enrolled]**
- **Candidate Business-Health signal:** Directory Resolution Success Rate (APQC
  *Effectiveness*); Resolution Latency (APQC *Efficiency*).
- **Dependencies:** EWS directory; recipient-FI registration state.
- **Observable vs black-box:** resolve success/failure partially observable at the
  calling bank; **directory data model, consistency, failover = EWS black-box**.

### 3.3 Payment initiation & authorization (sender bank)

- **What it does:** the sender initiates and authorizes inside their own bank app;
  the sending bank debits the sender's *available balance*. Credit-push model —
  there is no debit-pull. **[HIGH]**
- **Stakeholders & drivers:** sender (Customer Experience — "my send succeeds");
  the bank (Service Reliability, Revenue Integrity).
- **Customer outcome (works):** funds debited, payment accepted into the network.
- **Failure modes:** **false declines / risk holds** blocking legitimate sends;
  **payment-limit-exceeded** declines (an expected decline, not a fault — must be
  separated in error rates); send failures during bank-core or processor outages;
  duplicate sends (double-debit). **[HIGH]**
- **Candidate Business-Health signal:** Send Authorization Success Rate (APQC
  *Effectiveness*), with **decline-reason decomposition** (fraud-hold vs limit vs
  NSF vs system-error — this distinction is essential and is a payments-prior-art
  point, §7); Send-to-Confirmation Latency (APQC *Efficiency*).
- **Provenance:** Zelle "typically available in minutes" UX promise; bank send
  limits (Zelle Rules / bank policy).
- **Dependencies:** sender bank core/ledger; risk engine (3.4); the EWS hub (3.5).
- **Observable vs black-box:** observable bank-side; this is where a bank's
  *Process* and *System* signals (Parts 3–4) will live — internal.

### 3.4 Risk / fraud / sanctions decisioning (inline, blocking)

- **What it does:** an inline, often *blocking* decision point — fraud scoring,
  velocity/first-time-recipient/large-amount holds (commonly cited ~1–3 business
  days, bank-specific), and sanctions/OFAC screening (real-time rails expect
  sub-200ms screening, 24/7). **[HIGH that holds exist; MEDIUM on durations;
  HIGH that sanctions screening is an inline gate generally]**
- **Stakeholders & drivers:** fraud/risk (Service Reliability); compliance
  (Regulatory Compliance — OFAC, AML); customer (Customer Experience — false
  declines hurt; missed fraud hurts more).
- **Customer outcome (works):** legitimate payment passes quickly; bad payment
  blocked.
- **Failure modes:** false positives (legitimate send held/blocked); false
  negatives (fraud passes — the core of every lawsuit: instant + irreversible +
  weak verification = "money already gone"); screening latency breaching the
  real-time SLA; a missed screen = compliance breach. **[HIGH]**
- **Candidate Business-Health signal:** Risk-Hold Rate + False-Decline Rate (APQC
  *Effectiveness/Adaptability*); Screening Decision Latency (APQC *Efficiency*);
  Fraud-Loss Rate (→ Business Impact, §6).
- **Provenance:** OFAC sanctions obligations; Reg E liability split; Zelle Rules
  reimbursement requirements (imposter-scam reimbursement since 2023-06-30).
- **Dependencies:** bank/EWS risk models; sanctions watchlists; the National
  Shared Database (EWS).
- **Observable vs black-box:** rates observable bank-side; **risk-engine
  thresholds/models = proprietary**.

### 3.5 Network routing & messaging (EWS hub)

- **What it does:** the EWS hub routes the payment message from sender FI to
  recipient FI — the central switch of the network. Zelle moves the *message*; the
  banks move the money. **[HIGH]**
- **Stakeholders & drivers:** both banks (Service Reliability); EWS (network
  integrity).
- **Customer outcome (works):** recipient FI is notified of the incoming payment.
- **Failure modes:** hub unavailability (network-wide blast radius); message
  loss/duplication; partial degradation affecting a subset of FIs (federated
  design → "two people get different results"). **[MEDIUM — public sources
  describe behavior, not mechanism]**
- **Candidate Business-Health signal:** (network-level) End-to-End Message Success
  Rate; Hub Availability. *Mostly an EWS-owned signal — a participating bank observes only its edge.*
- **Dependencies:** EWS hub; every participating FI's integration.
- **Observable vs black-box:** **EWS hub architecture, redundancy, SLA, throughput
  = entirely black-box**; no public uptime numbers or post-mortems.

### 3.6 Clearing & settlement (ACH / RTP / card rails)

- **What it does:** interbank settlement over existing rails — historically
  deferred-net **ACH** (end-of-day netting), **RTP** since Feb 2021 (instant,
  irrevocable, 24/7), and card rails. The receiving bank typically makes funds
  available in minutes while interbank settlement completes later → **"real-time
  UX over (often) batch settlement,"** with the receiving bank effectively
  fronting funds. **[HIGH for the model; MEDIUM for the characterization; rail-
  selection logic NOT public]**
- **Stakeholders & drivers:** receiving bank (Revenue Integrity / settlement risk
  — it fronts funds before settlement); both banks (Service Reliability).
- **Customer outcome (works):** money credited; interbank settlement reconciles.
- **Failure modes:** **the two-layer success gap** — payment "completes" to the
  customer but **fails to reconcile** at settlement (the single biggest payments
  observability blind spot, §7); settlement delays/finality differences by rail;
  ACH returns/reversals days later; shared-processor settlement faults (e.g.,
  **May 2025 Fiserv** outage; 2023 "manual error at The Clearing House"
  cascading into bank deposits + Zelle). **[HIGH]**
- **Candidate Business-Health / reconciliation signal:** Settlement Reconciliation
  Break Rate + Unreconciled-Aging (APQC *Effectiveness* — *new class the SUD
  should add*); Return/Reversal Rate (post-completion SLO).
- **Provenance:** Nacha ACH rules (settlement windows, return deadlines); TCH RTP
  operating rules (irrevocability, finality code ACSC).
- **Dependencies:** ACH operator, The Clearing House/RTP, card networks, the
  Federal Reserve; **processors (Fiserv, FIS, Jack Henry) — a concentration-risk
  layer**.
- **Observable vs black-box:** reconciliation observable bank-side *if
  instrumented*; **per-transaction rail selection, netting cadence, settlement
  funding arrangements = black-box**.

### 3.7 Receiving-bank posting & funds availability

- **What it does:** the recipient's **own** FI (not Zelle) performs the final
  internal account lookup and posts/credits the funds. If the recipient is not
  enrolled, the **claim flow** fires: funds are debited from sender and held; the
  recipient has **14 calendar days** to enroll and claim, else the payment is
  cancelled and refunded. **[HIGH]**
- **Stakeholders & drivers:** recipient (Customer Experience — "I got my money");
  receiving bank (Funds Availability / Reg CC; Revenue Integrity).
- **Customer outcome (works):** funds posted, typically within minutes.
- **Failure modes:** **money debited but not received** (recipient unenrolled →
  pending; or posting failure); **delayed posting** (the Jan 2023 BofA "missing
  money" incident — already-posted transactions disappeared and re-debited,
  overdrawing accounts); incoming-side fraud-review holds. **[HIGH]**
- **Candidate Business-Health signal:** Receive-Posting Success Rate (APQC
  *Effectiveness*); Time-to-Funds-Available (APQC *Efficiency*); Claim-Flow
  Completion Rate.
- **Provenance:** Reg CC funds-availability schedules (regulated SLA, not just UX);
  the 14-day claim window (Zelle Rules).
- **Dependencies:** receiving bank core/ledger; enrollment state; settlement (3.6).
- **Observable vs black-box:** observable at the receiving bank; cross-bank
  posting timing is **only partially observable** (the heart of the attribution
  problem).

### 3.8 Notification & confirmation

- **What it does:** both sender and recipient receive confirmations (in-app,
  email, SMS). For unenrolled recipients, the notification *is* the claim
  invitation. **[HIGH]**
- **Stakeholders & drivers:** both parties (Customer Experience — "I know it
  worked"); the bank (fraud-warning obligations — Zelle Rules mandate real-time
  warnings before transfers).
- **Failure modes:** notification not delivered / delayed → customer can't tell
  state (amplifies the "is it up?" confusion); missing pre-transfer fraud warning
  (a Rules-mandated control).
- **Candidate Business-Health signal:** Notification Delivery Rate / Latency (APQC
  *Efficiency*).
- **Dependencies:** SMS/email providers; in-app push.
- **Observable vs black-box:** observable bank-side.

### 3.9 Dispute / error resolution / reimbursement (post-completion)

- **What it does:** when a customer reports an error or fraud, the bank must
  investigate and (for covered cases) reimburse. This is where the **unauthorized
  vs. authorized** line decides who eats the loss. **[HIGH]**
- **Stakeholders & drivers:** victim customer (Customer Experience); compliance
  (Regulatory Compliance — Reg E); the bank (Revenue Integrity, reputational/
  regulatory exposure).
- **Failure modes:** missed Reg E investigation deadlines; under-reimbursement
  (the 38%/12% figures, the lawsuits); the **"scam gap"** — authorized-but-deceived
  payments generally fall outside Reg E coverage.
- **Candidate Business-Health / Impact signal:** Dispute Resolution Time vs the
  10-business-day / 45-day SLA (APQC *Efficiency*); Reimbursement Rate; Fraud/Scam
  Loss $ (→ Business Impact).
- **Provenance (strong, citable) — two distinct clocks, don't conflate:**
  *Resolution clock* (12 CFR **1005.11**): investigate within **10 business
  days**; if unresolved, up to **45 days** *with provisional credit*; the **90-day**
  extension applies **only** to new-account (within 30 days of first deposit),
  foreign-initiated, and POS-debit transfers — it is *not* the routine deadline.
  *Reporting clock* (12 CFR **1005.6**): the consumer must report within **60
  days** of the statement to preserve liability protection, which maps to the
  **$50 / $500 / unlimited** liability tiers. **[confirmed 2026-06-20]**
- **Dependencies:** dispute systems; EWS fraud data; reimbursement policy.
- **Observable vs black-box:** SLA adherence observable bank-side; outcomes are
  exactly what regulators probed because they were *not* transparently reported.

---

## 4. Public incident history

| # | Date | What happened | Root cause (disclosed) | Flow step | Conf. |
|---|------|---------------|------------------------|-----------|-------|
| 1 | Jan 18, 2023 | BofA Zelle transactions **disappeared**, balances dropped, some accounts overdrawn; "transactions Jan 14–17 may be delayed posting"; resolved ~3 PM | **Single-bank** (BofA) posting/ledger fault; network unaffected. Deeper mechanism never disclosed | receive-post / settlement reconciliation | HIGH |
| 2 | 2023 (Wells & others) | Missing deposits, overdrafts; Zelle/transfers also unavailable in online banking | **Upstream** "manual human error at The Clearing House" (ACH/deposits); Zelle a downstream casualty | settlement/clearing → cascade | MEDIUM |
| 3 | May 2, 2025 | "Payment pending"/failed sends across **Truist, Navy Federal, Chase, BofA**; backlogs lingering for days | **Shared processor Fiserv** internal error during a planned data-center enhancement; reportedly disrupted **60+ applications** (American Banker, single-source) | settlement / shared infrastructure | HIGH |

**The pattern that proves the observability thesis [HIGH]:**
- ├── Same customer symptom ("Zelle is down / my money's stuck") arises from
  *three different root layers*: a single bank's core (#1), an upstream clearing
  operator (#2), and a shared processor (#3).
- ├── Because Zelle lives inside each bank's app, customers — and often
  responders — **cannot distinguish** bank-fault from network-fault from
  processor-fault in real time. Downdetector spikes for *multiple banks* even when
  the Zelle network is fully operational.
- └── Attribution is resolved only **post-hoc** by a spokesperson ("the problem
  was with Bank of America"; "originated on the banks' side"; "Fiserv internal
  issue"). **There is no public, real-time, per-step signal showing what's up vs.
  down or where traffic flowed** — which is precisely the gap this effort names.

This is the strongest single argument for business observability on Zelle: the
need is not hypothetical, it is the documented, repeated public failure pattern.

---

## 5. Stakeholders & drivers (consolidated — SUD Part 2 seed)

A candidate stakeholder set for the Business-Health chains, derived from the flow:

| # | Stakeholder | Driver (q15a) | Impact category (q15) | What they expect (q12) |
|---|-------------|---------------|-----------------------|------------------------|
| 1 | Sender (consumer) | Customer Experience | customer_experience | My send succeeds, goes to the right person, completes in minutes |
| 2 | Recipient (consumer) | Funds Availability | customer_experience | I receive my money quickly and reliably |
| 3 | Small business payee | Revenue Integrity | financial | Payments arrive and reconcile; I can run my business on it |
| 4 | Receiving bank (treasury) | Settlement Risk | financial | Fronted funds settle and reconcile; no settlement breaks |
| 5 | Fraud / risk function | Service Reliability | operational | Bad payments blocked; false declines minimized |
| 6 | Compliance | Regulatory Compliance | legal_risk | Reg E deadlines met; OFAC screening enforced; reimbursement rules honored |
| 7 | Bank brand / leadership | Reputational Exposure | legal_risk / financial | No repeat of the lawsuits / Senate findings |

---

## 6. Business impact — the protected outcomes (SUD Part 2b seed)

| # | Impact magnitude | Source | Conf. |
|---|------------------|--------|-------|
| 1 | ~**$870M** cumulative consumer losses over 7 years (CFPB suit, filed Dec 20 2024, D. Arizona, under CFPA + EFTA/Reg E, vs EWS + JPM/BofA/Wells); suit **dismissed with prejudice early Mar 2025** (batch of Biden-era withdrawals) | CFPB | HIGH (confirmed 2026-06-20) |
| 2 | **>$1B** stolen 2017–2023 (NY AG suit vs EWS, Aug 13 2025); quote: faults "a quick registration process that lacked important verification steps" | NY AG | HIGH (confirmed 2026-06-20) |
| 3 | Reimbursement: big-3 reimbursed **fraud** ~**38%** ($64M of $166M disputes) in 2023, down from **62%** in 2019; **scam** ~**12%**; ~**$560M** in scam disputes rejected 2021–2023 | Senate PSI (Jul 2024) | MEDIUM — confirmed via outlets quoting the PSI PDF; PDF not directly read (see verification doc) |
| 4 | 2021: only ~**47%** of reported-fraud dollars returned (2021–1H2022); ~**90%** of scam (authorized-transfer) cases not repaid | Warren report (Oct 2022) | MEDIUM — confirmed via outlets quoting the Warren PDF; PDF not directly read (see verification doc) |
| 5 | Per-bank variance: same network, very different outcomes (e.g., Truist ~82% vs PNC ~14% of unauthorized claims) — evidence each bank's risk/dispute handling drives consumer outcome | Warren report | HIGH |
| 6 | Voluntary policy: since **2023-06-30**, Zelle Rules require reimbursing qualifying **imposter scams** (above Reg E); scope criticized as narrow/opaque | EWS / press | HIGH |

**Regulatory SLO provenance (citable, for q22a):**
- 12 CFR **1005.11** — *resolution clock*: investigate within 10 business days;
  up to 45 days with provisional credit; 90 days **only** for new-account,
  foreign-initiated, or POS-debit transfers (not the routine deadline). **[confirmed 2026-06-20]**
- 12 CFR **1005.6** — *reporting clock*: report within 60 days of statement to
  preserve protection; liability tiers $50 / $500 / unlimited. **[confirmed 2026-06-20]**
- **Reg CC** — funds-availability schedules; next-day availability threshold
  **$275** (raised from $225 effective July 1 2025). A *legally mandated* SLA — generic SLO
  frameworks don't know SLAs can be statutory). **[HIGH]**
- **Contrast / prior-art tangent:** the UK PSR **mandatory APP-fraud reimbursement
  regime** (live 2024-10-07): 50/50 sender/receiver PSP split, reimburse within 5
  business days, £85,000 cap; ~88% reimbursed in year one. The US has **no**
  equivalent federal mandate (the CFPB's litigated attempt was dropped). Useful as
  a "where the puck is going" reference and a contrast for why US reimbursement
  rates are low. **[HIGH]**

---

## 7. Payment-domain prior art the SUD doesn't yet name (candidate instrument additions)

The v2 instrument grounds in generic prior art (SLODLC, FMEA, ISO 22301 BIA, BIAN,
Golden Signals, USE, COSO, ArchiMate). Zelle is a *payments* system, and the
payment domain has established prior art that surfaces signals a generic
instrument misses. **Each of these is a candidate question/dimension to add to a
payments-aware onboarding instrument** (ranked by what the generic SUD would most
likely miss):

| # | Candidate addition | Prior art | Why the generic SUD misses it |
|---|--------------------|-----------|-------------------------------|
| 1 | **Two-layer success: message-acceptance vs settlement-reconciliation.** Require *both* a "completed" signal and a reconciliation-break / unreconciled-aging signal | ACH deferred-net settlement; nostro/settlement-break reconciliation | SUD treats "success" as one event; payments succeed at the message layer yet fail to reconcile. Biggest gap |
| 2 | **End-to-end correlation ID as a required tracing primitive** | ISO 20022 **UETR** (UUID constant across the chain) | SUD has no notion of a standardized cross-hop trace key; payments ship one natively |
| 3 | **Native status + reason-code taxonomy** | ISO 20022 **pacs.002** (ACCP/ACSP/ACSC/PDNG/RJCT + mandatory reason codes) | SUD invents custom statuses; payments have a standardized, observable status stream |
| 4 | **Irrevocability → pre-send safety gate.** Duplicate/erroneous detection must fire *before* transmission | RTP/FedNow irrevocability, finality code ACSC | SUD's signal model is detect-after-the-fact; on irrevocable rails a missed pre-send check is uncorrectable |
| 5 | **Duplicate-payment / idempotency signals** (duplicate-attempt rate, dedup-hit rate) | Idempotency keys; exactly-once *processing* | Generic distributed-systems idea, but elevating it to a *monitored payment signal* is payment-specific |
| 6 | **Inline, blocking compliance gates with latency + decline-reason decomposition** | OFAC/sanctions screening (<200ms, 24/7); fraud/AML scoring | SUD lumps declines into "errors"; payments need fraud vs limit vs sanctions vs NSF separated to read error rates |
| 7 | **Post-completion reversal/return rate as an SLO** | Nacha returns/reversals (deadlines up to 60 days) | SUD treats success as final at send; payments can reverse days later |
| 8 | **Regulated (statutory) SLAs as hard SLOs** | Reg CC funds availability; Reg E §1005.11 timing | SUD's q22a allows regulatory provenance but doesn't prompt that an SLA can be *legally mandated*, not just internal |
| 9 | **Continuous-operation + liquidity/funding-position monitoring** | RTP/FedNow 24/7/365 RTGS | USE/Golden Signals cover availability but not the continuous-liquidity dimension of instant rails |
| 10 | **Payment-specific capability decomposition template** | BIAN Payment Initiation / Payment Order / Payment Execution service domains | SUD uses BIAN coarsely; the payment service domains give a ready sub-capability map (cf. §3) |
| 11 | **Request-for-Payment as a distinct lifecycle** (decline/expiry/timeout states) | ISO 20022 pain.013/.014; RTP/FedNow RfP | SUD models a single credit-transfer happy path; RfP is a separate request/response lifecycle |

**Recommendation:** treat these as candidate additions to a payments-aware
onboarding instrument profile. Items 1–4 are the highest-value and most defensible.

---

## 8. Gaps → where a participating bank's internal teams are required (mapped to SUD questions)

Public research **cannot** fill these — they route to a bank's internal Zelle
implementation teams and the EWS relationship. This list doubles as the
"what we need from dev partners" input.

| # | SUD question(s) | What's needed | Why public can't supply it |
|---|-----------------|---------------|---------------------------|
| 1 | q4, q6, q6a | Business unit, product/technical owners, CMDB IDs | bank org facts |
| 2 | q8 | Existing Zelle telemetry / current dashboards (the incident-blindness gap itself) | bank-specific |
| 3 | q9, q30 | Dependency *wiring* + resilience behavior: how the bank's Zelle path calls EWS, core banking, fraud, the rails; circuit breakers/fallbacks | implementation-specific |
| 4 | Part 3 (diagnostic_*) | Process-layer signals grounded to the bank's implementation of each sub-capability (§3) | internal |
| 5 | Part 4 (use_dimension) | System-layer signals (MQ/DB/server) — the metric-derived-synthetics layer | internal |
| 6 | Part 5 (q31, q32) | Escalation ladder + alert routing | bank on-call |
| — | (EWS black-boxes from §3) | Hub architecture/SLA; directory token internals; per-transaction rail-selection; settlement netting cadence; risk-engine thresholds | proprietary to EWS even a member bank may not see |

The EWS black-boxes (last row) are worth naming explicitly: some dependencies
are opaque **even to a member bank**, which bounds what any observability effort
can promise and is itself a finding — the standard has to live where the data is
producible.

---

## 9. Sources

Grounding is search-summary-based (see §0 caveat). Representative primary and
secondary URLs surfaced by the research; **open directly to verify figures before
external use.**

**Network / scale / governance:** earlywarning.com (products, brands, RFI
response, press releases); zelle.com (FAQs, press); aba.com partner directory;
prnewswire.com (RTP-settlement 2021; $1T/$1.2T releases); theclearinghouse.org
(RTP); en.wikipedia.org/wiki/Zelle (orientation).

**Flow / settlement:** bank FAQs (bankofamerica.com, wellsfargo.com, chase,
usbank.com, regions.com, becu.org); alacriti.com; lightspark.com; frbservices.org
(FedNow/ISO 20022/Same-Day ACH); nacha.org.

**Incidents:** time.com, npr.org, gpb.org, bleepingcomputer.com (Jan 2023 BofA);
cnn.com, aol.com, paymentsdive.com, americanbanker.com, ainvest.com (May 2025
Fiserv); nbcnews.com, themirror.com (2023 Wells/TCH).

**Fraud / regulatory:** consumerfinance.gov (CFPB suit + enforcement page);
hsgac.senate.gov (PSI report Jul 2024); warren.senate.gov (Oct 2022 report);
ag.ny.gov (Aug 2025 complaint); cnbc.com, bankingdive.com, paymentsdive.com,
emarketer.com; pymnts.com, nbcnews.com (2023 imposter-scam reimbursement);
psr.org.uk, freshfields.com, hoganlovells.com (UK APP regime); law.cornell.edu /
ecfr.gov (12 CFR 1005).

**Payment-domain prior art:** frbservices.org (ISO 20022, FedNow settlement
guide/operating procedures); cashbook.com, cpg.de, nexusglobalpayments.org
(pacs/pain messages); nacha.org (returns/reversals, Same Day ACH); crossriver.com,
eascorp.org (RTP vs FedNow); batonsystems.com, greshamtech.com, smart.stream
(reconciliation/settlement-break); stripe/adyen idempotency writeups; bian.org
(service domains); federalreserve.gov (Reg CC); workfusion.com, feedzai.com
(sanctions/transaction screening).
