# X45MovingSeamPhaseLock

**Label:** PAPER PROOF.
**Missing-lemma contribution:** a phase-shifted U3 insertion theorem for rooted p12/m9 moving seams with `|J'|-|J|=+/-1`.
**Theorem:** every exact 120-step edge obeys `2|J'|+|C'|=2|J|+|C|` and `U'=rotate_left(U,(|J'|-|J|) mod 3)`.
**Pumping bridge:** because the source/target U cuts differ by the same shift as their periodic U rows, an exact edge at `(q,k)=(14,100)` lifts to every independent `q>=14,k>=100`; the W9 cut is common.
**Scope:** rooted `(1000)^30` clock, all 30 U3 words, both centre parities, seam widths 3/4.
**Controls:** `calculation/new_structures/X45/phase_lock.py` checks 480 genuine decimal trajectories at q=20/40/80/160, k=100 (57,600 step comparisons), all 120 phases and shifted insertion identities.
**Not claimed:** no exact finite seam edge or cycle has been found; no exhaustive centre-value search; no decimal Lychrel certificate.