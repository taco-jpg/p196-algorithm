# Exact reverse-and-add of 196 on a single laptop GPU: a bit-sliced, time-blocked engine, and the orbit up to 6.04 × 10⁹ iterations (2.5 × 10⁹ digits)

**Status: draft.** Numbers marked as measured come from the production log of the run described in §6 and were
taken at the stop of the run on 2026-11-09 10:39 UTC. Nothing in this note is Lean-verified. The code is in
`calculation/lychrel196_v10.zip`; the data is in `calculation/paper/data/`.

## Abstract

We describe an exact engine that iterates the reverse-and-add map `N → N + rev(N)` on the number 196 and the
production run that used it. The state of an `n`-digit number is its `⌈n/2⌉` *pair sums* `S_j = d_j + d_{n-1-j}`,
held as five bit-planes. One step is two carry chains (each one binary integer addition per 32 pairs) and a
local update; the growth of the digit count and the palindrome test fall out of the same carries. Because pair
`j` of the next number depends only on pairs `j-1 … j+1` and on runs of pair-sums equal to 9, a block of the GPU can
run up to 256 steps on a tile of the number without talking to its neighbours, tracking at every step the interval
of pairs whose value is still exactly known; if the interval ever fails to cover the block, the window is replayed
by a slow per-step kernel. Inside a 64-step window the pair sums are kept in a decimal-friendly form (a BCD digit
and a carry-generate plane), whose update circuits were found by SAT and genetic search over 3-input logic gates.
The engine ran on one 6 GB RTX 4050 laptop GPU (about 35–43 W) from iteration 523,226,464 (216,579,568 digits) to
iteration 6,040,000,000 (2,500,134,759 digits) in 27.6 days. Every iterate computed in this run was tested for being a
palindrome; none is. The run was checked by exact certification, a mod-9 fingerprint of every window, a chain of
mod-9 checks between archives (202 of 202 passed up to iteration 6,025,000,000), a weekly independent recomputation
by a different kernel (4 of 4 passed) and agreement with the published value at iteration 10⁹.

**Scope.** This note is about computation only. A computation shows what happens in finitely many steps; it does
not say whether a palindrome ever appears, and it is not used in any argument here about all times.

## 1. The problem and what was computed

Write `rev(N)` for the decimal reversal of `N`. Let `N₀ = 196` and `N_{t+1} = N_t + rev(N_t)`. No `N_t` that is a
palindrome has ever been found; whether one exists is open (see the main README of this repository). The standard
way to gather evidence is to push `t` as far as possible and test every `N_t`. The digit count grows
by a nearly constant fraction per step (§6.3: 0.4139 digits per iteration over this run), so the work per step grows
linearly and the work up to iteration `T` grows like `T²`.

The published reference we compare against is the record at iteration 1,000,000,000 (413,930,770 digits) on
p196.org (news page dated 2011-12-27). This run passed that mark about 30 hours after its start and goes on to
6.04 × 10⁹ iterations.

## 2. One step in terms of pair sums

Let `N` have `n` digits `d_{n-1} … d₀` and let `h = ⌈n/2⌉`. Column `j` of `N + rev(N)` adds `d_j + d_{n-1-j}`. This
sum is the same for columns `j` and `n-1-j`, so the whole addition is described by the pair sums

> `S_j = d_j + d_{n-1-j}`,  `0 ≤ j < h`   (`0 ≤ S_j ≤ 18`; for odd `n` the middle pair is `2 d_mid`).

Define the generate and propagate indicators `G_j = [S_j ≥ 10]` and `P_j = [S_j = 9]`. Pair sum 9 propagates a
carry because `9 + 1 = 10`; a pair sum ≥ 10 produces a carry whatever comes in; a pair sum ≤ 8 absorbs it.

**Carries.** The carry into low column `j` is `a_j` and the carry into the mirrored high column `n-1-j` is `b_j`:

- `a_0 = 0`, `a_{j+1} = G_j ∨ (P_j ∧ a_j)`  (carries move up the low half);
- `b_{h-1} = a_h` if `n` is even, `a_{h-1}` if `n` is odd (the carry that crosses the middle),
  `b_{j-1} = G_j ∨ (P_j ∧ b_j)`  (the same recurrence, running down the pair index in the high half).

