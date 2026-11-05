# PremiseBReachEqualsAgent120

**Claim (PAPER PROOF, lemmas checked exhaustively — COMPUTED; 2026-11-04).** Premise (B) of ReachDiskRounds6to8 holds for 9-wire
streams. Fix base b, period T, clock g and stream e. Then the map v -> (trim v[t])_t is a bijection from the accepting reach
histories of height H with stream e onto the Agent120 exteriors (T, g, e) of width <= H (Theorem B). So an exterior gives a
reachable stream; a reported stream is a genuine B-cycle; the first height equals the minimum width; and COMPLETE without stream e
means there is no exterior of any width. The ROT quotient (Lemma R) and bx = reach (Lemma X) are proved in the same file.
**Bands (Theorem B').** A uniform-band template of height H with combined period T* = lcm(left-end period, band period) gives an
accepting reach path at height H or H+1; the +1 is real (base-10 example in the proof). Band exclusions at T therefore cover exactly
the templates with combined period T, and reported band fit heights (13/18, 55/75) are left-end height + 1.
**Method.** `calculation/decimal_frontier/round11/premiseB/PROOF.md`; exhaustive checks `chk_step.py`, `chk_int.py`, `chk_cycles.py`, `rotchk.sh` (0 mismatches).
**Not claimed:** premise (A) (soundness of finite window filters beyond the proofs in round9/last_cell); anything about 196.
