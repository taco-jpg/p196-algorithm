# Round 12, agent r12d: K1, centres for the decimal period-8 lattice exteriors, by SAT

Run on the Studio in ~/p196_run/r12d; paths below are relative to this directory.

Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF / UNDECIDED. Nothing here is a claim about 196, and no Lychrel number is
proved. **No certificate was found.** Every search below returned UNSAT / 0 returns, with the exact scope stated.

## 0. Summary

* New tool `tsat.py`: an exact SAT encoding of S reverse-and-add steps of a palindromic pairword with symbolic centre
  symbols, restricted to the complement of the two-inlet rooted prefix (the light cone of the centre). It is validated
  against the cen2 enumerator (five maximal-prefix values), against an independent pairword simulation (85 runs, every
  window cell at every step), against planted targets, and against genuine non-planted returns (the Lean-verified base-9
  lattice certificates are found with C free).
* Fixed-centre exact returns T^(80K)(P(q0,C)) = P(q0+K,C) (COMPUTED + PAPER PROOF reduction). Every legal centre of these
  lengths is excluded (table 4.1):
  * K = 1: rec1 and rec0, |C| <= 25 (was 16 / 14).
  * K = 2: rec1 <= 14, rec0 <= 13. K = 3: rec1 <= 13, rec0 <= 13. Here only rec0 gains one length each (by cen3); the K = 2/3
    cube runs for rec1 did not finish.
  * New periods: K = 4 (period 320), |C| <= 13; K = 5 and K = 6 (400, 480), |C| <= 12; these were never searched before.
  * The rec2 lattice (m = 48, period 192K), also new: K = 1 and 2, |C| <= 12; K = 3, |C| <= 11.
  Partial results beyond that are in 4.2. K = 1 time grows about x2 per unit of |C| at |C| = 25 (7,600 s for one instance),
  so |C| = 40 is out of reach with this encoding.
* Growing centres (task 2): the literal form P(q+K, X C Y) is impossible by a length count; every consistent
  growing-centre induction needs an inner structure that grows. The two classes that need no gun, an absorbing uniform core
  (AbsorbingBand format) and a self-mirror periodic band (LatticeBand format), were searched with a stationary or moving
  seam: no solution in the stated scope. All other inner structures need a gun, so they reduce to K1 for that structure.
* Confined kinks of ANY period (the defect stays in the top w folded columns): none for w <= 12, on both rec0 and rec1, in all
  four phase classes (table 4.5). This is the bounded-width form of K2. The all-width K2 statement is UNDECIDED (section 6).

## 1. Family, reductions, thresholds

P(q,C) = B0 W0^q C rev(W0)^q rev(B0) (pairword, LSB first), C a legal palindromic centre (symbols 0..18, odd |C| has an even
midpoint), lattices rec0, rec1 (m = 20) and rec2 (m = 48) of `lattice_formats/p8_scc.txt`, clock g = 10101010. A return of
period S = 2 m p K / sum(g) = 80K (m = 20) or 192K (m = 48) is T^S(P(q,C)) = P(q+K,C).

* **Shield thresholds** (`shield4.py`: lemma2.py's shield copied verbatim, plus an independent re-implementation; both agree
  everywhere). rec0 and rec1: q0 = 5, 8, 11, **15, 18, 21** for K = 1..6. All q in [q0, 12K+19] pass. rec2: q0 = **4, 6, 9** for
  K = 1, 2, 3. Bold values are new. Log: `shield_thresholds.log`.
* **Insertion kernel** (`lemma_orig.py` = p8_centre_exhaust/lemma.py): 640/640 for rec0 and rec1, and **640/640 for rec2**
  (one literal 48-block after the 11-site cap; new). All B_t have odd coefficients, so shielded states are never palindromes.
  As in P8FixedCentreLen12 (PAPER PROOF, same status), for every q >= q0(K): return(q) iff return(q0).
* **Below the threshold nothing is needed (PAPER PROOF).** A certificate is an infinite chain P(q,C) -> P(q+K,C) ->
  P(q+2K,C) -> ...; once q + jK >= q0 the iff applies. Hence a fixed-centre certificate of period S exists iff the return holds
  at q0(K). If K divides K', a period-80K return gives a period-80K' return at q0(K'). So K = 4 covers K = 1, 2 and K = 6 covers
  K = 1, 2, 3, 6.

## 2. The encoding (tsat.py) and why it is exact

Folded columns i = 0..M_t-1 (M_t = ceil(n_t/2)), n_t = n_0 + g_0 + ... + g_(t-1).
* **Step.** Low carry alpha_0 = 0, alpha_(i+1) = [P_i + alpha_i >= 10], lo_i = (P_i + alpha_i) mod 10 (i < floor(n/2)). For odd n
  the middle digit is (P_mid + alpha_mid) mod 10 and its carry starts the high chain; for even n beta_(n/2) = alpha_(n/2). High:
  hi_i = (P_i + beta_(i+1)) mod 10, beta_i = [P_i + beta_(i+1) >= 10], overflow = beta_0. The digit string of N + rev(N) is
  d_j = lo_j / middle / hi_(n-1-j), plus d_n = 1 on overflow, and P'_i = d_i + d_(n'-1-i) (middle: 2 d_mid). One position-to-
  variable map handles both parities and the overflow shift. This is exactly klib.pairword_step.