The carry out of the top column is `b_{-1}`; it is the *growth bit* `g`: `N + rev(N)` has `n+1` digits iff `g = 1`.
It follows from the recurrence that `g` is the generate bit of the **first pair, counted from the outside, whose
sum is not 9** (if every pair sum is 9, the carry across the middle decides).

**The next state.** If `g = 0` the new pair sums are

> `S'_j = 2 S_j + a_j + b_j − 10 (a_{j+1} + b_{j−1})`.

If `g = 1` the number has one more digit and the new pair `j` joins the low digit `lo_j = S_j + a_j − 10 a_{j+1}`
with the high digit of old pair `j−1`, `hi_{j−1} = S_{j−1} + b_{j−1} − 10 b_{j−2}`, where `hi_{−1} = 1` is the new
leading digit: `S'_j = lo_j + hi_{j−1}`. (For even `n` the new middle pair is `2 hi_{h−1}`.) The formulas are
those of `bits_core.h` and were checked against schoolbook big-number arithmetic.

**Palindrome test.** `N_{t+1}` is a palindrome iff its low digit `j` equals its high digit `j` for every `j`. In
terms of the same quantities: if `g = 0` this is `a_j = b_j` for all `j` (the difference of the two digits is
`(a_j − b_j) − 10 (a_{j+1} − b_{j−1})`, which can vanish only if both brackets do); if `g = 1` it is `lo_j = hi_{j−1}`
for all `j`. So the test costs one XOR per word and each iterate is tested exactly once, in the step that produces it.

**Digit sums.** `rev(x)` has the digit sum of `x`, so `x + rev(x) ≡ 2x (mod 9)` for every `x` (used in §5).

## 3. Bit-sliced state

The state is the `h` pair sums, five bits each, stored as five bit-planes of 32-bit words: word `k` of plane `q`
holds bit `q` of `S_{32k} … S_{32k+31}`. At 2.5 × 10⁹ digits this is `5 × 1.25 × 10⁹` bits = 0.78 GB. The GPU
memory in use at 2.47 × 10⁹ digits was 2.38 GiB, consistent with three copies of the state (current, next, and a
backup for replay) plus working space; this is why a 6 GB card suffices.

*Carries as integer additions.* For one word let `X = G ∨ P` (carry-capable pairs). The carry chain
`a_{j+1} = G_j ∨ (P_j a_j)` is the carry chain of the integer addition `X + G + c_in`, so the 32 carries of a word
are `(X + G + c_in) ⊕ X ⊕ G` and the carry out of the word is the carry out of that addition. The high chain is
the same addition on the bit-reversed words. Carries between words are resolved by scanning for the nearest word
that is not "all propagate" (all 32 pairs equal 9, probability about 10⁻³² per word on digit data that look random),
so the arithmetic is exact with no cutoff.

## 4. Time blocking with certified windows

A step touches every word, so a naive GPU implementation streams the whole state from memory each step. The engine
instead lets each thread block keep a *tile* of the state on chip and run many steps on it.

**Locality.** Pair `j` of the next state depends on pairs `j−1, j, j+1` and, through a carry chain, on the run of
9-pairs next to them. Suppose the values on pairs `[L, R)` of a tile are exact and nothing is known outside. After
one step the values are exact on `[L', R')` with

> `L' = (first pair ≥ L whose sum is not 9) + 1`,  `R' = (last pair < R whose sum is not 9) + g`,

because the carry past a non-9 pair no longer depends on the unknown side. (At the outer end of the number, `L = 0`
stays 0; in the middle, the interval is anchored by the carry across the centre.) For digit data that look random a
pair is a 9 with probability 0.1, so each edge moves about 1.1 pairs per step; 64 steps move an edge by about 71 pairs.
The interval is tracked at every step; no approximation or probabilistic argument is involved.

**Growth tape.** The growth bit of each step depends only on the outermost pairs. Before every launch of `K` steps a
small kernel runs the prefix of the number alone and writes `g_0 … g_{K−1}`, certified by the same interval rule, so
thread blocks never wait for each other during the launch. Production used `K = 256`.

