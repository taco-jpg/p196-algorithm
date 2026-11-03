# ReachDiskRounds6to8 -- detailed report

All results below are COMPUTED inside the left-end interface graph of `calculation/decimal_frontier/uniform_bands/`
(same cell rule, bottom boundary and leading-digit condition as `reach`/`reachmt`, main 95edd48c). Runs on a Mac Studio,
2026-11-01. Every UNREACHABLE assumes premise (B) below.

## Tools
- `reachdisk`: external-memory BFS (visited sets in per-bucket sorted files, height-by-height manifest, crash-resumable),
  quotient by the clock shift (ROT=1). Agrees exactly with `reachmt` on clock 01 T=8 (61,248 orbits), 0001 T=12 (45,570,
  three streams at height 53), clock 01 T=16 (257,093,986 orbits, height 592), base 13 (bands at 55, 75), `calib.sh`; three
  kill/resume tests give identical results.
- `backdisk`: backward cone from a target set over the same graph. Predecessors are found by a carry-pruned DFS over time.
  Checks: 10^6 random forward edges per configuration (5 configurations) have their source among the target's predecessors,
  and 10^6 random predecessors step forward to the target (0 mismatches). Positive controls: base 13 band at 55/75, base 4 at
  13/18, decimal p11 stream at 29, N12 at 53 (T=12 and T=24). Negative control: clock 01 T=8, all band targets unreachable.

## Premises
(A) Window filter. A_w(phase) = closure, under the time-local cell rule, of the bottom pattern, with start values ranging over
0..2B-2, no wrap condition and no root condition; independent of T. Every real edge applies this rule to every window, so by
induction every reachable interface has all its windows in A_w; pruning predecessors with a window outside A_w cannot change
REACHABLE/UNREACHABLE (PAPER PROOF). Exhaustive check of every reachable successor (before dedup), all T-w+1 window starts:

| task | w | states checked | violations |
|---|---|---|---|
| clock 0001, T=12 COMPLETE | 10 | 45,759 | 0 |
| clock 0001, T=24 COMPLETE | 10 | 6,626,085,128 | 0 |
| clock 0001, T=32 COMPLETE | 10 | 2,865,897 | 0 |
| clock 0001, T=40 COMPLETE | 10 | 132,850,243 | 0 |
| clock 0001, T=48, heights 1..4 | 10 | 4,134,634,272 | 0 |
| clock 01, T=16 COMPLETE | 8 | 258,054,380 | 0 |
| clock 01, T=24, heights 1..64 | 8 | 3,047,686,965 | 0 |
| clock 01, T=32, heights 1..15 | 8 | 4,896,252,176 | 0 |

Still to state: whether the cones also prune with windows that wrap across t = T-1 -> 0 (those were not in the check).

(B) Equivalence with the Agent120 exterior system (`calculation/neutral_band_search.py`: `nextB`, e2 = 1-e1, 9-trimming).
Checked, not proved: reach left ends map to Agent120 B-cycles that replay on big integers (p11 T=11/22 height 29; (0001)^3
height 53; (0001)^6 = N12 twice, height 53); all periodic orbits of the Agent120 mirror in bases 2 (width <= 10), 3 (<= 8),
4 (<= 6) appear in reach, first at height = max cycle width; state counts match `bx` (p22 via Burnside:
(26,365,606 + 18,060)/2 + 1 = 13,191,834). Of the 54 capped words of EXTERIOR.md, reach decides 51 (50 empty, (0001)^6 only
N12 twice); open: (01)^12, 00001110001100010000111000110001, (01)^16. Accepted streams agree: p11, p12, p22 only.

## 1. Uniform bands and 9-wire streams, left-end periods 25-32 (with 95edd48c: all T <= 31)
| T | tasks | COMPLETE | TOO_BIG | largest COMPLETE (orbits, height) |
|---|---|---|---|---|
| 24 | 2 | 1 | 1 | 6,625,354,893, 1346 |
| 25 | 2 | 2 | 0 | 23,995,940, 63 |
| 26 | 3 | 3 | 0 | 29,582,168, 31 |
| 27 | 9 | 9 | 0 | 5,031,498,868, 255 |
| 28 | 16 | 16 | 0 | 272,598,320, 112 |
| 29 | 1 | 1 | 0 | 13,077,005,892, 435 |
| 30 | 1 | 1 | 0 | 15,750,639,852, 175 |
| 31 | 36 | 36 | 0 | 3,415,282,296, 63 |
| 32 | 57 | 55 | 2 | 264,037,700, 29 |

(The light tasks of T = 25..32 were decided by the csweep stage under a 2M cap.) No COMPLETE task reaches a band; the only
9-wire stream is N12 twice at (24, 0001). UNDECIDED (cap 2x10^10 orbits): (24, 01) at height 184; (32, 0000111000110001) at
height 220; (32, 01) at height 21. Backward cones from all band and 9-wire targets also failed to finish for these three.

## 2. Chain 1 (Agent120 + Agent6NineRailCentreRenewal), clock (0001)^(P/4)
Targets: port words 01000101 and 10111010 (period 8) and 1000100001110111 (period 16), every shift by a multiple of 4 and
four alignments of the clock.
| P | method | result | size |
|---|---|---|---|
| 24 | forward, COMPLETE | only N12 twice (period 12), so no port word | 6.6x10^9 orbits |
| 24 | cone, no filter / w=10 | UNREACHABLE | 6,544,664 / 7,142 states |
| 32 | forward + cone | UNREACHABLE | 2,815,872 orbits / 73,511,429 states |
| 40 | forward + cone | UNREACHABLE | 132,509,676 orbits / 11,320,224 states |
| 48 | cone w=10, all phases | UNREACHABLE (COMPLETE) | 271,954,230 states, 120 layers |
| 56 | cone w=10 | UNDECIDED | 4.07x10^9 at layer 39, +1.6x10^8 per layer |
So chain 1 needs P >= 56 (P = 72 if the r = 3k pattern of THEORY.md section 7 holds).

## 3. Chain 6, clock (01)^8, period 32
The repo's m = 8 enumeration gives 128 primitive period-32 cycles (k=2: 128, as in Agent11E2P16M8AllTime). Charge, computed on
three laps (P = 96, since the formula needs 6 | P): 0 for all 1024 cuts (8 per cycle). Cut-to-cut steps checked under the reach
rule for cycles 0, 1, 50, 127. Backward cone, w = 8: frontier empty at layer 268, 63,734,031 states, all 1024 targets pass the
filter: UNREACHABLE. Without the filter: 16, 794,608, 336,273,408 new states in the first three layers (UNDECIDED, stopped).
Positive control (C4): the four cuts of `cert_b9_rec0.json` (base 9, T = 10, clock 1100011000) form the depth-61 4-element SCC
of the repo engine, and the cone reaches the bottom at height 61. Scope: m = 8, temporal period 32 only; the charge-zero cycles
of periods 96, 144, 160, 288, 608 remain open (tools support T <= 64).

## Not claimed
No candidate certificate. Premise (B) is unproved. Tool sources (`reachdisk.cpp`, `backdisk.cpp`, `run_r6.py`) and logs are
on the Studio and not yet in the repo.

Sources (Studio rounds 6-8 tools and design notes): `calculation/decimal_frontier/uniform_bands/rounds6to8/`.
