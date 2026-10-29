# AC30: phase-9 J5 two-centre all-width exclusion

**Label: PAPER PROOF**, supported by an exact **COMPUTED** 60-entry gate table. Scope: rooted decimal p12/m9 phase 9, canonical rows B9/W9, 120 true reverse-add steps, independent q>=14,k>=100, every J in {0,...,18}^5, all 30 rotations U=(9,a,18-a) with a even 0..18, and **exactly C=(4,14,4) or C=(4,4)**, palindromic centre coefficient words. The literal endpoint return P(q,k)->P(q,k+5) is impossible in this entire specified family. This excludes neither other centres nor moving/growing seams and establishes NO base-10 Lychrel certificate.

**Missing all-time-proof lemma supplied:** the protected centre-side three-site collar at the end of a 120-step epoch cannot equal its literal target for either specified centre, for any stationary five-site junction, because the two-ended carry influence cones from J and C are rigorously separated.

## Proof

Write P(q,k)=H+C+reverse(H), H=B9+W9^q+J+U^k. The exact decimal transition normalizes P with a forward carry and then folds the successor digits, with a shifted reflected index for gamma=1. This is the ordinary integer reverse-and-add formula, not a literal small-radius CA heuristic.

The original T12 two-carry reset-cone lemma establishes that differences in carry are forgotten at every coefficient x!=9 and propagated only through x=9. Rotate its clock to phase 9: gamma=1 iff (9+t) mod4=0, exactly 30 overflows through 120 steps. Independently checking all 30 temporal U-row sequences, every U_t consists of one isolated 9 per three-letter period, returns to U_0 at step120, and yields the phase-9 junction-side/centre-side defect-front advances (151,120), (150,121), (152,122) for its respective three rotations (10 words each). See phase9_cones.py for the finite exact recurrence check. Front movement is nondecreasing through all 120 phases.

At k=100 the two fronts enter a 300-coefficient U interval from opposite ends, leaving at least 300-152-122=26 unaffected coefficients between them at EVERY intermediate step. The same is true for k>100. Thus any change to J, however large its coefficients, is causally unable to affect the innermost 3 output coefficients, including the gamma-one reflected-carry lag, after 120 true steps. For q>=14 the rooted W phase clock and protected U cut persist by the phase-9 two-counter insertion/reset argument (phase-9 W rooted retreat is 92 with cut 52 protected). Hence a single literal q=14,k=100 witness of a midpoint-near mismatch for a given (U,C) rules out all independent q>=14,k>=100 and every fixed J of length five. No strict phasewise W9 MDD pruning is used.

## Finite centre table and independence

For each of the 30 U and the two listed C, use a canonical physical number realizing P(14,100;J,U,C) with J=(0,0,0,0,0), and run genuine ordinary decimal reverse-and-add for 120 steps. Let h=floor(length(P_120)/2). In every case one of the coefficients at positions h,h-1,h-2 differs from the required literal target P(14,105). The 60 exact rows are emitted by centre_gate.py with zero-based U index, complete U, C, mismatch distance and the actual/expected three coefficients. Counts:

- Even C=(4,4): nearest midpoint mismatch distances {0:29, 2:1}; only U=(9,0,18) needs distance2 (centre two coefficients themselves return).
- Odd C=(4,14,4): nearest distances {0:26, 1:4}; U zero-based indices 0,10,26,27 need distance1.

None has distance>2. This decides the **30*19^5=74,282,970** J/U possibilities for EACH of the two fixed centres by a finite 60-case table PLUS the all-width carry-independence theorem. It is NOT a literal enumeration of 148,565,940 J/U/C windows. The earlier independent odd-C mod11 gate and exhaustive 450,242-case digit-array endpoint census provide a separate cross-check.

The Python test makes **300** 120-edge source-number trajectories total: 60 at q=14,k=100 and another four widths for each (q,k)=(20,80),(40,160),(80,320),(160,640), with varied 5-site J. At all 36,000 physical steps, two independent implementations (schoolbook digit-vector, Python arbitrary-precision integer addition) agree exactly and all overflows match the phase-9 clock. These are controls, not the all-width proof; that is the two-carry reset-cone argument above.

## Reproduction

From the repo root, run:
python3 calculation/new_structures/AC30/phase9_cones.py
python3 calculation/new_structures/AC30/centre_gate.py 0 10
python3 calculation/new_structures/AC30/centre_gate.py 10 20
python3 calculation/new_structures/AC30/centre_gate.py 20 30

Each of the last three commands checks 100 two-engine trajectories, outputs 20 exact table rows, and asserts a midpoint-near mismatch for every row. A full 120-edge exact endpoint full-pairword return cannot coexist with an innermost-coefficient mismatch.

**Scope limits / UNDECIDED:** no claim covers arbitrary other palindromic centres (even of the same lengths), mutable seam J, mixed-U macro returns, q-changing returns, or any actual decimal all-time Lychrel orbit. No first-temporal-failure histogram is asserted: this is an endpoint-only necessary-condition exclusion, not strict-phase pruning.
