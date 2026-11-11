# r14a: the period-8 decimal lattices of the interface-graph SCC, centre closure lattice by lattice, all periods

Run directory `~/p196_run/r14a` (compute machine). Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF / UNDECIDED.
**No certificate was found. Nothing here is a claim about 196; no Lychrel number is proved.** The status tables were regenerated
on 2026-11-11 (UTC) from the logs after the last (tier-4) reruns had finished; they replace the agent's draft tables.

## 0. Summary

Setting (r13b sections 1-2, r12g sections 1-3, round 13): base 10, clock g = 10101010 (t mod 8). The interface graph IF(8) of
8-periodic rooted heads (r13c, round 13) has three non-trivial SCCs: the 20-cycles of rec0 and rec1, and one SCC of 1,056 nodes
(1,104 edges) containing rec2 (`../tails_no_centre/`, `logs/if_10_8.txt` there). Every primitive closed walk of this big SCC is the
bulk word W of a period-8 lattice. Phase phi = (t, j, par), phase orbits of length T = 4L (L even) or 8L (L odd), window relaxation
R_K, exact fold map F_K, accepting state = bottom cell off lattice.

- All 636 primitive closed walks of length <= 160 of the big SCC fall into 85 classes under time rotation by 2, spatial shift and
  complement (class 0 = rec0/rec1, class 1 = rec2 (L = 48), 83 classes with L in 61..159).
- **COMPUTED + Theorem A (PAPER PROOF): 55 of the 83 classes are closed for all periods**: for every phase-orbit class the
  all-period closure Cyc_acc(K) is empty at some K0 (16 <= K0 <= 39), F_K has no periodic orbit inside Cyc_acc(K) for K < K0
  (0 exact orbits in 8,979 level lines), and depth 0 is excluded by plain addition. So these lattices have no centre of any
  depth and any time period. L of the closed classes: 61, 64, 69, 92, 97, 102, 104, 111, 118, 119, 124, 125, 126 (x3), 130 (x4),
  132, 133 (x4), 137 (x3), 138, 139, 140 (x3), 144 (x2), 146, 152 (x6), 153, 158 (x4), 159 (x9).
- 28 classes are budget-limited (all-period closure not empty when the per-job memory cap was hit; up to 32 GB, K up to 34):
  UNDECIDED. Class ids 9, 20-25, 32-35, 47, 51, 52, 61, 63-73, 76, 80 (L = 109, 126, 133, 140, 145, 150, 152, 157, 159).
- **Family closure (Theorem F):** over all closed walks of the big SCC at once (rec2 carved out), exact fold cycles 0 at every
  level K <= 21: no lattice of the big SCC other than rec2 has a centre of exact depth 1..21 of any period (COMPUTED + PAPER
  PROOF). K = 22 exceeded 75 GB; the all-depth family statement is UNDECIDED.
- rec0, rec1, rec2 themselves: nothing new (r12g/r13b depth bounds; task K1).

## 1. Reduction: closed walks, all periods (PAPER PROOF; same objects as r13b section 2)

Fix a lattice W (clock g = 10101010, time period 8, bulk period m) and a phase orbit O of nu (length T = 4m for even m, 8m for odd
m). States of R_K on O are pairs (phi, w), w in {0..18}^K, phi in O; edges as in r12g Lemma 3 (free carry Din in {0,1} entering
from above, free top digit at frame shifts). A state is accepting if its bottom cell is off lattice: w_0 != L(t, c).

**Definition.** Cyc_acc(K) = states of R_K (on O) lying in a strongly connected component of size >= 2 that contains an accepting
state; equivalently the states lying on some closed walk (of any length) through an accepting state (the graph is layered by O,
so every closed walk has length >= 2).

**Lemma A1 (centre -> accepting closed walk).** Let X be a centre of any period and exact depth D >= K >= 1 with frame phases in O
(depth as in r12g section 1, frame c_t = h_t - D). Then the bottom K cells of X in this frame form a closed walk of R_K through an
accepting state, so every window state of X in that frame lies in Cyc_acc(K).
*Proof.* r12g Lemmas 2, 3: the D-window states form a periodic orbit of F_D with phases following nu (hence staying in O); by
Lemma 3 the projection to the bottom K cells is a closed walk of R_K. D is the exact depth, so at some time the column
c_t = h_t - D is off lattice: the bottom cell of the K-window is off lattice. QED

