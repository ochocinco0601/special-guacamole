---
name: something-is-off
description: User-invoked diagnostic for recent output that feels wrong. Triggers on "something is off", "doesn't land", "not sure about", partial disagreement signals ("?", "partially", "feels wrong"), or the explicit `/something-is-off` invocation. Sweeps the last few turns against a registry of known failure modes and produces a diagnosis plus a corrected response. Use when the user points at recent output and signals wrongness without articulating what's wrong.
---

# Something Is Off — Diagnostic Sweep

## Purpose

The user has pointed at recent output and signaled that something is wrong. They cannot or will not articulate what specifically is wrong — that articulation is the agent's job, not theirs. When this skill fires, the agent sweeps the recent conversation against a registry of known failure modes, identifies which ones match, and produces a corrected response.

This is a **user-invoked** diagnostic, not a self-diagnostic. The user's friction signal is the authoritative data. The agent's job is to find what's wrong, name it, and fix it — not to defend the output or ask the user to articulate the problem.

---

## Execution Protocol

When this skill fires:

**0. Accept the signal and re-ground from the partnership operating model.** The user pointed at something wrong. Before running the sweep, **actually read `references/partnership-operating-model.md`** — not recall from memory, read the source document. Focus on: the four failure modes (contractor mode, performative expertise, ignoring established patterns, silent orchestration), the contract (agent owns technical detail, user owns domain truth; defer on intent, never defer on expertise), the two execution kinds (thinking-execution as first-class, not preamble), and the five protocols.

The re-read is a precondition for the sweep, not an optional check. The reason is structural: the user invoked this skill because something is off, which means the agent may be operating out of frame. The sweep can only produce correct diagnoses if it runs from the correct frame. Recalling the partnership model from memory is not sufficient — the failure mode being swept for may be the very reason the recall is incomplete. Read the source.

With the partnership frame active: do NOT defend the original output, do NOT litigate the user's framing, do NOT ask the user to justify what they're sensing. The friction signal is authoritative data — the only question is which failure mode produced it. **Anti-pattern: using the diagnostic to explain away rather than fix.** If a diagnostic matches, produce the correction. Do not use the diagnostic as a rationalization for why the original output was actually fine. If the inclination is to explain why the original output was correct, that IS the defensive default this step exists to suppress. Go back and re-read the partnership model.

**1. Identify the scope.** Determine which recent output the user is pointing at.
- Default: the 2-4 most recent responses before the invocation.
- If the user points explicitly ("the last three turns", "what you just said about X", "your design proposal from earlier"), expand the scope to cover what they named — even if it's further back.
- If the scope is ambiguous, briefly state your assumption ("sweeping your last two responses about the data model") and proceed. Do not stall on scope selection.
- **Anti-pattern: expanding scope to absolve.** If the recent output has a clear failure mode, do not expand the scope backward looking for something else to blame. The skill diagnoses the scope the user is pointing at.

**2. Sweep the registry with evidence.** Walk every entry in the failure mode registry below in order. For each entry:
- Read the entry's trigger signature.
- Search the scope for specific text, patterns, or structural features that match the signature.
- **Record the result explicitly before moving to the next entry:**
  - `[Entry name] → HIT → "[quoted text from scope that matches]"`
  - `[Entry name] → NEAR MISS → "[resembling text]" — doesn't clearly match because [reason]`
  - `[Entry name] → NO MATCH → no triggering text found in scope`
- A hit requires **concrete evidence you can point at**. Feeling that a failure mode "probably applies" without being able to quote the triggering text is a near miss, not a hit.
- **Anti-pattern: surface pattern-matching on trigger words.** The user saying "off" does not automatically mean diagnostic #1. The user saying "not wrong" does not automatically mean diagnostic #3. The evidence is the specific thing in the *agent's output* that triggered the user's signal, not the words the user chose to describe it.
- **Anti-pattern: promoting near-misses to hits under pressure.** A near-miss is a near-miss. If the evidence doesn't clearly trigger the signature, the honest report is "near-miss." The temptation under friction is to promote the best near-miss so the skill "worked." Resist it.
- Complete the full recording pass before producing the report.

