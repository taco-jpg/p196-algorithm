# Round 12, agent r12g: K1 for the decimal period-8 lattices rec0, rec1, rec2: relaxation cyclic sets + exact fold check, all periods

Agents r12g, r12g2, r12g3, 2026-11-08. Run on the Studio in ~/p196_run/r12g; paths below are relative to this directory.
Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF / UNDECIDED. **No certificate was found. Nothing here is a claim about 196,
and no Lychrel number is proved.** Status of this file: FINAL (09:26 UTC); complete.

## 0. Summary

Question (K1): is there a centre C, of any period, that makes the template P(q,C) = B0 W0^q C rev(W0)^q rev(B0) return?
Method: the defect of a centre is confined to the top D folded columns ("depth" D, section 1). Such a centre is a periodic
orbit of the exact fold map F_D of the top D-window. Its bottom part lies in the cyclic set Cyc(Kb) of the bottom
relaxation, its top part in the cyclic set TopCyc(Kt) of the top relaxation. The forward iteration A_{n+1} = F(A_n) cap Z
from one phase per phase orbit cannot lose such an orbit (section 3), and it covers all periods at once.

* **COMPUTED (kfwd/kfwd3, PAPER PROOF reduction of section 3):**
  * rec0: no centre of depth <= 23, any period, all four phase classes (orbit 0 computed, the others by the complement
    symmetry Phi).
  * rec1: the same (its bulk tables are rec0's, shifted in phase; the window map does not see the exterior).
  * rec2: no centre of depth <= 27, any period (orbits 0 and 1 computed, 2 and 3 by Phi).
* **COMPUTED (direct fold check, kink7):** the exact fold map has no periodic orbit inside Cyc(K) for rec0 K <= 19 and for
  rec2 K <= 23 (both computed orbits); same conclusion for these depths by a second route that uses neither TopCyc nor the
  forward iteration. The independent code (genuine addition, its own cores) confirms it with equal successor counts for
  rec2 K = 17, 20..23 (both orbits) and rec0 K = 17, 18.
* **Two independent pipelines** (kfwd/kink7/ktop/kcommon versus src/indep, which shares no code: own parser, explicit
  words, genuine addition N + rev(N), own core algorithm; indep_g3 = the same code with the kink key format beyond 20 cells):
  * rec2 depth <= 24: fully independent for both computed orbits (Core(K) == Cyc(K) K <= 20; forward K = 21 and 24 identical);
  * rec2 depth <= 27: fully two-pipeline for both computed orbits: filters Core(K) == Cyc(K) for K <= 23 (SETS EQUAL, both
    orbits) and forward runs identical at every step (indep K = 27: 50 / 46 steps; K = 24 with own Core(20): 41 / 41 steps);
  * rec0/rec1 depth <= 22: fully two-pipeline: filters Core(K) == Cyc(K) for K <= 18 (SETS EQUAL, orbit 0) and forward runs
    identical at every step (indep K = 22 with its own Core(18): 49 steps, K = 20: 45 steps);
  * rec0/rec1 depth 23: kfwd3 + kink7 Cyc(19) only (Cyc(19) too large for the independent core).
* **Positive controls:** both pipelines find exactly the Lean-verified base-9 centres (b9r0 |C| = 6, 10; b9r1 |C| = 4) as the
  only periodic orbits, in the predicted phase classes (K <= 10 full filters), and keep them through the K > 25 packing
  path with planted filters at K = 26, 27, 29 (48/48 runs as predicted, both codes).
* **Closing route "per period, all depths" (relsat_period): does not close.** rec0 K0 = 22, T = 80 is SAT (an accepting
  closed walk of R_22 of length 80 exists, replayed). UNDECIDED whether any (K0, T) is UNSAT; none expected.
* **UNDECIDED:** centres of depth >= 24 (rec0, rec1) / >= 28 (rec2); K1 itself; fixed centres beyond r12d's lengths whose
  front falls more than 23 / 27 columns behind the fold.

## 1. Setting and the definition of depth

Number N with digits d_0 (least significant) .. d_{n-1}. Pair word P_x = d_x + d_{n-1-x} (x = 0..n-1, values 0..18,
palindromic); lower half x < h := ceil(n/2); for odd n the middle cell P_{h-1} = 2 d_{h-1} is even. T(N) = N + rev(N) =
sum_x P_x 10^x. Ascending carries a_0 = 0, a_{x+1} = [P_x + a_x >= 10], e_x = (P_x + a_x) mod 10; overflow gamma = a_n.
Descending carries b_x = carry into the mirror position n-1-x, with b_{h-1} = a_h (n even) or a_{h-1} (n odd, the middle
cell is its own mirror), b_{x-1} = [P_x + b_x >= 10], r_x = (P_x + b_x) mod 10 = digit at the mirror position, gamma =
[P_0 + b_0 >= 10]. New word, lower half: P'_x = e_x + r_{x-gamma} (n' = n + gamma); when n is even and gamma = 1 the new
middle cell is P'_h = 2 e_h = 2 r_{h-1}. (These formulas were checked against plain integer arithmetic on 20,000 random
windows over the rec0 lattice, all t, j, par: 0 mismatches.)

Lattice L (rec0, rec1, rec2 of `lattice_formats/p8_scc.txt`): L(t,x) = B[t mod 8][x] for x < nB, W[t mod 8][(x-nB) mod m]
otherwise (m = 20, 20, 48), clock g = 10101010; an exact solution of the pair-word dynamics with overflow g_t. Bulk tables
UP[t][j] / DN[t][j] = the periodic ascending carry into a column-j bulk cell / descending carry into its mirror. They are the
unique periodic solutions of the carry recursions because every bulk row has cells != 9 (max run of 9s: 1 for rec0/rec1,
2 for rec2; checked by r12g3, 0 recursion mismatches in all three tables).

