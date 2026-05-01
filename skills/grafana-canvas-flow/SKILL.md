---
name: grafana-canvas-flow
description: Generate Grafana Canvas panel JSON that visualizes service dependency flows as directed graphs. Use this skill whenever the user wants to visualize service dependencies, draw an application flow, create a service topology diagram in Grafana, or when a dashboard needs a flow panel. Triggers on "draw the flow", "visualize dependencies", "service flow", "canvas panel", "show me how services connect", "dependency diagram", "application flow diagram", or when generating dashboards that should include a service context panel. Also use proactively when onboarding a service and dependency data is available — every service dashboard benefits from a flow panel showing where the service sits in context.
---

# Canvas Flow — Service Dependency Visualization

Generate Grafana Canvas panel JSON from a service dependency description. Produces positioned nodes with directed connections that render as a flowchart in Grafana.

## Workflow

Every invocation follows this sequence. The detailed sections below are reference material organized by phase.

```
1. INPUT        Accept dependency description (natural language, edges, structured data, inline list)
2. NORMALIZE    Parse to edge list, classify node roles, confirm with user
3. LAYOUT       Classify topology → assign layers → position nodes → calculate dimensions
4. GENERATE     Assemble dashboard JSON using element schema + visual conventions + connection wiring
5. PUSH         Deploy to Grafana via REST API (optional — skip if no instance available)
6. VERIFY       Adversarial self-evaluation — screenshot, hard-fail checklist, iterate until clean
```

**Interactive vs automated:** In interactive mode (user conversation), confirm the edge list after step 2. In automated mode (pipeline, dashboard generation), skip confirmation and proceed directly — the pipeline validates downstream.

---

## Phase 1: Input

Accept any of these forms:

**Natural language:** "Draw a flow: Client calls API Gateway, which calls Auth Service and Cart Service. Cart Service reads from PostgreSQL."

**Structured edges:** An array of `{from, to, protocol?, direction?}` objects.

**Service profile data:** If a structured service profile exists with dependency information, parse the service names and directional relationships from it.

**Inline list:** The user names services and relationships in any format.

## Phase 2: Normalize

Parse the input into a canonical edge list. For each node, classify its role (entry point, hub, check, external, infrastructure, async destination) — this drives visual conventions in Phase 4.

In interactive mode, confirm: "I see N services with M connections — here's the graph. Look right?"

## Phase 3: Layout

Canvas has no auto-layout — every node needs explicit pixel coordinates. These rules produce readable results from 3 to 16 nodes (proven across 6 topologies in the spike).

### 3a. Classify the topology

| Pattern | Signal | Layout strategy |
|---------|--------|-----------------|
| **Linear** | Each node has ≤1 outbound | Single horizontal row, left-to-right |
| **Pipeline with branches** | Linear spine + side deps | Main row + branch rows above/below |
| **Fan-out** | One node → 3+ targets | Source on left, targets stacked vertically |
| **Hub-and-spoke** | One node has 4+ connections | Hub centered, spokes radiate |
| **Mesh** | Multiple nodes with 3+ connections | Layered left-to-right, minimize crossings |

Most real services are **pipeline with branches** — a main flow with databases, caches, and external services hanging off the sides.

### 3b. Assign layers (columns)

Walk the graph left-to-right. Entry points (no inbound edges) go in column 0. Their targets go in column 1. Continue until all nodes are placed. Nodes with multiple inbound edges go in the rightmost column that satisfies all dependencies.

Infrastructure nodes (databases, caches, message queues) go in the same column as the service that uses them, but offset vertically (above or below the main row).

### 3c. Position nodes

```
COLUMN_SPACING = 180    # px between column centers
ROW_SPACING = 55        # px between row centers  
NODE_WIDTH = 130        # px, standard service
NODE_HEIGHT = 45        # px, standard service
HUB_WIDTH = 150         # px, hub/orchestrator nodes
HUB_HEIGHT = 55         # px, hub/orchestrator nodes
INFRA_WIDTH = 110       # px, infrastructure nodes
INFRA_HEIGHT = 38       # px, infrastructure nodes
LEFT_MARGIN = 30        # px from panel edge
TOP_MARGIN = 30         # px from panel edge
```

