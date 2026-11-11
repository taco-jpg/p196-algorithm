# Main-session independent check of r13c (Theorem B towers)

`mc13e.cpp` was written by the main session from the recurrences (R1)-(R3) of an infinite closed L-history (FINAL.md section 1);
it shares no code with r13c's khr / kh3 / Python checks. Build: `clang++ -O2 -std=c++17 -pthread mc13e.cpp -o mc13e`.

Modes: `selftest SEED COUNT` (genuine addition vs the recurrence), `if G D` (|IF(D)| and saturation height), `root G L KMAX`
(plain tower from the root), `towers G D L THREADS NCAP SEC KMAX [SAMPLE] [0 IDX]` (one tower per rotation class of births; a single tower with `0 IDX`).

`drive1.sh` -> `drive1.out`, `logs/L16.out`, `logs/T55.out`; `drive2.sh` -> `drive2.out`, `logs/T55_tower665992.out`. Results:

* selftest PASS (200,000 numbers, 10,596,570 column checks).
* |IF| and a0 equal to r13c for all seven (g, d) pairs: (0001,4) 16/5, (01,8) 22,601/87, (0001,12) 22,657/70, (p11,11) 1,612/58,
  (00010010111,11) 1,483/44, (00100101010101,14) 337/15, (001010101,9) 137/16.
* Root towers: g = 00010010111 at L = 11 dies at level 45; L = 9 (root 9) at 17; L = 14 (root 14) at 16.
* Controls: N12 at d = 4, L = 12: 12 classes, 11 die (max level 3), 1 capped (the N12 tower); p11 at L = 22: 2,687 classes, all die, max 56.
* (01)^8, d = 8, L = 16: 68,520 births, 8,565 rotation classes, all die, max death level 526 (same histogram head as r13c).
* (00010010111)^5, d = 11, L = 55: 1,240,956 rotation classes; 1,240,955 die in the bulk run (max 230) and the one capped tower
  (index 665,992, capped at level 194) dies at level 345 in a single-tower run with a larger cap. So all die, deepest 345, as r13c reports.
