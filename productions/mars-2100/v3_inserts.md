# Cut v3: new voice + re-paced animation (proposal)

**Narration.** Sterling at natural speed (speech_rate 0), with dead-air pauses capped at
0.35 s, or 0.6 s between chapters.

| | Old (Archie, rate 75) | New (Sterling, rate 0) |
|---|---|---|
| Length | 58.25 s | 83.43 s |
| Pace | 4.07 words/s | 2.84 words/s |
| Media | — | `2590dfbd-6746-401f-97be-2e67179681ee` |

**Problem.** Re-timed to the new voice, 12 of the 26 shots would have to hold for 3.7–5.3 s.
The clips are only 4 s long, so this would mean slow-motion or long static holds, which is
boring.

**Fix.** Keep all 26 approved clips and add 12 new insert shots, taking the video from 26 to
38 cuts. The mean hold is about 2.2 s, the same visual rhythm as cut v2. Each insert adds a
small comic or story beat that matches the words spoken at that moment, and Pip stays the
same character.

Every insert uses DIRECT_VIDEO with the approved stage avatar plus the chapter environment
reference, at 4 s, 1080p, no audio, on seedance_2_5. No new images are needed.

## New insert shots

| # | Plays during (words) | Stage | New beat (amusing, on-script) |
|---|---|---|---|
| 1b | "…born on Mars in the year 2100?" | newborn | Wide aerial over the red plain: a cluster of colony domes half-buried in red soil, a rover trundling past a "MARS COLONY · EST. 2081" sign |
| 2b | "…three metres of dirt that blocks radiation" | newborn | Cut-away cross-section: a cosy nursery deep underground, layers of red dirt above, a sleeping bundle in a crib |
| 7b | "…a third of an Earth kid" | child | Pip lifts a crate stamped "HEAVY" over its head with one hand, and a classmate's jaw drops |
| 8b | "…a slow, floating flight" | child | Pip bounces too high and bumps gently into the tunnel ceiling, then drifts down giggling past a teacher shaking her head |
| 13b | "…swallows the whole planet for months" | teen | High wide shot: a towering rust-red dust wall rolls over the domes and swallows them |
| 14b | "…the colony rations every watt" | teen | Pip pedals an exercise bike hooked to a single dim light bulb so a younger kid can read a book |
| 15b | "…by hand, sol after sol" | teen | Pip, dusty and exhausted, flops face-first into a dust drift, then pops up and keeps shovelling |
| 16b | "…the only green for kilometres" | teen | Pip waters the tiny sapling with an eyedropper, one careful drop at a time, as the storm sky outside clears |
| 17b | "…a seat on the ship to Earth" | adult22 | Pip does a goofy victory dance in its quarters, waving the glowing boarding token |
| 18b | "…every twenty-six months. You've waited years." | adult22 | A wall of crossed-off paper calendars; Pip draws the final X with a marker |
| 20b | "…you'd feel nearly three times heavier" | adult22 | A gravity-simulator display: Pip's hologram on a 1 g planet squashes flat like a pancake |
| 20c | (same line, second half) | adult22 | Pip strains to lift a small dumbbell labelled "1 g" and it won't budge |

The existing shots keep their content. Only the cut points change, and each one is placed
0.05 s before the first word of its line. The same J-cuts are kept, along with the same
labels, captions style, diegetic audio on shot 17, and the daylight ending.

## Cost

| Item | Credits |
|---|---|
| 12 new shots × 48 (seedance_2_5, 4 s, 1080p, final) | 576 |
| New narration (already spent: Sterling takes, including the discarded +10 set) | ~17 |
| Images | 0 |
| **Total new** | **≈ 593** |

The balance before this step was about 2,165 credits.

**Cheaper option.** Generate 480p drafts first (12 × 12 = 144), then finalize only the
accepted ones (+48 each). This raises the total to about 720 credits if all 12 pass.