**Definition (depth).** An orbit (N_t), t >= t0, has its *defect confined to depth D* if for every t >= t0 the pair word
agrees with the lattice on every folded column below the frame c_t := h_t - D, i.e. P(t)_x = L(t,x) for 0 <= x < h_t - D,
and the overflow is gamma_t = g_t. Its *depth* is the least such D, i.e. D = sup_t (h_t - F_t) with r12d's lattice front
F_t = min{x : P(t)_x != L(t,x)}. A *centre of depth D* is such an orbit (the defect lives in the top D folded columns for
ever). This is r12d survscan's "confined kink in the top w folded columns" with w = D, and kink6's K. (Checked: kfwd
lifetimes with no filter reproduce survscan's lifetimes for w = 6, 7 in all 8 lattice/class cases.)

Phase of the frame: phi = (t mod 8, j = (c - nB) mod m, par = n mod 2). The frame moves exactly like h: c_{t+1} = c_t +
dh_t, dh_t = [g_t = 1 and par_t = 0]; phi_{t+1} = nu(phi_t) := (t+1, j+dh, par+g_t). nu is a permutation of the
2*8*m phases: 4 phase orbits of length 80 (rec0, rec1) and 4 of length 192 (rec2). A window state is s = (phi, w),
w = (P_{c}, ..., P_{h-1}) in {0..18}^D.

## 2. The objects

* **F_D (exact fold map)**: s_t -> s_{t+1} for the top D-window with exact lattice below the frame; undefined when a
  lattice cell below the new frame would change ("lattice breaks"). kcommon.h exact_step (= kink6 exact_succ); independent
  version indep fstep = genuine N + rev(N) on the explicit full word (exterior + 3 bulk periods + window + mirror).
* **R_K (bottom relaxation)**: window [c, c+K) with the same frame motion and the same exact lattice below, the cells above
  replaced by free inputs Din in {0,1} (descending carry entering from cell c+K) and topv in 0..9 (e-digit of cell c+K,
  used only when the frame shifts). Cyc(K) = states on a closed walk of R_K. kink6 (all orbits), kink7 (one phase orbit),
  indep core (bi-infinite core; = Cyc when the orbit has one cyclic SCC, which kink7 reports at every K).
* **Top relaxation** (ktop, indep topcore): top k cells [h-k, h), fold exact, free inputs from below a_in in {0,1} (carry
  into cell h-k) and r_in in 0..9 (r-digit of cell h-k-1, used only on overflow steps without frame shift); phase (t, par);
  no lattice at all (depends on base and clock only). TopCyc(k) = its cyclic set: |TopCyc(k)| = 232, 3896, 61464, 819952,
  10371912, 123287536 for k = 1..6.
* **Z(phi)** = windows whose bottom Kb cells lie in Cyc(Kb) at phi and whose top Kt cells lie in TopCyc(Kt) at (t, par);
  Kb + Kt <= K, the cells between are free.
* **kfwd / kfwd3** (r12g src/kfwd.cpp, src/kfwd_v3.cpp): A_0 = Z(phi0) restricted to genuine windows (even top cell when n is
  odd), A_{n+1} = F_K(A_n) cap Z(phi_{n+1}); EMPTY / STABLE / UNDECIDED. indep fwd: the same iteration with fstep.

## 3. PAPER PROOF: soundness of the pipeline

Throughout, D = K is the window depth, Kb = K - k the bottom filter depth, Kt <= k the top filter depth.

**Lemma 1 (window map is exact).** Let the pair word at time t agree with L(t,.) below the frame c = h - K, with c >= nB +
m + 3. Then the pair word at t+1 agrees with L(t+1,.) below c' = h' - K iff F_K(s_t) is defined, and then F_K(s_t) =
s_{t+1}; the overflow is g_t. The value F_K(s) depends only on s = (phi, w) (not on q or on the exterior).
*Proof.* Below c every cell is lattice, so the ascending carry into c is UP[t][j] (the row's carry recursion reaches its
periodic solution at the first non-9 bulk cell) and every e_x, x < c, is the lattice one. Inside the window e and a follow
from UP[t][j]; the fold input b_{h-1} is a_h (n even) or a_{h-1} (n odd), both computed from the window; b and r inside the
window follow downward. Below c the actual b_x differs from the bulk DN only until the first cell != 9 (at most 2 cells for
rec0/rec1, 3 for rec2): after that the same recursion with the same value gives the lattice carries, so the overflow is the
lattice's g_t and r_x is the lattice value for all lower cells. Hence P'_y = e_y + r_{y-g} differs from the lattice value
L(t+1,y) (y below the new frame) only through the <= 3 perturbed r-digits; wstep checks exactly these targets, and the cell
c itself when the frame shifts (dh = 1, c leaves the window). The new window cells are e_x + r_{x-g} (x in the new window;
r_{c-1} is the perturbed or the bulk value), and the new middle cell 2 e_h when dh = 1. This is kcommon wstep with
Din = b_{h-1} and the ghost e_h = (w_{K-1} + Din) mod 10. The independent fstep does the same by explicit addition and checks
every cell below the new frame and the overflow (overflow mismatches: 0 in every run). Validation of the rule against
genuine pair-word steps: klib test_klib, exact_small validate, indep selftests (a)-(e) (0 mismatches), q vs q+2. QED

**Lemma 2 (centres are periodic orbits).** A centre of depth <= K gives, for t >= t1 (t1 such that c_t >= nB + m + 3; h_t
grows by m per phase orbit), window states with s_{t+1} = F_K(s_t). The state space (phases x {0..18}^K) is finite and F_K is
a function, so (s_t) is eventually periodic: its periodic part O is a periodic orbit of F_K, and the phases of O form one
whole phase orbit (they follow nu, and the period is a multiple of the phase orbit length). A centre of depth D < K is also
a centre of depth <= K (the cells [h-K, h-D) are lattice cells in the window). In particular every fixed-centre return
T^S(P(q,C)) = P(q+K',C) (any q, any S) is a periodic orbit of F_K for every K >= its depth, and so is every orbit whose
defect stays confined (bounded depth) from some time on: periodicity is no restriction. QED

**Lemma 3 (bottom projection, incremental construction).** For Kb <= K let pi_b(phi, w) = (phi, w_0..w_{Kb-1}) (same frame).
If F_K(s) is defined then pi_b(s) -> pi_b(F_K(s)) is an edge of R_Kb, with Din = the descending carry leaving cell c+Kb (in
the window, or the fold input if Kb = K) and topv = e_{c+Kb}. *Proof:* wstep restricted to the bottom Kb cells reads only
the phase, these cells, the carry entering from above (Din), the e-digit of the next cell (topv, only when dh = 1: new cell
topv + r_{c+Kb-1}), and the same lattice check below c. QED. Consequences: (i) the bottom Kb cells of every state of a
periodic orbit of F_K lie in Cyc(Kb) (a periodic orbit projects to a closed walk); (ii) applied to R_K itself (drop the top
cell): Cyc(K) is contained in Cyc(K-1) x {0..18}, so Cyc(K) = the cyclic part of the subgraph of R_K induced on the candidate
set Cyc(K-1) x {0..18} -- a closed walk of R_K lies in the candidate set and vice versa. kink6/kink7 compute exactly this
(Tarjan; nontrivial SCCs plus self-loops); base: all 19^K windows for K <= 4 (kink6 full) or the empty window (indep, b9).
Cyc(K) splits by phase orbit (edges follow nu); kink7 computes one orbit.

**Lemma 4 (top projection).** For Kt <= K the top Kt cells of every state of a periodic orbit of F_K lie in TopCyc(Kt). The
top rule reads the phase (t, par), the top Kt cells, a_in = carry into h-Kt and r_in = r_{h-Kt-1}; the fold (Din, new middle
2 r_{h-1}) is computed exactly as in F_K. Dropping the bottom cell maps top-k edges to top-(k-1) edges, so TopCyc(k) is
built incrementally like Cyc. TopCyc depends on base and clock (a base-10 TopCyc used for base 9 lost the base-9 orbit;
with the base-9 TopCyc all controls pass). rec0, rec1, rec2 share base 10 and clock 10101010, so one TopCyc. QED

**Lemma 5 (parity).** If s' = F_K(s) and par(s') = 1 then the top cell of s' is even (g = 0: middle e_{h-1} + r_{h-1} with
b_{h-1} = a_{h-1}, so e = r; g = 1 and par = 0: new middle 2 e_h). Every state of a periodic orbit has a preimage, so the
parity condition on A_0 removes no periodic state. QED

