#!/usr/bin/env python3
"""Validate a faceless-what-if-shorts shot plan (or a Higgsfield analysis of a finished Short)
against the production rules measured from the reference set.

Usage:
  python3 validate_plan.py plan.json                  # plan rules (pre-production)
  python3 validate_plan.py plan.json --gate           # + gate before ANY paid job: cost preflight approved
  python3 validate_plan.py plan.json --gate-keyframes # + gate before scene keyframes: approved avatar ref
  python3 validate_plan.py --from-analysis final_analysis.json

All pacing checks use FINAL EDITED shot durations (`dur`), never the raw Seedance source
length (`gen_duration`, >= 4 s). Exit code 1 if any FAIL.
"""
import json
import re
import statistics
import sys

STAMP_RE = re.compile(
    r"\b(day|night|week|month|year|hour|minute|age)\s+"
    r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
    r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|"
    r"eighty|ninety|hundred|\d+)",
    re.I,
)
CTA_RE = re.compile(r"\b(subscribe|follow (me|us|for)|like (and|&) |comment below|link in bio)\b", re.I)
ONSET_TARGETS = [4, 17, 37, 57, 75]
SEEDANCE_MIN_S, SEEDANCE_MAX_S = 4, 30
VISUAL_SOURCES = {"KEYFRAME_REQUIRED", "DIRECT_VIDEO", "REUSE_REFERENCE"}
AUDIO_MODES = {"none", "diegetic"}
AVATAR_SPEC_FIELDS = ["silhouette", "proportions", "materials", "clothing", "identifying_features",
                      "stage_changes"]
# Reference-channel design language the new avatar / prop must not reproduce.
FORBIDDEN_DESIGN = re.compile(r"\b(skeleton|skeletal|skull|bones?|ribs?|glass|glassy|translucent|"
                              r"transparent|see-through|x-ray|lollipop)\b", re.I)
MEDIUM_FAMILY = {"Medium", "Medium Close-Up"}
CLOSE = {"Close-Up", "Extreme Close-Up"}


def words(t):
    if not t or re.match(r"^\s*(\[.*\]|\.\.\.|…)\s*$", t):
        return 0
    return len(re.findall(r"[A-Za-z0-9']+", t))


def norm_scale(s):
    s = s.replace(" Shot", "").strip()
    return {"Extreme Wide": "Wide"}.get(s, s)


def from_analysis(doc):
    inclusive = doc.get("timestamp_convention") == "inclusive"
    shots = []
    for s in doc["scenes"]:
        dur = s["end"] - s["start"] + (1 if inclusive else 0)
        shots.append({
            "id": s["n"], "start": float(s["start"]), "dur": float(dur), "line": s.get("audio", ""),
            "scale": norm_scale(s.get("shot", "Medium")), "avatar": None, "tags": [],
        })
    return {"shots": shots, "_analysis": True}


