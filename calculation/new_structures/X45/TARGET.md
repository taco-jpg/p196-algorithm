# X45 target: cross-cell moving-seam closure

**Exact statement under investigation.** For a genuine rooted p12/m9 phase-0 transition
`P(q,k;J,U,C) -> P(q,k+5;J',U',C')` after 120 ordinary decimal reverse-and-add steps,
with the same B34/W9 exterior, q fixed, U/U' among the 30 primitive charge-zero U3 words,
and `|J|,|J'| in {3,4}`, decide whether a finite cycle can use a seam-width change
`delta = |J'|-|J| = +/-1` while compensating with the centre length.

**Lemma supplied.** Every exact edge must satisfy `2|J'|+|C'|=2|J|+|C|` and
`U'=rotate_left(U, delta mod 3)`. More importantly, T12's fixed-cut insertion theorem
extends to these moving seams after the cuts are phase-shifted: a base edge at
`(q,k)=(14,100)` lifts to every independent `q>=14,k>=100`, provided the exact
endpoint edge and the forced U-rotation hold. Thus any finite cycle in this reduced
state graph is an all-width macro-cycle; the finite graph still needs to be searched.

**Remaining missing lemma.** A complete finite closure/emptiness decision for the
phase-locked cross-cell seam graph, including the actual centre values and carry states.

**Not claimed.** No complete seam return, no all-time decimal Lychrel number, and no
exhaustive search over centre coefficient values. The phase-lock theorem and conditional
edge-pumping proof are PAPER PROOF; the script is an independent arithmetic control only.