# T12 route, one period (round 12, agent r12a): the 120-step return has no solution

Target (T12): an exact return Phi^120(P(14,100)) = P(14,105), phase 0, rooted exterior B0 W0^q, 30 charge-zero U3
words (9,a,18-a) and rotations (a even), free junction J and free palindromic centre C.  By T12Rooted120CutPumping
the return at (14,100) is equivalent to the return at every (q,k), q>=14, k>=100.

## 1. Results

| # | Statement | Label |
|---|-----------|-------|
| A | **Seam theorem.** For every one of the 30 words U and every finite junction J (any length), the seam does not return. Hence **no T12 witness exists**, for any J, U, C. | PAPER PROOF (reduction) + COMPUTED (30 finite UNSAT lemmas D_12(V) = empty, two encodings, two solvers) |
| B | **Centre theorem.** For every one of the 30 words U and every palindromic centre C (any length), the centre does not return. Independently of A, **no T12 witness exists**. | PAPER PROOF (reduction) + COMPUTED (30 lemmas E_R(V) = empty, R = 4 or 6; base case \|C\| <= 15) |
| 1 | Task 1: seam SAT (round-11 encoding seamsat.py) \|J\| = 10, 11, 12 x 30 U: 90/90 UNSAT (no SAT). With round 11: every \|J\| <= 12 by direct SAT. | COMPUTED |
| 2 | Task 2: centre SAT (round-11 encoding satc.py) \|C\| = 13, 14, 15 x 30 U: 90/90 UNSAT (no SAT). With census/AC46: every \|C\| <= 15 by direct computation. | COMPUTED |
| 3 | Linear flux invariants: mod 9 the 120-step flux of W and of all 30 U is 0 (no obstruction); mod 11 the alternating charge is reset at every overflow step, leaving one always-satisfiable congruence on J. | PAPER PROOF + COMPUTED (previous r12a agent; log re-run in logs/flux.log) |
| 4 | Observation: a U3 band accepts many inlet histories other than its own (rigid2.py Uinlet: differences already at t = 1 for U6), so the exclusion is not a plain inlet rigidity; it comes from the return constraints of the foreign letters themselves. | COMPUTED (observation only) |

A and B each close the T12 route: **the T12 return equation has no solution.**  No witness, so nothing to replay.
Nothing is claimed about 196, about other phases, other exteriors, other band words or other return times.

## 2. Method

### 2.1 Folded two-carry law (as round 11)
Folded column i, row P_t (pair coefficients 0..18).  alpha_i = low carry entering column i, beta_i = high carry
entering column i-1 from column i; lo_i = (P_i+alpha_i)%10, hi_i = (P_i+beta_(i+1))%10,
alpha_(i+1) = [P_i+alpha_i >= 10], beta_i = [P_i+beta_(i+1) >= 10]; P'_i = lo_i+hi_i if gamma_t = 0 and
P'_i = lo_i+hi_(i-1) if gamma_t = 1.  The clock gamma_t = [t = 0 mod 4] is physically forced (AC46/T12).
The rule is the same at every bulk column (translation invariant), valid for every column that is not the root and
not the middle column.

### 2.2 Free ports
A window [x0, x1) talks to the outside only through: left inputs alpha_x0(t) and, at overflow steps, hi_(x0-1)(t);
right input beta_x1(t); outputs (beta_x0, alpha_x1, hi_(x1-1)) are unconstrained.  A **free port** lets the solver
choose these inputs arbitrarily at every t.  The pair (alpha_x0(t), hi_(x0-1)(t)) is jointly free: every pair in
{0,1} x {0..9} is produced by some P_(x0-1) in 0..18 and alpha_(x0-1), whatever beta_x0 is.  So a free port is a
superset of every genuine context: UNSAT with a free port is UNSAT for every context.

### 2.3 Seam: defect sets D_R(V)
For a rotation V of (9,a,18-a): D_R(V) = set of letters v != V[2] for which the window [y-R, y+171) admits an
assignment with
- columns [y, y+171) = V^57 (V phase 0 at y), column y-1 = v, columns [y-R, y-1) free in 0..18,
- left port FREE at y-R, right port beta_(y+171)(t) = the V background value (all 120 t),
- every column of the window returns (P_120 = P_0).
D_R is non-increasing in R (restrict a depth-(R+1) solution).  Code: rigid2.py defect (encoding = rigid.py encode,
unchanged); independent re-implementation indep_defect.py defect.

