# Service Understanding Document — Ledger-Writer Service (v2)

**Instrument:** `onboard/sud-questions-v2.yaml` (motivation chain capture)
**Pipeline version:** 2.0
**Service:** boa-ledger-writer
**Date:** 2026-05-27
**Purpose:** Coverage fixture — exercises all APQC dimensions, all impact categories, multi-stakeholder chains. Replaces checkout-v2-sud.md as the golden fixture.

---

## Sources

| ID | Source | Type |
|---|---|---|
| S1 | Bank of Anthos source code (`src/ledger/ledgerwriter/`) | Behavioral |
| S2 | Bank of Anthos README.md and docs/ | Descriptive |
| S3 | Kubernetes manifests (`kubernetes-manifests/ledger-writer.yaml`) | Definitional |
| S4 | Cross-service spike (`design/sud-needs-decomposition-spike.md`) | Analytical |
| S5 | Prometheus/Grafana extras (`extras/prometheus/`, `extras/metrics-dashboard/`) | Descriptive |

---

## Part 1 — Service Context

### q1: What does this service do?
Accepts and validates customer payment transactions before writing them to the
bank's ledger. Acts as the transaction acceptance gate — enforces authorization,
balance sufficiency, duplicate prevention, and format validation before any
money moves.
*Provenance: extracted [S1: LedgerWriterController.java, TransactionValidator.java]*

### q2: Name
- **Service ID:** boa-ledger-writer
- **Display name:** Ledger-Writer Service
*Provenance: extracted [S2, S3]*

### q3: Tier
Tier 1 — critical path for all payment transactions. Ledger-writer failure
blocks 100% of customer payment activity. No fallback or degraded mode exists.
Regulatory exposure: every transaction must produce an auditable record.
*Provenance: inferred from [S1: no fallback path in controller], extracted [S4: critical dependency analysis]*

### q4: Business unit
Bank of Anthos — Payments
*Provenance: extracted [S2]*

### q5: Functional category
Transaction Processing — validates and persists financial transactions.
*Provenance: extracted [S2: "Accepts and validates transactions before writing to ledger"]*

### q6: Ownership
- **Product owner:** Payments PO
- **Technical owner:** Ledger Team
*Provenance: inferred from [S2: service organization]*

### q6a: CMDB identifiers
- **Org ID:** BOA-PAYMENTS
- **App ID:** APP-LEDGER-WRITER
*Provenance: constructed — demo app has no CMDB*

### q6b: Tags
payments, ledger, critical-path, financial-services, regulatory

### q8: Custom telemetry
Spring Boot Actuator metrics via Micrometer. JVM memory (`jvm/memory/used`),
Tomcat HTTP metrics (request count, response time, connection pool), Hibernate
JPA statistics, Guava cache hit/miss rates (GuavaCacheMetrics). Stackdriver
metrics registry configured with k8s resource labels. Spring Cloud Sleuth
tracing at 100% sampling rate when enabled.
*Provenance: extracted [S1: LedgerWriterApplication.java metrics config, application.properties]*

### q9: Dependencies
Frontend → Ledger-Writer → {Balance-Reader (HTTP sync), Ledger-DB (JPA sync)}
User-Service → JWT public key (startup-only, mounted via secret)

Critical dependencies:
- **Balance-Reader** (HTTP, sync): Required for all internal (same-bank) transactions. Failure returns HTTP 500 — blocks ALL local payments. No circuit breaker, no timeout override, no fallback.
- **Ledger-DB** (PostgreSQL, JPA): Required for transaction persistence. Failure returns HTTP 500. No write-ahead or queue — synchronous write or fail.
- **JWT public key** (startup): Loaded once from PUB_KEY_PATH. Missing key = pod won't start. No runtime rotation.

Non-critical:
- **Stackdriver metrics** (optional): Disabled if ENABLE_METRICS=false.
- **Tracing** (optional): Disabled if ENABLE_TRACING=false.
*Provenance: extracted [S1: LedgerWriterController.java, LedgerWriterApplication.java]*

