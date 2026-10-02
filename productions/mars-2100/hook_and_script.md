# Hook selection and final script

## 3 hook candidates (scored against `references/hooks.md`)

| # | Hook | Words | Opener | Visual in frame 1 | Keeps the turn hidden | Verdict |
|---|---|---|---|---|---|---|
| A | **What would happen if you were born on Mars in the year 2100?** | 13 | default "What would happen if you" (4/5 refs) | ✔ newborn in a buried Mars nursery, red dust past the porthole | ✔ | **Selected** |
| B | What if you were the first child ever born on Mars? | 11 | variant "What if you" (1/5) | ✔ | ✔ | Drops the 2100 premise you set; "first child" also gives away the final line |
| C | What would happen if you grew up on Mars and could never visit Earth? | 14 | default | ✔ | ✘ reveals the chapter-4 turn in the hook | Rejected |

Why A wins:

- It is inside the 10–14-word band and uses the dominant opener.
- It carries both displacement axes (place: Mars; era: 2100).
- It passes all five premise gates in `hooks.md`:
  1. **Visual in frame 1:** a newborn in a Mars nursery.
  2. **Five chapters of escalation:** birth → school → storm → departure → legacy.
  3. **A turn exists:** the medical scan.
  4. **Original:** not one of the five reference premises.
  5. **Factual and safe:** see `research.md`.
- It does not spoil the payoff.
- "year 2100" sits inside the question, so the validator treats it as premise, not a chapter stamp.

## Final narration script (5 chapters, ~228 words)

Pre-narration timings come from `plan.json`. Phase 5 retimes them to Whisper word timestamps.

| Chapter | Stamp | Onset | Narration |
|---|---|---|---|
| Hook | — | 0.0 s | What would happen if you were born on Mars in the year 2100? |
| 1 | **Day one** | 2.4 s (4%) | Day one. You're born under three metres of dirt that blocks radiation. Your first cry reaches Earth twelve minutes later. Earth sends back a gift: an apple seed in a tin cup. |
| 2 | **Year six** | 9.8 s (17%) | Year six. You weigh just over a third of an Earth kid. Every jump in the school tunnel becomes a slow, floating flight. Outside, without a suit, the thin air would boil your blood. The noon sky is butterscotch. The sunsets glow blue. |
| 3 | **Year fourteen** | 20.2 s (35%) | Year fourteen. A dust storm swallows the whole planet for months. The solar panels go dark. The colony rations every watt. You dig the greenhouse out by hand, sol after sol. Your seed is now a sapling, the only green for kilometres. |
| 4 | **Year twenty-two** (turn) | 30.2 s (53%) | Year twenty-two. You finally win a seat on the ship to Earth. Launch windows open every twenty-six months. You've waited years. Then the medical scan flashes red. You grew up in Mars gravity. On Earth, you'd weigh almost triple. The ship leaves without you. |
| 5 | **Year thirty** (payoff) | 42.6 s (74%) | Year thirty. You run the largest garden on Mars. The seed from Earth is now a tree taller than you. Then a baby is born in the nursery where you were born. You plant a new seed in a tin cup. You were never an Earthling on Mars. You're the first Martian. |

- **Structure:** lifespan premise; gaps 0 → 6 → 14 → 22 → 30 years.
- **Turn:** an inversion. The dream of "going home" fails.
- **Payoff:** a perspective reversal. Home was never Earth.
- **Plant → payoff:** the tin cup and seed (ch1) → sapling (ch3) → tree, then a new seed in a new tin cup (ch5).
- **No CTA.**