**Windows and exact replay.** Three nested units are used. A *launch* is `K = 256` steps on a tile. Inside a launch
each block (v8 and later) works in *register windows* of up to 64 steps: it loads its pairs plus a halo of unverified
pairs, runs the window alone, and at the end compares the certified interval with the pairs it owns. The driver groups
launches into *verification windows* of 8,192 steps. If in a verification window any owned pair is not certified, any
palindrome flag is raised, or the fingerprint of §5 fails, the window is restored from its backup and replayed by
the slow, exact per-step kernel (`v4`), which resolves every carry by full scans. Production recorded 2 such
replays in 5,518 chunks of 10⁶ steps (neither was a fingerprint mismatch). Results are therefore bit-identical to the
schoolbook computation whether or not a window is replayed.

**Warp windows (v9).** The 32 lanes of a warp share a register window and pass the carries that cross lane
boundaries with warp shuffles: 32 groups are loaded and 30 are kept, instead of recomputing a halo word per thread.

**Decimal pair sums in registers (v10).** In v9 each step converted pair sums to carries with a 5-plane add and
subtract. In v10 a window keeps each pair sum as `S = D + 10 G` with `D = S mod 10` in four BCD planes and `G = [S ≥ 10]`
in one. Then `G` and `P = [D = 9]` are exactly the carry generate and propagate planes, and the new pair sum
depends only on the carries into the pair:

- no growth: `D' = (2D + c) mod 10` with `c = a_j + b_j`, and `G' = [D + (a_j ∧ b_j) ≥ 5] ∧ ¬(P ∧ (a_j ∨ b_j))`;
- growth: a BCD addition `D_j + a_j + hi_{j−1}` whose high digit is produced in excess-6 form, so the decimal carry is the
  binary carry out of bit 3.

The gate networks (3-input LOP3 gates, one instruction each) were found by exact SAT synthesis for single outputs
and by Cartesian genetic programming for multi-output functions, and checked exhaustively
(5,246,400 cases, `tests/unit_dg.cpp`). A word's no-growth update costs 10 gates (v9: about 29). The static
instruction counts of the step loop (compiler output, not measured) fall from about 220 ALU-pipe instructions per
lane-step in v9 to about 96 in v10 (2.0× fewer issue slots overall). Conversion between binary planes and `(D, G)`
happens only when a window is loaded or stored, so tiles, checkpoints and the other kernels are unchanged.

## 5. Checking a long run on hardware without ECC

The card has no ECC memory, so a flipped bit is a real possibility over weeks. The run uses five independent layers.

1. **Exactness by construction.** Certification and exact replay (§4). The CPU emulator compiles the very same
   kernel headers (`bits_core.h`, `bits_tb10.h`, `dg_arith.h`), so its gate (every certified block recomputed through
   the exact path; stress tests with planted 9-runs; growth edge cases; a differential v9-versus-v10 test of 120
   inputs; the 2-million-digit checkpoint advanced by 2000 steps in every configuration, equal to the schoolbook
   reference) tests the arithmetic that runs on the GPU.
2. **Mod-9 fingerprint of every window.** With `E_t = x_{t+1} mod 9` computed from the pair sums as
   `2 Σ S_j − [n odd] S_mid (mod 9)`, the identity of §2 requires `E_{t+m} = 2^m E_t (mod 9)`. A single flipped bit
   in a state plane changes the digit sum by `±2^{q+1}` (or `±2^q` for the middle pair of an odd number), never a
   multiple of 9, and later steps only multiply the discrepancy by powers of 2, so any single flipped state bit is detected. A mismatch after a time-blocked verification window triggers the exact replay; a mismatch after the per-step
   kernel stops the run. Over the run no fingerprint replay occurred.
3. **Archive chain.** Every 25 × 10⁶ iterations the checkpoint is compressed, the compressed file is read back and
   its digit SHA-256 compared, and the mod-9 identity between consecutive archives is checked on the digit strings
   themselves (`tools/mod9.c`): 202 of 202 passed (iterations 975,226,464 → 6,025,000,000). The three checkpoints kept at the end (6,038,000,000; 6,039,000,000; 6,040,000,000) also satisfy the identity pairwise (digit sums 1, 7, 4 mod 9; each step of 10⁶ iterations multiplies by 2^(10⁶) ≡ 7).