### q10: Failure modes
1. **Balance-Reader unavailable** — ResourceAccessException caught, returns HTTP 500. Blocks all local transactions. Cascade: frontend sees 500, customer can't send money. Detectable via transaction_success_rate drop correlated with balance_check_latency spike.
2. **Database write failure** — CannotCreateTransactionException caught, returns HTTP 500. Transaction not persisted. Detectable via transaction_success_rate and ledger_write_latency.
3. **JWT validation failure** — Invalid or expired token, returns HTTP 401. Single-user impact. Detectable via payment_validation_rate (auth step).
4. **Duplicate transaction** — Guava cache hit on requestUuid, returns HTTP 400. Correct behavior — but cache is per-pod, not distributed. Pod restart loses cache → duplicates possible on client retry.
5. **Insufficient balance** — Balance check fails, returns HTTP 400. Expected business logic. BUT: eventual consistency in balance-reader cache means two rapid payments can both pass → overdraft.
6. **Format validation failure** — Account/routing format invalid, returns HTTP 400. Client error, not system failure.
*Provenance: extracted [S1: LedgerWriterController.java exception handling], extracted [S4: precondition violation analysis]*

### q34-q36: Business capability
- **Capability:** Payment Transaction Acceptance (banking domain — BIAN: Payment Execution service domain)
- **Sole implementation:** Yes — single transaction acceptance gate in this architecture
- **What persists:** The need to validate and record payment transactions with authorization, balance sufficiency, and deduplication. If ledger-writer is replaced, the 6-step validation chain and audit trail requirement transfer.
*Provenance: extracted [S1], inferred [S2: BIAN alignment]*

### q37-q39: Flow participation
- **Process:** Send Payment (customer-to-customer funds transfer)
- **Step:** Transaction Acceptance (step 2 of initiate→validate→persist→update-balances→confirm)
- **Blocking:** Yes — ledger-writer failure blocks the entire payment pipeline
- **Downstream impact:** No transaction persisted → balance-reader never sees it → customer sees stale balance → payment appears lost
*Provenance: extracted [S4: Send Payment flow analysis]*

### q40-q43: Internal flow decomposition
Three distinct sub-capabilities:
1. **Transaction Validation** — JWT auth, format checks, sender authentication, business rules (amount > 0, no self-send). Steps 1-6 of the validation chain.
2. **Balance Verification** — HTTP call to balance-reader, sufficiency check. Step 7. Only for internal (same-bank) transactions.
3. **Ledger Persistence** — JPA write to ledger-db, deduplication cache update.

Telemetry distinguishes them: validation errors return HTTP 400 with distinct messages; balance check failures return HTTP 500 (dependency) or 400 (insufficient); persistence failures return HTTP 500. Span-level metrics differentiate the steps.
*Provenance: extracted [S1: LedgerWriterController.java, TransactionValidator.java]*

---

## Part 2 — Stakeholder Motivation Chains

*observabilityLayer: "Business Health" (structural — all signals in this part)*

### Chain 1: Bank Customers

**Stakeholder:** Bank Customers
**Expectation:** Payments complete successfully, quickly, and without double-charging
**Priority:** CRITICAL
*Provenance: inferred from [S2: "simulates a payment processing network", S4: "Can customers send money?"]*

**Driver:** Payment Reliability
**Impact category:** customer_experience
**Documentation:** Ledger-writer is the only path for customers to send money. Every payment goes through this service — there is no alternative channel, no degraded mode, no retry queue. When ledger-writer fails, customers experience immediate, total payment inability. The banking relationship depends on payment reliability more than any other single function.
**When violated:** Customers unable to send money, payment appears to fail or hang, potential double-charges from deduplication gaps, loss of trust in the platform, account closure
*Provenance: extracted [S1: no fallback in controller], inferred [S4: critical path analysis]*

**Coverage gate:** Three Business Health signals verify this expectation:
- Transaction Success Rate → APQC Effectiveness (are payments completing?)
- Transaction Processing Duration p95 → APQC Efficiency (fast enough?)
- Payment Volume Capacity Headroom → APQC Adaptability (can it handle payroll day?)

