Main-session check of r12f (2026-11-08, ~/p196_run/mchk12f on the Studio; nothing of r12f modified).
1. Col0Clock.lean recompiled with core Lean 4.19.0: exit 0, no sorry/native_decide, axioms propext, Classical.choice, Quot.sound.
   Statement read line by line: genuine reverse-and-add on Nat (digit lists), Genuine.lemmaK and Genuine.lemmaK_lower.
2. bcheck.py = third encoding of B_1, written only from the folded law (no code shared with brestore/mbres/mdefect/mindep).
   Rectangle window [y-R, y+172), T = 120, standard clock, plain (non-group) instance: all 30 V, R = 12, foreign letter at y-1:
   30/30 UNSAT (kissat404, 15-28 s), 3 of them also cadical153. g = 45 (final condition on [y+45, ..)): 30/30 UNSAT.
   Controls: no foreign constraint SAT; g = 70 SAT for 3 V (976-1522 s).
   bcheck.py validate (seeds 1-4): genuine big-integer orbits (q = 20, random J, V, C): law checked on all columns; with the
   genuine port the model equals the genuine letters at every (t, c); forbidding a genuine final letter is UNSAT;
   band start moves right by 60-63 columns per epoch.
3. bcheck.py cones: l_(120j) <= 150j+2, r_(120j) <= 120j+2 (j <= 40), one-epoch left front <= 152 from every rotation,
   exactly one 9 per period in every row, minimal period (at equal clock phase) 120: PASS for all 30 V.
4. Read the proof of Theorem A / Main Theorem (FINAL sec. 3, 4, 6) step by step; application of Lemma K to pair words checked.
   No error found.
