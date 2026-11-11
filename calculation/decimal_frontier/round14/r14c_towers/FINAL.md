# r14c: infinite closed L-histories (ICH) on the open overflow clocks, by exact interface chains

Run directory `~/p196_run/r14c` (compute machine). Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF / UNDECIDED. Nothing here is
LEAN-VERIFIED; nothing is claimed about 196 or about the existence of a decimal Lychrel number. Status of the towers as of
2026-11-11 (UTC), read from the logs in `logs/`; the agent's own report was written before the last towers finished, the
status below replaces its section 3.

## 0. Summary

**Method (PAPER PROOF, section 1).** A relative tower above a fixed L-periodic interface J (the object of r13c, round 13) is
exactly the set of chains J -> J1 -> J2 ... of L-periodic interfaces, each arrow a closed L-column (r13c Lemma I1). With
D(I) := 0 if no closed L-column exists above I, else 1 + max D(successors) (D = infinity iff a cycle is reachable), the tower dies
at level r iff D(J) + 1 = r, and survives forever iff D(J) = infinity. So a tower is decided by a finite DFS over interfaces
(`src/ifb.cpp`, `src/ifc.cpp`); no K-head graph is needed. The DFS is exact; a cycle gives a genuine ICH, not merely a cap.
Merges of interfaces are almost absent (6,789 memo hits among 1.47e9 edges for (01)^12), so a memory-free tree DFS with an
on-stack cycle check (`ifd`, mode `-tree`) suffices, and an exact chunk filter (halving the period; a child is kept iff the two
half-interfaces' boolean reachability matrices close) makes it fast (20-100 k interfaces/s per thread).

**Results (COMPUTED + Proposition C + r13c Theorem B).**

| word (clock, period T) | towers (rotation classes) | result | label |
|---|---|---|---|
| (01)^12, T = 24 | 38,546 | all die, max level 3309 (towers if=703 and if=7475; both also by r13c's K-head program: 3309) | COMPUTED: every ICH of period 24 on clock 01 is 8-periodic |
| (01)^16, T = 32 | 202,849 | 202,833 die in the word pass (cap 5e6 nodes per tower, max level 777); the 16 capped towers die in single runs at levels 797 (x2), 1700 (x2), 2607 (x2), 3208 (x2), 4249 (x2), 8857 (x2), 17604 (x2), 17714 (x2) | COMPUTED: every ICH of period 32 on clock 01 is 8-periodic |
| (01)^20, T = 40 | 1,203,631 | all die in one word pass, max level 1670 (if=7707/14317 class and if=790 class; if=790 also by the plain memo DFS `ifb3`: 1670) | COMPUTED: every ICH of period 40 on clock 01 is 8-periodic |
| (00100101010101)^4, T = 56 | 207,280 | 207,279 die in the word pass (max level 13); the capped tower if=49 dies at level 742 (tree DFS only; the K-head program stopped at its node cap, K = 291); the root word has no ICH of period 14 (D(root) = 15) | COMPUTED: no ICH of period 56 on this clock |
| (001010101)^6, T = 54 | r13c: one tower left (CAP54a) | running (`bin/ifd10 -tree`, 72 h cap; 86,000 s, 6.2e9 nodes, max depth 3327 at the last check); the root word has no ICH of period 9 | UNDECIDED |
| (0001)^15 = N12^5, T = 60 | r13c: two towers left | N60_1 dies at level 464 (1.72e9 nodes, 31,201 s); N60_2 running (86,000 s, 4.8e9 nodes, max depth 2116) | UNDECIDED |
| (0001)^12 = N12^4, T = 48 | r13c: eight towers left | not run to the end (probe of if=1961 stopped after 3.6 h, 9.3e8 nodes, no cycle) | UNDECIDED |

Twin structure (observation): on clock 01 the heavy towers come in pairs with identical death level and identical node count
(L = 24: 703/7475; L = 32: every pair above; L = 40: 7707/790). The hidden symmetry was not derived; every twin was computed.

## 1. Interface chains (PAPER PROOF)

Setting: r13c sections 1-2 (base b = 10, clock g of length P extended periodically, L a multiple of P, ICH = infinite closed
L-history, interfaces I = (c(t), xb(t), A(t)), t in Z/L, with c the forward carry into the next column, xb the digit below at
clock-1 phases, A(t) a non-empty subset of {0,1} of allowed backward carries; Lemma I1: a closed L-column v above I (all A'(t)
non-empty) yields the next interface I' = (floor((v+c)/b), v at clock-1 phases, A'), and the whole future above depends only on I).

**Proposition C.** Let J be an interface (L-periodic). There is a closed L-walk with r columns above the fixed column underlying J
iff there is a chain J = I_0 -> I_1 -> ... -> I_r of closed L-columns (each arrow by Lemma I1). Hence the relative tower of r13c
above J dies exactly at level r = D(J) + 1, where D(I) := longest chain length from I (infinity iff a cycle is reachable); it
survives forever iff D(J) = infinity, and then an ICH exists above J (the finite-state chain has a cycle; unroll it).
*Proof.* Lemma I1 and induction on r; finiteness of the set of interfaces gives the statement about infinity (a cycle gives an
infinite chain, hence by the correspondence an ICH; conversely an infinite chain revisits an interface). QED

**Exact reductions in the code.** (1) xb(t) enters only through (xb(t) + H) mod b, so xb is reduced mod b (exact merge). (2) Time
rotation by multiples of the clock period P commutes with the construction, so interfaces are canonicalised by their minimal
rotation (exact). (3) Interfaces with no closed column have D = 0 and are not stored. (4) Tree mode: no memo; repeated interfaces
are re-expanded, which is exact for the recurrence.

**Chunk filter.** Let L = 2 ELL. A closed L-column is a pair of half-walks (u on phases [0, ELL), w on [ELL, L)) with matching
boundary digits. For a child interface J = (u-part, w-part) a closed column above J exists iff trace(N_u N_w) != 0 for the boolean
reachability matrices N of the two half-interfaces, so children are filtered exactly before being expanded (`expandC4`).

**Use with r13c Theorem B.** Theorem B: if, for every d0-periodic interface I in IF(d0) and every closed L-column above I that is not
d0-periodic (a *birth*), the tower above dies, then every ICH of period L is d0-periodic. The word mode (`-word d0`) builds IF(d0)
by its own BFS, lists all births up to rotation and runs every tower; a word is decided when every tower has a DIES line.
For the root-14 word, d0 = 14 and the root word itself has no closed 14-history of any height beyond 15 (`scripts/root_check.py`,
independent Python), so no ICH of period 56 exists at all.

## 2. Programs and validation (COMPUTED)

`bin/ifb3` = `src/ifb.cpp` (memo DFS, plain expansion). `bin/ifd10` = `src/ifc.cpp`, `src/ifc_v9.cpp` = the source as it stood before ifd10 (builds ifd7..ifd9)
(chunk filter; `-tree` memo-free; `-word d0` own BFS of IF(d0) and births; `-every N` sampled towers; `-capnodes` per-tower cap;
ifd10 adds predecessor masks in the backward walk DFS, same logic; md5 of ifc.cpp = bd3ad736f2abb8a500e9307f4b2082e8).
- Per-tower comparison with r13c's K-head death levels (`scripts/ctrl_deaths.py` on r13c's complete `deaths.txt` lists): N24
  (125,090 towers) and N36 (1,219,563): 0 mismatches (`ctrl/deaths_N24_N36.log`). L = 16 (68,520 towers): 0 mismatches per the
  run notes; its log (12 MB) is not shipped; the L = 16 word histogram (8,565 classes, max 526) is in `ctrl/controls_rerun.out`.
