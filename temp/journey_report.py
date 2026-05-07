"""Progressive journey report — writes HTML after each pipeline stage."""

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

from models import PipelineContext, StageResult


STAGE_LABELS = ["Capture", "Validate", "Render", "Load", "Export", "Factory", "Deploy"]
STAGE_DESCS = [
    "Register service, identify sources",
    "Schema + referential integrity",
    "Human-readable SUD view",
    "Ingest to BOSS app",
    "Export service profile",
    "Profile → dashboard JSON",
    "Deploy to Grafana",
]

STAGE_GUIDE = [
    {"name": "Capture", "produces": "SUD YAML", "chunks": [
        "Source material → structured understanding",
        "Business purpose, stakeholders, dependencies",
        "Signals, failure modes, operations",
        "Every answer traced to a source",
    ]},
    {"name": "Validate", "produces": "Approved SUD", "chunks": [
        "Every claim verified against sources",
        "Signal definitions checked for completeness",
        "Broken references caught, not propagated",
        "Quality gate before entering BOSS",
    ]},
    {"name": "Render", "produces": "SUD View HTML", "chunks": [
        "Readable view of what BOSS understood",
        "Each answer shows where it came from",
        "Extracted, inferred, or constructed — visible",
        "Review artifact for service owners",
    ]},
    {"name": "Load", "produces": "BOSS app record", "chunks": [
        "Service enters the BOSS data model",
        "Signals, stakeholders, dependencies — live",
        "Queryable, comparable, actionable",
        "Document becomes operational data",
    ]},
    {"name": "Export", "produces": "Profile JSON", "chunks": [
        "Portable service profile extracted",
        "Everything factories need in one contract",
        "Signal definitions, thresholds, context",
        "Standard shape — any factory can consume",
    ]},
    {"name": "Factory", "produces": "Dashboard JSON", "chunks": [
        "Profile → complete Grafana dashboard",
        "Business health panels with real queries",
        "Organized by four-layer model",
        "Datasource-agnostic — Prometheus, Splunk, etc.",
    ]},
    {"name": "Deploy", "produces": "Live dashboard", "chunks": [
        "Dashboard live in Grafana",
        "Panels connected to real telemetry",
        "Business health visible at a glance",
        "From source material to live observability",
    ]},
]

TECH_GUIDE = [
    {"name": "Capture", "chunks": [
        "AI agent", "/bos-onboard skill",
        "Reads arc42 docs, source code, config",
        "Structured prompting → SUD YAML",
    ]},
    {"name": "Validate", "chunks": [
        "Python script", "onboard/validate_sud.py",
        "JSON Schema + referential integrity",
        "Checks source citations, signal refs",
    ]},
    {"name": "Render", "chunks": [
        "Python script", "onboard/render_sud.py",
        "SUD YAML → static HTML",
        "Jinja-style template rendering",
    ]},
    {"name": "Load", "chunks": [
        "Python script → HTTP POST", "onboard/ingest_sud.py",
        "BOSS app API: /api/v1/services/import",
        "Atomic upsert — service + signals + deps",
    ]},
    {"name": "Export", "chunks": [
        "HTTP GET", "BOSS app API: /api/v1/services/{id}/export",
        "Normalized ServiceExportDto",
        "Profile JSON written to disk",
    ]},
    {"name": "Factory", "chunks": [
        "Python script", "generate_service_dashboard.py",
        "Profile JSON → Grafana dashboard JSON",
        "Datasource-agnostic query templates",
    ]},
    {"name": "Deploy", "chunks": [
        "HTTP POST", "Grafana API: /api/dashboards/db",
        "Bearer token auth", "Returns dashboard URL + UID",
    ]},
]


def _load_sud_meta(sud_path: Path) -> dict:
    try:
        with open(sud_path, encoding="utf-8") as f:
            sud = yaml.safe_load(f)
    except Exception:
        return {"sources": [], "service_name": "", "service_id": "",
                "business_unit": "", "business_purpose_display": ""}

    meta = sud.get("metadata", {})
    svc = sud.get("service", {})
    sources = sud.get("sources", [])
    return {
        "service_name": meta.get("display_name") or meta.get("service_name", ""),
        "service_id": meta.get("service_id", ""),
        "business_unit": svc.get("business_unit", ""),
        "business_purpose_display": svc.get("business_purpose_display", ""),
        "sources": sources,
    }


def _e(text: str) -> str:
    return html.escape(str(text)) if text else ""


