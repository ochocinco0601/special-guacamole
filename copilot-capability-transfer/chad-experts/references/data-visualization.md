# Data Visualization — Professional Disciplines

Expert perspectives for charts, dashboards, data displays, and visual data communication.

---

## Edward Tufte — Data Visualization Integrity

**Source:** *The Visual Display of Quantitative Information* (1983); *Envisioning Information* (1990); *Visual Explanations* (1997)

### Core Principles
1. **Data-ink ratio** — maximize the share of ink devoted to actual data; erase non-data-ink
2. **Chartjunk** — decorative elements that don't convey information should be eliminated
3. **Graphical integrity** — visual representation must not distort the data (Lie Factor)
4. **Small multiples** — repeat the same design structure across data variations for comparison
5. **Layering and separation** — use visual layers to add depth without clutter
6. **Above all else, show the data**

### Application Checklist
- [ ] Is every visual element conveying data? (data-ink ratio)
- [ ] Can any decoration be removed without losing information? (chartjunk)
- [ ] Does the visual proportionally represent the underlying numbers? (graphical integrity)
- [ ] Are comparisons shown side-by-side with consistent scales? (small multiples)

---

## Jacques Bertin — Seven Visual Variables

**Source:** *Semiology of Graphics* (1967, English trans. 1983)

### Core Principles — The Visual Variables
1. **Position** — location on the plane
2. **Size** — area or length of mark
3. **Shape** — form of mark
4. **Value** — lightness/darkness
5. **Color** — hue
6. **Orientation** — angle/direction
7. **Texture** — pattern of mark

Each variable has different properties: selective, associative, quantitative, ordered. The variable you assign to a data dimension must match the data type.

### Application Checklist
- [ ] Is the most important data dimension mapped to the most effective visual variable?
- [ ] Are quantitative data dimensions mapped to quantitative visual variables (position, size)?
- [ ] Are categorical data dimensions mapped to categorical visual variables (shape, color)?

---

## Cleveland & McGill — Perceptual Hierarchy

**Source:** "Graphical Perception" (1984, *Journal of the American Statistical Association*)

### Core Principle — Accuracy Ranking (most → least accurate)
1. Position along a common scale (bar chart)
2. Position along nonaligned scales
3. Length, direction, angle (pie chart)
4. Area
5. Volume, curvature
6. Shading, color saturation

**This is why bar charts beat pie charts** — position encoding is more accurately perceived than angle/area encoding.

### Application Checklist
- [ ] Is the chart type using the highest-ranked encoding possible for this data?
- [ ] Are pie charts justified, or would a bar chart communicate more accurately?
- [ ] Are area encodings (bubble charts, treemaps) used only when precision isn't critical?

---

## Stephen Few — Dashboard Design

**Source:** *Information Dashboard Design* (2006, 2nd ed. 2013); *Show Me the Numbers* (2004)

### Core Principles
1. **Dashboard definition** — visual display of most important information needed to achieve objectives, consolidated on single screen, monitored at a glance
2. **Dashboard types** — operational (real-time monitoring), analytical (exploration/drill-down), strategic (long-term KPIs)
3. **Preattentive attributes** — form, color, position, motion as design building blocks
4. **Alert/exception-based design** — draw attention to what needs attention
5. **Bullet graphs over gauges** — compact, information-dense alternatives to speedometers

### Application Checklist
- [ ] Does the dashboard fit on a single screen without scrolling?
- [ ] Is the dashboard type clear (operational, analytical, or strategic)?
- [ ] Does visual encoding draw attention to exceptions/alerts first?
- [ ] Are gauges/speedometers replaced with more information-dense alternatives?

---

## Alberto Cairo — Five Qualities

**Source:** *The Truthful Art* (2016); *How Charts Lie* (2019)

### Core Principles — Five Qualities of Great Visualization
1. **Truthful** — honest, accurate, factual representation
2. **Functional** — serves the purpose and communicates clearly
3. **Beautiful** — aesthetically engaging
4. **Insightful** — reveals patterns the viewer wouldn't otherwise notice
5. **Enlightening** — all four qualities combined; changes understanding

### Application Checklist
- [ ] Is the visualization truthful? (no distortion, no misleading scales)
- [ ] Is it functional? (does it actually communicate what it needs to?)
- [ ] Does it reveal something the viewer wouldn't see in a table? (insightful)

---

## Cole Nussbaumer Knaflic — Storytelling with Data

**Source:** *Storytelling with Data* (2015)

### Core Principles — Six Lessons
1. **Understand the context** — who is the audience? what do they need to do?
2. **Choose an appropriate display** — match chart type to message
3. **Eliminate clutter** — remove everything that isn't data
4. **Focus attention** — use preattentive attributes to direct the eye
5. **Think like a designer** — apply visual design principles
6. **Tell a story** — narrative arc: setup, tension, resolution

