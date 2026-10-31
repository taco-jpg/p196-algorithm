# UniformBandLeftEndsT24: details

Labels: COMPUTED = exact finite computation, no state caps unless stated; UNDECIDED = hit a cap.
Code: `calculation/decimal_frontier/uniform_bands/` (reach.cpp, reachmt.cpp,
replay_band.py, sweep.py, calib.sh, README.md, data/).

## Certificate format
Periodic left end (cells 0..H-1 of the pair word, time period T, overflow clock w) + a UNIFORM band up to the centre.
The band is its own mirror, so no centre is needed. Bases 4 (Seal 1996) and 13 (repo, Lean) have certificates of this shape.
Base-10 uniform bands (cycles of v -> 2((v+c) mod 10), c=[v>=10], v != 9): {0}, {18}, {6,12}, {2,4,8,16,14,10}.
The 9-wire (value 9) with a stream is the neutral-band exterior.

## Method change: per-height set iteration -> plain reachability
up4/upband2/up5 iterate the interface set height by height and stop only when the set repeats. Round 4 saw no repeat at
T=24 after 400 heights. But "some left end of some height carries the band" is reachability in a finite graph
(nodes = interfaces (carry up, carry required from above, r-digits at overflow times)). A BFS with a visited set decides
it exactly: frontier empty = all heights checked (RESULT COMPLETE). Same cell rule and bottom boundary as up4, plus
"cell 0 >= 1 at all times" (leading digit), which up4 only checked at t=0. The reachable set depends only on (T, clock), so
one run checks every band in every phase and every wire stream.
- reachmt: multi-threaded, keys of 2T + 4*(#overflows) bits, sharded hash set, BATCH and SWEEP modes (SWEEP enumerates
  binary Lyndon words = one clock per rotation class).
- ROT=1 (quotient by the clock shift): the bottom interface is fixed by the time shift by the clock period p, the cell
  rule commutes with it, and every target set (all band phases, all wire streams) is closed under it. So BFS can store
  one interface per orbit; memory and time drop by up to T/p (8x for clock 01 at T=16). PAPER PROOF (3 lines) + checked:
  identical depths, targets and heights on base 4 T=12 (483598 interfaces = 242303 orbits) and base 10 clock 01 T=8
  (244784 = 61248 orbits), p12 (136652 = 45570 orbits; the 3 streams form one shift orbit).
- reach: single-threaded with parent pointers; prints the left end of a fit.
- replay_band.py: builds left end + L band cells + mirror (L = 1,2,3,5,8,13,40; n even and odd) and runs genuine
  big-integer reverse-and-add for 20 periods (overflow on the clock, pair word = template, no palindrome).

## Validation (all COMPUTED)
- Base 13, clock 1010010000, T=10: band {8,16} at heights 55 and 75 (= repo |B| 55, 75); complete (250301 interfaces).
- Base 4, clock 011001, T=6: band {2,4} at height 13 (= Seal's 13-digit block) and 18; complete (956).
- Rebuilt base-13 and base-4 left ends replay as genuine Lychrel templates (every L, both parities, 20 periods).
- Base 10 p11 clock: stream 00111010011 at height 29 (18060 interfaces); clock 0001, T=12: the 3 census streams at
  height 53 (136652). Clock 01, T=8: complete, 244784 interfaces, no band (upband2 needed 196 heights for this).
- reach and reachmt (different storage and hashing) agree on all counts; batch = single mode; sharded sweeps add up.

## Results, base 10 (COMPUTED unless marked)
- All binary clocks and all left-end periods T <= 24: 1,465,899 (T, clock) tasks.
  At a 2M-interface cap, 12 tasks are undecided, exactly the repo's capped list in lattice_formats/FORMATS.md §6
  (p16 x1, p18 x1, p21 x1, p22 x3, p23 x1, p24 x5).
  Every other task is COMPLETE or EMPTY: no uniform band is reachable. The only 9-wire streams are p11 (T=11) and p12
  (T=12), as in the census.
- Capped cases decided in the cloud with reachmt (2 threads, 7 GB); all COMPLETE, no band target, no new stream:
  - **Clock 01, T=16 (the repo's "(10)^8")**, with ROT=1: 257,093,986 orbits (about 2.06e9 interfaces), frontier empty
    at height 592, 398 s. Without the quotient it was TOO_BIG at 280M interfaces.
  - p18 word (101010100)^2, T=18: 7,599,800 interfaces, height 57.
  - p21 word 001001010101001010101, T=21: 43,844,578 interfaces, height 112.
  - p11 clock at T=22 (the census p22 = p11 twice): 26,365,606 interfaces; exactly one 9-wire stream,
    0011101001100111010011 = the p11 stream twice (agrees with Agent732P22BHistoryUniqueness).
  - T=22 0001000101010010100011: 3,280,644. T=22 00010010111: 43,763,920. T=23 00001010101010100100111: 8,455,916.
  - T=24: 000100010101010011100011 (27,155,320), 000100100011 (ROT=1, 4,291,961 orbits), 001001010100100101010101
    (12,435,424): all COMPLETE, nothing.
  - UNDECIDED, stopped by hand to protect the 7 GB container (open):
    T=24 clock 0001 (round 4's question), ROT=1: 136.6M orbits at height 81, +3.2M per level; the period-12 stream
    101101010010 (twice) appears at height 53, as expected.
    T=24 clock 01, ROT=1: 117.5M orbits at height 23, +17M per level and accelerating.
- So 1,465,897 of the 1,465,899 tasks with T <= 24 are decided, and no uniform band is reachable in any of them.
- Per-T counts: `calculation/decimal_frontier/uniform_bands/data/r5_csweep_T*_summary.txt`.

## Consequence
For left-end periods up to 24, apart from the two T=24 tasks above, no decimal certificate of the form
"left end + uniform band + mirror" exists (COMPUTED). This is the mechanism behind the base-4 and base-13
certificates. Open: the two T=24 tasks, T > 24, and non-uniform bands or centres.