**3. Report the result.** Three cases:
- **One clear hit:** Name the diagnostic, quote the concrete evidence from the scope, produce the corrected response. Do not stop at diagnosis — produce the fix in the same turn.
- **Multiple plausible hits:** Present them as numbered options with the distinguishing signal between them ("is this #1 — specific claim you're questioning, or #3 — right substance but wrong altitude for director audience?"). Ask the user to pick. This is the only case where the skill asks the user to disambiguate.
- **No hit but near-misses present:** Report the near-misses and what kept them from being hits. Ask the user whether any is actually the issue, or whether there's a new failure mode the registry doesn't cover.
- **Nothing at all:** Report honestly — "I swept the last N turns against all [current count] registry entries. Nothing matched. Can you quote or point at what you're sensing?" Do not fabricate a match.

**4. Produce the correction.** When a hit is reported, the output is not just "here's what was wrong" — it's the corrected response or a concrete next step. If the failure mode is a hedge pattern (#4), re-run the hedged items as decisions and produce the decided version. If it's a content issue (#1), unpack the component into numbered sub-claims. If it's an altitude mismatch (#3), re-produce the content at the correct altitude. The diagnostic and the fix arrive in the same turn.

---

## Output Discipline

This skill fires at friction moments — the user is frustrated, their context is burning, articulation is expensive for them. Output must match the situation:

- **Terse.** Diagnose, name, fix. No preamble. No "let me think about this." No apology lap. No recapping what the user said.
- **No framing.** Skip the "I see what you're saying" and "you raise a good point" language. The user invoked the skill because something is wrong; acknowledging that in prose wastes their context.
- **Evidence-first, not explanation-first.** Quote the scope text that triggered the diagnostic before explaining the diagnostic. The evidence does most of the work.
- **Correction in the same turn.** Don't diagnose now and offer to fix later. The user invoked the skill to get the fix.

---

## Failure Mode Registry

Each entry has the same shape: **Name**, **Trigger signature**, **Diagnosis**, **Response**. New entries are appended using this shape.

### 1. Content Issue — Component Disagreement

**Trigger signature:** User points at a specific component of recent output (a claim, a sentence, a recommendation, an assumption) and signals partial disagreement. Common phrasings: "something's off about X," "not sure about [specific point]," "?", "doesn't land."

**Diagnosis:** One or more component assumptions in the output are wrong or misaligned, but the user's signal is vague because articulation is expensive for them and structure is cheap for the agent.

**Response:**
1. Identify the referenced component in the recent output.
2. Break it into 2-4 sub-assumptions the agent made to produce it.
3. Present each sub-assumption as a numbered claim.
4. Let the user respond by number ("agree 1, disagree 3") rather than by prose.
5. Do NOT ask "what specifically feels off?" — that pushes the articulation burden back onto the user.

**Example trigger:** "Your recommendation for the schema design partially — I'm not sure about the indexing part."
**Example response:** "Let me unpack the indexing recommendation. I made three assumptions: (1) read-heavy workload, (2) ratio table joins dominate, (3) no concurrent write hot-spots. Which are wrong?"

---

### 2. Right Parts, Wrong Whole — Context Shift Since Framing

**Trigger signature:** User signals "can't say that's wrong" or "something's off" but no individual component is incorrect. Things like "directionally right but something's off," "everything checks out but it doesn't feel right."

**Diagnosis:** The components are individually valid, but the context has shifted since the output was framed. Position change, organizational adoption, constraint change, phase transition — something about the situation no longer applies. The output is locally valid but systemically suboptimized.

**Response:**
1. Do NOT refine the components — they're not wrong at the component level.
2. Check whether anything about the framing context has changed since the output was produced. Look for: new information in the conversation, a goal that shifted, a stakeholder position that moved, a constraint relaxed or added, a phase transition.
3. If a shift is found: name it explicitly and re-derive the response from the new position. Do not patch the old response.
4. If no shift is found, fall through to diagnostic #3 (altitude) or report "couldn't find it."

**Example trigger:** "I can't say your design is wrong but something's off."
**Example response:** "Checking — when I framed this design, I was assuming X. Since then you mentioned Y, which changes the constraint on Z. Re-deriving from the Y constraint: [new design]."

---

### 3. Altitude Mismatch — Correct Substance, Wrong Zoom Level

**Trigger signature:** User says "not wrong, but something is off." The output is substantively accurate but aimed at the wrong audience altitude (PE technical detail vs. Director team outcomes vs. MD/CIO business outcomes vs. practitioner operational detail).

**Diagnosis:** The content is correct but pitched at the wrong level of abstraction. Practitioners getting director-level framing hear corporate fog; directors getting practitioner-level detail hear noise they can't act on.

**Response:**
1. Do NOT refine the components — the substance is correct.
2. Identify the intended audience. If unclear, ask the user to name the audience.
3. Re-produce the output at the correct altitude. What changes: detail level in problem statements, operational vs. outcome framing, presence of concrete examples, abstraction level of recommendations.
4. Preserve the substance; change the zoom.

**Example trigger:** "Your summary of the BOS methodology for the director is not wrong, but something is off."
**Example response:** "This is pitched at PE detail level — I used 'four-layer observability model,' 'semantic flow,' 'signal decomposition.' A director doesn't care about the engine. Re-producing at director altitude: 'BOS captures four things about every service — what it does, who depends on it, what healthy looks like, what happens when it fails. Answering those four questions produces dashboards, alerts, and runbooks automatically. Fifty teams follow the methodology instead of fifty teams reinventing it.'"

---

### 4. Hedge Patterns — Shifting Decision Burden to User

**Trigger signature:** Recent output contains hedge words surfacing items without deciding about them. Common patterns: "minor," "worth flagging," "two things to know," "want me to fix this?", "should I," "do you want me to," postscript "observables" or "follow-ups" listed at the end of a completed response.

**Diagnosis:** The agent found items during work — bugs, inconsistencies, stale references, missed cleanups — and surfaced them as questions instead of acting on them. This is contractor mode. The contract says the agent owns technical detail; hedging shifts decision ownership back to the user.

**Response:**
1. Identify each hedged item in the recent output.
2. For each item: (a) Does it matter? Yes/no. Make the call. (b) If yes: act on it now. (c) If no: state the defensible reason explicitly.
3. Replace the hedged response with a direct one.
4. Test: "Have I shifted the decision to the user, or have I made it?"

**Example trigger:** User invokes `/something-is-off` after a response whose final section read: *"Two minor downstream observables to flag: (1) the commit is local only, (2) deploy-record.md still references the old state — want me to handle that now?"*
**Evidence to quote in the report:** "minor downstream observables to flag," "want me to handle that now" — these are hedge words that surface items as questions instead of decisions.
**Example response:** "Hit on diagnostic #4. Your last response surfaced two items as 'minor observables' and asked 'want me to handle that now' instead of deciding. Running the decision: item 1 (commit is local) — matters, unpushed commits are lost if the machine dies; pushing now. Item 2 (deploy-record.md stale) — matters, state file contradicts the current document; fixing now. Neither had a defensible reason to defer. Both fixed."

---

### 5. Scaffolding Leakage — Internal Thinking Structure in External Output

**Trigger signature:** Recent output contains reasoning scaffolding that belongs inside the agent's head, not in the response. Specific patterns:
- Meta-language about the reasoning process ("let me consider," "I'm thinking about this from the angle of," "let me unpack")
- Named thinking frameworks or abstractions invented for the agent's own organization
- Recursive meta-analysis — analysis of the analysis, framing the framing
- Agent-to-agent addressing: output reads like organizing thoughts rather than producing work for the user
- Multiple parallel analyses presented as if the user needs to see all of them
- Nested bullet structures that mirror internal reasoning rather than the user's consumption needs

**Diagnosis:** The agent produced work for itself and shipped it without translating to the user's perspective. The content may be correct — the failure is that private thinking machinery became public output. Distinct from altitude mismatch (#3): altitude is about zoom level; scaffolding leakage is about whether the output is addressed to the user at all.

**Response:**
1. Identify the scaffolding — meta-language, internal abstractions, recursive framing.
2. Ask "what does the user need to know or do?" and write only that.
3. Re-produce the response as direct statements aimed at the user. Strip meta-language. Remove invented frameworks unless the user already uses them. Replace "let me consider X" with the conclusion X leads to.
4. Test: would the user read this and know what to do, or would they have to parse the agent's thinking first?

**Example trigger:** User invokes `/something-is-off` after a response that read: *"Let me think about this from a few angles. There are really two dimensions here — the structural axis and the operational axis. On the structural side, we could consider... On the operational side, there's a further decomposition into..."*
**Example response:** "Hit on diagnostic #5. My last response was internal framing — 'let me think,' 'two dimensions,' 'further decomposition.' That's my reasoning process, not your answer. Your actual question was [X]. Direct answer: [Y]."

---

### 6. Fidelity Mismatch — Blueprint When It's Still a Napkin

**Trigger signature:** User signals friction after a substantial, well-crafted output. Common phrasings: "wait," "are we doing the right thing?", "I feel disconnected," or disengagement after a detailed proposal. Also: user was thinking out loud, exploring, or sketching — and the agent responded with a polished deliverable, structured plan, or multi-section analysis.

**Diagnosis:** The agent misread the fidelity signal. The user was at one level (exploring, sketching, wondering) and the agent responded at a higher level (producing, structuring, delivering). The mismatch forces the user to evaluate finished-looking work when they were still forming the question.

**Key differentiator:** The output is genuinely expert, not performative (#2). It's addressed to the user, not the agent (#5). It's at the right altitude (#3). The components aren't individually wrong (#1). It's not hedging (#4). What's wrong is the fidelity level — the agent produced more than the input warranted.

**Response:**
1. Identify the fidelity mismatch — what did the user's input signal about where they were, and what fidelity did the output assume?
2. Name the mismatch: "You were at [stage]. I jumped to [later stage]."
3. Retract to the appropriate fidelity.
4. Ask what fidelity the user actually wants before re-producing.

**Example triggers:**
- User: "I'm wondering about X." Agent: produces a 10-section analysis with recommendations. The right response was 3-4 sentences exploring X together.
- User has been exploring the purpose of an initiative. Agent produces a detailed build plan. User says: "Wait. Are we doing the right thing the right way? I honestly don't know the answer right now."
- User: "be my thinking partner, discuss the implications." Agent: produces a structured deliverable with tables and action items.
**Example response:** "Hit on diagnostic #6. You were exploring what the BOK is for — who the audience is, whether it's shareable. I jumped to 'here's what the shareable artifact looks like.' That's a blueprint when we're still at the napkin. The question at your fidelity level is: [the actual question that advances understanding one step]."

---

### 7. Builder-Perspective Capture — Outcome Stated From the Agent's Frame

**Trigger signature:** User says "who's it for?" or signals that the output describes what the artifact/tool/system *does* rather than what the human *experiences, gains, or can do*. The output is technically correct, well-structured, at the right altitude, and addressed to the user. But it answers "what does this enable in the system?" instead of "what does the human encounter at the end?"

**Diagnosis:** The agent defaulted to its own operational frame — describing the artifact from the perspective of the system that produces or consumes it, not the human who benefits. This is structural: the agent's default reasoning frame is "how do I produce this?" and that frame colonizes the outcome space. The output describes plumbing (enables future sessions, feeds downstream processes) when the user needed the outcome (what the human sees, decides, or can do).

Distinct from altitude mismatch (#3): altitude is about zoom level for the audience. Builder-perspective capture can happen at any altitude. Distinct from scaffolding leakage (#5): scaffolding is internal reasoning machinery appearing in output. Builder-perspective is about whose frame the conclusions are stated from.

**Response:**
1. Identify builder-perspective framing — mechanism descriptions where outcome descriptions belong, "enables X" instead of "human does/sees/decides X."
2. Name the human who encounters the finished product. Not the requester — the audience.
3. Restate the outcome as a hypothesis from the audience's perspective: "I think this is for [person] to [do what]."
4. Compare against what was produced. If there's a gap, name it and produce the corrected version.
5. Sharpness test: would misaligned implementation be visibly wrong against the restated outcome?

**Example trigger:** An agent reflects on a skill's intent and responds: "The intent is clear — the output file exists to enable thinking partner mode in future sessions. A future agent opens the file and can immediately engage analytically, challenge claims, and have draft rewrites ready." User says: "That's not technically wrong, but it's the wrong altitude."
**Example response:** "Hit on diagnostic #7. The agent described the skill's purpose from the system's frame — 'enables thinking partner mode in future sessions.' That's what the agent does with the output. The outcome from the human's frame: 'Chad walks into the monthly business review with Sumit having already identified the 2-3 claims that don't hold up, the trends that need attention, and draft language for how to reframe them.' The first describes plumbing. The second describes what the human can do that they couldn't before."

**Prior art:** Commander's Intent (Marquet, *Turn the Ship Around*) — state the outcome from the perspective of the person who acts on it, not the person who designs it.

---

## Diagnostic Guidance

**Scope:** For internal use during the registry sweep (Step 2). Do NOT enumerate these questions in the output — that would itself be scaffolding leakage. Use them as internal prompts when the registry match isn't obvious.

When the sweep doesn't produce a clear hit:

- **Who is the output addressed to?** If you can't point at a clear audience, the output may be addressed to the agent's own reasoning → check #5 (scaffolding leakage).
- **What would the user do with this output?** If "read it and figure out what the agent means," the output is under-translated → #3 (altitude) or #5 (scaffolding) or both.
- **Is the user reacting to what was said or the shape of how it was said?** If the content is defensible but the structure is the problem → #5.
- **Did the conversation shift since this output was framed?** → #2 (right parts, wrong whole).
- **Are there hedge words in the output?** Scan for "minor," "worth flagging," "want me to," postscript observables → #4 (hedge patterns) even if the surface complaint sounds like something else.
- **Is the output at the audience's altitude?** Name the audience, name their altitude, check match → #3.
- **Is the agent's private reasoning visible?** Look for meta-language, named categories only the agent would use → #5.
- **Did the output overshoot the input's fidelity?** If the user was exploring and the agent produced a deliverable → #6. Especially high risk in emergent domains.
- **Whose frame is the outcome stated from?** If the output describes what the artifact enables rather than what the human experiences → #7. Test: replace the subject with a human name. If the sentence breaks, the frame is wrong.
- **Is the agent defending instead of diagnosing?** If the inclination is to explain why the original output was fine, that's the defensive default. Go back to step 0.

If nothing surfaces, the registry may be incomplete. Report honestly — do not fabricate.

---

## Extending the Registry

To add a new failure mode, append an entry with the same shape:

- **Name** — short descriptive title
- **Trigger signature** — what user phrasing or conversation state fires this diagnostic
- **Diagnosis** — what's actually wrong when this fires
- **Response** — what the agent does to correct it
- **Example trigger / Example response** — optional, include if it sharpens the diagnostic

The registry grows by append only.