**Theorem (forward iteration).** Let phi0 be any phase and A_0, A_n as in section 2. If O is a periodic orbit of F_K whose
phases contain phi0, then for every n >= 0 some state (phi_n, w) of O has w in A_n. Hence A_N = {} for some N implies: F_K has
no periodic orbit in the phase orbit of phi0, so (Lemma 2) there is no centre of depth <= K, of any period, in this class.
*Proof.* O passes through phi0 at some state (phi0, w_0); w_0 is in Z(phi0) (Lemmas 3, 4) and satisfies the parity condition
(Lemma 5), so w_0 is in A_0. If (phi_n, w_n) is in O with w_n in A_n, then F_K(phi_n, w_n) = (phi_{n+1}, w_{n+1}) is defined
(O is an orbit), lies in O and in Z(phi_{n+1}) (Lemmas 3, 4), so w_{n+1} is in A_{n+1}. QED
* *Nesting.* Z(phi_Lo) = Z(phi0) and Lemma 5 give A_Lo subset A_0; X -> F(X) cap Z is monotone, so A_{n+Lo} subset A_n. The
  code checks this at multiples of Lo, but the check needs two multiples of Lo >= s0, so it is only exercised in the base-9
  controls (Lo = 20); in the base-10 runs A_n is empty before step 2 Lo = 160 / 384, and nesting_ok = 1 there is vacuous
  (nesting is not used for soundness). STABLE (A_{n+Lo} = A_n != {}) means F^Lo maps the finite set A_n onto itself, hence
  bijectively, so every state of A_n is periodic (used in the base-9 controls).
* *Chunking* (A_0 streamed in chunks of 2^27 windows, each iterated s0 = 8 steps alone, then merged): G(X) := F(X) cap Z
  satisfies G(X u Y) = G(X) u G(Y) because F is a (partial) function and Z is a pointwise filter; so the union of the
  chunk images after s0 steps is exactly A_{s0}. Per-thread sort/unique does not change the set. The logged sizes of steps
  1..s0-1 are sums over chunks (upper bounds); steps 0 and >= s0 are exact.
