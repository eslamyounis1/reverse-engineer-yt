# Retention DNA

## 1. Chapter stamps as micro-cliffhangers (5/5, High)

Each spoken time stamp resets attention and implicitly promises the next jump.

- Stamp onsets fall at ≈ 4 / 17 / 37 / 57 / 75% of runtime. Never leave more than 15 s between stamps.
- **On-screen chapter label:**
  - Show it when the stamp is spoken, for 1.2 s, in the upper third, e.g. "DAY 1", "YEAR 30".
  - Observed in 2/5; the analyser may under-report it (Medium confidence).
  - It is on by default and `assemble_short.py` burns it.

## 2. Pattern interrupts: at least 1 every 15 s (5/5, High)

Observed spacing is about 8–15 s. Tag each one `interrupt` in the plan. Choose from this menu
and vary the type across the video:

| Interrupt | Evidence | Build |
|---|---|---|
| New threat enters the frame | R2 bear (17 s), wolves' eyes (38 s) | The threat in the foreground, the avatar small behind |
| Visual anomaly | R2 hallucination, R3 glowing eyes, R4 glitching Earth | One impossible or glowing element in an otherwise normal frame |
| Direct-to-camera look | R3 menacing grin (21 s) | A static CU, the avatar staring into the lens. Once per video |
| Genre intrusion | R5 modern soldiers in a primitive world; R4 office email in space | Something from another era or genre arrives |
| Lighting or tonal flip | R1 neon party → night balcony at the turn | Hard change of lighting key on the cut |
| Sound beat | R5 1 s silent SFX splash | A 1 s shot with no narration, impact frame |
| Comic deflation | R4 ×3 | Spectacle + mundane complaint line |

## 3. Plant → payoff (3/5, High as a technique)

- Plant one original object or constraint in chapter 1, within the first 15% of runtime.
- Pay it off in the **final shot**: the object reappears in a changed context (R1, R5), or the
  constraint is removed (R3).
- Optional mid-video echo: the prop shows up as an environmental detail.

## 4. The turn and the escalation curve (5/5)

- Chapters 1–3 build. The turn arrives at chapter 4 or 5 (50–78% runtime).
- The turn chapter gets the most contrasting lighting key and the strongest interrupt.
- The stakes in the final chapter are the highest in the video: life/death, freedom, the
  meaning of the whole life, or the existence of the world.

## 5. Ending mechanisms (5/5: no CTA)

Choose one:

| Mechanism | Evidence | Shot pattern |
|---|---|---|
| **Moral reframe + calm tableau** | R1 | Final line ends on a single word → Wide calm frame with the payoff prop, held 3–4 s |
| **Reversal line + silent hold** | R5 | Reversal line → 2–3 s music- or silence-only tableau with the prop callback |
| **Triumphant release + push-in** | R3 | Constraint falls away → push-in to an emotional CU, 4–5 s |
| **Open dread / twist** | R4 | Twist line split across 2 shots → the avatar small against an overwhelming image; no resolution (good for loops) |
| **Warm coda + light joke** | R2 | Relief → reunion → a one-line wry closer over a cozy interior |

Rules:

- The final shot is the only shot allowed to run 4–5 s.
- Never add an end card, a logo, or a "subscribe" line.
- **Loop seam (optional):** make the final frame's composition echo frame 1 (same scale and
  placement, transformed avatar), so a replay feels continuous.

## 6. Retention checklist (validator tags)

- [ ] `hook` on shot 1 with a 10–14-word question
- [ ] First time stamp at 1.5–3.0 s
- [ ] 5 stamps at the target onsets
- [ ] At least one `interrupt` in every 15 s window
- [ ] `plant` in the first 15% and `payoff` on the final shot
- [ ] `turn` tag in chapter 4 or 5
- [ ] No CTA words in any line
