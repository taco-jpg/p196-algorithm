# X24 phase-1 rooted p12/m9 cell report

**Status: EXHAUSTED-NONE. Label: COMPUTED + PAPER PROOF; not Lean-verified.** This report covers the neighboring phase-1 W9|J cell, `|J|=3..4`, all 30 charge-zero U3 rows, and both even/odd canonical palindromic centres `C` of lengths 2..13. No odd-centre-only modular gate was applied to even centres.

## Exact search domain

At the reference width `(q,k)=(14,100)`, the compiled local-collar search enumerates the full unfiltered `(U,J)` product:

- `U`: 30 distinct U3 rows;
- `J`: `19^3 + 19^4 = 137,180` words;
- states tested: `4,115,400 = 30 * 137,180`.

For centre lengths 2..13, the legal palindromic coefficient-word count is `sum_{r=1..6}(19^r + 10*19^r) = 546,254,940`; the raw `(U,J,C)` product is `2,248,057,580,076,000`. `C` is not sampled: the U3 reset/cone lemma proves the endpoint result independent of every legal finite centre, including lengths beyond 13. Even centres remain in scope.

The tested necessary condition is endpoint-only: after 120 exact decimal reverse-and-add steps, does the complete rooted `B_1 ++ W_1^q` prefix return? Temporary W9 damage is allowed during the epoch. A finite seam-map cycle cannot exist in this cell without this endpoint condition, even if `J'`, `C'`, or `U'` were allowed to change.

## Soundness and all-width lift

Published phase-1 root data:

- `B_1 = [1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5]`;
- `W_1 = [10,14,13,12,9,7,10,4,5]`;
- overflow clock `gamma[(1+t) mod 12]`, with 30 overflows per 120 steps.

The 170-coefficient collar beyond W9|J exceeds the exact phase-1 U3 cone bounds. The cone pairs across all 30 rows are `(150,121)`, `(151,120)`, `(152,122)`, so left/right advances are at most 152/122. For `k>=100`, 300 U coefficients separate the junction from `C`; no centre carry can reach the tested boundary. The root B prefix remains exact in every searched endpoint.

T12's phase-rotated cut/insertion theorem lifts the reference-width endpoint decision to every independent `q>=14,k>=100`: a W row inserted after two W copies (cut 52) and a U row inserted after 55 U copies commute with the 120-step semantics. `verify_phase1.py` checks both insertion identities through `t=0..120` on representative widths and cross-checks local-collar output against full pairword, fresh-buffer digit-array, and arbitrary-precision integer reverse-add at `(q,k)=(20,100),(40,160),(80,320),(160,640)`.

The R02 361-state MDD was not used as a filter: no committed executable for it was found in the inspected main tree, and the full unfiltered enumeration avoids any completeness dependency on it. The phase-1 control mirrors R30's exact `actual()` arithmetic contract; the repository's symbolic CLI is phase-0-specific, so the all-width lift here uses T12 rather than a phase-mismatched symbolic run.

## Exhaustive result

42 contiguous chunks cover `[0,4,115,400)` with no gaps or overlaps. Aggregate output:

- tested: `4,115,400`;
- clock failures: `0`;
- rooted-B endpoint mismatches: `0`;
- W9 endpoint failures: `4,115,400`;
- W9 endpoint restorations: `0`;
- full-prefix restorations: `0`.

Because B is restored and B+W is not, every endpoint mismatch is strictly inside W9. The physical epoch-edge set for this cell is empty; therefore it has no fixed point or finite epoch cycle. Pi179's SCC bounded-cycle dichotomy is vacuous here and was not invoked because there are no physical edges.

Independent full-integer controls at q=`20,40,80,160` with k=`100,160,320,640` had first mismatch offsets relative to the W9|J cut `-25,-23,-22,-19`. For each, local-collar, full pairword, fresh-buffer digit-array, and Python arbitrary-precision reverse-add agree through all 120 steps. These are controls only; the exhaustive claim comes from the full `(U,J)` scan plus the centre-reset and phase-rotated insertion arguments.

## Reproduction

```sh
g++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/new_structures/X24/strict_w9_cell_local.cpp -o /tmp/x24-phase1
for s in $(seq 0 100000 4100000); do
  /tmp/x24-phase1 --start "$s" --limit 100000
done
python3 calculation/new_structures/X24/verify_phase1.py
```

**Redirect:** do not spend further search budget on phase-1 p12/m9, `|J|=3..4`, U3. Prioritize unresolved phase-0 seam dynamics, longer/moving junctions, or a distinct mixed-U6 cycle. This cell exclusion does not solve the decimal Lychrel problem globally.