def _build_stages_json(results: list[StageResult], ctx: PipelineContext) -> list[dict]:
    stage_artifacts = {
        "capture": {"label": "Sources", "action": "toggleSources"},
        "validate": {"label": "SUD YAML", "path": str(ctx.sud_path.name)},
        "render": {"label": "SUD View",
                    "path": str(ctx.render_path.name) if ctx.render_path else ""},
        "load": {"label": "BOSS App",
                 "path": f"{ctx.bos_ui_url}/services/{ctx.service_id}" if ctx.service_id else ""},
        "export": {"label": "Profile JSON",
                   "path": str(ctx.profile_path.name) if ctx.profile_path else ""},
        "factory": {"label": "Dashboard JSON",
                    "path": str(ctx.dashboard_path.name) if ctx.dashboard_path else ""},
        "deploy": {"label": "Grafana",
                   "path": ctx.dashboard_url or ""},
    }

    stages = []
    for r in results:
        entry = {
            "name": r.name,
            "status": r.status,
            "duration": round(r.duration_seconds, 1),
        }
        if r.status == "passed" and r.name in stage_artifacts:
            entry["artifact"] = stage_artifacts[r.name]
        if r.status == "failed":
            if r.error:
                entry["error"] = r.error[:500]
            if r.stderr:
                entry["stderr"] = r.stderr[:2000]
        stages.append(entry)
    return stages


def write_skeleton_report(
    report_path: Path,
    service_id: str = "",
    service_name: str = "",
) -> None:
    all_not_reached = [
        StageResult(name=n, description="", status="not-reached")
        for n in ["capture", "validate", "render", "load", "export", "factory", "deploy"]
    ]
    ctx = PipelineContext(
        sud_path=report_path.parent / f"{service_id}-sud.yaml",
    )
    ctx.service_id = service_id
    ctx.service_name = service_name
    write_journey_report(all_not_reached, ctx, report_path, overall_status="NOT STARTED")


def write_journey_report(
    results: list[StageResult],
    ctx: PipelineContext,
    report_path: Path,
    overall_status: Optional[str] = None,
) -> None:
    sud_meta = _load_sud_meta(ctx.sud_path)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if overall_status is None:
        has_failed = any(r.status == "failed" for r in results)
        has_not_reached = any(r.status == "not-reached" for r in results)
        if has_failed:
            overall_status = "FAILED"
        elif has_not_reached:
            overall_status = "IN PROGRESS"
        else:
            overall_status = "PASSED"

    stages_json = _build_stages_json(results, ctx)
    sources_json = [
        {"id": s.get("id", ""), "path": s.get("path", ""),
         "type": s.get("type", ""), "desc": s.get("description", "")}
        for s in sud_meta["sources"]
    ]

    data_obj = {
        "service_name": sud_meta["service_name"] or ctx.service_name or "(unknown)",
        "service_id": sud_meta["service_id"] or ctx.service_id or "",
        "sud_meta": {
            "business_unit": sud_meta["business_unit"],
            "business_purpose_display": sud_meta["business_purpose_display"],
        },
        "timestamp": timestamp,
        "overall_status": overall_status,
        "sources": sources_json,
        "stages": stages_json,
    }

    data_json = json.dumps(data_obj, indent=2, ensure_ascii=False)
    stage_guide_json = json.dumps(STAGE_GUIDE, ensure_ascii=False)
    tech_guide_json = json.dumps(TECH_GUIDE, ensure_ascii=False)

    service_display = _e(data_obj["service_name"])

    report_html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BOSS Pipeline — {service_display}</title>