* *Start phase:* any phase of the orbit works (select_phase.py picks the one with the smallest |Z(phi0)|). The bottom filter
  is the per-orbit kink7 file of the orbit of phi0: |A_0| > 0 in every run shows phi0 lies in that file's orbit, and the
  iteration only visits phases of that orbit, all of which the file covers.
* *Base-D packing* (kfwd3 and indep fwd for 25 < K <= 30): cells 0..14 in base 19 in the low 64 bits (19^15 < 2^64), cells
  15..K-1 (<= 15) in the high 64 bits. This is injective on {0..18}^K; sort/unique/includes/equality need only an injective
  key with a total order. Round trips: 4.4M windows K = 20..30 (test_wenc.cpp), 1e6 random windows at every indep start.
  For K <= 25: 5 bits per cell (125 bits). Filter keys use kink6's format (phase << 100 for K <= 20, << 118 for 21..23).
* *Direct fold check* (kink6/kink7 "exact cycles"): by Lemma 3 (Kb = K) every periodic orbit of F_K lies in Cyc(K), so it is
  a cycle of the functional graph of F_K restricted to Cyc(K); 0 cycles => no centre of depth <= K in that orbit.

**Symmetry Phi (complement).** Phi(t, j, par, w) = (t+tau, j+sigma, par, 18-w) with (tau, sigma) = (2,5) or (6,15) for
rec0/rec1 and (4,24) for rec2. Table identities L[t+tau][j+sigma] = 18 - L[t][j], UP -> 1-UP, DN -> 1-DN, G[t+tau] = G[t]
(symcheck.py; symcheck2.py with plain Python integers). Under complement every relation of the step maps to itself:
P + a -> 19 - (P + a), digit e -> 9 - e, carry -> 1 - carry, P' = e + r -> 18 - P'; fold input Din -> 1 - Din, ghost ->
9 - ghost, new middle -> 18 - new middle; the lattice checks map to the same checks at the shifted phase. Hence F_K o Phi =
Phi o F_K as partial maps (plain-integer check on 4000 random states, 0 mismatches; indep selftest (e)), and Phi maps periodic
orbits of F_K in a phase orbit O to periodic orbits in Phi(O). Phi permutes the 4 orbits of rec0 cyclically (0->3->2->1->0)
and swaps 0<->2, 1<->3 for rec2. So EMPTY for rec0 orbit 0 covers all four rec0 classes; EMPTY for rec2 orbits 0 and 1 covers
all four. (Phi is a symmetry of the window map only; that is all the argument needs.) Observed: kink6 rec0 K = 15 all
orbits = 4 x kink7 orbit 0, rec2 K = 17 = 2 x (orbit 0 + orbit 1), in every count.

**rec1.** L, UP, DN, G of rec1 equal rec0's shifted by (6,5) (and by (2,15)) (klib tables and symcheck2, plain integers).
F_K reads only these tables (Lemma 1), so F_K^rec1(t, j, par, w) = F_K^rec0(t+6, j+5, par, w) up to the phase relabelling;
periodic orbits correspond one to one. Every rec0 statement (any depth) holds for rec1. (Also observed: kink6 counts equal
for rec0 and rec1 at K = 3..7; plain-integer F_rec1(t,j) = F_rec0(t+6,j+5) on 4000 random states.)

**What is proved and what is computed.** Proved on paper: Lemmas 1-5 (given the tables), the Theorem, nesting, chunking,
packing, the symmetry transfers. The finite computation that the reduction needs, and how each part is checked:
* (C1) the tables L, UP, DN, G of rec0/rec1/rec2 from p8_scc.txt: two parsers (klib/export_tbl; indep mklat.py, explicit
  rows); periodic carry solutions unique (non-9 cells in every row, r12g3);
* (C2) the Phi and rec1-shift identities: symcheck.py (tables), symcheck2.py (plain integers), r12g3 (tables, again);
* (C3) the bottom filters Cyc(Kb) of the orbits used: kink7; equal as SETS to the independent cores for rec0 Kb <= 16 and
  rec2 Kb <= 17 (r12g2) [extension to rec2 Kb <= 20, rec0 Kb <= 17: section 9]; 1 cyclic SCC per orbit at every Kb;
* (C4) TopCyc(4): ktop = indep topcore (SETS EQUAL, k = 1..5);
* (C5) the forward runs (section 4.1) and their independent replications (sections 4.3, 9).
The code that implements the rule was validated against genuine pair-word arithmetic and re-implemented independently.
Independent confirmation of the filters as SETS: rec0 Cyc(K), K <= 18 (the filter of K = 22), rec2 Cyc(K), K <= 23 orbit 0
(the filter of K = 27), also K <= 23 orbit 1. Not independently confirmed as a set:
rec0 Cyc(19) (the filter of the K = 23 run; its check would need ~75 GB). For it the evidence is the same code being exact at
every smaller Kb, the kink6 = 4 x kink7 (rec0 K = 15) and 2 x (o0 + o1) (rec2 K = 17) identities, and the relsat models
(rec0 K = 16, rec2 K = 20) lying inside the files.

## 4. Results (COMPUTED)

### 4.1 Forward iteration (kfwd/kfwd3; bottom Cyc(Kb) of orbit o, top TopCyc(4); EMPTY = no periodic orbit in the class)