#### Signal: Transaction Success Rate
- **APQC Dimension:** Effectiveness
- **Signal type:** sli_ratio
- **Signal name:** transaction_success_rate
- **Business description:** Percentage of customer payment attempts that complete successfully
- **Technical description:** Ratio of HTTP 200 responses from /transactions endpoint to total POST requests. Includes all rejection reasons (auth, validation, balance, duplicate) in the denominator. Excludes health check and readiness probe traffic.
- **SLO target:** 99.5% (≥)
- **Target rationale:** At ~200 transactions/hour during normal load, 0.5% budget allows ~1 failure/hour. Banking tolerance: occasional failure acceptable if visible and recoverable. Sustained degradation triggers regulatory scrutiny.
- **Requirement source:** Internal SLO — Bank of Anthos Payments Team, informed by banking industry payment success benchmarks
- **Health thresholds:** Warning: 98.0%, Critical: 97.0%
- **Alerting:** Warning: 99.0%, Page: 97.0%
- **Time window:** 30d rolling
- **Budgeting:** occurrences
- **Queries:**
  - Numerator: `sum(rate(http_server_requests_seconds_count{service="ledgerwriter",uri="/transactions",status="200"}[5m]))`
  - Denominator: `sum(rate(http_server_requests_seconds_count{service="ledgerwriter",uri="/transactions",method="POST"}[5m]))`
- **Data source:** Prometheus
*Provenance: extracted [S1: controller endpoint], inferred [S4: composite health definition "success ≥ 99%"]*

#### Signal: Transaction Processing Duration p95
- **APQC Dimension:** Efficiency
- **Signal type:** sli_threshold
- **Signal name:** transaction_processing_duration_p95
- **Business description:** 95th percentile time from payment submission to confirmation
- **Technical description:** p95 of HTTP POST /transactions duration histogram. Includes JWT validation, format validation, balance check (HTTP call to balance-reader), and database write. Long tail from balance-reader latency and database contention.
- **SLO target:** 2000ms (<)
- **Target rationale:** Banking payment UX research: customers expect sub-2-second payment confirmation. Beyond 2 seconds, uncertainty ("did it go through?") drives duplicate submissions — which stresses the deduplication cache.
- **Requirement source:** Internal SLO — Bank of Anthos Payments Team, informed by UX research on payment confirmation latency
- **Health thresholds:** Warning: 1500ms, Critical: 2000ms
- **Alerting:** Warning: 1500ms, Page: 3000ms
- **Time window:** 30d rolling
- **Budgeting:** time_slices
- **Query:** `histogram_quantile(0.95, sum(rate(http_server_requests_seconds_bucket{service="ledgerwriter",uri="/transactions",method="POST"}[5m])) by (le)) * 1000`
- **Data source:** Prometheus
*Provenance: inferred [S4: composite health "latency < 2000ms"]*

#### Signal: Payment Volume Capacity Headroom
- **APQC Dimension:** Adaptability
- **Signal type:** sli_threshold
- **Signal name:** payment_volume_capacity_headroom
- **Business description:** How much room the payment system has to absorb transaction volume increases — current transactions per second as a percentage of tested maximum capacity
- **Technical description:** Ratio of current 5-minute average TPS to the service's rated capacity (determined by load testing). Rated capacity accounts for the full validation chain including the synchronous balance-reader call. When headroom drops below 20%, the system cannot absorb typical volume spikes (payroll days, month-end, promotional events) without degradation.
- **SLO target:** 80 (<)
- **Target rationale:** 20% headroom is the minimum buffer for absorbing volume spikes without SLO degradation. Banking transaction patterns are cyclical — payroll days see 2-3x baseline volume, month-end sees 1.5-2x. Below 20% headroom, any volume spike pushes the system past capacity, causing latency degradation that cascades to success rate.
- **Requirement source:** Internal SLO — Bank of Anthos Platform Engineering, informed by capacity planning discipline (Hixson, "Capacity Planning for Web Services")
- **Requirement source URL:** null
- **Health thresholds:** Warning: 70%, Critical: 80%
- **Alerting:** Warning: 70%, Page: 85%
- **Time window:** 30d rolling
- **Budgeting:** time_slices
- **Query:** `(sum(rate(http_server_requests_seconds_count{service="ledgerwriter",uri="/transactions",method="POST"}[5m])) / on() group_left() ledgerwriter_rated_capacity_tps) * 100`
- **Data source:** Prometheus
*Provenance: constructed — no existing capacity signal; derived from cross-service spike finding that balance-reader dependency is the bottleneck*

---

### Chain 2: Compliance & Risk Management

**Stakeholder:** Compliance & Risk Management
**Expectation:** Every processed transaction produces a complete, auditable record; no unauthorized transactions are accepted
**Priority:** CRITICAL
*Provenance: inferred from [S1: validation chain includes JWT auth + sender authentication check]*