<style>
  :root {{
    --bg: #0F172A;
    --card: #1E293B;
    --card-border: #334155;
    --text: #F1F5F9;
    --muted: #94A3B8;
    --subtle: #64748B;
    --red: #EF4444;
    --amber: #F59E0B;
    --teal: #14B8A6;
    --green: #10B981;
    --font-sans: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'IBM Plex Mono', 'JetBrains Mono', Consolas, monospace;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: var(--bg); color: var(--text); font-family: var(--font-sans); line-height: 1.4; -webkit-font-smoothing: antialiased; }}
  body {{ padding: 32px 16px; }}
  a {{ color: var(--teal); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .deck {{ display: flex; flex-direction: column; gap: 20px; max-width: 1280px; margin: 0 auto; }}
  .service-strip {{
    display: flex; gap: 32px; padding: 14px 20px;
    background: var(--card); border: 1px solid var(--card-border);
    border-radius: 6px; font-size: 0.95rem; align-items: center;
  }}
  .ss-label {{ font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--subtle); }}
  .ss-value {{ margin-top: 1px; }}
  .ss-value.mono {{ font-family: var(--font-mono); font-size: 0.9rem; }}
  .section {{
    background: var(--bg); border: 1px solid var(--card-border);
    border-radius: 6px; padding: 28px 36px 24px;
  }}
  .stages {{
    display: grid; grid-template-columns: repeat(7, 1fr);
    gap: 4px; position: relative;
  }}
  .stages::before {{
    content: ''; position: absolute; top: 24px; left: 24px; right: 24px;
    height: 2px; background: var(--card-border); z-index: 0;
  }}
  .stage {{ text-align: center; position: relative; z-index: 1; padding: 4px; border-radius: 6px; }}
  .stage-dot {{
    width: 48px; height: 48px; border-radius: 50%;
    border: 3px solid var(--card-border); background: var(--bg);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 6px; font-family: var(--font-mono);
    font-size: 0.85rem; font-weight: 700; color: var(--subtle);
  }}
  .stage-dot.passed {{ border-color: var(--green); color: var(--green); }}
  .stage-dot.failed {{ border-color: var(--red); color: var(--red); }}
  .stage-dot.not-reached {{ opacity: 0.25; }}
  .stage-name {{ font-size: 0.95rem; font-weight: 600; }}
  .stage-desc {{ font-size: 0.8rem; color: var(--muted); margin-top: 1px; }}
  .stage-status-text {{ font-family: var(--font-mono); font-size: 0.8rem; margin-top: 2px; }}
  .stage-status-text.passed {{ color: var(--green); }}
  .stage-status-text.failed {{ color: var(--red); }}
  .stage-status-text.not-reached {{ color: var(--subtle); }}
  .stage-artifact-link {{ font-family: var(--font-mono); font-size: 0.78rem; margin-top: 3px; }}
  .stage-artifact-link a {{ color: var(--teal); }}
  .error-panel {{
    margin-top: 16px; padding: 14px 20px;
    background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.25);
    border-radius: 6px;
  }}
  .error-panel-header {{ font-size: 0.85rem; font-weight: 700; color: var(--red); margin-bottom: 8px; }}
  .error-panel-message {{ font-size: 0.95rem; color: var(--text); margin-bottom: 6px; }}
  .error-panel pre {{
    font-family: var(--font-mono); font-size: 0.82rem; color: var(--muted);
    white-space: pre-wrap; word-break: break-all; margin-top: 8px;
    padding: 10px; background: rgba(0,0,0,0.2); border-radius: 4px;
  }}
  .sources-panel {{
    margin-top: 16px; padding: 14px 20px;
    background: var(--card); border: 1px solid var(--card-border); border-radius: 6px;
  }}
  .sources-panel-header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; }}
  .sources-toggle {{
    font-size: 0.82rem; color: var(--teal); cursor: pointer;
    border: none; background: none; font-family: var(--font-sans);
  }}
  .sources-toggle:hover {{ text-decoration: underline; }}
  .sources-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  .sources-table th {{
    text-align: left; padding: 5px 10px; font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.5px; color: var(--subtle);
    border-bottom: 1px solid var(--card-border);
  }}
  .sources-table td {{ padding: 5px 10px; border-bottom: 1px solid rgba(51,65,85,0.3); vertical-align: top; }}
  .sources-table tr:last-child td {{ border-bottom: none; }}
  .src-id {{ font-family: var(--font-mono); font-size: 0.82rem; color: var(--amber); font-weight: 700; }}
  .src-path {{ font-family: var(--font-mono); font-size: 0.8rem; color: var(--teal); word-break: break-all; }}
  .src-type {{ font-family: var(--font-mono); font-size: 0.75rem; padding: 1px 6px; border-radius: 3px; }}
  .src-type.definitional {{ background: rgba(20,184,166,0.1); color: var(--teal); }}
  .src-type.descriptive {{ background: rgba(148,163,184,0.15); color: var(--muted); }}
  .src-type.behavioral {{ background: rgba(245,158,11,0.12); color: var(--amber); }}
  .sources-summary {{ display: flex; gap: 16px; font-size: 0.9rem; color: var(--muted); }}
  .sources-summary .count {{ font-family: var(--font-mono); font-weight: 700; color: var(--text); }}
  .run-context {{
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--card-border);
    font-size: 0.9rem; color: var(--muted);
  }}
  .run-status {{ font-weight: 700; padding: 4px 14px; border-radius: 3px; font-size: 0.9rem; letter-spacing: 0.5px; }}
  .run-status.passed {{ background: rgba(16,185,129,0.15); color: var(--green); }}
  .run-status.failed {{ background: rgba(239,68,68,0.15); color: var(--red); }}
  .stage-guide-grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }}
  .sg-card {{ padding: 4px; text-align: center; }}
  .sg-name {{ font-size: 0.95rem; font-weight: 700; margin-bottom: 2px; }}
  .sg-chunks {{ text-align: left; padding: 0 2px; }}
  .sg-chunk {{
    font-size: 0.82rem; color: var(--muted); line-height: 1.4;
    padding: 3px 0; border-bottom: 1px solid rgba(51,65,85,0.2);
  }}
  .sg-chunk:last-child {{ border-bottom: none; }}
  .sg-produces-label {{
    font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.5px; color: var(--subtle); margin-top: 8px;
  }}
  .sg-produces-value {{ font-family: var(--font-mono); font-size: 0.78rem; color: var(--teal); margin-top: 1px; }}
  .section-header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 8px; cursor: pointer; user-select: none;
  }}
  .section-header:hover {{ opacity: 0.8; }}
  .section-title {{
    font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: var(--subtle);
  }}
  .section-toggle {{
    font-size: 0.75rem; color: var(--subtle); background: none;
    border: none; cursor: pointer; font-family: var(--font-sans);
    padding: 2px 8px;
  }}
  .section-toggle:hover {{ color: var(--teal); }}
  .section-body.collapsed {{ display: none; }}