- Plain memo (`ifb4`) vs chunked tree (`ifd8`) on sampled towers of all six open words (L = 32, 40, 48, 54, 56, 60): identical
  death-level histograms (`ctrl/reg_all.log`, `ctrl/reg_*.out`). Chunked vs plain BFS on the real heavy towers: identical new-live
  counts on CAP54a levels 1..12 and CAP56b levels 1..7.
- Whole-word regression at T = 24: memo DFS (`logs/ifb_L24.out`) and chunked tree (`logs/ifd_L24_tree.out`) give identical
  histograms; the two deepest towers also by r13c's K-head program (`logs/pass4_L24_if7475.out`: RDIES K = 3309) and per tower
  (`logs/ifb_L24_towers.out`). T = 40: tower if=790 by the plain memo DFS as well (`logs/ifb_L40_2_check.out`, K = 1670).
- Capped towers of the T = 32 word pass matched to their single runs up to rotation: `scripts/l32_match.py` ->
  `ctrl/l32_match.out` (16 of 16 have a DIES line).

## 3. Controls with known answers (`ctrl/controls_rerun.out`, re-run 2026-11-11)

- N12 at d0 = 4, L = 12: 12 tower classes, 11 die (max level 3), exactly 1 survives (cycle in the interface graph; the interface
  is r13c's survivor). Both `ifb3` and `ifd10`.
- p11 at d0 = 11, L = 22: IF(11) = 1,612 (a0 = 58), 2,687 towers, all die, max level 56 (= r13c, Theorem U of r12b). Both codes.
- Clock 01 at d0 = 4, L = 8: 1 tower, survives (the known T = 8 lock). Both codes.
- Base 9, clock (11000)^2, d0 = 5, L = 10: 137 interfaces (a0 = 21); 126 towers, 124 die (max level 9), 2 survive (one rotation
  class: the tower of the Lean-verified base-9 certificate). `ifb3`; the `ifd10` tree run on this INF tower did not finish in 100 s.
- Clock 01, d0 = 8, L = 16: 8,565 classes, all die, max level 526 (= r13c). Both codes.
- Root words (independent Python, `ctrl/root_check.out`): no ICH of period 9, 14, 11 (D(root) = 16, 15, 44 = r13c).

## 4. UNDECIDED

T = 54 (CAP54a running), T = 60 (N60_2 running), T = 48 (eight towers not run); every other clock and period. A decided word
says only that every ICH of that period is d0-periodic (or that none exists); it says nothing about centres.

## 5. Reproduction (`~/p196_run/r14c`)

Build: `clang++ -std=c++17 -O3 -march=native -o bin/ifb3 src/ifb.cpp`; the same for
`bin/ifd10` from `src/ifc.cpp`. The original runs used successive builds `ifd2`..`ifd10` of `src/ifc.cpp` with the same logic
(word passes `ifd2`/`ifd8`, single towers `ifd7`/`ifd8`/`ifd10`; checked against each other by the regressions of section 2).
Commands (current build):

    bin/ifb3 10 01 24 -word 8                                    # logs/ifb_L24.out  (25 min)
    bin/ifd10 10 01 24 -word 8 -tree -slots 4096                  # logs/ifd_L24_tree.out
    bin/ifd10 10 01 32 -word 8 -tree -capnodes 5e6                # logs/ifd_L32_word.out (16 TCAP lines -> out/towers/L32_tcap.txt)
    bin/ifd10 10 01 32 -runfile out/towers/L32_B_1.txt -tree -slots 4096 -sec 255000   # one capped tower (4.6-6.7 h each)
    bin/ifd10 10 01 40 -word 8 -tree -capnodes 2e8                # logs/ifd_L40_word.out (50 min)
    bin/ifd10 10 00100101010101 56 -word 14 -tree -capnodes 1e7   # logs/ifd_L56_word.out; then -runfile out/towers/CAP56b.txt (4.8 h)
    python3 scripts/root_check.py 00100101010101:14 001010101:9 00010010111:11
    bash scripts/reg_every.sh 01 32 8 40                         # one regression of ctrl/reg_all.log
    python3 scripts/l32_match.py                                 # from this directory
    bash scripts/r14c_relaunch.sh                                # the five long reruns (logs/main_*)

Progress logs (`*.err`, per-tower progress lines) are packed in `logs/progress_err.tar.gz`; `scripts/queue.txt` and
`scripts/slot_runner.sh` record the exact command lines of every run.
