# Round 7 design: backdisk (backward cone, external memory)

## Inputs that were not available
The task named `results/Agent10E2P24UniformCones.md`, `THEORY.md` section 7, `Agent11E2P16M8AllTime`, `agent11_p48_m4_charge.py`,
`calculation/neutral_band_search.py`, `Base9.lean`, `Agent6NineRailCentreRenewal`, `Agent120`. None of them is on this Mac (home, ~/Projects) or on studio.
So this design is built from `reachdisk.cpp` alone. Consequences:
- M1 (explicit port words) is fully specified and can be run. A hit could not be verified against `cycleOK`/`neutral_band_search.py` here.
- M2 (lattice cuts, charge) cannot be built: the 128 lattice cycles and the charge function are missing. M2 stays UNDECIDED (blocked).
- C4 (Base9 lattice positive case) is blocked for the same reason.

## Graph (identical to reachdisk)
Key = (c, d, r): carry stream c (T bits), d stream (T bits), r digits (4 bits) at the NOV overflow steps. Step: choose x0 in [0, 2B-2]; for t = 0..T-1
with running value x: choose d_t with floor((x+d_t)/B) = dneed_t; e = (x + cin_t) mod B; r = (x + d_t) mod B; co = floor((x + cin_t)/B);
next x = e + (ovf_t ? r_in(t) : r); need x_T = x0. The successor is (co stream, d stream, r at overflows). Bottom interface: c = 0, d = overflow mask, r = 1 at overflows.
Root rule: the edges leaving the bottom interface use x0 >= 1 and x_t >= 1 for all t. ROT=1: states are orbits under the shift by the clock period; the bottom and the target sets are shift-closed.

## Predecessors
Given J = (cs, ds, rs), find all I = (cc, cd, cr) and x0 with step(I, x0) = J.
Known at each t: d_t = ds_t, co_t = cs_t, and at overflow steps r_t = rs nibble. Unknown: cin_t in {0,1}, cr nibble in [0, B-1] at overflow steps, x0.
Constraints: floor((x + cin)/B) = co_t; at overflow steps (x + d_t) mod B = r_t; cd_t = floor((x + d_t)/B); next x = e + (ovf_t ? cr_nibble : (x + d_t) mod B).
Pruning: a backward table G[t][x] (bit mask over x0) says which x0 can still be closed from (t, x). DFS only enters (t+1, nx) when bit x0 of G[t+1][nx] is set.
So the work is proportional to the number of predecessors (times T), never 2^T. The root-valid bottom predecessor is flagged during the same DFS.

## Reverse BFS
Layer 1 = target keys (canonical under ROT). Layer h = predecessors of layer h-1 not in any earlier layer. External memory is reachdisk's:
1024 hash buckets, sorted base/delta generations, manifest as the only commit point, resumable.
- REACHABLE: while expanding a layer-(h-1) state (distance h-2 from the targets) a predecessor equals the bottom key and the DFS satisfied the root rule.
  Height = h-1 (one root edge plus h-2 steps). Checked for every generated predecessor, so the first hit is the shortest.
- UNREACHABLE (COMPLETE): a layer has no new state. Then no state of the cone, in particular no root successor, leads to a target.
- Guards: cap on cone size, disk free (checked each layer and while generating candidates), RSS 200 GB.

## Targets (spec arguments)
`bands` (all uniform bands whose period divides T, all phases), `band:v1,v2,..:phase`, `stream:BITS` (the 9-wire stream, d = complement of c, r = (B-1) c_t at
overflows, plus all its shifts by multiples of the clock period, so the set is closed under the shift).
M1 specs: for each of 01000101, 10111010 (period 8) and 1000100001110111 (period 16) repeated to length T, offsets 0..3 (the alignment convention is not relied on).

## Validation
See VALIDATE_R7.md. Self test (random forward edges vs predecessors), known heights (55, 75, 13, 18, 29, 53, 53), negative cases (clock 01 T=8; T=24 period-8 words).

## Bidirectional fallback (step D3)
If the backward cone explodes, forward reachdisk runs to height H and backdisk to depth D, and the visited sets (same key format, same bucket function) can be intersected
bucket by bucket. An empty intersection with no side complete only gives "no path of height <= H + D" and is UNDECIDED.

## Labels
REACHABLE (with a verified replay) = candidate; UNREACHABLE (COMPLETE) = COMPUTED; TOO_BIG / blocked = UNDECIDED. A finite replay is not a certificate.

## Window filter (added during the run; env WIN=w)
Without pruning the backward cone is huge because it contains many interfaces that the forward graph can never reach (forward T=32 clock 0001 has only 2.8M orbits, the
backward cone passed 3e9). `bands/window.cpp` and `backdisk` build a sound over-approximation that does not depend on T:
- A window is the content (c, d, r at the overflow slots) of w consecutive time slots starting at clock phase ph.
- The running value x at the window start is unknown (any of 0..2B-2) and the closure x_T = x0 is dropped.
- Every real edge I -> J gives an abstract edge between the window contents of I and J. So the windows of every real reachable interface, of any period T, lie in the
  closure A_w(ph) of the bottom pattern under the abstract step (one set per phase).
- In the predecessor DFS a partial assignment is dropped as soon as a completed window (any start slot) is outside its set. A pruned interface is not reachable from the bottom,
  so neither answer (REACHABLE / UNREACHABLE) changes. Target keys with a bad window are dropped at the start (they are unreachable for every T).
- w = 8: 2.6M abstract states (phase 0); w = 10: 28,699,436, 25,467,296, 114,741,888 and 97,404,348 states (phases 0..3). Larger w prunes harder (P=48: the cone is 272M states with w=10, while w=8 was still at +128M per layer
  at 3.3e9).
Soundness checks: the self test also asserts that every state on a random forward walk passes every window (300,000 edges per configuration, 0 violations); N12 is still reached at
height 53 for T=24 and T=48 with w=10. The windows say nothing about closure at the period T, so they never exclude a state that the exact graph reaches.
