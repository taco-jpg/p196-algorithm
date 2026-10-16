# 196 reverse-and-add: engine history and explainer

This repository holds the engine packages for the exact 196 reverse-and-add (Lychrel) search, and an
interactive explainer page, `196-Engine-Fixed.html`, that walks from the first kernel to the current
engine.

**Production is v9** (512 threads, J=32, tile 1900) since October 13, 2026, on an RTX 4050 Laptop GPU
(35 W firmware cap). v8 is kept for rollback.

## Current state (October 13, 2026)

| | |
|---|---|
| Engine | v9, 512 threads per block, 32 steps per barrier, tile 1900 words |
| First v9 chunk | iteration 981,226,464 · 406,161,163 digits · 198.314 µs/step · 0 certification replays · 0 fingerprint replays · SHA-256 verified |
| Sustained test (100,000 steps, same checkpoint copy) | v8 251.121 µs/step → v9 198.839 µs/step, **+26.3%**, identical output, 0 replays |
| Cost per digit | about 0.49 ps per digit per step (v8: about 0.62 ps) |
| Checks | every step's palindrome status; certified intervals with exact replay; mod-9 fingerprint every 8,192-step window; weekly per-step cross-check, Sundays 3 a.m. Pacific |

Projected dates at v9's measured speed, assuming no downtime (estimates, not measurements):

| Milestone | Estimate |
|---|---|
| 1 billion steps (Dolbeau 2011: 413,930,770 digits) | October 13, 2026, evening |
| 1 billion digits (Dolbeau 2015) | about October 19, 2026 |
| 2 billion digits | about November 8, 2026 |
| v9's limit, ~4.29e9 digits (32-bit pair index) | about mid-February 2027 |

v8's 2.147e9-digit limit no longer applies: v9 counts digits in 64 bits.

## Measured on the RTX 4050

A/B medians are 5,000 steps × 3 interleaved rounds on a copy of the production checkpoint; sustained
runs are 100,000 steps. A configuration counts only with 0 replays.

| Configuration | Compared with | µs/step | Change |
|---|---|---:|---:|
| **v9, 512 threads, tile 1900** (production) | v8, tile 1000, sustained | 251.121 → 198.839 | **+26.3%** |
| v9, 256 threads, tile 940 | v8, tile 1000, A/B | 247.981 → 199.336 | +24.4% |
| v9, 512 threads, tile 1900 | v8, tile 1000, A/B | 247.981 → 198.895 | +24.7% |
| v9 J=16 (warp windows alone) | v8, tile 1000, A/B | 247.981 → 204.779 | +21.1% |
| v9 J=32 vs J=16 | tile 940, A/B | 204.779 → 199.336 | +2.7% |
| v9 tile 940 vs 900 (every warp full) | 256 threads, A/B | 208.103 → 199.336 | +4.4% |
| v9 pipe balancing | v9, tile 940, A/B | 199.336 → 201.433 | −1.0% |
| v9 base-5 | v9, tile 940, A/B | 199.336 → 221.661 | −10.1% |
| v9 288 threads, tile 1060 | v9 256 threads, tile 940, A/B | 199.336 → 217.809 | −8.5% |
| v8b J=12 (best v8b option) | v8, tile 1000, sustained | 251.584 → 247.312 | +1.7% |
| v8b base-5 | v8b, tile 1000, A/B | 247.229 → 277.318 | −10.9% |
| v8b 288 threads, tile 1100 | v8b, tile 1000, A/B | 247.229 → 290.764 | −15.0% |

The gain came from removing duplicated work (v8 computed 6 words to keep 4; a v9 warp computes 32
groups to keep 30). The options that only moved work onto idle units (pipe balancing, base-5, more
threads) lost under the 35 W cap.

## The explainer page

Open `196-Engine-Fixed.html` in any modern browser. It is one self-contained file: no network access,
no build step, and nothing is sent anywhere. Each section opens with a small example, and the original
technical detail sits under an expandable block.

| Section | What it covers | Interactive |
|---|---|---|
| 1 · Problem | Reverse-and-add, why 196 is hard, digits vs. steps | Start a number (196, 89, 10911, …) and step through it |
| 2 · Fold | Why `x + rev(x)` needs each pair sum only once | Walk 196 + 691 one pair at a time |
| 3 · Carries | How a carry passes through runs of 9s | Animate a carry, replace a 9 with 8, edit pairs |
| 4 · Bit-planes (v4) | Five bit-planes, 32 pairs per 32-bit word | Pick pair sums and read their bits |
| 5 · 128 steps (v5) | Time-blocking: one load and one store per K steps, certified margins | Change the halo and K, re-roll the input |
| 6 · v6r3 → v8 | Barriers, private steps J, and why J=16 failed in v8 | Choose J and tile size; run a window |
| 7 · Base-5 | Splitting a pair sum into 10 + 5 + 2; measured slower | Try pair sums 9, 10, 17, 18 |
| 8 · Speed | Measured A/B and sustained results, v4 to v9 | Choose a comparison; chained speed bars; predictions vs. results |
| 9 · v9 warp windows | What v9 changes, where its gain came from, the mod-9 check | Lane map for 256/288/512 threads; live mod-9 check with a bit flip |
| 10 · Roadmap | Every version, what it tried, and the result | Expandable entries |
| 11 · What's next | Milestone timeline and open items | Hover markers for each milestone |

