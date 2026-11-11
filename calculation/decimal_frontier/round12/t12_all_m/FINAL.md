# T12 route, every period (round 12, agents r12f, r12f2, r12f3): Phi^(120m)(P(q,k)) != P(q,k+5m)

2026-11-08.  Run on the Studio in ~/p196_run/r12f; this directory holds its sources and logs.  Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF /
UNDECIDED.  Nothing here is a statement about 196.  No Lychrel number and no certificate is found or claimed; the
results below are EXCLUSIONS (they close one candidate mechanism for all time; they do not produce an instance).
Status: final (08:32 UTC).

## 0. Headline

**Main Theorem (label: PAPER PROOF, with COMPUTED inputs: B_1 = empty and the exact cone recurrences).**  For every m >= 1, every q >= 0, every U among the 30 rotations of
(9,a,18-a) (a even), all finite pair words J, C, and every k >= 90m+10:
            Phi^(120m)(P(q,k)) != P(q,k+5m).
It is the composition of three ingredients:
* **Lemma K (column-0 clock lemma; PAPER PROOF in sec. 3 with COMPUTED checks.  A Lean proof, Col0Clock.lean, theorems
  Genuine.lemmaK / Genuine.lemmaK_lower, was written and compiled by the agent; it is NOT part of this commit and the repository
  label of Lemma K is PAPER PROOF until it is added under lean/ with a registry fragment).**  Every m-return has the standard overflow clock gamma_t = [t = 0 mod 4], for every
  m and every q (sec. 3).  Independent COMPUTED checks: 19-state cycle enumeration, 203,600 big integers, 40 orbits.
* **Theorem A (one-epoch band restoration; label PAPER PROOF for the reduction, COMPUTED for B_1 = empty: ten SAT instances, UNSAT in
  two independent encodings x two solvers, all four combinations).**  Standard clock for t < 120m and k >= 90m+10
  => the band start strictly increases at every epoch (y_0 < y_1 < ... < y_m), so no m-return, for every m (sec. 4).
* the T12 cone lemma over 120m steps (PAPER PROOF; the exact front recurrence values are COMPUTED by two codes; sec. 2).

**Consequence for certificates.**  A template cycle of this shape (P(q,k) -> P(q,k+5m) for all k >= k_start, or along
one chain k, k+5m, k+10m, ...) does not exist for ANY (q, m, U, J, C): along a chain q is fixed and k -> infinity,
so some link has k >= 90m+10 and is excluded.  This closes the T12 m-period-return mechanism for all time.
**Stronger form (Corollary A3, sec. 4; label PAPER PROOF with COMPUTED input B_1^+(g=45), ten groups in two
encodings).**  Every return Phi^N(P(q,k)) = P(q',k') of the T12 family with exactly N/4 overflows (the standard-clock
class, Lemma K) and k >= 90*ceil(N/120)+10 has N = 120m, q' - q >= 46m/9 and k' - k <= -31m/3: the U band strictly
shrinks (the erosion speed is at least 46 columns per 120 steps, genuine orbits 57-63).  So no chain of standard-clock
returns can stay in the regime k >= 90m+10 forever (in particular none with k -> infinity).

