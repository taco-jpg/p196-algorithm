# FILTER_R8 — the window filter: definition, soundness argument, exhaustive check

Code: `bands/backdisk.cpp` (`buildWindowSet`, `winOK`, env `WIN=w`), `bands/window.cpp` (stand-alone version), forward check `bands/reachdisk_wc.cpp` (env `WINCHECK=w`).

## 1. The graph (as in reachmt / reachdisk / backdisk)
An interface is I = (c, d, r): c, d in {0,1}^T and, at each overflow slot t (clock bit 1), a digit r_t in 0..B-1.
One edge I -> J chooses x_0 in [1, 2B-2] (root edge) or [0, 2B-2], and then runs t = 0..T-1 with a running value x_t:
* choose d'_t in {0,1} with floor((x_t + d'_t)/B) = d_t;
* e = (x_t + c_t) mod B, r' = (x_t + d'_t) mod B, c'_t = floor((x_t + c_t)/B);
* x_{t+1} = e + (r_t if t is an overflow slot else r'), and the digit r' is stored in J at an overflow slot.
The edge exists iff x_T = x_0. J = (c', d', r'). The root edge uses x_t >= 1 for all t. The bottom interface is c = 0, d = overflow mask, r = 1 at overflow slots.
Always 0 <= x_t <= 2B-2 (e <= B-1 and the digit added is <= B-1).

## 2. Definition of the window sets
Let L be the length of the clock word and w the window width. For a clock phase ph in 0..L-1 let ovf_ph(j) = clock[(ph + j) mod L], j = 0..w-1.
A window content is W = (c_0..c_{w-1}, d_0..d_{w-1}, r at the overflow slots j of the window).
The abstract step A_ph(W) is the set of all W' = (c', d', r') obtained by running the same per-slot rule for j = 0..w-1 from ANY start value x_0 in 0..2B-2,
with **no** closing condition x_w = x_0 and no root condition.
A_w(ph) is the smallest set that contains the bottom pattern W_bot(ph) = (c = 0, d = ovf_ph, r = 1 at overflow slots) and is closed under A_ph.
(It is computed by BFS; for w = 10, clock 0001 the four sets have 28,699,436 / 25,467,296 / 114,741,888 / 97,404,348 elements.)

The filter says: an interface I of period T (T a multiple of L) is "window-admissible" iff for EVERY start slot s with 0 <= s and s + w <= T the content of I on
slots s..s+w-1 lies in A_w(s mod L). Windows never wrap around T.

## 3. Why every reachable interface is admissible (argument)
Claim: if I is reachable from the bottom interface (by any number of edges, the first being the root edge), then I is window-admissible, for every T, every w, every s.

Proof by induction on the number of edges.
* Base: the bottom interface restricted to slots s..s+w-1 is exactly W_bot(s mod L), which is in A_w(s mod L) by definition (the overflow pattern of the clock on those slots is ovf_{s mod L}).
* Step: let I -> J be an edge with running values x_0, ..., x_T (x_T = x_0). Fix s. The per-slot rule at slot t uses only (x_t, c_t, d_t, r_t if t is an overflow slot) and produces (c'_t, d'_t, r'_t) and x_{t+1}.
  So the content of J on slots s..s+w-1 is obtained from the content of I on the same slots by running the per-slot rule from the start value x_s, which lies in 0..2B-2. That is exactly one application of A_{s mod L} with start value x_s.
  By the induction hypothesis the content of I on those slots is in A_w(s mod L). Because A_w(s mod L) is closed under A_{s mod L}, the content of J is in A_w(s mod L) as well.
  The edge also needs x_T = x_0 and (for the root edge) x_t >= 1: the abstract step ignores these conditions, so it only allows more, never fewer, successors. ∎

Consequences used by the tools:
1. **backdisk pruning:** in the predecessor DFS a partial assignment is dropped as soon as a completed window falls outside its set. A dropped partial assignment cannot be completed to a reachable interface, so no path from the bottom to a target passes through it. Therefore REACHABLE and UNREACHABLE answers (and the first height) are unchanged. Target keys with a non-admissible window are unreachable for every T.
2. **ROT=1:** the canonical representative of an orbit is a rotation by a multiple of the clock length; the family of all windows (all s) is invariant under such a rotation, and the rotated interface is reachable iff the original is (the bottom interface is fixed by the rotation and the rule commutes with it). So pruning on raw predecessors and storing canonical keys is consistent.
3. The sets do not depend on T. The filter at P = 48 uses the same sets as at P = 24.

What the argument needs from the code (and what the checks below test): the code's abstract step is identical to the per-slot rule (same lines as `Expander::dfs`), the start value x_s ranges over all of 0..2B-2, the overflow digit bookkeeping (`wpre`, `wNOVp`) extracts exactly the digits of the window's overflow slots, and the check `winOK` is applied for every start slot s (not only multiples of L).

## 4. Exhaustive check (forward, all reachable interfaces)
`reachdisk_wc` = reachdisk with `WINCHECK=10`: every successor state produced by the BFS (before de-duplication, all candidates of every height, all T-s windows) is tested with `winOK`. A single failure would print `WINDOW VIOLATION` and the P = 48 conclusion would be withdrawn.
Runs: clock 0001, T = 12, 24, 32, 40 (T = 24, 32, 40 are the sizes asked for; P = 48 uses w = 10, so w = 10 is used).

| task | filter | height reached | candidate states checked (all windows each) | violations |
|---|---|---|---|---|
| clock 0001, T = 12, COMPLETE (45,570 orbits) | w = 10 | 71 (empty) | 45,759 | **0** |
| clock 0001, T = 24, COMPLETE (6,625,354,893 orbits, same count as round 6) | w = 10 | 1346 (empty) | 6,626,085,128 | **0** |
| clock 0001, T = 32, COMPLETE (2,815,872 orbits) | w = 10 | 13 (empty) | 2,865,897 | **0** |
| clock 0001, T = 40, COMPLETE (132,509,676 orbits) | w = 10 | 13 (empty) | 132,850,243 | **0** |
| clock 0001, T = 48, partial (TOO_BIG at the cap, heights 1..4) | w = 10 | 4 | 4,134,634,272 | **0** |
| clock 01, T = 16, COMPLETE (257,093,986 orbits) | w = 8 | 592 (empty) | 258,054,380 | **0** |
| clock 01, T = 32, partial (cap 4e9, heights 1..15) | w = 8 | 15 | 4,896,252,176 | **0** |
| clock 01, T = 24, partial (cap 3e9, heights 1..64) | w = 8 | 64 | 3,047,686,965 | **0** |

"Candidate states" are all successor states generated by the BFS before de-duplication (every one is a reachable interface), each tested against every window start s = 0..T-w.
T = 12, 24, 32, 40 with w = 10 are exhaustive: the forward BFS is COMPLETE, so these are all reachable interfaces (as orbits under the clock shift, which is harmless: the window family is rotation invariant).
T = 48 is not exhaustive (the forward set is too large; the check covers the first four heights). The P = 48 conclusion therefore rests on the argument of section 3 plus the exhaustive checks at the smaller T (the sets do not depend on T), not on an exhaustive forward enumeration at T = 48.
The clock-01 rows are the check for the w = 8 filter used in M2 (T = 16 exhaustive, T = 24 and T = 32 partial).

**Verdict: no violation anywhere, so the P = 48 result (UNREACHABLE, COMPLETE) is kept as COMPUTED.** Its premises are the argument in section 3 (a proof, not only a test) and the code checks above.