**Seam lemma (PAPER PROOF).** If for each rotation V of a there is R <= 90 with D_R(V) empty, then for every rotation
U of a and every finite J the seam does not return.
Proof.  In a witness (q>=14, k large by pumping) every column of [0, J0+|J|+3k) returns (the target left half
B0 W0^q J U^(k+5) agrees with the start on these columns; this is the round-11 seam condition).  Let y* be minimal
such that [y*, J0+|J|+3k) is a factor of the periodic word U^inf (J0 = 34+9q); let V be the rotation with phase 0 at
y*.  All letters of every (9,a,18-a), a even, are even or 9, and W0 ends with the letter 5 at column J0-1, so
y* >= J0; by minimality the letter at y*-1 (a letter of J, or the W letter 5 if y* = J0) is not V[2].
The band [y*, ...) is pure at t=0, so by the T12 cone lemma its protected left edge advances at most 152 < 171
columns in 120 steps (any rotation: 150/151/152); hence beta at y*+171 equals the V background at every t.  The genuine
left context is one choice of the free port.  So the genuine window [y*-R, y*+171) satisfies every constraint of the
D_R(V) instance and its letter at y*-1 lies in D_R(V) = empty.  Contradiction.  (y*-R >= 160-90 > 0: the window never contains the root column.)

**Computed (COMPUTED).** D_12(V) = empty for all 30 V (also D_6 = empty for the six rotations of a = 4, 14).
=> Seam theorem A for all 30 U and every J.
Positive side of the same instances: D_1(V) is NON-empty for 10 rotations (e.g. D_1(U5) = {6,7,15,16},
D_1(U14) = {17}): with a free port directly behind it, a foreign letter can sit in front of a band; the defects
disappear once the free port is pushed back (all D_12 empty).  This shows the defect search does find defects when
the over-approximation allows them.

### 2.4 Centre: comoving defect sets E_R(V)
In the absolute left frame the centre drifts: the target has 15 more U columns before C, so every column of the
centre region must satisfy P_120(i) = P_0(i-15) (and band columns return, 15 = 0 mod 3).
E_R(V) = set of letters v != V[0] for which the window [y-141, y+R) admits an assignment with
- columns [y-141, y) = V^47 (V phase 0 at y-141 and at y), column y = v, columns (y, y+R) free in 0..18,
- left port = exact V background (alpha and the value of column y-142; 141 > 122 = centre-side cone radius),
- right port beta_(y+R)(t) FREE,
- comoving return: P_120(i) = V-continuation if i-15 < y, P_120(i) = P_0(i-15) otherwise.
Code: rigid2.py cdefect; independent indep_defect.py cdefect.

**Centre lemma (PAPER PROOF).** If for each rotation V of a, E_(R_V)(V) is empty, then every centre witness for a
rotation of a reduces to a centre witness C'' with |C''| <= 2 max_V R_V + 3.
Proof.  Folded, C occupies columns y_C .. y_C+h-1 (h = floor(|C|/2) regular columns) followed by the middle.  Let z*
be the first column >= y_C deviating from the U continuation, V the rotation with phase 0 at z*.
Case A: z* + R_V <= y_C + h.  Then the window [z*-141, z*+R_V) consists of regular (non-middle) columns at all times
(the middle only moves right), its left port is the exact background (band pure there by the cone lemma, k large), the
genuine right context is one choice of the free port, and the genuine comoving target is the instance target; so
P_0(z*) lies in E_(R_V)(V) = empty, impossible.
Case B: otherwise C begins with >= h-R_V+1 letters of U continuation (possibly all h).  Strip q whole periods from both
ends: U^k C rev(U)^k = U^(k+q) C'' rev(U)^(k+q) is the same integer, so C'' is a witness (pumping), and
|C''| <= |C| - 6q <= 2R_V+3.

**Computed (COMPUTED).** E_4(V) = empty for 26 V; E_4 non-empty but E_6 = E_8 = empty for V = U5 (16,9,2), U8 (14,9,4),
U23 (4,9,14), U26 (2,9,16).  Base case |C''| <= 15: |C| = 1..6 AC46, 7..12 round-11 census, 13..15 task 2 (this round),
|C| = 0 (empty centre) logs/empty_centre.log.  => Centre theorem B for all 30 U and every C.