**Driver:** Regulatory Compliance
**Impact category:** legal_risk
**Documentation:** Financial transaction processing is subject to regulatory requirements (BSA/AML, Reg E, SOX controls). Every transaction must produce an immutable audit trail — who sent, who received, what amount, when, and the authorization chain. Gaps in the audit trail are examination findings. The 6-step validation chain exists to prevent unauthorized transactions, but the audit trail requirement goes beyond validation — even correctly rejected transactions must be logged.
**When violated:** Regulatory examination findings, BSA/AML reporting gaps, consent order risk, mandatory incident disclosure, potential enforcement action
*Provenance: inferred from [S1: validation logic implies regulatory requirement], constructed [banking domain knowledge — regulatory requirements are inherent]*

**Coverage gate:** One Business Health signal verifies this expectation:
- Transaction Audit Completeness → APQC Effectiveness (does every transaction produce a complete audit record?)

#### Signal: Transaction Audit Completeness
- **APQC Dimension:** Effectiveness
- **Signal type:** sli_ratio
- **Signal name:** transaction_audit_completeness
- **Business description:** Percentage of processed transactions (accepted or rejected) that produce a complete audit record with all required fields: sender, receiver, amount, timestamp, authorization chain, and disposition
- **Technical description:** Ratio of transaction log entries with all required audit fields populated to total transaction attempts. Measures completeness of the structured log/database record, not just whether the transaction was processed. Includes rejected transactions — the audit trail must show WHY a transaction was rejected, not just that it was.
- **SLO target:** 99.99% (≥)
- **Target rationale:** Regulatory: zero tolerance for audit gaps in practice, but 99.99% allows for infrastructure-level log loss (network partition, disk full). At 200 txn/hour, 0.01% budget = ~0.5 gaps/day. Any gap triggers investigation.
- **Requirement source:** Regulatory — BSA/AML transaction record requirements, SOX IT general controls for financial record integrity
- **Requirement source URL:** null
- **Health thresholds:** Warning: 99.95%, Critical: 99.9%
- **Alerting:** Warning: 99.95%, Page: 99.9%
- **Time window:** 30d rolling
- **Budgeting:** occurrences
- **Queries:**
  - Numerator: `sum(rate(ledgerwriter_audit_records_complete_total{service="ledgerwriter"}[5m]))`
  - Denominator: `sum(rate(http_server_requests_seconds_count{service="ledgerwriter",uri="/transactions",method="POST"}[5m]))`
- **Data source:** Prometheus
*Provenance: inferred from [S1: transaction validation produces structured responses], constructed [banking regulatory domain knowledge]*

---

### Chain 3: Finance & Treasury

**Stakeholder:** Finance & Treasury
**Expectation:** Ledger balances are accurate — no duplicate entries, no missing transactions, reconciliation closes daily
**Priority:** HIGH
*Provenance: inferred from [S4: overdraft risk from cache staleness, S1: Guava dedup cache]*

**Driver:** Financial Integrity
**Impact category:** financial
**Documentation:** The ledger is the system of record for all account balances. Duplicate transactions inflate balances; missing transactions deflate them. The Guava deduplication cache is per-pod and expires after 1 hour — pod restarts or multi-replica deployments create windows for duplicate writes. Finance reconciles daily; every discrepancy requires manual investigation that delays close.
**When violated:** Customer balance errors, overdraft exposure from eventual consistency, daily reconciliation failures, manual correction costs, potential financial restatement
*Provenance: extracted [S1: Guava cache TTL = 1 hour, per-pod], extracted [S4: "two rapid payments both pass balance check"]*

**Coverage gate:** One Business Health signal verifies this expectation:
- Duplicate Prevention Rate → APQC Effectiveness (are duplicates being caught?)

#### Signal: Duplicate Prevention Rate
- **APQC Dimension:** Effectiveness
- **Signal type:** sli_ratio
- **Signal name:** duplicate_prevention_rate
- **Business description:** Percentage of duplicate payment attempts that are correctly identified and rejected before ledger write
- **Technical description:** Ratio of correctly rejected duplicate transaction UUIDs to total duplicate attempts (same UUID submitted more than once within the cache TTL). Measures the Guava cache deduplication mechanism. Known limitation: cache is per-pod, not distributed. Pod restart or cross-replica retry is a blind spot — this signal measures cache effectiveness, not absolute deduplication.
- **SLO target:** 99.9% (≥)
- **Target rationale:** At scale, even 0.1% duplicate leakage means ~5 duplicate transactions/day requiring manual reversal. Each reversal is a customer-impacting event and a reconciliation break.
- **Requirement source:** Internal SLO — Finance & Treasury reconciliation requirement, informed by Guava cache architecture constraints
- **Health thresholds:** Warning: 99.5%, Critical: 99.0%
- **Alerting:** Warning: 99.5%, Page: 99.0%
- **Time window:** 30d rolling
- **Budgeting:** occurrences
- **Queries:**
  - Numerator: `sum(rate(ledgerwriter_duplicate_rejected_total{service="ledgerwriter"}[5m]))`
  - Denominator: `sum(rate(ledgerwriter_duplicate_attempts_total{service="ledgerwriter"}[5m]))`
