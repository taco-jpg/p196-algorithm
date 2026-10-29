# CELL LEDGER (census coverage; maintained by agent AB59 and the lead)

Predicate for every cell: rooted p12/m9 template B_p||W_p^q||J||U^k||C||rev(...), exact 120-step physical carry/overflow semantics, reference width (q,k)=(14,100) with the T12 cut/insertion lift, **endpoint-only return of the SAME J, same C, W9 prefix and U flank (k->k+5)**. "strict-W9 phasewise" pruning is only sound for strict trajectories and is labelled as such. All entries are agent-reported (COMPUTED) unless marked; independent audit Z53 found no unsound prefilter in ten of them. NONE of these is a certificate.

| cell | status | source |
|---|---|---|
| junction phase 0, \|J\|=3-4, >=10 U rotations (incl. U6 words), odd+even C | EXHAUSTED-NONE | V/W/X/Z agents, #474/#475 CELL lines |
| junction phase 1, \|J\|=3-4, all 30 U (4,115,400 tested) | EXHAUSTED-NONE | Z agents |
| junction phase 0, \|J\|=5, several U (2,476,099 J words per U), slices 10/12, 11/12 | EXHAUSTED-NONE | Z03, Z10 |
| junction phase 0, \|J\|=6, slice 3/12 (U ranks 3/15/27), 141,137,643 J/U pairs | EXHAUSTED-NONE (endpoint-only) | Z14 |
| centre-only, all 30 U, palindromic C of length 1-6, both parities | EXHAUSTED-NONE (no endpoint transition restores both U flanks) | S05, V37 |
| two-coefficient W\|J collar extension, 361 pairs, q=k=20/40/80/160 | all lose W9 prefix by t=120 | S15 |
| period-2 bulk census, 360 non-all-9 U in {0..18}^2 | only trivial diagonal 240-returns | S42 |
| known one-epoch W9-preserving seams (R18 phase4 J24, R12 J40, R13 J17, N27, N09, S30 J50, R24) | lose ~22 W9 columns at epoch 2; lead replay of R18-t4 J24: 245 mismatching coefficients at t=120 (junction window ~85 + centre window ~50 per half), W9 and length exact | lead, 2026-10-29 |
| UNCOVERED (priority) | junction phases 2..11 with \|J\|=3-4; \|J\|=5 other phases/U; \|J\|=6 all but slice 3/12; centre \|C\|>=7; \|J\|>=7 (needs a SOUND endpoint-only pruner; the strict-W9 MDD artifact is absent from main) | -- |
