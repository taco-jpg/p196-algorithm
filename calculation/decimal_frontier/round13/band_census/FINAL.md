# Report of agent r13a (round 13, 2026-11-08), as delivered; paths shortened. Per-job logs are in logs.tar.gz (logs/<tag>/i*.log); job lists in jobs/. The independent main-session checks are in main_check/.

**Packaging corrections (checked against the logs, 2026-11-10).** (1) U3 at epoch T' = 40: `logs/u3rot/u3rot.log` shows 27 of the 30 words (tau = 0..32) UNSAT in three solver/encoding pairs; the three words at tau = 36 have two pairs each (kissat404/enc2 errored on rotation 0, cadical195/enc1 is absent for rotations 1, 2). All 30 are UNSAT in at least two pairs. (2) Census cross-check by SAT enumeration: four cases are logged as CROSS PASS (`logs/xcensus2.log`, `logs/xcensus3.log`): (p11,4,22), (1000,4,32), (10,4,16), (p11,3,33); the (1000,3,120) match mentioned below is not in a shipped log. (3) NOTES.md (agent log) is not shipped.

# r13a FINAL — band census and one-epoch left/right restoration test (first draft 10:50 UTC, updated continuously)

Agent r13a, 2026-11-08 (work dir ~/p196_run/r13a on the Studio; log NOTES.md).  Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF /
UNDECIDED.  Nothing here is a statement about 196.  No Lychrel number and no certificate is found or claimed.

## 0. Status
Census complete for all three clocks up to s = 8; controls complete; L/R test results, variants and real-thing attempts are summarised in sec. 0b (hand-written summary, machine tally and explicit lists below); tables in sec. 7 (machine generated).

## 1. Definitions and instance statements

Folded law (r12f sec. 1).  Row P (letters 0..2b-2, column c increasing towards the middle).  alpha_(c+1) = [P_c + alpha_c >= b],
beta_c = [P_c + beta_(c+1) >= b], lo_c = (P_c+alpha_c) mod b, hi_c = (P_c+beta_(c+1)) mod b; next row P'_c = lo_c + hi_c if the
step has no overflow (gamma = 0), P'_c = lo_c + hi_(c-1) if gamma = 1.  Periodic row map R_g for a word V in {0..2b-2}^s with at
least one letter != b-1: V -> V' with the periodic carries (uniquely determined because of the non-(b-1) letter).

**Band** for a clock g of period p: a word V, with a period T (p | T) such that V_0 = V, V_(t+1) = R_(g_t)(V_t) and V_T = V, and
every V_t has a letter != b-1.  Twist: minimal T_rot | T with V_(T_rot) = a rotation of V (twist r: V_(T_rot) = shift^r V).
Bands are enumerated as cycles of F = R_(g_(p-1)) o ... o R_(g_0) on cyclic words of length s (phase-0 rows), up to rotation
(bandcensus.cpp: bitset of all (2b-1)^s words, A <- F(A) until stable; F is then a bijection on A).  Only primitive words are
listed for each s (a band with spatial period d | s, d < s, appears under s = d).

**Fronts (general band).**  For a band row V_t in phase 0 at column y (arbitrary context left of y, pure band to the right):
l_0 = 0, l_(t+1) = l_t + 1 + (length of the run of (b-1) in V_t starting at column l_t) (letters right of y + l_t are pure at time t).
Right end (pure on (-inf, z), arbitrary context right of z): r_0 = 0, r_(t+1) = r_t + 1 - g_t + (length of the run of (b-1) in
V_t ending at column z-1-r_t).  (Both reduce to the T12 recurrences when the 9s are isolated; validated on genuine orbits, see 4.)

**Test L (left restoration; instance L(V,W,tau,R,M)).**  W is a rotation of V_tau (origin tau, default 0), phase 0 at y.  Columns
[y-R, y-1) free, column y-1 foreign (letter != W[s-1]), columns [y, inf) band W^inf (rows V_(tau+t) rotated); left port free
(alpha_(y-R)(t) for all t and hi_(y-R-1)(t) at overflow steps); right side exact background: the window is cone-trimmed
[y-R, y + l_t + Delta) with Delta = s+3 (rows beyond are background constants) (or a rectangle wider than the maximal front, enc2);
clock = forced g_(tau+t); horizon T' = M T (M = number of epochs).  Final condition: the band is correct on [y, inf) at time T'.
UNSAT for all rotations W of V_tau: the band cannot be stationary (Theorem GA below).

