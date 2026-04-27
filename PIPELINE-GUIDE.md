# BOS Onboarding Pipeline

## What this is

The BOS onboarding pipeline takes a service from "no business observability" to "deployed business health dashboard with live telemetry." It is one chain with six stages:

```
Sources (docs, code, ops history)
  → Capture (SUD — structured understanding about the service)
    → Validate (quality gate — completeness, citations, reasoning depth)
      → Load (BOS app — managed service profile with stakeholders, signals, impacts)
        → Factory (service profile → Grafana dashboard JSON)
          → Deploy (live dashboard querying real datasources)
```

The **service profile in the app** is the stable contract. Everything upstream produces it; everything downstream consumes it. The factory never sees raw sources — it operates on the data model.

The factory currently produces **dashboards**. The same data model will feed alert configs, runbooks, playbooks, and signal specs as those factories are built.

## The pipeline's capabilities

### Capture — producing a SUD

The pipeline's input is a YAML file called a **Service Understanding Document (SUD)**. It draws from the ITIL Service Design Package (observability requirements) and SLODLC Discover (structured stakeholder and signal elicitation). It captures who depends on the service, what "healthy" means in business terms, what breaks when it fails, and what signals measure those expectations. You produce one by answering 49 questions about your service.

The question set (`onboard/sud-questions.md`) is organized by what it captures, not by the data model it feeds. Each question carries guidance on how to answer well and identifies the data model fields it populates.

The `/bos-onboard` skill facilitates AI-assisted capture — given source material about a service, it structures the answers into a validated SUD. The human provides domain understanding; the AI handles format and completeness. `golden-fixture/pitstop-workshop-mgmt-sud.yaml` is a complete example.

Every answer requires source citations (`[S1:]`, `[S2:]`) and reasoning. This isn't bureaucratic overhead — it's provenance. When someone six months from now asks "why is the SLO target 95%?", the citation chain traces back to the specific document, metric, or conversation that justified it.

### Validate — quality gate

Validation confirms the SUD is complete, structurally correct, and meets quality standards before the pipeline will accept it. Three checks:

- **Structure** — YAML parses, all required fields present, values match allowed types and enums
- **Completeness** — required sections populated, signal definitions have SLO targets and query definitions
- **Quality** — reasoning fields cite sources, reasoning meets minimum depth (30 words), provenance vocabulary used correctly

```bash
python onboard/validate_sud.py <sud.yaml>
```

Passes: `Validation passed: syntax OK, schema OK, quality OK`

Fails with actionable errors identifying the field and what's wrong:

| Error type | Example |
|------------|---------|
| `SYNTAX ERROR` | Bad YAML indentation at line 42 |
| `SCHEMA ERROR` | `signals[0]` missing required `slo_target` |
| `QUALITY ERROR` | No `[Sn:]` citations in reasoning field |
| `QUALITY WARNING` | Reasoning under 30 words (advisory) |

### Load — populating the data model

Loading transforms the SUD into the BOS app's data model and stores it as a managed service profile. The service's stakeholders, signals, impacts, traceability mappings, and operational metadata become structured, queryable entities in the app.

```bash
python onboard/ingest_sud.py <sud.yaml>
```

The app's import endpoint (`POST /api/v1/services/import`) handles this as an atomic operation — it either succeeds completely or changes nothing. Loading a service that already exists replaces it.

After loading, the service profile is accessible through the app's API and UI:
- **API:** `GET /api/v1/services/<service-id>/export` returns the full profile
- **UI:** `http://localhost:4301` — browse to the service for visual confirmation

Use `--org-id` and `--app-id` flags when the app's reference data doesn't match the SUD's values. Use `--base-url` if the app isn't at the default `http://localhost:5000`.

### Factory — producing artifacts

The dashboard factory reads a service profile from the app and produces a Grafana dashboard with panels for each signal, organized by business relevance:

1. **Business Health** — the signals that directly measure stakeholder expectations
2. **Business Impact** — what breaks in business terms when the service fails
3. **Process** — decomposed process-level indicators
4. **System** — infrastructure and platform signals

```bash
curl -s http://localhost:5000/api/v1/services/<service-id>/export > profile.json
python dashboard/generate_service_dashboard.py profile.json --output dashboard.json
```

Each signal's queries run against the datasource defined in the service profile. The factory is datasource-agnostic — Prometheus, Splunk, AppDynamics, and others are supported through `dashboard/datasource-config.yaml`, which maps datasource types to Grafana datasource UIDs in your environment.

### Deploy — live observability

The factory's output is a deployable Grafana dashboard. Deployment is part of the pipeline's scope — configuration that isn't deployed and populated with real telemetry hasn't demonstrated anything.

```bash
curl -X POST "http://<grafana-host>/api/dashboards/db" -H "Content-Type: application/json" -H "Authorization: Bearer <your-api-key>" -d @dashboard.json
```

The deployed dashboard is at `http://<grafana-host>/d/bos-factory-<service-id>`.

**The acceptance test is not "did the dashboard deploy." It's: can a service owner look at this dashboard and answer "is my business healthy?" with confidence.** Business Health signals at the top should show meaningful SLO status. Business Impact panels should show what's at stake. If the dashboard answers infrastructure questions instead of business questions, the onboarding failed — regardless of whether the pipeline ran cleanly.

## Verification

After the pipeline completes, check three things:

1. **Data integrity** — export the service profile (`/api/v1/services/<service-id>/export`) and confirm stakeholders, signals, impacts, and their traceability connections are present
2. **Dashboard structure** — the Grafana dashboard has panels organized by observability layer with Business Health at the top, not System metrics
3. **Live telemetry** — signal panels show data from the actual datasources, not empty panels or placeholder queries

## Environment

- **Python 3.8+** with `pip install pyyaml jsonschema requests`
- **BOS app** running at `http://localhost:5000` (backend) and optionally `http://localhost:4301` (UI)
- **Grafana** with `gapit-htmlgraphics-panel` plugin installed

All pipeline commands assume you are in the `bos-factory/` directory.

**Quick environment check** — validate an included example:

```bash
python onboard/validate_sud.py golden-fixture/pitstop-workshop-mgmt-sud.yaml
```

Expected: `Validation passed: syntax OK, schema OK, quality OK`

## Maintaining the pipeline

After changing the question set (`onboard/sud-questions.yaml`) or SUD schema (`schema/sud-schema.json`), confirm alignment:

```bash
python onboard/validate_coverage_sud.py
```

After changing questions, regenerate the human-readable guide:

```bash
python onboard/generate_docs.py
```

The datasource config (`dashboard/datasource-config.yaml`) is deployment-specific — edit it to match the Grafana datasource UIDs in each environment where dashboards will be deployed.
