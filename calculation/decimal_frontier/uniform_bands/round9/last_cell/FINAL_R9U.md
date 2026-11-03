# Round 9u — the last uniform-band cell (T = 32, left-end clock 0000111000110001)

Labels: COMPUTED / UNDECIDED only. "UNREACHABLE" is a statement about the reach graph of reachmt / reachdisk / backdisk
(premise (B) of ReachDiskRounds6to8: reach graph = Agent120 exterior system, checked, not proved — unchanged).
Studio directory `~/p196_run/r9u/` (sources, logs, DECISIONS.md); copy on the laptop `~/Desktop/p196_studio/r9u/`.
Nothing in `~/p196_run/r9/`, `~/p196_repo` or other processes was touched.

## 0. Result

**(T = 32, clock 0000111000110001): no uniform band (the four targets with period | 32: {0}, {18}, {6,12} both phases) and no 9-wire
stream is reachable from the bottom interface at any height. UNREACHABLE (COMPLETE) — COMPUTED.**
Premises: (A) the forward window abstraction of FILTER_R8 (proof + checks, extended here to wrapped windows), (C) the new
co-reachability window filter (proof in section 2, exhaustive checks in section 4), and premise (B) as before.

| run | filter | result | size | time |
|---|---|---|---|---|
| forward, T=32, ROT=1 (quotient by the 16-shift) | co-windows w = 8 (all 23 + 7 wrapped windows) | **frontier empty after height 294; 0 band targets, 0 wire streams** | 13,065,715 orbits; 13,670,306,208 successor candidates generated, 13,657,226,827 dropped by the filter | 2,919 s, 12 threads, RSS 2.4 GB |
| same, independent width (cross-check) | co-windows w = 9 | **frontier empty after height 294; 0 band targets, 0 wire streams** | 6,331,756 orbits; 9,870,681,680 candidates, 9,864,342,061 dropped | 2,081 s, 12 threads, RSS 16.4 GB |

Every one of the 13.67e9 generated successors (all are genuinely reachable interfaces) was also tested against the forward window sets
A_8 (non-wrapping and wrapping): **0 violations** (this is also the wrapped-window check of section 3 on this clock).

With this cell closed, together with rounds 6–8 and the paper argument for (24,01), (32,01): every decimal left end with period T ≤ 32
fails to carry a uniform band (under premise (B)).

