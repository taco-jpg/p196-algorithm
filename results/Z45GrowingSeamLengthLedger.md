# Z45 Growing-Seam Length Ledger

**Label:** PAPER PROOF.

**Missing-lemma contribution:** proves that a rooted p12/m9 120-step edge with fixed centre and `k -> k+5` must preserve the literal seam length, even if the W9 cut is reindexed.

**Statement:** The physical overflow clock has 30 ones, so the decimal length gain is 30. For `P=H C reverse(H)`, `H=B34 W9^q J U^k`, `|W9|=9`, and `|U|=3`, the target `q'=q`, `k'=k+5`, `J'=w1 J w2` has length gain `30+2d`, where `d=|w1|+|w2|`. Thus `d=0` is necessary; every positive seam extension of length 1–3 is impossible for this literal target.

**Scope:** all coefficient values and all charge-zero U3 words of length 3; fixed centre and exact 120-clock. Not a global no-go for alternate `k` increments or a different centre/growth family.

**Reproduction:** `python3 calculation/new_structures/Z45/length_ledger.py` (four independent big-integer/digit-array length controls).

**Redirect:** test the length-compatible `d=3`, `k -> k+4` branch; no physical carry closure is claimed.
