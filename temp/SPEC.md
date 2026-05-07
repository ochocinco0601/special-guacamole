# BOSS Pipeline Journey Report — Build Specification

You are an AI agent adding a progressive pipeline execution dashboard to the existing `/bos-onboard` e2e pipeline. Your repo already has the pipeline runner (`run_pipeline.py`, `orchestrator.py`, `models.py`, `ensure_env.py`, `stages.py`). This spec tells you what to add and what to modify.

## Transfer package contents

| File | Action |
|------|--------|
| `journey_report.py` | **NEW** — add to `runner/src/`. The complete HTML generator. Drop in as-is. |
| `example-pipeline-report.html` | **REFERENCE** — open in browser to see the exact target output. Not deployed, just for understanding. |
| `SPEC.md` | **THIS FILE** — read fully before starting. |

## Modifications to existing files

| Existing file | What to change |
|---------------|----------------|
| `runner/src/models.py` | Add `bos_ui_url: str = ""` field to `PipelineContext` |
| `runner/src/ensure_env.py` | Add BOS UI port discovery (§6). Add `bos_ui_ok` + `bos_ui_url` to `EnvStatus`. |
| `runner/src/orchestrator.py` | Add `on_stage_complete` callback parameter to `run_pipeline()` (§7). Pipe discovered `bos_ui_url` into `ctx`. Add BOS UI preflight check. |
| `runner/src/run_pipeline.py` | Import `journey_report`. Wire progressive callback. Print journey path before pipeline. Add journey HTML to `commit_artifacts`. |
| `/bos-onboard` skill | Step 0: create skeleton + present URL + open browser. Step 6: tell user to refresh. (§8, §9) |

---

## 1. What you're building and why

Every `/bos-onboard` invocation will produce a **single self-contained HTML file** that shows pipeline progress from the moment onboarding starts. The user opens it at Step 0 (before capture), watches stages light up as the pipeline executes, and has a persistent record when it finishes — whether it passed, failed, or crashed mid-run.

This replaces the flat post-hoc table report as the primary consumer artifact. The existing `generate_report()` call and its output stay — both reports are produced. Do not remove the old report generation.

**Output file:** `{sud_directory}/{serviceId}-sud-pipeline.html` — fully self-contained, no external CSS/JS/CDN dependencies. Opens in any browser offline.

---

## 2. Product frame — what success looks like

The BOSS pipeline takes a service from "we have source material" to "live business observability dashboard in Grafana" in a single `/bos-onboard` invocation. That's 7 stages, multiple tools, multiple APIs, minutes of execution. Today the user has no visibility into this process — they wait for terminal output and hope it works.

**The consumer** is the person who triggered onboarding. They need to answer one question at any moment: *Where are we?* And when it's done: *Did it work? Where are my artifacts?*

**Success looks like this:** The user invokes `/bos-onboard`. Immediately — before any capture or processing — a browser tab opens showing the pipeline dashboard with all 7 stages dimmed and "NOT STARTED." They can see what's coming. Minutes later, when the mechanical pipeline runs, they refresh and watch stages light up green one by one. If something fails, they see exactly where — which stage, what error, what stderr. If the pipeline crashes without completing, the dashboard already shows what succeeded before the crash. When everything passes, every artifact has a clickable link: the SUD View, the BOSS app service page, the Grafana dashboard.

**The pipeline dashboard IS the product.** It's not a debugging tool or a log viewer. It's the consumer's experience of what BOSS does. A stakeholder seeing this for the first time understands: source material goes in, structured understanding comes out, and a live dashboard appears — with full traceability of every step.

**Failure of this feature** is: the dashboard exists but the consumer still has to ask the AI "what happened?" or read terminal logs to understand pipeline state. If they need anything beyond opening the HTML file and looking at it, we haven't succeeded.

---

## 3. The data contract

The HTML embeds a single `DATA` JSON object. The JavaScript renders everything from this object. This is the interface — populate it from your pipeline context and stage results.

