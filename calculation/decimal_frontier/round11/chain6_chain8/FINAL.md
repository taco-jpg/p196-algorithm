# r11f — chain 6 (long-period clock-01 cut words, P96, windows w = 9/10) and chain 8 (root [9,17,5], clock G = 110001001000)

Labels: COMPUTED / PAPER PROOF / UNDECIDED. "UNREACHABLE / no stream" statements are about the reach graph of reachdisk/backdisk
(premise (B) of ReachDiskRounds6to8: reach graph = Agent120 exterior system — checked, not proved; unchanged here).
Window premises: (A) forward windows A_w (FILTER_R8 + r9u wrapped windows), (C) co-reachability windows BB_w (FINAL_R9U.md §2).
Studio dir `~/p196_run/r11f/`; laptop copy `~/Desktop/p196_studio/r11f/`. This run resumed after the first r11f agent died (network).
Nothing in `~/p196_repo` or other agents' processes was touched; no git push.

## 0. Results

| part | question | result | label |
|---|---|---|---|
| 6 / P32 | 128 charge-0 cycles (256 cut keys), clock (01)^16 | backward cone with A_8: **UNREACHABLE (COMPLETE)**, frontier empty after layer 268, 63,734,031 orbits (first r11f agent, `logs/cone_P32_w8.log`) | **COMPUTED** (premises A, B) |
| 6 / P96 | 56 charge-0 cycles (200 cut keys), clock (01)^48 | (i) every cut window lies in A_9 and in A_10 (no cycle excluded); (ii) BB_9 and BB_10 contain the bottom window in both phases (no all-T exclusion); (iii) backward cone with A_9: layers 7 → 148,217 → 285,187,608 new, **RESULT TOO_BIG at layer 4** (disk guard during candidate generation, > 190 GB of layer-4 candidates) | **UNDECIDED** |
| 8 / T=12, 24 | any 9-wire stream (any exterior, any root) with clock G at T = 12, 24 | **none**: unfiltered forward search COMPLETE (T=12: 8,446 interfaces, height 24; T=24: 4,291,961 orbits, height 39); BB-filtered T=24 run agrees (8,653 orbits, height 36) | **COMPUTED** (premise B) |
| 8 / T=48 (k=2) | exterior reaching the PR381 centre stream e=010100110100101011001011 | **none**: forward search with BB_10(PR381 windows) + EARLY COMPLETE, frontier empty after height 78, 11,790,840 orbits, 0 streams; 22,969,371 successors window-checked, 0 violations | **COMPUTED** (premises A, B, C) |
| 8 / T=72 (k=3) | same | forward BB_10 run **still running** at report time (height 15: 158,138,339 orbits visited, 92.2M new at h15, ×5 per height; cap 4e9) | **UNDECIDED** (in progress) |
| 8 / all k | PR381-compatible exterior for every k | BB_10 contains the bottom window in all 12 phases (`logs/wb8.log`) → no T-independent window exclusion | **UNDECIDED** |
| 8 / root [9,17,5] | K-head lifting (Agent120 head, clock G, phase 0 prefix [9,17,5]) | root-restricted cyclic core never empties up to K = 22 (K=22: 12,687,616 vertices; K=23 candidate cap); **closed-arc core = 0 for every K ≤ 22** ⇒ no 9-padded periodic exterior of width ≤ 22 with this root, any period | **COMPUTED** (width-bounded only); all-width **UNDECIDED** |
| 8 / roots [9,17,4], [9,17,17] | same lifting | core EMPTY at K = 11 and K = 27 respectively ⇒ no periodic exterior with clock G^ω, any width/period, with these roots | **COMPUTED** (lifting completeness: truncation maps closed walks to closed walks, as in #481 PRO-R01-d-8a07) |

Net: chain 6 P96 — UNDECIDED. Chain 8 — COMPUTED for T = 12, 24 (no stream at all) and T = 48 (no PR381-compatible exterior) and
for widths ≤ 22 at root [9,17,5]; UNDECIDED for k ≥ 3 and for unbounded width at root [9,17,5]. No PAPER PROOF claim in this route.

## 1. Method
* **Backward cone** (`backdisk9w.cpp`: backdisk9 with the overflow-digit stream widened to 256 bits so clock 01 works up to T = 128):
  reverse BFS from the cut keys (`cuts6_P*.txt`, decimal L/H/Y from `cuts6.json` via `cuts6.py`), predecessors pruned with the forward
  window bitsets A_w (exact, `wbuild`), ROT quotient by the clock shift. UNREACHABLE ⇔ reverse frontier empty without meeting the bottom.
* **Target-window tests** (`chk_targets.py`): a cut with one window outside A_w is unreachable; cuts k → k+1 of a cycle are real reach
  edges (`chk_conv6.py`: 552 cycles, 530,432 cut-to-cut cell checks, 0 violations), so one excluded cut kills its cycle.
* **Co-reachability windows** (`bwin6.cpp`, targets from `wtargets.py` / `mk_wire_targets.py`): BB_w(ph) = windows of A_w(ph) from which
  a target window is reachable by abstract steps inside A_w. If the bottom window is outside BB_w in some phase, no target is reachable
  at ANY T. Otherwise BB_w is used as a forward filter (premise C): `reachdisk128.cpp` (reachdisk_wc_r10 with 128-bit streams) with
  BFILT=1 EARLY=1 WRAP=1 drops successors with a window outside BB_w; a target-reaching path is never dropped.
* **K-head lifting** (`kheadc.cpp`, independent of `khead_root.py`): root-restricted cyclic core S_K, lifted by all 19 coefficients;
  "closed" arcs = arcs that are genuine exteriors of width ≤ K (9-padded); a closed cycle through a root vertex = a periodic exterior.

## 2. Validation (positive controls before trusting negatives)
* **BB filter with the exact r11f tools** (reachdisk128 + bwin6 file targets + EARLY): clock 0001, BB_10 built from the N12 stream
  101101010010 windows ONLY (12 windows; |BB|/|A| 43.7/37.2/30.0/22.8 %). T=12: **N12 stream found at height 53**, 3,366 orbits;
  T=24: **stream found at height 53**, 35,284,177 orbits (identical count to r10's posB_T24 run with all-wire BB). 106,521,802 successors
  window-checked, 0 violations. (`logs/ctl_N12_build.log`, `logs/ctl_N12_bfilt_T12.log`, `logs/ctl_N12_bfilt_T24.log`)
* Unfiltered reachdisk128: clock 0001 T=12 finds the N12 stream (`logs/ctl_T12_0001.log`); base 4 clock 100 T=66 finds a stream at
  height 2 (`logs/ctl_b4_T66.log`, stopped after height 3, control only).
* kheadc closed-arc detection: base 4, clock 100, all roots: **closed 3-cycle found at K = 7** (width-7 exterior), detection works.
  (No decimal exterior of width ≤ 22 is known for clock G, so the decimal negative is width-bounded only.)
* backdisk positive controls: inherited from rounds 7/9 (N12 recovered); the P32 cone here is a negative.
* Target windows: `wtargets.py` regenerates the P96 part of the earlier `t6_all_w9.txt` exactly; note that `t6_all_w9.txt` lacked
  492 of the 512 P32 windows (it was not used for any P32 claim; P32 was decided by the cone). `t6_P96_w10.txt`/`t6_all_w10.txt` are fresh.

## 3. Observations
* |BB_10| for the P96 cut targets = 304,821,658 / 178,608,930 — **identical** to r10's BB_10 for (24,01) bands + all 9-wire targets.
  Likewise at w=8 all six periods give the same |BB|. The co-reachability closure saturates to a target-independent set: windows of
  width ≤ 10 cannot separate the long-period targets from the bottom. A decision for P96 needs either a much sharper invariant or a
  forward search at T = 96 (reachdisk128 supports ≤ 32 overflow slots; clock 01 at T=96 has 48, and (32,01) forward was already
  UNDECIDED in r10 at height 260).
* Chain 8 forward sizes grow fast with k: T=24 8.7e3, T=48 1.18e7, T=72 > 1.58e8 at height 15 (BB-filtered orbits).

## 4. Still running / how to resume
* `g381_T72_bfilt` (PID see `pgrep reachdisk128`, cwd r11f, 6 threads, nice 10, cap 4e9, disk guard 20 %). Resume after a stop with
  `WINCHECK=10 WINDIR=wsets8 BFILT=1 EARLY=1 BPREFIX=bwinE ROT=1 WRAP=1 THREADS=6 nice -n 10 ./reachdisk128 10 72 110001001000 WIRE wd/g72b 4000000000 0.20 >> logs/g381_T72_bfilt.log`.
  `watchdog.sh` (kills r11f jobs above 110 GB summed RSS) exits by itself when no r11f job remains.

## 5. Files to push (repo-relative suggestion: calculation/decimal_frontier/r11f/)
Sources: backdisk9w.cpp, reachdisk128.cpp, winbits128.h, wincd128.h, bwin6.cpp, kheadc.cpp, khead_root.py, wtargets.py,
mk_wire_targets.py, chk_targets.py, chk_conv6.py, cuts6.py, watchdog.sh. Data: cuts6.json, cuts6_P32.txt, cuts6_P96.txt, t6_P96_w10.txt,
tgt8.json, tgt8_w10.txt, tgt_N12_w10.txt. Logs: cone_P32_w8, cone_P96_w9, chk_targets_w8/w9/w10, chk_conv6, bwin6_all_w9, bwin6_P96_w10,
bb8.log, wb8, g381_T12/T24/T24_bfilt/T48_bfilt/T72_bfilt, ctl_*, kc_9175/kh_9175/kh_9174/kh_91717. FINAL.md.
