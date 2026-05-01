# Grafana Canvas Panel — JSON Schema Reference

Load this file when generating Canvas panel JSON. Contains exact field names, types, and proven patterns.

## Dashboard Wrapper

```json
{
  "dashboard": {
    "uid": "unique-id",
    "title": "Dashboard Title",
    "tags": ["canvas"],
    "schemaVersion": 39,
    "panels": [ /* canvas panel(s) */ ]
  },
  "overwrite": true
}
```

## Canvas Panel Structure

```json
{
  "id": 1,
  "type": "canvas",
  "title": "Panel Title",
  "gridPos": { "h": 16, "w": 24, "x": 0, "y": 0 },
  "fieldConfig": { "defaults": {}, "overrides": [] },
  "options": {
    "inlineEditing": true,
    "panZoom": true,
    "root": {
      "name": "root",
      "background": { "color": { "fixed": "transparent" } },
      "border": { "color": { "fixed": "dark-green" } },
      "constraint": { "horizontal": "left", "vertical": "top" },
      "placement": { "height": 100, "left": 0, "top": 0, "width": 100, "rotation": 0 },
      "elements": [],
      "connections": []
    }
  }
}
```

Root-level `connections: []` MUST stay empty. All connections go on source elements.

## Element Schema

```json
{
  "name": "unique-element-id",
  "type": "rectangle",
  "config": {
    "align": "center",
    "valign": "middle",
    "color": { "fixed": "#FFFFFF" },
    "text": { "fixed": "Display Label" },
    "size": 14
  },
  "placement": {
    "left": 100,
    "top": 50,
    "width": 140,
    "height": 50,
    "rotation": 0
  },
  "background": { "color": { "fixed": "#1f77b4" } },
  "border": { "color": { "fixed": "#1564a0" }, "width": 1 },
  "constraint": { "horizontal": "left", "vertical": "top" },
  "links": [],
  "connections": []
}
```

### Critical gotchas

- `config.color` is the **TEXT** color — not the element color. Setting this to the same value as `background.color` makes text invisible.
- `config.size` is a bare number (font size in px), not an object.
- `constraint` is required on every element or positioning breaks.
- `placement` uses absolute pixel coordinates within the panel viewport.
- `name` must be unique across all elements — connections reference elements by name.

### Available element types

`rectangle`, `ellipse`, `text`, `icon`, `server`, `triangle`, `cloud`, `parallelogram`, `button`, `wind-turbine`, `drone-top`, `drone-front`, `drone-side`

## Connection Schema

Connections are arrays on the **source** element. Each connection draws a line from this element to a target element.

```json
{
  "source": { "x": 1, "y": 0 },
  "target": { "x": -1, "y": 0 },
  "targetName": "target-element-name",
  "path": "straight",
  "color": { "fixed": "#aaaaaa" },
  "size": { "fixed": 1.5, "min": 1, "max": 10 }
}
```

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `source` | `{x, y}` | Anchor point on THIS element. Normalized -1 to 1. |
| `target` | `{x, y}` | Anchor point on the TARGET element. Normalized -1 to 1. |
| `targetName` | string | The `name` of the destination element. |
| `path` | string | Must be `"straight"`. |

### Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `color` | `{fixed: string}` | Line color. Hex or rgb(). |
| `size` | `{fixed, min, max}` | Line thickness. |
| `direction` | `{fixed: string}` | Arrow: `"forward"`, `"reverse"`, `"both"`, `"none"`. Default renders arrows. |
| `lineStyle` | string | `"solid"`, `"dashed"`, `"dotted"`. NOTE: dashed/dotted NOT working in v11.3.2. |
| `vertices` | `[{x, y}]` | Intermediate bend points. Max 10. |

### Anchor coordinate system

Normalized to element bounding box, centered at `{0, 0}`:

```
              {0, 1} top
                 |
{-1, 0} left ——{0,0}—— {1, 0} right
                 |
             {0, -1} bottom
```

Y-axis is inverted from DOM (positive y = up in anchor space).

### Fan-out pattern

When one element connects to multiple targets, use fractional y values on the source anchor to spread the lines:

```json
{ "source": { "x": 1, "y": -0.7 }, "target": { "x": -1, "y": 0 }, "targetName": "target-1", "path": "straight" },
{ "source": { "x": 1, "y": -0.3 }, "target": { "x": -1, "y": 0 }, "targetName": "target-2", "path": "straight" },
{ "source": { "x": 1, "y":  0.3 }, "target": { "x": -1, "y": 0 }, "targetName": "target-3", "path": "straight" },
{ "source": { "x": 1, "y":  0.7 }, "target": { "x": -1, "y": 0 }, "targetName": "target-4", "path": "straight" }
```

### Fan-in pattern

When multiple elements connect to one target, use fractional y values on the target anchor:

```json
// On element "channel-1":
{ "source": { "x": 1, "y": 0 }, "target": { "x": -1, "y": -0.5 }, "targetName": "gateway", "path": "straight" }
// On element "channel-2":
{ "source": { "x": 1, "y": 0 }, "target": { "x": -1, "y": 0 },    "targetName": "gateway", "path": "straight" }
// On element "channel-3":
{ "source": { "x": 1, "y": 0 }, "target": { "x": -1, "y": 0.5 },  "targetName": "gateway", "path": "straight" }
```

## REST API

Push dashboard:
```bash
curl -s -X POST http://<grafana-url>/api/dashboards/db \
  -H "Authorization: Bearer <service-account-token>" \
  -H "Content-Type: application/json" \
  -d @dashboard.json
```

Response: `{"status":"success","uid":"...","url":"/d/..."}` — the `url` field is the dashboard path.

## Proven Limits (from spike, Grafana v11.3.2)

- 16 nodes: readable, practical upper bound without panZoom
- 6 connections from one node: dense but usable upper bound
- No auto-routing: edge crossings must be minimized via node placement
- Panel clipping: layout must fit within ~1050px horizontal extent
- `lineStyle: "dashed"`: not rendered in v11.3.2