What counts as measured on the page:

- **Measured on the RTX 4050**: the speed numbers in sections 4–10.
- **Estimates**: the "~20× schoolbook" figure (memory-bandwidth estimate), the chained "≈29×" (a
  product of ratios measured at different sizes, 2M to ~405M digits), and the milestone dates.
- **Static compile counts, not timings**: the v8b-vs-v9 instruction counts in section 9.

## Versions

| Version | Status | Notes |
|---|---|---|
| Original kernel | Reference | One thread per pair; 38.5 µs/step at 2.05M digits |
| v4 | Adopted | Bit-planes, 32 pairs per word; 9.4× |
| v5 | Adopted | Time-blocked tiles, certified intervals, exact replay; run mode |
| v6 / v6r / v6r2 | v6 lost; v6r, v6r2 adopted | Tracking off the busiest warp (1.48×); inlined fast path (1.10×) |
| v6r3 | Adopted | Tile 860 (224 groups for 224 workers); +19.87% sustained |
| v7 / v7r | Lost, kept old engine | Transposed layout (−31%); fewer instructions but −4% |
| v8 | Adopted; production until Oct 13 | Control tape + register windows, J=8; +23.49% sustained |
| v8b | Passed GPU gate; not adopted | 64-bit digit counts, 288 threads, J=12 and base-5 options; best +1.7% |
| **v9** | **Production since Oct 13** | Warp windows, mod-9 fingerprint, includes v8b; +26.3% sustained |

## Repository contents

Packages are zips in the repo root, named `lychrel196_v<N>[_<suffix>].zip`. `math_v<N>.zip` is the
math package.

| File | Contents |
|---|---|
| `196-Engine-Fixed.html` | The explainer page described above |
| `lychrel196_v3_cuda_metal_codex.zip` | CUDA/Metal release: `pair_step_optimized.metal`, `verify_math.py`, `CODEX_TASK.md`, `README.zh.md`, checkpoint |
| `lychrel196_v4_bits.zip` | Bit-plane engine, `bits_core.h`, math identity tests, `bench_vs_old.sh` |
| `lychrel196_v5.zip` | Time-blocked engine, `bits_core.h`, `bits_tb.h`, math tests |
| `lychrel196_v5_diag.zip` | v5 diagnostics (`v5/` headers, driver, SHA-256) |
| `lychrel196_v6.zip`, `_v6r.zip`, `_v6r2.zip`, `_v6r3.zip` | v6 family: CUDA sources, emulators, benches, READMEs |
| `lychrel196_v7.zip` | v7 CUDA source, `math/v7_proto.py` |
| `lychrel196_v7r.zip` | v7r (fewer instructions per word; measured slower): CUDA source, emulator, tests, checkpoint |
| `lychrel196_v8.zip` | v8 engine (rollback): `cuda196_v8.cu`, `driver8.h`, `emu196_v8.cpp`, `tests/`, `baseline_v6r3/`, `bench_v8.sh` |
| `lychrel196_v8b.zip` | v8b: 64-bit digit counts, 288-thread/J/base-5 options, ISF writer, mod-9 and cross-check tools, `bench_v8b.sh` |
| `lychrel196_v9.zip` | v9 production engine: `cuda196_v9.cu`, `emu196_v9.cpp`, `warp_ops.h`, `bits_tb9.h`, `driver9.h`, `bench_v9.sh`, `tools/`, `tests/`, `baseline_v8/`, `baseline_v8b/` |
| `math_v6.zip` | Math package: `recount.py`, `crt_proof.py`, `lut3.py`, `growth_identity.py` |

Each package's own `README.md` has the build commands and test details for that version. The zips are
kept exactly as the GPU agent tested them, so the README inside `lychrel196_v9.zip` still shows the
pre-GPU estimate ("+10–35%"); the measured results are in this file and on the page.

## Rules this project follows

- Measured numbers only, no exaggeration. Estimates are labelled as estimates.
- Exact results: every step's palindrome status is checked, uncertified work is replayed, and no carry
  cutoff is used.
- The production engine changes only after a sustained GPU test wins on the same workload, and only
  with the owner's go-ahead. Benchmarks run on a copy of a checkpoint, never the live file.