4. **Weekly independent recomputation.** Once a week (four times so far) 10⁶ steps were recomputed from a saved
   production checkpoint with the per-step reference kernel (a different code path, 3.8–8.8 ms per step against
   0.3–0.7 ms for the production kernel); the result had to equal the production checkpoint byte for byte.
   4 of 4 passed (from iterations 2,083,000,000; 3,594,000,000; 4,895,000,000; 5,922,000,000).
5. **External reference.** At iteration 1,000,000,000 the digit count (413,930,770) and the 25 leading digits
   (`3932472453326071578739224`) equal the published values; the checkpoint was also converted to the ISF format
   used by p196.org (CRC-16 header, 70 digits per line) with `tools/isf.c`.

## 6. The production run

### 6.1 Setup

- Hardware: one NVIDIA GeForce RTX 4050 Laptop GPU (Ada, `sm_89`, 20 SMs, 6 GB, no ECC) with a 13th-gen Core i7 host
  and 30 GB RAM; board power 35 W early in the run and about 42 W (median) later, GPU temperature 68 °C early and
  81 °C (median) later.
- Final configuration: `v10`, 512 threads per block, 64-step register windows, `K = 256`, tile 1892 words (60,544 pairs),
  verification windows of 8,192 steps, checkpoint every 10⁶ iterations, three live checkpoints kept. A supervisor restarts the engine from the newest checkpoint and
  records one observation per checkpoint.
- Start: a checkpoint at iteration 523,226,464 (216,579,568 digits) from an earlier engine generation. This
  paper does not rely on its provenance beyond the agreement at iteration 10⁹.

### 6.2 Engine generations

The engine was upgraded in place at checkpoint boundaries while the run continued; the results of each generation
were required to be identical to the previous one. Medians are over chunks in which the board drew more than 30 W
(this excludes chunks that overlapped a pause).

| Engine | Iterations | Digits (10⁶) | Chunks | Median steps/s |
|---|---|---:|---:|---:|
| v6r2 (tile in shared memory, certified interval) | 523.2 M – 618.2 M | 216.6 – 255.9 | 89 | 4,636 |
| v6r3 (barrier-light) | 619.2 M – 669.2 M | 256.3 – 277.0 | 48 | 4,893 |
| v8 (hybrid blocks with growth tape, 64-bit digit counts) | 670.2 M – 980.2 M | 277.4 – 405.7 | 308 | 4,769 |
| v9 (warp windows) | 981.2 M – 2,489 M | 406.2 – 1,030.3 | 1,492 | 2,851 |
| v10 (decimal pair sums) | 2,490 M – 6,040 M | 1,030.7 – 2,500.1 | 3,551 | 2,219 |

The speed falls as the number grows (the work per step is proportional to `n`). The switch from v9 to v10 can
be read at equal size: around 1.03 × 10⁹ digits the median was 2,060 steps/s (v9, 187 chunks before the switch) and
3,228 steps/s (v10, 160 chunks after it), a factor of 1.57, within the 1.4–1.9 range predicted from the
instruction counts.

### 6.3 Throughput and growth

| Iteration | Digits | Steps/s (one chunk) | µs per step |
|---:|---:|---:|---:|
| 2,490,000,000 | 1,030,678,354 | 3,349 | 297 |
| 3,000,000,000 | 1,241,792,914 | 2,758 | 361 |
| 4,000,000,000 | 1,655,710,949 | 2,370 | 420 |
| 5,000,000,000 | 2,069,641,916 | 1,871 | 532 |
| 5,977,000,000 | 2,474,055,055 | 1,512 | 658 |
| 6,040,000,000 | 2,500,134,759 | 1,535 | 648 |

Over the whole run the digit count grew by 0.41393 digits per iteration; the last chunk before the stop added
413,593 digits for 10⁶ iterations. At 2.5 × 10⁹ digits one step takes 648 µs, about 3.8 × 10¹² digits per second.
In total the run performed about 3.7 × 10¹⁸ pair updates.

### 6.4 Checkpoint hashes

`data/milestones.csv` lists the digit count and the SHA-256 of the digit string (no header, no newline) of the
checkpoint at every multiple of 5 × 10⁸ iterations, and of the final checkpoint. For example, at iteration
10⁹: 413,930,770 digits, SHA-256 `e2418907e5be1f4b3b74a11d904f3e7b069022d0cbd6cdefc1cefc890c822365`. The full
digit files (2–3 GB each) are not stored in this repository.

