# Z45 growing-seam epoch map, variant 4

**Status: EXHAUSTED-NONE (structural; 6,859/6,859 extension-word pairs excluded). Label: PAPER PROOF.** This is a route-local obstruction, not a decimal Lychrel nonexistence theorem and not a successful certificate.

## Exact scope

Rooted phase-0 p12/m9 template `P(q,k;J,U,C)=H C reverse(H)`, `H=B34 W9^q J U^k`, with `|B34|=34`, `|W9|=9`, `|U|=3`, fixed `q`, fixed centre `C`, and the exact 120-step overflow clock `100010001000` repeated ten times. Variant 4 uses `J'=w1 J w2`, `|w1|=1`, `|w2|=2`, over pair-coefficients `0..18`, while requiring `k -> k+5` and unchanged W9 column count. There are `19^3=6,859` possible `(w1,w2)` pairs.

## Exact length algebra

The clock has 30 overflow bits, so a genuine 120-step edge changes the decimal digit length by exactly `30`. The template length is

`L(q,k;J,C) = 2*(34 + 9q + |J| + 3k) + |C|`.

For `d=|J'|-|J|`, fixed `q,C`, and `k -> k+5`, the template's length change is `2*(d+15)=30+2d`. Exact return therefore requires `d=0`; the assigned `d=3` edge is impossible for every coefficient choice. More generally, with fixed centre but allowing integer `Δq`, `9*Δq + 3*Δk + d = 15`; setting `Δk=5` forces `9*Δq=-d`, impossible for `d=1,2,3`. A coefficient-cut reindexing by `+22` is not a length-changing operation and cannot pay the extra six digits. If the centre length were allowed to change, one edge would require `Δ|C|=-2d`; a fixed positive `d` would make a finite centre shrink without bound over repeated epochs.

The supplied mismatch positions `(+1,-22,-43,-66,-89)` have exact successive differences `(-23,-21,-23,-23)`. Thus the stated `-22` is an approximate drift, not an exact constant decrement. In a bookkeeping model that assumes `q_new=q_old-22+s`, keeping the count requires `s=22`, but that equation alone says nothing about physical carry closure.

## Independent controls

`python3 calculation/new_structures/Z45/length_ledger.py` constructs canonical decimal integers from the physical B34/W9 pair-coefficient data and `U=(9,6,12)`, and compares Python big-integer reverse-and-add against an independent schoolbook digit-array implementation. At `q=20,40,80,160` with `k=5q`, all 480 ordinary steps agree and the exact overflow pattern is reproduced. Each control gains 30 digits; its fixed-J `k+5` template also gains 30, while the literal `d=3` growing-seam template gains 36. These are semantic/length controls only, not evidence of a surviving orbit or a seam candidate.

| q | k | Start digits | Overflow bits | Actual gain | Fixed-J target gain | Growing-J target gain |
|---:|---:|---:|---:|---:|---:|---:|
| 20 | 100 | 1,031 | 30 | 30 | 30 | 36 |
| 40 | 200 | 1,991 | 30 | 30 | 30 | 36 |
| 80 | 400 | 3,911 | 30 | 30 | 30 | 36 |
| 160 | 800 | 7,751 | 30 | 30 | 30 | 36 |

**REDIRECT:** The literal variant-4 `(1,2), k+5` family is closed by the global length invariant even under a coefficient-cut reindexing; the next length-compatible branch is `(1,2), k+4`, whose physical carry closure is still UNDECIDED. No ALERT is warranted.
