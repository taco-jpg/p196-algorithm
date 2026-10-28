# W7 KINK.md -- decimal p=8 lattice exterior: does an exactly periodic centre ("kink") exist?

Status at wrap-up (session ended early by owner). Labels: COMPUTED / PAPER PROOF / UNDECIDED, exact scope given.
No decimal cycle found; no certificate; nothing to replay.  The question for ALL widths is UNDECIDED.

## 1. Setting (re-derived, validated)  [COMPUTED]
* Pair word P_i = d_i + d_{n-1-i}; step = carry-normalise P to digits O, n' = n+gam, P'_x = O_x + O_{n'-1-x}.  Lower-half coordinates with ascending
  carries and "descending" carries D (carry into the mirror cell); per cell P' = 2P + a + D - 10(a'+D').
* Lattice (W3, p=8, g=10101010, m=20, two SCCs; m=48 for rec2; p12 m9) is a valid bulk solution (free_evo.py, plain pair-word RAR).
* Centre drift: h=ceil(n/2) advances 2 per 8 steps; smallest symmetry-compatible time T=80 (m=20), 192 (m=48), 72 (p12m9).  Any kink = cycle of the
  finite window map, so its period is a multiple of T (4 phase classes o = n mod 4 for lat0/lat2, 3 for p12m9).
* The two m=20 SCCs are the SAME lattice shifted (L1_{t+6}[j+5]=L0_t[j], 0/160 mismatches); NO mirror relation (124/160 disagree) => no phase-slip kink;
  lattice has complement symmetry 18-L (shifts (5,2),(15,6)).
* Validation: code/lib7.py (RAR digit list vs big-int vs pair-word, 3000 cases), code/win.h window map vs full pair-word evolution (60,000 random steps,
  0 mismatches), SAT encoding code/sat_kink.py: free-mode solutions replayed through win_step 0 mismatches; horizon mode == DFS exactly (w=5 o=1 SAT at H=22,
  UNSAT 23; w=6 o=0 -> 20, o=1 -> 23, both tools agree).

## 2. Methods
* DFS (surv.cpp): bottom-up pruned search over 19^w windows with ternary simulation; cost x8-10 per width unit (w=7: 52 s).
* SAT (sat_kink.py, CaDiCaL, 1 thread): exact window map as CNF, modes per (period-T orbit), hor (survive H steps), free (control).  Cost ~x2-3 per width unit
  (periodic T=80, lat0, o=0: w=5 1.1 s, w=6 4.2 s, w=7 6.7 s, w=8 16 s)  => far better than DFS.
* Key logic point: a kink of ANY period survives forever, so "no window of width w survives H steps from phase 0 in all 4 classes" excludes kinks of every
  period at that width (stronger and cheaper than T=80 periodic search).

## 3. Scope of exclusions (lattice 0 = rec0, m=20, T=80)
* [COMPUTED, DFS and SAT agree] max lifetime L(w) (steps survived, over o=0..3): w=5: 22, w=6: 23, w=7: >= 28 (SAT; w=7 o=0..3 = 28,27,24,26 -- the SAT
  numbers for o with small start H were checked by bisection from H=2w).  Every o class has finite lifetime => NO kink (any period) with free window
  width <= 7 in the lower half.  (Extends W3's width <= 5.)
* [COMPUTED, SAT only, partial] w=8: lifetime o=0: 32, o=1: 34 (o=2,3 NOT run); w=9: o=0: 36, o=1: 38 (o=2,3 NOT run).  So w=8,9 are excluded only for
  the phase classes o=0,1; o=2,3 pending (minutes each by SAT).  T=80-periodic orbits: UNSAT for w=5..8, o=0 only.
* Not run: rec1 (should equal rec0 by the shift relation), rec2 (T=192), p12m9 (T=72) beyond the earlier w=5 exclusions (rec2, p12m9: no window of width 5
  survives T steps; DFS).
* Observed: L(w) grows ~ +4 per extra width unit (22,23,28,34,38), i.e. a disordered core of width w lives ~4w steps: core growth rate ~1/4 cell/step.

## 4. Obstructions
* mod 9: s_{t+1}=2 s_t; kink with T=80 => 3 s_t = 0 mod 9 (Lambda_t = 0 mod 9 for all lattices): necessary congruence s_t = 0 mod 3, NOT a contradiction [PAPER+checked].
* mod 11: N_t = 0 mod 11 at all times for this parity pattern; no contradiction.
* Heuristic [UNDECIDED, not a proof]: generic disorder invades the lattice (wall speed ~ -0.2/step in free_evo.py); a bounded kink needs wall speed +1/4
  relative to the lattice, i.e. a "gun" satisfying ~80 interface carry-bit constraints per period; expected number of kinks ~ rho^80 per width, negligible,
  but no all-width theorem.  Windows survive up to ~4w steps, so the width needed to reach 80 steps is w ~ 20 -> exhaustive exclusion needs w >= 20 (SAT
  extrapolation: x2-3 per width => w=12-14 maybe hours single-thread; w=20 not reachable by brute force; a stronger argument is needed).
* No ordered (neutral/absorbing) core: no other reachable SCC and none self-mirror (ordered-core route belongs to W6).

## 5. Studio plan -> see STUDIO_JOBS.md
## 6. Open items / next steps
1. Finish o=2,3 for w=8,9; extend lifetimes w=10..14 by SAT (lifet.py), lat0 first, then rec2 (Hin up to 192) and p12m9.
2. Replace brute force: cut-state NFA / transfer-operator on the interface carry bits; relaxation bound on max wall speed; this would give an all-width answer.
3. If SAT 'per' mode ever returns SAT: decode (verify_sat.py logic in code/sat_verify.py), build integer, replay >= 20,000 plain big-int steps, save JSON, STOP.