* **Window.** R_t is the two-inlet rooted prefix: the folded columns that are identical for every interior, computed with
  both possible carries entering from the centre side (lemma2.py's step). Each instance asserts that the clock is forced there
  (overflow = g_t for every interior). Only columns [a_t, M_t), a_t = |R_t| - 2, are SAT variables. Step t uses columns
  [a_(t+1)-1, M_t); its constants below a_t and the low carry entering at a_(t+1)-1 come from R_t. Columns [a_t, |R_t|) are
  also unit-fixed to R_t. That is redundant, and the `--nounits` and `--margin 6` runs give the same answers. The final rooted
  prefix R_S is checked against the target prefix (`final_prefix_ok=True` in every instance).
* **CNF.** One-hot pairword cells (19 values), one-hot digits (10), carry bits. Adder: for every value x and carry-in c,
  (P = x and cin = c) -> digit = (x+c) mod 10; carry-out: x >= 10 -> 1, x <= 8 -> 0, x = 9 -> cout = cin. Sum: (X = x and Y = y)
  -> P' = x + y. The middle allows only even values. At-least-one and at-most-one constraints hold on digits, free symbols and
  the final row. For inner rows the at-most-one clauses are optional (`--noamo`): they are implied, because two values
  v1 != v2 of one cell would need (v1+c) mod 10 = (v2+c) mod 10, so v2 = v1 +- 10, and the carry clauses of the next adder then
  contradict.
* **Target.** The final row equals P(q0+K, C) on [a_S, M_S): lattice symbols below H1, then the same centre variables.
  Every model is a genuine integer orbit and every genuine orbit is a model, so UNSAT means no legal centre of that length
  returns.
* `cubes2.py` (adaptive cube-and-conquer on the outermost centre symbols: one incremental solver, conflict budget, split the
  undecided cubes) is an exact partition of the centre space, used to parallelise large L.
* `cen3.cpp` is cen2.cpp with the period computed as S = 2 m p K / sum(g) (cen2 hard-codes 80K), needed for rec2. It enumerates
  every centre in exact integer arithmetic, with no pruning.

## 3. Validation (all COMPUTED, logs in logs/val, logs/scale, logs/test)

* **sim:** C fixed, no target, model compared cell by cell with klib.pairword_step at every step. 85 runs (rec0/rec1, K = 1..4,
  |C| = 4..41; rec2; base 9) plus `--noamo`, `--phase` and wall templates (`--simfix`): **0 mismatches**. One early bug (a known
  carry was passed as an int and treated as a constant) was caught by exactly this check; it was fixed before any production run.
* **max prefix vs cen2** (prefix mode: only the first k folded final columns must match). k = maxprefix is SAT and k + 1 is
  UNSAT in every case: rec1 K1 L9 (144), rec0 K1 L6 (139), rec1 K1 L12 (142), rec1 K2 L6 (179), rec0 K3 L5 (218).
  These are all equal to the cen2 histograms of r11a.
* **planted targets** (target = exact image of a random C): SAT for rec1 L13, rec1 L21, rec0 L30 and base 9 L10. Each
  time the solver returned a *different* centre with the identical image. The orbits merge, because N -> N + rev(N) is not
  injective; for rec1 L21 the planted and the found orbit coincide from step 5 on. The image was checked by simulation.
* **genuine returns, C free (positive control):** base-9 lattices from `cert_b9_rec0/1.json` (the Lean-verified certificates):
  b9r0 |C| = 6, 10 SAT with C = [1,1,15,15,1,1] and [1,1,15,15,1,1,15,15,1,1] (the lattice itself), |C| = 4, 8 UNSAT; b9r1
  |C| = 4, 8 SAT ([11,5,5,11], ...), |C| = 6, 10 UNSAT. These were confirmed by independent simulation.
  bandscan control: b9r0 S = 20, mU = 4 finds J = U = [1,1,15,15] and the return holds exactly for band lengths = l0 mod 4.
* **other solvers / variants:** rec1 K1 L12 is UNSAT with cadical195 (108 s), maplechrono (68 s) and glucose4 (787 s); prefix
  L9 k145 is UNSAT with kissat404. rec1 K1 L16 with `--nounits` and with `--margin 6`: UNSAT.
* **SAT against enumeration on the same instances** (both must give UNSAT / 0 returns, and they do): K=4 rec0 L4 and rec1
  L5 (cen3); rec2 K1 L4 (cen3); K2 rec0 L4, L8 and rec1 L4, L8 (cen2, r11a); K3 rec1 L4 and rec0 L8 (cen2). The cubes2 control
  on base 9 finds the genuine returns: b9r0 L10 and b9r1 L8 SAT, b9r0 L8 UNSAT, the same as tsrun.
* **confined kinks vs KINK.md:** rec0 w8 o=0 32, o=1 34; w9 o=0 36; w7 o=2 24, o=3 26 are the same as KINK.md's SAT/DFS
  values.

## 4. Results

All labels in this section are COMPUTED (an exact program run, scope as stated) on top of the PAPER PROOF reduction of
section 1, unless marked otherwise. "UNSAT" means CaDiCaL 1.9.5 (pysat) reported unsatisfiable. No DRAT proof was checked.
Agreement with cen2/cen3, with other solvers and with the controls is listed in section 3.

### 4.1 Fixed centres: combined scope (q >= q0(K), every legal palindromic centre)

| exterior | K (period) | q0 | before this run | excluded now, all \|C\| in | new lengths by | further isolated lengths |
|---|---|---|---|---|---|---|
| rec1 | 1 (80) | 5 | <= 16 (cen2, r11a) | **4..25** | SAT-solver: 9 | - |
| rec1 | 2 (160) | 8 | <= 14 (cen2, r11a) | **4..14** | - | - |
| rec1 | 3 (240) | 11 | <= 13 (cen2, r11a) | **4..13** | - | - |
| rec1 | 4 (320) | 15 | - | **4..13** | SAT-solver: 1, enumeration: 9 | - |
| rec1 | 5 (400) | 18 | - | **4..12** | enumeration: 9 | - |
| rec1 | 6 (480) | 21 | - | **4..12** | enumeration: 9 | - |
| rec0 | 1 (80) | 5 | <= 14 (cen2, r11a) | **4..25** | SAT-solver: 11 | - |
| rec0 | 2 (160) | 8 | <= 12 (cen2, r11a) | **4..13** | enumeration: 1 | - |
| rec0 | 3 (240) | 11 | <= 12 (cen2, r11a) | **4..13** | enumeration: 1 | - |
| rec0 | 4 (320) | 15 | - | **4..13** | SAT-solver: 1, enumeration: 9 | - |
| rec0 | 5 (400) | 18 | - | **4..12** | enumeration: 9 | - |
| rec0 | 6 (480) | 21 | - | **4..12** | enumeration: 9 | - |
| rec2 | 1 (192) | 4 | - | **4..12** | SAT-solver: 1, enumeration: 8 | - |
| rec2 | 2 (384) | 6 | - | **4..12** | enumeration: 9 | - |
| rec2 | 3 (576) | 9 | - | **4..11** | enumeration: 8 | - |

### 4.2 Detail: SAT runs and enumeration runs

**SAT (tsat exact encoding):**

| exterior | K (period) | q0 | |C| UNSAT | |C| SAT | times (s) |
|---|---|---|---|---|---|
| rec0 | 1 (80) | 5 | 15..25 | - | 15:160, 16:195, 17:210, 18:281, 19:653, 20:580, 21:1063, 22:1837, 23:2104, 24:4069, 25:7590 |
| rec0 | 2 (160) | 8 | 4, 8 | - | 4:252, 8:456 |
| rec0 | 3 (240) | 11 | 8 | - | 8:999 |
| rec0 | 4 (320) | 15 | 4 | - | 4:1040 |
| rec1 | 1 (80) | 5 | 17..25 | - | 17:199, 18:242, 19:417, 20:1069, 21:1186, 22:1787, 23:2562, 24:6694, 25:7793 |
| rec1 | 2 (160) | 8 | 4, 8 | - | 4:343, 8:391 |
| rec1 | 3 (240) | 11 | 4 | - | 4:757 |
| rec1 | 4 (320) | 15 | 5 | - | 5:944 |
| rec2 | 1 (192) | 4 | 4 | - | 4:574 |

**Exhaustive enumeration (cen3):**

| exterior | K (period) | q0 | |C| | centres | returns | dev | max prefix / target |
|---|---|---|---|---|---|---|---|
| rec0 | 2 (160) | 8 | 13 | 470,458,810 | 0 | 0 | 200 / 491 |
| rec0 | 3 (240) | 11 | 13 | 470,458,810 | 0 | 0 | 254 / 651 |
| rec0 | 4 (320) | 15 | 4 | 361 | 0 | 0 | 279 / 842 |
| rec0 | 4 (320) | 15 | 5 | 3,610 | 0 | 0 | 279 / 843 |
| rec0 | 4 (320) | 15 | 6 | 6,859 | 0 | 0 | 284 / 844 |
| rec0 | 4 (320) | 15 | 7 | 68,590 | 0 | 0 | 287 / 845 |
| rec0 | 4 (320) | 15 | 8 | 130,321 | 0 | 0 | 294 / 846 |
| rec0 | 4 (320) | 15 | 9 | 1,303,210 | 0 | 0 | 298 / 847 |
| rec0 | 4 (320) | 15 | 10 | 2,476,099 | 0 | 0 | 299 / 848 |
| rec0 | 4 (320) | 15 | 11 | 24,760,990 | 0 | 0 | 301 / 849 |
| rec0 | 4 (320) | 15 | 12 | 47,045,881 | 0 | 0 | 309 / 850 |
| rec0 | 4 (320) | 15 | 13 | 470,458,810 | 0 | 0 | 316 / 851 |
| rec0 | 5 (400) | 18 | 4 | 361 | 0 | 0 | 321 / 1002 |
| rec0 | 5 (400) | 18 | 5 | 3,610 | 0 | 0 | 321 / 1003 |
| rec0 | 5 (400) | 18 | 6 | 6,859 | 0 | 0 | 327 / 1004 |
| rec0 | 5 (400) | 18 | 7 | 68,590 | 0 | 0 | 328 / 1005 |
| rec0 | 5 (400) | 18 | 8 | 130,321 | 0 | 0 | 336 / 1006 |
| rec0 | 5 (400) | 18 | 9 | 1,303,210 | 0 | 0 | 339 / 1007 |
| rec0 | 5 (400) | 18 | 10 | 2,476,099 | 0 | 0 | 341 / 1008 |
| rec0 | 5 (400) | 18 | 11 | 24,760,990 | 0 | 0 | 343 / 1009 |
| rec0 | 5 (400) | 18 | 12 | 47,045,881 | 0 | 0 | 352 / 1010 |
| rec0 | 6 (480) | 21 | 4 | 361 | 0 | 0 | 363 / 1162 |
| rec0 | 6 (480) | 21 | 5 | 3,610 | 0 | 0 | 363 / 1163 |
| rec0 | 6 (480) | 21 | 6 | 6,859 | 0 | 0 | 368 / 1164 |
| rec0 | 6 (480) | 21 | 7 | 68,590 | 0 | 0 | 369 / 1165 |
| rec0 | 6 (480) | 21 | 8 | 130,321 | 0 | 0 | 378 / 1166 |
| rec0 | 6 (480) | 21 | 9 | 1,303,210 | 0 | 0 | 381 / 1167 |
| rec0 | 6 (480) | 21 | 10 | 2,476,099 | 0 | 0 | 383 / 1168 |
| rec0 | 6 (480) | 21 | 11 | 24,760,990 | 0 | 0 | 384 / 1169 |
| rec0 | 6 (480) | 21 | 12 | 47,045,881 | 0 | 0 | 394 / 1170 |
| rec1 | 4 (320) | 15 | 4 | 361 | 0 | 0 | 278 / 842 |
| rec1 | 4 (320) | 15 | 5 | 3,610 | 0 | 0 | 284 / 843 |
| rec1 | 4 (320) | 15 | 6 | 6,859 | 0 | 0 | 284 / 844 |
| rec1 | 4 (320) | 15 | 7 | 68,590 | 0 | 0 | 289 / 845 |
| rec1 | 4 (320) | 15 | 8 | 130,321 | 0 | 0 | 297 / 846 |
| rec1 | 4 (320) | 15 | 9 | 1,303,210 | 0 | 0 | 297 / 847 |
| rec1 | 4 (320) | 15 | 10 | 2,476,099 | 0 | 0 | 311 / 848 |
| rec1 | 4 (320) | 15 | 11 | 24,760,990 | 0 | 0 | 302 / 849 |
| rec1 | 4 (320) | 15 | 12 | 47,045,881 | 0 | 0 | 308 / 850 |
| rec1 | 4 (320) | 15 | 13 | 470,458,810 | 0 | 0 | 318 / 851 |
| rec1 | 5 (400) | 18 | 4 | 361 | 0 | 0 | 319 / 1002 |
| rec1 | 5 (400) | 18 | 5 | 3,610 | 0 | 0 | 326 / 1003 |
| rec1 | 5 (400) | 18 | 6 | 6,859 | 0 | 0 | 326 / 1004 |
| rec1 | 5 (400) | 18 | 7 | 68,590 | 0 | 0 | 331 / 1005 |
| rec1 | 5 (400) | 18 | 8 | 130,321 | 0 | 0 | 338 / 1006 |
| rec1 | 5 (400) | 18 | 9 | 1,303,210 | 0 | 0 | 338 / 1007 |
| rec1 | 5 (400) | 18 | 10 | 2,476,099 | 0 | 0 | 353 / 1008 |
| rec1 | 5 (400) | 18 | 11 | 24,760,990 | 0 | 0 | 344 / 1009 |
| rec1 | 5 (400) | 18 | 12 | 47,045,881 | 0 | 0 | 349 / 1010 |
| rec1 | 6 (480) | 21 | 4 | 361 | 0 | 0 | 362 / 1162 |
| rec1 | 6 (480) | 21 | 5 | 3,610 | 0 | 0 | 368 / 1163 |
| rec1 | 6 (480) | 21 | 6 | 6,859 | 0 | 0 | 368 / 1164 |
| rec1 | 6 (480) | 21 | 7 | 68,590 | 0 | 0 | 373 / 1165 |
| rec1 | 6 (480) | 21 | 8 | 130,321 | 0 | 0 | 379 / 1166 |
| rec1 | 6 (480) | 21 | 9 | 1,303,210 | 0 | 0 | 379 / 1167 |
| rec1 | 6 (480) | 21 | 10 | 2,476,099 | 0 | 0 | 394 / 1168 |
| rec1 | 6 (480) | 21 | 11 | 24,760,990 | 0 | 0 | 386 / 1169 |
| rec1 | 6 (480) | 21 | 12 | 47,045,881 | 0 | 0 | 391 / 1170 |
| rec2 | 1 (192) | 4 | 4 | 361 | 0 | 0 | 189 / 506 |
| rec2 | 1 (192) | 4 | 5 | 3,610 | 0 | 0 | 184 / 507 |
| rec2 | 1 (192) | 4 | 6 | 6,859 | 0 | 0 | 190 / 508 |
| rec2 | 1 (192) | 4 | 7 | 68,590 | 0 | 0 | 192 / 509 |
| rec2 | 1 (192) | 4 | 8 | 130,321 | 0 | 0 | 194 / 510 |
| rec2 | 1 (192) | 4 | 9 | 1,303,210 | 0 | 0 | 202 / 511 |
| rec2 | 1 (192) | 4 | 10 | 2,476,099 | 0 | 0 | 201 / 512 |
| rec2 | 1 (192) | 4 | 11 | 24,760,990 | 0 | 0 | 204 / 513 |
| rec2 | 1 (192) | 4 | 12 | 47,045,881 | 0 | 0 | 203 / 514 |
| rec2 | 2 (384) | 6 | 4 | 361 | 0 | 0 | 259 / 794 |
| rec2 | 2 (384) | 6 | 5 | 3,610 | 0 | 0 | 256 / 795 |
| rec2 | 2 (384) | 6 | 6 | 6,859 | 0 | 0 | 256 / 796 |
| rec2 | 2 (384) | 6 | 7 | 68,590 | 0 | 0 | 265 / 797 |
| rec2 | 2 (384) | 6 | 8 | 130,321 | 0 | 0 | 265 / 798 |
| rec2 | 2 (384) | 6 | 9 | 1,303,210 | 0 | 0 | 271 / 799 |
| rec2 | 2 (384) | 6 | 10 | 2,476,099 | 0 | 0 | 270 / 800 |
| rec2 | 2 (384) | 6 | 11 | 24,760,990 | 0 | 0 | 279 / 801 |
| rec2 | 2 (384) | 6 | 12 | 47,045,881 | 0 | 0 | 275 / 802 |
| rec2 | 3 (576) | 9 | 4 | 361 | 0 | 0 | 376 / 1178 |
| rec2 | 3 (576) | 9 | 5 | 3,610 | 0 | 0 | 374 / 1179 |
| rec2 | 3 (576) | 9 | 6 | 6,859 | 0 | 0 | 374 / 1180 |
| rec2 | 3 (576) | 9 | 7 | 68,590 | 0 | 0 | 382 / 1181 |
| rec2 | 3 (576) | 9 | 8 | 130,321 | 0 | 0 | 388 / 1182 |
| rec2 | 3 (576) | 9 | 9 | 1,303,210 | 0 | 0 | 388 / 1183 |
| rec2 | 3 (576) | 9 | 10 | 2,476,099 | 0 | 0 | 389 / 1184 |
| rec2 | 3 (576) | 9 | 11 | 24,760,990 | 0 | 0 | 398 / 1185 |

Moving centres of the same length. In every enumeration the maximal matching prefix stays far below H1 = nB + m(q0+K), the
end of the lattice part of the target. So **no** centre of these lengths even restores the lattice after S steps, which
excludes moving-centre chains of that length whose lattice is restored every S steps:
* K = 4: max prefix <= 318 < H1 = 419. K = 5: <= 353 < 499. K = 6: <= 394 < 579.
* rec2 K = 1: <= 204 < 251. rec2 K = 2: <= 279 < 395. rec2 K = 3: <= 398 < 587.
* rec0 K = 2, |C| = 13: 200 < 239. rec0 K = 3, |C| = 13: 254 < 319.
For K = 1..3 and |C| up to 16 / 14 / 13 the cen2 histograms of r11a show the same: max prefix 147 < 159, 200 < 239, 257 < 319.

**Partial results (UNDECIDED as a whole, exact for the stated part).** All of these were stopped at the wrap-up.
* K = 1, |C| = 26: the monolithic runs (rec0, rec1) were stopped after about 2.5 h with no answer.
* K = 1, |C| = 27, by cube-and-conquer: every centre with outermost symbol c0 in 0..14 (rec0) or 0..9 (rec1) is UNSAT.
* K = 1, |C| = 28, rec1: every centre with c0 in 0..9 is UNSAT.
* The remaining c0 ranges, the cubes2 runs K = 2 rec1 |C| = 15, K = 2 rec0 |C| = 14 and K = 3 rec1 |C| = 14, and cen3 rec0 K2 L14 /
  rec1 K3 L14 did not finish.
* The cube statistics show very uneven hardness. The c0 in [0,5) splits took 20-36 s, rec1 [5,10) 27 s and rec0 [10,15)
  54 s. rec0 [5,10) took 5,519 s. The rec1 [10,15) and both [15,19) splits were still open after more than 1.5 h.

### 4.3 Growing centres with an absorbing core (wallscan.py)

| exterior | S | Kb | w | r | cores | instances | result |
|---|---|---|---|---|---|---|---|
| rec0 | 16 | 0 | 12 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec0 | 16 | 0 | 24 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec0 | 24 | 0 | 12 | r=[0,20) | [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] | 200 | DONE 200 UNSAT |
| rec0 | 24 | 0 | 16 | r=[0,20) | [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] | 115 | PARTIAL 115 UNSAT |
| rec0 | 8 | 0 | 12 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec0 | 8 | 0 | 24 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec1 | 16 | 0 | 12 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec1 | 16 | 0 | 24 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec1 | 24 | 0 | 12 | r=[0,20) | [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] | 200 | DONE 200 UNSAT |
| rec1 | 24 | 0 | 16 | r=[0,20) | [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] | 124 | PARTIAL 124 UNSAT |
| rec1 | 24 | 0 | 24 | r=[0,20) | [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] | 8 | PARTIAL 8 UNSAT (stopped) |
| rec1 | 8 | 0 | 12 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec1 | 8 | 0 | 24 | r=[0,20) | [0, 6, 12, 18] | 80 | DONE 80 UNSAT |
| rec2 | 16 | 0 | 12 | r=[0,48) | [0, 6, 12, 18] | 192 | DONE 192 UNSAT |
| rec2 | 24 | 0 | 12 | r=[0,48) | [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] | 2 | PARTIAL 2 UNSAT |
| rec2 | 8 | 0 | 12 | r=[0,48) | [0, 6, 12, 18] | 192 | DONE 192 UNSAT |

### 4.4 Growing centres with a periodic inner band (bandscan.py)

| exterior | S | w | mU | l0 | result |
|---|---|---|---|---|---|
| rec0 | 16 | 28 | 2 | 48 | UNSAT |
| rec0 | 16 | 28 | 2 | 49 | UNSAT |
| rec0 | 16 | 28 | 2 | 50 | UNSAT |
| rec0 | 16 | 28 | 2 | 51 | UNSAT |
| rec0 | 16 | 28 | 4 | 48 | UNSAT |
| rec0 | 16 | 28 | 4 | 49 | UNSAT |
| rec0 | 16 | 28 | 4 | 50 | UNSAT |
| rec0 | 16 | 28 | 4 | 51 | UNSAT |
| rec0 | 16 | 28 | 4 | 52 | UNSAT |
| rec0 | 16 | 28 | 4 | 53 | UNSAT |
| rec0 | 16 | 28 | 4 | 54 | UNSAT |
| rec0 | 16 | 28 | 4 | 55 | UNSAT |
| rec1 | 16 | 28 | 2 | 48 | UNSAT |
| rec1 | 16 | 28 | 2 | 49 | UNSAT |
| rec1 | 16 | 28 | 2 | 50 | UNSAT |
| rec1 | 16 | 28 | 2 | 51 | UNSAT |
| rec1 | 16 | 28 | 4 | 48 | UNSAT |
| rec1 | 16 | 28 | 4 | 49 | UNSAT |
| rec1 | 16 | 28 | 4 | 50 | UNSAT |
| rec1 | 16 | 28 | 4 | 51 | UNSAT |
| rec1 | 16 | 28 | 4 | 52 | UNSAT |
| rec1 | 16 | 28 | 4 | 53 | UNSAT |
| rec1 | 16 | 28 | 4 | 54 | UNSAT |
| rec1 | 16 | 28 | 4 | 55 | UNSAT |

### 4.5 Confined kinks of any period (survscan.py)

| exterior | w | lifetime o=0 | o=1 | o=2 | o=3 | all classes die |
|---|---|---|---|---|---|---|
| rec0 | 6 | 21 | 22 | 20 | 22 | yes |
| rec0 | 7 | 25 | 33 | 24 | 26 | yes |
| rec0 | 8 | 32 | 34 | 28 | 34 | yes |
| rec0 | 9 | 36 | 42 | 37 | 38 | yes |
| rec0 | 10 | 40 | 45 | 41 | 43 | yes |
| rec0 | 11 | 48 | 46 | 48 | 46 | yes |
| rec0 | 12 | 60 | 50 | 49 | 53 | yes |
| rec0 | 13 | 63 | - | - | - | partial |
| rec0 | 14 | - | - | - | - | partial |
| rec1 | 6 | 21 | 25 | 24 | 34 | yes |
| rec1 | 7 | 28 | 26 | 24 | 37 | yes |
| rec1 | 8 | 36 | 29 | 36 | 35 | yes |
| rec1 | 9 | 41 | 41 | 40 | 46 | yes |
| rec1 | 10 | 40 | 46 | 44 | 43 | yes |
| rec1 | 11 | 52 | 46 | 44 | 47 | yes |
| rec1 | 12 | 52 | 50 | 52 | 51 | yes |
| rec1 | 13 | - | - | - | - | partial |

## 5. Growing centres (task 2): the induction such a return would need

* **The literal form is impossible (PAPER PROOF).** For q >= q0(K) the overflow sequence of the first 80K steps is forced by
  the cap, whatever the interior. So |T^(80K) P(q,C)| = |P(q,C)| + 40K = |P(q+K,C)|, which forces |X| + |Y| = 0 in
  T^(80K)(P(q,C)) = P(q+K, X C Y). For q < q0 the lattice count grows every period, so the chain reaches q >= q0 and the same
  count applies.
* **Consistent form.** The lattice gains Kb <= K blocks per side per period, and the centre gains dh = 40(K - Kb)
  coefficients:
  T^(80K)(P(q, C_j)) = P(q+Kb, C_(j+1)), |C_(j+1)| = |C_j| + dh. A finite certificate needs a finite description of the C_j.
  Its natural form is C_j = J Z_j rev(J), with an inner structure Z_j that grows by dh per period. An induction over j then
  needs four things:
  (i) Z is spatially periodic with block U, time-periodic in the clock, and absorbing (its carry-out does not depend on its
      carry-in). This gives the pumping lemma, as the 640-case kernel does for W0.
  (ii) Z closes at the middle. Either U is **self-mirror** (no core needed: LatticeBand / AbsorbingBand format, Lean
      infrastructure exists), or Z ends in a core that is a time-periodic centre (a gun) **for U**. The second case is
      problem K1 again, for the lattice U.
  (iii) The seam J between W0 and U returns: it is stationary for Kb = 0 and moves with the lattice for Kb > 0. This is a
      finite check.
  (iv) Shield thresholds on both sides, as in the two-counter pumping of T12 (r11c NOTES).
  So the only growing centres that need no gun are **(G2)** a uniform absorbing core c^h (c on one of the loops {0}, {18},
  {6,12}, {2,4,8,16,14,10}) and **(G3)** a self-mirror periodic band. Both were searched with an exact seam J (tables 4.3, 4.4).
  The template is the same encoder with constants and free symbols in the centre. A core length h0 >= 2S + 10 makes the
  result independent of h: a core cell != 9 absorbs every carry, so the seam's influence enters the core at most one column per
  step, and the two seams cannot interact within S steps. A certificate must work for every large h, so UNSAT at h0 is an
  exclusion.
  Known before: the uniform-band census (FORMATS.md 8.2) decided the period-8 stream (10)^4 (no hit, any width). Our S = 8 runs
  reproduce this for w <= 24. S = 16, 24, ... are the dense streams (10)^8, (10)^12 that the census could not decide (capped);
  here they are covered only in the restricted form "p8 lattice + seam of width <= w + core/band".
* Inner structures that are not self-mirror (rec0/rec1/rec2 at another phase, a T12-like U lattice) need a gun for U. For the
  p8 clock this is K1 for that lattice. rec2 is covered in table 4.1.

## 6. K2 (wall-speed argument)

* **Exact form.** For a fixed-centre return the lattice front F_t (the first folded column that differs from the lattice in
  the root frame) must advance by exactly 20K in 80K steps. For a kink of any period the front must advance at mean speed
  exactly 1/4 for ever, with a bounded defect behind it.
* **A local bound c < 1/4 is false.** In genuine orbits the front can run faster than 1/4. For the best |C| = 9 centre
  (prefix 144, `spacetime.py`) the front moves 139 -> 144 over t = 0..44, then 144 -> 148 over t = 44..52 (0.5 per step), and
  then recedes to 144 by t = 80. A front game with an adversarial interior is trivially lost, because the adversary can imitate
  the lattice. So K2 cannot be a local front-speed lemma. It needs a global invariant (mod 9 and mod 11 give only linear
  congruences on C, as KINK.md notes).
* **Decided: the bounded-width version.** No defect confined to the top w folded columns survives for w <= 12
  (table 4.5, any period; rec0 and rec1, all four classes). Lifetimes grow roughly as 4w..5w, so in its lifetime the frame advances by about one defect width.
  A confined defect seems able to "pay" for the lattice it must emit only for about its own width. This suggests a fuel-type
  invariant, but it is UNDECIDED and there is no proof.
* All widths: **UNDECIDED.** A proof would be K1 itself (no gun for the p8 lattices).

## 7. What is still open (UNDECIDED)

* Fixed centres beyond the bounds of table 4.1. The monolithic K = 1 time grew from 242 s (|C| = 18) to 7,800 s (|C| = 25),
  about x2 per unit of |C| at the end. That puts |C| = 40 at more than 10^7 CPU-s per instance with this encoding. Cube
  splitting helps only on the easy c0 ranges. Periods K >= 7 were not searched.
* Moving centres of the same length (any C' after S steps). These are excluded only where a max-prefix histogram exists: K = 1
  to |C| <= 16, K = 2 to 14, K = 3 to 13 (cen2), K = 4 to 13, K = 5 and K = 6 to 12, rec2 K = 1 and K = 2 to 12, rec2 K = 3 to
  11 (cen3).
* G2 / G3 beyond the scanned (S, w, mU, l0):
  * S >= 32 walls;
  * S = 24 walls of width 16 (about 60 % done);
  * bands with mU >= 8 or S != 16;
  * walls and seams closer to the cap than q0(S) (q0(S) = 2 for S <= 24, 3 for S = 32..48).
* K2 for all widths. No fuel invariant has been found.

## 8. Protocol for a hit (prepared, not needed)

`verify_hit.py` replays a candidate with two independent implementations at every step: klib.pairword_step on the pairword,
and plain Python integers N + int(str(N)[::-1]) with the pairword recomputed from the digit string. It runs >= 20,000 steps and
>= 3 periods, and checks no palindrome, the clock, and the exact template at every multiple of the period. It writes the
pairwords of one period, the overflow word and N0 as JSON for the Lean side. A wall + core hit fits the AbsorbingBand format
(B = B0 W0^q W0[:r] J, band c). A band hit fits LatticeBand (B as above, band U). A fixed-centre hit needs a new format (lattice
+ centre); its finite data are the per-step pairwords plus the 640-case insertion kernel. Self-test: the max-prefix rec1 L9
centre is replayed correctly and rejected at t = 80 (NO_RETURN).

## 9. Files (this directory; binaries not included)

Sources:
* `tsat.py`: the exact encoder (templates, any base). Packaging fix: `solve_inst` now catches the NotImplementedError that
  PySAT's Kissat raises from `accum_stats` (the first kissat404 run of the main-session check crashed there after solving);
  nothing else changed.
* `tsrun.py`: driver for ret / lat / prefix / sim / planted / wall.
* `cubes2.py` and `cubes.py`: cube-and-conquer.
* `wallscan.py`: G2 absorbing-core walls. `bandscan.py`: G3 periodic inner bands. `survscan.py` and `survall.py`: confined
  kinks.
* `shield4.py`: thresholds. `lemma_orig.py`: the insertion kernel, a copy of `../../lattice_kinks/p8_centre_exhaust/lemma.py`
  with only the import path changed.
* `cen3.cpp`: `../../round11/p8_stack_centres/cen2.cpp` with the general period and HN = 2048 (`c++ -O3 -std=c++17 -o cen3 cen3.cpp`).
  `rec2.tbl`: the rec2 table for cen3, exported from klib; `rec0.tbl`, `rec1.tbl` are copies of the round-11 tables.
* `verify_hit.py`: the hit protocol. `spacetime.py`: the front data of section 6.
* `pool.py` and `watchdog.py`: job pool and RSS guard; `jobs_*.txt`: the job lists. `collect.py`, `final_tables.py`, `scope.py`,
  `assemble_final.py`: report generation (`scope_table.md`).
* `retsat.py`: the first version of the encoder. It is superseded by tsat.py and kept for the history of the bug found by the
  sim check (and for `rooted_rows`, used by shield4.py).

klib.py, p8_scc.txt and the base-9 certificate JSON are read from the repository (`../../lattice_kinks/edge_relaxation`,
`../../lattice_formats`). The round-11 helpers lemma2.py, lemma2s.py, bigint2.py, stackcheck.py, mkstack.py, ref2gen.py,
cen2.cpp, stk1.tbl were used unchanged from `../../round11/p8_stack_centres/` and are not repeated here.

Logs:
* `shield_thresholds.log`, `shield4.log`, `shield4_rec2.log`, `lemma_rec{0,1,2}.log` (full output of `python3 lemma_orig.py recN`,
  header and PASS (1) included).
* `logs/prod`: SAT production (`RESULT` lines). `logs/cen`: cen3 enumeration (`RESULT ... returns=0`).
* `logs/wall` and `logs/band`: growing centres. `logs/surv`: confined kinks.
* `logs/main_check/`: the main-session check (README.txt; independent enumerator `indep_enum.py`, base-9 check `b9check.py`,
  maplechrono and kissat404 reruns, rec2 prefix k = 189/190).
* Packed in `logs.tar.gz`: `logs/val` (validation), `logs/scale`, `logs/test` (timings and controls), the pool logs.

Reproduce one line of each kind:
* `python3 tsrun.py ret --lat rec1 --q0 5 --K 1 --L 20`
* `python3 cubes2.py ret rec0 5 1 27 --lo 0 --hi 5`
* `./cen3 rec1.tbl 12 15 4 6`
* `python3 wallscan.py rec1 16 0 24`
* `python3 bandscan.py rec1 16 0 28 4 0 1 --l0 52`
* `python3 survscan.py rec1 10 32`
* `python3 tsrun.py sim --lat rec0 --q0 15 --K 4 --L 20 --seed 5`
* `python3 shield4.py`; `python3 lemma_orig.py rec0` (and rec1, rec2)

These need python-sat (cadical195) and a C++17 compiler.