### 6.5 Result

The run stopped on request at the first checkpoint with at least 2.5 × 10⁹ digits: iteration 6,040,000,000, with
2,500,134,759 digits, on 2026-11-09 at 10:39 UTC, 27.6 days after the start. The leading 25 digits are
`1712328959881746707154772`, the trailing 25 digits are `5187460706747189948933117`, and the SHA-256 of the digit string is
`256b41db46da72891caae69cf51fd9c52a2e5cbe3a6ad804ebd8de0d55b177a9`. The number is not a palindrome. No window needed a
fingerprint replay, two windows needed a certification replay, and all archive, weekly and external checks listed
in §5 passed. This is the end of a finite computation: it says nothing about iterations beyond 6,040,000,000.

## 7. Limits and costs

- Pair indices are 32-bit, so the engine handles `n < 4.29 × 10⁹` digits. Three state copies at that size are about 4 GB
  (within the 6 GB of the card).
- Time per step grows linearly with `n`. Reaching 4 × 10⁹ digits needs iteration ≈ 9.7 × 10⁹; extrapolating the measured
  3.8 × 10¹² digits/s, that is about five to six more weeks on this card (an extrapolation, not a measurement).
- The fingerprint catches any single flip per window, not every multi-bit corruption; the weekly recomputation and the
  archive chain are the backstop. Neither of them can prove the absence of an error that cancelled in all of them.
- Everything above concerns the finitely many iterates computed.

## 8. Reproducing

```bash
unzip calculation/lychrel196_v10.zip && cd lychrel196_v10
nvcc -O3 -std=c++17 -arch=sm_89 cuda196_v10.cu -o cuda196_v10
./cuda196_v10 run checkpoint_4942464.txt 4942464 out --chunk=1000000 --keep=3 --K=256 --tile=1892
cc -O2 tools/mod9.c -o mod9 && ./mod9 A.txt IT_A B.txt IT_B       # mod-9 chain between two checkpoints
./bench_v10.sh gate                                                 # CPU-emulator gate and GPU exactness suites
```

`tools/ref.c` is the schoolbook reference; `tools/crosscheck.sh` is the weekly independent recomputation;
`synth/` reproduces the gate networks.

## References

1. p196.org, news page: record at iteration 10⁹, 413,930,770 digits (2011-12-27).
2. This repository, `calculation/lychrel196_v10.zip` (README, `bits_core.h`, `bits_tb10.h`, `dg_arith.h`, `tests/`, `synth/`).
3. *To add before submission:* the earlier 196 computations and the ISF format description; literature on carry
   chains as integer additions and on SAT / CGP synthesis of small circuits.

## 中文摘要

本文只讲计算。把 N → N + rev(N) 的状态写成“对位和” S_j = d_j + d_(n−1−j) 的五个比特平面；一步由两条进位链（每 32 对一次整数加法）
和一个局部更新组成，位数增长位与回文检测都来自同样的进位。因为下一步的第 j 对只依赖第 j−1…j+1 对以及相邻的“和为 9”的连续段，GPU
的一个线程块可以在不与邻块通信的情况下对一块区域连续做至多 256 步，并逐步跟踪“仍然精确已知”的区间；一旦区间不足以覆盖本块，就用慢速的
逐步内核精确重放。v10 在 64 步窗口内用“BCD 位 + 进位生成位”保存对位和，其更新电路由 SAT 与遗传搜索得到。引擎在一块 6 GB 的 RTX 4050 笔记本
GPU（约 35–43 W）上，从第 523,226,464 次迭代（216,579,568 位）算到第 6,040,000,000 次迭代（2,500,134,759 位），用时 27.6 天；
本次运行中的每个迭代结果都做了回文检测，没有一个是回文。校验手段：精确认证 + 每个窗口的 mod 9 指纹 + 归档之间的 mod 9 链（到 6,025,000,000 为止 202/202 通过）
+ 每周用另一套内核独立重算（4/4 通过）+ 与 2011 年公布的第 10⁹ 次迭代数值一致。计算只说明有限步内的情况，不说明任何关于“永远”的结论。
