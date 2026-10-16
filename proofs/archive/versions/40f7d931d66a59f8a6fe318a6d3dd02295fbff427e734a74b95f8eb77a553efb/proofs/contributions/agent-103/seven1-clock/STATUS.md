# Agent #103 — extending the UNKNOWN_CAP scalar-clock probes `seven_1` and `primitive14`

Task `agent103-seven1-clock`. **Result: both clocks remain UNKNOWN.** The caps
were raised from 500,000 to 30,000,000 raw vertices. The exact necessary
prefix-lift hierarchy does not empty: `seven_1` survives through width 22 and
`primitive14` through width 15. In each, one cyclic SCC dominates and grows
geometrically. **No exclusion and no infinite-orbit claim follows.** A surviving
recurrent graph is only a necessary condition; it is not a realizable integer
orbit.

## Method (unchanged relation; only caps differ)

`continue_clock.py` imports the reviewed relation
`../../2026-10-14-broader-return/branching_lift.py` and the root construction
`../../2026-10-14-scalar-clock/scalar_clock.py` (`initial`, `CLOCKS`). Both are
used unchanged; their SHA-256 values are recorded in each `continuation.json`.
The script re-derives every width from width 1. Each width that the original
capped run archived is compared byte-for-byte with the archived file:

- `seven_1`: widths 1–15, raw and recurrent, 30 files.
- `primitive14`: widths 1–12, 24 files.

All are **identical**. The script then continues the same lift/recurrent loop
with caps of 30,000,000 raw vertices and width 40.

## Results

### `seven_1` = (1, 2, 4, 9, 18, 9, 10), overflow clock (0, 0, 0, 0, 1, 1, 1)

| Width | Raw vertices | Raw edges | Cyclic SCCs | Retained vertices | Largest SCC |
|---:|---:|---:|---:|---:|---:|
| 1 | 7 | 9 | 1 | 7 | 7 |
| 2 | 133 | 171 | 1 | 18 | 18 |
| 3 | 342 | 532 | 1 | 42 | 42 |
| 4 | 798 | 1,273 | 1 | 137 | 137 |
| 5 | 2,603 | 4,275 | 1 | 397 | 397 |
| 6 | 7,543 | 12,312 | 2 | 482 | 471 |
| 7 | 9,158 | 14,953 | 3 | 646 | 283 |
| 8 | 12,274 | 19,988 | 4 | 1,271 | 765 |
| 9 | 24,149 | 39,786 | 2 | 2,171 | 1,270 |
| 10 | 41,249 | 68,058 | 4 | 4,015 | 2,427 |
| 11 | 76,285 | 124,906 | 4 | 4,918 | 3,029 |
| 12 | 93,442 | 154,033 | 7 | 6,632 | 5,227 |
| 13 | 126,008 | 208,183 | 7 | 12,375 | 10,637 |
| 14 | 235,125 | 392,160 | 8 | 18,786 | 18,486 |
| 15 | 356,934 | 597,284 | 8 | 29,009 | 28,435 |
| 16 | 551,171 | 919,030 | 6 | 48,633 | 47,487 |
| 17 | 924,027 | 1,547,436 | 8 | 86,875 | 86,069 |
| 18 | 1,650,625 | 2,785,457 | 9 | 170,608 | 169,455 |
| 19 | 3,241,552 | 5,475,990 | 9 | 345,554 | 344,485 |
| 20 | 6,565,526 | 11,110,307 | 10 | 591,540 | 590,468 |
| 21 | 11,239,260 | 18,958,751 | 11 | 970,948 | 969,900 |
| 22 | 18,448,012 | 31,168,417 | 8 | 1,755,494 | 1,754,210 |

Status: **UNKNOWN_CAP**; next lift width 23: 33,354,386 raw vertices, 56,436,707 raw edges (cap 30,000,000). Archived-artifact comparisons: 30, all byte-identical.