| lattice | K | Kb | orbit | phi0 | |A_0| | |A_8| | EMPTY at | lifetime | time | RSS | 2nd pipeline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rec0 | 20 | 16 | 0 | (1,5,1) | 3,266,141,040 | 16,583,800 | 44 | 43 | 714 s | 10.2 GB | indep, own Core(16): identical, all 45 steps |
| rec0 | 21 | 17 | 0 | (1,9,1) | 6,940,696,200 | 31,730,133 | 44 | 43 | 1688 s | 11.0 GB | - |
| rec0 | 22 | 18 | 0 | (1,9,1) | 14,678,298,000 | 65,774,047 | 48 | 47 | 2914 s | 13.8 GB | indep, own Core(18): identical, all 49 steps |
| rec0 | 23 | 19 | 0 | (5,12,1) | 30,074,643,720 | 123,240,785 | 49 | 48 | 6356 s | 16.5 GB | - |
| rec2 | 21 | 17 | 0 | (5,18,1) | 74,972,040 | 407,730 | 39 | 38 | 20 s | | indep, own Core(17): identical, all steps |
| rec2 | 21 | 17 | 1 | (7,18,1) | 68,187,240 | 323,405 | 36 | 35 | 18 s | | indep, own Core(17): identical, all steps |
| rec2 | 23 | 19 | 0 | (1,17,1) | 212,117,520 | 1,398,331 | 40 | 39 | 53 s | 7.3 GB | - |
| rec2 | 23 | 19 | 1 | (3,17,1) | 177,360,840 | 1,270,869 | 37 | 36 | 49 s | 7.3 GB | - |
| rec2 | 24 | 20 | 0 | (5,16,1) | 353,272,200 | 2,240,826 | 40 | 39 | 128 s | 6.6 GB | indep, own Core(20): identical, all 41 steps |
| rec2 | 24 | 20 | 1 | (3,15,1) | 324,544,740 | 1,310,210 | 40 | 39 | 108 s | 7.0 GB | indep, own Core(20): identical, all 41 steps |
| rec2 | 27 | 23 | 0 | (5,14,1) | 2,479,181,340 | 12,194,467 | 49 | 48 | 591 s | 9.1 GB | indep fwd (same Cyc(23)): identical, all 50 steps |
| rec2 | 27 | 23 | 1 | (7,14,1) | 1,815,412,020 | 9,734,444 | 45 | 44 | 448 s | 8.9 GB | indep fwd (same Cyc(23)): identical, all 46 steps |

(|A_0| before the parity filter. Logs: logs/fwd/, logs/fwd2/, logs/indep/ifwd_*.)

### 4.2 Cyclic sets and the direct fold check (kink7, one orbit; all with exactly 1 cyclic SCC, exact cycles 0)

rec0 orbit 0: |Cyc(K)| = 9,140,287 / 19,389,807 / 40,126,496 / 80,883,639 / 160,733,468 for K = 15..19 (accepting states
416,237 / 778,743 / 1,564,911 / 3,149,706 / 5,943,487; K = 19: 1.54e9 candidates, 2262 s, 17.5 GB). kink6 (all orbits)
K <= 15 = 4 x orbit 0.
rec2: orbit 0 |Cyc(K)| = 3,829,624 / 5,991,829 / 9,514,444 / 15,274,048 / 24,582,382 / 39,861,868 / 63,618,453 (K = 17..23);
orbit 1: 3,274,529 / 5,095,160 / 7,974,177 / 12,597,715 / 20,216,881 / 32,186,852 / 51,798,710. kink6 K = 17 (all orbits)
= 2 x (orbit 0 + orbit 1).
Exact fold map inside Cyc(K): **0 cycles** for rec0 K <= 19 and rec2 K <= 23 (both orbits).

### 4.3 Independent pipeline src/indep (r12g2)

Own lattice parser (mklat.py), explicit rows, genuine addition, bi-infinite core by queue trimming, own top core, own forward
iteration, own packing. Results: Core(K) == Cyc(K) (SETS EQUAL) for rec0 orbit 0 K = 3..16 and rec2 orbit 0 K = 3..17
(r12g2), extended by r12g3 to rec2 orbits 0 AND 1, K = 17..20 (indep core, 809 s / 690 s, 8.3 / 6.9 GB) and, with the
key-format extension indep_g3 corefrom (own Core(20) -> K = 21..23, 4 thr, 743 s, 40.8 GB), rec2 orbit 0 K = 21, 22, 23
(63,618,453 states, accepting 889,749 = kink7); rec0 orbit 0 K = 15..18 (indep core to K = 17, 232 s, 21.6 GB; corefrom own
Core(17) -> K = 18, 261 s, 40.7 GB: 80,883,639 states, accepting 3,149,706 = kink7), i.e. the filter of the rec0 K = 22 run; indep fold check inside its own Core(20), rec2 o0 / o1: 10,595,481 / 8,737,601 fold
successors inside (= kink7), 0 cycles, overflow mismatches 0 (r12g3); the same inside Core(21..23) of rec2 o0 / o1
(17,079,408 / 27,736,184 / 44,301,524 and 14,054,984 / 22,412,638 / 36,099,977 successors, = kink7) and inside Core(17), Core(18)
of rec0 o0 (28,583,281 and 57,547,232 successors, = kink7), all with 0 cycles;
TopCore(1..5) == TopCyc(1..5); fold check inside Core(17) rec2: 2,644,006 successors, 0 cycles (= kink7); forward rec2 K = 21
and rec0 K = 20: |A_n| identical at every step; base-9 control: the Lean-verified centres and nothing else (section 4.4).

### 4.4 Controls