def production_checks(plan, shots, fails, warns, rows):
    """Execution rules: Seedance source clips + trim, keyframe policy, audio policy, avatar spec."""
    # --- 1. Seedance minimum duration: generate >= 4 s, trim to the planned edited hold ---
    for s in shots:
        sid, dur = s["id"], s["dur"]
        gen = s.get("gen_duration")
        win = s.get("useful_window")
        if gen is None or win is None:
            fails.append(f"shot {sid}: missing gen_duration / useful_window (source clip spec)")
            continue
        if not (isinstance(gen, int) and SEEDANCE_MIN_S <= gen <= SEEDANCE_MAX_S):
            fails.append(f"shot {sid}: gen_duration {gen} must be an integer {SEEDANCE_MIN_S}–{SEEDANCE_MAX_S} s")
            continue
        a, b = win
        if not (0 <= a < b <= gen):
            fails.append(f"shot {sid}: useful_window {win} must lie inside the {gen}s source clip")
        elif b - a + 1e-6 < dur:
            fails.append(f"shot {sid}: useful_window {win} ({b - a:.2f}s) shorter than edited hold {dur}s")
        elif a < 0.15:
            warns.append(f"shot {sid}: useful_window starts at {a}s; Seedance first frames often settle, "
                         f"start at >= 0.2s")
    # --- 5. Keyframe policy ---
    srcs = [s.get("visual_source") for s in shots]
    bad = [s["id"] for s in shots if s.get("visual_source") not in VISUAL_SOURCES]
    if bad:
        fails.append(f"visual_source missing/invalid on shots {bad} (KEYFRAME_REQUIRED|DIRECT_VIDEO|REUSE_REFERENCE)")
    for s in shots:
        if s.get("visual_source") == "REUSE_REFERENCE" and not s.get("reuse_of"):
            fails.append(f"shot {s['id']}: REUSE_REFERENCE needs reuse_of (existing avatar/env/keyframe ref)")
        if s.get("visual_source") == "KEYFRAME_REQUIRED" and not s.get("keyframe_reason"):
            warns.append(f"shot {s['id']}: KEYFRAME_REQUIRED without keyframe_reason")
    for tag, s in (("hook", shots[0]), ("payoff", shots[-1])):
        if s.get("visual_source") != "KEYFRAME_REQUIRED":
            warns.append(f"{tag} shot {s['id']} is not KEYFRAME_REQUIRED (it is the most important frame)")
    n_kf = srcs.count("KEYFRAME_REQUIRED")
    pct_kf = round(100 * n_kf / len(shots))
    rows.append(("keyframe_required_shots", f"{n_kf} ({pct_kf}%)", "only where control is needed; <=60%"))
    rows.append(("direct_video / reuse_reference", f"{srcs.count('DIRECT_VIDEO')} / {srcs.count('REUSE_REFERENCE')}", "—"))
    if pct_kf > 60:
        warns.append(f"{pct_kf}% of shots are KEYFRAME_REQUIRED: do not keyframe every shot by default")
    # --- 4. Avatar reuse: every avatar shot must point at the approved avatar reference ---
    for s in shots:
        if s.get("avatar") and not any(str(r).startswith("avatar") for r in s.get("refs", [])):
            fails.append(f"shot {s['id']}: avatar in frame but refs has no avatar reference (reuse AVATAR_REF/stage)")
    # --- 2. Audio policy ---
    for s in shots:
        mode = s.get("audio", "none")
        if mode not in AUDIO_MODES:
            fails.append(f"shot {s['id']}: audio must be 'none' or 'diegetic'")
        elif mode == "diegetic" and not s.get("audio_note"):
            fails.append(f"shot {s['id']}: diegetic audio must be justified in audio_note")
    n_dieg = sum(s.get("audio") == "diegetic" for s in shots)
    rows.append(("diegetic_audio_shots", n_dieg, "default 0; generate_audio true only on these"))
    # --- 4. Avatar specification + originality guard ---
    av = plan.get("avatar", {})
    spec = av.get("spec", {})
    missing = [f for f in AVATAR_SPEC_FIELDS if not spec.get(f)]
    if missing:
        fails.append(f"avatar.spec missing fields: {missing}")
    stages = {c.get("chapter") for c in spec.get("stage_changes", [])}
    if spec.get("stage_changes") is not None and not {1, 2, 3, 4, 5} <= stages:
        fails.append("avatar.spec.stage_changes must cover chapters 1–5")
    text = json.dumps(spec) + " " + str(av.get("design", "")) + " " + str(plan.get("signature_prop", ""))
    hits = sorted({m.group(0).lower() for m in FORBIDDEN_DESIGN.finditer(text)})
    if hits:
        fails.append(f"avatar/prop reuses reference-channel design language: {hits}")


def gate_checks(plan, fails):
    """Hard gate before ANY paid Higgsfield job (run with --gate)."""
    cost = plan.get("cost_preflight", {})
    for k in ("image", "video", "narration", "total"):
        if cost.get(k) is None:
            fails.append(f"GATE: cost_preflight.{k} missing — run the cost preflight (SKILL.md Phase 3)")
    if not cost.get("approved_by_user"):
        fails.append("GATE: cost_preflight.approved_by_user is not true — ask the user before paid jobs")