For each column, center nodes vertically around the main flow row. Stagger fan-out targets with equal vertical spacing.

### 3d. Calculate panel dimensions

```
gridPos.w = 24  (always full width)
gridPos.h = max(10, ceil((max_vertical_extent + 80) / 30))
```

If total horizontal extent exceeds ~1000px, either compress spacing or warn the user.

## Phase 4: Generate

Assemble the dashboard JSON. Read `references/canvas-schema.md` for the exact field-level schema, and `references/minimal-example.json` for a complete 3-node working example.

### Element conventions

**Naming:** Element `name` values use kebab-case slugs derived from the display label: "Account Opening Svc" → `account-opening-svc`. Names must be unique — connections reference elements by `name`.

**Font size (`config.size`):** Hub/orchestrator nodes: 10-11. Standard nodes: 10-11. Infrastructure/small nodes: 10-11. Entry points and key terminals: 11-12. Keep sizes consistent within a role category.

### Node colors by role

| Role | Background | Text | Border | When to use |
|------|-----------|------|--------|-------------|
| Entry point / channel | `#1565C0` | `#FFFFFF` | `#0D47A1` | First node(s) — user-facing |
| Core service | `#2E7D32` | `#FFFFFF` | `#1B5E20` | Standard internal service |
| Orchestrator / hub | `#AD1457` | `#FFFFFF` | `#880E4F` + width 2 | Node with 4+ connections |
| Validation / check | `#E65100` | `#FFFFFF` | `#BF360C` | Auth, fraud, credit checks |
| Processing | `#6A1B9A` | `#FFFFFF` | `#4A148C` | Transform, scoring, underwriting |
| Error / decline | `#C62828` | `#FFFFFF` | `#B71C1C` | Error handlers, decline paths |
| Success / completion | `#00695C` | `#FFFFFF` | `#004D40` | Closing, funding, approval |
| External service | `#E0E0E0` | `#333333` | `#BDBDBD` | Third-party, outside boundary |
| Infrastructure | `#455A64` | `#FFFFFF` | `#263238` | Database, cache, message queue |
| Async destination | `#FF5722` | `#FFFFFF` | `#E64A19` | Kafka, RabbitMQ, event bus |

### Edge colors by type

| Type | Color | When |
|------|-------|------|
| Standard sync | `#90CAF9` | Default — HTTP, gRPC calls |
| Async / event | `#FF9800` | Message queues, event buses |
| Error path | `#EF5350` | Decline, failure routing |
| Success path | `#66BB6A` | Approval, completion |
| Infrastructure access | `#78909C` | DB reads, cache lookups |

All edges use `size.fixed: 1.5` unless intentionally varied for semantic meaning. Random variation is a visual defect.

### The "subject service" rule

When generating a flow for a specific service (e.g., from a service profile), that service should be visually prominent:
- Slightly larger node (hub dimensions)
- Thicker border (width: 2)
- Centered in the layout where topology allows

### Connection wiring rules

- Connections live on the **source element** in its `connections[]` array, NOT at the root level
- `source` and `target` are **anchor coordinates** (`{x, y}`, normalized -1 to 1), not element names
- `targetName` is the string that identifies the destination element
- `path: "straight"` is required
- Common anchors: right edge `{x:1, y:0}`, left edge `{x:-1, y:0}`, bottom `{x:0, y:-1}`, top `{x:0, y:1}`
- For fan-out, use fractional y values: `{x:1, y:-0.5}`, `{x:1, y:0.5}` to spread connections

### Y-axis is inverted from DOM (CRITICAL)

In anchor coordinate space, **y=1 is TOP** and **y=-1 is BOTTOM**. This is the opposite of CSS/DOM where higher numbers go down. Getting this wrong causes lines that pass through node bodies instead of exiting from edges.

