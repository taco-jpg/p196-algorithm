# Uniform bands and 9-wire streams via exact reachability (reach / reachmt)

## The question
A periodic left end (cells 0..H-1 of the pair word P_x = d_x + d_{n-1-x}, time period T, overflow clock w) followed by
a UNIFORM band reaching to the centre is a complete Lychrel certificate format: the band is its own mirror, so no centre
is needed. Bases 4 (Seal 1996, 13-digit block) and 13 (repo, Lean) have certificates of exactly this shape.
Base 10 uniform bands (cycles of v -> 2((v+c) mod 10), c = [v >= 10], v != 9):
- {0}, {18}: excluded for every clock by the repo (results/E2ExtremeUniformIsolation, Lean). Our tool must never reach
  them; if it does, that is a bug or a contradiction to investigate before anything else.
- {6,12} (carries 1/0, r-digits 3/6), and the 6-cycle 2,4,8,16,14,10 (carries 0,0,0,1,1,1; r-digits 2,4,8,7,5,1).
The 9-wire (value 9, carry stream s up, 1-s down) is the neutral-band exterior of the earlier rounds.
**Some left end of some height H carries a band  <=>  an accepting interface is reachable from the bottom.**

## Why a new tool
up4 / upband2 / up5 iterate the set of interfaces height by height and stop when the SET repeats. The sets need not
repeat soon (round 4: no repeat at T=24 after 400 heights) although the question is plain reachability in a finite
graph. reach/reachmt do a BFS with a visited set: when the frontier is empty, every height has been checked
(RESULT COMPLETE). Same cell rule, same bottom boundary as up4; in addition cell 0 >= 1 at ALL times (it holds the
leading digit; up4 only checked t=0) -- a true constraint, so exclusions stay valid.

## Tools
- `reachmt` (multi-thread, compact keys of 2T + 4*(#overflows) bits; decision only)
  `THREADS=24 ./reachmt 10 T CLOCK ALL [cap]` checks in ONE run every uniform band whose period divides T, in every
  phase, plus every 9-wire stream. Lines: `TARGET band[..] phase p REACHED at height H (BAND='..' PH=p)`,
  `NEW STREAM at height H: ..`, `RESULT COMPLETE|EMPTY|TOO_BIG|MAXDEPTH`. Batch: `reachmt BATCH 10 ALL cap < "T CLOCK" lines`.
- `ROT=1` (env for reachmt; sweep.py --stage heavy uses it by default, --rot 0 switches it off): store one interface
  per orbit of the time shift by the clock period p. Exact: the bottom interface is fixed by the shift, the cell rule
  commutes with it, and every target set (all band phases, all wire streams) is closed under it. Memory and time drop by
  up to T/p (8x for clock 01 at T=16, 12x at T=24, 6x for 0001 at T=24). Counts are then orbits (Burnside: orbits >=
  interfaces / (T/p)); depth, targets and their heights are unchanged (calib.sh checks this).
- `reach` (single thread, parent pointers): `BAND='c:r,..' PH=p ./reach 10 T CLOCK BAND` stops at the first fit of
  that band and prints the left end (`LEFTEND` block, cell x: values at t = 0..T-1). Also `WIRE` mode.
- `replay_band.py FIT_LOG` builds left end + L band cells + mirror for L = 1,2,3,5,8,13,40, n even and odd, and runs
  genuine big-integer reverse-and-add for 20 periods: overflow on the clock, pair word = template, no palindrome.
- `sweep.py` driver (resumable JSONL, results in ../results/): `--stage csweep` = every clock (binary Lyndon word, one
  per rotation class; ALL mode covers every phase) and every T in [tmin, tmax] via C++ SWEEP shards, small cap, only
  non-EMPTY tasks written; `--stage words` = clocks from a file, T up to tmax; `--stage heavy` = every TOO_BIG task in
  the store, one at a time, multi-threaded, big cap. Any band target -> ALERT_TARGET.txt + rebuild with reach + replay.
- `calib.sh`: builds both tools and checks every known answer below. Must print CALIBRATION PASS.

## Known answers (calib.sh)
- base 13, clock 1010010000, T=10: band {8,16} phase 0 at height 55, phase 1 at 75; complete, 250301 interfaces;
  rebuilt left ends replay as genuine base-13 Lychrel templates.
- base 4, clock 011001, T=6: band {2,4} at height 13 (and 18), complete, 956 interfaces; replay PASS.
- base 10: p11 clock 00001110001: stream 00111010011 at height 29 (complete, 18060); clock 0001, T=12: 3 streams at
  height 53 (136652); clock 01, T=8: complete, 244784 interfaces, no band.

## Results in data/ (2 cloud cores, 7 GB)
- `data/r5_csweep_T*_summary.txt`: per-T counts of the full sweep (every binary clock, every T <= 24, cap 2M).
- `data/sweep_T1-24_nonempty.jsonl.gz`: every non-EMPTY task (EMPTY ones are only counted); usable as `--seed` after gunzip.
- `data/heavy_*.log`: full logs of the 12 tasks that exceeded the 2M cap (10 COMPLETE, 2 stopped).
Reproduce: `bash calib.sh`, then
`python3 sweep.py --stage csweep --tmin 1 --tmax 24 --shards 64 --out res/r.jsonl` and
`python3 sweep.py --stage heavy --tmin 1 --tmax 24 --heavy-cap N --out res/r.jsonl` (ROT=1 by default).

## Memory (reachmt)
Stored key = ceil((2T + 4*overflows)/64) words. Measured peak bytes per stored key (table at load <= 0.75, doubling,
frontier buffers included): 1 word ~20 B (clock 01, T=16: 257M orbits in 4.6 GB), 2 words ~35-47 B (T=24: 137M in
4.8 GB, 118M in 5.5 GB); plan ~65 B for 3 words, ~85 B for 4. With ROT=1 a stored key is an orbit. Choose
cap = (memory budget) / bytes. reach needs ~44 B per interface (only for rebuilding a fit; it stops at the fit height).
Speed: ~0.3-0.7 M interfaces/s per thread. csweep: ~0.25 ms per (T, clock) task; T=21..24 (1.35M tasks) took 55 s on
2 cloud cores, so T=25..28 (~19M tasks) and T=29..32 (~260M tasks) are minutes / ~1-2 h on 28 cores.

## Labels
COMPLETE / EMPTY = COMPUTED (exact, all heights). TOO_BIG / TIMEOUT / MAXDEPTH = UNDECIDED. A band fit is a
"certificate candidate" only after replay PASS; a certificate needs the induction over band length (as in the repo's
Lean base-13/base-20 templates).