def main(argv):
    analysis = "--from-analysis" in argv
    path = [a for a in argv if not a.startswith("--")][0]
    doc = json.load(open(path))
    plan = from_analysis(doc) if analysis else doc
    shots = plan["shots"]
    fails, warns, oks = [], [], []
    rows = []

    def check(name, value, ok, target, hard_ok=True):
        rows.append((name, value, target))
        if not hard_ok:
            fails.append(f"{name} = {value} (target {target})")
        elif not ok:
            warns.append(f"{name} = {value} (target {target})")
        else:
            oks.append(name)

    durs = [s["dur"] for s in shots]
    total = round(sum(durs), 2)
    n = len(shots)
    check("duration_s", total, 50 <= total <= 60, "50–60", 45 <= total <= 64)
    check("shots", n, 0.33 * total <= n <= 0.48 * total, "≈0.4/s (20–26 @55s)", 15 <= n <= 30)
    mean_hold = round(statistics.mean(durs), 2)
    check("mean_edited_hold_s", mean_hold, 2.2 <= mean_hold <= 2.8, "2.2–2.8", mean_hold <= 3.35)
    pct3 = round(100 * sum(d <= 3.0 for d in durs) / n)
    check("pct_shots_le_3s", pct3, pct3 >= 85, "≥85%", pct3 >= 67)
    body_max = max(durs[:-1]) if n > 1 else durs[0]
    check("max_edited_hold_s (excl. final)", body_max, body_max <= 4.0, "≤4.0", body_max <= (5.0 if analysis else 4.0))
    check("final_edited_shot_s", durs[-1], durs[-1] <= 5.0, "≤5.0", durs[-1] <= 5.5)
    cuts10 = round(10 * (n - 1) / total, 2)
    check("cuts_per_10s", cuts10, 3.5 <= cuts10 <= 4.5, "3.5–4.5", 2.6 <= cuts10 <= 5.5)
    short = [s["id"] for s in shots[:-1] if s["dur"] < 1.5 and not
             set(s.get("tags", [])) & {"interrupt", "montage", "flash"}]
    if short and not analysis:
        warns.append(f"holds <1.5s without interrupt/montage/flash tag: shots {short}")

    # Hook
    hook = shots[0]
    q = hook["line"].find("?")
    hook_text = hook["line"][: q + 1] if q >= 0 else hook["line"]
    hw = words(hook_text)
    check("hook_words", hw, 10 <= hw <= 14, "10–14", 9 <= hw <= 15)
    hook_ok = bool(re.match(r"\s*what (would happen )?if you\b", hook_text, re.I))
    check("hook_opener", hook_ok, hook_ok, "'What (would happen) if you…'", hook_ok or analysis)

    # Chapters
    stamps = []
    for s in shots:
        qpos = s["line"].find("?") if s is hook else -1
        for m in STAMP_RE.finditer(s["line"]):
            if m.start() < qpos:
                continue
            frac = words(s["line"][: m.start()]) / max(1, words(s["line"]))
            stamps.append((round(s["start"] + frac * s["dur"], 2), m.group(0)))
    check("chapter_count", len(stamps), len(stamps) == 5, "5", len(stamps) == 5 or (analysis and 4 <= len(stamps) <= 6))
    if stamps:
        first_t = stamps[0][0]
        check("first_stamp_s", first_t, 1.5 <= first_t <= 3.0, "1.5–3.0", first_t <= 3.5)
        onsets = [round(100 * t / total) for t, _ in stamps]
        for i, (o, tgt) in enumerate(zip(onsets, ONSET_TARGETS)):
            check(f"ch{i+1}_onset_pct", o, abs(o - tgt) <= 6, f"{tgt}±6", abs(o - tgt) <= 10)
        final_len = round(total - stamps[-1][0], 1)
        check("final_chapter_s", final_len, 12 <= final_len <= 17, "12–17", 9 <= final_len <= 20)
        if len(stamps) >= 2:
            spans = [b[0] - a[0] for a, b in zip(stamps, stamps[1:])] + [final_len]
            if spans and final_len < max(spans[:-1]):
                warns.append("final chapter is not the longest")

    # Words
    spoken = sum(words(s["line"]) for s in shots)
    wps = round(spoken / total, 2)
    check("words_per_sec", wps, 3.6 <= wps <= 4.2, "3.6–4.2", 3.2 <= wps <= 4.7)
    wmax = max(words(s["line"]) for s in shots)
    check("max_words_per_shot", wmax, wmax <= 16, "≤16", wmax <= 25)

    # Shot mix
    scales = [norm_scale(s["scale"]) for s in shots]
    med = round(100 * sum(x in MEDIUM_FAMILY for x in scales) / n)
    wide = round(100 * sum(x == "Wide" for x in scales) / n)
    close = round(100 * sum(x in CLOSE for x in scales) / n)
    check("pct_medium_family", med, 60 <= med <= 80, "60–80", 50 <= med <= 90)
    check("pct_wide", wide, 10 <= wide <= 30, "10–30", wide <= 47)
    check("pct_close", close, 5 <= close <= 15, "5–15", close <= 25)
    changes = sum(a != b for a, b in zip(scales, scales[1:])) / max(1, n - 1)
    check("scale_change_rate", round(changes, 2), changes >= 0.66, "≥0.66", changes >= 0.5)

    # CTA
    cta = [s["id"] for s in shots if CTA_RE.search(s["line"])]
    check("no_cta", not cta, not cta, "no CTA", not cta)

    if not analysis:
        av = [s for s in shots if s.get("avatar")]
        pav = round(100 * len(av) / n)
        check("pct_avatar_in_frame", pav, pav >= 95, "≥95", pav >= 90)
        tags = [(s["start"], set(s.get("tags", []))) for s in shots]
        # interrupts: every 15s window
        it = [t for t, tg in tags if "interrupt" in tg]
        gaps, prev = [], 0.0
        for t in it + [total]:
            gaps.append(t - prev)
            prev = t
        check("max_gap_between_interrupts_s", round(max(gaps), 1), max(gaps) <= 15, "≤15", max(gaps) <= 20)
        plant = [t for t, tg in tags if "plant" in tg]
        check("plant_in_first_15pct", bool(plant and plant[0] <= 0.15 * total), bool(plant and plant[0] <= 0.15 * total),
              "plant ≤15%", bool(plant))
        check("payoff_on_final_shot", "payoff" in tags[-1][1], "payoff" in tags[-1][1], "final shot tagged payoff",
              "payoff" in tags[-1][1])
        turn = [s for s in shots if "turn" in s.get("tags", [])]
        turn_ok = bool(turn) and all(s.get("chapter") in (4, 5) for s in turn)
        check("turn_in_ch4_or_5", turn_ok, turn_ok, "turn tag in ch4/5", bool(turn))
        # continuity of timeline
        t = 0.0
        for s in shots:
            if abs(s["start"] - t) > 0.15:
                fails.append(f"timeline gap/overlap at shot {s['id']}: start {s['start']} expected {round(t, 2)}")
                break
            t = s["start"] + s["dur"]
        production_checks(plan, shots, fails, warns, rows)
        if "--gate" in argv or "--gate-keyframes" in argv:
            gate_checks(plan, fails)
        if "--gate-keyframes" in argv:
            ref = plan.get("avatar", {}).get("reference", {})
            if not ref.get("job_id") or not ref.get("approved_by_user"):
                fails.append("GATE: avatar.reference.job_id + approved_by_user required before scene keyframes")

    print(f"{'metric':32} {'measured':>10}   target")
    for name, value, target in rows:
        print(f"{name:32} {str(value):>10}   {target}")
    print()
    for f in fails:
        print("FAIL", f)
    for w in warns:
        print("WARN", w)
    print(f"\n{len(fails)} FAIL, {len(warns)} WARN, {len(oks)} OK")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