## 3. Soundness
- Inputs that are PAPER PROOF from earlier rounds: folded two-carry law, forced clock (1000)^30, T12 cone radii
  (junction side <= 152, centre side <= 122, results/T12MinimalCarryCone.md), pumping (T12Rooted120CutPumping),
  centre/seam independence (round 11).  Base case of B uses AC46 and the round-11 census (COMPUTED).
- Free port = superset of every genuine context (2.2).  Right port of the seam windows and left port of the centre
  windows are exact by the cone lemma; this was also checked on genuine orbits (below).
- Every computed lemma is the UNSAT answer of a finite CNF (no DRAT certificate was produced).  Each of the 60 lemma
  instances (30 D_12, 30 E_R) was solved by (i) rigid2.py + cadical195, (ii) the independent re-implementation
  indep_defect.py + cadical195, (iii) rigid2.py + kissat404 (every one of the 60 instances gave EMPTY in all three runs).

## 4. Validation (all PASS)
- Previous agent: seam controls |J| = 10 (neg UNSAT; planted cone image SAT and replay match; W-continuation return SAT),
  satc.py selftest (6 fixed C agree with AC46 core and simulation; positive controls SAT), rigid.py --noconstraint
  controls SAT (U0 band, W band).
- rigid.py encoding on genuine rooted dynamics, 6 cases (rig2/val_*.log): right port at y+171 == U background; genuine
  init + genuine port reproduces the genuine final row (SAT, also matching intermediate port bits); one changed final
  value UNSAT; return required on a non-returning genuine window UNSAT.
- Positive return control with a non-trivial left context (rig2/wleft_r9_pin_genport.log): the genuine returning
  configuration B0 W0^inf (B is not W) satisfies the free-port RETURN encoding with constraint (P_25..P_33) != W: SAT,
  columns = B suffix.
- Independent re-implementation on genuine BIG-INTEGER orbits (n + reverse(n)): seam side 4 cases
  (indep/genuine_*.log: right port == cyclic background, genuine dynamics SAT, changed final UNSAT, return UNSAT);
  centre side 3 cases (indep/cgenuine_*.log: left port == cyclic background, genuine dynamics SAT, changed final UNSAT).
- Consistency: theorems A and B predict UNSAT for every task-1 and task-2 instance; observed 180/180 UNSAT (90 seam, 90 centre), no SAT.
- Depth-3 rigidity data of the previous agent (16 of 30 U rigid at depth 3 with a free port) is consistent with the
  D sets (one rigid rotation forces D_3, D_2, D_1 empty for its three rotations).

## 5. Numbers
### Seam defect sets D_R(V) (letters that can precede a maximal band V^inf)
| V | word | D_1 (rigid2/cadical) | D_12 rigid2/cadical195 | D_12 indep enc2/cadical195 | D_12 rigid2/kissat404 |
|---|------|------|------|------|------|
| U0 | (9, 0, 18) | empty | empty | empty | empty |
| U1 | (0, 18, 9) | empty | empty | empty | empty |
| U2 | (18, 9, 0) | {5, 14} | empty | empty | empty |
| U3 | (9, 2, 16) | empty | empty | empty | empty |
| U4 | (2, 16, 9) | empty | empty | empty | empty |
| U5 | (16, 9, 2) | {6, 7, 15, 16} | empty | empty | empty |
| U6 | (9, 4, 14) | {15, 16} | empty | empty | empty |
| U7 | (4, 14, 9) | empty | empty | empty | empty |
| U8 | (14, 9, 4) | {7, 8} | empty | empty | empty |
| U9 | (9, 6, 12) | empty | empty | empty | empty |
| U10 | (6, 12, 9) | empty | empty | empty | empty |
| U11 | (12, 9, 6) | empty | empty | empty | empty |
| U12 | (9, 8, 10) | empty | empty | empty | empty |
| U13 | (8, 10, 9) | empty | empty | empty | empty |
| U14 | (10, 9, 8) | {17} | empty | empty | empty |
| U15 | (9, 10, 8) | empty | empty | empty | empty |
| U16 | (10, 8, 9) | empty | empty | empty | empty |
| U17 | (8, 9, 10) | {1} | empty | empty | empty |
| U18 | (9, 12, 6) | empty | empty | empty | empty |
| U19 | (12, 6, 9) | empty | empty | empty | empty |
| U20 | (6, 9, 12) | empty | empty | empty | empty |
| U21 | (9, 14, 4) | {2, 3} | empty | empty | empty |
| U22 | (14, 4, 9) | empty | empty | empty | empty |
| U23 | (4, 9, 14) | {10, 11} | empty | empty | empty |
| U24 | (9, 16, 2) | empty | empty | empty | empty |
| U25 | (16, 2, 9) | empty | empty | empty | empty |
| U26 | (2, 9, 16) | {2, 3, 11, 12} | empty | empty | empty |
| U27 | (9, 18, 0) | empty | empty | empty | empty |
| U28 | (18, 0, 9) | empty | empty | empty | empty |
| U29 | (0, 9, 18) | {4, 13} | empty | empty | empty |

