# R08MovingSeamShield
**Label:** PAPER PROOF (finite arithmetic kernel, independently replayed).
**Scope:** Base 10, rooted p12/m9 B34/W9, q in {20,40,80,160}, all 30 complement-nine U3 rotations, all r>=200, and every canonical palindromic middle D of any size.
**Theorem:** For P=B W^q U^r D rev(U)^r rev(W)^q rev(B), its true 120-step pairword never begins with the literal B W^q.
**Proof:** Exact three-column two-ended carry-shield induction; a finite kernel checks 120 phasewise carry-reset guards and the nonzero W boundary defect for each of 120 (q,U) cases.
**Consequence:** A moving junction which permanently recedes inward across at least 200 U copies cannot periodically repair this W/U boundary for these q; a regeneration search must keep its emitter near the boundary or alter W.
**Not claimed:** No decimal Lychrel number proved, no general all-q theorem, no exclusion of boundary-attached active emitters, and no nonpalindrome certificate.
**Reproduce:** python3 calculation/new_structures/R08/shield.py
**Evidence/derivation:** calculation/new_structures/R08/{TARGET.md,NOTES.md,IDEAS.md,shield.py}.
