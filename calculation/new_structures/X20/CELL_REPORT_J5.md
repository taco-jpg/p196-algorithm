# CELL_REPORT_J5 — rooted p12/m9 U6 length-5 junction cell

**Status: EXHAUSTED-NONE**  
**Label: COMPUTED**  
**Scope:** `U=(3,3,9,15,15,9)`, rooted phase-0 p12/m9 exterior, `|J|=5`, 240-step macro `P(q,k;J,C) -> P(q,k+5;J,C)`, all `q>=24`, `k>=100`, all physically realizable palindromic centres. This does not decide other U6 words, `|J|>=6`, moving seams, the U3 target, or global Lychrel existence.

## Reduction

The 240-step clock is exactly `(1000)^60`. The six-column U6 bulk returns after 240 phases (and is half-rotated at phase 120); every phase row has sum 54 and no adjacent 9s. Exact carry-reset cone losses are bounded by 300 coefficients from the junction and 240 from the centre. A cut after 55 U6 copies (330 coefficients) therefore retains at least 30 protected columns on both sides when `k>=100`, so the tracked prefix is independent of `C`. The rooted W9 cut loses 181 coefficients over 240 phases; at `q=24`, the root prefix still reaches index 69 and the insertion cut at 52 retains a W9 period plus reset guard. The two insertion lemmas reduce every fixed-seam return to `(q,k)=(24,100)`.

## Complete endpoint census

The compiled exact carry engine enumerates every ordered length-5 junction over coefficients `0..18`, with no modular, MDD, SAT, or other pruning:

- Search space: `19^5 = 2,476,099` junctions.
- Assertion-enabled run: all four disjoint ID shards completed; checked count reconciles to `2,476,099`.
- W9-prefix restorations at t=240: **0 / 2,476,099**.
- Complete tracked-prefix returns: **0 / 2,476,099**.
- First mismatch indices: **202 through 216**, while the W9 endpoint is index 250.
- Every junction first mismatches 34–48 coefficients before the W9 endpoint.

Mismatch-distance histogram (`distance = 250 - first_mismatch`): `34:32, 36:44, 37:62, 38:661, 39:581, 40:9037, 41:7016, 42:90380, 43:136448, 45:1155148, 46:990192, 47:64869, 48:21629`. The counts sum to `2,476,099`. Since the mismatch is in the rooted W9 band, no seam or centre choice can repair it at the macro endpoint within this cell.

## Independent controls

`u6_240.py` compares the exact local prefix recurrence with full arbitrary-precision decimal `n + reverse(n)` at every phase and an independent LSD digit-array oracle. It covers q=20,24,40,80,160 with scaled k and now includes length-5 J controls. Paired W/U6 insertion checks pass at q=24,40,80,160, including odd and even centre samples. The R30 CLI is U3-specific and is not reused for this U6 result.

Reproduce:

```sh
python3 calculation/new_structures/X20/u6_240.py
g++ -O3 -std=c++17 -pthread calculation/new_structures/X20/scan_u6_j5.cpp -o /tmp/scan_u6_j5
/tmp/scan_u6_j5 24 4
```

**Redirect:** this exhausts only the fixed U6 motif with `|J|=5`; move to another U6 bulk cycle, longer junctions, or a genuinely moving/phase-changing seam. No global no-go is claimed.
