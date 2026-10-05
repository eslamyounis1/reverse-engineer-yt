---
name: channel-reverse-engineer
description: >-
  Reverse-engineer the repeatable production system behind a set of reference short-form
  videos, using Higgsfield MCP video analysis as evidence, then turn the findings into a
  reusable Claude Skill that can create original content in the same format without copying
  scripts, branding, characters, or distinctive assets.
---

# channel-reverse-engineer

Use this Skill when the user gives you several videos from one channel / creator / format and
wants you to understand the *production system* behind them, then convert that system into a
reusable Skill.

The goal is not to imitate one output. The goal is to recover the decision rules that consistently
produce the format.

## Core principle

Learn the process, not the output.

Do not copy:
- scripts or distinctive lines;
- creator identity or branding;
- distinctive characters, props, logos, or protected visual assets;
- one-off details that are not supported across several references.

Do extract:
- hook formulas;
- narrative structure;
- pacing;
- shot-length distribution;
- chapter / beat structure;
- visual grammar;
- retention devices;
- recurring production decisions;
- measurable constraints that another agent can execute.

## Input

Ask for 3–8 reference videos from the same format.

Prefer at least 5 references when available.

For every reference, keep:
- reference ID;
- title;
- URL;
- duration;
- raw Higgsfield scene analysis;
- independent notes.

## Rule 1 — Analyze every video independently first

Do **not** start with cross-video conclusions.

For every reference:

1. Run Higgsfield MCP video analysis on the video.
2. Save the raw scene-by-scene result.
3. Create one independent analysis file.
4. Only describe what is supported by that video's evidence.

Every observation must distinguish:

- **OBSERVED** — directly present in the video / analysis.
- **INFERRED** — a production rule inferred from the evidence.
- **CONFIDENCE** — High / Medium / Low.

Suggested per-reference sections:

- Hook
- Narration
- Story / chapter structure
- Shot timing
- Camera / framing
- Main-character usage
- Environments
- Props
- Pattern interrupts
- Stakes / escalation
- Ending / payoff
- Anything uncertain or underreported by the analyser

Do not let analysis of an earlier reference contaminate a later one.

## Rule 2 — Quantify what can be quantified

Avoid vague conclusions such as:

- "fast paced"
- "engaging"
- "cinematic"
- "uses lots of cuts"

Turn them into numbers whenever the raw data supports it.

Examples:

- mean / median shot duration;
- shortest / longest hold;
- percentage of shots <= 3 seconds;
- cuts per 10 seconds;
- scene count;
- hook duration;
- hook word count;
- words per second;
- number of chapters;
- chapter onset percentages;
- final-chapter duration;
- shot-scale distribution;
- main-avatar presence;
- interval between pattern interrupts.

If a metric can be computed from the raw analysis, write a script and compute it.
Do not eyeball a number that can be calculated.

Save the calculations so they are reproducible.

## Rule 3 — Cross-reference only after all independent analyses finish

After all references are complete:

1. Build a cross-reference table.
2. Compare each candidate rule across references.
3. Record:
   - references that support it;
   - references that contradict it;
   - observed count;
   - confidence;
   - whether it becomes a production rule.

A pattern should normally appear in **at least 3 reference videos** before it becomes a
channel-level rule.

A rule can still be included below that threshold only when:
- the evidence is exceptionally strong;
- it is clearly marked optional / low-confidence;
- the Skill does not pretend it is universal.

Do not confuse:
- one-off creative choices;
- analyser mistakes;
- merged cuts;
- underreported subtitles/music/camera;
with channel-level rules.

## Rule 4 — Preserve uncertainty

If the video analyser merges fast montage cuts, misses subtitles, or underreports camera movement,
state that explicitly.

If a measured value needs an "effective cuts" correction or another documented adjustment, keep the
raw measurement and explain the correction.

Never silently rewrite evidence to fit the hypothesis.

## Rule 5 — Build the Production DNA

Synthesize the validated rules into five reusable groups:

1. **Hook DNA**
   - premise shape;
   - wording;
   - hook duration;
   - visual first frame.

2. **Narrative DNA**
   - chapter / beat structure;
   - tense and point of view;
   - escalation;
   - turn;
   - payoff.

3. **Pacing DNA**
   - duration;
   - scene count;
   - shot holds;
   - cut rate;
   - word rate;
   - chapter onset timing.

4. **Visual DNA**
   - subject / avatar role;
   - shot-scale mix;
   - environment changes;
   - lighting progression;
   - prop logic;
   - camera grammar.

5. **Retention DNA**
   - pattern interrupts;
   - plants / callbacks;
   - escalation;
   - chapter cliffhangers;
   - final reframe.

Every important production rule should be:
- measurable when possible;
- supported by evidence;
- executable by another agent.

## Rule 6 — Generate a reusable production Skill

Once the Production DNA is stable, create a new Skill for producing **original** videos in the
learned format.

The generated Skill should contain:

- `SKILL.md`
- `references/hooks.md`
- `references/narrative.md`
- `references/pacing.md`
- `references/visual-language.md`
- `references/retention.md`

When useful, also create:
- validation scripts;
- cost-preflight scripts;
- assembly scripts;
- example plans.

The generated Skill should tell Claude:
- what inputs it needs;
- what defaults it can use;
- how to research;
- how to write;
- how to plan shots;
- how to validate pacing;
- how to generate assets;
- how to assemble;
- how to review the finished output.

## Rule 7 — Originality boundary

The production Skill must recreate the *structure and decision system*, not the creator's identity.

Create:
- an original avatar;
- an original signature prop;
- original worlds;
- original stories;
- original wording.

Do not preserve distinctive reference-channel branding or protected visual identifiers.

## Output layout

Use a structure similar to:

```text
analysis/
  raw/
    R1_*.json
    R2_*.json
    ...
  references/
    R1_*.md
    R2_*.md
    ...
  metrics.py
  metrics.json
  cross_reference.md

<generated-skill>/
  SKILL.md
  references/
    hooks.md
    narrative.md
    pacing.md
    visual-language.md
    retention.md
  scripts/
  examples/
```

Before declaring the Skill finished, summarize:

- strongest high-confidence rules;
- important quantified targets;
- low-confidence / optional patterns;
- analyser limitations;
- what the generated Skill will do differently from simply prompting for "a similar video".
