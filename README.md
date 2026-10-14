# 196 reverse-and-add: engine history and explainer

This repository holds the engine packages for the exact 196 reverse-and-add (Lychrel) search, and an
interactive explainer page, `196-Engine-Fixed.html`, that walks from the first kernel to the current
versions.

**Production is still v8.** v8b and v9 are built and checked on the CPU emulator, but they have not
been measured on the GPU yet. Nothing on this page marks them as production.

## The explainer page

Open `196-Engine-Fixed.html` in any modern browser. It is one self-contained file: no network access,
no build step, and nothing is sent anywhere. The page is written for a reader who knows ordinary
addition. Each section opens with a small example, and the original technical detail sits under an
expandable "original" block.

| Section | What it covers | Interactive |
|---|---|---|
| 1 · Problem | Reverse-and-add, why 196 is hard, digits vs. steps | Start a number (196, 89, 10911, …) and step through it |
| 2 · Fold | Why `x + rev(x)` needs each pair sum only once | Walk 196 + 691 one pair at a time |
| 3 · Carries | How a carry passes through runs of 9s | Animate a carry, replace a 9 with 8, edit pairs |
| 4 · Bit-planes (v4) | Five bit-planes, 32 pairs per 32-bit word | Pick pair sums and read their bits |
| 5 · 128 steps (v5) | Time-blocking: one load and one store per K steps, certified margins | Change the halo and K, re-roll the input |
| 6 · v6r3 → v8 | Barriers, private steps J, and why J=16 failed | Choose J and tile size; run a window |
| 7 · Base-5 (v8b option) | Splitting a pair sum into 10 + 5 + 2 | Try pair sums 9, 10, 17, 18 |
| 8 · Speed | Measured A/B results from the original runs | Choose a comparison; chained speed bars |
| 9 · v9 warp windows | What v9 changes, and the mod-9 check | Lane map for 256/288/512 threads; live mod-9 check with a bit flip |
| 10 · Roadmap | Every version, what it tried, and the result | Expandable entries |
| 11 · What's next | Milestone timeline and open items | Hover markers for each milestone |

## Status and what counts as measured

- **Measured on the RTX 4050 Laptop GPU** (35 W cap): the speed numbers in sections 4, 5, 6, 8 and 10,
  taken from the A/B and sustained runs recorded in the roadmap.
- **Estimates, not measurements**: the "~20× schoolbook" figure, the Dolbeau speed comparison, and
  the v9 "+10–35%" expectation.
- **Static counts, not timings**: the v8b-vs-v9 instruction counts in section 9. The GPU's executed
  counts will differ.
- **Not yet run on a GPU**: v8b and v9. Their CPU emulator checks are included in the zips; the GPU
  gate, the 2.147e9-digit test, and the A/B are still to do.

## Versions

| Version | Status | Notes |
|---|---|---|
| Original kernel | Reference | One thread per pair; 38.5 µs/step at 2.05M digits |
| v4 | Adopted | Bit-planes, 32 pairs per word |
| v5 | Adopted (became production base) | Time-blocked tiles, certified intervals, exact replay |
| v6 / v6r / v6r2 | v6r adopted, v6 kept old | Lean loop and diagnostics; v6r2 inlined fast path |
| v6r3 | Adopted | Tile 860 (224 groups for 224 workers); +19.87% sustained |
| v7 / v7r | Kept old engine | Transposed layout and fewer instructions, but slower |
| v8 | **Production; passed** | Register windows, J=8; +23.49% sustained, 0 replays |
| v8b | Built, GPU tests pending | 64-bit digit counts (limit ~4.29e9), 288 threads, optional J=12 and base-5 |
| v9 | Built, GPU tests pending | Warp windows, pipe balancing option, mod-9 fingerprint; includes v8b |

v8 refuses to go past 2.147 billion digits, so production must move to a 64-bit engine (v8b or v9)
before then.

## Repository contents

Packages are zips in the repo root, named `lychrel196_v<N>[_<suffix>].zip`. `math_v<N>.zip` is the math
package.

| File | Contents |
|---|---|
| `196-Engine-Fixed.html` | The explainer page described above |
| `lychrel196_v3_cuda_metal_codex.zip` | CUDA/Metal release: `pair_step_optimized.metal`, `verify_math.py`, `CODEX_TASK.md`, `README.zh.md`, checkpoint |
| `lychrel196_v4_bits.zip` | Bit-plane engine, `bits_core.h`, math identity tests, `bench_vs_old.sh` |
| `lychrel196_v5.zip` | Time-blocked engine, `bits_core.h`, `bits_tb.h`, math tests |
| `lychrel196_v5_diag.zip` | v5 diagnostics (`v5/` headers, driver, SHA-256) |
| `lychrel196_v6.zip`, `_v6r.zip`, `_v6r2.zip`, `_v6r3.zip` | v6 family: CUDA sources, emulators, benches, READMEs |
| `lychrel196_v7.zip` | v7 CUDA source, `math/v7_proto.py` |
| `lychrel196_v8.zip` | v8 production engine: `cuda196_v8.cu`, `driver8.h`, `emu196_v8.cpp`, `tests/`, `baseline_v6r3/`, `bench_v8.sh`, `AGENT_TASK.md`. Does not include v8b. |
| `lychrel196_v9.zip` | v9 engine: `cuda196_v9.cu`, `emu196_v9.cpp`, `warp_ops.h`, `bits_tb9.h`, `driver9.h`, `bench_v9.sh`, `tools/`, `tests/`, and the baselines `baseline_v8/` and `baseline_v8b/` (v8b is inside this zip) |
| `math_v6.zip` | Math package: `recount.py`, `crt_proof.py`, `lut3.py`, `growth_identity.py` |

Each package's own `README.md` (where it has one) has the build commands and test details for that
version. For v9, see `lychrel196_v9/README.md` inside its zip.

## Rules this project follows

- Measured numbers only, no exaggeration. Estimates are labelled as estimates.
- Exact results: every certified block is checked, uncertified work is replayed, and no carry cutoff is
  used.
- A change to the production engine happens only after a sustained GPU test wins on the same
  workload.
