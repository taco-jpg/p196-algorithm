# Z45 Rooted W9 Cut-Shift Obstruction

**Label:** PAPER PROOF.

**Missing-lemma contribution:** no physical 22-column shift can preserve both the fixed rooted exterior `B34` and the W9 band count `q` in the literal concatenated template.

**Proof:** `|B34|=34`, `|W9|=9`, and `22=2*9+4`. Moving only the inner W9 cut left by 22 makes the band span `9q-22`, not `9q`. Translating the whole length-`9q` window left by 22 moves its left edge to coefficient index `34-22=12`, inside the fixed exterior. The actual root has `B[12]=10`, while `10` is absent from every phase of `W9=[5,18,4,8,1,15,4,0,5]`; hence no phase can match at the overlap. A pure coordinate reindexing changes no physical coefficient and cannot relocate the mismatch into the seam.

**Scope:** literal `B34 ++ W9^q ++ J ++ U3^k` with fixed rooted exterior and fixed `q`; not a no-go for a differently defined, non-concatenative template family.

**Reproduction:** `python3 calculation/new_structures/Z45/cut_shift_obstruction.py`.

**Redirect:** a viable shift must explicitly change another physical component or the template definition; a `+22` coordinate label alone is not a repair.