**Still UNDECIDED (sec. 6):** template returns of other shapes, in particular "fast" returns
Phi^N(P(q,k)) = P(q,k+j) with N < 24j (more than N/4 overflows), cross-q cycles P(q,k) -> P(q',k') with q' > q
(q' <= q is excluded for cycles with exactly N/4 overflows, Corollary A2), and single m-returns with k < 90m+10
(irrelevant for certificates).

### 0b. Results and labels
| # | statement | label | where |
|---|---|---|---|
| K | Lemma K: leading+last digit = 10 at steps 0 and N and exactly N/4 digit gains => gains exactly at t = 0 mod 4; always >= N/4 gains | PAPER PROOF + COMPUTED checks (Lean proof not in this commit) | sec. 3 |
| Cone | U-band cones over 120m steps: l_(120j) <= 150j+2, l <= 152 per epoch, r_(120m) <= 120m+2 | PAPER PROOF (T12), values COMPUTED by two codes | sec. 2 |
| Per | every U row has minimal return period 120 under the standard clock | COMPUTED (period_check.py, period2.py; T12 cut.py) | sec. 1 |
| B_1 | one-epoch band restoration: ten group instances UNSAT | COMPUTED (2 encodings x 2 solvers, all combinations) | sec. 4 |
| A | erosion: standard clock + k >= 90m+10 => y_0 < y_1 < ... < y_m | PAPER PROOF (inputs B_1, Cone) | sec. 4 |
| **Main** | **no m-return for any m >= 1, q >= 0, U, J, C, k >= 90m+10** | **PAPER PROOF (inputs K, A)** | sec. 0, 4 |
| A+ | erosion speed: standard clock, k >= 90m+10 => y_(j+1) >= y_j + 46 (g = 45; g = 15 also) | PAPER PROOF (input B_1^+ COMPUTED: ten instances UNSAT, 2 encodings) | sec. 4, 7.3 |
| A3 | every return with exactly N/4 overflows (k >= 90*ceil(N/120)+10) has N = 120m, q'-q >= 46m/9, k' <= k - 31m/3 | PAPER PROOF (inputs K, A+) | sec. 4 |
| D | m = 2, 3 multi-epoch seam sets D_12^(2) = empty, ten m = 3 group instances UNSAT | COMPUTED (2 encodings) | sec. 5.1 |
| E | E_4^(2), E_6^(2) as listed | COMPUTED (2 encodings) | sec. 5.4 |
| W | W_m(q) window instances (implied by K; consistency) | COMPUTED | sec. 7 |
| M | W-band-end advance M(z,R) (mirror of B_1): SAT for deep phase 0, R = 1, 6, 12 (no local obstruction) | COMPUTED | sec. 8 |
| open | fast returns N < 24j; cross-q cycles q' > q; other template shapes | UNDECIDED | sec. 6, 8 |

## 1. Setting (T12 sec. 1-4)

Pair word of an integer with LSD-first digits d_0..d_(L-1): P_i = d_i + d_(L-1-i) (0..18), palindromic.  One step
n -> n + reverse(n) in folded form (index i = 0 outermost): low carries alpha_0 = 0, alpha_(i+1) = [P_i+alpha_i >= 10];
high carries beta_i = [P_i + beta_(i+1) >= 10] (entering from the middle); lo_i = (P_i+alpha_i) mod 10,
hi_i = (P_i+beta_(i+1)) mod 10, overflow gamma = beta_0.  gamma = 0: P'_i = lo_i + hi_i;  gamma = 1: P'_0 = lo_0 + 1,
P'_i = lo_i + hi_(i-1) (i >= 1).  Each overflow adds exactly one digit; no other step changes the length.
Template: P(q,k) = H C rev(H), H = B0 W0^q J U^k, B0 = (10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,
14,8,12,17,10,4,6,4,0,5) (34 letters, ends with 5), W0 = (5,18,4,8,1,15,4,0,5), J0 = 34+9q, y_U = J0+|J| (first U
column), q >= 0, |J| >= 0 arbitrary, C arbitrary (any centre making P(q,k) a valid pair word).
m-return: Phi^(120m)(P(q,k)) = P(q,k+5m).  It has exactly 30m overflows (P(q,k+5m) has 30m more digits).
Standard clock: gamma_t = [t = 0 mod 4].  Under the standard clock the reference exterior rows B_t W_t are
12-periodic with B_t[0] in {10,1,2,5}; every pure U band row U_t has minimal period exactly 120 (period_check.py,
T12 cut.py); every U row has one isolated 9 per 3 letters at every phase.
Letters of the U bands are 9 and even numbers; the odd letters 5 (end of B0, end of W0), 1, 15, 7, 13, 17 are
never band letters ("foreign").

## 2. Cone lemma over 120m steps (T12 sec. 2, 8; cones_m.py; COMPUTED exact recurrences + PAPER PROOF)

If two pair words agree on an interval and have the same clock, the agreement persists on a shrinking interval whose
edges move by the exact front recurrences (a non-9 resets a carry difference, a 9 transmits it).  For a band that is
pure on [a,b) at time s, under the standard clock and with ARBITRARY contents/carries outside, it is pure at time s+t
on [a + l_t, b - r_t), with l_(t+1) = l_t + 1 + [V_t[l_t mod 3] = 9] (junction side) and r_(t+1) = r_t + 1 +
[V_t[(-r_t-1) mod 3] = 9] - gamma_t (centre side).  Exact values (cones_m.py, all 30 U, m = 1..4; independent recomputation fronts2.py with
mindep.py's own background code, r3/fronts2_m4.log, identical; T12 table for m = 1): l over one epoch <= 152 for every rotation and every start phase; l_(120j) = 150j+2 / 150j+1 / 150j for the
three rotations; r_(120j) = 120j+1 / 120j+2 / 120j.  For j >= 2 the per-epoch increments are exactly 150 and 120
because the recurrence depends only on (t mod 120, front mod 3) and 150 = 120 = 0 mod 3 (the epoch state recurs);
so l_(120j) <= 150j+2 and r_t <= r_(120m) <= 120m+2 for all j, m, t <= 120m (r is non-decreasing).

## 3. Lemma K: the clock of every m-return is standard (all m, all q)

**Lemma K.**  Let n_0, ..., n_N be consecutive values of the reverse-and-add orbit, each with >= 2 digits, let
P_0(t) = (leading digit + last digit of n_t) and gamma_t = 1 iff n_(t+1) has more digits than n_t.  If
P_0(0) = P_0(N) = 10 then sum_t gamma_t >= N/4, and if sum_t gamma_t = N/4 then gamma_t = [t = 0 mod 4] for all
t < N (and P_0 runs through 10, 1, 2, 5 periodically).
*Proof (PAPER PROOF).*  (i) Transition.  Let b_t in {0,1} be the carry into the top digit column of n_t+rev(n_t).
The units digit of n_(t+1) is P_0 mod 10 (no carry into the units column); the top column sum is P_0 + b_t.  So
gamma_t = [P_0 + b_t >= 10]; if gamma_t = 0 then P_0 <= 9 and P_0' = P_0 + (P_0 + b_t) = 2P_0 + b_t; if gamma_t = 1
the new leading digit is 1 and P_0' = (P_0 mod 10) + 1.  Explicitly: P <= 8 -> 2P+b (no overflow); 9 -> 18 (b = 0,
no overflow) or 10 (b = 1, overflow); P >= 10 -> P-9 (overflow).  P_0 >= 1 always (leading digit >= 1).
(ii) Potential pi(P) = 3 - floor(log2 P) (pi = 3 for P = 1; 2 for 2,3; 1 for 4..7; 0 for 8..15; -1 for 16..18).
For every transition, 4*gamma - 1 >= pi(P') - pi(P): a non-overflow step doubles (floor(log2(2P+b)) =
floor(log2 P) + 1), equality; overflow 9 -> 10: 0 < 3; overflow P -> P-9, P in 10..15: pi(P-9) - 0 <= 3 with
equality iff P = 10; P in 16..18: pi(P-9) + 1 <= 2 < 3.
(iii) Summing over the segment: sum_t (4 gamma_t - 1) >= pi(P_0(N)) - pi(P_0(0)) = 0, i.e. sum gamma_t >= N/4.  If
equality holds, every step is tight: every overflow is 10 -> 1 and every other step is a doubling P -> 2P+b.  Between
two overflows the value goes from 1 to 10 by doublings; the only such path is 1 -> 2 -> 5 -> 10 (10 = 2*5+0,
5 = 2*2+1, 2 = 2*1+0; 3 leads to 6,7 and then 12..15, never to 10; 9 -> 18 is a dead end since 18 only overflows to
9, not tight).  The segment starts at 10 (tight overflow at t = 0), so it is (10,1,2,5)^(N/4) 10: clock (1000)^(N/4).
QED.
*Application.*  An m-return has P_0 = B0[0] = 10 at t = 0 and t = 120m and exactly 30m = (120m)/4 overflows, so its
clock is standard for all t < 120m, for every m >= 1, every q >= 0 and any U, J, C, k.
*Lean (not in this commit):* Col0Clock.lean (self-contained, core Lean 4.19.0, no Mathlib, no sorry /
native_decide; axioms propext, Classical.choice, Quot.sound; 11 s, 0.5 GB; recompiled by the main session).  It defines
reverse-and-add on Nat from scratch (digit lists, `Genuine.rev`, `Genuine.step`, `Genuine.P0` = leading + last digit,
`Genuine.ovf` = digit-count increment, `Genuine.iter`).  **`Genuine.lemmaK`**: if n has >= 2 digits, P0 n = 10,
P0 (iter N n) = 10 and 4*(len (iter N n) - len n) = N, then for all t < N: ovf (iter t n) = [t = 0 mod 4].
**`Genuine.lemmaK_lower`**: under P0 n = P0 (iter N n) = 10: N <= 4*(len (iter N n) - len n).  Structure: the 19-state
column-0 automaton (`clock_rigid`, `at_least_quarter`: potential, dead set closed under tight steps), the arithmetic
of one step (`col0_arith`), and the connection genuine digits -> automaton (`Genuine.decomp`, `Genuine.one_step`,
`Genuine.orbit_walk`).  Nothing is assumed about reversal: `Genuine.decomp` derives the decomposition from the digit
list.  Applied to a template return: P_0 of the pair word is leading + last digit of the integer, B0[0] = 10.
*Checks (COMPUTED, independent of the proof):* rootcycles.py part 1 (r3/rootcycles_c3.log): the column-0 automaton,
SCC of 10 = {1..18}, all 15 simple cycles: weights >= 0, the only zero-weight cycle is (1,2,5,10); the Bellman-Ford
potential from 10 equals pi; the only cycle of tight edges is (1,2,5,10).  col0check.py (r3/col0check.log): the
transition table agrees with genuine big-integer n + reverse(n) on 203,600 integers (lengths 2..400, all 36 pairs
(P_0,b) hit), the potential inequality holds on all 36 pairs (tight exactly as stated), and a DP over N = 4..2400 finds
exactly one walk 10 -> 10 with N/4 overflows and none with fewer.  PASS.  SAT confirmation by a third code path:
wclock3 with window c = 1 (column 0 alone, free beta_1), T = 240, exactly 60 overflows, some deviation: UNSAT (2 s);
same for c = 2..34.  Orbit-level check col0orbit.py (r3/col0orbit.log): 40 genuine orbits of templates with q = 0..3
(root disturbed after 12q+40 steps), 1500 steps each, all develop a non-standard clock; at all 5313 times with
P_0 = 10 the count is >= N/4, equality (2474 cases) only while the clock is still standard.  PASS.
*Remark.*  Lemma K is a statement about column 0 only (an elementary property of reverse-and-add for arbitrary
integers: between two times with leading + last digit = 10, at least one digit per four steps is gained, with equality
only for the exact four-step rhythm); it supersedes the window instances W_m(q) and the cone
threshold q >= 10m-3 (sec. 5.2, kept as consistency checks).  It does NOT bound the overflow count from above:
"fast" segments (more than N/4 overflows) exist already for column 0 (cycles of weight > 0).

## 4. Theorem A (all m): one-epoch band restoration

**Instance B_1(V,R)** (brestore.py, exact folded law, standard clock gamma_s = [s%4 = 0], s < 120).  Columns
[y-R, y-1) free (one-hot 0..18), column y-1 = v != V[2] ("foreign"), columns [y, inf) = V^inf (V phase 0 at y).  Left
port FREE at y-R: the low carry alpha_(y-R)(s) and, at overflow steps, the high digit hi_(y-R-1)(s) are free at every
step (these are the only couplings to the columns left of y-R).  Right side exact: cone-trimmed region
[y-R, y + l_s + DELTA) (DELTA = 3), band-background constants and the periodic background beta beyond it.  NO
condition on the free part at s = 120.  Condition: at s = 120 the columns [y, inf) are again V^inf (U rows are
120-periodic, so the background at s = 120 is V itself).
**Group form** (triple (P_(y-3),P_(y-2),P_(y-1)) != (V0,V1,V2) instead of the foreign letter): UNSAT implies
B_1(V,R) = B_1(V'',R-1) = B_1(V',R-2) = empty for the three rotations V, V'' = (V2,V0,V1), V' = (V1,V2,V0) of one a:
for a band of rotation V, V'', V' starting at y* with a foreign letter at y*-1, put the instance's y at y*, y*+1,
y*+2; the triple then differs in its last, middle or first letter, and "band correct on [y*,inf)" implies the
instance's "band correct on [y,inf)".  Increasing R is a restriction (the extra columns generate one choice of the
free port), so UNSAT at R implies UNSAT at every R' >= R.
**Computed (B_1 = empty).**  Group instances U2 R3 (a=0), U5 R3 (2), U6 R12 (4), U9 R3 (6), U12 R3 (8), U15 R3 (10),
U18 R3 (12), U21 R12 (14), U26 R3 (16), U27 R3 (18): all UNSAT with
 - brestore + kissat404 (35-57 s, <= 1.4 GB; 0.38M vars / 4.8M clauses for U2),
 - brestore + cadical195 (53-115 s),
 - mbres.py + kissat404 (independent enc2 of mindep.py: rectangle window [y-R, y+171), direct one-hot successor and
   carry relations, no digit variables, no trimming; 46-56 s),
 - mbres.py + cadical195 (r12f3: all ten UNSAT, 32-39 s, <= 6.6 GB; r3/mbres_group_*),
 - robustness of the cone trimming: brestore --delta 6 (three more variable columns beyond the front) U2 R3, U6 R12,
   U21 R12 UNSAT (r3/brestore_group_*_delta6_*).
Controls: nofor U0 SAT (pure band restores itself), full U2 UNSAT and full U3 SAT (= depth-3 rigidity uleft m=1 of
r12a, in both encodings), defect U5 R1 full = {6,7,15,16} (= D_1(U5) of r12a).  Both encodings' building blocks are
validated against genuine big-integer orbits (mdefect validate/cvalidate m = 1,2,3; mindep genuine/cgenuine).
Erosion controls on genuine big-integer orbits: erosion_check.py (r12f2) 600 orbits (30 U x 20 random J, q = 20),
band start moves right by 57-63 columns in one epoch; erosion3.py (r12f3, r3/erosion3.log) 180 orbits (30 U x 6 J,
|J| = 0..30, q = 30, K = 400) over three epochs: the band start moves right in EVERY epoch (57-63, then exactly 60
per epoch), 540 epochs, 0 violations.

**Theorem A (band erosion, every m).**  Let m >= 1, k >= 90m+10, q >= 0, any U, J, C, and suppose the orbit of P(q,k)
has the standard clock for t < 120m (no return is assumed).  Let P_t = pair word at time t, Xi_j = y_U + 3k - r_(120j)
and y_j = min{ y : P_(120j)(i) = U_0[(i-y_U) mod 3] for all i in [y, Xi_j) } (start of the maximal band-correct run
ending at the protected zone; j = 0..m).  Then y_0 < y_1 < ... < y_m; in particular y_m >= y_0 + m.
*Proof (PAPER PROOF).*
(a) Cone lemma from t = 0 (band [y_U, y_U+3k) pure, arbitrary context on both sides): for every t <= 120m the band
is background on [y_U + l_t, y_U + 3k - r_t); the background at t = 120j is U_0 (period 120).
(b) By (a) (the interval [y_U + l_(120j), Xi_j) is non-empty by the inequality in (d)), y_j <= y_U + l_(120j)
<= y_U + 150j + 2.  At t = 0 the letter at column J0-1 is the last letter of B0 W0^q, namely 5, never a band letter,
so y_0 >= J0 >= 34 > 12 >= R for every R used.
(c) Induction on j < m: suppose y_j >= 34.  Put y* = y_j, V = rotation of U_0 with phase 0 at y*.  At t = 120 j column
y*-1 is not the band letter (minimality) and [y*, Xi_j) is pure.
(d) Epoch j (t = 120 j + s, s <= 120; standard clock [s%4 = 0] since 120 j = 0 mod 4).  Cone lemma from 120 j:
background on [y* + l^V_s, y_U + 3k - r_(120 j + s)).  The trimmed instance needs DELTA+5 = 8 background columns at its
right edge (isolated 9s), mbres needs [y*, y*+173): y* + l^V_s + 8 <= y_U + 150(m-1) + 2 + 152 + 8 = y_U + 150m + 12
and y* + 173 <= y_U + 150m + 25, while y_U + 3k - r_(120m) >= y_U + 270m + 30 - 120m - 2 = y_U + 150m + 28.  So the
genuine columns [y*-R, ...) during epoch j form a solution of B_1(V,R) (free port = genuine alpha_(y*-R)(t) and
hi_(y*-R-1)(t); free columns = genuine values), except possibly for the final condition.
(e) If y_(j+1) <= y*, then [y*, Xi_(j+1)) is pure at t = 120(j+1); this contains the instance's final window
[y*, y* + l^V_120 + DELTA) (and [y*, y*+171)), since y* + 171 <= y_U + 150m + 23 < Xi_(j+1).  So the final condition
holds: contradiction with B_1 = empty (group instance of the a of U).  Hence y_(j+1) > y_j >= 34.  QED.
(Only the seam side is used; no centre lemma, no condition on q or |J|.  The clock enters through the forced clock of
the instance and through the cone lemma in (a), (d).  Equivalently, in r12f2's form: take j with y_j maximal.)

**Corollary A1 (no m-return).**  In an m-return (standard clock by Lemma K), the target has the same seam side
B0 W0^q J U^(k+5m) at the same columns, so P_(120m) = P_0 on [0, y_U+3k) and, as Xi_m <= Xi_0, y_m = y_0:
contradiction with Theorem A.
**Corollary A2 (returns with q' != q; PAPER PROOF).**  If Phi^(120m)(P(q,k)) = P(q',k') for some q', k' (same U, J, C)
with exactly 30m overflows (i.e. 18(q'-q) + 6(k'-k) = 30m) and k >= 90m+10, then by Lemma K the clock is standard, the
target band phase agrees with the protected zone (9(q'-q) = 0 mod 3), the band-correct suffix of J is the same in
source and target (the letter before J is 5 in both), hence y_m - y_0 = 9(q'-q), and Theorem A gives q' - q >= m/9.
So every cycle P(q,k) -> P(q',k') with q' <= q and exactly N/4 overflows is excluded.  (Corollary A3 below sharpens
this with the erosion speed: also q' > q is restricted, and the band must shrink.)

**Theorem A+ (erosion speed; label PAPER PROOF, input COMPUTED).**  Let g >= 0 and suppose the ten group instances
B_1^+(V,R,g) (brestg.py / mbresg.py = B_1 group instance with the final condition only on [y+g, inf)) are UNSAT.  Then
under the standard clock and k >= 90m+10, y_(j+1) >= y_j + g + 1 for j = 0..m-1.  Proof: Theorem A with the final window
[ŷ+g, ŷ+l^V_120+DELTA), where ŷ in {y*, y*+1, y*+2} is the position at which the group rotation has phase 0: if
y_(j+1) <= y* + g then the band is correct on [y*+g, Xi_(j+1)), which contains the final window since ŷ >= y* and
b_T <= Xi_(j+1); this contradicts UNSAT.  QED.
*Computed:* g = 15 and g = 45: all ten group instances UNSAT with brestg+kissat404 and with the independent encoding
mbresg+kissat404 (sec. 7.3); g = 30 UNSAT (brestg).  g = 56: the a = 0 group U2 is SAT (419 s), so 45 < g*(a = 0) <= 55:
adversarial left contexts can slow the erosion below the 57-63 seen in genuine orbits.  So every standard-clock epoch
moves the band start right by at least 46 columns.  Controls: g = 0 reproduces B_1 (same clause count, UNSAT); final
window empty (g = 170): SAT; nofor (pure band): SAT.

**Corollary A3 (standard-clock returns of the T12 family; PAPER PROOF).**  If Phi^N(P(q,k)) = P(q',k') (same U, J, C)
with exactly N/4 overflows and k >= 90*ceil(N/120)+10, then N = 120m and q' - q >= 46m/9 and k' - k = 5m - 3(q'-q)
<= -31m/3 < 0.  Proof: Lemma K gives the standard clock (P_0 = 10 at both ends, N/4 overflows); the protected band zone
at time N carries U_N and, by the target, U_0 at phases agreeing mod 3 (9(q'-q) = 0 mod 3), so 120 | N (N = 0 mod 4,
minimal period 120); Corollary A2's computation gives y_m - y_0 = 9(q'-q); Theorem A+ with g = 45 gives y_m - y_0 >= 46m;
finally 9(q'-q) + 3(k'-k) = 15m (digit count).  QED.  (General g: k'-k <= m(14-g)/3; g = 15 already gives k' < k.)
Consequences: (i) q' = q (m-returns) and q' < q are impossible;
(ii) in the regime k >= 90m+10 every standard-clock return strictly shortens the U band (k' <= k - 31m/3), so no chain of
standard-clock returns stays in that regime forever: there is no certificate of template type P(q,k) -> P(q',k') with
exactly N/4 overflows and k -> infinity or k bounded >= 90m+10.  (Not covered: chains whose k stays below 90m+10, where
the cones may meet and the band need not be protected.)

**Main Theorem** = Lemma K (standard clock in every m-return) + Theorem A / Corollary A1.  Label: PAPER PROOF, with COMPUTED inputs (B_1, cone values).

## 5. Supporting and superseded results (consistency checks)

### 5.1 Multi-epoch seam theorems for m = 2, 3 (r12f; logically different instance families)
D_R^(m)(V) (mdefect.py / mindep.py defect): free [y-R, y-1), foreign y-1, V band from y, free left port, every column
of the region returns after 120m steps.  Seam lemma (Appendix S below): if for each rotation V some
D_R^(m)(V) = empty, no m-return with the standard clock and k >= 90m+10 (applied at the template's own band start).
m = 2: D_12^(2)(V) = empty for all 30 V (mdefect+kissat, mindep+kissat; cadical spot checks U0, U14, U26).
m = 3: ten group instances (uleft R3; R12 for a = 4, 14) UNSAT (mdefect+kissat, mindep+kissat; cadical spot check U5);
D_12^(3)(U0), D_12^(3)(U1) empty directly.  With Lemma K these hold for every q >= 0.  So for m = 2, 3 the exclusion
has two independent proofs (B_1 one-epoch, D/uleft multi-epoch), each with two encodings.
### 5.2 Clock: window instances and exterior cone (superseded by Lemma K)
- Exterior cone (clockq.py, clockq2.py; PAPER PROOF from COMPUTED recurrences): with an arbitrary inlet at J0 the clock
  is forced exactly for t < 12q+40, i.e. for all t < 120m iff q >= 10m-3 (retreat 91, then exactly 90 per epoch;
  one-epoch threshold l* = 96).
- Clock-rigidity window instances W_m(q) (wclock.py; window [0, 34+9q), free inlet, computed clock, return at 120m,
  30m overflows, some deviation): UNSAT for the cases in sec. 7.1, consistent with Lemma K (which implies them).
### 5.3 Pumping (r12f Task 2, PAPER PROOF; numeric control pump_m.py COMPUTED): Return_m(q,k) <=> Return_m(10m+4, 90m+10)
for q >= 10m+4, k >= 90m+10.  Not needed any more.
### 5.4 Centre side (second, incomplete route; not needed): E_4^(2) for 26 V, E_6^(2) for U5, U8, U23, U26 empty
(mdefect+kissat; U0 cadical; r12f3: all 31 instances also with mindep cdefect + kissat404, identical results, positive
control E_4^(2)(U5) = {3,12} in both encodings); centre base case for m >= 2 (mcentre.py) not run.

## 6. Scope, gaps and adversarial review

**Exactly what is proved.**  For each (m, q, U, J, C) and each k >= 90m+10: no m-return.  No assumption on q (q >= 0)
or on |J|; the centre C is arbitrary.
**Hypotheses and where they are discharged.**  (H1) standard clock for t < 120m: Lemma K (needs only P_0 = 10 at both
ends, true for every template since B0[0] = 10, and the overflow count 30m, true for every m-return).  (H2) the U-band
cones of every epoch stay apart: k >= 90m+10, inequality (d) of sec. 4, uses l_(120j) <= 150j+2, l <= 152 per
epoch, r_(120m) <= 120m+2 (sec. 2, valid for all m by the periodic-recurrence argument).  (H3) B_1 = empty: ten
group instances, two encodings x two solvers.  (H4) instance soundness: free left port = the only couplings to the
left (alpha bit + overflow-step high digit); trimmed right side needs 8 background columns, supplied by (H2); the
background at the end of an epoch is V because U rows are 120-periodic; 120 j = 0 mod 4 aligns the forced clock;
y* = y_j >= y_0 >= 34 > R at every epoch (induction, y_j strictly increases).
**Role of k0(m) = 90m+10.**  Only separation: it keeps the junction-side cones (from y_U and, inside each epoch, from
y_j) and the centre-side cone r apart for all 120m steps (inequalities (d), (e) of sec. 4).  It equals r12f's pumping
threshold (not needed any more).  No centre lemma is used; the centre word C enters only through the arbitrary carries
at the right end of the protected zone (the E^(2) sets of sec. 5.4 are a second, incomplete route and not needed).
**What happens below the thresholds.**  k < 90m+10: a single m-return is not excluded (the cones may meet; the seam
side is then not a semi-infinite seam word).  This is irrelevant for certificates (k -> infinity along a chain).
There is no q threshold left (q < 14 and 14 <= q < 10m-3 are covered by Lemma K).
**Certificate-chain point.**  In a chain P(q,k) -> P(q,k+5m) -> P(q,k+10m) -> ... the counter k grows without bound
and q is fixed.  The theorem excludes every link with k >= 90m+10 for every q >= 0, so no such chain is infinite:
covered for ALL q (the earlier gap q < 14 is closed by Lemma K, which needs no exterior length).  This uses a fixed
period m along the chain (a finite certificate has a fixed cycle).  A chain with periods m_i growing so fast that
k_i < 90 m_i + 10 at every link is not excluded by the theorem (and is not a finite certificate).
**Review log (r12f3).**  Re-read line by line: brestore.py (build, group constraint, final window), mdefect.step and
band_bg/fronts (left free port, right exact port, overflow-step coupling), mbres.py + mindep.build (rectangle, right
port bits, H digit), wclock.py, mwclock.py; re-derived the separation inequalities and the group-rotation case split
by hand; independently recomputed the cone radii (fronts2.py), the U period (period2.py) and the column-0 facts
(rootcycles.py, col0check.py, col0orbit.py, Lean).  Found no error in r12f/r12f2's B_1 and seam work; the only
corrections are of scope (the q thresholds were unnecessary) and the proof is restated in the stronger erosion form.
**NOT covered (UNDECIDED).**
1. "Fast" template returns Phi^N(P(q,k)) = P(q,k+j) with N < 24j.  (A template return has exactly 6j overflows and,
   by Lemma K, at least N/4, so N <= 24j.  N = 24j forces the standard clock; then, for k >= 90*ceil(N/120)+10, the
   protected band region at time N must carry both U_N and U_0, so 120 | N (minimal period 120) and j = 5m: an
   m-return, excluded.)  Fast returns need a non-standard clock; they are impossible when the exterior cone forces the clock for
   t < N, i.e. for N <= 12q+40, but open for N > 12q+40.  Theorem A's instance uses the standard clock; r12f2's
   free-clock relaxation (bfree.py) shows that with an adversarial root-realizable clock a foreign letter CAN sit in
   front of a band without eroding it (SAT), so B_1 does not extend to fast clocks as it stands.
2. Cross-q cycles with q' > q (Corollary A2 excludes q' <= q when the cycle has exactly N/4 overflows; for q' > q the
   erosion is consistent with y_m - y_0 = 9(q'-q) >= m, "travelling junction"; genuine orbits show a front speed of
   60 columns per epoch but a chaotic, non-periodic wake behind it, wake.py, r3/wake.log), cycles through other
   template shapes, other roots than B0.
3. Single m-returns with k < 90m+10 (finitely many k per m; no certificate can consist of them).
4. Lemma K has a Lean proof outside this commit (PAPER PROOF here).  B_1 = empty rests on SAT solvers (two encodings, two solvers; no
   DRAT proofs kept).  The cone radii rest on two independent codes.  Theorem A's reduction and the Main Theorem's
   composition are PAPER PROOF (not formalised).

## 7. Computation tables

### 7.1 Window instances W (window [0,c), c = 34+9q unless stated; T = 120m; count 30m)
| instance | encoding + solver | result | time, RSS |
|---|---|---|---|
| W_2(14) | wclock+kissat404 / wclock+cadical195 / mwclock(enc2)+kissat404 | UNSAT x3 | 29 s / 22 s / 173 s, 15.3 GB |
| W_2(15), W_2(16), W_2(13), W_2(10), W_2(7), W_2(4), W_2(0) | wclock+kissat404 | UNSAT | 14-30 s |
| W_3(14) | wclock+kissat404 / wclock+cadical195 / mwclock+kissat404 | UNSAT x3 | 101 s / 121 s / 326 s, 14.3 GB |
| W_3(q), q = 15..26 | wclock+kissat404 | UNSAT | 33-106 s |
| W_4(14), W_5(14), W_6(14) | mwclock(enc2)+kissat404 | UNSAT | 644 s, 783 s, 1182 s (<= 24.4 GB) |
| W_4(14), W_5(14), W_6(14), W_7(14), W_8(14) | wclock+kissat404 | UNSAT | 240 s, 271 s, 514 s, 1471 s, 2403 s (<= 12.6 GB) |
| window c = 34, 20, 12, 8, 6, 5, 4, 3, 2, 1 (prefixes of B0), T = 240, count 60 | wclock3+kissat404 | UNSAT | 2-23 s |
| window c = 8, 6, 5, 4, 3, 2, 1, T = 240, NO count | wclock3+kissat404 | SAT (fast clocks, e.g. c = 8: 92 overflows) | 0-935 s |
| refcheck q14 m2, m4, m8; c34 T240 (inlet = reference carries) | wclock / wclock3 + kissat404 | SAT, standard clock | 2-30 s |
All rows above finished (no job left running at the end of the run).
All rows of 7.1 are implied by Lemma K; they are kept as independent consistency checks.
### 7.3 Quantitative erosion B_1^+(V,R,g) (final condition on [y+g, inf); ten groups U2 R3 | U5 R3 | U6 R12 | U9 R3 | U12 R3 | U15 R3 | U18 R3 | U21 R12 | U26 R3 | U27 R3)
| g | encoding + solver | result | time |
|---|---|---|---|
| 0 | brestg = brestore group (kissat404, same clause counts) | UNSAT (U2 R3 checked) | 37 s |
| 15 | brestg + kissat404 | 10/10 UNSAT | 34-60 s |
| 15 | mbresg (independent enc2) + kissat404 | 10/10 UNSAT | 43-58 s |
| 15 | brestg + cadical195 | 10/10 UNSAT | 67-104 s |
| 30 | brestg + kissat404 | 10/10 UNSAT | 40-57 s |
| 45 | brestg + kissat404 | 10/10 UNSAT | 49-170 s |
| 45 | mbresg (independent enc2) + kissat404 | 10/10 UNSAT | 48-93 s |
| 56 | brestg + kissat404 | U2 R3: SAT (419 s); others killed (not needed) | |
| 170 | brestg + kissat404 (final window empty; control) | SAT | 2 s |
| nofor g = 15, U0 R3 | brestg + kissat404 (control) | SAT | 41 s |
Interpretation: UNSAT at g means every standard-clock epoch moves the band start right by >= g+1 columns (for all
left contexts).  g = 45: >= 46 columns per epoch.  Genuine orbits (erosion_check.py, erosion3.py): 57-63 in the first epoch, exactly 60
afterwards.

### 7.4 Travelling-junction search TW (twjunction.py; standard clock; consistency check of Corollary A3)
| instance | solver | result | time, RSS |
|---|---|---|---|
| TW(U, m = 1, a = 1, LJ = 30), all 30 U (covers every junction of length <= 30, every band phase) | kissat404 | 30/30 UNSAT | 125-240 s, <= 2.3 GB |
| a = 0 control (frozen junction, U2) | kissat404 | UNSAT (= Theorem A) | 139 s |
| validate U2 LJ 30 seeds 1, 2 (genuine big-integer orbit: genuine target SAT, changed column UNSAT), nofinal control SAT | kissat404 | PASS | |
(Implied by Corollary A3: a junction moving 9a columns per epoch contradicts the erosion speed >= 46 unless 9a >= 46m,
and then 3a > 5m: the band would shrink.  The direct search confirms it in the sample m = 1, a = 1.)

### 7.2 B_1, D, uleft, E: sec. 4, 5 and Appendix S (cross-check tally at hand-over).

## 8. Fast returns (exploratory, r12f3)

rootcycles.py part 2: in G_c x Z_4 (window [0,c), free inlet, phase t mod 4) the strongly connected component of
(B0[0,c), 0) contains non-standard edges for c = 1, 2, 3 (47, 816, 11125 edges): short root windows can return with a
faster clock (c = 4, 5: the whole forward-reachable set, 191,920 / 1,989,884 product states, is one SCC with
127,650 / 1,327,338 non-standard edges).  SAT without the count condition (wclock3 --nocount, T = 240): c = 1..6 SAT
within 104 s; c = 8 (prefix of B0) is SAT (935 s):
the window returns to B0[0,8) after 240 steps with 92 overflows (instead of 60), clock standard up to t = 60, then
fast.  So the first 8 root columns do not forbid fast returns.  (c = 34: no answer after 75 min, killed at 07:32;
c = 20, 12: killed after 8 min.)
A fast return of a full template would in addition need the exterior W band, J and the U band junction to return
under a fast clock; B_1 does not apply (free-clock relaxation SAT, r12f2 bfree.py).  UNDECIDED.
Cross-q gap (q' > q, standard clock): the natural local obstruction, "the reference-correct exterior prefix cannot
advance by one column during one epoch" (wadvance.py, instance M(z,R): [z-L,z) reference W rows, foreign letter at z,
free columns (z,z+R), free inlet at z+R, standard clock, T = 120; condition: [z-L,z] reference at t = 120), is FALSE:
M is SAT for deep-W phase 0 with R = 1, 6, 12 (T = 120; also T = 12, 24, 60 with R = 1) (r3/wadv_*).  So a suitable
right context can repair the W-band end (R = 24 killed unfinished at 07:32).  The cross-q gap is instead closed in the
standard-clock class by the erosion-speed Theorem A+/Corollary A3 (sec. 4).

## 8b. Reproduction (from this directory, PY = python3 with python-sat (kissat404, cadical195))
- Lemma K: $PY rootcycles.py 3; $PY col0check.py; $PY col0orbit.py; SAT check $PY wclock3.py rigid --c 1 --T 240 (UNSAT).
- B_1 (ten group instances, (U,R) in {(2,3),(5,3),(6,12),(9,3),(12,3),(15,3),(18,3),(21,12),(26,3),(27,3)}):
  $PY brestore.py group --U u --r R --n 1 --solver kissat404|cadical195   and
  $PY mbres.py group --V u --R R --m 1 --solver kissat404|cadical195   -> RESULT ... EMPTY.
  Controls: brestore.py group --U 0 --r 3 --n 1 --nofor (SAT); --full U2 (UNSAT), U3 (SAT); defect --U 5 --r 1 --full.
- Cone radii: $PY cones_m.py (logs/cones_m.log); $PY fronts2.py --m 4 (r3/fronts2_m4.log).  U period 120:
  $PY period_check.py (logs/period_check.log), also T12 cut.py / verify.cpp in the repository.
- Genuine-orbit controls: $PY erosion_check.py; $PY erosion3.py.

## 8c. Natural next steps (NOT done here)
(a) Fast returns: an upper bound on the overflow rate of a returning exterior window, or an erosion theorem valid for
    non-standard clocks (B_1 with a free clock is SAT, so the clock must be coupled to the root/exterior dynamics).
(b) Standard-clock returns with k < 90m+10 (band shorter than the cones): not covered by A+/A3.
    (Travelling junctions with sustained band growth, 3a <= 5m, are already excluded by Corollary A3; the direct SAT
    search twjunction.py, m = 1, a = 1, |J| <= 30, all 30 U, gave 30/30 UNSAT, sec. 7.4.)

## 9. Files (this directory)
Sources: rootcycles.py, col0check.py, col0orbit.py (Lemma K checks), fronts2.py, period2.py (cone radii, U period: second codes),
brestore.py (B_1, mdefect encoding), mbres.py (B_1, enc2), brestg.py, mbresg.py (B_1^+(g)), mdefect.py, mindep.py
(D/uleft/E instances), wclock.py, mwclock.py, wclock3.py (window instances), wadvance.py (instance M), twjunction.py
(travelling junction), erosion_check.py, erosion3.py, wake.py (genuine-orbit controls), clockq.py, clockq2.py, clockscc.py,
gapk.py, cones_m.py, period_check.py, pump_m.py, plant.py, mcentre.py, bfree.py, bfree_val.py, mbfree.py; unchanged copies
of `../../round11/t12_seam/seamsat.py`, `seam_check.py` (imported by cones_m.py, clockq*.py).  Drivers: r3sched.sh + r3run.sh
(queue r3queue.txt), brun.sh/bpool.sh, mbrun.sh/mbpool.sh, bfrun.sh/bfpool.sh, bgrun.sh/bgpool.sh, wrun.sh/wpool.sh,
sched.sh/run1.sh/pool.sh (queue.txt), val_seq.sh, watchdog.sh (written for ~/p196_run/r12f on the Studio).
Logs: logs/*.log, r3/ (key logs plain: rootcycles_c3, col0check, col0orbit, erosion3, fronts2_m4, period2, wake; pool.log
and sched.log list every run with its RESULT line), bres/pool.log, val/val.log; logs/main_check/ (main-session check:
README.txt, bcheck.py = third encoding of B_1).  All per-instance logs of bres/, r3/, m2/, m3/, val/ and
logs/main_check/logs/ are in logs.tar.gz (`tar xzf logs.tar.gz` restores them in place).

## Appendix S. Multi-epoch seam lemma and cross-check tally (copied from the r12f working notes; "r12a" = ../t12_m1/FINAL.md)

### Seam lemma for m epochs (PAPER PROOF; inputs: cone lemma over 120m steps, pumping, separation)
If for each rotation V of (9,a,18-a) some D_R^(m)(V) (1 <= R <= 200) is empty, then for every rotation U of a and every
finite J the seam of P(q,k) does not return after 120m steps (q >= q0(m), k >= k0(m)), so no m-return witness with that U.
Proof: as r12a sec. 2.3.  In a witness every column of [0, J0+|J|+3k) returns (source and target P(q,k+5m) agree there).
y* = minimal start of a V-periodic factor ending at J0+|J|+3k; W0 ends with 5 (not a letter of any (9,a,18-a), a even),
so y* >= J0 >= 34+9*q0 > 200 >= R and the letter at y*-1 is not V[2].  The band [y*, J0+|J|+3k) is pure at t=0; by
the cone lemma (fronts l_t <= 150m+2, r_t <= 120m+2) and separation (>= 26 protected columns) the columns
[y*+l_t, y*+l_t+DELTA+5) are background at every t <= 120m, which is all the trimmed instance uses on its right side
(constant pair values and the background beta at the region edge; one non-9 suffices, U3 rows have exactly one
isolated 9).  The genuine left context is one choice of the free port.  So the genuine window satisfies the
D_R^(m)(V) instance and its letter at y*-1 lies in D_R^(m)(V) = empty.  Contradiction.

### Cross-check tally at hand-over (all from m2/pool.log, m3/pool.log, val/pool.log; every line re-read)
| family | encoding + solver | instances | result |
|---|---|---|---|
| D_12^(2)(V), all 30 V | mdefect (cone-trimmed) + kissat404 | 30 | 30 EMPTY (248-724 s, <= 5.1 GB) |
| D_12^(2)(V), all 30 V | mindep (enc2, rectangle M=321) + kissat404 | 30 | 30 EMPTY (258-577 s, <= 14 GB) |
| D_12^(2) cadical spot checks U0, U14, U26 | mdefect + cadical195 | 3 | 3 EMPTY (648-903 s, <= 12.3 GB) |
| m=2 group instances uleft (U2,U5,U9,U12,U15,U18,U26,U27 R3; U6,U21 R12) | mindep + kissat404 | 10 | 10 UNSAT (274-439 s) |
| m=3 group instances, same ten | mdefect + kissat404 | 10 | 10 UNSAT (1089-1392 s, <= 8.3 GB) |
| m=3 group instances, same ten | mindep (rectangle M=471) + kissat404 | 10 | 10 UNSAT (845-1159 s, <= 14.5 GB) |
| m=3 cadical spot check uleft U5 R3 | mdefect + cadical195 | 1 | UNSAT (2175 s, 25.3 GB) |
| D_12^(3)(U0), D_12^(3)(U1) | mdefect + kissat404 | 2 | EMPTY (2972 s, 1604 s) |
| D_12^(3)(U1) | mindep + kissat404 | 1 | EMPTY (865 s, 12.6 GB) |
| E_4^(2) (26 V), E_6^(2) (U5,U8,U23,U26) | mdefect + kissat404 (U0: cadical195) | 30 | 30 EMPTY |
| positive controls m=2 | mdefect | 3 | D_1^(2)(U5)={6,7,15,16} (cadical), E_4^(2)(U5)={3,12} (cadical) |
| m=1 consistency | md/mi uleft U2 R3, U3 R3, U6 R12 | 6 | UNSAT, SAT, UNSAT (= r12a) in both encodings |
=> the m=2 seam theorem rests on two encodings x two instance families (single D_12^(2) and group uleft), the m=3
   seam theorem on two encodings (group uleft x10 each).  No cross-check of the seam theorems is missing.
   Missing (not needed for the seam theorems): second encoding of the E^(2) sets (mindep cdefect), any E^(3) set, and
   the centre base case for m >= 2.
