# reverse-engineer-yt

This repo reverse-engineers the **faceless hypothetical-storytelling Shorts** format from
Helix² (@H3lixSquar3d) into a reusable production Skill. The Skill generates original content.

## Layout

```
analysis/
  raw/R1…R5_*.json        Higgsfield scene-by-scene analyses (evidence)
  references/R1…R5_*.md   independent per-video analyses (observed / inferred / confidence)
  cross_reference.md      cross-video evidence, quantified rules, Production DNA
  metrics.py              computes every number in the docs from raw/ → metrics.json
faceless-what-if-shorts/  the generated Skill
  SKILL.md                pipeline: premise → script → plan → GPT Image 2.5 → Seedance 2.5 → narration → assembly → captions → QC
  references/             hooks, narrative, pacing, visual-language, retention
  scripts/validate_plan.py  plan / finished-video rule checker
  scripts/assemble_short.py sandbox assembler (tested locally with ffmpeg)
  examples/example_plan.json  original example plan (0 FAIL / 0 WARN)
```

## Reproduce

```
python3 analysis/metrics.py
python3 faceless-what-if-shorts/scripts/validate_plan.py --from-analysis analysis/raw/R2_FEPc8jsf_Wc.json
python3 faceless-what-if-shorts/scripts/validate_plan.py faceless-what-if-shorts/examples/example_plan.json
```

## Install the Skill

Copy `faceless-what-if-shorts/` into your Claude skills directory, e.g. `~/.claude/skills/`.
The Skill requires the Higgsfield MCP server.