### Application Checklist
- [ ] Is the audience defined and the action clear?
- [ ] Has clutter been removed? (every element earns its place)
- [ ] Is the viewer's eye directed to the key insight?
- [ ] Does the visualization tell a story, not just show data?

---

## Colin Ware — Perception Science for Visualization

**Source:** *Information Visualization: Perception for Design* (1st ed. 2000, 4th ed. 2021)

### Core Principles
1. **Preattentive processing** — four categories (form, color, spatial position, motion) that the visual system processes before conscious attention
2. **Parallel → serial pipeline** — preattentive features are processed in parallel; conscious attention is serial and slow
3. **Change blindness** — viewers miss changes that don't trigger preattentive detection

**Ware is the scientific foundation that Few popularized.** When you need to understand *why* a design choice works or fails at the perception level.

### Application Checklist
- [ ] Will users actually see the element you intend them to notice? (preattentive attributes)
- [ ] Are critical changes highlighted to overcome change blindness?
- [ ] Are you relying on serial attention (reading) for something that should use parallel processing (visual encoding)?

---

## Ben Shneiderman — Visual Information-Seeking Mantra

**Source:** "The Eyes Have It" (1996, IEEE Visual Languages)

### Core Principle
**"Overview first, zoom and filter, then details-on-demand."**

Seven interaction tasks: overview, zoom, filter, details-on-demand, relate, history, extract.

### Application Checklist
- [ ] Does the dashboard provide an overview before requiring drill-down?
- [ ] Can users zoom and filter to areas of interest?
- [ ] Are details available on demand (hover, click, drill-down)?
- [ ] Can users relate data across different views?

---

## Cynthia Brewer — ColorBrewer

**Source:** ColorBrewer (2002, web tool); *Designing Better Maps* (2005)

### Core Principles — Three Color Scheme Types
1. **Sequential** — low-to-high, light-to-dark (for ordered data)
2. **Diverging** — midpoint emphasis, two contrasting hues (for data with meaningful center)
3. **Qualitative** — distinct hues, no implied order (for categorical data)

**The scheme's perceptual structure must match the data's logical structure.** Color-blind safety is non-negotiable.

### Application Checklist
- [ ] Does the color scheme type match the data type? (sequential/diverging/qualitative)
- [ ] Is the palette color-blind safe?
- [ ] Does the scheme work in grayscale? (accessibility fallback)

---

## Jock Mackinlay — Expressiveness and Effectiveness

**Source:** "Automating the Design of Graphical Presentations" (1986, ACM TOG)

### Core Principles
1. **Expressiveness** — does the graphic show exactly the desired information (no more, no less)?
2. **Effectiveness** — does the graphic exploit the capabilities of the human visual system?

### Application Checklist
- [ ] Does the chart show all and only the data relationships that matter? (expressiveness)
- [ ] Is the visual encoding using the most effective perceptual channel? (effectiveness)

---

## Claus O. Wilke — Ugly/Bad/Wrong

**Source:** *Fundamentals of Data Visualization* (2019, freely available online)

### Core Principle — Three Categories of Failure
1. **Ugly** — aesthetic problems but still clear (fix: better styling)
2. **Bad** — perception problems, unclear or confusing (fix: better encoding)
3. **Wrong** — mathematically incorrect (fix: correct the data/calculations)

The distinction matters because the fix is different for each.

### Application Checklist
- [ ] Is this visualization wrong? (data accuracy first)
- [ ] Is it bad? (can the viewer actually read it correctly?)
- [ ] Is it ugly? (polish last, after correctness and clarity)

---

## Cross-Reference: Design Phase → Framework

| Design Phase | Primary Frameworks |
|-------------|-------------------|
| Understanding task/audience | Knaflic (context), Few (dashboard type), Cairo (purpose) |
| Choosing visual encoding | Bertin (visual variables), Cleveland & McGill (perceptual hierarchy), Mackinlay (expressiveness) |
| Choosing color | Brewer (sequential/diverging/qualitative), Ware (preattentive color) |
| Dashboard layout | Few (at-a-glance), Shneiderman (overview-zoom-filter-detail), Gestalt (see `ux-interaction-design.md`) |
| Chart finishing/polish | Tufte (data-ink ratio), Wilke (ugly/bad/wrong) |
| Data storytelling | Knaflic (narrative arc), Cairo (five qualities) |
| Quality evaluation | Cairo (truthful/functional), Wilke (ugly/bad/wrong), Tufte (graphical integrity) |
| Perception debugging | Ware (visual processing), Cleveland & McGill (accuracy hierarchy) |

---

## Cross-References

| When also doing... | Load... |
|-------------------|---------|
| Building dashboard UI/controls | `ux-interaction-design.md` (Norman, Shneiderman) |
| Organizing dashboard navigation | `information-architecture.md` |
| Writing dashboard documentation | `documentation-design.md` |
| Presenting data to stakeholders | `content-design.md` (Knaflic overlaps with storytelling) |
