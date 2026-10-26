# Neutral-band certificate search, base 10

Goal: one cycle accepted by `Agent120.Neutral.cycleOK 10` (lean/P196/Drafts/Agent120NeutralBandCalibration).
`lychrel_of_cycle` (proved in Lean for every base) then gives a decimal Lychrel number. Nobody has one.
The exact Python mirror of the checker is `../neutral_band_search.py` (`selftest` re-accepts all eight known
certificates: bases 2, 4, 8, 16, 32, 11, 17, 26).

Four toolkits, written by four independent agents on 2026-10-25 (computation only; nothing here is a Lean result):

| folder | method | start with |
| --- | --- | --- |
| `structure/` | exact automata in C++: `bauto` lists every exterior (B) cycle of a period for all lengths; `cauto` decides the center (C) for a given carry/overflow stream, for all C lengths (`-allm`); `pipeline.py` chains them and replays hits in the mirror | `studio_run.sh` |
| `breaks/` | exact B-cycle census (`studio/run_btransfer.py`), padded CP-SAT center solver (`studio/ccycle_padded.py`, `full_search.py`) | `studio/run_all.sh` |
| `bases/` | exterior BFS for any base, CP-SAT center solver, base 3–40 comparison | `studio_exterior.py`, `studio_pipeline.py` |
| `solver/` | CP-SAT over whole cycles with a length schedule (independent cross-check) | `README_STUDIO.txt`, `run_studio.sh` |

## What is known (computed; the decoupling and counting facts are also argued on paper)

* `Hyp` forces `e2 = 1 - e1`, so the exterior B evolves on its own and emits two bit streams per step: the carry
  `e1` and the overflow `gam`. The center C sees only these streams. **A certificate = a B-cycle and a C-cycle with
  the same streams.**
* Along a closed cycle `|nextB| = |B| + gam` and `|nextC| = |C| + gam`, so `Σu = Σgam`, `Σv = Σgam/2` and
  `Σ(u+v) = 1.5·Σgam`: the condition "gain ≥ overflows" is automatic; any closed cycle is a certificate.
* A break (`e1 = e2`) never happens right after an overflow step (200,000 random base-10 starts: 21,431 breaks,
  0 after an overflow).
* Base 10, B side (agreed by three toolkits): no B-cycle for period p ≤ 10, 13, 14, 15, 17, 19; at p = 11 one
  stream `g = 11100010000`, `e = 10100110011` (|B| = 29; re-checked by hand: B returns after 11 steps); at p = 12
  `g = 100010001000` with three `e` (|B| = 52–53). p = 16, 18 undecided. Base 10 needs Σgam ≥ 4 per cycle
  (every known certificate in other bases has Σgam = 2).
* Base 10, C side (all C lengths, `cauto -allm`): **no center closes** for the p = 11 stream with one period
  (k = 1, 55 trim patterns), with two periods (k = 2, period 22, all 7,315 patterns), and for each of the three
  p = 12 streams with two periods (k = 2, period 24, 2,024 patterns each). The three p = 12 streams are one
  B-cycle started at different steps. (CP-SAT also found no C for p = 11, k = 3 up to width 41.)
* `structure/cauto_fast.cpp` gives the same answers as `cauto.cpp` about 3,000 times faster (prefix sharing
  across trim patterns, per-segment factorisation, `-sym` time-shift symmetry; `-skip`/`-patterns` to resume).
  Differential tests: 131,896 brute-force cases and 8,106 old-vs-new patterns, 0 mismatches; the base-11/26
  pipeline output is byte-identical. The old `cauto` packs its state into 128 bits, which truncates the last
  field when the period is 22 or more; use `cauto_fast` for long periods.

## Run book for the Mac Studio (32 cores, ≤ 150 GB)

```bash
cd ~/p196-merge-check && git fetch origin && git checkout -B main origin/main
python3 -m venv ~/nbenv && ~/nbenv/bin/pip install ortools ; export PATH=~/nbenv/bin:$PATH
export MIRROR=$PWD/calculation P196_ALGO=$PWD REPO=$PWD
cd calculation/neutral_band/structure && g++ -O2 -o bauto bauto.cpp && g++ -O2 -o cauto cauto.cpp && g++ -O2 -o cmatch cmatch.cpp && mkdir -p out
```

0. **Validation (≈ 5 min).** `python3 pipeline.py 11 3 1 2 | head -5` (must print a base-11 cycle with cycleOK = True);
   `./bauto 10 11 12` (must print the p = 12 ACCEPT lines); `(cd ../breaks/studio && python3 test_bcore.py &&
   python3 test_cpad.py 26 4 20 20)`; `(cd ../solver && bash run_studio.sh phase0)`.
1. **Confirm the center results with `cauto_fast` (minutes).**
   `g++ -O2 -std=c++17 -o cauto_fast cauto_fast.cpp`, then for each stream (p = 11: `G=11100010000 E=10100110011`;
   p = 12: `G=100010001000` with `E=101010010101`):
   `for i in $(seq 0 29); do ./cauto_fast 10 $E$E $G$G 1 1 -vall -allm -cap 30000000 -sym -part $i 30 > out/f_$i.txt 2> out/f_$i.err & done; wait`
   `grep -h "FEASIBLE\|NOPERIOD\|CAPPED" out/f_*.txt | sort | uniq -c` (empty = no certificate; every `DONE` line
   should say `status=none`). Next candidates, now cheap: p = 11 with k = 3 (`$E$E$E $G$G$G`) and p = 12 with k = 4.
2. **More B-cycles (p = 16–24).** ≤ 10 GB per process, so at most 12 processes:
   `for i in $(seq 0 11); do ./bauto 10 16 24 -w -part $i 12 -cap 300000000 > out/b_$i.txt 2> out/b_$i.err & done; wait`
   Every new `ACCEPT` stream goes through step 1 with `cauto_fast` (k = 1, 2, and more while cheap). "state cap" in .err = undecided.
3. **Independent cross-check of step 1** with CP-SAT (different code, different author):
   `cd ../breaks/studio && python3 run_btransfer.py --base 10 --pmin 11 --pmax 12 --procs 4 --out b10.jsonl &&
   python3 full_search.py --in b10.jsonl --procs 24 --zlo 3 --zhi 100 --tl 600 --out certs10.jsonl`.
4. Lower priority: `bash ../solver/run_studio.sh phase1` (whole-cycle CP-SAT, p ≤ 12, |B| ≤ 30, |C| ≤ 45).

Any hit: keep the full edge list and check `cycleOK 10` in Lean (`decide`) before claiming anything.