- **Data source:** Prometheus
*Provenance: extracted [S1: Guava cache dedup in LedgerWriterController], inferred [S4: dedup gap analysis]*

---

### Chain 4: Payments Operations

**Stakeholder:** Payments Operations
**Expectation:** Transaction failures are visible and diagnosable within 15 minutes; the system handles volume changes without manual intervention
**Priority:** HIGH
*Provenance: inferred from [S1: error handling patterns, S4: cascading failure analysis]*

**Driver:** Operational Continuity
**Impact category:** operational
**Documentation:** Payments Operations monitors and responds to payment system health. When ledger-writer degrades, the first question is "what broke and how bad?" The 6-step validation chain produces distinct error messages for each failure type, but there is no composite health signal — operators must correlate individual metrics to determine overall payment system state. The balance-reader dependency is the single largest operational risk: when it degrades, ALL local transactions fail, but the failure surfaces as an HTTP 500 from ledger-writer, not a clear dependency signal.
**When violated:** Blind spots in payment health, manual investigation backlog, SLA breaches on incident response time, cascading failures from undetected dependency degradation
*Provenance: inferred from [S1: error handling, no composite health], extracted [S4: balance-reader cascading failure]*

**Coverage gate:** Transaction Success Rate (from Chain 1) also verifies this expectation — when it degrades, Operations must respond. Payment Volume Capacity Headroom (from Chain 1) also serves Operations — capacity planning is an operational concern. No additional BH signal needed; existing signals serve this chain through shared traceability.

---

## Part 2b — Business Impact Assessments

*observabilityLayer: "Business Impact" (structural)*

### Impact: Customers Affected
- **Signal name:** customers_affected
- **Assesses Drivers:** Payment Reliability (Bank Customers)
- **Impact category:** customer_experience
- **Impact unit:** customers/hour
- **Business description:** Count of unique customers experiencing payment failures per hour. Derived from transaction failure rate and unique sender accounts in failed transactions.
- **Escalation:** Hour 1: ~12 customers affected at baseline volume. Hour 4: cumulative impact triggers exec notification. Hour 24: customer complaint volume triggers regulatory attention.
*Provenance: inferred from [S1: transaction volume, S4: baseline analysis]*

### Impact: Revenue at Risk
- **Signal name:** revenue_at_risk
- **Assesses Drivers:** Payment Reliability (Bank Customers), Financial Integrity (Finance & Treasury)
- **Impact category:** financial
- **Impact unit:** $/hour
- **Business description:** Estimated dollar value of failed payment transactions per hour. Based on average transaction value and failure rate. Includes both direct loss (failed payments) and indirect cost (manual reconciliation, customer compensation).
- **Escalation:** Hour 1: ~$2,400/hour at baseline. Hour 4: cumulative $9,600+ triggers Finance escalation. Hour 24: material financial impact requiring disclosure.
*Provenance: constructed [derived from transaction volume × average value × failure rate]*

### Impact: Regulatory Exposure Hours
- **Signal name:** regulatory_exposure_hours
- **Assesses Drivers:** Regulatory Compliance (Compliance & Risk Management)
- **Impact category:** legal_risk
- **Impact unit:** hours
- **Business description:** Cumulative hours where transaction audit completeness is below regulatory threshold. Each hour of gap accumulates exposure — regulators measure duration of non-compliance, not just occurrence. Triggers mandatory incident reporting at defined thresholds.
- **Escalation:** Hour 1: Internal compliance notification. Hour 4: Mandatory compliance officer briefing. Hour 24: Regulatory reporting obligation triggered.
*Provenance: constructed [banking regulatory domain knowledge — duration-based exposure assessment]*