```
             {0, 1} = TOP of node
                |
{-1, 0} left ——{0,0}—— {1, 0} right
                |
            {0, -1} = BOTTOM of node
```

**Concrete example — connecting downward from a hub to a node below it:**
- Source anchor: `{x: -1, y: -0.5}` = left side, toward BOTTOM (lower on screen)
- Target anchor: `{x: 0, y: 1}` = center, TOP edge (upper edge of target)
- This draws a line exiting the hub's lower-left and arriving at the target's top — clean diagonal down-left

**Anti-pattern that causes lines through bodies:**
- `{source: {y: 1}, target: {y: -1}}` on a horizontal connection = line exits TOP of source and enters BOTTOM of target, cutting diagonally through both node bodies. Use `y: 0` for horizontal connections.

### Fan-out anchor matching rule

When a source fans out to multiple targets stacked vertically, the source anchor positions MUST match the spatial arrangement of the targets:

- **Upper source anchor** (higher y value, e.g., `y: 0.5`) → connects to the **upper target** (lower `top` value on screen)
- **Lower source anchor** (lower y value, e.g., `y: -0.5`) → connects to the **lower target** (higher `top` value on screen)

If you swap these — upper anchor to lower target and vice versa — the lines MUST cross each other to reach their destinations. This is always wrong. Check every fan-out by tracing each line mentally: does the line go straight to its target, or does it cross another line from the same source?

### Async lane separation

When a node has both synchronous fan-out (e.g., right side to downstream checks) AND an async connection (e.g., to a message queue), route the async connection out the **opposite side** of the node from the sync fan-out. If sync goes right, async exits left. Position the async target (message queue) on that opposite side so the async line never crosses the sync lines.

**Proven pattern from spike:** Hub fans out right to checks → async exits hub's left-bottom `{x:-1, y:-0.5}` → MQ positioned far left (left=100) and below (top=195) → MQ then fans out rightward to its own consumers. The async lane is spatially separated from the sync lane.

### Output file

Save the generated JSON to the appropriate project or dashboard directory. Name the file descriptively: `canvas-account-opening.json`, `canvas-payment-hub.json`.

## Phase 5: Push (Optional)

If a Grafana instance is available, use the Grafana MCP tools or REST API to push the dashboard. After push, proceed immediately to Phase 6.

## Phase 6: Verify (MANDATORY — Adversarial Self-Evaluation)

The default verdict is **FAIL**. You are looking for the worst thing in the image, not confirming it looks OK. This checklist exists because the spike proved that without it, basic defects ship — lines through node bodies, unnecessary crossings, inconsistent weights — and the user has to catch them. That is unacceptable. If you would not show this diagram to a stakeholder, it fails.

### Scoring System

Every evaluation iteration produces a score out of 100:

```
START AT 100
  Each hard fail:         -25 points
  Each soft check failure: -8 points
PASS THRESHOLD: 80
```

One hard fail = 75 max → automatic FAIL. All hard fails clear with 2 soft check failures = 84 → PASS. All hard fails clear with 3 soft check failures = 76 → FAIL.

### Iteration Rules

- **Maximum 5 iterations.** If the score hasn't reached 80 after 5 push-screenshot-fix cycles, stop and present to the user with an honest assessment of what couldn't be fixed.
- Each iteration: fix the issues found, re-push, re-screenshot, re-score.
- Score ≥ 80 → **PASS** — stop iterating, present to user.
- Score < 80 after iteration 5 → **FAIL** — present to user with the score history and remaining defects.
- Fix only the issues found in the current evaluation. Don't re-break things that were already passing.

### Protocol

1. **Push** the dashboard JSON to Grafana (via MCP tools or REST API)
2. **Navigate** to the dashboard URL in the browser (kiosk mode: append `?kiosk`)
3. **Screenshot** the rendered panel (if browser tools are available)
4. **Read the screenshot back** into context — inspect what was actually produced, not what you intended
5. **Score the hard fail checklist** first. Any hard fail = fix immediately, re-push, re-screenshot (counts as an iteration)
6. **Score the soft checklist** once hard fails are clear
7. **Calculate score**, record in the iteration log
8. **If score ≥ 80:** present the dashboard link + evaluation summary to the user
9. **If score < 80 and iterations < 5:** fix issues, go to step 1
10. **If score < 80 and iterations = 5:** stop, present with honest failure assessment