* p12m9 (B0/W9): kink6 counts identical to run_checks.sh; kfwd from all 18 t = 0 phases EMPTY at K = 5 (known: no periodic
  orbit of the depth-5 map).
* Lifetimes (k = K, no filter) = r12d survscan for w = 6, 7, all four classes of rec0 and rec1; four longest-lived windows
  replayed with big integers (repo replay_kink.py): "lattice broken at step T+1" exactly as kfwd says.
* Base 9 (export_b.py, generic-base tables from the Lean-verified certificate JSONs): kink7 from Cyc(0), K = 1..10, all 4
  orbits of b9r0 and b9r1: exactly one exact cycle per K (period 20) in the orbit predicted by the centres; kfwd STABLE with
  that orbit ([1,15,15,1], [1,1,15,15,1,1,15,15,1], [11,5,5,11,11,5,5,11]) and EMPTY elsewhere; indep the same.
* **Base-9 planted control of the K > 25 path (r12g3, logs/g3/b9_planted.log).** Bottom filter = the lattice window only (at
  every phase), top = base-9 TopCyc(4); b9r0, b9r1; K = 26, 27 (k = 4) and 29 (k = 6, two free middle cells); all 4 classes;
  kfwd3 and indep: 48 runs, 12 STABLE / 36 EMPTY, identical verdicts in both codes; STABLE exactly in the class predicted by
  the Lean-verified centres, each time one periodic orbit of period 20, all-lattice. So the base-19/17 packing (cells 15..K-1
  in the high word) and the STABLE detection keep a known periodic orbit (this tests the iteration, not Cyc's completeness).
* relsat (repo SAT encoding of R_K, fixed period): SAT models at rec0 K = 8, 16 (T = 80), rec2 K = 12, 20 (T = 192) replay
  with klib.window_step and lie 80/80 resp. 192/192 inside the cyclic-set files (completeness direction of Cyc).

### 4.5 Evidence matrix (what rests on what)

"Filter" = the bottom cyclic set Cyc(Kb) used; "two pipelines" means: filter sets equal between kink7 and the independent core,
and forward runs identical at every step (or, for the fold check, identical successor counts).

| claim | filter | kfwd/kfwd3 run | independent code |
|---|---|---|---|
| rec0, rec1 depth <= 20 | Cyc(16) | yes | filter set equal (own Core(16)), forward identical (45 steps): **two pipelines** |
| rec0, rec1 depth <= 21 | Cyc(17) | yes | filter set equal (own Core(17)); forward covered by the K = 22 replication |
| rec0, rec1 depth <= 22 | Cyc(18) | yes | filter set equal (own Core(18), corefrom), forward identical (49 steps): **two pipelines** |
| rec0, rec1 depth <= 23 | Cyc(19) | yes | kink7 + kfwd3 only (Cyc(19) too large to re-check: ~80 GB) |
| rec2 depth <= 21 | Cyc(17) o0, o1 | yes | filter sets equal, forward identical, both orbits: **two pipelines** |
| rec2 depth <= 24 | Cyc(20) o0, o1 | yes | filter sets equal (own Core(20)), forward identical (41 steps each): **two pipelines** |
| rec2 depth <= 27 | Cyc(23) o0, o1 | yes | filter sets equal (corefrom, both orbits), forward identical (50 / 46 steps): **two pipelines** |
| fold check rec0 K <= 19 | Cyc(K) | kink7 | independent fold counts equal for K = 17, 18 (K = 19 not re-checked) |
| fold check rec2 K <= 23 | Cyc(K) | kink7 | independent fold counts equal for K = 17, 20..23, both orbits |

## 5. The theorem, and the fixed-centre language of r12d

**Theorem K1-depth (COMPUTED + PAPER PROOF reduction).** Let L be rec0 or rec1 (m = 20) and D = 23, or L = rec2 (m = 48)
and D = 27. There is no orbit of reverse-and-add whose pair word, from some time on, agrees with the lattice L (exterior
B0, bulk W0, clock 10101010) on every folded column more than D columns below the fold at every step. In particular there
is no centre of depth <= D, of any period and in any phase class.

The statement also holds for any other exterior with the same bulk and clock (the window map does not see the exterior).

**Fixed-centre form (exact translation).** r12d's family is P(q,C) = B0 W0^q C rev(W0)^q rev(B0) at a time t = 0 (mod 8),
with return T^S(P(q,C)) = P(q+K',C), S = 80K' (m = 20) or 192K' (m = 48).
* (a) *Every return is a centre.* A return that continues as a chain P(q,C) -> P(q+K',C) -> ... (for q >= q0(K') a single
  return already does, by r12d's shield reduction; a sporadic return below the threshold that does not continue is not a
  certificate and is not covered; along a chain q grows, so Lemma 1 applies from some time on) is a periodic orbit of the fold
  map; it has a finite depth D_C = max_{0 <= t < S} (h_t - F_t). At t = 0, h_0 - F_0 <= ceil(|C|/2)
  (B0 W0^q is lattice). The Theorem says D_C >= 24 (rec0, rec1) / 28 (rec2) for EVERY return, of every |C| and every period.
  For |C| <= 2D = 46 / 54 this means: if such a C returned, its lattice front would have to fall behind the fold by more than
  D columns at some time of the period.
* (b) *Every centre is a return.* Within a phase orbit, at the times t = 0 (mod 8) the frame column j advances by 2 per 8
  steps (n grows by 4) and par is constant, so the 4 phase orbits correspond to (j mod 2, par) at t = 0 (mod 8), and every
  orbit reaches j = epsilon in {0,1}. Reading a centre of depth D and period S at such a time gives a fixed-centre return of
  period S with C = (W0[0..epsilon) + the D-window, mirrored), i.e. |C| = 2(D + epsilon) - par in {2D-1, 2D, 2D+1, 2D+2}.
  Checked (r12g3, phase map): for the frame at depth D, kink7 orbits 0, 1, 2, 3 are (epsilon, par) = (0,0), (0,1), (1,0),
  (1,1) at t = 0 (mod 8), i.e. canonical |C| = 2D, 2D-1, 2D+2, 2D+1; at t = 0 (mod 8) each orbit visits all m/2 columns j of
  its parity (10 for m = 20, 24 for m = 48), so the same centre also reads as |C| = 2(D + j) - par for those j.
* So in r12d's language the Theorem rules out exactly: every return, of any period and any |C|, whose front never falls more
  than 23 (rec0/rec1) / 27 (rec2) columns behind the fold; in canonical form these are the returns with |C| <= 2D + 2 = 48 / 56
  and a confined front. It does not rule out a length range unconditionally: a short C whose front falls behind further is
  not covered (r12d's fixed-centre searches cover those, for |C| <= 25 at period 80 etc.).
* **Consistency with r12d.** (i) Same depth convention: survscan lifetimes w = 6, 7 reproduced exactly (8 cases). (ii) r12d's
  confined-kink result (w <= 12, any period, rec0/rec1) is contained in depth <= 23. (iii) By (b), a period-80 centre of depth
  D <= 11 would be a period-80 fixed-centre return with |C| <= 2D + 2 <= 24 (for very small D choose a column j with
  4 <= 2(D + j) - par, reading C from a slightly lower block boundary), which r12d excludes (|C| = 4..25, all classes); the
  same holds for periods 160, 240, 320 (|C| <= 13: depth <= 5), 400, 480 (|C| <= 12: depth <= 5), rec2 192, 384 (|C| <= 12:
  depth <= 5) and 576 (|C| <= 11: depth <= 4).
  All of these are contained in the depth exclusion: the two results agree (both negative) wherever they overlap, and none
  of the depth runs produced a periodic orbit that r12d's searches should have seen. The depth result is stronger for
  confined centres (all periods, depth up to 23 / 27, i.e. canonical |C| up to 48 / 56); r12d's is stronger for short centres
  whose front falls far behind within one period (r12d section 6: in genuine near misses the front runs ahead and recedes).

## 6. Closing attempts and heuristics

* **relsat_period (PAPER PROOF of the reduction, r12g2):** a centre of period dividing T and depth exactly D >= K0 has, in
  the frame h - D, bottom K0 cells forming a closed R_K0-walk of length T through an accepting state (the bottom cell is
  off-lattice at some time, by minimality of D). So UNSAT at (K0, T) plus "no centre of depth <= K0 - 1" would exclude every
  centre of period dividing T at every depth. **rec0 K0 = 22, T = 80: SAT** (77,638 vars, 927,203 clauses, 1847 s, 2.1 GB;
  replay OK, bottom off-lattice at 2/80 steps). So this route does not close at (22, 80). The relaxations keep accepting
  cycles at every K computed (accepting states grow about x2 per level for rec0), so there is no concrete reason to expect
  UNSAT at another (K0, T); no further runs.
* markov_test: the extension sets of Cyc(K) are not a function of a bounded suffix (rec0 K = 10, 12) -- no finite-memory
  structure, so the "Cyc(K+1) determined by Cyc(K)" proof route has no support.
* Decay (HEURISTIC ONLY, not a result): the exact forward sets shrink by a factor 6.6-7.3 per frame shift (4 steps) in every
  run (src/decay.py, least-squares fit of log|A_n| for 8 <= n <= lifetime - 4):

  | run | K | |A_8| | lifetime | factor per 4 steps | 8 + ln|A_8| / (ln factor / 4) |
  |---|---|---|---|---|---|
  | rec0 o0 | 20 | 16,583,800 | 43 | 7.21 | 42 |
  | rec0 o0 | 21 | 31,730,133 | 43 | 7.01 | 43 |
  | rec0 o0 | 22 | 65,774,047 | 47 | 6.88 | 45 |
  | rec0 o0 | 23 | 123,240,785 | 48 | 6.75 | 47 |
  | rec2 o0 / o1 | 21 | 407,730 / 323,405 | 38 / 35 | 7.17 / 7.30 | 34 / 34 |
  | rec2 o0 / o1 | 23 | 1,398,331 / 1,270,869 | 39 / 36 | 6.70 / 7.29 | 38 / 36 |
  | rec2 o0 / o1 | 27 | 12,194,467 / 9,734,444 | 48 / 44 | 6.61 / 7.29 | 43 / 40 |

  The lifetime grows only logarithmically in |A_8|, which itself grows about x2 per depth level (rec0) -- so the cost of a
  further level is dominated by |A_0| (x2 per level) and the runs stay EMPTY by a wide margin; nothing here is proved.
  Front statistics (indep IFWD_FRONT): the defect stays put in absolute position while the frame
  climbs at speed 1/4, then falls out of the window bottom and breaks the lattice -- the K2 mechanism on the actual fold
  inputs; a local front-speed lemma stays impossible because the relaxation sustains half-kinks.

## 7. UNDECIDED

* Centres of depth >= 24 (rec0, rec1) and >= 28 (rec2), any period; K1 for these lattices in general.
* Fixed centres beyond r12d's length bounds whose front sinks below depth 23 / 27.
* Whether some (K0, T) makes relsat_period UNSAT (none expected).
* **The missing lemma.** K1 for these lattices (no centre of any depth) needs exactly: for every D the exact fold map F_D has
  no periodic orbit in the lattice exact-below regime. The theorem above is this statement for D <= 23 / 27. No finite
  extension of the present method reaches all D: the relaxations R_K keep accepting cycles at every K computed (rec0 K0 =
  22, T = 80 is SAT), so the relaxation cannot close it, and the natural all-depth mechanism (a front-speed bound) is false
  locally (r12d section 6). "One depth further" (task 5) was not run: the kink6/kink7 key has 5 bits per cell below bit
  118, so Kb <= 23 (a new key format would be needed for rec2 K = 28), and rec0 K = 24 needs Cyc(20) (~35 GB) plus ~3.5 h for
  kfwd3; the time was spent on making the existing depths two-pipeline results instead.

## 8. Files (this directory; binaries and data not included)

* `src/kcommon.h` (window rule, tables), `src/kink7.cpp`, `src/ktop.cpp`, `src/kfwd.cpp`, `src/kfwd_v3.cpp` (= bin/kfwd3),
  `src/test_wenc.cpp`, `src/select_phase.py`, `src/symcheck.py`, `src/relsat_check.py`, `src/relsat_period.py`, `src/decay.py`,
  `src/export_b.py`, `src/markov_test.py`, `src/verify_kink.py`, `src/check_table.py`, `src/collect*.py`, `src/cmpsteps.py`
  (step-by-step comparison of two forward logs), `src/planted_filter.py`.
* `src/indep/`: `indep.cpp`, `indep_g3.cpp` (+ mode corefrom, the independent core beyond 20 cells), `indep_g3f.cpp` (+ fold mode
  with the kink key format for K > 20), `mklat.py`, `mkrows_json.py`, `symcheck2.py` (independent pipeline).
* Build: `c++ -O3 -std=c++17 -I shim -o bin/kink7 src/kink7.cpp` (likewise ktop, kfwd, kfwd3 from kfwd_v3.cpp, indep_b from
  indep.cpp, indep_g3, indep_g3f); `shim/bits/stdc++.h` replaces the GCC header on macOS clang.
* `data/lat_*.tbl`: the lattice tables (from `../../lattice_kinks/edge_relaxation/export_tbl.py`; `*_b.tbl` from
  `src/export_b.py`). Repository inputs used unchanged: `../../lattice_kinks/edge_relaxation/` (kink6.cpp, klib.py, relsat.py,
  replay_kink.py, export_tbl.py), `../../lattice_formats/` (p8_scc.txt, cert_b9_rec*.json).
* Drivers: `run_k6.sh`, `run_k7.sh`, `run_fwd.sh`, `run_life.sh`, `chain_*.sh`, `g3_b9_planted.sh`, `g3_core_rec2.sh`,
  `watchdog.py` (written for ~/p196_run/r12g on the Studio).
* Logs (plain): `logs/fwd/`, `logs/fwd2/` (forward runs of table 4.1, `EMPTY at step` lines), `logs/g3/cmp*.log` (pipeline
  comparisons, `IDENTICAL` / `SETS EQUAL`), `logs/g3/b9_planted.log`, `logs/ctrl/`, `logs/life/`, `logs/relsat/`, `logs/relsat2/`,
  `logs/ktop_*`. Packed in `logs.tar.gz`: every log, including `logs/k6_*`, `logs/k7_*` (cyclic-set sizes and the exact fold
  check, `cycles=0` lines), `logs/indep/` and the rest of `logs/g3/`.
* Not copied: `data/` (kink6/kink7 cyclic sets, top sets, independent cores and rows, about 22 GB; regenerable with steps 1-3
  below), the working notes.
* Reproduce (the chain behind one line of table 4.1, on the Studio):
  1. tables: repo `edge_relaxation/export_tbl.py` -> data/lat_rec*.tbl (independent: `src/indep/mklat.py` -> data/indep/*.rows);
  2. Cyc(Kb): `bin/kink6 lat.tbl 3 full ...`, then `run_k6.sh LAT 4 14` (kink6 incr) and `run_k7.sh LAT ORBIT 15 Kb PREV`
     (kink7, one phase orbit); independent: `bin/indep_b core ROWS t0 j0 p0 Kmax OUTDIR threads 3` (Kmax <= 20) and
     `bin/indep_g3 corefrom ROWS Core(20) 20 Kmax OUTDIR threads 3` (Kmax <= 23);
  3. TopCyc(4): `bin/ktop lat.tbl 4 full data/top/top_4.bin` (independent: `bin/indep_b topcore ROWS 5 OUTDIR`);
  4. start phase: `src/select_phase.py CYCFILE Kb m 4 data/top/top_4.bin` (BEST line);
  5. forward: `bin/kfwd3 data/lat_rec2.tbl 27 4 data/k7/rec2_K23_o0.bin 5 14 1 4000 3 0 data/top/top_4.bin 4`
     (expect `EMPTY at step 49`); independent: `bin/indep_b fwd data/indep/rec2.rows 27 23 data/k7/rec2_K23_o0.bin 4
     data/indep/top/top_4.bin 5 14 1 3 8 27 3`; compare with `src/cmpsteps.py LOG1 LOG2`.
  The rec0 K = 23 run takes 6,356 s and 16.5 GB, its filter Cyc(19) 2,262 s and 17.5 GB.