### Impact: Manual Investigation Backlog
- **Signal name:** manual_investigation_backlog
- **Assesses Drivers:** Operational Continuity (Payments Operations)
- **Impact category:** operational
- **Impact unit:** investigations/hour
- **Business description:** Rate of payment failures requiring manual investigation by operations staff. Each failed transaction without clear diagnostic context generates an investigation ticket. At sustained rates, backlog exceeds team capacity and response SLAs breach.
- **Escalation:** Hour 1: ~6 investigations queued (manageable). Hour 4: 24+ investigations — exceeds single-operator capacity. Hour 24: 144+ investigations — backlog requires additional staffing.
*Provenance: inferred from [S1: error handling produces diagnostic context], constructed [operational staffing model]*

---

## Part 3 — Developer Diagnostic Signals

*observabilityLayer: "Process" (structural — all signals in this part)*

### Signal: Payment Validation Rate
- **Golden Signal Dimension:** Errors
- **Sub-capability:** Transaction Validation
- **Causal links:** Helps explain Transaction Success Rate failures (validation failures are a direct cause of payment rejection — auth errors, format errors, business rule violations)
- **Signal type:** sli_ratio
- **Signal name:** payment_validation_rate
- **Business description:** Percentage of payment attempts that pass all validation checks (auth, format, business rules) before reaching the balance check step
- **Technical description:** Ratio of transactions that pass the 6-step validation chain (steps 1-6) to total transaction attempts. Excludes balance check (step 7) — a transaction that passes validation but fails balance check is a validation success. Measures the gate, not the outcome.
- **SLO target:** 99.5% (≥)
- **Requirement source:** Internal SLO — Ledger Team
- **Health thresholds:** Warning: 98.0%, Critical: 97.0%
- **Alerting:** Warning: 99.0%, Page: 97.0%
- **Time window:** 30d rolling
- **Budgeting:** occurrences
- **Queries:**
  - Numerator: `sum(rate(ledgerwriter_validation_passed_total{service="ledgerwriter"}[5m]))`
  - Denominator: `sum(rate(http_server_requests_seconds_count{service="ledgerwriter",uri="/transactions",method="POST"}[5m]))`
- **Data source:** Prometheus
- **Owner:** Ledger Team
*Provenance: extracted [S1: TransactionValidator.java — 6-step chain]*

### Signal: Balance Check Latency p95
- **Golden Signal Dimension:** Latency
- **Sub-capability:** Balance Verification
- **Causal links:** Helps explain Transaction Processing Duration p95 (balance check is the synchronous HTTP dependency — its latency directly adds to total transaction time). Also helps explain Transaction Success Rate when balance-reader is unavailable (HTTP 500 from ResourceAccessException).
- **Signal type:** sli_threshold
- **Signal name:** balance_check_latency_p95
- **Business description:** 95th percentile time to verify the sender has sufficient balance for the transaction
- **Technical description:** p95 of HTTP GET to balance-reader /balances/{account_num} endpoint. Only fires for internal transactions (fromRoutingNum == LOCAL_ROUTING_NUM). External transactions skip this step. Timeout behavior: relies on RestTemplate defaults — no explicit timeout configured.
- **SLO target:** 500ms (<)
- **Requirement source:** Internal SLO — Ledger Team, derived from transaction_processing_duration_p95 budget allocation
- **Health thresholds:** Warning: 300ms, Critical: 500ms
- **Alerting:** Warning: 300ms, Page: 1000ms
- **Time window:** 30d rolling
- **Budgeting:** time_slices
- **Query:** `histogram_quantile(0.95, sum(rate(http_client_requests_seconds_bucket{service="ledgerwriter",uri="/balances/{accountNum}"}[5m])) by (le)) * 1000`
- **Data source:** Prometheus
- **Owner:** Ledger Team
*Provenance: extracted [S1: LedgerWriterController.java — balance check HTTP call]*