### Hard Fail Checks (-25 points each)

These are non-negotiable. Each was discovered by a human catching what the self-evaluation missed.

```
HARD FAIL CHECKLIST — run these FIRST:
□ Lines through node bodies: Trace every connection visually. Does any line
  enter or exit through the INTERIOR of a node instead of its edge? This
  typically means y-axis confusion (y=1 is TOP, not bottom). [-25]
□ Unnecessary line crossings: Do any lines from the same source cross each
  other? This means fan-out anchors are swapped — upper anchor going to lower
  target. Fix by matching anchor position to target position. [-25]
□ Lines crossing unrelated nodes: Does any connection line pass through a node
  that is not its source or target? Reposition nodes or change anchor points
  to route around it. [-25]
□ Inconsistent line weights: Are all lines the same size (1.5 default)? If any
  line is a different weight, it MUST have semantic meaning (e.g., thicker =
  primary flow). Accidental variation. [-25]
□ Visual verified: Did you actually inspect the rendered output (screenshot or
  direct observation)? If you are evaluating from JSON alone while Grafana is
  available, STOP and verify visually. [-25]
```

### Soft Checks (-8 points each)

```
SOFT CHECKLIST — score after hard fails are clear:
□ All labels readable: [text visible against background on every node?] [-8]
□ No clipping: [all nodes fully within panel bounds? check right edge] [-8]
□ All connections rendering: [count arrows vs expected edge count — match?] [-8]
□ Connection targets correct: [arrows point to the right nodes?] [-8]
□ Flow direction clear: [left-to-right reading order maintained?] [-8]
□ Visual hierarchy: [hub visually prominent? externals lighter?] [-8]
□ Subject service prominent: [if profile-based, is subject service larger/bolder?] [-8]
□ Async separation: [async lines routed away from sync fan-out?] [-8]
□ Color conventions applied: [sync=blue, async=orange, error=red, grey?] [-8]
□ Node overlap: [any nodes overlapping each other?] [-8]
□ Panel height sufficient: [content uses space well, no excess empty area?] [-8]
□ Worst remaining thing: [name it — if nothing, score this as pass] [-8]
```

### Evaluation Summary Template

```
ITERATION: [N of 5]
SCORE: [0-100]
VERDICT: [PASS (≥80) / FAIL (<80)]
Hard fails: [count × -25 = X] — [list each and fix applied]
Soft failures: [count × -8 = Y] — [list each]
Score history: [iter1: XX, iter2: XX, ...]
Remaining concerns: [honest list, or "none"]
```

### Structural Validation Fallback

If you cannot reach Grafana (no running instance), validate JSON structurally and score using the same system — but note that hard fail #5 (visual verified) is automatically scored as a failure (-25) since visual verification was not performed. This means the structural-only path starts at 75 max and requires all other checks to pass for a score of 75. Present this to the user with a note that visual verification is needed for a true PASS.

Structural checks:
- Every `targetName` references an existing element `name`
- No duplicate element names
- All element `name` values are kebab-case slugs
- All placements within panel bounds (right edge = left + width < 1050)
- All connection anchors use correct y-axis convention (y=1 is top, y=-1 is bottom)
- Fan-out anchor y-values match target spatial order (upper anchor → upper target)
- All `size.fixed` values are consistent (1.5) unless semantic variation is intentional

## Constraints (from spike)

- `lineStyle: "dashed"` does NOT work in Grafana v11.3.2 — use edge color to distinguish sync vs async
- Practical limit: ~16 nodes per panel before readability degrades
- No auto-routing — edge crossings are inevitable in mesh topologies; minimize via node placement
- All iterations used `type: "rectangle"` — other shapes (ellipse, cloud, server) are available but untested
- Arrow heads render by default — no explicit `direction` field needed for standard flows