**Lemma A2 (incremental).** For K >= 2, Cyc_acc(K) is contained in Cyc_acc(K-1) x {0..18}.
*Proof.* A closed walk of R_K through an accepting state projects (drop the top cell, r12g Lemma 3) to a closed walk of R_{K-1}
through a state with the same bottom cell, hence an accepting one. QED

**Lemma A3 (exact orbits).** If F_K has no periodic orbit inside Cyc_acc(K), there is no centre of exact depth K in O.
*Proof.* A centre of exact depth K is a periodic orbit of F_K lying in Cyc_acc(K) by Lemma A1. QED

**Theorem A (all periods).** If Cyc_acc(K0) is empty for some K0 >= 1 and F_K has no periodic orbit inside Cyc_acc(K) for
1 <= K < K0, then there is no centre of any period and any depth >= 1 with frame phases in O.
*Proof.* Depth D >= K0: Lemma A1 with K = K0 would give a state in the empty set. Depth 1 <= D < K0: Lemma A3 with K = D. QED

**Depth 0.** A depth-0 centre (no defect at all, the lattice itself up to the fold) is tested directly with plain big-number
addition at every phase (`src/depth0.py`): 258 orbit lines over all 85 representatives, none possible (`class/depth0.txt`).

**Fixed period.** E_acc(K,T) := states on a closed walk of length exactly T through an accepting state. If E_acc(K0,T) = {} and F_K
has no orbit of period dividing T inside E_acc(K,T) for K < K0, then there is no centre of period dividing T at any depth >= 1
(r13b Theorem R4; same proof). Used only as a consistency check here (`src/check_consistency.py`: 173 pairs of runs, 4,717 levels,
E_acc <= Cyc_acc at every level, 0 violations).

**Symmetries.** For r in Z/4, c in {0,1}, sigma in Z/m let W' be the lattice W'(t,x) = C^c W(t + 2r, x + sigma) (C = complement
18 - .). The clock is 2-periodic and complement commutes with both carry streams, so (t, j, par, w) at W' <-> (t + 2r, j + sigma,
par, C^c w) at W is a conjugacy of F_K and R_K preserving "accepting". Hence results transfer along the class and between orbits
identified by the stabiliser; `src/symcheck.py` confirmed the predicted identifications by direct computation for K <= 11 on
classes 1, 2, 3, 4, 7, 12, 16, 30 (`logs/symcheck*.log`).

**Family version (Theorem F).** Let F be a set of edges (I, v) of the interface graph; interface data c_I(t) (forward carry into the
bottom of the window), xb_I(t) (previous column at g_t = 1), A_I(t) (admissible descending carries) replace the lattice tables UP,
RB1, BOK in the window rule; the state is (t, par, (I, v), w), and at a frame shift (g_t = 1, par = 0) the leaving cell must equal
v(t+1) and (I, v) moves to (delta(I, v), v') for any out-edge (delta(I,v), v') of F. By r13c Lemma I1 (locality of interfaces),
every lattice whose bulk word is a closed walk in F, at a frame deep inside its bulk, has its windows on closed walks of this family
graph; and any closed walk of the family graph is a closed walk of R_K of the lattice given by its closed edge walk. Define
Cyc_acc^F(K) as for Theorem A; the edges on the four 48-cycles (the words of rec2) are tagged, and an SCC is kept only if it
contains an accepting state and a layer whose edge is not tagged; a closed walk of the SCC graph that is not a power of a 48-cycle
uses an untagged edge (the 48-cycles are vertex-disjoint), so the carve-out loses no other lattice.
**Theorem F.** If Cyc_acc^F(K0) (with carve-out) is empty and the exact step graph (F_K with branching only at frame shifts) has no
cycle inside Cyc_acc^F(K) for 1 <= K < K0, then no lattice of F other than rec2 has a centre of depth >= 1 of any period. Without
emptiness, the absence of cycles for K <= K1 gives: no such centre of exact depth D <= K1.
The family is computed in phase class A = {(t, par): (0,0),(1,1),(2,1),(3,0),(4,0),(5,1),(6,1),(7,0)}; class B is its image under
the automorphism R (time rotation by 2), checked at K <= 8. The quotient by <R^2, C> (order 4; the SCC is invariant under R and C
as a labelled graph, `src/symgraph.py`, 0 mismatches) uses canonical states; quotient counts weighted by orbit size agree with
the non-symmetric counts (K <= 8).