### Signal: Ledger Write Latency p95
- **Golden Signal Dimension:** Latency
- **Sub-capability:** Ledger Persistence
- **Causal links:** Helps explain Transaction Processing Duration p95 (database write time is a component of total transaction time). Helps explain Transaction Success Rate when database is degraded (CannotCreateTransactionException).
- **Signal type:** sli_threshold
- **Signal name:** ledger_write_latency_p95
- **Business description:** 95th percentile time to write a validated transaction to the ledger database
- **Technical description:** p95 of JPA transactionRepository.save() duration. Measures the PostgreSQL write path including connection acquisition from the HikariCP pool, Hibernate entity persistence, and transaction commit.
- **SLO target:** 200ms (<)
- **Requirement source:** Internal SLO — Ledger Team, derived from transaction_processing_duration_p95 budget allocation
- **Health thresholds:** Warning: 100ms, Critical: 200ms
- **Alerting:** Warning: 100ms, Page: 500ms
- **Time window:** 30d rolling
- **Budgeting:** time_slices
- **Query:** `histogram_quantile(0.95, sum(rate(spring_data_repository_invocations_seconds_bucket{service="ledgerwriter",method="save"}[5m])) by (le)) * 1000`
- **Data source:** Prometheus
- **Owner:** Ledger Team
*Provenance: extracted [S1: transactionRepository.save() in controller]*

### Signal: Transaction Request Rate
- **Golden Signal Dimension:** Traffic
- **Sub-capability:** (service-wide)
- **Causal links:** Helps explain Payment Volume Capacity Headroom (request rate is the numerator of the capacity ratio). Traffic spikes that exceed capacity headroom cause latency and error rate degradation.
- **Signal type:** sli_threshold
- **Signal name:** transaction_request_rate
- **Business description:** Incoming payment transaction requests per second — the volume of demand on the payment system
- **Technical description:** Rate of HTTP POST requests to /transactions endpoint per second. Includes all outcomes (success, validation failure, balance failure, error). Measures demand, not throughput.
- **SLO target:** null (informational — no target on traffic volume, but used as input to capacity headroom calculation)
- **Requirement source:** Capacity planning — monitoring signal, not SLO-bearing
- **Health thresholds:** Warning: null, Critical: null
- **Alerting:** Warning: null, Page: null
- **Time window:** 5m rolling average
- **Budgeting:** N/A
- **Query:** `sum(rate(http_server_requests_seconds_count{service="ledgerwriter",uri="/transactions",method="POST"}[5m]))`
- **Data source:** Prometheus
- **Owner:** Ledger Team
*Provenance: extracted [S1: single endpoint]*

---

## Part 4 — Platform Infrastructure Signals

*observabilityLayer: "System" (structural — all signals in this part)*

### Signal: Ledger-Writer Availability
- **USE Dimension:** Errors
- **Signal type:** sli_ratio
- **Signal name:** ledger_writer_availability
- **Business description:** Percentage of time the ledger-writer service is accepting and processing requests
- **Technical description:** Derived from Kubernetes readiness probe success rate (GET /ready). Measures infrastructure availability: can the service accept connections? Distinct from transaction_success_rate which measures business outcomes.
- **SLO target:** 99.9% (≥)
- **Requirement source:** Internal SLO — Bank of Anthos Platform Engineering
- **Health thresholds:** Warning: 99.5%, Critical: 99.0%
- **Alerting:** Warning: 99.5%, Page: 99.0%
- **Time window:** 30d rolling
- **Budgeting:** time_slices
- **Queries:**
  - Numerator: `sum(rate(up{service="ledgerwriter",job="kubernetes-pods"}[5m]))`
  - Denominator: `count(up{service="ledgerwriter",job="kubernetes-pods"})`
- **Data source:** Prometheus
- **Owner:** Platform Team
*Provenance: extracted [S3: readiness probe config]*

### Signal: Ledger-Writer CPU Utilization
- **USE Dimension:** Utilization
- **Signal type:** sli_threshold
- **Signal name:** ledger_writer_cpu_utilization
- **Business description:** CPU usage relative to allocated limits — measures how hard the service is working relative to its resource budget
- **Technical description:** Ratio of actual CPU seconds consumed to CPU limit (500m = 0.5 cores). JVM workload: JWT verification (crypto), JSON serialization, HTTP client calls, JPA entity mapping. JVM_OPTS constrain heap to 256m-512m.
- **SLO target:** 70 (<)
- **Requirement source:** Internal SLO — Platform Engineering capacity planning standard
- **Health thresholds:** Warning: 60%, Critical: 70%
- **Alerting:** Warning: 60%, Page: 80%
- **Time window:** 30d rolling
- **Budgeting:** time_slices
- **Query:** `(sum(rate(container_cpu_usage_seconds_total{container="ledgerwriter"}[5m])) / sum(kube_pod_container_resource_limits{container="ledgerwriter",resource="cpu"})) * 100`
- **Data source:** Prometheus
- **Owner:** Platform Team
*Provenance: extracted [S3: resource limits CPU 500m]*

