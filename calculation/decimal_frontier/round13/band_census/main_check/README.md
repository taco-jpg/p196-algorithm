# Main-session independent checks of r13a, and the band-centre scan

All programs written by the main session (no code shared with r13a's bandcensus.cpp / bandsat*.py / centregen.py). Run on the
Studio 2026-11-08 / 2026-11-09; paths `~/p196_run/...` are those of the run machine.

| file | what | output |
|---|---|---|
| `bandcount.cpp`, `drive_bc.sh` | recount of the band census (cycles of F on phase-0 words, primitive, up to rotation), s <= 8 | `drive_bc.out`, `logs/bc_*.txt` |
| `report.py` | compares the recount with r13a's `census/b*_s*.txt` (counts and period multisets) and summarises the scan | `report.out` |
| `lcheck.py`, `spot.sh` | own one-hot SAT encoding of the L and R instances (rectangle window), spot checks of r13a's ALLUNSAT bands and of two controls | `logs/spot.out` |
| `bandscan.py`, `drive_scan.sh` | every census band with T <= 400 as a lattice with empty preamble (band background on both sides); all-period closure `mc13c runscc` (`../../k1_fixed_period/main_check/mc13c.cpp`), K <= 60, 120 s per phase orbit | `logs/scan_*.jsonl`, `logs/scan_*.out` |
| `foldsim.py` | plain fold simulation (exact window map on the band background, all exact periodic orbits of depth K) | `foldsim.out` |
| `match13a.py` | locates r13a's two centre-bearing bands in the scan | `match13a.out` |
| `lat_1000_11_8_5.txt`, `lat_1000_13_10_7.txt` | the two band lattice files written by `bandscan.py` (input of `foldsim.py`) | |

Results:

* Census: 265 / 284 / 161 bands for clocks 1000 / 10 / 00001110001, 0 differences per (clock, s) in counts and in the multiset of periods T (`report.out`).
* Spot checks: all 20 ALLUNSAT instances tested are UNSAT for every rotation in the own encoding; the T12 row W0, the band (11,8,5) and the no-foreign-letter control are SAT (`logs/spot.out`).
* Scan (`report.out`): clock 1000: 214 bands with T <= 400; 93 closed (E_acc empty at some K for every phase orbit, so the list of exact
  orbits found is the complete list of centres of that band background, all periods and depths), 121 not closed within the limits
  (UNDECIDED); 73 bands have at least one exact periodic orbit (a centre). Clock 10: 259 / 114 / 145 / 113. Clock p11: 128 / 77 / 51 / 58.
* foldsim: for band (11,8,5) (file row 11,8,5; T = 24) the depth-2 window map has exactly one periodic orbit, of period 24, and it contains
  the window (13,2) = lower half of r13a's centre C = (13,2,13); for band (13,10,7) likewise one period-24 orbit containing (5,16), the
  lower half of C = (5,16,5) (`foldsim.out`). The scan finds these bands not closed, with many further exact period-24 orbits at depths up to 11 (`match13a.out`).

Reproduce: `sh drive_bc.sh` (about 70 min in all, 8 threads), `sh drive_scan.sh` (about 11 hours wall clock for the three clocks, 6 workers), `sh spot.sh`,
`python3 report.py`, `python3 foldsim.py lat_1000_11_8_5.txt 2 13 2`, `python3 foldsim.py lat_1000_13_10_7.txt 2 5 16`.