## 2. Results per class

`class/compact_table.txt` (one line per class) and `class/table.md` (one line per class and phase-orbit class: status, last K,
peak, exact orbits) are generated by `src/mk_compact.py`, `src/mk_table.py` from `logs/sweep_scc.txt`, `logs/rerun_scc.txt`,
`logs/sweep_run.txt`; `class/summary.txt` by `src/mksummary.py`:

    Classes with T >= 256: 83. Closed for all periods (every orbit class EMPTY): 55. Death level K0: min 16, max 39;
    peak |Cyc_acc| per job: max 57,808,125; exact-orbit lines: 0. Partial: 0. No orbit class closed within the budget: 28.

Change against the agent's draft: class 36 (L = 152, `latw/w152_14.txt`) was partial (3/4); its last orbit class (orbit 0) closed in
the tier-4 rerun at 32 GB: EMPTY at K = 39, peak 57,808,125 (`logs/rr_scc_c36_o0.log`). The tier-4 reruns of classes 9, 23, 25
reached K = 32-34 with 1.4-1.7e8 states and stayed BUDGET. Per-job logs: `logs/job_logs.tar.gz` (`sw_scc_c<class>_o<orbit>.log`
= first sweep, 7 GB; `rr_scc_*` = reruns, 14 or 32 GB; `sw_run_*` = fixed period T_min).

## 3. Controls

- **Fixed-period chain (`mc14a` = round-13 mc13c + memory/time watchdog, rule unchanged):** rec0 orbit 0: E_acc(44,80) = 709,
  EMPTY at K = 45; rec2 orbit 0: E_acc(24,192) = 32,130,849, EMPTY at K = 40 (r13b's numbers; `logs/ctrl_rec0_o0.log`,
  `logs/ctrl_rec2_o0.log`).
- **Positive controls (all-period closure):** base-9 lattices b9r0/b9r1 (Lean-verified centres): exact periodic orbits appear at
  K = 1, 3, 5, 7, 9, 11 in the orbit carrying the centre and the sets do not die up to K = 12; the phase orbits without centres die
  at K = 1 (`ctrl/pos_control.txt`, `ctrl/scc_b9*.log`).
- **Negative control:** p12m9 (three orbits) dies at K = 6, identical to the round-13 main-session logs (`ctrl/scc_p12m9_o*.log`).
- **Selftest:** genuine big-number addition vs F_K and R_K on all 85 class representatives (`class/selftests.txt`).
- **Second pipeline** (`src/indep_scc.cpp`: r13b indep_acc rule with genuine carries, Kosaraju SCCs, functional-graph exact orbits;
  input rows from `src/mk_indep_scc.py`, `rows/`): identical |Cyc_acc|, accepting and exact-orbit counts at every level K = 1 ..
  EMPTY level for w61_0 orbits 0, 1 (K0 = 25), w102_0 orbits 0, 3 (K0 = 18, 25) and w64_0 orbit 0 (K0 = 31)
  (`logs/ctrl_indep.log`, `logs/ctrl_indep2.log`, `ctrl/indep_*.log`).
- **Third code (main session, plain Python `../tails_no_centre/pyscc.py`, explicit carries along the whole word, plain Tarjan):**
  w61_0 orbit 0, levels K = 1..21 identical to `logs/sw_scc_c7_o0.log` (|Cyc_acc| and accepting counts) (`ctrl/pyscc_w61_0_o0.out`).
  The run was stopped at K = 21 (no output after 2026-11-10 06:11 UTC; not running any more); K = 22..25 (EMPTY at 25) were not
  reached by this code.