### `primitive14` = (3, 6, 13, 4, 8, 17, 8, 17, 8, 16, 7, 15, 6, 12), overflow clock (0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1)

| Width | Raw vertices | Raw edges | Cyclic SCCs | Retained vertices | Largest SCC |
|---:|---:|---:|---:|---:|---:|
| 1 | 14 | 20 | 1 | 14 | 14 |
| 2 | 266 | 380 | 1 | 51 | 51 |
| 3 | 969 | 1,558 | 1 | 64 | 64 |
| 4 | 1,216 | 1,957 | 1 | 121 | 121 |
| 5 | 2,299 | 3,743 | 2 | 147 | 114 |
| 6 | 2,793 | 4,484 | 1 | 230 | 230 |
| 7 | 4,370 | 7,410 | 2 | 173 | 95 |
| 8 | 3,287 | 5,168 | 1 | 357 | 357 |
| 9 | 6,783 | 11,837 | 1 | 937 | 937 |
| 10 | 17,803 | 32,110 | 1 | 4,604 | 4,604 |
| 11 | 87,476 | 160,645 | 1 | 17,783 | 17,783 |
| 12 | 337,877 | 615,638 | 1 | 60,826 | 60,826 |
| 13 | 1,155,694 | 2,105,067 | 1 | 225,901 | 225,901 |
| 14 | 4,292,119 | 7,849,090 | 2 | 734,588 | 734,272 |
| 15 | 13,957,172 | 25,489,127 | 2 | 2,377,016 | 2,376,887 |

Status: **UNKNOWN_CAP**; next lift width 16: 45,163,304 raw vertices, 82,360,117 raw edges (cap 30,000,000). Archived-artifact comparisons: 24, all byte-identical.


## Interpretation and consequences

- For `seven_4`, the clock that is now Lean-checked (98/94 periods), the same
  method empties by width 14. For `seven_1` and `primitive14` the dominant SCC
  keeps growing:
  - `seven_1`: about ×1.6–2.0 per width from width 16 to width 22;
  - `primitive14`: about ×3.2–3.8 per width from width 11 to width 15.
- The next lifts already have 33.4M and 45.2M raw vertices. So pushing caps
  further is very unlikely to settle these clocks; a different invariant or
  argument is needed. This record is meant to save others that compute.
- Under the rotation noted in `SCALAR_CLOCK_BOUND.md`, `seven_1` contains the
  one-column trace (4,9,18,9,10,1,2). Exactly three one-column seven-step
  traces return to outer coefficient 4: (4,8,16,7,15,6,13), (4,9,18,9,10,1,2)
  and (4,9,10,1,3,6,13), checked by enumerating all 128 controls. The "outer
  coefficient 4 every seven steps" question therefore stays open through
  `seven_1`.
- A quick direct experiment (not a proof; `../seven1-clock/` does not retain
  it) found that random seeds of 6–30 digits follow either clock for at most
  about 7 periods (longest run of 53 steps for `seven_4` and 41 for `seven_1`
  among 3,000 seeds). The hierarchy growth therefore reflects slack in the
  necessary relation, not observed long runs.

## Retained files and reproduction

Retained:

- `continuation.json` per clock: per-width counts, SCC size histograms, the
  SHA-256 and byte size of **every** raw and recurrent artifact, and the
  archived comparisons.
- Recurrent graphs with compressed size at most 2 MB.

Not retained in git (deterministic, about 475 MB): all raw graphs and the
larger recurrent graphs. Their exact SHA-256 values are in `continuation.json`.
Regenerate them byte-identically with:

```sh
python3 -I proofs/contributions/agent-103/seven1-clock/continue_clock.py seven_1
python3 -I proofs/contributions/agent-103/seven1-clock/continue_clock.py primitive14
```

Run times: about 25 minutes for `seven_1` and 10 minutes for `primitive14`,
single-threaded, peak RSS under 2 GB.