**Test R (right end; instance R(V,W,M,R_f)).**  W rotation of V_tau, phase 0 at z.  Band on (-inf, z) (exact left background: left window
edge beyond the right front r_T' + Delta, alpha and overflow-step hi of the column left of the window = background constants),
column z foreign (letter != W[0]), columns (z, z+R_f) free (one-hot), right port beta_(z+R_f)(t) free for all t.  Epochs M minimal such that S'
= overflows in T' = M T is even and delta = S'/2 = 0 mod s.  Final condition at time T': the band is correct on (-inf, z+delta).
Right port: the ONLY input from the right of the window into columns < z+R_f is the high carry beta_(z+R_f)(t), one bit per step.  (Column c
at time t+1 needs lo_c, hi_c or hi_(c-1); hi_x needs beta_(x+1), so the right boundary needs only beta_x1; the low carries come from
the left; the fold/centre enters only through beta_x1.)  Validated on genuine orbits: with the genuine bit beta_x1(t) = alpha_(L-x1)(t) of the full addition the
encoding reproduces every letter of the genuine orbit (bandval.py).  A free bit is a superset of every genuine context (the window stays left of the middle
column at all times: the middle only moves right).

**Variants used (all are additional necessary conditions; UNSAT for all rotations at any one (variant, origin) excludes stationary left junctions by the theorems below; SAT means nothing more than no obstruction).**
- L (one epoch): T' = T (tau = 0).  Lr = "rotating epoch": T' = T_rot (or M T_rot) with final condition "band correct at time T'" (rows V_(T') are a rotation of V_tau).  L* (multi-epoch): T' = M T with the band also correct at all intermediate marks (every T_rot resp. T; bandrun --markevery).  LD (D-type, --ret): L plus "the free columns [y-R, y) return exactly at time T'" (an exact-period junction of period dividing T' in the free-port relaxation).  tau-scan: the same tests at other origins tau (rows V_tau): UNSAT at a single origin for all rotations suffices.  R: as above; R*: comoving return of the free cells (Theorem GR*).

## 2. The generalised erosion theorem

**Theorem GA (generalised erosion; label PAPER PROOF, input COMPUTED: the listed UNSAT instances).**
Let b >= 2, g a periodic clock, V a band with rows V_t and period T (p | T), T_rot the minimal time multiple of p with V_(T_rot) a rotation of V, T' a multiple of T_rot (T' = M T or M T_rot), tau an origin (row V_tau, clock phase tau mod p), R >= 1.
Suppose L(V,W,tau,R,M) is UNSAT for EVERY rotation W of V_tau.  Let P_t be the pair words of any genuine orbit such that
(H1) the overflow clock satisfies gamma_(tau+u) = g_(tau+u) for 0 <= u < nT' (n epochs) [for a template return with a fixed exterior, Lemma-K type arguments or the exterior cone give this];
(H2) at time tau the band is present: P_tau(c) = V_tau-periodic extension on a maximal run [y_0, e), with y_0 >= R+1 (there are columns y_0-R-1 >= 0 left of the free window) ;
(H3) separation: e - y_0 >= n(L + R') + 2 Delta + 3s + 8, where L = maximal one-epoch left-front radius over all rotations of V_tau at origin tau over T' steps
(= max_W l^W_(T')), R' = maximal one-epoch right-front radius over T' (l, r are the recurrences of sec. 1), Delta = s + 3.
Let y_j (j = 0..n) be the start of the maximal run of band-correct columns (V_tau-phase) contained in the protected interval [·, e - r_(jT')) at time tau + jT' (r = right-front recurrence over j epochs).  Then y_0 < y_1 < ... < y_n.  In particular y_n >= y_0 + n and no stationary left junction exists for this band under this clock (for any exterior and any left context).

*Proof (PAPER PROOF).*  It is r12f's Theorem A with general s, T'.  (The bounds used below: l over j epochs <= jL and r over j epochs <= jR', because the increment of a front over one epoch started at any position equals the one-epoch front of the rotation of V_tau having phase 0 at that position.)
(a) Cone lemma for general bands.  Claim: if P_t (t <= N) is any orbit with clock g and P_0 equals the V-band row (phase a) on [a, e), then P_t equals V_t (phase a) on [a + l_t, e - r_t) with the recurrences of sec. 1 (the run lengths computed in the band rows V_t).  Proof by induction on t: on the agreement interval the carries agree with the band background as soon as a non-(b-1) letter has occurred (a letter != b-1 determines the outgoing carry regardless of the incoming one), so alpha_c is correct for c >= a_t + 1 + rho (rho = run of (b-1) in V_t starting at a_t) and beta_c is correct for c <= e_t - 1 - rho' (rho' = run of (b-1) ending at e_t - 1); hence lo_c is correct on [a_t+1+rho, e_t) and hi_c on (a_t, e_t - 1 - rho'), and P'_c = lo_c + hi_c (g=0) / lo_c + hi_(c-1) (g=1) is correct on [a_t + 1 + rho, e_t - 1 - rho' + g_t).  This is exactly l_(t+1) = l_t + 1 + rho, r_(t+1) = r_t + 1 - g_t + rho'.  (Same statement as r12f sec. 2 for s = 3; also validated on 20+ genuine orbits, bandval.py: cone check on all columns.)  Under the clock g the left and right fronts satisfy the recurrences of sec. 1: the only couplings of a pure interval to its context are the carries at its ends (alpha at the left end, beta at the right end, hi of the column left of the interval at overflow steps).
(b) y_j is well defined by (H3) (the interval [y_0 + l_(jT'), e - r_(jT')) is non-empty and pure) and y_j <= y_0 + jL + ... ; y_j >= R+1 for all j: holds for j = 0 by (H2), and the induction below makes y_j strictly increase.
(c) Induction.  At time tau + jT' the row of the band is a rotation of V_tau (T_rot | T'; exactly V_tau if T | T').  Put y* = y_j and let W be the rotation of V_tau with phase 0 at y*.  By maximality of the run the letter at y*-1 is not W[s-1] (y* >= 1).
(d) Over the epoch [tau+jT', tau+(j+1)T'] the clock is forced by (H1) and equals g_(tau+u) because T' is a multiple of p.  The columns [y*-R, y*+l^W_u+Delta) at time tau+jT'+u form a solution of L(W,R,M), except possibly the final condition, with the genuine values as the free cells and the genuine alpha_(y*-R), hi_(y*-R-1) as the free left port (columns y*-R-1 >= 0 exist by (b)).  The band background at the right edge of the trimmed window is correct by the cone lemma applied at time tau+jT' to the pure interval [y*, e - r_(jT')) with (H3): the column y*+l^W_u+Delta+s+2 is < e - r_(jT'+u) (L, R' bounds).
(e) If y_(j+1) <= y*, then the columns [y*, e - r_((j+1)T')) are pure at time tau+(j+1)T', which contains the final window of the instance, by (H3).  This contradicts UNSAT.  Hence y_(j+1) > y_j.  QED.
(Origin: the choice of tau only fixes which row of the band cycle the epochs start from.  A stationary junction of period P = mT' -- every column band-correct region periodic -- would give, for every origin tau and every M, a solution: take j maximising y_j over a period.  So UNSAT at one origin tau and one M for all rotations already excludes every stationary junction.)

**Theorem GA* (multi-epoch L*).**  L*(V,W,tau,R,M) is L(V,W,tau,R,M) with the band additionally required to be correct on [y, inf) at all intermediate epoch boundaries j T, j = 1..M.  If L*(M) is UNSAT for every rotation W of V_tau, then under (H1)-(H3) (with n epochs of length T = T'/M) one has: for every j there is an i <= M with y_(j+i) > y_j; in particular no stationary junction exists.  Proof: as Theorem GA, using epoch length T (the right-port background is unchanged): if y_(j+i) <= y_j for all i = 1..M, the genuine columns solve L*(M) (at each epoch boundary the band is correct on [y_j, ·)).  In particular if y_j is periodic (stationary junction of any period), take j maximising y_j over the period: contradiction.  Label: PAPER PROOF, input COMPUTED.  (L(M) with a single final condition is the instance of Theorem GA for epoch length M T; L* is usually easier for the solver and stronger as a test because it contains more unit constraints.  Neither implies the other's UNSAT in general.)

**Corollary GB (template returns).**  Let Phi^N(P) = P' be a return of a template with an exterior/junction, a pure band V^k (k large by (H3)) and a stationary left part (the band starts at the same column before and after), under a clock with T' | N.  If L(V,W,tau,R,M) is UNSAT for all rotations W of V_tau, the return is impossible.
Scope: every statement is for the fixed clock g (phase-aligned at time tau, which is automatic when T' is a multiple of p and the return has clock g); no statement about bands not in the tables, about larger T, or about other clocks.

**Theorem GR (right end; label PAPER PROOF, input COMPUTED).**  If R(V,W,M,R_f) is UNSAT for every rotation W of V_tau, then in any orbit with clock g over the epochs, at each epoch time j with the maximal band-correct run ending at z_j (letter at z_j != band continuation, the run reaching the protected left zone) and z_j + R_f <= middle column, one has z_(j+1) <= z_j + delta - 1.  So the right end loses at least one column per epoch relative to the centre (which moves exactly delta = S'/2 per epoch), and no template with a bounded centre can return.  Not covered: centres with z_j + R_f > middle column (very short centres, the centre lemma base case), and templates whose band runs through the middle without a foreign letter (self-mirror lattices); these need the exact middle coupling (see sec. 6).

**Theorem GR* (comoving right end; label PAPER PROOF, input COMPUTED).**  R*(V,W,M,R_f) is R(V,W,M,R_f) plus the comoving condition: the letters of columns [z+delta, z+R_f) at time T' equal the letters of columns [z, z+R_f-delta) at time 0.  If R* is UNSAT for every rotation W of V_tau, then no template whose band V ends at a first deviating column z (letter at z != band continuation), with z + R_f <= middle column and with a comoving return (P_(T')(c+delta) = P_0(c) for the columns c >= z left of the middle, i.e. the centre region just shifts by delta columns per return T' = M T under clock g) exists.  (This is the generalisation of r12a's centre lemma E_R; R_f >= delta + 1 makes the comoving part non-empty.)  The proof is the genuine-solution argument of Theorem GR.  Not covered: centres with z + R_f > middle column, handled only by the direct small-centre SAT sweeps (centregen.py, sec. 6.3).


## 0b. Results in brief (final summary, 14:55 UTC, corrected 15:15 after an audit of the logs; explicit lists and tallies below; tables in sec. 7)

**1. Census (COMPUTED).**  All bands up to rotation with s <= 8: clock 1000: 265; clock 10: 284; clock 00001110001 (p11): 161; periods T up to 10752.  bandcensus.cpp (bitset F-iteration over all (2b-1)^s words), cross-checked against independent SAT all-solutions enumeration (cross_census.py: exact match at (1000,3,120), (1000,4,32), (10,4,16), (p11,3,33), (p11,4,22); the larger cases (1000,5,40), (1000,5,120), (1000,5,240), (10,5,30) did not finish).  W0 (s=9) and the p8 lattices (s=20,48) are outside the range.

**2. Generalised erosion (PAPER PROOF, COMPUTED inputs; sec. 2).**  Theorem GA: if the one-epoch L instance is UNSAT for every rotation of V_tau (one origin tau, epoch T' a multiple of T_rot), then under the forced clock the band start strictly increases at every epoch; in particular no stationary left junction exists for ANY exterior (hypotheses H1-H3: forced clock on the epochs, band present and long enough).  Same proof for general s, T.  Variants L* (intermediate marks), Lr (T' = T_rot), tau-scans.  Theorems GR, GR*: foreign-letter right ends / comoving centres.

**3. Controls: all pass (sec. 3).**  U3 words: 30/30 UNSAT in 3 solver/encoding combinations at T=120 (reproducing r12f) and 30/30 UNSAT at the shorter epoch T_rot = 40 (new, stronger, 3 methods); W0 and p8 rows SAT; base-9 certificates pass L and R, base-9 centre SAT finds their fold centres; exact big-integer replay of the base-9 template (fullreplay.py) MATCH; rooted exterior SAT recovers B0 exactly from the band W0 (positive control of rootseam.py); 78 genuine big-integer validations of every encoding (L, R, enc1 trimmed/rectangle, enc2, bases 9/10/13) and SEAMVAL PASS for the seam encoding; all clear.

**4. L and R (M = 1 unless stated; R = 12; label COMPUTED; numbers in the machine tally below).**
- clock 1000: L: 112 PASS, 4 ALLUNSAT [(0), (18), (9,18,9,0), U3 (18,9,0)], 14 UNDECIDED (timeouts), 26 with T <= 120 not run (s >= 7, T > 60), 109 with T > 120 not run; R: 114 PASS, 4 ALLUNSAT [same four bands], 14 UNDECIDED; R* (comoving foreign-letter centre, R_f >= delta): 28 ALLUNSAT, 58 PASS.
- additional L exclusions at clock 1000: tau-scan (T <= 24): (5,2,1), (11,9,2), (16,12,16,2,6,2); L* M=4: (11,9,2); Lr (U3, (9,18,9,0)); (L*/Lr/tau results all in the sec. 7 tables).
- clock 10 (T <= 36): L: 131 PASS, 6 ALLUNSAT [(0), (18), (12,9,6), (9,12,6), (9,18,9,0), (12,9,9,6,18,9,0)], 17 UNDEC; R: 107 PASS, 6 ALLUNSAT [same six bands]; R*: 44 PASS, 33 ALLUNSAT.
- clock p11 (T <= 33): L: 13 PASS, 2 ALLUNSAT [(0), (18)]; R: 11 PASS, 2 ALLUNSAT [same].
- Observation: in the T <= 36 (clock 10) and T <= 33 (p11) cases the L-ALLUNSAT and R-ALLUNSAT sets coincide (also clock 1000 for T <= 120).  One-epoch L/R pass for most short-period bands: necessary tests only.  Every ALLUNSAT above was confirmed with at least two further solver/encoding combinations (audit 15:12 over all logs: 0 contradictions between methods, every non-LD ALLUNSAT key has three solver/encoding combinations).
- CANDIDATES (pass L and R, one epoch): clock 1000: 97 (57 of them also pass R*); clock 10: 101; p11: 11 (R* not run).  Self-mirror (SM) bands can close at the fold without a foreign letter (R/R* do not apply to the fold).

**5. Real-thing attempts.**
(a) Centres (exact SAT centregen.py in the style of satc.py, general base/band/clock; forced clock; replayed by direct digit arithmetic centre_replay.py): NON-TRIVIAL centres exist at clock 1000, N = 24, j = 1: band (11,8,5), T=24: V0 = (5,11,8), C = (13,2,13); band (13,10,7), T=24, row (13,7,10) at tau=4: C = (5,16,5).  Fold centres (C empty) for (6),(12),(2),(4),(15,0,15),(3,18,3),(5,8,5),(8,2,8).  LABEL COMPUTED (centre instance only: the band background is assumed on both sides, the window is V^m C rev(V)^m with band-exact boundary; it is not yet a full template).
(b) Junctions from the T12 exterior W0 (seamgen.py, validated on genuine orbits; kissat404 only, NOT cross-checked with a second solver; exterior phase rotE = 0; all origins up to T_rot and all rotations): no SAT found.  Exact scope: T in {4,12} (17 L-PASS bands, N = 12): complete for |J| <= 12.  T in {4,12,24} (49 L-PASS bands, N = lcm(12,T) <= 24; bands with T = 16 or 20 have N = 48, 60 and were NOT swept): complete for |J| <= 8 for 39 bands; 10 bands were stopped by the per-band budget (complete only for |J| <= 4..7, see sec. 7).  Deeper sweep |J| = 9..12 at T = 24 (18 survivor bands): complete only for the three bands (11,8,5), (13,10,7), (8,5,5); 12 others budget-limited (partial); (14,10,0), (15,13,2), (16,11,3) have no result, and one instance each of (16,5,1), (17,7,2), (8,13,3) was lost, because my own cleanup killed those processes at 14:20.  Seams against the p8 lattices (clock 10) and the p11 exterior were NOT run.
(c) Rooted exterior search (rootseam.py: exterior word X of width w with exact root conditions, period N, band V to the right; validated: for V = W0, N = 12, w = 34 SAT finds X = B0 exactly): for the centre-bearing bands at the origin of their centre only ((11,8,5) tau = 0, (13,10,7) tau = 4), N = 24, cadical195, one solver: rotation r = 0: UNSAT for all widths w <= 20, widths 21..32 undecided (100 s timeouts); rotation 1: UNSAT for w <= 18 and w <= 19 respectively, then timeouts (80 s); rotation 2 not reached.  Widths are the exact exterior width (no monotonicity is claimed).  (15,15,0) (T = 12, N = 12, tau = 0, all rotations, w <= 40): UNSAT.  Uniform bands (2),(4),(6),(12) with N = 24: not finished (stopped).  (8,5,5), (8,8,2): stopped without a summary.
No full template, no certificate, no statement about 196.

**6. Exact-period junctions in the free-port relaxation (LD; extra):** clock 1000, T <= 24, m = 1,2: 26 of 46 tested bands admit an exact-period junction (list below); several T=4 bands (18,16,2), (2,16,0), (10,1,17,2,0), (16,18,8,17,1), (5,5,2,13,11,0), (7,18,13,13,16,5) at m = 1.

**Cross-check bookkeeping:** every ALLUNSAT entry in the explicit list carries at least two solver/encoding combinations (cadical195/enc1, kissat404/enc2 in addition to kissat404/enc1) except the two rotating-epoch entries listed as single-method in the auto list below: Lr (U3, T'=40) and Lr ((9,18,9,0), T'=16): both are also confirmed with cadical195/enc1 and kissat404/enc2, the logs are outside the i*.log pattern (logs/u3rot/u3rot.log, logs/xchk_lr.log).  LD (exact-period) ALLUNSAT entries are single-method (kissat404/enc1) and are not used for any exclusion statement.
## 0b. Status summary (generated by status_gen.py; hand-written context in FINAL_head; last run see date below)

**Clock 1000: bands with an ALLUNSAT result** (V, mode, T, horizon T', origin tau, R; methods listed in sec. 7 explicit list):
(0) T=4 [L:T'=4, L:T'=8, LD:T'=4, LD:T'=8, R:T'=8]; (12) T=4 [LD:T'=4, LD:T'=8, R*:T'=8]; (18) T=4 [L:T'=4, L:T'=8, LD:T'=4, LD:T'=8, R:T'=8]; (6) T=4 [LD:T'=4, LD:T'=8, R*:T'=8]; (2) T=12 [LD:T'=12, LD:T'=24, R*:T'=24]; (4) T=12 [LD:T'=12, LD:T'=24, R*:T'=24]; (15,15,0) T=12 [LD:T'=12, LD:T'=24, R*:T'=24]; (16,18,2) T=12 [LD:T'=12]; (16,2,0) T=12 [LD:T'=12]; (18,3,3) T=12 [LD:T'=12, LD:T'=24, R*:T'=24]; (10,18,2) T=24 [R*:T'=24]; (11,9,2) T=24 [L:T'=24,tau=8, L:T'=24,tau=12, L:T'=48, L*:T'=96, LD:T'=24, LD:T'=48]; (13,15,2) T=24 [LD:T'=24]; (15,12,9) T=24 [LD:T'=24, R*:T'=24]; (16,5,3) T=24 [LD:T'=24]; (16,8,0) T=24 [R*:T'=24]; (18,10,2) T=24 [LD:T'=24]; (5,2,1) T=24 [L:T'=24,tau=16, L:T'=24,tau=20, LD:T'=24]; (8,16,0) T=24 [LD:T'=24]; (9,6,3) T=24 [LD:T'=24, R*:T'=24]; (18,9,0) T=120 [L:T'=120, Lr:T'=40, R:T'=120]; (9,18,9,0) T=32 [L:T'=32, Lr:T'=16, R:T'=32]; (17,8,18,16,1) T=20 [R*:T'=40]; (2,17,1,10,0) T=20 [R*:T'=40]; (5,13,17,9,1) T=20 [LD:T'=20, LD:T'=40, R*:T'=40]; (9,17,13,5,1) T=20 [LD:T'=20, LD:T'=40, R*:T'=40]; (2,9,6,9,1) T=40 [R*:T'=40]; (6,11,8,8,3) T=40 [R*:T'=40]; (8,8,11,6,3) T=40 [R*:T'=40]; (9,6,9,2,1) T=40 [R*:T'=40]; (8,4,16,10,14,2) T=4 [LD:T'=4, LD:T'=8]; (14,6,9,4,9,0) T=16 [R*:T'=48]; (17,2,18,9,10,1) T=16 [R*:T'=48]; (9,3,7,9,9,2) T=16 [R*:T'=48]; (9,8,17,1,16,0) T=16 [R*:T'=48]; (15,13,13,15,2,2) T=24 [LD:T'=24, R*:T'=48]; (16,12,16,2,6,2) T=24 [L:T'=24,tau=4, LD:T'=24, R*:T'=48]; (16,14,15,2,7,0) T=24 [LD:T'=24]; (9,12,6,12,9,0) T=24 [LD:T'=24, R*:T'=48]; (10,8,18,8,10,0) T=48 [R*:T'=48]; (9,18,9,9,9,0) T=48 [R*:T'=48]; (13,16,2,16,13,0,0) T=28 [R*:T'=56]

**Clock 10: bands with an ALLUNSAT result** (V, mode, T, horizon T', origin tau, R; methods listed in sec. 7 explicit list):
(0) T=2 [L:T'=2, R:T'=4]; (12) T=2 [R*:T'=4]; (18) T=2 [L:T'=2, R:T'=4]; (6) T=2 [R*:T'=4]; (10,4,4) T=6 [R*:T'=12]; (10,6,2) T=6 [R*:T'=12]; (12,4,2) T=6 [R*:T'=12]; (12,9,6) T=6 [L:T'=6, R:T'=12]; (14,2,2) T=6 [R*:T'=12]; (16,9,2) T=6 [R*:T'=12]; (4,12,2) T=6 [R*:T'=12]; (6,10,2) T=6 [R*:T'=12]; (9,12,6) T=6 [L:T'=6, R:T'=12]; (9,16,2) T=6 [R*:T'=12]; (10,8,4) T=12 [R*:T'=12]; (13,10,3) T=12 [R*:T'=12]; (14,4,0) T=12 [R*:T'=12]; (16,2,0) T=12 [R*:T'=12]; (11,17,7,1) T=4 [R*:T'=16]; (9,18,9,0) T=8 [L:T'=8, R:T'=16]; (4,4,2,2) T=16 [R*:T'=16]; (6,10,6,2) T=16 [R*:T'=16]; (14,4,16,9,2) T=10 [R*:T'=20]; (15,4,15,1,1) T=10 [R*:T'=20]; (17,17,3,14,3) T=10 [R*:T'=20]; (9,16,4,14,2) T=10 [R*:T'=20]; (10,9,14,9,7,2) T=6 [R*:T'=24]; (13,8,15,5,10,3) T=6 [R*:T'=24]; (9,11,16,8,9,4) T=6 [R*:T'=24]; (7,9,14,9,10,2) T=12 [R*:T'=24]; (9,15,9,9,9,3) T=12 [R*:T'=24]; (9,17,17,9,1,1) T=12 [R*:T'=24]; (9,8,16,11,9,4) T=12 [R*:T'=24]; (9,9,9,15,9,3) T=12 [R*:T'=24]; (14,2,12,5,4,1) T=24 [R*:T'=24]; (8,6,4,8,2,0) T=24 [R*:T'=24]; (12,9,9,6,18,9,0) T=14 [L:T'=14, R:T'=28]; (18,11,13,9,5,7,0) T=14 [R*:T'=28]; (13,8,6,9,5,10,3) T=28 [R*:T'=28]

**Clock 00001110001: bands with an ALLUNSAT result** (V, mode, T, horizon T', origin tau, R; methods listed in sec. 7 explicit list):
(0) T=11 [L:T'=11, R:T'=11]; (18) T=11 [L:T'=11, R:T'=11]

**Survivors so far** = bands whose L(M=1, tau=0) result is PASS and with NO ALLUNSAT in any applicable test (L, L*, Lr, tau-scans, and R, R* except for self-mirror bands, whose centre can be the fold) up to now; the list is the current "candidate" set of the census (a pass is only a necessary test).  Bands with timeouts count as UNDECIDED, not survivors.

clock 1000: 76 survivors: (18,16,2) s=3 T=4 [R:PASS R*:PASS]; (2,16,0) s=3 T=4 [R:PASS R*:PASS]; (11,8,5) s=3 T=24 [R:PASS R*:PASS]; (13,10,7) s=3 T=24 [R:PASS R*:PASS]; (14,10,0) s=3 T=24 [R:PASS R*:PASS]; (15,13,2) s=3 T=24 [R:PASS R*:PASS]; (16,11,3) s=3 T=24 [R:PASS R*:PASS]; (16,5,1) s=3 T=24 [R:PASS R*:PASS]; (17,7,2) s=3 T=24 [R:PASS R*:PASS]; (8,13,3) s=3 T=24 [R:PASS R*:PASS]; (8,5,5) s=3 T=24 [SM R:PASS R*:PASS]; (8,8,2) s=3 T=24 [SM R:PASS R*:PASS]; (2,0,0) s=3 T=36 [SM R:PASS R*:-]; (2,2,0) s=3 T=36 [SM R:PASS R*:-]; (10,10,2,2) s=4 T=32 [SM R:PASS R*:PASS]; (13,4,13,0) s=4 T=32 [SM R:PASS R*:PASS]; (17,4,9,0) s=4 T=32 [R:PASS R*:PASS]; (18,9,14,1) s=4 T=32 [R:PASS R*:PASS]; (16,16,0,0) s=4 T=48 [SM R:UNDEC R*:-]; (8,8,0,0) s=4 T=48 [SM R:UNDEC R*:-]; (10,1,17,2,0) s=5 T=4 [R:PASS R*:PASS]; (16,18,8,17,1) s=5 T=4 [R:PASS R*:PASS]; (13,4,1,10,0) s=5 T=12 [R:UNDEC R*:-]; (8,8,16,9,0) s=5 T=12 [R:UNDEC R*:-]; (17,16,18,11,4) s=5 T=40 [R:PASS R*:PASS]; (7,14,1,2,0) s=5 T=40 [R:PASS R*:PASS]; (8,14,14,8,0) s=5 T=60 [SM R:UNDEC R*:-]; (10,8,18,9,0) s=5 T=80 [R:PASS R*:-]; (9,18,8,10,0) s=5 T=80 [R:PASS R*:-]; (5,5,2,13,11,0) s=6 T=4 [R:PASS R*:PASS]; (7,18,13,13,16,5) s=6 T=4 [R:PASS R*:PASS]; (11,13,2,5,5,0) s=6 T=24 [R:PASS R*:PASS]; (14,10,16,4,8,2) s=6 T=24 [R:PASS R*:PASS]; (16,13,13,18,7,5) s=6 T=24 [R:PASS R*:PASS]; (16,7,7,16,1,1) s=6 T=24 [SM R:PASS R*:PASS]; (17,17,2,11,11,2) s=6 T=24 [SM R:PASS R*:PASS]; (7,2,15,14,16,0) s=6 T=24 [R:PASS R*:PASS]; (12,12,10,18,10,2) s=6 T=36 [R:- R*:-]; (8,16,6,6,8,0) s=6 T=36 [R:- R*:-]; (18,18,10,18,8,0) s=6 T=44 [R:- R*:-]; (8,0,10,18,0,0) s=6 T=44 [R:- R*:-]; (10,10,0,0,0,0) s=6 T=48 [SM R:PASS R*:PASS]; (10,8,18,8,10,0) s=6 T=48 [SM R:PASS R*:ALLUNSAT]; (10,9,18,2,17,1) s=6 T=48 [R:PASS R*:PASS]; (10,9,8,18,9,0) s=6 T=48 [R:PASS R*:PASS]; (12,12,0,8,8,0) s=6 T=48 [SM R:PASS R*:PASS]; (12,14,17,18,3,0) s=6 T=48 [R:PASS R*:PASS]; (13,9,7,8,11,3) s=6 T=48 [R:PASS R*:PASS]; (15,18,6,4,1,0) s=6 T=48 [R:PASS R*:PASS]; (15,6,5,16,4,2) s=6 T=48 [R:PASS R*:PASS]; (15,7,10,11,9,5) s=6 T=48 [R:PASS R*:PASS]; (15,7,3,3,14,0) s=6 T=48 [R:PASS R*:PASS]; (16,1,17,8,9,0) s=6 T=48 [R:PASS R*:PASS]; (16,14,14,16,0,0) s=6 T=48 [SM R:PASS R*:PASS]; (17,16,17,0,4,0) s=6 T=48 [SM R:PASS R*:PASS]; (18,18,2,4,4,2) s=6 T=48 [SM R:PASS R*:PASS]; (9,4,9,6,14,0) s=6 T=48 [R:PASS R*:PASS]; (9,9,7,3,9,2) s=6 T=48 [R:PASS R*:PASS]; (1,6,5,0,0,0) s=6 T=56 [R:- R*:-]; (6,15,4,17,0,0) s=6 T=56 [R:- R*:-]; (10,18,10,12,12,2) s=6 T=72 [R:- R*:-]; (8,6,6,16,8,0) s=6 T=72 [R:- R*:-]; (13,16,2,16,13,0,0) s=7 T=28 [SM R:PASS R*:ALLUNSAT]; (16,2,5,18,18,5,2) s=7 T=28 [SM R:PASS R*:-]; (10,11,8,8,9,10,7) s=7 T=56 [R:PASS R*:PASS]; (10,18,8,9,16,16,4) s=7 T=56 [R:PASS R*:PASS]; (10,9,2,2,14,8,0) s=7 T=56 [R:PASS R*:PASS]; (16,10,4,4,10,16,0) s=7 T=56 [SM R:PASS R*:-]; (16,16,1,13,6,13,1) s=7 T=56 [SM R:PASS R*:-]; (16,16,9,8,18,10,4) s=7 T=56 [R:PASS R*:-]; (18,2,16,16,16,4,0) s=7 T=56 [R:PASS R*:-]; (7,11,12,12,11,7,0) s=7 T=56 [SM R:PASS R*:-]; (8,14,2,2,9,10,0) s=7 T=56 [R:PASS R*:-]; (17,9,1,14,15,11,12,0) s=8 T=24 [R:- R*:-]; (9,9,14,4,9,17,9,0) s=8 T=24 [R:- R*:-]; (10,16,12,11,18,16,8,5) s=8 T=64 [R:PASS R*:-]

clock 10: 108 survivors: (12) s=1 T=2 [SM R:PASS R*:ALLUNSAT]; (6) s=1 T=2 [SM R:PASS R*:ALLUNSAT]; (2) s=1 T=6 [SM R:PASS R*:PASS]; (4) s=1 T=6 [SM R:PASS R*:PASS]; (10,10,4) s=3 T=6 [SM R:PASS R*:PASS]; (10,4,4) s=3 T=6 [SM R:PASS R*:ALLUNSAT]; (14,2,2) s=3 T=6 [SM R:PASS R*:ALLUNSAT]; (14,8,8) s=3 T=6 [SM R:PASS R*:PASS]; (18,6,6) s=3 T=6 [SM R:PASS R*:PASS]; (6,0,0) s=3 T=6 [SM R:PASS R*:PASS]; (12,6,0) s=3 T=12 [R:PASS R*:PASS]; (18,0,0) s=3 T=12 [SM R:PASS R*:PASS]; (18,9,0) s=3 T=12 [R:PASS R*:PASS]; (6,12,0) s=3 T=12 [R:PASS R*:PASS]; (2,0,0) s=3 T=18 [SM R:PASS R*:-]; (6,2,2) s=3 T=18 [SM R:PASS R*:-]; (10,4,0) s=3 T=36 [R:PASS R*:-]; (4,9,0) s=3 T=36 [R:PASS R*:-]; (9,4,0) s=3 T=36 [R:PASS R*:-]; (7,17,11,1) s=4 T=8 [R:PASS R*:PASS]; (10,10,2,2) s=4 T=16 [SM R:PASS R*:PASS]; (16,16,8,8) s=4 T=16 [SM R:PASS R*:PASS]; (4,4,2,2) s=4 T=16 [SM R:PASS R*:ALLUNSAT]; (6,10,6,2) s=4 T=16 [SM R:PASS R*:ALLUNSAT]; (4,6,2,0) s=4 T=48 [R:- R*:-]; (9,12,3,0) s=4 T=48 [R:- R*:-]; (5,15,8,7,1) s=5 T=4 [R:PASS R*:PASS]; (11,10,17,9,1) s=5 T=10 [R:PASS R*:PASS]; (12,11,16,3,0) s=5 T=10 [R:PASS R*:PASS]; (15,4,15,1,1) s=5 T=10 [SM R:PASS R*:ALLUNSAT]; (17,16,16,17,0) s=5 T=10 [SM R:PASS R*:PASS]; (17,17,3,14,3) s=5 T=10 [SM R:PASS R*:ALLUNSAT]; (7,8,7,1,1) s=5 T=10 [SM R:PASS R*:PASS]; (9,11,6,7,0) s=5 T=10 [R:PASS R*:PASS]; (9,17,10,11,1) s=5 T=10 [R:PASS R*:PASS]; (15,7,9,11,3) s=5 T=20 [R:PASS R*:PASS]; (7,8,15,5,1) s=5 T=20 [R:PASS R*:PASS]; (17,12,17,1,1) s=5 T=30 [SM R:- R*:-]; (17,17,1,6,1) s=5 T=30 [SM R:- R*:-]; (2,6,2,0,0) s=5 T=30 [SM R:- R*:-]; (6,14,6,0,0) s=5 T=30 [SM R:- R*:-]; (10,5,15,8,13,3) s=6 T=4 [R:PASS R*:PASS]; (12,14,7,17,17,5) s=6 T=4 [R:PASS R*:PASS]; (13,6,4,11,1,1) s=6 T=4 [R:PASS R*:PASS]; (5,9,6,8,7,1) s=6 T=4 [R:PASS R*:PASS]; (11,4,6,13,1,1) s=6 T=6 [R:PASS R*:PASS]; (17,17,7,14,12,5) s=6 T=6 [R:PASS R*:PASS]; (7,8,6,9,5,1) s=6 T=12 [R:PASS R*:PASS]; (9,17,17,9,1,1) s=6 T=12 [SM R:PASS R*:ALLUNSAT]; (13,8,18,14,17,4) s=6 T=18 [R:- R*:-]; (4,1,14,5,10,0) s=6 T=18 [R:- R*:-]; (12,9,17,6,9,1) s=6 T=24 [R:PASS R*:PASS]; (13,9,3,15,9,1) s=6 T=24 [R:PASS R*:PASS]; (15,9,5,17,9,3) s=6 T=24 [R:PASS R*:PASS]; (2,1,11,17,5,0) s=6 T=24 [R:PASS R*:PASS]; (5,17,11,1,2,0) s=6 T=24 [R:PASS R*:PASS]; (9,15,15,9,3,3) s=6 T=24 [SM R:PASS R*:PASS]; (10,5,14,1,4,0) s=6 T=36 [R:- R*:-]; (17,12,17,0,0,0) s=6 T=36 [SM R:- R*:-]; (17,14,18,8,13,4) s=6 T=36 [R:- R*:-]; (7,1,10,1,7,0) s=6 T=36 [SM R:- R*:-]; (12,15,12,9,0,0) s=6 T=48 [R:- R*:-]; (10,5,9,6,8,13,3) s=7 T=4 [R:PASS R*:PASS]; (3,17,10,15,9,7,0) s=7 T=6 [R:- R*:-]; (8,3,9,11,18,15,1) s=7 T=6 [R:- R*:-]; (13,13,0,9,16,9,0) s=7 T=14 [SM R:PASS R*:PASS]; (17,2,2,17,0,10,0) s=7 T=14 [SM R:PASS R*:PASS]; (18,8,18,1,16,16,1) s=7 T=14 [SM R:PASS R*:PASS]; (4,14,17,11,9,7,1) s=7 T=14 [R:PASS R*:PASS]; (7,9,11,17,14,4,1) s=7 T=14 [R:PASS R*:PASS]; (9,18,5,5,18,9,2) s=7 T=14 [SM R:PASS R*:PASS]; (14,7,1,9,6,17,0) s=7 T=28 [R:PASS R*:PASS]; (17,6,9,1,7,14,0) s=7 T=28 [R:PASS R*:PASS]; (14,1,6,10,8,8,1) s=7 T=42 [R:- R*:-]; (14,1,8,8,10,6,1) s=7 T=42 [R:- R*:-]; (15,18,11,9,3,8,1) s=7 T=42 [R:- R*:-]; (16,5,12,12,10,4,1) s=7 T=42 [R:- R*:-]; (17,12,17,1,2,2,1) s=7 T=42 [SM R:- R*:-]; (18,0,16,1,1,16,0) s=7 T=42 [SM R:- R*:-]; (4,10,12,12,5,16,1) s=7 T=42 [R:- R*:-] ...

clock p11: 13 survivors: (6) s=1 T=22 [SM R:PASS R*:-]; (16,9,2) s=3 T=33 [R:PASS R*:-]; (18,9,9) s=3 T=33 [SM R:PASS R*:-]; (9,16,2) s=3 T=33 [R:PASS R*:-]; (9,9,0) s=3 T=33 [SM R:PASS R*:-]; (16,16,2,2) s=4 T=22 [SM R:PASS R*:-]; (6,10,6,2) s=4 T=22 [SM R:PASS R*:-]; (8,8,4,4) s=4 T=22 [SM R:PASS R*:-]; (9,12,9,6) s=4 T=22 [SM R:PASS R*:-]; (7,11,8,11,9,2) s=6 T=22 [R:- R*:-]; (7,14,8,6,9,4) s=6 T=22 [R:- R*:-]; (18,18,9,9,0,0) s=6 T=33 [R:PASS R*:-]; (9,9,18,18,0,0) s=6 T=33 [R:PASS R*:-]

**ALLUNSAT entries with only one solver/encoding so far (cross-checks pending):** 39
- LD clock=1000 V=0 T=4 M=1 T'=4 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=0 T=4 M=2 T'=8 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=11,9,2 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=11,9,2 T=24 M=2 T'=48 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=12 T=4 M=1 T'=4 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=12 T=4 M=2 T'=8 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=13,15,2 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=15,12,9 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=15,13,13,15,2,2 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=15,15,0 T=12 M=1 T'=12 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=15,15,0 T=12 M=2 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=16,12,16,2,6,2 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=16,14,15,2,7,0 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=16,18,2 T=12 M=1 T'=12 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=16,2,0 T=12 M=1 T'=12 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=16,5,3 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=18 T=4 M=1 T'=4 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=18 T=4 M=2 T'=8 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=18,10,2 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=18,3,3 T=12 M=1 T'=12 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=18,3,3 T=12 M=2 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=2 T=12 M=1 T'=12 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=2 T=12 M=2 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=4 T=12 M=1 T'=12 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=4 T=12 M=2 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=5,13,17,9,1 T=20 M=1 T'=20 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=5,13,17,9,1 T=20 M=2 T'=40 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=5,2,1 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=6 T=4 M=1 T'=4 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=6 T=4 M=2 T'=8 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=8,16,0 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=8,4,16,10,14,2 T=4 M=1 T'=4 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=8,4,16,10,14,2 T=4 M=2 T'=8 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=9,12,6,12,9,0 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=9,17,13,5,1 T=20 M=1 T'=20 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=9,17,13,5,1 T=20 M=2 T'=40 tau=0 R=12: [('kissat404', '1')]
- LD clock=1000 V=9,6,3 T=24 M=1 T'=24 tau=0 R=12: [('kissat404', '1')]
- Lr clock=1000 V=18,9,0 T=120 M=1 T'=40 tau=0 R=12: [('kissat404', '1')]
- Lr clock=1000 V=9,18,9,0 T=32 M=1 T'=16 tau=0 R=12: [('kissat404', '1')]

**D-type results (LD, exact-period junction in the free-port relaxation, R=12; not a necessary condition for all periods, only for the tested period mT):**
clock 1000: 57 bands tested; 33 with an exact-period junction (LD SAT for some rotation at m=1 or 2):
(10,18,2) m=1:SUU; (11,8,5) m=1:USU; (13,10,7) m=1:USU; (14,10,0) m=1:SSS; (15,13,2) m=1:SSS; (16,11,3) m=1:USS; (16,18,2) m=2:SSU; (16,5,1) m=1:UUS; (16,8,0) m=1:USU; (17,7,2) m=1:UUS; (18,16,2) m=1:SUU m=2:SUS; (2,16,0) m=1:UUS m=2:USS; (8,13,3) m=1:STS; (8,5,5) m=1:SUS; (8,8,2) m=1:SSU; (10,1,17,2,0) m=1:UUUUS m=2:UUUUS; (13,4,1,10,0) m=1:UUUUS m=2:UUUUS; (16,18,8,17,1) m=1:USUUU m=2:USUUU; (17,8,18,16,1) m=1:UUSUS; (2,17,1,10,0) m=1:USUUS; (8,8,16,9,0) m=1:UUUSU m=2:UUUSU; (11,13,2,5,5,0) m=1:SUUSUS; (14,10,16,4,8,2) m=1:STSSST; (14,6,9,4,9,0) m=1:SUUUUU m=2:SUUUUT; (16,13,13,18,7,5) m=1:USUSSU; (16,7,7,16,1,1) m=1:USSUSS; (17,17,2,11,11,2) m=1:SSUSSU; (17,2,18,9,10,1) m=1:SUSUUU m=2:TSTUUT; (5,5,2,13,11,0) m=1:UUSUUU m=2:USSUUU; (7,18,13,13,16,5) m=1:UUUUSU m=2:UUUSSU; (7,2,15,14,16,0) m=1:UUSSSS; (9,3,7,9,9,2) m=1:SUUUUU; (9,8,17,1,16,0) m=1:UUUSUS

```
machine tally 15:16 UTC:
--- clock 1000: 265 bands
 L(M=1,tau=0): {'ALLUNSAT': 4, 'PASS': 112, 'UNDEC': 14, 'NOTRUN(T=1..)': 109, 'NOTRUN(T=0..)': 26}
 bands with some ALLUNSAT at (M,tau) in L/L*: 27
 multi-epoch/tau records: 218
 R: {'ALLUNSAT': 4, 'PASS': 114, 'UNDEC': 14, 'NOTRUN': 133}
 R*: {'ALLUNSAT': 28, 'PASS': 58}
--- clock 10: 284 bands
 L(M=1,tau=0): {'ALLUNSAT': 6, 'PASS': 131, 'UNDEC': 17, 'NOTRUN(T=1..)': 72, 'NOTRUN(T=0..)': 58}
 bands with some ALLUNSAT at (M,tau) in L/L*: 6
 multi-epoch/tau records: 0
 R: {'ALLUNSAT': 6, 'PASS': 107, 'NOTRUN': 171}
 R*: {'PASS': 44, 'ALLUNSAT': 33}
--- clock 00001110001: 161 bands
 L(M=1,tau=0): {'ALLUNSAT': 2, 'NOTRUN(T=0..)': 56, 'PASS': 13, 'NOTRUN(T=1..)': 90}
 bands with some ALLUNSAT at (M,tau) in L/L*: 2
 multi-epoch/tau records: 0
 R: {'ALLUNSAT': 2, 'NOTRUN': 148, 'PASS': 11}
 R*: {}
```

## 3. Mandatory controls
(For twisted bands the epoch can be T_rot instead of T: the statement of Theorem GA requires only that T' is a multiple of T_rot.  The U3 band (T=120, T_rot=40, twist 1) has all 30 word/rotation instances UNSAT already at epoch T' = 40: sec. 3.1.)
(status lines are updated as jobs finish; exact output lines are in logs/ctrl1.log, logs/ctrlU3/*, logs/val/*)
- (i) U3 words at clock 1000 (band (18,9,0), T = 120, T_rot = 40, origins tau = 0,4,..,36 x rotations 0..2 = the 30 words (9,a,18-a)): one-epoch L (R = 12) must be UNSAT (r12f):
  * epoch T' = T_rot = 40 (stronger): all 30 word instances UNSAT with kissat404/enc1, cadical195/enc1, kissat404/enc2 (logs/u3rot/u3rot.log, 5-15 s per word) -- COMPUTED, three methods;
  * epoch T = 120 (R = 12): all 30 words UNSAT in all three combinations kissat404/enc1, cadical195/enc1, kissat404/enc2 (table sec. 3.2; 17-55 s per instance), reproducing r12f.
  In the plain R test (sec. 6.1) the U3 band is also ALLUNSAT (T = 120, delta = 15, R_f = 18), consistent with r12a's centre theorem.
- (ii) T12 exterior W0 = (5,18,4,8,1,15,4,0,5) (s = 9, T = 12, clock 1000): L with the true band-start rotation (phase 0 at the first band-correct column of B0 W0^q): SAT (kissat404, cadical195; logs/ctrl1.log).  Period-8 lattice rows of lattice_formats/p8_scc.txt (s = 20, T = 8, clock 10; rows checked against the row map): L SAT at 4 rotations (both solvers).
- (iii) Base 9: certificate rows cert_b9_rec0 / rec1 (s = 4, T = 10, clock 1100011000, rows checked against the base-9 row map): L SAT at all rotations incl. the true band-start rotation (rec0: y* = 58, rotation 1; rec1: y* = 60, rotation 3), both solvers.  R (2 periods, S' = 8, delta = 4) with foreign letter: SAT at all rotations, both solvers.  So the base-9 certificates pass both tests.
- (iii-b) Planted control for W0 (ctrl/plant_w0.py): L instance with the genuine free letters/ports of the true T12 exterior at y* = 31: SAT, model = genuine letters at all (t,c).  Base-9 centre SAT (centregen.py, N = 20, j = 1): finds the fold centres (C = [] for V = (1,15,15,1), (15,1,1,15), (11,5,5,11), (5,11,11,5); C = band continuation for the Lc compatible with the axis), UNSAT for the incompatible Lc.  So the base-9 certificates' real centre (a fold) is reproduced by the centre tool.
- (iv) Genuine big-integer validations (bandval.py, Python integers, n -> n + rev n, any base): for random V (s = 1..7), random prefix/junction/centre, T = 24..40, GENUINE clock fed to the encoder, bases 9, 10, 13:
  cone recurrences checked on every column; L encoding (trimmed, rectangle, enc2) reproduces every letter of the genuine orbit with the genuine left port (alpha at y-R, hi digit at overflow steps), forbidding a genuine final letter UNSAT;
  R encoding (with the genuine right port bit beta_(z+R)(t) = alpha_(L-(z+R))(t) of the full addition) likewise.  Result: 78 runs (seeds 11-16; s = 1,2,4,5,7 base 10, s = 4 base 9, s = 3 base 13 rectangle mode; enc1 trim, enc2; T = 24-36; plus the seeds 1-5 used during development) all VALIDATE PASS (jobs_val.txt, logs/ctrl); seam encoding genuine check SEAMVAL PASS (seamval.py, N = 24, |J| = 5).  The validation exercises the L and R encodings with the genuine clock (arbitrary, not a fixed clock), including overflow-step couplings, the right-port bit beta_x1(t) = alpha_(L-x1)(t), and the left free port (alpha, hi digit).

### 3.1 U3 reproduction table
(filled from logs/ctrlU3)

## 4. Encodings and solvers
- enc1 (bandsat.py): one-hot letters, LO/HI digit variables, cone trimming (variables only left of y + l_t + Delta) and optional rectangle mode.
- enc2 (bandsat2.py): independent code, rectangle window, direct successor relations (no digit variables), periodic background re-derived by fixed-point iteration.
- Solvers: kissat404 (pysat) main; cadical195 cross-check.  Every UNSAT used in a statement of sec. 5/6 is reported with the solver/encoding combinations in the tables.

## 5. Census results
Bands are the F-cycles of sec. 1.  Counts per (clock, s) and the period distribution are in sec. 7.0; each band is listed with its period T, T_rot, twist and its L/R results in sec. 7.1-7.3 (machine generated from the logs).  The census was cross-checked by an independent SAT enumeration of all words with V_T = V (cross_census.py: s = 3, T = 120 clock 1000 exact match of the 110 necklaces at phase 0; further pairs as listed in NOTES).

## 6. L and R results, candidates, follow-up
Definition of the test outcomes: PASS(rotations) = at least one rotation SAT (a necessary condition holds; nothing more); ALLUNSAT = all rotations UNSAT (the band has no stationary left junction / no right end for that clock, Theorems GA, GR, GR*); UNDECIDED = some rotation timed out and no rotation SAT (or not all UNSAT).  Bound statement: the one-epoch L test (R = 12, origin tau = 0) was attempted for all bands with T <= 120 at clock 1000 (s <= 8 up to s = 7 for T > 60, with per-rotation timeouts 200/120/90 s, see the tables), for clocks 10 and p11 with T <= 36 (and 36 < T <= 60 as far as the time box allowed); bands beyond these bounds are UNDECIDED (NOTRUN) and are listed in sec. 8.  R is the test of sec. 1 with M minimal such that delta = S'/2 = 0 mod s; R* adds the comoving condition (sec. 2).
The explicit list of all ALLUNSAT bands is at the end of sec. 7 and in the machine tally of sec. 0b; survivors (bands not excluded by any test so far) are listed in sec. 0b as well.

### 6.1 Details and choices for test R (see also sec. 1, 2)
- Foreign letter: the instance as written in the task (free cells [z, z+R), no foreign condition) is trivially satisfiable by the band continuation (column z continuing the band, free right port = background carry).  So the meaningful instance has column z foreign (letter != W[0]), exactly as r12a's E_R and the L instance do.  Trivial nofor runs: SAT (controls).
- r12a relation: E_R(V) of r12a = the same instance with R_f = R <= delta and delta replaced by R_f (for U3 at R = 4 the comoving return reduces to "band correct on (-inf, z+4)" since 4 < 15), UNSAT for 26 of 30 U3 words at R = 4; with R_f >= delta and the comoving condition we get R* (sec. 2).  Plain R (no comoving condition) is weaker; a band with foreign right end that is R-UNSAT cannot keep up with the centre.
- delta must be an integer multiple of s for an exact return (the centre comoves by delta columns while the band phase must recur); the epoch count M is the minimal one with S' = overflows in MT even and delta = S'/2 = 0 mod s.
- Blind spots: the R theorem does not apply when the first deviation z from the band continuation lies within R_f of the middle column (the free cells would reach across the fold), and it does not treat templates whose band reaches the middle without a foreign letter (self-mirror lattice closure).  For such small centres the exact centre SAT (centregen.py: absolute-frame window V^m C rev(V)^m with the true fold, general base/clock; selftested against direct simulation) is the correct tool; used in the candidate sweeps of sec. 6.3.

### 3.2 U3 control at the full epoch (generated 15:16 UTC)
U3 words at T=120, R=12: 30 word instances reported; validation runs: {'VALIDATE PASS': 78}
| tau | rot | word | kissat404/enc1 | cadical195/enc1 | kissat404/enc2 |
|---|---|---|---|---|---|
| 0 | 0 | (18, 9, 0) | UNSAT 21s | UNSAT 21s | UNSAT 38s |
| 0 | 1 | (9, 0, 18) | UNSAT 20s | UNSAT 27s | UNSAT 37s |
| 0 | 2 | (0, 18, 9) | UNSAT 19s | UNSAT 25s | UNSAT 38s |
| 4 | 0 | (9, 12, 6) | UNSAT 24s | UNSAT 24s | UNSAT 40s |
| 4 | 1 | (12, 6, 9) | UNSAT 24s | UNSAT 29s | UNSAT 41s |
| 4 | 2 | (6, 9, 12) | UNSAT 26s | UNSAT 26s | UNSAT 40s |
| 8 | 0 | (10, 8, 9) | UNSAT 24s | UNSAT 27s | UNSAT 37s |
| 8 | 1 | (8, 9, 10) | UNSAT 22s | UNSAT 22s | UNSAT 41s |
| 8 | 2 | (9, 10, 8) | UNSAT 22s | UNSAT 23s | UNSAT 38s |
| 12 | 0 | (14, 9, 4) | UNSAT 19s | UNSAT 21s | UNSAT 43s |
| 12 | 1 | (9, 4, 14) | UNSAT 19s | UNSAT 23s | UNSAT 37s |
| 12 | 2 | (4, 14, 9) | UNSAT 24s | UNSAT 23s | UNSAT 37s |
| 16 | 0 | (9, 2, 16) | UNSAT 22s | UNSAT 23s | UNSAT 43s |
| 16 | 1 | (2, 16, 9) | UNSAT 17s | UNSAT 16s | UNSAT 35s |
| 16 | 2 | (16, 9, 2) | UNSAT 24s | UNSAT 23s | UNSAT 36s |
| 20 | 0 | (18, 0, 9) | UNSAT 20s | UNSAT 26s | UNSAT 37s |
| 20 | 1 | (0, 9, 18) | UNSAT 25s | UNSAT 24s | UNSAT 36s |
| 20 | 2 | (9, 18, 0) | UNSAT 25s | UNSAT 24s | UNSAT 36s |
| 24 | 0 | (12, 9, 6) | UNSAT 18s | UNSAT 25s | UNSAT 36s |
| 24 | 1 | (9, 6, 12) | UNSAT 20s | UNSAT 24s | UNSAT 42s |
| 24 | 2 | (6, 12, 9) | UNSAT 33s | UNSAT 23s | UNSAT 36s |
| 28 | 0 | (9, 8, 10) | UNSAT 35s | UNSAT 28s | UNSAT 47s |
| 28 | 1 | (8, 10, 9) | UNSAT 23s | UNSAT 30s | UNSAT 40s |
| 28 | 2 | (10, 9, 8) | UNSAT 23s | UNSAT 25s | UNSAT 35s |
| 32 | 0 | (14, 4, 9) | UNSAT 22s | UNSAT 23s | UNSAT 35s |
| 32 | 1 | (4, 9, 14) | UNSAT 24s | UNSAT 24s | UNSAT 37s |
| 32 | 2 | (9, 14, 4) | UNSAT 23s | UNSAT 25s | UNSAT 42s |
| 36 | 0 | (2, 9, 16) | UNSAT 22s | UNSAT 28s | UNSAT 35s |
| 36 | 1 | (9, 16, 2) | UNSAT 18s | UNSAT 22s | UNSAT 45s |
| 36 | 2 | (16, 2, 9) | UNSAT 19s | UNSAT 24s | UNSAT 40s |

Rows with UNSAT in all three method combinations: 30 of 30

## 7. Band tables (generated 15:16 UTC by mkfinal.py)
## 7.0 Census summary (number of bands up to rotation, primitive words)

- clock 1000 (N12 / T12 exterior): 265 bands; s=1:6 s=3:31 s=4:7 s=5:44 s=6:55 s=7:72 s=8:50
  period T distribution: 4x11, 12x8, 16x4, 20x4, 24x32, 28x2, 32x5, 36x4, 40x6, 44x2, 48x20, 56x14, 60x4, 64x12, 72x2, 80x2, 84x8, 96x2, 108x2, 112x5, 120x7, 128x4, 140x2, 148x2, 160x4, 168x5, 180x2, 192x3, 216x2, 224x2, 240x4, 252x4, 264x2, 280x4, 300x2, 320x2, 336x6, 340x2, 360x2, 364x2, 392x2, 440x2, 480x6, 504x2, 512x4, 560x2, 616x1, 672x2, 700x2, 780x2, 840x2, 896x2, 960x2, 1036x2, 1216x3, 1316x4, 1392x2, 1904x4, 2400x2, 2464x1, 2784x2, 10752x2
- clock 10 (period-8 lattices): 284 bands; s=1:6 s=3:28 s=4:11 s=5:33 s=6:40 s=7:67 s=8:99
  period T distribution: 2x6, 4x8, 6x24, 8x2, 10x10, 12x14, 14x8, 16x7, 18x4, 20x2, 24x10, 28x3, 30x6, 32x18, 36x10, 42x12, 48x14, 56x2, 60x11, 70x4, 72x2, 96x31, 112x4, 126x4, 130x2, 140x1, 144x4, 160x5, 168x8, 180x1, 240x2, 280x6, 288x8, 336x2, 348x2, 360x2, 504x2, 532x2, 544x1, 608x2, 720x2, 960x2, 1064x2, 1344x2, 1392x2, 1526x4, 2200x2, 4400x2
- clock 00001110001 (p11): 161 bands; s=1:4 s=3:18 s=4:10 s=5:22 s=6:22 s=7:48 s=8:37
  period T distribution: 11x2, 22x7, 33x6, 44x15, 66x24, 77x6, 88x4, 110x7, 132x17, 154x12, 220x4, 231x2, 264x2, 308x6, 330x13, 396x1, 462x12, 484x4, 528x4, 770x4, 924x2, 1232x1, 1386x2, 1452x1, 2310x1, 4774x2


### 7.1 clock 1000 (N12 / T12 exterior): 265 bands (all spatial periods s <= 8 enumerated; primitive words, up to rotation)

| s | V (canonical row, clock phase 0) | T | T_rot/twist | S | #9 | SM | L(M=1) rots | L(1) | L*, Lr, LD, tau-scan (M, status) | R (M) | R* (M) | class | time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 4 | 4/0 | 1 | 0 | Y,d | U | ALLUNSAT | LDM=1:ALLUNSAT(U); LDM=2:ALLUNSAT(U); LM=2:ALLUNSAT(U) | M=2:ALLUNSAT(U) | - | EXCLUDED(L) | kissat404 0s |
| 1 | 12 | 4 | 4/0 | 1 | 0 | Y,d | S | PASS | LDM=1:ALLUNSAT(U); LDM=2:ALLUNSAT(U); LM=2:PASS(S); L*M=24:PASS(S) | M=2:PASS(S) | M=2:ALLUNSAT(U) | CAND | cadical195 0s |
| 1 | 18 | 4 | 4/0 | 1 | 0 | Y,d | U | ALLUNSAT | LDM=1:ALLUNSAT(U); LDM=2:ALLUNSAT(U); LM=2:ALLUNSAT(U) | M=2:ALLUNSAT(U) | - | EXCLUDED(L) | kissat404 0s |
| 1 | 6 | 4 | 4/0 | 1 | 0 | Y,d | S | PASS | LDM=1:ALLUNSAT(U); LDM=2:ALLUNSAT(U); LM=2:PASS(S); L*M=24:PASS(S) | M=2:PASS(S) | M=2:ALLUNSAT(U) | CAND | kissat404 0s |
| 1 | 2 | 12 | 12/0 | 3 | 0 | Y,d | S | PASS | LDM=1:ALLUNSAT(U); LM=1tau4:PASS(S); LM=1tau8:PASS(S); LDM=2:ALLUNSAT(U); LM=2:PASS(S); L*M=8:PASS(S) | M=2:PASS(S) | M=2:ALLUNSAT(U) | CAND | kissat404 1s |
| 1 | 4 | 12 | 12/0 | 3 | 0 | Y,d | S | PASS | LDM=1:ALLUNSAT(U); LM=1tau8:PASS(S); LM=1tau4:PASS(S); LDM=2:ALLUNSAT(U); LM=2:PASS(S); L*M=8:PASS(S) | M=2:PASS(S) | M=2:ALLUNSAT(U) | CAND | cadical195 0s |
| 3 | 18,16,2 | 4 | 4/0 | 1 | 0 | N | S?? | PASS | LDM=1:PASS(SUU); LDM=2:PASS(SUS); L*M=24:PASS(S??) | M=6:PASS(S??) | M=6:PASS(US?) | CAND | kissat404 0s |
| 3 | 2,16,0 | 4 | 4/0 | 1 | 0 | N | US? | PASS | LDM=1:PASS(UUS); LDM=2:PASS(USS); L*M=24:PASS(US?) | M=6:PASS(S??) | M=6:PASS(S??) | CAND | kissat404 0s |
| 3 | 15,15,0 | 12 | 4/1 | 3 | 0 | Y,d | SSS | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LDM=2:ALLUNSAT(UUU); LM=2:PASS(SSS); L*M=8:PASS(S??) | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | cadical195 1s |
| 3 | 16,18,2 | 12 | 4/2 | 3 | 0 | N,d | SSS | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LDM=2:PASS(SSU); L*M=8:PASS(S??) | M=2:PASS(S??) | M=2:PASS(S??) | CAND | kissat404 2s |
| 3 | 16,2,0 | 12 | 4/2 | 3 | 0 | N,d | SSS | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LDM=2:UNDEC(UTT); L*M=8:PASS(S??) | M=2:PASS(S??) | M=2:PASS(S??) | CAND | cadical195 1s |
| 3 | 18,3,3 | 12 | 4/1 | 3 | 0 | Y,d | SSS | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LDM=2:ALLUNSAT(UUU); LM=2:PASS(SSS); L*M=8:PASS(S??) | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 2s |
| 3 | 10,18,2 | 24 | 8/2 | 6 | 0 | N,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(SUU); LM=1tau4:PASS(S??); LDM=2:UNDEC(TTT); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:ALLUNSAT(UUU) | CAND | kissat404 2s |
| 3 | 11,8,5 | 24 | 8/2 | 6 | 0 | N,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(USU); LM=1tau4:PASS(S??); LDM=2:UNDEC(TTT); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(UUS) | CAND | kissat404 4s |
| 3 | 11,9,2 | 24 | 24/0 | 6 | 1 | N,d | SUU | PASS | LDM=1:ALLUNSAT(UUU); LM=1tau20:PASS(US?); LM=1tau16:PASS(S??); LM=1tau8:ALLUNSAT(UUU); LM=1tau12:ALLUNSAT(UUU); LM=1tau4:PASS(S??); LDM=2:ALLUNSAT(UUU); LM=2:ALLUNSAT(UUU); L*M=4:ALLUNSAT(UUU) | M=1:PASS(S??) | M=1:PASS(UUS) | EXCLUDED(L) | cadical195 4s |
| 3 | 13,10,7 | 24 | 8/2 | 6 | 0 | N,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(USU); LM=1tau4:PASS(S??); LDM=2:UNDEC(TTT); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(UUS) | CAND | kissat404 2s |
| 3 | 13,15,2 | 24 | 8/2 | 6 | 0 | N,d | SSS | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LM=1tau4:PASS(S??); LDM=2:UNDEC(TTT); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 10s |
| 3 | 14,10,0 | 24 | 24/0 | 6 | 0 | N,d | S?? | PASS | LDM=1:PASS(SSS); LM=1tau20:PASS(S??); LM=1tau16:PASS(S??); LM=1tau8:PASS(S??); LM=1tau12:PASS(S??); LM=1tau4:PASS(S??); LDM=2:UNDEC(TTT); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 2s |
| 3 | 15,12,9 | 24 | 8/2 | 6 | 1 | N,d | SSU | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(US?) | M=1:ALLUNSAT(UUU) | CAND | cadical195 4s |
| 3 | 15,13,2 | 24 | 8/2 | 6 | 0 | N,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(SSS); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(UUS) | CAND | kissat404 2s |
| 3 | 16,11,3 | 24 | 24/0 | 6 | 0 | N,d | S?? | PASS | LDM=1:PASS(USS); LM=1tau12:PASS(S??); LM=1tau16:PASS(S??); LM=1tau8:PASS(S??); LM=1tau4:PASS(S??); LM=1tau20:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 1s |
| 3 | 16,5,1 | 24 | 24/0 | 6 | 0 | N,d | S?? | PASS | LDM=1:PASS(UUS); LM=1tau20:PASS(S??); LM=1tau4:PASS(S??); LM=1tau8:PASS(S??); LM=1tau16:PASS(S??); LM=1tau12:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 2s |
| 3 | 16,5,3 | 24 | 8/2 | 6 | 0 | N,d | SSS | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | cadical195 7s |
| 3 | 16,8,0 | 24 | 8/2 | 6 | 0 | N,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(USU); LM=1tau4:PASS(S??); L*M=4:PASS(TS?) | M=1:PASS(S??) | M=1:ALLUNSAT(UUU) | CAND | kissat404 3s |
| 3 | 17,7,2 | 24 | 24/0 | 6 | 0 | N,d | S?? | PASS | LDM=1:PASS(UUS); LM=1tau4:PASS(S??); LM=1tau8:PASS(S??); LM=1tau12:PASS(S??); LM=1tau20:PASS(S??); LM=1tau16:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 1s |
| 3 | 18,10,2 | 24 | 8/2 | 6 | 0 | N,d | SUS | PASS | LrM=1:PASS(S??); LDM=1:ALLUNSAT(UUU); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | cadical195 4s |
| 3 | 5,2,1 | 24 | 24/0 | 6 | 0 | N,d | SSS | PASS | LDM=1:ALLUNSAT(UUU); LM=1tau16:ALLUNSAT(UUU); LM=1tau20:ALLUNSAT(UUU); LM=1tau12:PASS(S??); LM=1tau8:PASS(US?); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | EXCLUDED(L) | kissat404 9s |
| 3 | 8,13,3 | 24 | 8/2 | 6 | 0 | N,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(STS); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 2s |
| 3 | 8,16,0 | 24 | 8/2 | 6 | 0 | N,d | USS | PASS | LrM=1:PASS(US?); LDM=1:ALLUNSAT(UUU); LM=1tau4:PASS(S??); L*M=4:PASS(US?) | M=1:PASS(S??) | M=1:PASS(S??) | CAND | cadical195 4s |
| 3 | 8,5,5 | 24 | 8/2 | 6 | 0 | Y,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(SUS); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(US?) | CAND | kissat404 3s |
| 3 | 8,8,2 | 24 | 8/2 | 6 | 0 | Y,d | S?? | PASS | LrM=1:PASS(S??); LDM=1:PASS(SSU); LM=1tau4:PASS(S??); L*M=4:PASS(S??) | M=1:PASS(S??) | M=1:PASS(US?) | CAND | kissat404 2s |
| 3 | 9,6,3 | 24 | 8/2 | 6 | 1 | N,d | USS | PASS | LrM=1:PASS(US?); LDM=1:ALLUNSAT(UUU); LM=1tau4:PASS(S??); L*M=4:PASS(US?) | M=1:PASS(S??) | M=1:ALLUNSAT(UUU) | CAND | cadical195 4s |
| 3 | 2,0,0 | 36 | 36/0 | 9 | 0 | Y,d | US? | PASS | L*M=3:PASS(US?) | M=2:PASS(S??) | - | CAND | kissat404 21s |
| 3 | 2,2,0 | 36 | 36/0 | 9 | 0 | Y,d | US? | PASS | L*M=3:PASS(US?) | M=2:PASS(S??) | - | CAND | kissat404 10s |
| 3 | 13,5,0 | 120 | 40/1 | 30 | 0 | N,d | TTT | UNDECIDED | LrM=1:PASS(S??) | M=1:UNDECIDED(TTT) | - | UNDEC | kissat404 900s |
| 3 | 18,9,0 | 120 | 40/1 | 30 | 1 | N,d | UUU | ALLUNSAT | LrM=1:ALLUNSAT(UUU) | M=1:ALLUNSAT(UUU) | - | EXCLUDED(L) | kissat404 117s |
| 3 | 8,10,0 | 120 | 40/1 | 30 | 0 | N,d | TTT | UNDECIDED | LrM=1:PASS(US?) | M=1:UNDECIDED(TTT) | - | UNDEC | kissat404 900s |
| 4 | 10,10,2,2 | 32 | 8/1 | 8 | 0 | Y,d | S??? | PASS | LrM=1:PASS(S???); L*M=3:PASS(S???) | M=1:PASS(S???) | M=1:PASS(S???) | CAND | kissat404 13s |
| 4 | 13,4,13,0 | 32 | 8/1 | 8 | 0 | Y,d | S??? | PASS | LrM=1:PASS(S???); L*M=3:PASS(S???) | M=1:PASS(S???) | M=1:PASS(S???) | CAND | kissat404 11s |
| 4 | 17,4,9,0 | 32 | 16/2 | 8 | 1 | N,d | S??? | PASS | LrM=1:PASS(S???); L*M=3:PASS(S???) | M=1:PASS(S???) | M=1:PASS(US??) | CAND | kissat404 3s |
| 4 | 18,9,14,1 | 32 | 16/2 | 8 | 1 | N,d | S??? | PASS | LrM=1:PASS(S???); L*M=3:PASS(S???) | M=1:PASS(S???) | M=1:PASS(UUUS) | CAND | kissat404 7s |
| 4 | 9,18,9,0 | 32 | 16/2 | 8 | 2 | Y,d | UUUU | ALLUNSAT | LrM=1:ALLUNSAT(UUUU) | M=1:ALLUNSAT(UUUU) | - | EXCLUDED(L) | cadical195 12s |
| 4 | 16,16,0,0 | 48 | 48/0 | 12 | 0 | Y,d | S??? | PASS | L*M=2:UNDEC(TTTB) | M=2:UNDECIDED(TTTT) | - | UNDEC | kissat404 198s |
| 4 | 8,8,0,0 | 48 | 48/0 | 12 | 0 | Y,d | S??? | PASS | L*M=2:UNDEC(TTTB) | M=2:UNDECIDED(TTTT) | - | UNDEC | kissat404 196s |
| 5 | 10,1,17,2,0 | 4 | 4/0 | 1 | 0 | N | S???? | PASS | LDM=1:PASS(UUUUS); LDM=2:PASS(UUUUS); L*M=24:PASS(S????) | M=10:PASS(S????) | M=10:PASS(S????) | CAND | kissat404 0s |
| 5 | 16,18,8,17,1 | 4 | 4/0 | 1 | 0 | N | S???? | PASS | LDM=1:PASS(USUUU); LDM=2:PASS(USUUU); L*M=24:PASS(S????) | M=10:PASS(S????) | M=10:PASS(S????) | CAND | kissat404 0s |
| 5 | 13,4,1,10,0 | 12 | 12/0 | 3 | 0 | N | S???? | PASS | LDM=1:PASS(UUUUS); LM=1tau4:PASS(S????); LM=1tau8:PASS(S????); LDM=2:PASS(UUUUS); L*M=8:PASS(S????) | M=10:UNDECIDED(TTTTT) | - | UNDEC | kissat404 0s |
| 5 | 8,8,16,9,0 | 12 | 12/0 | 3 | 1 | N | US??? | PASS | LDM=1:PASS(UUUSU); LM=1tau8:PASS(S????); LM=1tau4:PASS(S????); LDM=2:PASS(UUUSU); L*M=8:PASS(US???) | M=10:UNDECIDED(TTTTT) | - | UNDEC | kissat404 0s |
| 5 | 17,8,18,16,1 | 20 | 4/4 | 5 | 0 | N,d | S???? | PASS | LrM=1:PASS(S????); LDM=1:PASS(UUSUS); LDM=2:UNDEC(TTTTT); L*M=5:PASS(S????) | M=2:PASS(S????) | M=2:ALLUNSAT(UUUUU) | CAND | kissat404 1s |
| 5 | 2,17,1,10,0 | 20 | 4/4 | 5 | 0 | N,d | S???? | PASS | LrM=1:PASS(US???); LDM=1:PASS(USUUS); LDM=2:UNDEC(TTTTT); L*M=5:PASS(US???) | M=2:PASS(S????) | M=2:ALLUNSAT(UUUUU) | CAND | kissat404 1s |
| 5 | 5,13,17,9,1 | 20 | 4/2 | 5 | 1 | N,d | USSSU | PASS | LrM=1:PASS(S????); LDM=1:ALLUNSAT(UUUUU); LDM=2:ALLUNSAT(UUUUU); LM=2:PASS(USSSU); L*M=5:PASS(US???) | M=2:PASS(S????) | M=2:ALLUNSAT(UUUUU) | CAND | cadical195 3s |
| 5 | 9,17,13,5,1 | 20 | 4/2 | 5 | 1 | N,d | SUUSS | PASS | LrM=1:PASS(UUS??); LDM=1:ALLUNSAT(UUUUU); LDM=2:ALLUNSAT(UUUUU); LM=2:PASS(SUUSS); L*M=5:PASS(UUUS?) | M=2:PASS(US???) | M=2:ALLUNSAT(UUUUU) | CAND | kissat404 10s |
| 5 | 17,16,18,11,4 | 40 | 8/4 | 10 | 0 | N,d | S???? | PASS | LrM=1:PASS(S????); L*M=3:UNDEC(TTTBB) | M=1:PASS(S????) | M=1:PASS(S????) | CAND | kissat404 94s |
| 5 | 2,9,6,9,1 | 40 | 8/2 | 10 | 2 | N,d | S???? | PASS | LrM=1:PASS(S????); L*M=3:PASS(S????) | M=1:PASS(S????) | M=1:ALLUNSAT(UUUUU) | CAND | kissat404 10s |
| 5 | 6,11,8,8,3 | 40 | 8/1 | 10 | 0 | N,d | S???? | PASS | LrM=1:PASS(S????); L*M=3:PASS(S????) | M=1:PASS(S????) | M=1:ALLUNSAT(UUUUU) | CAND | kissat404 12s |
| 5 | 7,14,1,2,0 | 40 | 8/4 | 10 | 0 | N,d | US??? | PASS | LrM=1:PASS(US???); L*M=3:UNDEC(UTTTB) | M=1:PASS(S????) | M=1:PASS(S????) | CAND | kissat404 52s |
| 5 | 8,8,11,6,3 | 40 | 8/2 | 10 | 0 | N,d | S???? | PASS | LrM=1:PASS(S????); L*M=3:PASS(S????) | M=1:PASS(S????) | M=1:ALLUNSAT(UUUUU) | CAND | kissat404 10s |
| 5 | 9,6,9,2,1 | 40 | 8/1 | 10 | 2 | N,d | US??? | PASS | LrM=1:PASS(US???); L*M=3:PASS(US???) | M=1:PASS(S????) | M=1:ALLUNSAT(UUUUU) | CAND | kissat404 16s |
| 5 | 10,1,4,13,0 | 60 | 12/2 | 15 | 0 | N,d | TTTTT | UNDECIDED | LrM=1:PASS(S????) | M=2:PASS(S????) | - | UNDEC | kissat404 600s |
| 5 | 10,18,10,4,4 | 60 | 12/1 | 15 | 0 | Y,d | TTTTT | UNDECIDED | LrM=1:PASS(S????) | M=2:UNDECIDED(TTTTT) | - | UNDEC | kissat404 600s |
| 5 | 8,14,14,8,0 | 60 | 12/1 | 15 | 0 | Y,d | S???? | PASS | LrM=1:PASS(US???); L*M=2:PASS(US???) | M=2:UNDECIDED(TTTTT) | - | UNDEC | kissat404 94s |
| 5 | 9,16,8,8,0 | 60 | 12/2 | 15 | 1 | N,d | TTTTT | UNDECIDED | LrM=1:PASS(S????) | M=2:PASS(TS???) | - | UNDEC | kissat404 600s |
| 5 | 10,8,18,9,0 | 80 | 16/3 | 20 | 1 | N,d | US??? | PASS | LrM=1:PASS(US???) | M=1:PASS(S????) | - | CAND | kissat404 45s |
| 5 | 9,18,8,10,0 | 80 | 16/3 | 20 | 1 | N,d | UUUS? | PASS | LrM=1:PASS(UUUS?) | M=1:PASS(UUS??) | - | CAND | kissat404 108s |
| 5 | 2,16,16,2,0 | 120 | 24/2 | 30 | 0 | Y,d | TTTTT | UNDECIDED | LrM=1:PASS(S????) | M=1:UNDECIDED(TTTTT) | - | UNDEC | kissat404 450s |
| 5 | 5,4,4,5,0 | 120 | 24/2 | 30 | 0 | Y,d | TTTTT | UNDECIDED | LrM=1:PASS(S????) | M=1:UNDECIDED(TTTTT) | - | UNDEC | kissat404 450s |
| 5 | 11,3,15,7,0 | 160 | 32/1 | 40 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S????) | - | - | UNDEC |  |
| 5 | 18,11,4,3,0 | 160 | 32/1 | 40 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S????) | - | - | UNDEC |  |
| 5 | 18,15,14,7,0 | 160 | 32/1 | 40 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S????) | - | - | UNDEC |  |
| 5 | 7,15,8,4,2 | 160 | 32/1 | 40 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S????) | - | - | UNDEC |  |
| 5 | 11,14,11,0,0 | 180 | 36/3 | 45 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S????) | - | - | UNDEC |  |
| 5 | 18,0,0,0,0 | 180 | 36/3 | 45 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S????) | - | - | UNDEC |  |
| 5 | 16,10,2,8,0 | 240 | 48/4 | 60 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S????) | - | - | UNDEC |  |
| 5 | 8,4,12,12,0 | 240 | 48/4 | 60 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 12,13,16,1,0 | 280 | 56/2 | 70 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 18,12,17,1,0 | 280 | 56/2 | 70 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 2,4,17,1,0 | 280 | 56/4 | 70 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 5,9,2,5,0 | 280 | 56/4 | 70 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 6,0,6,0,0 | 340 | 68/4 | 85 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 6,12,6,0,0 | 340 | 68/4 | 85 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,7,13,3,0 | 360 | 72/1 | 90 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,9,12,3,1 | 360 | 72/1 | 90 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 3,3,16,2,0 | 440 | 88/4 | 110 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,4,16,1,0 | 440 | 88/4 | 110 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 18,16,2,0,0 | 480 | 96/3 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 18,18,16,2,0 | 480 | 96/3 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 2,16,2,0,0 | 780 | 156/3 | 195 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,4,9,0,0 | 780 | 156/3 | 195 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 5,5,2,13,11,0 | 4 | 4/0 | 1 | 0 | N | US???? | PASS | LDM=1:PASS(UUSUUU); LDM=2:PASS(USSUUU); L*M=24:PASS(US????) | M=12:PASS(S?????) | M=12:PASS(S?????) | CAND | kissat404 0s |
| 6 | 7,18,13,13,16,5 | 4 | 4/0 | 1 | 0 | N | S????? | PASS | LDM=1:PASS(UUUUSU); LDM=2:PASS(UUUSSU); L*M=24:PASS(S?????) | M=12:PASS(S?????) | M=12:PASS(S?????) | CAND | kissat404 0s |
| 6 | 8,4,16,10,14,2 | 4 | 4/0 | 1 | 0 | N | SSSSSS | PASS | LDM=1:ALLUNSAT(UUUUUU); LDM=2:ALLUNSAT(UUUUUU); LM=2:PASS(SSSSSS); L*M=24:PASS(S?????) | M=12:PASS(S?????) | M=12:PASS(S?????) | CAND | cadical195 1s |
| 6 | 14,6,9,4,9,0 | 16 | 8/3 | 4 | 2 | N | S????? | PASS | LrM=1:PASS(S?????); LDM=1:PASS(SUUUUU); LM=1tau4:PASS(S?????); LDM=2:PASS(SUUUUT); L*M=6:PASS(S?????) | M=3:PASS(S?????) | M=3:ALLUNSAT(UUUUUU) | CAND | kissat404 1s |
| 6 | 17,2,18,9,10,1 | 16 | 8/3 | 4 | 1 | N | S????? | PASS | LrM=1:PASS(S?????); LDM=1:PASS(SUSUUU); LM=1tau4:PASS(S?????); LDM=2:PASS(TSTUUT); L*M=6:PASS(S?????) | M=3:PASS(S?????) | M=3:ALLUNSAT(UUUUUU) | CAND | kissat404 1s |
| 6 | 9,3,7,9,9,2 | 16 | 8/3 | 4 | 3 | N | S????? | PASS | LrM=1:PASS(S?????); LDM=1:PASS(SUUUUU); LM=1tau4:PASS(S?????); LDM=2:UNDEC(TUTUUT); L*M=6:PASS(S?????) | M=3:PASS(S?????) | M=3:ALLUNSAT(UUUUUU) | CAND | kissat404 0s |
| 6 | 9,8,17,1,16,0 | 16 | 8/3 | 4 | 1 | N | S????? | PASS | LrM=1:PASS(US????); LDM=1:PASS(UUUSUS); LM=1tau4:PASS(S?????); LDM=2:UNDEC(UUTTTT); L*M=6:PASS(US????) | M=3:PASS(S?????) | M=3:ALLUNSAT(UUUUUU) | CAND | kissat404 1s |
| 6 | 11,13,2,5,5,0 | 24 | 4/5 | 6 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????); LDM=1:PASS(SUUSUS); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:PASS(TS????) | CAND | kissat404 3s |
| 6 | 14,10,16,4,8,2 | 24 | 4/5 | 6 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????); LDM=1:PASS(STSSST); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:PASS(S?????) | CAND | kissat404 4s |
| 6 | 15,13,13,15,2,2 | 24 | 8/2 | 6 | 0 | Y,d | SSSSSS | PASS | LrM=1:PASS(S?????); LDM=1:ALLUNSAT(UUUUUU); LM=1tau4:PASS(UUUS??); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:ALLUNSAT(UUUUUU) | CAND | cadical195 8s |
| 6 | 16,12,16,2,6,2 | 24 | 8/2 | 6 | 0 | Y,d | SSSSSS | PASS | LrM=1:PASS(S?????); LDM=1:ALLUNSAT(UUUUUU); LM=1tau4:ALLUNSAT(UUUUUU); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:ALLUNSAT(UUUUUU) | EXCLUDED(L) | kissat404 17s |
| 6 | 16,13,13,18,7,5 | 24 | 4/5 | 6 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????); LDM=1:PASS(USUSSU); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:PASS(TS????) | CAND | kissat404 4s |
| 6 | 16,14,15,2,7,0 | 24 | 8/2 | 6 | 0 | N,d | SSSSSS | PASS | LrM=1:PASS(S?????); LDM=1:ALLUNSAT(UUUUUU); LM=1tau4:PASS(S?????); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:PASS(S?????) | CAND | cadical195 13s |
| 6 | 16,7,7,16,1,1 | 24 | 24/0 | 6 | 0 | Y,d | S????? | PASS | LDM=1:PASS(USSUSS); LM=1tau8:PASS(S?????); LM=1tau12:PASS(S?????); LM=1tau20:PASS(S?????); LM=1tau16:PASS(S?????); LM=1tau4:PASS(S?????); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:PASS(TS????) | CAND | kissat404 2s |
| 6 | 17,17,2,11,11,2 | 24 | 24/0 | 6 | 0 | Y,d | S????? | PASS | LDM=1:PASS(SSUSSU); LM=1tau4:PASS(S?????); LM=1tau8:PASS(S?????); LM=1tau20:PASS(S?????); LM=1tau16:PASS(S?????); LM=1tau12:PASS(S?????); L*M=4:PASS(S?????) | M=2:PASS(S?????) | M=2:PASS(TTTS??) | CAND | kissat404 2s |
| 6 | 7,2,15,14,16,0 | 24 | 8/2 | 6 | 0 | N,d | S????? | PASS | LrM=1:PASS(US????); LDM=1:PASS(UUSSSS); LM=1tau4:PASS(S?????); L*M=4:PASS(US????) | M=2:PASS(S?????) | M=2:PASS(S?????) | CAND | kissat404 2s |
| 6 | 9,12,6,12,9,0 | 24 | 8/2 | 6 | 2 | Y,d | UUUSUU | PASS | LrM=1:PASS(UUUS??); LDM=1:ALLUNSAT(UUUUUU); LM=1tau4:PASS(S?????); L*M=4:PASS(UUUS??) | M=2:PASS(UUS???) | M=2:ALLUNSAT(UUUUUU) | CAND | kissat404 15s |
| 6 | 12,12,10,18,10,2 | 36 | 12/4 | 9 | 0 | N | S????? | PASS | LrM=1:PASS(S?????); L*M=3:PASS(S?????) | - | - | UNDEC | kissat404 15s |
| 6 | 8,16,6,6,8,0 | 36 | 12/4 | 9 | 0 | N | US???? | PASS | LrM=1:PASS(US????); L*M=3:PASS(US????) | - | - | UNDEC | kissat404 18s |
| 6 | 18,18,10,18,8,0 | 44 | 44/0 | 11 | 0 | N | S????? | PASS | - | - | - | UNDEC | kissat404 21s |
| 6 | 8,0,10,18,0,0 | 44 | 44/0 | 11 | 0 | N | S????? | PASS | - | - | - | UNDEC | kissat404 58s |
| 6 | 10,10,0,0,0,0 | 48 | 24/3 | 12 | 0 | Y,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 127s |
| 6 | 10,8,18,8,10,0 | 48 | 8/5 | 12 | 0 | Y,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:ALLUNSAT(UUUUUU) | CAND | kissat404 7s |
| 6 | 10,9,18,2,17,1 | 48 | 8/1 | 12 | 1 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(TUTTS?) | CAND | kissat404 15s |
| 6 | 10,9,8,18,9,0 | 48 | 48/0 | 12 | 2 | N,d | S????? | PASS | L*M=2:UNDEC(TTTBBB) | M=1:PASS(S?????) | M=1:PASS(UUS???) | CAND | kissat404 60s |
| 6 | 12,12,0,8,8,0 | 48 | 24/3 | 12 | 0 | Y,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 46s |
| 6 | 12,14,17,18,3,0 | 48 | 24/3 | 12 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 56s |
| 6 | 13,9,7,8,11,3 | 48 | 8/5 | 12 | 1 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(UUS???) | CAND | kissat404 32s |
| 6 | 15,18,6,4,1,0 | 48 | 24/3 | 12 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(TUS???) | CAND | kissat404 135s |
| 6 | 15,6,5,16,4,2 | 48 | 24/3 | 12 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 163s |
| 6 | 15,7,10,11,9,5 | 48 | 8/5 | 12 | 1 | N,d | US???? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(US????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 72s |
| 6 | 15,7,3,3,14,0 | 48 | 24/3 | 12 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(TS????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 76s |
| 6 | 16,1,17,8,9,0 | 48 | 8/1 | 12 | 1 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 16s |
| 6 | 16,14,14,16,0,0 | 48 | 8/5 | 12 | 0 | Y,d | TTS??? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 506s |
| 6 | 17,16,17,0,4,0 | 48 | 16/4 | 12 | 0 | Y,d | TS???? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(TS????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 300s |
| 6 | 18,18,2,4,4,2 | 48 | 8/5 | 12 | 0 | Y,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(TS????) | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 75s |
| 6 | 9,18,9,9,9,0 | 48 | 16/4 | 12 | 4 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:ALLUNSAT(UUUUUU) | CAND | kissat404 22s |
| 6 | 9,4,9,6,14,0 | 48 | 8/1 | 12 | 2 | N,d | US???? | PASS | LrM=1:PASS(US????); L*M=2:PASS(US????) | M=1:PASS(S?????) | M=1:PASS(TUUS??) | CAND | kissat404 19s |
| 6 | 9,9,7,3,9,2 | 48 | 8/1 | 12 | 3 | N,d | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | M=1:PASS(S?????) | M=1:PASS(TTUS??) | CAND | kissat404 12s |
| 6 | 1,6,5,0,0,0 | 56 | 28/3 | 14 | 0 | N | UTS??? | PASS | LrM=1:PASS(US????); L*M=2:UNDEC(UTTTBB) | - | - | UNDEC | kissat404 341s |
| 6 | 6,15,4,17,0,0 | 56 | 28/3 | 14 | 0 | N | S????? | PASS | LrM=1:PASS(S?????); L*M=2:PASS(S?????) | - | - | UNDEC | kissat404 86s |
| 6 | 10,18,10,12,12,2 | 72 | 12/5 | 18 | 0 | N,d | S????? | PASS | LrM=1:PASS(S?????) | - | - | UNDEC | kissat404 82s |
| 6 | 8,6,6,16,8,0 | 72 | 12/5 | 18 | 0 | N,d | US???? | PASS | LrM=1:PASS(US????) | - | - | UNDEC | kissat404 51s |
| 6 | 17,4,15,6,0,0 | 84 | 28/2 | 21 | 0 | N | TTTTTU | UNDECIDED | LrM=1:PASS(S?????) | - | - | UNDEC | kissat404 481s |
| 6 | 5,6,1,0,0,0 | 84 | 28/2 | 21 | 0 | N | TTTTUT | UNDECIDED | LrM=1:PASS(S?????) | - | - | UNDEC | kissat404 483s |
| 6 | 11,12,10,10,1,0 | 108 | 36/4 | 27 | 0 | N | TTTTTT | UNDECIDED | LrM=1:PASS(S?????) | - | - | UNDEC | kissat404 540s |
| 6 | 17,4,1,2,10,0 | 108 | 36/4 | 27 | 0 | N | TTTTTT | UNDECIDED | LrM=1:PASS(S?????) | - | - | UNDEC | kissat404 540s |
| 6 | 6,6,0,0,0,0 | 192 | 64/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 9,3,3,9,0,0 | 192 | 64/4 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 1,10,10,12,11,0 | 216 | 36/5 | 54 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S?????) | - | - | UNDEC |  |
| 6 | 10,2,1,4,17,0 | 216 | 36/5 | 54 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S?????) | - | - | UNDEC |  |
| 6 | 18,10,0,8,0,0 | 264 | 44/1 | 66 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S?????) | - | - | UNDEC |  |
| 6 | 8,18,10,18,18,0 | 264 | 44/1 | 66 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S?????) | - | - | UNDEC |  |
| 6 | 13,8,14,2,5,0 | 336 | 56/5 | 84 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 18,13,11,7,15,2 | 336 | 56/5 | 84 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,16,2,16,13,0,0 | 28 | 4/3 | 7 | 0 | Y,d | S?????? | PASS | LrM=1:PASS(S??????) | M=2:PASS(S??????) | M=2:ALLUNSAT(UUUUUUU) | CAND | kissat404 2s |
| 7 | 16,2,5,18,18,5,2 | 28 | 4/3 | 7 | 0 | Y,d | S?????? | PASS | LrM=1:PASS(S??????) | M=2:PASS(S??????) | - | CAND | kissat404 2s |
| 7 | 10,10,9,8,11,8,7 | 56 | 8/6 | 14 | 1 | N,d | TTTTTTT | UNDECIDED | LrM=1:PASS(S??????) | M=1:PASS(S??????) | M=1:PASS(UTTTTUS) | UNDEC | kissat404 1400s |
| 7 | 10,11,8,8,9,10,7 | 56 | 8/6 | 14 | 1 | N,d | TTTS??? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | M=1:PASS(US?????) | CAND | kissat404 796s |
| 7 | 10,18,8,9,16,16,4 | 56 | 8/1 | 14 | 1 | N,d | S?????? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | M=1:PASS(S??????) | CAND | kissat404 125s |
| 7 | 10,9,2,2,14,8,0 | 56 | 8/1 | 14 | 1 | N,d | S?????? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | M=1:PASS(TTTS???) | CAND | kissat404 58s |
| 7 | 16,10,4,4,10,16,0 | 56 | 8/6 | 14 | 0 | Y,d | S?????? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | - | CAND | kissat404 52s |
| 7 | 16,16,1,13,6,13,1 | 56 | 8/6 | 14 | 0 | Y,d | TS????? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | - | CAND | kissat404 326s |
| 7 | 16,16,9,8,18,10,4 | 56 | 8/4 | 14 | 1 | N,d | TS????? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | - | CAND | kissat404 236s |
| 7 | 18,2,16,16,16,4,0 | 56 | 8/6 | 14 | 0 | N,d | TTTS??? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | - | CAND | kissat404 686s |
| 7 | 18,2,8,14,14,8,2 | 56 | 8/6 | 14 | 0 | Y,d | TTTTTTT | UNDECIDED | LrM=1:PASS(S??????) | M=1:PASS(S??????) | - | UNDEC | kissat404 840s |
| 7 | 4,16,16,16,2,18,0 | 56 | 8/6 | 14 | 0 | N,d | TTTTTTT | UNDECIDED | LrM=1:PASS(US?????) | M=1:PASS(S??????) | - | UNDEC | kissat404 840s |
| 7 | 7,11,12,12,11,7,0 | 56 | 8/6 | 14 | 0 | Y,d | S?????? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | - | CAND | kissat404 126s |
| 7 | 8,14,2,2,9,10,0 | 56 | 8/4 | 14 | 1 | N,d | TTS???? | PASS | LrM=1:PASS(S??????) | M=1:PASS(S??????) | - | CAND | kissat404 310s |
| 7 | 15,8,12,8,15,0,0 | 84 | 12/2 | 21 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 4,4,4,4,2,4,2 | 84 | 12/2 | 21 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 6,14,6,0,0,0,0 | 84 | 12/2 | 21 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 8,5,8,8,5,8,4 | 84 | 12/2 | 21 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 8,8,0,1,14,1,0 | 84 | 12/2 | 21 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(US?????) | - | - | UNDEC |  |
| 7 | 9,9,4,9,4,9,4 | 84 | 12/2 | 21 | 4 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 1,13,13,13,13,1,0 | 112 | 16/5 | 28 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | M=1:UNDECIDED(TTTTTTT) | - | UNDEC |  |
| 7 | 11,9,9,7,17,9,1 | 112 | 16/5 | 28 | 3 | N,d | - | NOTRUN | LrM=1:PASS(UUS????) | M=1:PASS(S??????) | - | UNDEC |  |
| 7 | 13,13,1,12,2,12,1 | 112 | 16/5 | 28 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | M=1:UNDECIDED(TTTTTTT) | - | UNDEC |  |
| 7 | 13,13,11,10,4,2,1 | 112 | 16/5 | 28 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | M=1:UNDECIDED(TTTTTTT) | - | UNDEC |  |
| 7 | 2,4,10,11,13,13,1 | 112 | 16/5 | 28 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | M=1:UNDECIDED(TTTTTTT) | - | UNDEC |  |
| 7 | 15,15,3,3,18,9,0 | 140 | 20/1 | 35 | 1 | N,d | - | NOTRUN | LrM=1:PASS(US?????) | - | - | UNDEC |  |
| 7 | 17,5,13,1,18,9,0 | 140 | 20/1 | 35 | 1 | N,d | - | NOTRUN | LrM=1:PASS(US?????) | - | - | UNDEC |  |
| 7 | 1,6,1,2,8,0,0 | 148 | 148/0 | 37 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,6,12,10,0,0,0 | 148 | 148/0 | 37 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 14,9,16,16,9,14,0 | 168 | 24/4 | 42 | 2 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 8,0,6,14,14,6,0 | 168 | 24/4 | 42 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(US?????) | - | - | UNDEC |  |
| 7 | 9,17,14,14,17,9,0 | 168 | 24/4 | 42 | 2 | Y,d | - | NOTRUN | LrM=1:PASS(UUUS???) | - | - | UNDEC |  |
| 7 | 9,18,9,0,0,0,0 | 168 | 24/4 | 42 | 2 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 9,18,9,1,4,4,1 | 168 | 24/4 | 42 | 2 | Y,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 17,11,10,9,8,7,1 | 224 | 32/3 | 56 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 7,8,9,10,11,17,1 | 224 | 32/3 | 56 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 11,13,4,1,9,0,0 | 252 | 36/3 | 63 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 12,10,17,5,15,5,0 | 252 | 36/2 | 63 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 14,18,9,15,17,9,0 | 252 | 36/3 | 63 | 2 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 9,1,4,13,11,0,0 | 252 | 36/2 | 63 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S??????) | - | - | UNDEC |  |
| 7 | 12,11,3,17,15,11,1 | 336 | 48/1 | 84 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,4,1,8,0,0,0 | 336 | 48/1 | 84 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 16,11,6,4,9,6,1 | 336 | 48/1 | 84 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 16,5,17,9,15,2,0 | 336 | 48/1 | 84 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,9,5,18,9,9,0 | 364 | 52/4 | 91 | 3 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,9,18,5,9,13,0 | 364 | 52/4 | 91 | 3 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 14,0,13,7,15,5,0 | 392 | 56/1 | 98 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 16,14,12,3,6,3,0 | 392 | 56/6 | 98 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,6,13,2,15,2,0 | 504 | 72/5 | 126 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 18,10,14,18,10,0,0 | 504 | 72/5 | 126 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,0,6,0,0,0,0 | 560 | 80/4 | 140 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 7,1,8,1,7,0,0 | 560 | 80/4 | 140 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 1,9,17,17,9,1,0 | 672 | 96/2 | 168 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 18,0,0,0,0,0,0 | 672 | 96/2 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 15,9,9,15,0,12,0 | 700 | 100/5 | 175 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 7,3,10,3,7,0,0 | 700 | 100/5 | 175 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,14,18,12,0,0,0 | 840 | 120/6 | 210 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,18,14,10,0,0,0 | 840 | 120/6 | 210 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,9,4,2,12,2,0 | 896 | 128/5 | 224 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,12,16,10,9,0,0 | 896 | 128/5 | 224 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,12,6,8,0,0,0 | 1036 | 148/5 | 259 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,2,1,6,1,0,0 | 1036 | 148/5 | 259 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,14,13,15,5,1,0 | 1316 | 188/6 | 329 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 15,5,7,13,8,0,0 | 1316 | 188/3 | 329 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,8,14,1,15,1,0 | 1316 | 188/3 | 329 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,13,7,5,15,0,0 | 1316 | 188/6 | 329 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 15,10,13,4,6,0,0 | 1904 | 272/3 | 476 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 16,7,12,7,0,0,0 | 1904 | 272/3 | 476 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,4,17,10,11,0,0 | 1904 | 272/6 | 476 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 7,12,7,16,0,0,0 | 1904 | 272/6 | 476 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 14,18,6,2,0,0,0 | 10752 | 1536/4 | 2688 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,11,6,3,0,0,0 | 10752 | 1536/4 | 2688 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,9,1,14,15,11,12,0 | 24 | 24/0 | 6 | 1 | N | S??????? | PASS | LM=1tau8:PASS(S???????); LM=1tau4:PASS(S???????); LM=1tau20:PASS(US??????); LM=1tau12:PASS(S???????); LM=1tau16:PASS(S???????) | - | - | UNDEC | kissat404 2s |
| 8 | 9,9,14,4,9,17,9,0 | 24 | 24/0 | 6 | 4 | N | S??????? | PASS | LM=1tau16:PASS(S???????); LM=1tau20:PASS(S???????); LM=1tau8:PASS(S???????); LM=1tau12:PASS(S???????); LM=1tau4:PASS(S???????) | - | - | UNDEC | kissat404 2s |
| 8 | 10,16,12,11,18,16,8,5 | 64 | 8/7 | 16 | 0 | N,d | TTTTS??? | PASS | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | CAND | kissat404 597s |
| 8 | 10,2,9,3,4,3,9,2 | 64 | 8/3 | 16 | 2 | Y,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 11,9,9,9,7,17,9,1 | 64 | 16/6 | 16 | 4 | N,d | - | NOTRUN | LrM=1:PASS(UUS?????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 12,5,12,12,5,12,1,1 | 64 | 8/3 | 16 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 14,0,5,12,0,12,5,0 | 64 | 8/7 | 16 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 15,14,14,15,4,9,9,4 | 64 | 8/3 | 16 | 2 | Y,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 16,16,1,9,10,15,2,0 | 64 | 16/6 | 16 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 16,16,11,9,11,7,5,0 | 64 | 16/6 | 16 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 17,6,6,17,1,12,12,1 | 64 | 16/6 | 16 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 18,13,6,18,6,13,18,4 | 64 | 8/7 | 16 | 0 | Y,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 3,10,9,4,9,10,3,0 | 64 | 8/3 | 16 | 2 | Y,d | - | NOTRUN | LrM=1:PASS(S???????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 7,6,2,8,13,10,2,0 | 64 | 8/7 | 16 | 0 | N,d | - | NOTRUN | LrM=1:PASS(US??????) | M=1:PASS(S???????) | - | UNDEC |  |
| 8 | 11,14,13,7,8,13,2,0 | 96 | 24/2 | 24 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S???????) | - | - | UNDEC |  |
| 8 | 12,11,15,14,1,9,17,0 | 96 | 24/2 | 24 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S???????) | - | - | UNDEC |  |
| 8 | 14,13,9,16,5,3,4,0 | 120 | 60/4 | 30 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,9,8,15,7,10,2,0 | 120 | 60/4 | 30 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 12,18,13,9,15,5,3,0 | 128 | 16/1 | 32 | 1 | N,d | - | NOTRUN | LrM=1:PASS(S???????) | - | - | UNDEC |  |
| 8 | 3,12,4,12,18,6,5,0 | 128 | 16/1 | 32 | 0 | N,d | - | NOTRUN | LrM=1:PASS(US??????) | - | - | UNDEC |  |
| 8 | 5,6,18,12,4,12,3,0 | 128 | 16/3 | 32 | 0 | N,d | - | NOTRUN | LrM=1:PASS(US??????) | - | - | UNDEC |  |
| 8 | 6,14,6,15,18,13,12,0 | 128 | 16/3 | 32 | 0 | N,d | - | NOTRUN | LrM=1:PASS(US??????) | - | - | UNDEC |  |
| 8 | 9,18,9,1,9,17,9,0 | 192 | 48/2 | 48 | 4 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,7,15,9,0,12,0,0 | 240 | 60/6 | 60 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,8,11,10,13,6,13,0 | 240 | 60/6 | 60 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 18,11,6,9,9,2,0,0 | 300 | 300/0 | 75 | 2 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,7,1,15,14,0,0,0 | 300 | 300/0 | 75 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 16,10,18,2,4,4,0,0 | 320 | 40/3 | 80 | 0 | N,d | - | NOTRUN | LrM=1:PASS(S???????) | - | - | UNDEC |  |
| 8 | 9,11,18,16,9,9,0,0 | 320 | 40/3 | 80 | 3 | N,d | - | NOTRUN | LrM=1:PASS(S???????) | - | - | UNDEC |  |
| 8 | 10,10,10,2,1,16,7,0 | 480 | 60/5 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 12,0,9,15,7,13,0,0 | 480 | 60/3 | 120 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,6,13,10,11,8,9,0 | 480 | 60/3 | 120 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,7,2,1,13,10,8,0 | 480 | 60/5 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,12,4,12,6,0,0,0 | 512 | 128/2 | 128 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 6,12,4,12,14,0,0,0 | 512 | 128/6 | 128 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,8,17,13,5,9,0,0 | 512 | 128/6 | 128 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,5,13,17,8,8,0,0 | 512 | 128/2 | 128 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,11,11,5,14,0,0,0 | 616 | 616/0 | 154 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,7,7,7,0,0,0,0 | 960 | 120/1 | 240 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,9,5,5,9,8,0,0 | 960 | 120/1 | 240 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,12,1,9,16,9,0,0 | 1216 | 304/2 | 304 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 16,12,0,12,8,0,0,0 | 1216 | 304/2 | 304 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,15,18,18,11,3,0,0 | 1216 | 152/5 | 304 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,12,13,10,7,0,0,0 | 1392 | 696/4 | 348 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,1,5,13,0,0,0,0 | 1392 | 696/4 | 348 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,15,1,7,7,0,0,0 | 2400 | 300/5 | 600 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 15,7,3,11,2,2,0,0 | 2400 | 300/5 | 600 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,5,11,11,13,0,0,0 | 2464 | 616/6 | 616 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,5,1,9,0,0,0,0 | 2784 | 696/6 | 696 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,10,13,12,2,0,0,0 | 2784 | 696/6 | 696 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |

### 7.2 clock 10 (period-8 lattices): 284 bands (all spatial periods s <= 8 enumerated; primitive words, up to rotation)

| s | V (canonical row, clock phase 0) | T | T_rot/twist | S | #9 | SM | L(M=1) rots | L(1) | L*, Lr, LD, tau-scan (M, status) | R (M) | R* (M) | class | time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 2 | 2/0 | 1 | 0 | Y,d | U | ALLUNSAT | - | M=2:ALLUNSAT(U) | - | EXCLUDED(L) | kissat404 0s |
| 1 | 12 | 2 | 2/0 | 1 | 0 | Y,d | S | PASS | - | M=2:PASS(S) | M=2:ALLUNSAT(U) | CAND | kissat404 0s |
| 1 | 18 | 2 | 2/0 | 1 | 0 | Y,d | U | ALLUNSAT | - | M=2:ALLUNSAT(U) | - | EXCLUDED(L) | kissat404 0s |
| 1 | 6 | 2 | 2/0 | 1 | 0 | Y,d | S | PASS | - | M=2:PASS(S) | M=2:ALLUNSAT(U) | CAND | kissat404 0s |
| 1 | 2 | 6 | 6/0 | 3 | 0 | Y,d | S | PASS | - | M=2:PASS(S) | M=2:PASS(S) | CAND | kissat404 0s |
| 1 | 4 | 6 | 6/0 | 3 | 0 | Y,d | S | PASS | - | M=2:PASS(S) | M=2:PASS(S) | CAND | kissat404 0s |
| 3 | 10,10,4 | 6 | 2/1 | 3 | 0 | Y,d | S?? | PASS | - | M=2:PASS(S??) | M=2:PASS(S??) | CAND | kissat404 0s |
| 3 | 10,4,4 | 6 | 6/0 | 3 | 0 | Y,d | S?? | PASS | - | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 10,6,2 | 6 | 6/0 | 3 | 0 | N,d | S?? | PASS | - | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 12,4,2 | 6 | 6/0 | 3 | 0 | N,d | S?? | PASS | - | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 12,9,6 | 6 | 2/1 | 3 | 1 | N,d | UUU | ALLUNSAT | - | M=2:ALLUNSAT(UUU) | - | EXCLUDED(L) | kissat404 0s |
| 3 | 14,2,2 | 6 | 6/0 | 3 | 0 | Y,d | S?? | PASS | - | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 14,8,8 | 6 | 2/1 | 3 | 0 | Y,d | S?? | PASS | - | M=2:PASS(S??) | M=2:PASS(S??) | CAND | kissat404 0s |
| 3 | 16,9,2 | 6 | 6/0 | 3 | 1 | N,d | S?? | PASS | - | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 18,6,6 | 6 | 6/0 | 3 | 0 | Y,d | S?? | PASS | - | M=2:PASS(S??) | M=2:PASS(S??) | CAND | kissat404 0s |
| 3 | 4,12,2 | 6 | 6/0 | 3 | 0 | N,d | S?? | PASS | - | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 6,0,0 | 6 | 6/0 | 3 | 0 | Y,d | US? | PASS | - | M=2:PASS(S??) | M=2:PASS(S??) | CAND | kissat404 0s |
| 3 | 6,10,2 | 6 | 6/0 | 3 | 0 | N,d | S?? | PASS | - | M=2:PASS(S??) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 9,12,6 | 6 | 2/1 | 3 | 1 | N,d | UUU | ALLUNSAT | - | M=2:ALLUNSAT(UUU) | - | EXCLUDED(L) | kissat404 0s |
| 3 | 9,16,2 | 6 | 6/0 | 3 | 1 | N,d | UUS | PASS | - | M=2:PASS(US?) | M=2:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 10,8,4 | 12 | 12/0 | 6 | 0 | N,d | S?? | PASS | - | M=1:PASS(S??) | M=1:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 12,6,0 | 12 | 4/2 | 6 | 0 | N,d | S?? | PASS | - | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 0s |
| 3 | 13,10,3 | 12 | 12/0 | 6 | 0 | N,d | S?? | PASS | - | M=1:PASS(S??) | M=1:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 14,4,0 | 12 | 12/0 | 6 | 0 | N,d | S?? | PASS | - | M=1:PASS(S??) | M=1:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 16,2,0 | 12 | 12/0 | 6 | 0 | N,d | S?? | PASS | - | M=1:PASS(S??) | M=1:ALLUNSAT(UUU) | CAND | kissat404 0s |
| 3 | 18,0,0 | 12 | 4/2 | 6 | 0 | Y,d | S?? | PASS | - | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 0s |
| 3 | 18,9,0 | 12 | 4/2 | 6 | 1 | N,d | S?? | PASS | - | M=1:PASS(S??) | M=1:PASS(S??) | CAND | kissat404 0s |
| 3 | 6,12,0 | 12 | 4/2 | 6 | 0 | N,d | US? | PASS | - | M=1:PASS(S??) | M=1:PASS(US?) | CAND | kissat404 1s |
| 3 | 2,0,0 | 18 | 18/0 | 9 | 0 | Y,d | S?? | PASS | - | M=2:PASS(S??) | - | CAND | kissat404 4s |
| 3 | 6,2,2 | 18 | 18/0 | 9 | 0 | Y,d | S?? | PASS | - | M=2:PASS(S??) | - | CAND | kissat404 1s |
| 3 | 10,4,0 | 36 | 12/1 | 18 | 0 | N,d | S?? | PASS | - | M=1:PASS(S??) | - | CAND | kissat404 4s |
| 3 | 4,9,0 | 36 | 12/1 | 18 | 1 | N,d | UUS | PASS | - | M=1:PASS(S??) | - | CAND | kissat404 3s |
| 3 | 9,4,0 | 36 | 12/2 | 18 | 1 | N,d | UTS | PASS | - | M=1:PASS(S??) | - | CAND | kissat404 111s |
| 3 | 9,8,0 | 36 | 12/2 | 18 | 1 | N,d | UTT | UNDECIDED | - | M=1:PASS(S??) | - | UNDEC | kissat404 201s |
| 4 | 11,17,7,1 | 4 | 2/2 | 2 | 0 | N | S??? | PASS | - | M=4:PASS(S???) | M=4:ALLUNSAT(UUUU) | CAND | kissat404 0s |
| 4 | 7,17,11,1 | 8 | 2/1 | 4 | 0 | N,d | S??? | PASS | - | M=2:PASS(S???) | M=2:PASS(S???) | CAND | kissat404 0s |
| 4 | 9,18,9,0 | 8 | 8/0 | 4 | 2 | Y,d | UUUU | ALLUNSAT | - | M=2:ALLUNSAT(UUUU) | - | EXCLUDED(L) | kissat404 0s |
| 4 | 10,10,2,2 | 16 | 4/1 | 8 | 0 | Y,d | S??? | PASS | - | M=1:PASS(S???) | M=1:PASS(S???) | CAND | kissat404 2s |
| 4 | 16,16,8,8 | 16 | 4/1 | 8 | 0 | Y,d | S??? | PASS | - | M=1:PASS(S???) | M=1:PASS(S???) | CAND | kissat404 1s |
| 4 | 4,4,2,2 | 16 | 4/1 | 8 | 0 | Y,d | S??? | PASS | - | M=1:PASS(S???) | M=1:ALLUNSAT(UUUU) | CAND | kissat404 1s |
| 4 | 6,10,6,2 | 16 | 4/1 | 8 | 0 | Y,d | S??? | PASS | - | M=1:PASS(S???) | M=1:ALLUNSAT(UUUU) | CAND | kissat404 1s |
| 4 | 13,13,1,1 | 48 | 12/1 | 24 | 0 | Y,d | TTTT | UNDECIDED | - | - | - | UNDEC | kissat404 400s |
| 4 | 14,1,10,1 | 48 | 12/1 | 24 | 0 | Y,d | TTTT | UNDECIDED | - | - | - | UNDEC | kissat404 400s |
| 4 | 4,6,2,0 | 48 | 24/2 | 24 | 0 | N,d | S??? | PASS | - | - | - | UNDEC | kissat404 31s |
| 4 | 9,12,3,0 | 48 | 24/2 | 24 | 1 | N,d | UUUS | PASS | - | - | - | UNDEC | kissat404 58s |
| 5 | 5,15,8,7,1 | 4 | 4/0 | 2 | 0 | N | S???? | PASS | - | M=5:PASS(S????) | M=5:PASS(S????) | CAND | kissat404 0s |
| 5 | 11,10,17,9,1 | 10 | 10/0 | 5 | 1 | N,d | S???? | PASS | - | M=2:PASS(S????) | M=2:PASS(S????) | CAND | kissat404 0s |
| 5 | 12,11,16,3,0 | 10 | 10/0 | 5 | 0 | N,d | S???? | PASS | - | M=2:PASS(S????) | M=2:PASS(S????) | CAND | kissat404 0s |
| 5 | 14,4,16,9,2 | 10 | 2/2 | 5 | 1 | N,d | US??? | PASS | - | M=2:PASS(S????) | M=2:ALLUNSAT(UUUUU) | CAND | kissat404 0s |
| 5 | 15,4,15,1,1 | 10 | 2/2 | 5 | 0 | Y,d | S???? | PASS | - | M=2:PASS(S????) | M=2:ALLUNSAT(UUUUU) | CAND | kissat404 0s |
| 5 | 17,16,16,17,0 | 10 | 10/0 | 5 | 0 | Y,d | S???? | PASS | - | M=2:PASS(S????) | M=2:PASS(S????) | CAND | kissat404 0s |
| 5 | 17,17,3,14,3 | 10 | 2/2 | 5 | 0 | Y,d | S???? | PASS | - | M=2:PASS(S????) | M=2:ALLUNSAT(UUUUU) | CAND | kissat404 0s |
| 5 | 7,8,7,1,1 | 10 | 10/0 | 5 | 0 | Y,d | S???? | PASS | - | M=2:PASS(S????) | M=2:PASS(S????) | CAND | kissat404 0s |
| 5 | 9,11,6,7,0 | 10 | 10/0 | 5 | 1 | N,d | S???? | PASS | - | M=2:PASS(S????) | M=2:PASS(S????) | CAND | kissat404 0s |
| 5 | 9,16,4,14,2 | 10 | 2/2 | 5 | 1 | N,d | UUUS? | PASS | - | M=2:PASS(UUS??) | M=2:ALLUNSAT(UUUUU) | CAND | kissat404 1s |
| 5 | 9,17,10,11,1 | 10 | 10/0 | 5 | 1 | N,d | S???? | PASS | - | M=2:PASS(US???) | M=2:PASS(US???) | CAND | kissat404 0s |
| 5 | 15,7,9,11,3 | 20 | 4/4 | 10 | 1 | N,d | S???? | PASS | - | M=1:PASS(S????) | M=1:PASS(S????) | CAND | kissat404 6s |
| 5 | 7,8,15,5,1 | 20 | 4/3 | 10 | 0 | N,d | S???? | PASS | - | M=1:PASS(S????) | M=1:PASS(S????) | CAND | kissat404 4s |
| 5 | 17,12,17,1,1 | 30 | 6/1 | 15 | 0 | Y,d | S???? | PASS | - | - | - | UNDEC | kissat404 4s |
| 5 | 17,17,1,6,1 | 30 | 6/1 | 15 | 0 | Y,d | S???? | PASS | - | - | - | UNDEC | kissat404 7s |
| 5 | 2,6,2,0,0 | 30 | 30/0 | 15 | 0 | Y,d | S???? | PASS | - | - | - | UNDEC | kissat404 42s |
| 5 | 6,14,6,0,0 | 30 | 30/0 | 15 | 0 | Y,d | US??? | PASS | - | - | - | UNDEC | kissat404 100s |
| 5 | 1,10,1,0,0 | 60 | 12/2 | 30 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 10,4,6,6,0 | 60 | 12/2 | 30 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 12,6,16,9,2 | 60 | 12/2 | 30 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 15,12,12,15,0 | 60 | 12/2 | 30 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 3,17,17,3,2 | 60 | 12/2 | 30 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 3,9,14,9,1 | 60 | 12/1 | 30 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 6,12,10,6,0 | 60 | 12/2 | 30 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 6,6,0,6,0 | 60 | 12/2 | 30 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,13,5,9,0 | 60 | 12/3 | 30 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,14,9,3,1 | 60 | 12/3 | 30 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,9,8,1,0 | 60 | 12/1 | 30 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 6,12,18,9,0 | 130 | 26/1 | 65 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,18,12,6,0 | 130 | 26/1 | 65 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 18,18,0,0,0 | 180 | 36/1 | 90 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 7,9,14,3,0 | 280 | 56/1 | 140 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,3,4,5,0 | 280 | 56/1 | 140 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 10,5,15,8,13,3 | 4 | 2/3 | 2 | 0 | N | S????? | PASS | - | M=6:PASS(S?????) | M=6:PASS(S?????) | CAND | kissat404 0s |
| 6 | 12,14,7,17,17,5 | 4 | 2/3 | 2 | 0 | N | S????? | PASS | - | M=6:PASS(S?????) | M=6:PASS(S?????) | CAND | kissat404 0s |
| 6 | 13,6,4,11,1,1 | 4 | 2/3 | 2 | 0 | N | S????? | PASS | - | M=6:PASS(S?????) | M=6:PASS(S?????) | CAND | kissat404 0s |
| 6 | 5,9,6,8,7,1 | 4 | 4/0 | 2 | 1 | N | S????? | PASS | - | M=6:PASS(S?????) | M=6:PASS(S?????) | CAND | kissat404 0s |
| 6 | 10,9,14,9,7,2 | 6 | 2/4 | 3 | 2 | N | S????? | PASS | - | M=4:PASS(S?????) | M=4:ALLUNSAT(UUUUUU) | CAND | kissat404 0s |
| 6 | 11,4,6,13,1,1 | 6 | 2/2 | 3 | 0 | N | S????? | PASS | - | M=4:PASS(S?????) | M=4:PASS(S?????) | CAND | kissat404 0s |
| 6 | 13,8,15,5,10,3 | 6 | 2/2 | 3 | 0 | N | S????? | PASS | - | M=4:PASS(S?????) | M=4:ALLUNSAT(UUUUUU) | CAND | kissat404 0s |
| 6 | 17,17,7,14,12,5 | 6 | 2/2 | 3 | 0 | N | S????? | PASS | - | M=4:PASS(S?????) | M=4:PASS(S?????) | CAND | kissat404 0s |
| 6 | 9,11,16,8,9,4 | 6 | 2/4 | 3 | 2 | N | S????? | PASS | - | M=4:PASS(UUS???) | M=4:ALLUNSAT(UUUUUU) | CAND | kissat404 0s |
| 6 | 7,8,6,9,5,1 | 12 | 4/4 | 6 | 1 | N,d | S????? | PASS | - | M=2:PASS(S?????) | M=2:PASS(S?????) | CAND | kissat404 0s |
| 6 | 7,9,14,9,10,2 | 12 | 2/1 | 6 | 2 | N,d | S????? | PASS | - | M=2:PASS(S?????) | M=2:ALLUNSAT(UUUUUU) | CAND | kissat404 0s |
| 6 | 9,15,9,9,9,3 | 12 | 4/2 | 6 | 4 | N,d | UUUUS? | PASS | - | M=2:PASS(UUUS??) | M=2:ALLUNSAT(UUUUUU) | CAND | kissat404 1s |
| 6 | 9,17,17,9,1,1 | 12 | 4/2 | 6 | 2 | Y,d | S????? | PASS | - | M=2:PASS(US????) | M=2:ALLUNSAT(UUUUUU) | CAND | kissat404 0s |
| 6 | 9,8,16,11,9,4 | 12 | 2/1 | 6 | 2 | N,d | US???? | PASS | - | M=2:PASS(S?????) | M=2:ALLUNSAT(UUUUUU) | CAND | kissat404 1s |
| 6 | 9,9,9,15,9,3 | 12 | 4/2 | 6 | 4 | N,d | UUS??? | PASS | - | M=2:PASS(US????) | M=2:ALLUNSAT(UUUUUU) | CAND | kissat404 1s |
| 6 | 13,8,18,14,17,4 | 18 | 6/4 | 9 | 0 | N | S????? | PASS | - | - | - | UNDEC | kissat404 2s |
| 6 | 4,1,14,5,10,0 | 18 | 6/4 | 9 | 0 | N | S????? | PASS | - | - | - | UNDEC | kissat404 2s |
| 6 | 12,9,17,6,9,1 | 24 | 4/5 | 12 | 2 | N,d | S????? | PASS | - | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 37s |
| 6 | 13,9,3,15,9,1 | 24 | 12/3 | 12 | 2 | N,d | US???? | PASS | - | M=1:PASS(S?????) | M=1:PASS(UUS???) | CAND | kissat404 6s |
| 6 | 14,2,12,5,4,1 | 24 | 12/3 | 12 | 0 | N,d | S????? | PASS | - | M=1:PASS(S?????) | M=1:ALLUNSAT(UUUUUU) | CAND | kissat404 1s |
| 6 | 15,9,5,17,9,3 | 24 | 12/3 | 12 | 2 | N,d | S????? | PASS | - | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 15s |
| 6 | 2,1,11,17,5,0 | 24 | 8/4 | 12 | 0 | N,d | S????? | PASS | - | M=1:PASS(S?????) | M=1:PASS(US????) | CAND | kissat404 8s |
| 6 | 5,17,11,1,2,0 | 24 | 8/4 | 12 | 0 | N,d | US???? | PASS | - | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 8s |
| 6 | 8,6,4,8,2,0 | 24 | 12/3 | 12 | 0 | N,d | US???? | PASS | - | M=1:PASS(S?????) | M=1:ALLUNSAT(UUUUUU) | CAND | kissat404 3s |
| 6 | 9,15,15,9,3,3 | 24 | 4/5 | 12 | 2 | Y,d | S????? | PASS | - | M=1:PASS(S?????) | M=1:PASS(S?????) | CAND | kissat404 7s |
| 6 | 10,5,14,1,4,0 | 36 | 6/5 | 18 | 0 | N,d | TS???? | PASS | - | - | - | UNDEC | kissat404 128s |
| 6 | 17,12,17,0,0,0 | 36 | 36/0 | 18 | 0 | Y,d | TS???? | PASS | - | - | - | UNDEC | kissat404 161s |
| 6 | 17,14,18,8,13,4 | 36 | 6/5 | 18 | 0 | N,d | TTS??? | PASS | - | - | - | UNDEC | kissat404 228s |
| 6 | 7,1,10,1,7,0 | 36 | 36/0 | 18 | 0 | Y,d | S????? | PASS | - | - | - | UNDEC | kissat404 90s |
| 6 | 10,4,2,8,0,0 | 48 | 48/0 | 24 | 0 | N,d | TTTTTT | UNDECIDED | - | - | - | UNDEC | kissat404 600s |
| 6 | 12,15,12,9,0,0 | 48 | 48/0 | 24 | 1 | N,d | TTTTUS | PASS | - | - | - | UNDEC | kissat404 467s |
| 6 | 12,6,18,10,8,0 | 48 | 24/3 | 24 | 0 | N,d | TTTUTT | UNDECIDED | - | - | - | UNDEC | kissat404 504s |
| 6 | 14,4,18,12,6,0 | 48 | 24/3 | 24 | 0 | N,d | TTTTTT | UNDECIDED | - | - | - | UNDEC | kissat404 600s |
| 6 | 18,11,13,5,7,0 | 48 | 16/2 | 24 | 0 | N,d | TUTTTT | UNDECIDED | - | - | - | UNDEC | kissat404 505s |
| 6 | 8,2,4,10,0,0 | 48 | 48/0 | 24 | 0 | N,d | UTTTTT | UNDECIDED | - | - | - | UNDEC | kissat404 503s |
| 6 | 9,12,15,12,0,0 | 48 | 48/0 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 10,18,10,10,8,0 | 72 | 36/3 | 36 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 13,17,17,15,2,0 | 72 | 36/3 | 36 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 6,12,12,6,0,0 | 96 | 16/5 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 6,18,6,0,6,0 | 96 | 16/5 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,5,9,6,8,13,3 | 4 | 4/0 | 2 | 1 | N | S?????? | PASS | - | M=7:PASS(S??????) | M=7:PASS(S??????) | CAND | kissat404 0s |
| 7 | 3,17,10,15,9,7,0 | 6 | 6/0 | 3 | 1 | N | S?????? | PASS | - | - | - | UNDEC | kissat404 0s |
| 7 | 8,3,9,11,18,15,1 | 6 | 6/0 | 3 | 1 | N | S?????? | PASS | - | - | - | UNDEC | kissat404 0s |
| 7 | 12,9,9,6,18,9,0 | 14 | 14/0 | 7 | 3 | N,d | UUUUUUU | ALLUNSAT | - | M=2:ALLUNSAT(UUUUUUU) | - | EXCLUDED(L) | kissat404 3s |
| 7 | 13,13,0,9,16,9,0 | 14 | 2/3 | 7 | 2 | Y,d | US????? | PASS | - | M=2:PASS(S??????) | M=2:PASS(S??????) | CAND | kissat404 1s |
| 7 | 17,2,2,17,0,10,0 | 14 | 2/3 | 7 | 0 | Y,d | S?????? | PASS | - | M=2:PASS(S??????) | M=2:PASS(US?????) | CAND | kissat404 1s |
| 7 | 18,11,13,9,5,7,0 | 14 | 14/0 | 7 | 1 | N,d | S?????? | PASS | - | M=2:PASS(S??????) | M=2:ALLUNSAT(UUUUUUU) | CAND | kissat404 1s |
| 7 | 18,8,18,1,16,16,1 | 14 | 2/3 | 7 | 0 | Y,d | S?????? | PASS | - | M=2:PASS(S??????) | M=2:PASS(TS?????) | CAND | kissat404 1s |
| 7 | 4,14,17,11,9,7,1 | 14 | 2/3 | 7 | 1 | N,d | S?????? | PASS | - | M=2:PASS(S??????) | M=2:PASS(S??????) | CAND | kissat404 1s |
| 7 | 7,9,11,17,14,4,1 | 14 | 2/3 | 7 | 1 | N,d | S?????? | PASS | - | M=2:PASS(S??????) | M=2:PASS(S??????) | CAND | kissat404 0s |
| 7 | 9,18,5,5,18,9,2 | 14 | 2/3 | 7 | 2 | Y,d | UUUS??? | PASS | - | M=2:PASS(UUS????) | M=2:PASS(UUS????) | CAND | kissat404 1s |
| 7 | 13,8,6,9,5,10,3 | 28 | 4/5 | 14 | 1 | N,d | TTTUTTT | UNDECIDED | - | M=1:PASS(S??????) | M=1:ALLUNSAT(UUUUUUU) | UNDEC | kissat404 603s |
| 7 | 14,7,1,9,6,17,0 | 28 | 4/6 | 14 | 1 | N,d | S?????? | PASS | - | M=1:PASS(S??????) | M=1:PASS(S??????) | CAND | kissat404 38s |
| 7 | 17,6,9,1,7,14,0 | 28 | 4/6 | 14 | 1 | N,d | S?????? | PASS | - | M=1:PASS(S??????) | M=1:PASS(US?????) | CAND | kissat404 70s |
| 7 | 12,13,6,13,12,1,1 | 42 | 6/2 | 21 | 0 | Y,d | TTTTTTT | UNDECIDED | - | - | - | UNDEC | kissat404 700s |
| 7 | 14,1,6,10,8,8,1 | 42 | 6/3 | 21 | 0 | N,d | S?????? | PASS | - | - | - | UNDEC | kissat404 28s |
| 7 | 14,1,8,8,10,6,1 | 42 | 6/1 | 21 | 0 | N,d | S?????? | PASS | - | - | - | UNDEC | kissat404 79s |
| 7 | 14,3,9,12,12,9,3 | 42 | 6/2 | 21 | 2 | Y,d | UTTTTTU | UNDECIDED | - | - | - | UNDEC | kissat404 632s |
| 7 | 15,18,11,9,3,8,1 | 42 | 6/4 | 21 | 1 | N,d | S?????? | PASS | - | - | - | UNDEC | kissat404 27s |
| 7 | 16,5,12,12,10,4,1 | 42 | 6/3 | 21 | 0 | N,d | S?????? | PASS | - | - | - | UNDEC | kissat404 20s |
| 7 | 17,12,17,1,2,2,1 | 42 | 6/2 | 21 | 0 | Y,d | S?????? | PASS | - | - | - | UNDEC | kissat404 70s |
| 7 | 17,16,16,17,1,6,1 | 42 | 6/2 | 21 | 0 | Y,d | TTTTTTT | UNDECIDED | - | - | - | UNDEC | kissat404 700s |
| 7 | 18,0,16,1,1,16,0 | 42 | 6/2 | 21 | 0 | Y,d | TTTTS?? | PASS | - | - | - | UNDEC | kissat404 459s |
| 7 | 4,10,12,12,5,16,1 | 42 | 6/1 | 21 | 0 | N,d | TS????? | PASS | - | - | - | UNDEC | kissat404 158s |
| 7 | 4,2,14,2,4,0,0 | 42 | 6/2 | 21 | 0 | Y,d | TTTTTTT | UNDECIDED | - | - | - | UNDEC | kissat404 700s |
| 7 | 7,9,15,10,17,3,0 | 42 | 6/4 | 21 | 1 | N,d | UUUUS?? | PASS | - | - | - | UNDEC | kissat404 59s |
| 7 | 12,11,17,8,10,7,1 | 56 | 8/5 | 28 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,5,17,7,10,2,1 | 56 | 8/5 | 28 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,16,13,9,9,6,1 | 70 | 10/6 | 35 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,1,15,8,16,7,0 | 70 | 10/3 | 35 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 7,16,8,15,1,13,0 | 70 | 10/6 | 35 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,15,12,9,8,3,1 | 70 | 10/3 | 35 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,1,8,10,10,8,1 | 112 | 16/3 | 56 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 14,14,0,0,14,0,0 | 112 | 16/3 | 56 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 18,10,18,4,9,4,0 | 112 | 16/1 | 56 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 18,14,9,14,0,8,0 | 112 | 16/5 | 56 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 1,17,12,17,1,0,0 | 126 | 126/0 | 63 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,4,4,4,13,1,1 | 126 | 18/6 | 63 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 14,0,2,16,16,2,0 | 126 | 18/6 | 63 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 7,12,4,12,7,0,0 | 126 | 126/0 | 63 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,10,12,12,10,4,2 | 140 | 20/2 | 70 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,14,4,10,10,0,0 | 168 | 24/1 | 84 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,11,11,13,2,3,0 | 168 | 24/1 | 84 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 14,17,14,17,14,1,1 | 168 | 24/1 | 84 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 15,15,0,9,6,9,0 | 168 | 24/1 | 84 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,18,8,18,9,3,0 | 168 | 24/1 | 84 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,5,13,17,1,2,0 | 168 | 24/1 | 84 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 5,1,1,5,0,0,0 | 168 | 24/1 | 84 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,14,10,14,8,0,0 | 168 | 24/1 | 84 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 18,15,14,8,9,2,0 | 280 | 40/4 | 140 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,6,1,10,1,2,0 | 280 | 40/4 | 140 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,0,0,0,0,0,0 | 280 | 40/4 | 140 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,18,18,18,6,0,0 | 280 | 40/4 | 140 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 5,16,9,3,6,2,0 | 336 | 48/2 | 168 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,8,11,18,4,1,1 | 336 | 48/2 | 168 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,10,12,0,0,0,0 | 504 | 72/3 | 252 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,13,6,6,13,9,0 | 504 | 72/3 | 252 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,13,9,1,14,2,0 | 532 | 76/2 | 266 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 5,18,9,15,8,2,0 | 532 | 76/2 | 266 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,9,15,18,17,1,0 | 1064 | 152/4 | 532 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 5,13,18,17,9,1,0 | 1064 | 152/4 | 532 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 7,9,13,5,1,0,0 | 1344 | 192/1 | 672 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,5,9,12,3,0,0 | 1344 | 192/1 | 672 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,9,18,1,4,0,0 | 1526 | 218/1 | 763 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,1,18,9,13,0,0 | 1526 | 218/2 | 763 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,10,11,17,11,1,0 | 1526 | 218/2 | 763 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,2,4,2,2,2,0 | 1526 | 218/1 | 763 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,10,15,7,4,9,18,2 | 2 | 2/0 | 1 | 1 | N | S??????? | PASS | - | M=16:PASS(S???????) | - | CAND | kissat404 0s |
| 8 | 16,5,8,3,11,14,9,0 | 2 | 2/0 | 1 | 1 | N | S??????? | PASS | - | M=16:PASS(S???????) | - | CAND | kissat404 0s |
| 8 | 9,6,8,13,9,12,10,5 | 4 | 2/4 | 2 | 2 | N | US?????? | PASS | - | M=8:PASS(S???????) | - | CAND | kissat404 0s |
| 8 | 14,2,7,17,4,16,11,1 | 6 | 6/0 | 3 | 0 | N | S??????? | PASS | - | - | - | UNDEC | kissat404 0s |
| 8 | 10,12,9,13,8,6,9,5 | 16 | 2/3 | 8 | 2 | N,d | S??????? | PASS | - | M=2:PASS(S???????) | - | CAND | kissat404 3s |
| 8 | 18,9,4,7,15,10,13,2 | 16 | 2/7 | 8 | 1 | N,d | S??????? | PASS | - | M=2:PASS(S???????) | - | CAND | kissat404 2s |
| 8 | 9,14,11,3,8,5,16,0 | 16 | 2/7 | 8 | 1 | N,d | UUUS???? | PASS | - | M=2:PASS(US??????) | - | CAND | kissat404 2s |
| 8 | 15,14,12,17,0,11,15,0 | 24 | 6/6 | 12 | 0 | N | S??????? | PASS | - | - | - | UNDEC | kissat404 3s |
| 8 | 16,1,14,2,6,5,16,0 | 24 | 6/6 | 12 | 0 | N | S??????? | PASS | - | - | - | UNDEC | kissat404 13s |
| 8 | 4,8,11,10,7,12,8,0 | 30 | 30/0 | 15 | 0 | N | S??????? | PASS | - | - | - | UNDEC | kissat404 23s |
| 8 | 8,6,0,2,16,16,0,0 | 30 | 30/0 | 15 | 0 | N | US?????? | PASS | - | - | - | UNDEC | kissat404 20s |
| 8 | 1,15,10,10,11,9,1,0 | 32 | 8/6 | 16 | 1 | N,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 44s |
| 8 | 11,17,18,18,7,1,0,0 | 32 | 32/0 | 16 | 0 | N,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 16s |
| 8 | 11,7,18,12,1,17,6,0 | 32 | 4/7 | 16 | 0 | N,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 60s |
| 8 | 13,10,14,15,5,8,4,3 | 32 | 4/7 | 16 | 0 | N,d | TTTTTTTT | UNDECIDED | - | M=1:PASS(S???????) | - | UNDEC | kissat404 800s |
| 8 | 17,11,4,18,1,7,14,0 | 32 | 4/7 | 16 | 0 | N,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 44s |
| 8 | 17,15,16,16,15,17,0,0 | 32 | 4/3 | 16 | 0 | Y,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 88s |
| 8 | 17,16,17,0,15,4,15,0 | 32 | 16/4 | 16 | 0 | Y,d | TS?????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 190s |
| 8 | 17,18,17,9,7,8,8,3 | 32 | 8/6 | 16 | 1 | N,d | TTTS???? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 349s |
| 8 | 17,2,2,17,0,5,5,0 | 32 | 4/7 | 16 | 0 | Y,d | TTTTTTTT | UNDECIDED | - | M=1:PASS(S???????) | - | UNDEC | kissat404 800s |
| 8 | 17,6,9,1,7,9,5,0 | 32 | 4/7 | 16 | 2 | N,d | TTTTTTTT | UNDECIDED | - | M=1:PASS(S???????) | - | UNDEC | kissat404 800s |
| 8 | 17,8,15,4,15,8,17,0 | 32 | 8/2 | 16 | 0 | Y,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 20s |
| 8 | 18,18,1,3,2,2,3,1 | 32 | 4/3 | 16 | 0 | Y,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 52s |
| 8 | 18,3,14,3,18,1,2,1 | 32 | 16/4 | 16 | 0 | Y,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 55s |
| 8 | 18,8,18,1,7,18,7,1 | 32 | 4/7 | 16 | 0 | Y,d | TTTTS??? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 463s |
| 8 | 5,8,16,16,8,5,1,1 | 32 | 8/2 | 16 | 0 | Y,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 67s |
| 8 | 5,9,7,1,9,6,17,0 | 32 | 4/7 | 16 | 2 | N,d | UTTTTTTT | UNDECIDED | - | M=1:PASS(S???????) | - | UNDEC | kissat404 728s |
| 8 | 6,17,1,12,18,7,11,0 | 32 | 4/7 | 16 | 0 | N,d | S??????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 33s |
| 8 | 7,15,12,18,11,3,6,0 | 32 | 4/7 | 16 | 0 | N,d | TS?????? | PASS | - | M=1:PASS(S???????) | - | CAND | kissat404 159s |
| 8 | 16,12,12,4,1,16,3,0 | 36 | 18/4 | 18 | 0 | N | S??????? | PASS | - | - | - | UNDEC | kissat404 45s |
| 8 | 2,3,12,5,10,0,6,0 | 36 | 18/4 | 18 | 0 | N | S??????? | PASS | - | - | - | UNDEC | kissat404 42s |
| 8 | 14,5,9,17,4,13,9,1 | 48 | 6/5 | 24 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 16,5,6,2,14,1,16,0 | 48 | 6/7 | 24 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,12,14,15,0,15,11,0 | 48 | 6/7 | 24 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 1,9,13,4,1,15,2,0 | 96 | 12/5 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,10,0,2,8,8,2,0 | 96 | 24/6 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,3,14,14,3,8,9,0 | 96 | 12/3 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 11,3,6,6,3,11,0,0 | 96 | 12/1 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 11,9,16,7,1,8,7,0 | 96 | 12/7 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 12,12,0,0,0,0,0,0 | 96 | 24/6 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,4,15,4,15,4,13,0 | 96 | 12/1 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,7,1,14,1,7,13,0 | 96 | 12/1 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,0,0,10,6,10,0,0 | 96 | 48/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,0,2,16,14,16,2,0 | 96 | 12/1 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,0,9,18,4,18,9,0 | 96 | 24/6 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,16,15,4,15,16,14,0 | 96 | 12/1 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,9,9,4,18,12,6,0 | 96 | 48/4 | 48 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 15,15,0,9,14,14,9,0 | 96 | 12/1 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 15,4,15,0,13,8,13,0 | 96 | 24/6 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,15,1,8,7,13,11,0 | 96 | 12/5 | 48 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,17,2,9,14,9,3,1 | 96 | 12/5 | 48 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,6,8,6,17,0,14,0 | 96 | 12/1 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 18,7,5,11,10,17,3,1 | 96 | 12/5 | 48 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,15,1,4,13,9,1,0 | 96 | 12/5 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 6,18,18,18,18,6,0,0 | 96 | 24/6 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,16,16,16,16,8,0,0 | 96 | 12/1 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,18,12,4,12,18,8,0 | 96 | 48/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,13,10,12,10,13,9,0 | 96 | 12/1 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,14,9,6,11,14,5,0 | 96 | 12/3 | 48 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,3,6,10,16,3,7,0 | 96 | 12/5 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,6,9,1,2,14,2,1 | 96 | 12/1 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,8,3,14,14,3,10,0 | 96 | 12/7 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,9,17,17,9,9,1,1 | 96 | 12/1 | 48 | 4 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,6,6,10,0,0,0,0 | 144 | 144/0 | 72 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 17,10,14,13,0,15,7,0 | 144 | 18/3 | 72 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 5,9,9,5,0,0,0,0 | 144 | 144/0 | 72 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 6,0,10,5,12,3,2,0 | 144 | 18/3 | 72 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,12,4,12,10,0,0,0 | 160 | 20/7 | 80 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 12,1,15,18,6,17,3,0 | 160 | 20/3 | 80 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 16,9,4,9,11,4,13,0 | 160 | 20/3 | 80 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,8,8,2,0,2,2,0 | 160 | 20/7 | 80 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 6,15,5,9,17,4,2,2 | 160 | 20/3 | 80 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 16,16,2,0,6,8,0,0 | 240 | 30/1 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,12,7,10,11,8,4,0 | 240 | 30/1 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,10,10,0,4,18,4,0 | 288 | 36/7 | 144 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,4,5,9,16,7,2,2 | 288 | 36/7 | 144 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 16,2,18,12,18,0,6,0 | 288 | 36/3 | 144 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 3,9,12,9,3,0,0,0 | 288 | 36/7 | 144 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 4,6,0,6,10,4,2,0 | 288 | 36/7 | 144 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 5,13,13,5,0,0,0,0 | 288 | 36/7 | 144 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,11,18,14,7,11,4,0 | 288 | 36/3 | 144 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,9,16,9,9,0,6,0 | 288 | 36/7 | 144 | 4 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,8,12,14,18,10,0,0 | 348 | 174/4 | 174 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 4,0,1,9,18,3,0,0 | 348 | 174/4 | 174 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 16,18,14,14,6,6,2,0 | 360 | 90/6 | 180 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,11,14,0,5,11,1,0 | 360 | 90/6 | 180 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,5,17,18,8,13,1,0 | 544 | 68/7 | 272 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 13,11,18,11,13,0,0,0 | 608 | 76/1 | 304 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 3,9,9,9,9,3,0,0 | 608 | 76/1 | 304 | 4 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 1,11,5,0,14,11,2,0 | 720 | 90/5 | 360 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,6,14,17,8,3,2,0 | 720 | 90/5 | 360 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 12,10,10,14,2,0,0,0 | 960 | 960/0 | 480 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 5,13,10,16,15,1,0,0 | 960 | 960/0 | 480 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,18,14,12,8,2,0,0 | 1392 | 174/5 | 696 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 3,18,9,1,0,4,0,0 | 1392 | 174/5 | 696 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 1,9,9,3,2,0,0,0 | 2200 | 550/6 | 1100 | 2 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,1,16,9,9,3,0,0 | 2200 | 550/6 | 1100 | 2 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,3,9,9,1,0,0,0 | 4400 | 550/7 | 2200 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 5,18,5,5,14,1,0,0 | 4400 | 550/7 | 2200 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |

### 7.3 clock 00001110001 (p11): 161 bands (all spatial periods s <= 8 enumerated; primitive words, up to rotation)

| s | V (canonical row, clock phase 0) | T | T_rot/twist | S | #9 | SM | L(M=1) rots | L(1) | L*, Lr, LD, tau-scan (M, status) | R (M) | R* (M) | class | time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 11 | 11/0 | 4 | 0 | Y,d | U | ALLUNSAT | - | M=1:ALLUNSAT(U) | - | EXCLUDED(L) | kissat404 0s |
| 1 | 18 | 11 | 11/0 | 4 | 0 | Y,d | U | ALLUNSAT | - | M=1:ALLUNSAT(U) | - | EXCLUDED(L) | kissat404 0s |
| 1 | 6 | 22 | 22/0 | 8 | 0 | Y,d | S | PASS | - | M=1:PASS(S) | - | CAND | kissat404 2s |
| 1 | 2 | 66 | 66/0 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 16,9,2 | 33 | 11/1 | 12 | 1 | N,d | UUS | PASS | - | M=1:PASS(US?) | - | CAND | kissat404 4s |
| 3 | 18,9,9 | 33 | 11/1 | 12 | 2 | Y,d | S?? | PASS | - | M=1:PASS(US?) | - | CAND | kissat404 7s |
| 3 | 9,16,2 | 33 | 11/1 | 12 | 1 | N,d | US? | PASS | - | M=1:PASS(S??) | - | CAND | kissat404 3s |
| 3 | 9,9,0 | 33 | 11/1 | 12 | 2 | Y,d | US? | PASS | - | M=1:PASS(S??) | - | CAND | kissat404 6s |
| 3 | 8,7,3 | 44 | 44/0 | 16 | 0 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 8,9,1 | 44 | 44/0 | 16 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 10,10,4 | 66 | 22/2 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 10,7,7 | 66 | 22/2 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 12,9,6 | 66 | 22/2 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 15,12,9 | 66 | 22/2 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 3,3,2 | 66 | 66/0 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 4,2,2 | 66 | 66/0 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 9,12,6 | 66 | 22/2 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 9,6,3 | 66 | 22/2 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 9,9,6 | 66 | 22/2 | 24 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 18,9,0 | 132 | 44/1 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 7,8,3 | 132 | 44/2 | 48 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 3 | 9,8,1 | 132 | 44/2 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 4 | 16,16,2,2 | 22 | 11/2 | 8 | 0 | Y,d | S??? | PASS | - | M=1:PASS(S???) | - | CAND | kissat404 2s |
| 4 | 6,10,6,2 | 22 | 22/0 | 8 | 0 | Y,d | S??? | PASS | - | M=1:PASS(S???) | - | CAND | kissat404 2s |
| 4 | 8,8,4,4 | 22 | 22/0 | 8 | 0 | Y,d | S??? | PASS | - | M=1:PASS(S???) | - | CAND | kissat404 3s |
| 4 | 9,12,9,6 | 22 | 11/2 | 8 | 2 | Y,d | US?? | PASS | - | M=1:PASS(S???) | - | CAND | kissat404 3s |
| 4 | 6,10,9,5 | 44 | 22/2 | 16 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 4 | 9,10,6,5 | 44 | 22/2 | 16 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 4 | 12,12,4,4 | 132 | 66/2 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 4 | 4,8,4,0 | 132 | 66/2 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 4 | 6,6,2,2 | 132 | 66/2 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 4 | 7,14,7,0 | 132 | 66/2 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 1,6,5,0,0 | 110 | 110/0 | 40 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 11,11,7,8,5 | 110 | 22/4 | 40 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 14,9,9,9,4 | 110 | 22/1 | 40 | 3 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 5,6,1,0,0 | 110 | 110/0 | 40 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 8,7,11,11,5 | 110 | 22/3 | 40 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 8,7,7,7,7 | 110 | 22/1 | 40 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,6,9,6,6 | 110 | 22/1 | 40 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 2,5,4,1,0 | 220 | 220/0 | 80 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 7,12,7,3,1 | 220 | 220/0 | 80 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 10,12,10,5,5 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 2,7,9,4,0 | 330 | 66/2 | 120 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 4,10,8,3,3 | 330 | 66/4 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 4,8,4,2,2 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 4,9,7,2,0 | 330 | 66/4 | 120 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 5,8,5,1,1 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 6,7,7,6,0 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 6,8,6,2,2 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 7,14,14,7,2 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 8,10,4,3,3 | 330 | 66/2 | 120 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 8,16,16,8,0 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 8,6,8,5,5 | 330 | 66/3 | 120 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 5 | 9,9,3,4,3 | 330 | 66/3 | 120 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 7,11,8,11,9,2 | 22 | 22/0 | 8 | 1 | N | S????? | PASS | - | - | - | UNDEC | kissat404 3s |
| 6 | 7,14,8,6,9,4 | 22 | 22/0 | 8 | 1 | N | S????? | PASS | - | - | - | UNDEC | kissat404 1s |
| 6 | 18,18,9,9,0,0 | 33 | 11/4 | 12 | 2 | N,d | S????? | PASS | - | M=1:PASS(S?????) | - | CAND | kissat404 8s |
| 6 | 9,9,18,18,0,0 | 33 | 11/4 | 12 | 2 | N,d | US???? | PASS | - | M=1:PASS(S?????) | - | CAND | kissat404 12s |
| 6 | 4,8,10,9,4,1 | 44 | 44/0 | 16 | 1 | N | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 1,4,9,10,4,0 | 66 | 66/0 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 10,13,10,7,4,4 | 66 | 22/2 | 24 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 11,14,15,17,10,5 | 66 | 22/2 | 24 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 12,12,4,8,8,4 | 66 | 66/0 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 13,6,13,5,12,5 | 66 | 11/1 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 16,10,14,4,8,2 | 66 | 22/2 | 24 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 3,8,12,8,3,2 | 66 | 66/0 | 24 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 4,10,9,4,1,0 | 66 | 66/0 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 6,9,6,9,9,3 | 66 | 22/2 | 24 | 3 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 7,10,13,10,4,4 | 66 | 22/2 | 24 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 8,13,7,4,3,1 | 66 | 22/2 | 24 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 9,11,8,11,7,2 | 66 | 22/4 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 9,6,8,14,7,4 | 66 | 22/4 | 24 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 9,9,6,9,6,3 | 66 | 22/2 | 24 | 3 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 4,9,10,8,4,1 | 132 | 44/2 | 48 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 5,12,8,9,8,0 | 462 | 154/2 | 168 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 6 | 8,9,8,12,5,0 | 462 | 154/2 | 168 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,16,14,16,10,3,3 | 77 | 11/5 | 28 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,9,9,10,5,6,5 | 77 | 11/5 | 28 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 13,12,13,8,9,9,8 | 77 | 11/5 | 28 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,12,6,14,15,9,3 | 77 | 11/5 | 28 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,15,15,8,2,4,2 | 77 | 11/5 | 28 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,15,14,6,12,4,3 | 77 | 11/5 | 28 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 1,4,10,10,4,1,0 | 154 | 22/3 | 56 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,12,10,11,10,8,5 | 154 | 22/5 | 56 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 17,10,4,2,5,6,1 | 154 | 22/3 | 56 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 18,15,14,9,4,3,0 | 154 | 22/3 | 56 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 18,18,1,9,17,0,0 | 154 | 154/0 | 56 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,11,9,9,11,3,2 | 154 | 22/3 | 56 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,4,9,14,15,18,0 | 154 | 22/3 | 56 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,5,2,4,10,17,1 | 154 | 22/3 | 56 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,10,11,10,12,10,5 | 154 | 22/1 | 56 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,8,4,8,8,3,3 | 154 | 22/3 | 56 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,12,12,12,9,3,3 | 154 | 22/3 | 56 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,18,9,9,9,9,0 | 154 | 154/0 | 56 | 5 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 17,10,3,9,15,8,1 | 231 | 33/1 | 84 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,15,9,3,10,17,1 | 231 | 33/1 | 84 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 1,8,10,11,16,8,0 | 308 | 44/2 | 112 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,11,12,6,17,8,5 | 308 | 44/6 | 112 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,6,7,8,13,10,1 | 308 | 44/6 | 112 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,2,3,3,3,3,1 | 308 | 44/2 | 112 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,3,3,3,2,3,1 | 308 | 44/3 | 112 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,16,11,10,8,1,0 | 308 | 44/3 | 112 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 1,7,7,2,2,1,0 | 462 | 462/0 | 168 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,10,0,9,16,9,0 | 462 | 66/2 | 168 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,12,0,4,6,4,0 | 462 | 66/2 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 16,7,2,7,16,0,0 | 462 | 66/2 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 2,4,11,11,4,2,0 | 462 | 462/0 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,4,4,3,2,2,2 | 462 | 66/2 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,8,4,2,3,3,2 | 462 | 66/2 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 5,9,10,7,2,1,0 | 462 | 462/0 | 168 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,7,4,7,6,1,1 | 462 | 66/2 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 8,14,8,2,5,5,2 | 462 | 66/2 | 168 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,10,0,6,10,6,0 | 770 | 110/1 | 280 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 10,8,15,8,6,8,2 | 770 | 110/1 | 280 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 12,3,3,3,4,6,2 | 770 | 110/1 | 280 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 7,8,8,7,0,0,0 | 770 | 110/1 | 280 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 2,4,9,9,4,2,0 | 924 | 132/4 | 336 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,9,0,6,12,6,0 | 924 | 132/4 | 336 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,4,1,1,4,4,0 | 1232 | 176/3 | 448 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 4,4,7,8,4,3,0 | 1386 | 198/2 | 504 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 6,11,7,8,8,2,0 | 1386 | 198/3 | 504 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 3,12,13,13,12,3,0 | 2310 | 330/3 | 840 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,14,11,17,9,0,0 | 4774 | 682/5 | 1736 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 7 | 9,17,11,14,9,0,0 | 4774 | 682/6 | 1736 | 2 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,16,10,3,8,14,8,3 | 44 | 11/2 | 16 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,6,9,12,8,12,9,6 | 44 | 11/2 | 16 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 11,7,12,7,11,1,4,1 | 44 | 22/4 | 16 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 3,7,6,9,15,8,0,0 | 44 | 22/4 | 16 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,13,13,7,1,3,3,1 | 44 | 22/4 | 16 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,15,10,4,10,15,8,2 | 44 | 11/2 | 16 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,15,9,6,7,3,0,0 | 44 | 22/4 | 16 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,11,12,12,11,9,4,4 | 44 | 22/4 | 16 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,9,10,10,9,9,8,8 | 44 | 11/2 | 16 | 4 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,9,4,7,13,13,7,4 | 44 | 22/4 | 16 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,6,14,17,13,5,3,1 | 88 | 22/2 | 32 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 3,5,13,17,14,6,10,1 | 88 | 22/6 | 32 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 4,12,8,17,15,13,5,1 | 88 | 22/6 | 32 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 5,13,15,17,8,12,4,1 | 88 | 22/2 | 32 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 1,5,6,4,6,5,1,0 | 132 | 66/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 10,10,3,9,7,7,9,3 | 132 | 66/4 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,7,14,14,7,2,1,1 | 132 | 66/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 4,4,4,6,4,4,4,2 | 132 | 66/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 5,9,13,18,13,9,5,0 | 132 | 33/2 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,11,11,7,2,3,3,2 | 132 | 66/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,7,1,6,10,10,6,1 | 132 | 66/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,7,3,4,11,11,4,3 | 132 | 66/4 | 48 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,10,10,10,10,9,1,1 | 132 | 66/4 | 48 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 12,16,16,12,3,5,5,3 | 220 | 55/6 | 80 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 6,15,13,13,15,6,2,2 | 220 | 55/6 | 80 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 14,12,10,5,13,5,8,1 | 264 | 66/6 | 96 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,5,13,5,10,12,14,1 | 264 | 66/2 | 96 | 0 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 5,8,6,6,8,5,1,1 | 396 | 198/4 | 144 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 2,6,7,8,9,4,0,0 | 484 | 121/2 | 176 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 3,9,9,9,9,9,6,0 | 484 | 121/2 | 176 | 5 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 4,9,8,7,6,2,0,0 | 484 | 121/2 | 176 | 1 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 6,9,9,9,9,9,3,0 | 484 | 121/2 | 176 | 5 | N,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 1,10,18,10,1,0,0,0 | 528 | 264/4 | 192 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 6,12,15,18,15,12,6,0 | 528 | 264/4 | 192 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 8,12,8,12,8,0,0,0 | 528 | 264/4 | 192 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 9,10,0,10,9,0,2,0 | 528 | 264/4 | 192 | 2 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |
| 8 | 7,14,7,0,0,0,0,0 | 1452 | 726/4 | 528 | 0 | Y,d | - | NOTRUN | - | - | - | UNDEC |  |

Column SM: Y if every phase-0 row of the band is a palindromic necklace (self-mirror; together with s | S the fold closes without a centre, merged-lattice format; the R/R* tests do not apply to such a fold centre), the suffix d marks s divides S (S = overflows per T).


### Tally (M=1, tau=0, R=12)

- clock 1000 (N12 / T12 exterior): {'EXCLUDED(L)': 7, 'CAND': 94, 'UNDEC': 164}
- clock 10 (period-8 lattices): {'EXCLUDED(L)': 6, 'CAND': 101, 'UNDEC': 177}
- clock 00001110001 (p11): {'EXCLUDED(L)': 2, 'CAND': 11, 'UNDEC': 148}

### Explicit list of all bands with an ALLUNSAT result (mode, epochs M, origin tau, R; solver/encoding pairs that report it)

- L clock=00001110001 V=0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=00001110001 V=18 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=00001110001 V=0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=00001110001 V=18 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=10 V=0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=10 V=18 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=10 V=12,9,6 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=10 V=9,12,6 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=10 V=9,18,9,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=10 V=12,9,9,6,18,9,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=10 V=0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=10 V=18 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=10 V=12,9,6 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=10 V=9,12,6 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=10 V=9,18,9,0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=10 V=12,9,9,6,18,9,0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=12 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=6 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=10,4,4 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=10,6,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=10,8,4 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=12,4,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=13,10,3 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=14,2,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=14,4,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=16,2,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=16,9,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=4,12,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=6,10,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=9,16,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=11,17,7,1 M=4 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=4,4,2,2 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=6,10,6,2 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=14,4,16,9,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=15,4,15,1,1 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=17,17,3,14,3 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=9,16,4,14,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=10,9,14,9,7,2 M=4 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=13,8,15,5,10,3 M=4 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=14,2,12,5,4,1 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=7,9,14,9,10,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=8,6,4,8,2,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=9,11,16,8,9,4 M=4 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=9,15,9,9,9,3 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=9,17,17,9,1,1 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=9,8,16,11,9,4 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=9,9,9,15,9,3 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=13,8,6,9,5,10,3 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=10 V=18,11,13,9,5,7,0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc2]
- L clock=1000 V=18 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=18 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc2]
- L clock=1000 V=11,9,2 M=1 tau=8 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=11,9,2 M=1 tau=12 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=11,9,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc2]
- L clock=1000 V=18,9,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=5,2,1 M=1 tau=16 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=5,2,1 M=1 tau=20 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=9,18,9,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L clock=1000 V=16,12,16,2,6,2 M=1 tau=4 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- L* clock=1000 V=11,9,2 M=4 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- LD clock=1000 V=0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=0 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=12 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=12 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=18 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=18 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=2 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=4 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=4 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=6 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=6 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=11,9,2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=11,9,2 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=13,15,2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=15,12,9 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=15,15,0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=15,15,0 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=16,18,2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=16,2,0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=16,5,3 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=18,10,2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=18,3,3 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=18,3,3 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=5,2,1 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=8,16,0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=9,6,3 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=5,13,17,9,1 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=5,13,17,9,1 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=9,17,13,5,1 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=9,17,13,5,1 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=15,13,13,15,2,2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=16,12,16,2,6,2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=16,14,15,2,7,0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=8,4,16,10,14,2 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=8,4,16,10,14,2 M=2 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- LD clock=1000 V=9,12,6,12,9,0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- Lr clock=1000 V=18,9,0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- Lr clock=1000 V=9,18,9,0 M=1 tau=0 R=12: ALLUNSAT [kissat404/enc1]
- R clock=1000 V=0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=1000 V=18 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=1000 V=18,9,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R clock=1000 V=9,18,9,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=12 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=4 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=6 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=10,18,2 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=15,12,9 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=15,15,0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=16,8,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=18,3,3 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=9,6,3 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=17,8,18,16,1 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=2,17,1,10,0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=2,9,6,9,1 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=5,13,17,9,1 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=6,11,8,8,3 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=8,8,11,6,3 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=9,17,13,5,1 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=9,6,9,2,1 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=10,8,18,8,10,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=14,6,9,4,9,0 M=3 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=15,13,13,15,2,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=16,12,16,2,6,2 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=17,2,18,9,10,1 M=3 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=9,12,6,12,9,0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=9,18,9,9,9,0 M=1 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=9,3,7,9,9,2 M=3 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=9,8,17,1,16,0 M=3 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]
- R* clock=1000 V=13,16,2,16,13,0,0 M=2 tau=0 R=12: ALLUNSAT [cadical195/enc1, kissat404/enc1, kissat404/enc2]

### Seam sweeps (exterior | J | band; every line = one band sweep; SAT lines are listed verbatim)

| job | result |
|---|---|
| deepseam/i00004.log | SEAMBAND done V=15,15,0 Lmax=16 taus=1 rots=3 ran=12 unsat=12 timeouts=0 found=False elapsed=14s |
| deepseam/i00005.log | SEAMBAND done V=18,3,3 Lmax=16 taus=1 rots=3 ran=12 unsat=12 timeouts=0 found=False elapsed=14s |
| seam1000a/i00000.log | SEAMBAND done V=12 Lmax=12 taus=1 rots=1 ran=13 unsat=13 timeouts=0 found=False elapsed=6s |
| seam1000a/i00001.log | SEAMBAND done V=2 Lmax=12 taus=3 rots=1 ran=39 unsat=39 timeouts=0 found=False elapsed=20s |
| seam1000a/i00002.log | SEAMBAND done V=4 Lmax=12 taus=3 rots=1 ran=39 unsat=39 timeouts=0 found=False elapsed=20s |
| seam1000a/i00003.log | SEAMBAND done V=6 Lmax=12 taus=1 rots=1 ran=13 unsat=13 timeouts=0 found=False elapsed=5s |
| seam1000a/i00004.log | SEAMBAND done V=15,15,0 Lmax=12 taus=1 rots=3 ran=39 unsat=39 timeouts=0 found=False elapsed=18s |
| seam1000a/i00005.log | SEAMBAND done V=16,18,2 Lmax=12 taus=1 rots=3 ran=39 unsat=39 timeouts=0 found=False elapsed=22s |
| seam1000a/i00006.log | SEAMBAND done V=16,2,0 Lmax=12 taus=1 rots=3 ran=39 unsat=39 timeouts=0 found=False elapsed=22s |
| seam1000a/i00007.log | SEAMBAND done V=18,16,2 Lmax=12 taus=1 rots=3 ran=39 unsat=39 timeouts=0 found=False elapsed=22s |
| seam1000a/i00008.log | SEAMBAND done V=18,3,3 Lmax=12 taus=1 rots=3 ran=39 unsat=39 timeouts=0 found=False elapsed=19s |
| seam1000a/i00009.log | SEAMBAND done V=2,16,0 Lmax=12 taus=1 rots=3 ran=39 unsat=39 timeouts=0 found=False elapsed=21s |
| seam1000a/i00010.log | SEAMBAND done V=10,1,17,2,0 Lmax=12 taus=1 rots=5 ran=65 unsat=65 timeouts=0 found=False elapsed=26s |
| seam1000a/i00011.log | SEAMBAND done V=13,4,1,10,0 Lmax=12 taus=3 rots=5 ran=195 unsat=195 timeouts=0 found=False elapsed=94s |
| seam1000a/i00012.log | SEAMBAND done V=16,18,8,17,1 Lmax=12 taus=1 rots=5 ran=65 unsat=65 timeouts=0 found=False elapsed=27s |
| seam1000a/i00013.log | SEAMBAND done V=8,8,16,9,0 Lmax=12 taus=3 rots=5 ran=195 unsat=195 timeouts=0 found=False elapsed=93s |
| seam1000a/i00014.log | SEAMBAND done V=5,5,2,13,11,0 Lmax=12 taus=1 rots=6 ran=78 unsat=78 timeouts=0 found=False elapsed=40s |
| seam1000a/i00015.log | SEAMBAND done V=7,18,13,13,16,5 Lmax=12 taus=1 rots=6 ran=78 unsat=78 timeouts=0 found=False elapsed=39s |
| seam1000a/i00016.log | SEAMBAND done V=8,4,16,10,14,2 Lmax=12 taus=1 rots=6 ran=78 unsat=78 timeouts=0 found=False elapsed=44s |
| seam1000b/i00000.log | SEAMBAND done V=12 Lmax=8 taus=1 rots=1 ran=9 unsat=9 timeouts=0 found=False elapsed=3s |
| seam1000b/i00001.log | SEAMBAND done V=2 Lmax=8 taus=3 rots=1 ran=27 unsat=27 timeouts=0 found=False elapsed=9s |
| seam1000b/i00002.log | SEAMBAND done V=4 Lmax=8 taus=3 rots=1 ran=27 unsat=27 timeouts=0 found=False elapsed=9s |
| seam1000b/i00003.log | SEAMBAND done V=6 Lmax=8 taus=1 rots=1 ran=9 unsat=9 timeouts=0 found=False elapsed=3s |
| seam1000b/i00004.log | SEAMBAND done V=15,15,0 Lmax=8 taus=1 rots=3 ran=27 unsat=27 timeouts=0 found=False elapsed=8s |
| seam1000b/i00005.log | SEAMBAND done V=16,18,2 Lmax=8 taus=1 rots=3 ran=27 unsat=27 timeouts=0 found=False elapsed=9s |
| seam1000b/i00006.log | SEAMBAND done V=16,2,0 Lmax=8 taus=1 rots=3 ran=27 unsat=27 timeouts=0 found=False elapsed=9s |
| seam1000b/i00007.log | SEAMBAND done V=18,16,2 Lmax=8 taus=1 rots=3 ran=27 unsat=27 timeouts=0 found=False elapsed=9s |
| seam1000b/i00008.log | SEAMBAND done V=18,3,3 Lmax=8 taus=1 rots=3 ran=27 unsat=27 timeouts=0 found=False elapsed=8s |
| seam1000b/i00009.log | SEAMBAND done V=2,16,0 Lmax=8 taus=1 rots=3 ran=27 unsat=27 timeouts=0 found=False elapsed=9s |
| seam1000b/i00010.log | SEAMBAND done V=10,1,17,2,0 Lmax=8 taus=1 rots=5 ran=45 unsat=45 timeouts=0 found=False elapsed=13s |
| seam1000b/i00011.log | SEAMBAND done V=13,4,1,10,0 Lmax=8 taus=3 rots=5 ran=135 unsat=135 timeouts=0 found=False elapsed=42s |
| seam1000b/i00012.log | SEAMBAND done V=16,18,8,17,1 Lmax=8 taus=1 rots=5 ran=45 unsat=45 timeouts=0 found=False elapsed=13s |
| seam1000b/i00013.log | SEAMBAND done V=8,8,16,9,0 Lmax=8 taus=3 rots=5 ran=135 unsat=135 timeouts=0 found=False elapsed=42s |
| seam1000b/i00014.log | SEAMBAND done V=5,5,2,13,11,0 Lmax=8 taus=1 rots=6 ran=54 unsat=54 timeouts=0 found=False elapsed=17s |
| seam1000b/i00015.log | SEAMBAND done V=7,18,13,13,16,5 Lmax=8 taus=1 rots=6 ran=54 unsat=54 timeouts=0 found=False elapsed=17s |
| seam1000b/i00016.log | SEAMBAND done V=8,4,16,10,14,2 Lmax=8 taus=1 rots=6 ran=54 unsat=54 timeouts=0 found=False elapsed=18s |
| seam1000b/i00017.log | SEAMBAND done V=10,18,2 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=99s |
| seam1000b/i00018.log | SEAMBAND done V=11,8,5 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=79s |
| seam1000b/i00019.log | SEAMBAND budget hit: V=11,9,2 done up to Lj=8 tau=16 r=1 ran=157 unsat=157 timeouts=0 |
| seam1000b/i00020.log | SEAMBAND done V=13,10,7 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=84s |
| seam1000b/i00021.log | SEAMBAND done V=13,15,2 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=104s |
| seam1000b/i00022.log | SEAMBAND budget hit: V=14,10,0 done up to Lj=7 tau=20 r=0 ran=141 unsat=141 timeouts=0 |
| seam1000b/i00023.log | SEAMBAND done V=15,12,9 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=67s |
| seam1000b/i00024.log | SEAMBAND done V=15,13,2 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=86s |
| seam1000b/i00025.log | SEAMBAND budget hit: V=16,11,3 done up to Lj=7 tau=16 r=1 ran=139 unsat=139 timeouts=0 |
| seam1000b/i00026.log | SEAMBAND budget hit: V=16,5,1 done up to Lj=8 tau=4 r=2 ran=149 unsat=149 timeouts=0 |
| seam1000b/i00027.log | SEAMBAND done V=16,5,3 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=99s |
| seam1000b/i00028.log | SEAMBAND done V=16,8,0 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=97s |
| seam1000b/i00029.log | SEAMBAND budget hit: V=17,7,2 done up to Lj=8 tau=4 r=1 ran=148 unsat=148 timeouts=0 |
| seam1000b/i00030.log | SEAMBAND done V=18,10,2 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=59s |
| seam1000b/i00031.log | SEAMBAND budget hit: V=5,2,1 done up to Lj=8 tau=16 r=2 ran=158 unsat=158 timeouts=0 |
| seam1000b/i00032.log | SEAMBAND done V=8,13,3 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=90s |
| seam1000b/i00033.log | SEAMBAND done V=8,16,0 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=56s |
| seam1000b/i00034.log | SEAMBAND done V=8,5,5 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=100s |
| seam1000b/i00035.log | SEAMBAND done V=8,8,2 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=101s |
| seam1000b/i00036.log | SEAMBAND done V=9,6,3 Lmax=8 taus=2 rots=3 ran=54 unsat=54 timeouts=0 found=False elapsed=72s |
| seam1000b/i00037.log | SEAMBAND done V=11,13,2,5,5,0 Lmax=8 taus=1 rots=6 ran=54 unsat=54 timeouts=0 found=False elapsed=105s |
| seam1000b/i00038.log | SEAMBAND done V=14,10,16,4,8,2 Lmax=8 taus=1 rots=6 ran=54 unsat=54 timeouts=0 found=False elapsed=126s |
| seam1000b/i00039.log | SEAMBAND done V=15,13,13,15,2,2 Lmax=8 taus=2 rots=6 ran=108 unsat=108 timeouts=0 found=False elapsed=116s |
| seam1000b/i00040.log | SEAMBAND done V=16,12,16,2,6,2 Lmax=8 taus=2 rots=6 ran=108 unsat=108 timeouts=0 found=False elapsed=186s |
| seam1000b/i00041.log | SEAMBAND done V=16,13,13,18,7,5 Lmax=8 taus=1 rots=6 ran=54 unsat=54 timeouts=0 found=False elapsed=103s |
| seam1000b/i00042.log | SEAMBAND done V=16,14,15,2,7,0 Lmax=8 taus=2 rots=6 ran=108 unsat=108 timeouts=0 found=False elapsed=173s |
| seam1000b/i00043.log | SEAMBAND budget hit: V=16,7,7,16,1,1 done up to Lj=5 tau=16 r=4 ran=208 unsat=208 timeouts=0 |
| seam1000b/i00044.log | SEAMBAND budget hit: V=17,17,2,11,11,2 done up to Lj=5 tau=16 r=4 ran=208 unsat=208 timeouts=0 |
| seam1000b/i00045.log | SEAMBAND done V=7,2,15,14,16,0 Lmax=8 taus=2 rots=6 ran=108 unsat=108 timeouts=0 found=False elapsed=188s |
| seam1000b/i00046.log | SEAMBAND done V=9,12,6,12,9,0 Lmax=8 taus=2 rots=6 ran=108 unsat=108 timeouts=0 found=False elapsed=113s |
| seam1000b/i00047.log | SEAMBAND budget hit: V=17,9,1,14,15,11,12,0 done up to Lj=5 tau=4 r=7 ran=255 unsat=255 timeouts=0 |
| seam1000b/i00048.log | SEAMBAND budget hit: V=9,9,14,4,9,17,9,0 done up to Lj=5 tau=4 r=4 ran=252 unsat=252 timeouts=0 |
| seam1000c/i00000.log | SEAMBAND done V=11,8,5 Lmax=12 taus=2 rots=3 ran=24 unsat=24 timeouts=0 found=False elapsed=172s |
| seam1000c/i00001.log | SEAMBAND done V=13,10,7 Lmax=12 taus=2 rots=3 ran=24 unsat=24 timeouts=0 found=False elapsed=173s |
| seam1000c/i00005.log | SEAMBAND budget hit: V=16,5,1 done up to Lj=11 tau=0 r=0 ran=36 unsat=35 timeouts=0 |
| seam1000c/i00006.log | SEAMBAND budget hit: V=17,7,2 done up to Lj=11 tau=0 r=0 ran=36 unsat=35 timeouts=0 |
| seam1000c/i00007.log | SEAMBAND budget hit: V=8,13,3 done up to Lj=12 tau=4 r=0 ran=21 unsat=20 timeouts=0 |
| seam1000c/i00008.log | SEAMBAND done V=8,5,5 Lmax=12 taus=2 rots=3 ran=24 unsat=24 timeouts=0 found=False elapsed=200s |
| seam1000c/i00009.log | SEAMBAND budget hit: V=8,8,2 done up to Lj=12 tau=4 r=0 ran=21 unsat=21 timeouts=0 |
| seam1000c/i00010.log | SEAMBAND budget hit: V=11,13,2,5,5,0 done up to Lj=12 tau=0 r=3 ran=21 unsat=21 timeouts=0 |
| seam1000c/i00011.log | SEAMBAND budget hit: V=14,10,16,4,8,2 done up to Lj=12 tau=0 r=0 ran=18 unsat=18 timeouts=0 |
| seam1000c/i00012.log | SEAMBAND budget hit: V=16,13,13,18,7,5 done up to Lj=12 tau=0 r=3 ran=21 unsat=21 timeouts=0 |
| seam1000c/i00013.log | SEAMBAND budget hit: V=16,7,7,16,1,1 done up to Lj=9 tau=20 r=1 ran=31 unsat=31 timeouts=0 |
| seam1000c/i00014.log | SEAMBAND budget hit: V=17,17,2,11,11,2 done up to Lj=9 tau=20 r=1 ran=31 unsat=31 timeouts=0 |
| seam1000c/i00015.log | SEAMBAND budget hit: V=7,2,15,14,16,0 done up to Lj=11 tau=4 r=0 ran=30 unsat=30 timeouts=0 |
| seam1000c/i00016.log | SEAMBAND budget hit: V=17,9,1,14,15,11,12,0 done up to Lj=9 tau=20 r=3 ran=43 unsat=43 timeouts=0 |
| seam1000c/i00017.log | SEAMBAND budget hit: V=9,9,14,4,9,17,9,0 done up to Lj=9 tau=20 r=1 ran=41 unsat=41 timeouts=0 |

### Centre sweeps

| job | result |
|---|---|
| centre1000/i00000.log | CENTRE-SAT V=12 T=4 N=8 j=1 tau=0 r=0 word=[12] Lc=0: V=[12] Lc=0 m=18 j=1 N=8 vars=6536 clauses=80955 enc=0.0s | RESULT SAT time=0.1s | WITNESS_C [] |  ; CENTREBAND FOUND V=12 Lc=0 tau=0 r=0 |
| centre1000/i00001.log | CENTRE-SAT V=6 T=4 N=8 j=1 tau=0 r=0 word=[6] Lc=0: V=[6] Lc=0 m=18 j=1 N=8 vars=6536 clauses=80955 enc=0.0s | RESULT SAT time=0.0s | WITNESS_C [] |  ; CENTREBAND FOUND V=6 Lc=0 tau=0 r=0 |
| centre1000/i00002.log | CENTRE-SAT V=2 T=12 N=24 j=3 tau=0 r=0 word=[2] Lc=0: V=[2] Lc=0 m=30 j=3 N=24 vars=31944 clauses=399657 enc=0.1s | RESULT SAT time=0.2s | WITNESS_C [] |  ; CENTREBAND FOUND V=2 Lc=0 tau=0 r=0 |
| centre1000/i00003.log | CENTRE-SAT V=4 T=12 N=24 j=3 tau=0 r=0 word=[4] Lc=0: V=[4] Lc=0 m=30 j=3 N=24 vars=31944 clauses=399657 enc=0.1s | RESULT SAT time=0.3s | WITNESS_C [] |  ; CENTREBAND FOUND V=4 Lc=0 tau=0 r=0 |
| centre1000/i00004.log | CENTREBAND done V=10,18,2 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=50s |
| centre1000/i00005.log | CENTRE-SAT V=11,8,5 T=24 N=24 j=1 tau=0 r=2 word=[5, 11, 8] Lc=3: V=[5, 11, 8] Lc=3 m=12 j=1 N=24 vars=39476 clauses=493978 enc=0.1s | RESULT SAT time=1.3s | WITNESS_C [13, 2, 13] |  ; CENTREBAND FOUND V=11,8,5 Lc=3 tau=0 r=2 |
| centre1000/i00006.log | CENTREBAND budget hit V=11,9,2 Lc=5 tau=20 r=1 ran=106 unsat=106 timeouts=0 |
| centre1000/i00007.log | CENTRE-SAT V=13,10,7 T=24 N=24 j=1 tau=4 r=0 word=[13, 7, 10] Lc=3: V=[13, 7, 10] Lc=3 m=12 j=1 N=24 vars=39476 clauses=493978 enc=0.1s | RESULT SAT time=1.4s | WITNESS_C [5, 16, 5] |  ; CENTREBAND FOUND V=13,10,7 Lc=3 tau=4 r=0 |
| centre1000/i00008.log | CENTREBAND done V=13,15,2 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=41s |
| centre1000/i00009.log | CENTREBAND budget hit V=14,10,0 Lc=5 tau=12 r=2 ran=101 unsat=101 timeouts=0 |
| centre1000/i00010.log | CENTREBAND done V=15,12,9 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=64s |
| centre1000/i00011.log | CENTREBAND done V=15,13,2 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=54s |
| centre1000/i00012.log | CENTRE-SAT V=15,15,0 T=12 N=24 j=1 tau=0 r=1 word=[15, 0, 15] Lc=0: V=[15, 0, 15] Lc=0 m=12 j=1 N=24 vars=37962 clauses=475011 enc=0.1s | RESULT SAT time=0.2s | WITNESS_C [] |  ; CENTREBAND FOUND V=15,15,0 Lc=0 tau=0 r=1 |
| centre1000/i00013.log | CENTREBAND budget hit V=16,11,3 Lc=5 tau=20 r=0 ran=105 unsat=105 timeouts=0 |
| centre1000/i00014.log | CENTREBAND done V=16,18,2 T=12 N=24 j=1 Lmax=6 ran=21 unsat=21 timeouts=0 found=False elapsed=26s |
| centre1000/i00015.log | CENTREBAND done V=16,2,0 T=12 N=24 j=1 Lmax=6 ran=21 unsat=21 timeouts=0 found=False elapsed=26s |
| centre1000/i00016.log | CENTREBAND budget hit V=16,5,1 Lc=5 tau=20 r=2 ran=107 unsat=107 timeouts=0 |
| centre1000/i00017.log | CENTREBAND done V=16,5,3 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=46s |
| centre1000/i00018.log | CENTREBAND done V=16,8,0 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=54s |
| centre1000/i00019.log | CENTREBAND budget hit V=17,7,2 Lc=5 tau=20 r=0 ran=105 unsat=105 timeouts=0 |
| centre1000/i00020.log | CENTREBAND done V=18,10,2 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=59s |
| centre1000/i00021.log | CENTREBAND done V=18,16,2 T=4 N=24 j=1 Lmax=6 ran=21 unsat=21 timeouts=0 found=False elapsed=32s |
| centre1000/i00022.log | CENTRE-SAT V=18,3,3 T=12 N=24 j=1 tau=0 r=2 word=[3, 18, 3] Lc=0: V=[3, 18, 3] Lc=0 m=12 j=1 N=24 vars=37962 clauses=475011 enc=0.1s | RESULT SAT time=0.3s | WITNESS_C [] |  ; CENTREBAND FOUND V=18,3,3 Lc=0 tau=0 r=2 |
| centre1000/i00023.log | CENTREBAND done V=2,16,0 T=4 N=24 j=1 Lmax=6 ran=21 unsat=21 timeouts=0 found=False elapsed=27s |
| centre1000/i00024.log | CENTREBAND budget hit V=5,2,1 Lc=6 tau=8 r=1 ran=115 unsat=115 timeouts=0 |
| centre1000/i00025.log | CENTREBAND done V=8,13,3 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=46s |
| centre1000/i00026.log | CENTREBAND done V=8,16,0 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=52s |
| centre1000/i00027.log | CENTRE-SAT V=8,5,5 T=24 N=24 j=1 tau=0 r=2 word=[5, 8, 5] Lc=0: V=[5, 8, 5] Lc=0 m=12 j=1 N=24 vars=37962 clauses=475011 enc=0.1s | RESULT SAT time=0.3s | WITNESS_C [] |  ; CENTREBAND FOUND V=8,5,5 Lc=0 tau=0 r=2 |
| centre1000/i00028.log | CENTRE-SAT V=8,8,2 T=24 N=24 j=1 tau=0 r=1 word=[8, 2, 8] Lc=0: V=[8, 2, 8] Lc=0 m=12 j=1 N=24 vars=37962 clauses=475011 enc=0.1s | RESULT SAT time=0.3s | WITNESS_C [] |  ; CENTREBAND FOUND V=8,8,2 Lc=0 tau=0 r=1 |
| centre1000/i00029.log | CENTREBAND done V=9,6,3 T=24 N=24 j=1 Lmax=6 ran=42 unsat=42 timeouts=0 found=False elapsed=48s |

## 8. What is UNDECIDED (scope of all negative statements)
- Bands and clocks: everything is for the three clocks 1000, 10, 00001110001 and the census range s <= 8 (bands up to rotation, primitive words).  s >= 9 is not enumerated (W0, s = 9, and the p8 lattices, s = 20/48, are bands outside the census range; the census does not exclude longer bands).  No statement for other clocks.
- T bounds (L one-epoch test at origin tau = 0, R = 12, per-rotation timeout as listed): clock 1000: T <= 64 complete except s = 8 and timeouts; T in (64, 120]: s <= 6 only; T > 120: UNDECIDED (not run; the rotating-epoch test Lr has been run for T > 120 when T_rot <= 120 as far as the time box allowed, see tables); clock 10 and p11: T <= 36 complete except timeouts; 36 < T <= 60: only 22 of 78 band jobs were run before this stage was stopped (14:15, priority change); T > 60 not run.  NOTRUN entries in the tables mean exactly this: not attempted.  UNDECIDED in the tables: some rotation timed out and no rotation SAT.
- Time origins: tau = 0 everywhere; tau-scan (all phase-0 rows up to T_rot) only for T <= 24 at clock 1000 (and T <= 36 if finished).
- R: M minimal (delta integer, delta = 0 mod s), R_f = max(12, delta + s), T' <= 120 for clock 1000 and T' <= 36 / 120 as far as the time boxes allowed for clocks 10 and p11; R*: clock 1000 for 86 R-PASS bands (the batch was stopped at 167 of 195 jobs); clocks 10/p11: 77 of 118 band jobs (T' <= 36).
- All UNSAT results rest on SAT solvers (no DRAT certificates; every ALLUNSAT used in a statement above is confirmed by at least two different encoding/solver combinations unless listed under "ALLUNSAT entries with only one solver/encoding").  The PAPER PROOF steps (Theorems GA, GA*, GB, GR, GR*) are not formalised in Lean.
- Real-thing attempts cover only the T12 exterior for clock 1000 (exact scope in sec. 0b item 5; kissat404 only); seams against the p8 lattices were not run; the p11 exterior (finite rooted word, not a periodic band) was not attempted (would need the root-based seam of the neutral-band format).  Larger junctions, other junction phases, other exteriors: UNDECIDED.
- Nothing is claimed about 196; no Lychrel number, certificate or template return was found.

## 9. Files
Studio ~/p196_run/r13a (mirror ~/Desktop/p196_studio/r13a on the Mac): census/bandcensus.cpp, census/runall.sh and census outputs b<clock>_s<s>.txt; bandsat.py (enc1: strip with cone trimming, L, R, R*, L*, LD), bandsat2.py (enc2: direct relations), bandval.py (genuine validation), bandrun.py (one instance), bandjob.py (all rotations of one band), bandenum_sat.py + cross_census.py (SAT enumeration cross-check of the census), seamgen.py + seamjob.py (E | J | V seam SAT and sweeps, genuine validation seamval.py, replay seamreplay.py), centregen.py + centrejob.py (exact-centre SAT in the style of satc.py, selftest and base-9 control), gen*.py (job generators), pool.py, mkfinal.py / tally.py / status_gen.py / undecided.py / mk_u3table.py (tables and summaries, assembled by assemble.sh into FINAL.md), ctrl/ (controls: rows_ctrl.py, plant_w0.py, run_b9_centre.sh), logs/<tag>/i*.log (one log per job) and NOTES.md (chronological log with UTC times).

## 8.1 Per-clock status of the census bands (generated)

**clock 1000** (265 bands).  L(M=1,tau=0,R=12): 135 not run, 14 UNDECIDED (all rotations timed out or not decided).  R: 133 not run, 14 UNDECIDED.
  not run (T distribution): T=64x11, T=84x6, T=96x2, T=112x5, T=120x2, T=128x4, T=140x2, T=148x2, T=160x4, T=168x5, T=180x2, T=192x3, T=216x2, T=224x2, T=240x4, T=252x4, T=264x2, T=280x4, T=300x2, T=320x2, T=336x6, T=340x2, T=360x2, T=364x2, T=392x2, T=440x2, T=480x6, T=504x2, T=512x4, T=560x2, T=616x1, T=672x2, T=700x2, T=780x2, T=840x2, T=896x2, T=960x2, T=1036x2, T=1216x3, T=1316x4, T=1392x2, T=1904x4, T=2400x2, T=2464x1, T=2784x2, T=10752x2
  L UNDECIDED: (13,5,0) T=120 [TTT]; (8,10,0) T=120 [TTT]; (2,16,16,2,0) T=120 [TTTTT]; (5,4,4,5,0) T=120 [TTTTT]; (9,16,8,8,0) T=60 [TTTTT]; (10,1,4,13,0) T=60 [TTTTT]; (10,18,10,4,4) T=60 [TTTTT]; (5,6,1,0,0,0) T=84 [TTTTUT]; (17,4,15,6,0,0) T=84 [TTTTTU]; (11,12,10,10,1,0) T=108 [TTTTTT]; (17,4,1,2,10,0) T=108 [TTTTTT]; (4,16,16,16,2,18,0) T=56 [TTTTTTT]; (18,2,8,14,14,8,2) T=56 [TTTTTTT]; (10,10,9,8,11,8,7) T=56 [TTTTTTT]
  R UNDECIDED: (13,5,0) T=120 [TTT]; (8,10,0) T=120 [TTT]; (8,8,0,0) T=48 [TTTT]; (16,16,0,0) T=48 [TTTT]; (2,16,16,2,0) T=120 [TTTTT]; (5,4,4,5,0) T=120 [TTTTT]; (8,14,14,8,0) T=60 [TTTTT]; (8,8,16,9,0) T=12 [TTTTT]; (13,4,1,10,0) T=12 [TTTTT]; (10,18,10,4,4) T=60 [TTTTT]; (1,13,13,13,13,1,0) T=112 [TTTTTTT]; (13,13,11,10,4,2,1) T=112 [TTTTTTT]; (13,13,1,12,2,12,1) T=112 [TTTTTTT]; (2,4,10,11,13,13,1) T=112 [TTTTTTT]

**clock 10** (284 bands).  L(M=1,tau=0,R=12): 130 not run, 17 UNDECIDED (all rotations timed out or not decided).  R: 171 not run, 0 UNDECIDED.
  not run (T distribution): T=48x4, T=56x2, T=60x11, T=70x4, T=72x2, T=96x31, T=112x4, T=126x4, T=130x2, T=140x1, T=144x4, T=160x5, T=168x8, T=180x1, T=240x2, T=280x6, T=288x8, T=336x2, T=348x2, T=360x2, T=504x2, T=532x2, T=544x1, T=608x2, T=720x2, T=960x2, T=1064x2, T=1344x2, T=1392x2, T=1526x4, T=2200x2, T=4400x2
  L UNDECIDED: (9,8,0) T=36 [UTT]; (13,13,1,1) T=48 [TTTT]; (14,1,10,1) T=48 [TTTT]; (10,4,2,8,0,0) T=48 [TTTTTT]; (8,2,4,10,0,0) T=48 [UTTTTT]; (14,4,18,12,6,0) T=48 [TTTTTT]; (18,11,13,5,7,0) T=48 [TUTTTT]; (12,6,18,10,8,0) T=48 [TTTUTT]; (4,2,14,2,4,0,0) T=42 [TTTTTTT]; (12,13,6,13,12,1,1) T=42 [TTTTTTT]; (17,16,16,17,1,6,1) T=42 [TTTTTTT]; (14,3,9,12,12,9,3) T=42 [UTTTTTU]; (13,8,6,9,5,10,3) T=28 [TTTUTTT]; (17,2,2,17,0,5,5,0) T=32 [TTTTTTTT]; (17,6,9,1,7,9,5,0) T=32 [TTTTTTTT]; (5,9,7,1,9,6,17,0) T=32 [UTTTTTTT]; (13,10,14,15,5,8,4,3) T=32 [TTTTTTTT]

**clock 00001110001** (161 bands).  L(M=1,tau=0,R=12): 146 not run, 0 UNDECIDED (all rotations timed out or not decided).  R: 148 not run, 0 UNDECIDED.
  not run (T distribution): T=44x15, T=66x24, T=77x6, T=88x4, T=110x7, T=132x17, T=154x12, T=220x4, T=231x2, T=264x2, T=308x6, T=330x13, T=396x1, T=462x12, T=484x4, T=528x4, T=770x4, T=924x2, T=1232x1, T=1386x2, T=1452x1, T=2310x1, T=4774x2