```json
{
  "service_name": "Invoice Service",
  "service_id": "pitstop-invoice",
  "sud_meta": {
    "business_unit": "Pitstop Garage",
    "business_purpose_display": "Generates and sends invoices for completed maintenance jobs — the garage's revenue collection mechanism."
  },
  "timestamp": "2026-05-07 12:56:58 UTC",
  "overall_status": "PASSED",
  "sources": [
    {
      "id": "S1",
      "path": "pitstop/docs/arc42/01-introduction-and-goals.md",
      "type": "descriptive",
      "desc": "Requirements overview, quality goals, stakeholders"
    }
  ],
  "stages": [
    {
      "name": "capture",
      "status": "passed",
      "duration": 0,
      "artifact": { "label": "Sources", "action": "toggleSources" }
    },
    {
      "name": "validate",
      "status": "passed",
      "duration": 0.3,
      "artifact": { "label": "SUD YAML", "path": "pitstop-invoice-sud.yaml" }
    },
    {
      "name": "render",
      "status": "passed",
      "duration": 0.2,
      "artifact": { "label": "SUD View", "path": "pitstop-invoice-sud-view.html" }
    },
    {
      "name": "load",
      "status": "passed",
      "duration": 0.4,
      "artifact": { "label": "BOSS App", "path": "http://localhost:4200/services/pitstop-invoice" }
    },
    {
      "name": "export",
      "status": "passed",
      "duration": 0.0,
      "artifact": { "label": "Profile JSON", "path": "pitstop-invoice-sud-profile.json" }
    },
    {
      "name": "factory",
      "status": "passed",
      "duration": 0.2,
      "artifact": { "label": "Dashboard JSON", "path": "pitstop-invoice-sud-dashboard.json" }
    },
    {
      "name": "deploy",
      "status": "passed",
      "duration": 0.1,
      "artifact": { "label": "Grafana", "path": "http://localhost:3000/d/bos-factory-pitstop-invoice/..." }
    }
  ]
}
```

### Field sources — where each value comes from

| Field | Source |
|-------|--------|
| `service_name` | SUD YAML → `metadata.display_name` (fallback: `metadata.service_name`) |
| `service_id` | SUD YAML → `metadata.service_id` |
| `business_unit` | SUD YAML → `service.business_unit` (NOT `metadata.`) |
| `business_purpose_display` | SUD YAML → `service.business_purpose_display` (NOT `metadata.`) |
| `timestamp` | `datetime.now(UTC)` formatted as `YYYY-MM-DD HH:MM:SS UTC` |
| `overall_status` | Derived (see §3) |
| `sources[]` | SUD YAML → `sources` array |
| `stages[].status` | From each `StageResult.status`: `"passed"`, `"failed"`, or `"not-reached"` |
| `stages[].duration` | From `StageResult.duration_seconds`, rounded to 1 decimal |
| `stages[].artifact` | Only present when `status == "passed"` (see §4 for per-stage mapping) |
| `stages[].error` | Only present when `status == "failed"` — first 500 chars of error message |
| `stages[].stderr` | Only present when `status == "failed"` — first 2000 chars of stderr |

---

## 4. Status badge derivation

```
if any stage has status "failed"       → "FAILED"
elif any stage has status "not-reached" → "IN PROGRESS"
elif all stages have status "passed"   → "PASSED"
```

The skeleton (before pipeline runs) uses `"NOT STARTED"`.

The `overall_status` JSON value is always one of: `PASSED`, `FAILED`, `IN PROGRESS`, `NOT STARTED`. The rendered badge appends the stage name for failures (e.g., "FAILED at Load") — this is display-only, derived from `stages[]` by the JavaScript, not stored in the data.

---

## 5. The 7 stages — artifact mapping

Each stage has a fixed artifact link when it passes. The Capture stage is special — it uses a JS action instead of a URL.