## 1. What was tried first (kept for the record)
* Backward cone with the forward windows only (w = 10 bitset windows, all 16 phases, + wrapped windows), targets = 4 bands + all
  9-wire keys (1,048,580 survive the windows): layers 0.52M, 28.4M, 180M, 395M, 665M, 1.06G new (2.33e9 states after layer 6),
  still growing ×1.6 per layer; stopped by hand at layer 7 for disk (the other agent's run uses ~300 GB). UNDECIDED. (`logs/main_T32.log`)
  The w = 10 window sets for this clock are 0.19–3.3e9 states per phase (46 GB of bitsets); round 7's w = 8 cone was ×8 per layer.
* The forward search alone (round 6) was 2.0e10 orbits at height 220 with 1e8 new per height.

## 2. The new idea: co-reachability windows (premise C)
For every clock phase ph, BB_w(ph) ⊆ A_w(ph) is the set of window contents W in A_w(ph) from which a **target window** can be reached by a
chain of abstract steps (the same abstract step as A_w: per-slot rule from any start value 0..2B-2, no closing, no root condition) that
stays inside A_w(ph). Target windows = the windows (w consecutive slots, phase ph) of target interfaces: 9-wire interfaces
(d = complement of c, r = 9 at overflow slots with c = 1, r = 0 with c = 0, every c) and uniform bands (all uniform cycles, every phase;
a superset of the four used targets). Computed by a fixpoint over the bitset of A_w (`bwin.cpp`).

**Claim.** If I_0 (bottom) → I_1 → ... → I_n is a path of real edges and I_n is a target, then for every k ≥ 1 and every window start s
(wrapped windows included) the content of I_k on that window is in BB_w(s mod L).
*Proof.* (i) It is in A_w(s mod L) by FILTER_R8 section 3 (and section 3 below for wrapped windows). (ii) Downward induction on k:
the window of I_n is a target window and lies in A_w, so it is in BB_w. If the window of I_{k+1} is in BB_w, then the window of I_k
steps to it by one abstract step (start value x_s of the real edge I_k → I_{k+1}; FILTER_R8 section 3 step), and it lies in A_w,
so the fixpoint puts it into BB_w. ∎

**Use.** The forward BFS (reachdisk) drops every successor having a window outside BB_w. By the claim no interface on a bottom → target
path is ever dropped, so if a target is reachable the pruned BFS still meets it (and at the same first height, since the whole
shortest path survives); if the pruned BFS ends with an empty frontier and no target, no target is reachable. The target test is done on
every generated successor before the filter. The ROT quotient is unaffected (the family of all windows, wrapped ones included, is
invariant under the clock shift).
Forward states satisfy A_w automatically, and states of an A_w-pruned backward cone satisfy BB_w automatically, so the new
information is in the combination forward + BB_w.
Pruning power per window at w = 8 on this clock: |BB|/|A| between 13 % and 70 % per phase (`logs/bwin8_build.log`); on full
interfaces the forward set shrinks from > 2e10 to 1.3e7 orbits.

## 3. Wrapped windows (the open item of rounds 6–8)
* Round 8 tools (backdisk.cpp `winOK`, reachdisk_wc) never used windows that wrap across t = T-1 → 0: `winOK` only tests
  s0 = t1 - w ≥ 0, and the M1/M2 cones were pruned with non-wrapping windows only. So the round-8 conclusions are not affected.
* This round uses them (option WRAP=1 in backdisk_r9u; always in `allInB`). Proof: a real edge has x_T = x_0, so slot 0 receives the
  running value that slot T-1 produced; the content of a wrapped window of J is the per-slot rule applied to the content of I on the
  same slots, started at x_s, with clock phases (s + j) mod L because L | T. The bottom pattern on a wrapped window is the bottom
  pattern of phase s mod L. The induction of FILTER_R8 section 3 goes through word for word.
* Exhaustive forward checks of the wrapped windows (every generated successor, all start slots T-w+1..T-1), 0 violations everywhere:

| clock, T | w | successors checked | non-wrap viol. | wrap viol. |
|---|---|---|---|---|
| 0001, T=12 COMPLETE | 10 | 45,759 | 0 | 0 |
| 0001, T=32 COMPLETE | 10 | 2,865,897 | 0 | 0 |
| 0001, T=40 COMPLETE | 10 | 132,850,243 | 0 | 0 |
| 0000111000110001, T=16 COMPLETE | 10 | 144,898 | 0 | 0 |
| 0001, T=24 (pruned forward, all generated successors) | 10 | 2,143,137,286 | 0 | 0 |
| 0000111000110001, T=32 (pruned forward, all generated successors) | 8 | 13,670,306,208 | 0 | 0 |
| 0001, T=12 (pruned forward) | 10 | 25,978 | 0 | 0 |
| 0000111000110001, T=32 (pruned forward, BB_9 run) | 9 | 9,870,681,680 | 0 | 0 |
| 13, T=10, clock 1010010000 (pruned forward) | 10 | 172,804 | 0 | 0 |
| 4, T=6, clock 011001 (pruned forward) | 6 | 892 | 0 | 0 |

## 4. Validation of the new code
* Bitset storage (`winbits.h`, `wbuild.cpp`) reproduces round 8's hash-set window sets exactly: clock 0000111000110001 w = 8, all 16
  phases (15,475,120 … 54,680,464), and clock 0001 w = 10, all 4 phases (28,699,436 / 25,467,296 / 114,741,888 / 97,404,348).
* backdisk_r9u self test (T=32, this clock, w=10, WRAP=1): 100,000 random forward edges, 0 mismatches (predecessors, forward
  re-step, all windows incl. wrapped).
* Positive control, backward cone, same code: (24, 0001), w = 10 + wrapped windows, targets bands + all 9-wire keys:
  **REACHABLE at height 53** (as in rounds 6–8). 160 s.
* **Positive control, forward with co-windows, same code as the main run:** (24, 0001) with BB_10: **N12 twice
  (101101010010101101010010) at height 53**, nothing else; COMPLETE after height 1344, 35,284,177 orbits (unpruned round 6:
  6,625,354,893 orbits, COMPLETE after 1346, the same single stream). (12, 0001) with BB_10: N12 at height 53, COMPLETE, 3,366 orbits
  (unpruned 45,570).
* Exhaustive co-window check on whole graphs (`pathcheck.cpp`: full graph in memory without quotient, every state on a
  bottom → target path tested against A_w and BB_w):

| case | reachable | first target height | states on bottom→target paths | outside A_w | on path, outside BB_w | off-path states passing BB_w |
|---|---|---|---|---|---|---|
| B=10, T=12, clock 0001, w=10 | 136,652 | 53 | 157 | 0 | **0** | 9,919 of 136,495 |
| B=13, T=10, clock 1010010000, w=10 | 250,301 | 55 | 156 | 0 | **0** | 23,665 of 250,145 |
| B=4, T=6, clock 011001, w=6 | 956 | 9 | 23 | 0 | **0** | 193 of 933 |
| B=10, T=11, clock 00001110001 (p11), w=10 | 18,060 | 29 | 29 | 0 | **0** | 910 of 18,031 |
  (reachable counts equal the round-5 calibration: 136,652, 250,301, 956.)
* Forward with co-windows on the certificate cases, same code: base 13 T=10: band {8,16} phase 0 at **55**, phase 1 at **75**
  (23,821 interfaces instead of 250,301); base 4 T=6: stream 101010 at 9, band {2,4} phase 1 at **13**, stream 010101 at 14,
  band phase 0 at 18 — every target and every first height identical to the unpruned calibration logs.

## 5. Files (studio `~/p196_run/r9u/`, copied to `~/Desktop/p196_studio/r9u/`)
* `winbits.h` (bitset windows, wrapped windows, BB_w family), `wbuild.cpp` (A_w builder), `bwin.cpp` (BB_w fixpoint),
  `backdisk_r9u.cpp`, `reachdisk_wc_r9u.cpp` (forward + window check + BFILT), `pathcheck.cpp`, `wincd.h` (c,d-only windows: written,
  not used — its builder was too slow at w = 12).
* Logs: `logs/fwdB8_T32.log` (main result), `logs/fwdB9_T32.log`, `logs/posB_T24_0001.log`, `logs/posB_T12_0001.log`, `logs/posB_b13.log`,
  `logs/posB_b4.log`, `logs/controls2.log`, `logs/controls3.log` (path checks),
  `logs/pos_T24_0001_w10wrap.log`, `logs/main_T32.log`, `logs/wc_*.log`, `logs/wbuild10.log`, `logs/bwin8_build.log`, `logs/w9_chain.log`.
* Window bitsets `wsets/` (23 GB kept: w = 8 and w = 9 A/BB sets of this clock, clock 0001 w = 10, base 13 w = 10, base 4 w = 6;
  the w = 10 sets of this clock and of p11, 63 GB, were deleted, see DECISIONS.md; all can be rebuilt with `wbuild` / `bwin`).
* Reproduce the main result: `./wbuild 10 0000111000110001 8 wsets 12; ./bwin 10 0000111000110001 8 wsets 12;
  WINCHECK=8 BFILT=1 WINDIR=wsets ROT=1 THREADS=12 ./reachdisk_wc_r9u 10 32 0000111000110001 ALL wd/x 15000000000 0.18` (about 50 min).

## 6. Labels
| item | label |
|---|---|
| (32, 0000111000110001): no band, no 9-wire stream (forward with BB_8, COMPLETE at height 294) | COMPUTED (premises A, C, B) |
| wrapped windows: proof + 0 violations | COMPUTED |
| co-window filter: proof + positive controls + path checks | COMPUTED |
| backward cone w = 10 + wrap | UNDECIDED (stopped, not needed) |
| reach = Agent120 equivalence (premise B) | unchanged: checked, not proved |