D_12 solve times 20-106 s over 90 runs.

### Centre comoving defect sets E_R(V) (letters that can follow a maximal band, comoving return)
| V | word | E_4 (rigid2/cadical) | R used | E_R rigid2/cadical195 | E_R indep enc2/cadical195 | E_R rigid2/kissat404 |
|---|------|------|---|------|------|------|
| U0 | (9, 0, 18) | empty | 4 | empty | empty | empty |
| U1 | (0, 18, 9) | empty | 4 | empty | empty | empty |
| U2 | (18, 9, 0) | empty | 4 | empty | empty | empty |
| U3 | (9, 2, 16) | empty | 4 | empty | empty | empty |
| U4 | (2, 16, 9) | empty | 4 | empty | empty | empty |
| U5 | (16, 9, 2) | {3, 12} | 6 | empty | empty | empty |
| U6 | (9, 4, 14) | empty | 4 | empty | empty | empty |
| U7 | (4, 14, 9) | empty | 4 | empty | empty | empty |
| U8 | (14, 9, 4) | {2, 11} | 6 | empty | empty | empty |
| U9 | (9, 6, 12) | empty | 4 | empty | empty | empty |
| U10 | (6, 12, 9) | empty | 4 | empty | empty | empty |
| U11 | (12, 9, 6) | empty | 4 | empty | empty | empty |
| U12 | (9, 8, 10) | empty | 4 | empty | empty | empty |
| U13 | (8, 10, 9) | empty | 4 | empty | empty | empty |
| U14 | (10, 9, 8) | empty | 4 | empty | empty | empty |
| U15 | (9, 10, 8) | empty | 4 | empty | empty | empty |
| U16 | (10, 8, 9) | empty | 4 | empty | empty | empty |
| U17 | (8, 9, 10) | empty | 4 | empty | empty | empty |
| U18 | (9, 12, 6) | empty | 4 | empty | empty | empty |
| U19 | (12, 6, 9) | empty | 4 | empty | empty | empty |
| U20 | (6, 9, 12) | empty | 4 | empty | empty | empty |
| U21 | (9, 14, 4) | empty | 4 | empty | empty | empty |
| U22 | (14, 4, 9) | empty | 4 | empty | empty | empty |
| U23 | (4, 9, 14) | {7, 16} | 6 | empty | empty | empty |
| U24 | (9, 16, 2) | empty | 4 | empty | empty | empty |
| U25 | (16, 2, 9) | empty | 4 | empty | empty | empty |
| U26 | (2, 9, 16) | {6, 15} | 6 | empty | empty | empty |
| U27 | (9, 18, 0) | empty | 4 | empty | empty | empty |
| U28 | (18, 0, 9) | empty | 4 | empty | empty | empty |
| U29 | (0, 9, 18) | empty | 4 | empty | empty | empty |

Also E_8 (rigid2/cadical): U5 empty, U8 empty, U23 empty, U26 empty.

### Task 1: seam SAT (seamsat.py), all 30 U
| length | UNSAT | SAT | other/missing | solve time min-max (s) |
|---|---|---|---|---|
| 10 | 30 | 0 | 0 | 171-2791 |
| 11 | 30 | 0 | 0 | 123-916 |
| 12 | 30 | 0 | 0 | 206-1365 |
max RSS 8.5 GB