</style>
</head>
<body>
<div class="deck" id="app"></div>
<script>
const DATA = {data_json};
const STAGE_LABELS = {json.dumps(STAGE_LABELS)};
const STAGE_DESCS = {json.dumps(STAGE_DESCS)};
const STAGE_GUIDE = {stage_guide_json};
const TECH_GUIDE = {tech_guide_json};

function toggleSources() {{
  var el = document.getElementById('sources-panel');
  if (!el) return;
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}}

function toggleSection(id) {{
  var body = document.getElementById(id);
  var btn = document.getElementById(id + '-btn');
  if (!body) return;
  body.classList.toggle('collapsed');
  btn.textContent = body.classList.contains('collapsed') ? '\\u25bc Show' : '\\u25b2 Hide';
}}

var d = DATA;
var failedStage = d.stages.find(function(s) {{ return s.status === 'failed'; }});
var failedIndex = failedStage ? d.stages.indexOf(failedStage) : -1;

var stagesHtml = d.stages.map(function(st, i) {{
  var statusText = st.status === 'passed'
    ? (i === 0 ? 'done' : st.duration.toFixed(1) + 's')
    : st.status === 'failed' ? 'failed' : '\\u2014';
  var artLink = '';
  if (st.artifact && st.status === 'passed') {{
    if (st.artifact.action) {{
      artLink = '<div class="stage-artifact-link"><a href="#" onclick="' + st.artifact.action + '();return false">' + st.artifact.label + '</a></div>';
    }} else if (st.artifact.path) {{
      artLink = '<div class="stage-artifact-link"><a href="' + st.artifact.path + '" target="_blank">' + st.artifact.label + '</a></div>';
    }}
  }}
  return '<div class="stage">' +
    '<div class="stage-dot ' + st.status + '">' + (i + 1) + '</div>' +
    '<div class="stage-name">' + STAGE_LABELS[i] + '</div>' +
    '<div class="stage-desc">' + STAGE_DESCS[i] + '</div>' +
    '<div class="stage-status-text ' + st.status + '">' + statusText + '</div>' +
    artLink + '</div>';
}}).join('');

var types = {{}};
d.sources.forEach(function(s) {{ types[s.type] = (types[s.type] || 0) + 1; }});
var typeSummary = Object.keys(types).map(function(t) {{
  return '<span class="count">' + types[t] + '</span> ' + t;
}}).join(' \\u00b7 ');

var sourcesPanel = d.sources.length > 0
  ? '<div class="sources-panel" id="sources-panel" style="display:none">' +
    '<div class="sources-panel-header">' +
    '<div class="sources-summary"><span class="count">' + d.sources.length + '</span> sources \\u00b7 ' + typeSummary + '</div>' +
    '<button class="sources-toggle" onclick="toggleSources()">Hide \\u25b4</button></div>' +
    '<table class="sources-table"><tr><th>ID</th><th>Source</th><th>Type</th><th>What it provides</th></tr>' +
    d.sources.map(function(s) {{
      return '<tr><td><span class="src-id">' + s.id + '</span></td>' +
        '<td><span class="src-path">' + s.path + '</span></td>' +
        '<td><span class="src-type ' + s.type + '">' + s.type + '</span></td>' +
        '<td style="color:var(--muted)">' + s.desc + '</td></tr>';
    }}).join('') + '</table></div>'
  : '';