| # | Stage name | Description | Artifact label | Artifact link |
|---|-----------|-------------|---------------|---------------|
| 1 | Capture | Register service, identify sources | Sources | `{"action": "toggleSources"}` — calls JS function |
| 2 | Validate | Schema + referential integrity | SUD YAML | `{serviceId}-sud.yaml` (relative file path) |
| 3 | Render | Human-readable SUD view | SUD View | `{serviceId}-sud-view.html` (relative file path) |
| 4 | Load | Ingest to BOSS app | BOSS App | `{discovered_bos_ui_url}/services/{serviceId}` |
| 5 | Export | Export service profile | Profile JSON | `{serviceId}-sud-profile.json` (relative file path) |
| 6 | Factory | Profile → dashboard JSON | Dashboard JSON | `{serviceId}-sud-dashboard.json` (relative file path) |
| 7 | Deploy | Deploy to Grafana | Grafana | `{discovered_grafana_url}/d/{dashboard_uid}/...` |

**Duration display rule:** Capture (stage index 0) always shows `"done"`. All other stages show `"X.Xs"` (even `"0.0s"`). Not-reached stages show `"—"`. Failed stages show `"failed"`.

**Capture's "Sources" link:** When clicked, toggles a collapsible sources panel below the stage dots. The panel contains a table of all source materials from the SUD (id, path, type, description) with a summary row showing counts by type.

---

## 6. URL discovery — runtime, not config

All URLs in artifact links must be **discovered at runtime** during preflight, not hardcoded:

| Service | Discovery method |
|---------|-----------------|
| BOSS app API | Check reachability at configured base URL (e.g. `localhost:5000/api/v1/services`) |
| BOSS UI | Probe ports 4200, 4201, 4202 in order — first reachable wins. This is the Angular frontend, separate process from the API. |
| Grafana | Check configured URL. If unreachable, detect Docker dynamic port mapping via `docker port grafana 3000`. |

Discovered URLs flow into the pipeline context. The journey report reads them from context when building artifact links. If the BOSS UI isn't found, omit the link (don't produce a broken URL).

---

## 7. Progressive rendering — the core mechanic

The report is written to disk **after every stage completes**, not once at the end. Full HTML rewrite each time — the same file path, overwritten.

### Integration pattern

Your pipeline orchestrator needs a callback hook:

```python
def run_pipeline(ctx, on_stage_complete=None):
    results = []
    for i, stage in enumerate(STAGES):
        result = stage.run(ctx)
        results.append(result)

        if result.status == "failed":
            # Mark remaining stages as not-reached
            for remaining in STAGES[i + 1:]:
                results.append(StageResult(name=remaining.name, status="not-reached"))

        # PROGRESSIVE WRITE — this is the key addition
        if on_stage_complete:
            on_stage_complete(results)

        if result.status == "failed":
            break
    return results
```

The caller wires it:

```python
journey_path = sud_path.parent / f"{sud_stem}-pipeline.html"

def on_stage_complete(results_so_far):
    all_results = [capture_result] + results_so_far
    write_journey_report(all_results, ctx, journey_path)

results = run_pipeline(ctx, on_stage_complete=on_stage_complete)

# Final write with definitive status
write_journey_report([capture_result] + results, ctx, journey_path, overall_status="PASSED" or "FAILED")
```

The file is valid HTML at every intermediate write. The user refreshes the browser to see stages light up.

### Commit the journey report

After the pipeline completes, include the journey HTML in the git commit alongside other artifacts (SUD, view, profile, dashboard JSON, old report).

---

## 8. Skeleton at Step 0

**Before capture begins** — at the very start of `/bos-onboard` — create a skeleton report:

- Service name and ID from user input (the SUD doesn't exist yet)
- All 7 stages as `"not-reached"` (dimmed)
- Status badge: `"NOT STARTED"`
- Empty sources (SUD not written yet)
- Collapsible reference sections (collapsed by default)

The skill must do two things with it:
1. **Present the file URL to the user in chat** (as a `file:///` URL)
2. **Open it in the browser** so the user sees the dashboard immediately

The user watches from Step 0. The pipeline overwrites this file progressively at Step 6.

---

## 9. Skill integration sequence

| Step | What happens with the journey report |
|------|--------------------------------------|
| 0 (pre-flight) | Create skeleton HTML. Present URL in chat. Open in browser. |
| 1-4 (capture) | No changes — skeleton sits at NOT STARTED |
| 5 (validate) | No changes — still NOT STARTED |
| 6 (pipeline) | Each stage overwrites the HTML. User refreshes to see progress. |
| 6 (complete) | Final write with PASSED/FAILED. Journey HTML committed to git. |

---

## 10. Exact modifications to existing files

### 10a. `runner/src/models.py` — add one field

Add `bos_ui_url` to `PipelineContext`:

```python
@dataclass
class PipelineContext:
    sud_path: Path
    base_url: str = "http://localhost:5000"
    bos_ui_url: str = ""          # ← ADD THIS — populated at runtime by preflight
    grafana_url: str = ""
    # ... rest unchanged
```

### 10b. `runner/src/ensure_env.py` — add BOS UI discovery

Add port probe list and `bos_ui_ok`/`bos_ui_url` to `EnvStatus`:

```python
BOS_UI_PORTS = [4200, 4201, 4202]

@dataclass
class EnvStatus:
    bos_app_ok: bool
    bos_app_url: str
    bos_ui_ok: bool              # ← ADD
    bos_ui_url: str              # ← ADD
    grafana_ok: bool
    grafana_url: str
    grafana_api_key: str
    messages: list
```

In `ensure_env()`, add between the BOS app check and the Grafana check:

```python
    # BOS UI
    bos_ui_ok = False
    bos_ui_url = ""
    for port in BOS_UI_PORTS:
        candidate = f"http://localhost:{port}"
        if _is_reachable(candidate):
            bos_ui_ok = True
            bos_ui_url = candidate
            messages.append(f"[OK] BOS UI reachable: {bos_ui_url}")
            break
    if not bos_ui_ok:
        messages.append(f"[WARN] BOS UI not found on ports {BOS_UI_PORTS}")
```

Include `bos_ui_ok` and `bos_ui_url` in the returned `EnvStatus`.

### 10c. `runner/src/orchestrator.py` — add callback + pipe UI URL

Add callback parameter to `run_pipeline`:

```python
from typing import Callable, Optional

OnStageComplete = Callable[[list[StageResult]], None]

def run_pipeline(ctx, on_stage_complete=None):    # ← ADD parameter
    results = []
    for i, stage in enumerate(STAGES):
        result = stage.run(ctx)
        results.append(result)

        if result.status == "passed":
            print(f"OK ({result.duration_seconds:.1f}s)")
        else:
            print(f"FAILED")
            for remaining in STAGES[i + 1:]:
                results.append(StageResult(
                    name=remaining.name, description=remaining.description,
                    status="not-reached",
                ))

        if on_stage_complete:               # ← ADD — call after every stage
            on_stage_complete(results)

        if result.status == "failed":
            break
    return results
```

In `run_preflight`, after `ctx.grafana_url = status.grafana_url`, add:

```python
    ctx.bos_ui_url = status.bos_ui_url

    checks.append(PreflightResult("BOS UI", status.bos_ui_ok, status.bos_ui_url or "not found"))
```

### 10d. `runner/src/run_pipeline.py` — wire progressive reporting

Add import:

```python
from journey_report import write_journey_report
```

After preflight, before the `run_pipeline` call, create the capture result. Capture represents work already done (the AI produced the SUD). It's always `"passed"` with duration `0` — it's a bookkeeping entry, not a stage the runner executes:

```python
    capture_result = StageResult(
        name="capture", description="SUD capture (/bos-onboard)",
        status="passed", duration_seconds=0,
        artifacts={"sud_path": str(ctx.sud_path)},
    )

    journey_path = ctx.sud_path.parent / f"{ctx.sud_path.stem}-pipeline.html"
    print(f"  Journey: {journey_path}")

    def on_stage_complete(results_so_far):
        all_so_far = [capture_result] + results_so_far
        write_journey_report(all_so_far, ctx, journey_path)
```

Pass the callback:

```python
    results = run_pipeline(ctx, on_stage_complete=on_stage_complete)
```

After the pipeline completes, final write:

```python
    write_journey_report(all_results, ctx, journey_path, overall_status=overall)
```

Print the journey path at the end:

```python
    print(f"Journey: {journey_path}")
```

Add journey to `commit_artifacts` — add `journey_path` to the file list:

```python
def commit_artifacts(ctx, report_path, journey_path):
    files_to_commit = [str(ctx.sud_path), str(report_path), str(journey_path)]
    # ... rest unchanged
```

### 10e. `/bos-onboard` skill — Step 0 and Step 6 updates

**Step 0** — after pre-flight, before reading any sources:

Create the skeleton report:
```python
from journey_report import write_skeleton_report
write_skeleton_report(
    Path('golden-fixture/{serviceId}-sud-pipeline.html'),
    service_id='{serviceId}',
    service_name='{Service Display Name}',
)
```

Present URL in chat AND open in browser for the user.

**Step 6** — before running the pipeline, tell user:
> "The journey report is updating — refresh your browser to see stages light up."

The pipeline's progressive callback handles the rest.

---

## 11. Error panel structure

When a stage fails, an error panel auto-appears below the stage dots:

```
┌─────────────────────────────────────────────────────────┐
│  4. Load — FAILED                                       │  ← stage number + name, red
│                                                         │
│  SQLite Error 19: FOREIGN KEY constraint failed         │  ← error message, white
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Import failed: 500 Server Error for url: ...      │  │  ← stderr in pre block, muted
│  │ Microsoft.Data.Sqlite.SqliteException (0x80004005)│  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

Error message is capped at 500 chars. Stderr is capped at 2000 chars.

---

## 12. Collapsible reference sections

Two sections below the pipeline, **both collapsed by default**:

### "The pipeline — stage by stage" (product frame)

7-column grid aligned with the stages above. Each column contains scannable chunks describing what the stage does and what it produces:

| Capture | Validate | Render | Load | Export | Factory | Deploy |
|---------|----------|--------|------|--------|---------|--------|
| Source material → structured understanding | Every claim verified against sources | Readable view of what BOSS understood | Service enters the BOSS data model | Portable service profile extracted | Profile → complete Grafana dashboard | Dashboard live in Grafana |
| Business purpose, stakeholders, dependencies | Signal definitions checked for completeness | Each answer shows where it came from | Signals, stakeholders, dependencies — live | Everything factories need in one contract | Business health panels with real queries | Panels connected to real telemetry |
| Signals, failure modes, operations | Broken references caught, not propagated | Extracted, inferred, or constructed — visible | Queryable, comparable, actionable | Signal definitions, thresholds, context | Organized by four-layer model | Business health visible at a glance |
| Every answer traced to a source | Quality gate before entering BOSS | Review artifact for service owners | Document becomes operational data | Standard shape — any factory can consume | Datasource-agnostic — Prometheus, Splunk, etc. | From source material to live observability |
| **Produces:** SUD YAML | **Produces:** Approved SUD | **Produces:** SUD View HTML | **Produces:** BOSS app record | **Produces:** Profile JSON | **Produces:** Dashboard JSON | **Produces:** Live dashboard |

### "System components — how the factory works" (technical frame)

Same 7-column grid. Each column lists the implementation components:

| Capture | Validate | Render | Load | Export | Factory | Deploy |
|---------|----------|--------|------|--------|---------|--------|
| AI agent | Python script | Python script | Python script → HTTP POST | HTTP GET | Python script | HTTP POST |
| /bos-onboard skill | onboard/validate_sud.py | onboard/render_sud.py | onboard/ingest_sud.py | BOSS app API: /api/v1/services/{id}/export | generate_service_dashboard.py | Grafana API: /api/dashboards/db |
| Reads arc42 docs, source code, config | JSON Schema + referential integrity | SUD YAML → static HTML | BOSS app API: /api/v1/services/import | Normalized ServiceExportDto | Profile JSON → Grafana dashboard JSON | Bearer token auth |
| Structured prompting → SUD YAML | Checks source citations, signal refs | Jinja-style template rendering | Atomic upsert — service + signals + deps | Profile JSON written to disk | Datasource-agnostic query templates | Returns dashboard URL + UID |

---

## 13. Visual design specification

### Color tokens

```
--bg:          #0F172A    (page background)
--card:        #1E293B    (card/panel background)
--card-border: #334155    (borders)
--text:        #F1F5F9    (primary text)
--muted:       #94A3B8    (secondary text)
--subtle:      #64748B    (labels, dimmed text)
--red:         #EF4444    (failed status)
--amber:       #F59E0B    (running status, source IDs)
--teal:        #14B8A6    (links, artifact labels)
--green:       #10B981    (passed status)
```

### Typography

- Headings/body: `'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Code/data: `'IBM Plex Mono', 'JetBrains Mono', Consolas, monospace`

### Layout

- Max width: 1280px, centered
- Three stacked sections separated by 20px gap:
  1. Service identity strip (card background)
  2. Pipeline section (bg background with border) — stages + error + sources + run context
  3. Two collapsible reference sections

### Stage dots

- 48px circles, 3px border, numbered 1-7 in monospace
- Connected by a 2px horizontal line at the circle center
- Green border = passed, red border = failed, 25% opacity = not reached

### BOSS branding (top-left of service strip)

```
BOSS                                          (1.1rem, bold)
Business Observability Standard & System      (0.82rem, subtle)
AI-driven pipeline                            (0.75rem, subtle italic)
```

Separated from service details by a 1px vertical border.

### Timestamp

Stored as UTC in a `data-utc` attribute. JavaScript converts to viewer's local timezone on page load using `toLocaleString` with `timeZoneName: 'short'`. Displays e.g. "5/7/2026, 8:13:56 AM CDT".

### Source type badges

- `definitional` → teal tint background, teal text
- `descriptive` → muted tint background, muted text
- `behavioral` → amber tint background, amber text

---

## 14. What NOT to build

- No websocket or live-reload — the user refreshes manually
- No maturity chevrons or maturity model — that concept is not ready
- No re-run command — the AI agent is the orchestrator
- No fabricated quality metrics — only show data computed from real sources
- No total pipeline duration — summed stage durations ≠ wall-clock time
- No standalone artifacts grid — every artifact is linked under its stage

---

## 15. Verification

After building, verify:

1. **Skeleton state:** Create with a service ID and no SUD. All 7 stages dimmed. Status: NOT STARTED. Opens in browser without errors.
2. **Passed state:** Run the pipeline against a valid SUD. All 7 stages green with durations and artifact links. Status: PASSED. BOSS App link points to discovered UI URL. Grafana link points to actual dashboard.
3. **Failed state:** Simulate a failure at Load (e.g. stop the BOSS app). Stages 1-3 green, stage 4 red with error panel, stages 5-7 dimmed. Status: FAILED at Load.
4. **Progressive state:** Mid-pipeline, open the file. Shows completed stages green, remaining dimmed. Status: IN PROGRESS.
5. **Sources panel:** Click "Sources" under Capture. Panel toggles open showing source table with type badges.
6. **Collapsible sections:** Both reference sections start collapsed. Click headers to expand/collapse.
7. **Timestamp:** Shows in viewer's local timezone, not UTC.
8. **Links open in new tabs:** All artifact links use `target="_blank"`.