### Signal: Ledger-DB Connection Pool Saturation
- **USE Dimension:** Saturation
- **Signal type:** sli_threshold
- **Signal name:** ledger_db_connection_pool_saturation
- **Business description:** How full the database connection pool is — when saturated, new transactions queue waiting for a connection, causing latency spikes and timeouts
- **Technical description:** Ratio of active HikariCP connections to maximum pool size. Default Spring Boot HikariCP pool: 10 connections max. Each transaction holds a connection for the duration of the JPA save. Connection pool saturation is the leading indicator of database-side bottleneck before transaction failures begin.
- **SLO target:** 80 (<)
- **Requirement source:** Internal SLO — Platform Engineering, informed by HikariCP operational guidance
- **Health thresholds:** Warning: 60%, Critical: 80%
- **Alerting:** Warning: 60%, Page: 90%
- **Time window:** 5m rolling
- **Budgeting:** time_slices
- **Query:** `(sum(hikaricp_connections_active{service="ledgerwriter"}) / sum(hikaricp_connections_max{service="ledgerwriter"})) * 100`
- **Data source:** Prometheus
- **Owner:** Platform Team
*Provenance: extracted [S1: Spring Data JPA + HikariCP default], extracted [S3: PostgreSQL datasource config]*

---

## Part 5 — Operational Context

### q30: Dependency flow
Frontend → Ledger-Writer → {Balance-Reader (HTTP sync), Ledger-DB (PostgreSQL sync)}
User-Service → JWT public key (startup mount only)
*Provenance: extracted [S1, S3]*

### q31: Escalation policy
P1: Page payments on-call → 15min: Escalate to ledger team lead → 30min: Escalate to payments engineering manager → 4hr: Compliance officer notification (if audit completeness impacted)
*Provenance: constructed — demo app has no escalation policy; modeled on banking incident management*

### q32: Alert routing
#payments-alerts (operational), #compliance-alerts (audit completeness breaches)
*Provenance: constructed*

---

## Coverage Verification

### APQC Dimension Coverage (Business Health)
| Dimension | Signals | Count |
|-----------|---------|-------|
| Effectiveness | Transaction Success Rate, Transaction Audit Completeness, Duplicate Prevention Rate | 3 |
| Efficiency | Transaction Processing Duration p95 | 1 |
| Adaptability | Payment Volume Capacity Headroom | 1 |
| **Total** | | **5** |

### Impact Category Coverage (Business Impact)
| Category | Signal | Stakeholder |
|----------|--------|-------------|
| customer_experience | Customers Affected | Bank Customers |
| financial | Revenue at Risk | Bank Customers, Finance & Treasury |
| legal_risk | Regulatory Exposure Hours | Compliance & Risk Management |
| operational | Manual Investigation Backlog | Payments Operations |
| **Total** | | **4** |

### Golden Signal Coverage (Process)
| Dimension | Signals | Count |
|-----------|---------|-------|
| Errors | Payment Validation Rate | 1 |
| Latency | Balance Check Latency p95, Ledger Write Latency p95 | 2 |
| Traffic | Transaction Request Rate | 1 |
| Saturation | (uncovered — saturation at Process layer captured at System via DB pool) | 0 |
| **Total** | | **4** |

### USE Coverage (System)
| Dimension | Signals | Count |
|-----------|---------|-------|
| Errors | Ledger-Writer Availability | 1 |
| Utilization | Ledger-Writer CPU Utilization | 1 |
| Saturation | Ledger-DB Connection Pool Saturation | 1 |
| **Total** | | **3** |

### Stakeholder Coverage
| Stakeholder | Priority | Impact Category | BH Signals | Impact Signals |
|-------------|----------|----------------|------------|----------------|
| Bank Customers | CRITICAL | customer_experience | 3 (success, duration, capacity) | 1 (customers_affected) |
| Compliance & Risk | CRITICAL | legal_risk | 1 (audit completeness) | 1 (regulatory_exposure_hours) |
| Finance & Treasury | HIGH | financial | 1 (duplicate prevention) | 1 (revenue_at_risk) |
| Payments Operations | HIGH | operational | 0 (served by Chain 1 signals via shared traceability) | 1 (manual_investigation_backlog) |

### Grand Total: 16 signals across 4 layers
- Business Health: 5
- Business Impact: 4
- Process: 4
- System: 3