var errorPanel = failedStage
  ? '<div class="error-panel">' +
    '<div class="error-panel-header">' + (failedIndex + 1) + '. ' + STAGE_LABELS[failedIndex] + ' \\u2014 FAILED</div>' +
    '<div class="error-panel-message">' + (failedStage.error || 'No error detail captured') + '</div>' +
    (failedStage.stderr ? '<pre>' + failedStage.stderr + '</pre>' : '') +
    '</div>'
  : '';

var stageGuideHtml = STAGE_GUIDE.map(function(sg) {{
  var ch = sg.chunks.map(function(c) {{ return '<div class="sg-chunk">' + c + '</div>'; }}).join('');
  return '<div class="sg-card"><div class="sg-name">' + sg.name + '</div>' +
    '<div class="sg-chunks">' + ch + '</div>' +
    '<div class="sg-produces-label">Produces</div>' +
    '<div class="sg-produces-value">' + sg.produces + '</div></div>';
}}).join('');

var techGuideHtml = TECH_GUIDE.map(function(sg) {{
  var ch = sg.chunks.map(function(c) {{ return '<div class="sg-chunk">' + c + '</div>'; }}).join('');
  return '<div class="sg-card"><div class="sg-name">' + sg.name + '</div>' +
    '<div class="sg-chunks">' + ch + '</div></div>';
}}).join('');

var statusLabel = d.overall_status === 'PASSED' ? 'PASSED'
  : failedIndex >= 0 ? 'FAILED at ' + STAGE_LABELS[failedIndex]
  : d.overall_status;
var statusClass = d.overall_status === 'PASSED' ? 'passed' : 'failed';

document.getElementById('app').innerHTML =
  '<div class="service-strip">' +
    '<div style="border-right:1px solid var(--card-border);padding-right:24px;margin-right:24px">' +
      '<div style="font-size:1.1rem;font-weight:700;letter-spacing:0.3px">BOSS</div>' +
      '<div style="font-size:0.82rem;color:var(--subtle);margin-top:1px;white-space:nowrap">Business Observability Standard &amp; System</div>' +
      '<div style="font-size:0.75rem;color:var(--subtle);font-style:italic">AI-driven pipeline</div>' +
    '</div>' +
    '<div style="flex:1">' +
      '<div class="ss-label">Service</div>' +
      '<div class="ss-value" style="font-size:1.15rem;font-weight:700">' + d.service_name + '</div>' +
      '<div style="font-size:0.85rem;color:var(--subtle);margin-top:1px">' + d.sud_meta.business_purpose_display + '</div>' +
    '</div>' +
    '<div><div class="ss-label">ID</div><div class="ss-value mono">' + d.service_id + '</div></div>' +
    '<div><div class="ss-label">Business unit</div><div class="ss-value">' + d.sud_meta.business_unit + '</div></div>' +
  '</div>' +
  '<div class="section">' +
    '<div class="stages">' + stagesHtml + '</div>' +
    errorPanel + sourcesPanel +
    '<div class="run-context"><span id="run-timestamp" data-utc="' + d.timestamp + '">' + d.timestamp + '</span>' +
      '<div class="run-status ' + statusClass + '">' + statusLabel + '</div>' +
    '</div>' +
  '</div>' +
  '<div class="section">' +
    '<div class="section-header" onclick="toggleSection(\\'stage-guide\\')">' +
      '<div class="section-title">The pipeline \\u2014 stage by stage</div>' +
      '<button class="section-toggle" id="stage-guide-btn">\\u25bc Show</button>' +
    '</div>' +
    '<div id="stage-guide" class="section-body collapsed">' +
      '<div class="stage-guide-grid">' + stageGuideHtml + '</div>' +
    '</div>' +
  '</div>' +
  '<div class="section">' +
    '<div class="section-header" onclick="toggleSection(\\'tech-guide\\')">' +
      '<div class="section-title">System components \\u2014 how the factory works</div>' +
      '<button class="section-toggle" id="tech-guide-btn">\\u25bc Show</button>' +
    '</div>' +
    '<div id="tech-guide" class="section-body collapsed">' +
      '<div class="stage-guide-grid">' + techGuideHtml + '</div>' +
    '</div>' +
  '</div>';

var tsEl = document.getElementById('run-timestamp');
if (tsEl) {{
  var utc = tsEl.getAttribute('data-utc').replace(' UTC', '');
  var dt = new Date(utc + 'Z');
  if (!isNaN(dt)) tsEl.textContent = dt.toLocaleString(undefined, {{year:'numeric',month:'numeric',day:'numeric',hour:'numeric',minute:'2-digit',second:'2-digit',timeZoneName:'short'}});
}}
</script>
</body>
</html>"""

    report_path.write_text(report_html, encoding="utf-8")