- **Family program (`src/mc14f3.cpp`):** single-lattice families w61_0, w64_0, w102_0: classes A/B = orbit pairs; at every level
  E_acc and accepting counts equal the sums of the single-lattice runs, EMPTY at the same K (`logs/famtest_*.log`, `fam/w*_A.log`,
  `fam/w*_B.log`); full SCC family: quotient weighted count = non-symmetric count and class A = class B for K <= 8.

## 4. Family-wide closure (Theorem F): all lattices of the big SCC at once

The family closure can die only after every lattice of the SCC has died (it is the union over all closed walks). Result
(`fam/all_A_c1_s1.log`, quotient by <R^2, C>, class A, rec2 carved out): K = 1: 4,034 quotient states, K = 8: 672,759, K = 16:
33.8 M, K = 21: 222,739,963 (8.9e8 upstairs), exact fold cycles 0 at every level K <= 21; K = 22 exceeded the 75 GB cap.
Hence (Theorem F, depth-bounded form) no lattice of the big SCC other than rec2 has a centre of exact depth 1..21 of any period.
The all-depth family statement is UNDECIDED (growth about 1.42 per level).

## 5. UNDECIDED

- the 28 budget-limited classes (for these the fixed-period runs, where listed in `class/table.md`, exclude only centres of
  period dividing T_min, at the depths reached);
- lattices of the big SCC with bulk words of length > 160, except for the family-wide bound depth <= 21;
- rec0, rec1, rec2 for all periods beyond r12g's depth bounds (depth >= 24 / 28); task K1 itself;
- left parts on clock 10 that wander in the big SCC without being periodic, beyond depth 21.

## 6. Commands (run directory `~/p196_run/r14a`; the scripts `chdir` there)

    clang++ -O3 -mcpu=native -std=c++17 -pthread src/mc14a.cpp -o bin_mc14a      # likewise src/indep_scc.cpp, src/mc14f3.cpp
    python3 src/walks.py 160 latw                         # 636 primitive closed walks of length <= 160 (latw.tar.gz)
    python3 src/classes2.py latw/w*.txt lat/rec0.txt lat/rec1.txt lat/rec2.txt   # class/classes.json, classes.txt
    python3 src/check_subset.py                           # every simple-cycle lattice of the main-session list is in a class
    ./bin_mc14a selftest LAT SEED COUNT                   # class/selftests.txt (src/selftest_all.sh)
    ./bin_mc14a runscc LAT ORBIT KMAX THREADS 1           # Cyc_acc(K), exact orbits of any period
    ./bin_mc14a run LAT ORBIT KMAX THREADS 1              # E_acc(K, T_min)
    python3 src/sweep.py scc 10 7 5400 all                # first all-period sweep: logs/sweep_scc.txt, logs/sw_scc_c*_o*.log
    python3 src/rerun_budget.py scc RSSGB SEC THREADS WORKERS    # reruns: logs/rerun_scc.txt, logs/rr_scc_c*_o*.log; tier 4: src/tier4.sh
    python3 src/sweep.py run ...                          # fixed period: logs/sweep_run.txt
    python3 src/depth0.py $(cat class/rep_list.txt)       # class/depth0.txt
    python3 src/symcheck.py <class ids> ; python3 src/symgraph.py
    sh src/ctrl_indep.sh ; sh src/ctrl_indep2.sh          # second pipeline comparisons
    python3 src/famexport.py fam/all.fam all ; ./bin_mc14f3c fam/all.fam KMAX THREADS CARVE PHASECLASS SYM ; python3 src/famtest.py LAT KMAX THREADS
    python3 src/mksummary.py ; python3 src/mk_compact.py > class/compact_table.txt ; python3 src/mk_table.py > class/table.md ; python3 src/check_consistency.py

Each closed all-period job took at most 1.5 h on one thread (7-32 GB). Lattice files: `latw.tar.gz` (the 636 words, format of
the round-13 mc13b/mc13c lattice files), `lat/` (rec0, rec1, rec2, p12m9, b9r0, b9r1).