### Task 2: centre SAT (satc.py), all 30 U
| length | UNSAT | SAT | other/missing | solve time min-max (s) |
|---|---|---|---|---|
| 13 | 30 | 0 | 0 | 68-149 |
| 14 | 30 | 0 | 0 | 61-160 |
| 15 | 30 | 0 | 0 | 72-224 |
max RSS 7.2 GB

Full per-instance listing: summary.txt (output of summarize.py).

Optional third argument, not used: W right-rigidity (rigid2.py Wright: maximal W continuation followed by a foreign
letter, free right port).  Depth 3 is SAT (previous agent); depth 12, phase 0 gave no answer in 27 min (killed).

## 6. Still open
- T12 is closed: no exact 120-step return of this shape exists.  Other routes (other phases, exteriors, band words,
  return times, non-same-J/C returns) are untouched; the defect-set method (free port + maximal band + cone-exact
  far port) is generic and is the natural first test for any future band-junction route.
- The computed lemmas have no proof certificates (DRAT); they rest on two encodings and two solvers.
- Scope: only the same-J/C 120-step return of the phase-0 rooted B34/W9 exterior with the 30 charge-zero U3 words.
  The proof uses the forced clock (1000)^30 and the T12 cone radii; it says nothing about other periods (e.g. 240
  steps), other exteriors or phases, or bands other than U3.
- No Lychrel number; nothing about 196.

## 7. Files (relative to this directory)
Sources: rigid.py (previous agent), rigid2.py, indep_defect.py, seamctl.py (previous agent), flux.py (previous agent),
empty_centre.py, summarize.py, mdtables.py, watchdog.sh, dsetsid.sh, chain_cross.sh, sat_seam/pool.sh,
sat_seam/poolB.sh, sat_centre/pool.sh, rig/pool_Uleft.sh, rig2/defect_pool.sh, rig2/val.sh, cdef/pool.sh,
indep/pool.sh, indep/run_genuine.sh, indep/run_cgenuine.sh, xsolver/pool.sh, inlet/run.sh, wright/run.sh, job lists
(*.txt).  Unchanged copies of round-11 tools (needed for imports): seamsat.py, seam_check.py, satc.py, cone.py,
seam.cpp, census.cpp, centre_census.cpp, independent.py, wbfs.py.
Logs: logs/*.log (controls, flux, empty centre), logs/main_check/ (main-session spot check), per-subdirectory pool tallies
(*/pool.log, *pool*.out), summary.txt (summarize.py), tables.md (mdtables.py).  The per-instance logs of sat_seam/, sat_centre/,
rig/, rig2/, cdef/, indep/, xsolver/, inlet/, wright/ are packed in logs.tar.gz (`tar xzf logs.tar.gz` restores them in place).
The round-11 tools that are only needed for imports (seamsat.py, seam_check.py, satc.py, cone.py) are unchanged copies of
`../../round11/t12_seam/`; census.cpp, centre_census.cpp, seam.cpp, independent.py, wbfs.py are not copied (see round 11).

## 8. Reproduction (python-sat with cadical195 / kissat404; one instance = 20-110 s, <= 9 GB)
The pool scripts were run from `~/p196_run/r12a` on the Studio; from this directory the same commands are:
- Seam sets D_R(V): `python3 rigid2.py defect --U u --r 12 --solver cadical195|kissat404` and
  `python3 indep_defect.py defect --V u --R 12 --solver cadical195` (u = 0..29) -> `RESULT D=[] EMPTY`.
  Positive side: `python3 rigid2.py defect --U 5 --r 1` -> `D=[6, 7, 15, 16] NONEMPTY`.
- Centre sets E_R(V): `python3 rigid2.py cdefect --U u --r R` and `python3 indep_defect.py cdefect --V u --R R --solver cadical195`
  with R = 6 for u in {5, 8, 23, 26}, R = 4 otherwise -> `RESULT E=[] EMPTY`.
- Task 1 / task 2: `python3 seamsat.py seam --U u --Lj L` (L = 10, 11, 12) and `python3 satc.py --U u --L L` (L = 13, 14, 15)
  -> `RESULT UNSAT`; tally `python3 summarize.py > summary.txt`.
- Validation: `rig2/val.sh`, `indep/run_genuine.sh`, `indep/run_cgenuine.sh`; `python3 empty_centre.py`, `python3 flux.py`.
