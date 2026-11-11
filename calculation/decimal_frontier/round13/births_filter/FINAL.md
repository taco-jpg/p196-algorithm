# Report of agent r13c (round 13, 2026-11-08), as delivered; paths shortened, pass-2 status made final; NOTES.md (agent log) and the FINAL_*.md parts are not shipped. Large files not shipped: out/*/deaths.txt (up to 193 MB), out/allL/n12_iflist.txt (1.4 MB); binaries in bin/ are not shipped (build from src/).

# r13c FINAL: a primitive-part filter for the clock families (01)^{4m} and (0001)^{3k}: births above saturated interfaces

Studio run directory `~/p196_run/r13c`. Repository read only, nothing pushed or posted. Labels: PAPER PROOF / COMPUTED / UNDECIDED; nothing here is LEAN-VERIFIED and nothing is claimed about 196. Section 5 was generated from the run outputs (`py/mk_results.py`); the other sections are hand-written.

## 0. Summary

1. **The naive "primitive part empty" filter is the wrong statement (PAPER).** "At level K no closed L-walk is non-periodic" neither holds for the families here (the exact closed-walk sets of G_K are dominated by primitive walks at every level K) nor would it suffice: a closed L-walk of G_{K+1} can be non-d-periodic although its projection to G_K is d-periodic (late desynchronisation). Section 1.
2. **Theorem B (PAPER PROOF, section 2).** Fix a base period d0 (8 on clock 01, 12 on clock 0001). The set IF(d0) of *interfaces* of d0-periodic heads is finite and computed exactly by BFS (22,601 interfaces, saturation height a0 = 87; resp. 22,657, a0 = 70). An infinite closed L-history (ICH; every exterior, uniform-band template or lattice with clock g of length L is one) that is not d0-periodic has a first non-d0-periodic column (the *birth*) above a d0-periodic head; above that birth one gets a relative K-head tower with a fixed L-periodic bottom. If all these finitely many towers die, then every ICH of period L is d0-periodic. (Theorem B′ is the plain K-head form, Lemma AL the all-L pre-filter.) Rotation by the clock period reduces the towers by the factor L/P.
3. **Computed instances (COMPUTED + Theorem B, table in section 5; "DIES-primitive" means all births die).** Complete: clock (01)^8 (T = 16): every ICH is 8-periodic; clock (0001)^6 (T = 24) and (0001)^9 (T = 36): every ICH is 12-periodic (second proofs of P(6), P(9), independent of ReachDisk and r12b Theorem U, and stronger: they cover all closed histories, not only 9-wire exteriors). Partial (UNDECIDED remainder listed): (01)^12 (T = 24), (01)^16 (T = 32), (0001)^12 = N12^4 (T = 48), (0001)^15 = N12^5 (T = 60), and two imprimitive capped census words (root lengths 9 and 14, T = 54 and 56), which are reduced to one tower each; the imprimitive capped census word (00010010111)^5 (root length 11, T = 55) is DECIDED: all 1,240,956 tower classes die, and the root word itself has no closed 11-walk at level 45, so no ICH of period 55 exists at all (no exterior, band or lattice).
4. **Controls.** Clock 0001 at d0 = 4, L = 12: exactly 1 of the 12 tower classes survives and it is N12 (its birth column is N12's column 2; windows checked independently). Base-9 clock (11000)^2 at d0 = 5, L = 10: 1 of 63 tower classes survives and it is the Lean-verified base-9 certificate (its birth column is the certificate's first non-5-periodic column 13). Clock 01 at d0 = 4, L = 8: the single tower class survives, its birth column is the known period-8 lock column. p11 at d0 = 11, L = 22, 33, 44: all towers die (known answer, r12b Theorem U).
5. **Validation of the reduction.** Plain K-head exact sets (khp) and the towers agree exactly on Rig(K), the first non-periodic column of the closed walks at level K: for (01, L = 16) at K = 1..40 and at every checked level up to 120 (including the jumps 3 -> 7 at K = 30 and 7 -> 22 at K = 119); for (0001, L = 36) at all 35 checked levels up to K = 500. Independent recomputations of towers (Python, C++) and of the birth lists agree.
6. **Limits.** All multiples at once (Corollary T): only partial (for clock 0001 the all-L test certifies 22,518 of 22,657 interfaces as birth-free/dead for every L; 139 "hard" interfaces remain); the primitive capped census words have no proper divisor period, so Theorem B does not apply to them; no certificate is produced.


## 1. The notion of primitivity: births, not levels

Notation of r12b FINAL §2: base b = 10, clock g ∈ {0,1}^P (extended P-periodically), K-head graph G_K(g), carries H_i(t), L_i(t), `trans`.

**ICH (infinite closed L-history), PAPER.** For P | L: columns x_i(t) ∈ 0..18 (i ≥ 0, t ∈ Z/L, x_0(t) ≥ 1) and bits H_i(t), L_i(t) with L_0 = 0, H_0(t) = g_t and, for all i, t:
 (R1) H_i(t) = ⌊(x_i(t) + H_{i+1}(t))/b⌋, (R2) L_{i+1}(t) = ⌊(x_i(t) + L_i(t))/b⌋,
 (R3) x_i(t+1) = (x_i(t) + L_i(t)) mod b + (g_t ? (i=0 ? 1 : (x_{i−1}(t)+H_i(t)) mod b) : (x_i(t)+H_{i+1}(t)) mod b).
By r12b Lemma K1/K4, the K-heads of an ICH are closed L-walks of G_K(g), and by König's lemma a family of compatible closed L-walks of all G_K is an ICH.
Exteriors (any width, padded with 9s, Lemma K2), uniform-band templates (Lemma K3: the columns above the left end are u_t) and lattices (columns L-periodic, spatially periodic above a preamble) with clock g of length L all give ICHs of period L. An ICH is **d-periodic** (d | L, P | d) if x_i(t+d) = x_i(t) for all i, t.

**Why "the primitive part of G_K is empty at some K" cannot be the criterion.** A closed L-walk of G_{K+1} may be non-d-periodic although its projection to G_K is d-periodic (late desynchronisation): the d-periodic head can be extended by a non-d-periodic column. So "at level K every closed L-walk is a repetition" (i) is a statement about the first K columns only, and (ii) is false at every K for the families in question: for clock 01, L = 16, the exact closed-walk node set at K = 104 has 718,603 nodes, almost all on primitive walks (khp: 1,556,644 ordered off-diagonal closure pairs); the first non-8-periodic column of the closed walks ("Rig(K)", section 4) grows only slowly. The correct unit of analysis is the **birth**: the first non-d-periodic column of a history. Everything above a d-periodic head depends only on a finite *interface*, so births can be analysed one interface at a time.

## 2. Theorem B (PAPER PROOF)

**Interface of a d-periodic head.** Let P | d. A d-periodic head W of height a ≥ 0 is a closed d-walk of G_a(g) (a = 0: the empty head). Its interface is I(W) = (c(t), xb(t) [t with g_t = 1], A(t)), t ∈ Z/d, where c(t) = L_a(t) (forward carry into column a), xb(t) = x_{a−1}(t) (for a = 0 the root: "part = 1", and column 0 digits ≥ 1), A(t) = {h ∈ {0,1} : W has an edge from x(t) to x(t+1) with top bit h} (for a = 0: A(t) = {g_t}).

**Lemma I1 (locality).** Let d | L and let v(t), t ∈ Z/L, be a column above I. Put for each t: A'(t) = {h : H := ⌊(v(t)+h)/b⌋ ∈ A(t), y(h) = v(t+1)}, where y(h) = (v(t)+c(t)) mod b + (g_t ? (xb(t)+H) mod b [root: 1] : (v(t)+h) mod b). Then W extended by the column v is a head with edges exactly when all A'(t) ≠ ∅, and its interface above v is (⌊(v+c)/b⌋, v, A') (L-periodic). Consequently the whole future above W (all columns ≥ a, with all carry conditions) depends only on I(W).
*Proof.* Direct from trans / Lemma K4: an edge at level a+1 with top bit h restricted to the low a columns is the edge with top bit H; the only new condition is the digit y_a = v(t+1). ∎

**Lemma I2 (saturation).** IF(d) := {I(W) : W a d-periodic head of any height} is finite and is computed by BFS from the root interface, each step adding one d-periodic column (a closed d-walk of the level-1 relative graph of Lemma I1); it stops when no new interface appears. (Lemma I1 shows the BFS reaches exactly the interfaces of d-periodic heads, because closed d-walks of G_a project to closed d-walks of G_{a−1}.)

**Relative tower.** An L-periodic interface I' (above a fixed column) defines a K-head construction: level-1 nodes (w, t), w ∈ 0..18, t ∈ Z/L, with edges of Lemma I1; levels ≥ 2 by the incremental rule of khx (r12b §1). Pruning: trim and exact closed-L-walk node set (r12e -exactset; one lap, since phases are mod L). "The tower DIES at level r" means: no closed L-walk with r columns above the fixed column exists.

**Theorem B.** Let P | d | L. Suppose that for every I ∈ IF(d) and every closed L-column v above I that is not d-periodic, the relative tower above (I, v) dies. Then every ICH of period L is d-periodic. Hence every exterior, uniform-band template or lattice with clock g of length L is d-periodic, i.e. a repetition of one of period d.

*Proof.* Let X be an ICH of period L that is not d-periodic and let a be the least index such that x_a(·) is not d-periodic. Columns 0..a−1 form a d-periodic head W with interface I := I(W) ∈ IF(d) and v := x_a is a closed L-column above I, not d-periodic. By Lemma I1, for every r the columns a+1..a+r of X form a closed L-walk of the relative tower above (I, v). This contradicts its death. The consequence follows from the fact that exteriors/bands/lattices are ICHs (with x_i(t+d) = x_i(t) meaning: the object repeats with period d). ∎

**Theorem B′ (plain form).** Let a0 = the saturation level of IF(d). If at some level K every closed L-walk of G_K has a d-periodic (a0+1)-head, then every ICH of period L is d-periodic. (Same proof: a birth above height > a0 can be transplanted, with Lemma I1, to the same interface at height ≤ a0, which produces a closed L-walk at level K with non-d-periodic (a0+1)-head.)
Theorem B′ is checked for small K independently of the towers (section 4), but towers are the efficient route (the plain sets at L = 16 reach 10^6 nodes at K ≈ 110 while the worst relative tower is small).

**Rotation symmetry (used to cut the work, PAPER).** A time rotation by a multiple of P maps (I, v) to (rot I, rot v) with the same tower behaviour (the clock is P-periodic). Towers are run once per rotation class; the Lemma above applies to any representative.

**All-L test (Lemma AL, partial transfer to all multiples, PAPER).** Let I ∈ IF(d). Build the relative graphs H_r(I) with phases mod d (not L), level 1 = the column above I, and keep at each level only the nodes in cyclic SCCs. If at some r the graph is empty (DEAD), or every cyclic SCC has its level-1 digit a function of the phase (BIRTHFREE), then **for every L (multiple of d)** no closed L-walk has a non-d-periodic column directly above I. So a BIRTHFREE/DEAD interface carries no birth for any L; only the remaining "hard" interfaces need the L-specific towers. (Used as a pre-filter; if the list of hard interfaces is empty this is an all-L theorem.)

## 4. Validation (COMPUTED; each item can be re-run with the commands of section 7)

1. **IF(d) BFS, two implementations.** `py/ifsat.py` (Python) and `bin/khr` (C++) give identical interface counts and saturation levels: g = 01, d = 8: 22,601 / a0 = 87; g = 0001, d = 12: 22,657 / a0 = 70.
2. **Birth enumeration, two implementations.** For (g, d, L) = (01, 8, 16): `py/births_check.py` (independent Python: its own BFS, its own closed-column DFS) and `khr` list exactly the same 68,520 distinct interfaces I' above the births.
3. **Towers, independent recomputation.** `py/khr_check.py` (dict windows, full-window transitions recomputed from scratch for every edge, explicit forward/backward closed-walk search; no code shared with khr) and `src/kh3.cpp` (C++, string windows, full-window transitions, per-source forward+backward walks) on random samples of the L = 16 towers: 800 (D ≤ 25) + 3,000 (D ≤ 45) identical death levels in Python, 60 (D ≤ 80) identical in kh3 for L = 16; for (0001, 12, 36) kh3 on 68 random towers (death levels 20..107): 66 identical, 2 skipped by the kh3 node cap, 0 differences (`ctrl/kh3_N36.out`); 0 differences in all checks.
4. **Tower deaths vs the plain K-head graph (the whole reduction).** `src/khp.cpp` = r12e khxt + at chosen levels a test on the plain exact closed-L-walk set: Rig(K) := the first column at which some closed L-walk of G_K is not d-periodic (computed via the pairs u, u′ with u ->^d u′ ->^{L-d} u, windows compared). Prediction from the towers (`khr -predict`): Rig_pred(K) = min{a : some interface at height a with a birth tower of level D has a + D ≥ K}. For (01, 8, 16): Rig = Rig_pred at K = 1..40 at every level and at K = 44, 48, ..., 116 (none / 1 / none / 3 until K = 29 / 7 from K = 30 to K = 116), and at K = 120 the plain value is Rig = 22, exactly as predicted (Rig_pred jumps 7 -> 22 at K = 119); the plain run was stopped by its time cap right after K = 120 (kept set 1.63M nodes, `ctrl/plain_L16.err`, `out/L16/pred.txt`). For (0001, 12, 36) the same comparison on 35 grid levels up to K = 500 (`ctrl/plain_N36.err`, `out/N36/pred.txt`; kept 54,372 at K = 500) is exact at every level (e.g. Rig_plain = Rig_pred = 137 at K = 160, 278 at K = 300, 476 at K = 500), and the 1,219,563 births (full list, not rotation-reduced) all die with max level 107, consistent with the 135,703 rotation classes of the bulk run.
5. **Controls with a known answer.**
   - **N12 at d = 4, L = 12** (real primitive object above 4-periodic heads): IF(4) has 16 interfaces (a0 = 5), 12 towers (up to rotation) of which exactly 1 survives to the cap (level 800, kept 430 nodes) and 11 die at levels ≤ 3. The survivor's birth column equals N12's column 2 (rotated by 8 steps), and `py/control_n12.py` (independent exact recomputation of this tower) verifies that N12's windows (columns 3..62) are in the kept set at every level ≤ 60. So real primitive structure is not filtered out.
   - **p11 at L = 22, d = 11** (known: Theorem U of r12b, p11^2 carries only p11): IF(11) has 1,612 interfaces (a0 = 58), 2,687 towers (rotation classes), all die, maximum level 56. The same for p11 at L = 33 and L = 44 (d = 11): 12,267 and 65,358 tower classes, all die, maximum levels 139 and 236.
   - **Base 9 lattice control** (clock 1100011000 = (11000)^2, the Lean-verified base-9 certificate has a primitive lattice of period 10): IF(5) has 137 interfaces (a0 = 21), 63 tower classes; 62 die (level ≤ 9) and exactly 1 survives to the cap (level 134 at 300 s; kept 2.05M, positive-entropy growth). Its birth column (2,4,5,11,4,9,3,4,9,0) equals, rotated by 5 steps, column 13 of the certificate left end `cert_b9_rec0.json` (B_t, 61 columns), which is exactly its first non-5-periodic column. So the filter keeps precisely the known primitive object here, too.
   - **Clock 01, d = 4, L = 8** (the known T = 8 objects): IF(4) has 5 interfaces (a0 = 2), 1 tower class, it survives to the cap (level 180 at 300 s, kept 1.26M); its birth column is (12,5,13,6,14,8,16,13) = the first non-4-periodic column of the known period-8 lock (the cells (12,5,13,6,14,8,16,13) of OPEN_PROBLEMS / FORMATS §6).
   - **N12 (0001)^6, (0001)^9** are themselves controls relative to ReachDisk (T = 24, 'only N12 twice') and r12b Theorem U (T = 36).
6. **Rotation classes.** The reduction to rotation classes of births (a time rotation by the clock period maps towers to towers with the same death level) was checked on L = 16: the rotation-reduced run gives exactly 1/8 of the towers (8,565 of 68,520) and exactly 1/8 of every level of the death-level histogram.

## 5. Results per word

Verdict column of the raw table below: 'die = all towers dead' means DIES-primitive (every ICH of that period is d0-periodic); 'survive (cap)' towers hit the per-tower caps and are UNDECIDED (they are listed in out/*/ as TSURV lines and in FINAL_results.md if rerun).

| word | T | d0 | IF(d0) (a0) | births distinct / rotation classes | towers run | die | capped (TSURV) | verdict | max death level | widest level (candidate nodes) |
|---|--:|--:|--:|--:|--:|--:|--:|---|--:|--:|
| (01)^8 | 16 | 8 | 22,601 (87) | 68,520 / 8,565 | 68,520 | 68,520 | 0 | DIES-primitive | 526 | 366,339 |
| (01)^12 | 24 | 8 | 22,601 (87) | 462,450 / ~38,600 | 38,546 | 38,544 | 2 | PARTIAL: 2 towers capped | 1272 | 29,725,310 |
| (01)^16 | 32 | 8 | 22,601 (87) | 3,177,064 / ~198,600 | 208,705 | 208,691 | 14 | PARTIAL: 14 towers capped | 797 | 60,330,206 |
| (01)^20 | 40 | 8 | 22,601 (87) | 24,071,865 / ~1.2M | 1,293,285 | 1,293,282 | 3 | PARTIAL: 3 towers capped | 432 | 54,207,380 |
| (0001)^6 = N12^2 | 24 | 12 | 22,657 (70) | 125,090 | 125,090 | 125,090 | 0 | DIES-primitive | 1369 | 6,017,851 |
| (0001)^9 = N12^3 | 36 | 12 | 22,657 (70) | 1,219,563 / 135,703 | 135,703 | 135,703 | 0 | DIES-primitive | 107 | 0 |
| (0001)^12 = N12^4 | 48 | 12 | 22,657 (70) | 12,489,586 / ~1,040,000 | 1,052,357 | 1,052,349 | 8 | PARTIAL: 8 towers capped | 329 | 159,053,940 |
| (0001)^15 = N12^5 | 60 | 12 | 22,657 (70) |  | 9,763,414 | 9,763,412 | 2 | PARTIAL: 2 towers capped | 319 | 107,405,727 |
| root 14: (00100101010101)^4 | 56 | 14 | 337 (15) | 826,032 | 207,280 | 207,279 | 1 | PARTIAL: 1 towers capped | 13 | 72,284,341 |
| root 9: (001010101)^6 | 54 | 9 | 137 (16) | 16,407,243 | 2,735,776 | 2,735,775 | 1 | PARTIAL: 1 towers capped | 226 | 63,480,140 |
| root 11: (00010010111)^5 | 55 | 11 | 1483 (44) | 6,204,780 | 1,240,956 | 1,240,956 | 0 | DIES-primitive | 345 | 52,581,759 |

**(01)^12: capped towers (TSURV; UNDECIDED):**
  - if=703 K=2215 kept=746457 time col_period=24
  - if=7475 K=2213 kept=739618 time col_period=24
**(01)^16: capped towers (TSURV; UNDECIDED):**
  - if=4510 K=1135 kept=635413 time col_period=32
  - if=7760 K=150 kept=2911492 time col_period=16
  - if=11990 K=98 kept=3137220 time col_period=16
  - if=17560 K=153 kept=3016550 time col_period=16
  - if=20680 K=885 kept=764652 time col_period=16
  - if=155 K=93 kept=2975726 time col_period=16
  - if=1893 K=635 kept=1859892 time col_period=16
  - if=1939 K=634 kept=1836712 time col_period=16
  - if=1941 K=141 kept=2499522 time col_period=16
  - if=2119 K=138 kept=2426624 time col_period=16
  - if=7393 K=1180 kept=827895 time col_period=32
  - if=20245 K=820 kept=654166 time col_period=16
  - if=22235 K=544 kept=1373960 time col_period=16
  - if=22391 K=567 kept=1349970 time col_period=16
**(01)^20: capped towers (TSURV; UNDECIDED):**
  - if=7707 K=509 kept=2629830 time col_period=40
  - if=790 K=507 kept=2579931 time col_period=40
  - if=14317 K=507 kept=2579931 time col_period=40
**(0001)^12 = N12^4: capped towers (TSURV; UNDECIDED):**
  - if=3824 K=103 kept=4233534 time col_period=24
  - if=14772 K=119 kept=5987192 time col_period=24
  - if=69 K=95 kept=8349970 time col_period=24
  - if=1961 K=136 kept=3519608 time col_period=24
  - if=9669 K=133 kept=5757674 time col_period=24
  - if=12874 K=75 kept=7070930 time col_period=24
  - if=11751 K=351 kept=1894281 time col_period=48
  - if=13231 K=786 kept=1255600 time col_period=24
**(0001)^15 = N12^5: capped towers (TSURV; UNDECIDED):**
  - if=2259 K=290 kept=4640880 time col_period=60
  - if=2259 K=201 kept=3885438 time col_period=60
**root 14: (00100101010101)^4: capped towers (TSURV; UNDECIDED):**
  - if=49 K=198 kept=3541889 time col_period=56
**root 9: (001010101)^6: capped towers (TSURV; UNDECIDED):**
  - if=61 K=216 kept=821650 time col_period=27

**Pass-2 runs on capped towers (out/pass2/):**
- CAP54a: stopped at the session end without a result (out/pass2/CAP54a.out); UNDECIDED
- CAP56b: stopped at the session end without a result (out/pass2/CAP56b.out); UNDECIDED
- L24_if703: finished; dies at K = 3309 (maxn 29725310, 7837.88 s)
- L24_if7475: stopped at the session end without a result (out/pass2/L24_if7475.out); UNDECIDED (a later main-session run with kmax 400 also ended without a decision)
- N48_if11751: finished; dies at K = 792 (maxn 50036272, 1932.93 s)
- N48_if13231: finished; dies at K = 1265 (maxn 56911574, 2868.49 s)


Raw table (auto-generated from out/*/s*.out, py/collect.py):

| dir | word | shards done | interfaces (a0) | towers run | die | survive (cap) | max death level | widest level | max secs |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| L16 | 01 L=16 | 8 | 22601 (87) | 68520 | 68520 | 0 | 526 | 366339 | 9 |
| L24r | 01 L=24 | 6 | 22601 (87) | 38546 | 38544 | 2 | 1272 | 29725310 | 7205 |
| L32 | 01 L=32 | 2 | 22601 (87) | 208705 | 208691 | 14 | 797 | 60330206 | 12891 |
| L40 | 01 L=40 | 3 | 22601 (87) | 1293285 | 1293282 | 3 | 432 | 54207380 | 3234 |
| N24 | 0001 L=24 | 6 | 22657 (70) | 125090 | 125090 | 0 | 1369 | 6017851 | 610 |
| N36 | 0001 L=36 | 6 | 22657 (70) | 1355266 | 1355266 | 0 | 107 | 2011264 | 69 |
| N48 | 0001 L=48 | 4 | 22657 (70) | 1052357 | 1052349 | 8 | 329 | 159053940 | 4251 |
| N60 | 0001 L=60 | 3 | 22657 (70) | 9763414 | 9763412 | 2 | 319 | 107405727 | 3236 |
| CTRL_N12d4 | 0001 L=12 | 1 | 16 (5) | 12 | 11 | 1 | 3 | 35473 | 0 |
| CTRL_p11 | 00001110001 L=22 | 1 | 1612 (58) | 2687 | 2687 | 0 | 56 | 0 | 0 |
| CTRL_b9 |  | 0 |  () | 0 | 0 | 0 | 0 | 0 | 0 |
| CTRL_01d4 |  | 0 |  () | 0 | 0 | 0 | 0 | 0 | 0 |

Survivors in L24r (2):
   TSURV if=703 K=2215 kept=746457 reason=time maxn=29725310 secs=3601.24 iface=001010010010110001111000|0,4,0,4,0,6,0,12,0
   TSURV if=7475 K=2213 kept=739618 reason=time maxn=29725310 secs=3601.25 iface=101101001110000111110101|0,6,0,12,0,10,0,5

Survivors in L32 (14):
   TSURV if=4510 K=1135 kept=635413 reason=time maxn=18992115 secs=1200.91 iface=00110011001100110011001100110111|0,6,0,10,
   TSURV if=7760 K=150 kept=2911492 reason=time maxn=56259494 secs=1220.87 iface=00100101001010110010010100101011|0,5,0,3,0
   TSURV if=11990 K=98 kept=3137220 reason=time maxn=60330206 secs=1213.93 iface=00101101011110010010110101111001|0,6,0,7,0
   TSURV if=17560 K=153 kept=3016550 reason=time maxn=56259494 secs=1211.91 iface=01010011011010110101001101101011|0,12,0,1
   TSURV if=20680 K=885 kept=764652 reason=time maxn=22936876 secs=1201.06 iface=01101010011110110110101001111011|0,13,0,3,
   TSURV if=155 K=93 kept=2975726 reason=time maxn=60330206 secs=1222.08 iface=00101000011011010010100001101101|0,7,0,2,0,1
   TSURV if=1893 K=635 kept=1859892 reason=time maxn=35278478 secs=1202.12 iface=00111010001110110011101000111011|0,7,0,12,
   TSURV if=1939 K=634 kept=1836712 reason=time maxn=35278478 secs=1205.89 iface=01001100010111000100110001011100|0,13,0,7,
   TSURV if=1941 K=141 kept=2499522 reason=time maxn=50673608 secs=1207.58 iface=00101010101001010010101010100101|0,9,0,5,0
   TSURV if=2119 K=138 kept=2426624 reason=time maxn=50673608 secs=1215.78 iface=01010101011010110101010101101011|0,13,0,16
   TSURV if=7393 K=1180 kept=827895 reason=time maxn=18992115 secs=1202.96 iface=00110010001100110011001100110011|0,8,0,10,
   TSURV if=20245 K=820 kept=654166 reason=time maxn=22936876 secs=1201.49 iface=00100101011000010010010101100001|0,8,0,5,0
   TSURV if=22235 K=544 kept=1373960 reason=time maxn=30675348 secs=1204.23 iface=00100010011001100010001001100110|0,2,0,0,
   TSURV if=22391 K=567 kept=1349970 reason=time maxn=30675348 secs=1203.31 iface=01100111011101100110011101110110|0,15,0,5

Survivors in L40 (3):
   TSURV if=7707 K=509 kept=2629830 reason=time maxn=54207380 secs=1511.04 iface=0001101001001110000111100100101101011110|0
   TSURV if=790 K=507 kept=2579931 reason=time maxn=54207380 secs=1514.84 iface=0001101101001010000111100101101100011110|0,
   TSURV if=14317 K=507 kept=2579931 reason=time maxn=54207380 secs=1512.82 iface=0001101001001110000111100100101101011110|

Survivors in N48 (8):
   TSURV if=3824 K=103 kept=4233534 reason=time maxn=91197948 secs=1206.17 iface=101100101001101100111001101100101001101100
   TSURV if=14772 K=119 kept=5987192 reason=time maxn=108176690 secs=1239.26 iface=0101100001110101100101100101100001110101
   TSURV if=69 K=95 kept=8349970 reason=time maxn=159053940 secs=1251.08 iface=01001011100001011010100001001011100001011010
   TSURV if=1961 K=136 kept=3519608 reason=time maxn=98140016 secs=1215.81 iface=001010110111001110110111001010110111001110
   TSURV if=9669 K=133 kept=5757674 reason=time maxn=106691650 secs=1212.10 iface=10001010100110011010100010001010100110011
   TSURV if=12874 K=75 kept=7070930 reason=time maxn=127559464 secs=1201.70 iface=00111101010000111110010000111101010000111
   TSURV if=11751 K=351 kept=1894281 reason=time maxn=50036272 secs=1201.55 iface=10001100101010001100101010001100101010001
   TSURV if=13231 K=786 kept=1255600 reason=time maxn=47530628 secs=1202.39 iface=00111000110100111001110000111000110100111

Survivors in N60 (2):
   TSURV if=2259 K=290 kept=4640880 reason=time maxn=88785727 secs=1506.68 iface=000110101011000110111010000110101011000110
   TSURV if=2259 K=201 kept=3885438 reason=time maxn=107405727 secs=1500.55 iface=00011010101100011011101100011011101000011

Survivors in CTRL_N12d4 (1):
   TSURV if=2 K=800 kept=430 reason=kmax maxn=35473 secs=0.11 iface=100010001001|0,0,0,6,0,0,0,7,0,0,0,15|211321232123 col=


## 6. What is new relative to r12b / r12e, and what stays UNDECIDED

**New in this round.**
1. *Method.* A correct "primitive-part" filter: Theorem B (births above the saturated interface set IF(d0), PAPER PROOF), its plain form Theorem B′, the reduction to rotation classes of births, and the all-L pre-filter (Lemma AL). r12b/r12e had Theorem K (death of the whole K-head set: impossible for these families) and Theorem U (stabilisation of the whole kept set: only worked for L = 36 and p11-type clocks). Theorem B needs neither.
2. *Full results (COMPUTED + Theorem B; see section 5 for exactly what finished):* clock (01)^8 (T = 16): every infinite closed 16-history is 8-periodic, hence no exterior or uniform band (T = 8 has none, bx saturation and ReachDisk) and every lattice is a repetition of a T = 8 lattice; clock (0001)^6 (T = 24) and (0001)^9 (T = 36): every infinite closed history is 12-periodic, i.e. a second, independent proof of P(6) (ReachDisk) and P(9) (r12b Theorem U), stronger than both because it also covers lattices and all non-accepting histories. (Items in section 5 marked PARTIAL or not run are not claimed.)
3. *Partial results.* For the words listed as PARTIAL in section 5 the method leaves an explicit finite list of unresolved towers (interface index and birth column are in out/*/s*.out TSURV lines): for T = 48 on clock 0001 (N12^4), 1,052,349 of 1,052,357 tower classes die in pass 1 and 8 were capped (7 of the 8 with a birth column of exact period 24); of these 8, the towers if=13231 and if=11751 died in pass 2 at levels 1265 and 792 (out/pass2/N48_if*.out), the other 6 (all with birth columns of exact period 24 and kept sets of 3.5M to 8.3M at levels 75 to 136 at the 20-minute cap) are UNDECIDED (see the pass-2 list in section 5 for the final state); so P(12) is reduced to the explicit list of remaining towers (UNDECIDED, not proved). The same for T = 32 on clock 01 and T = 60 on clock 0001 (N12^5) as listed in section 5.
4. *Structure.* The heavy towers are all, up to rare exceptions, those whose birth column has exact period L/2 (the walks that are "L/2-periodic for a while"); the death levels of rotation classes for T = 24 (D up to 1369 on clock 0001, 1272+ on clock 01) are much larger than for T = 36 (107): period doubling is the expensive case.
5. *Validation.* Plain K-head graphs against towers: the predicted first non-periodic column Rig(K) equals the plain value at every checked level for (01, 8, 16) (K = 1..40 and every 4th level to K = 120, including the jump 7 -> 22 at K = 119) and (0001, 12, 36) (35 levels up to K = 500). Controls with real objects (N12, the base-9 Lean certificate, the period-8 lock) are kept, as the theorem requires; controls with known uniqueness (p11^2) die.

**UNDECIDED (nothing claimed).**
- Every word marked PARTIAL or "not run" in section 5: the listed towers/shards did not finish within the caps.
- The primitive capped census words of r12e §6 (T = 51, 53 (three), 54, 55, 56 and p34): they have no proper divisor period, so Theorem B has nothing to act on; r12e's long K-head runs remain the only tool. The imprimitive capped census words of r12e §6 with roots of length 9, 11, 14 (T = 54, 55, 56): **the root-11 word (00010010111)^5 (T = 55) is now DECIDED: all 1,240,956 tower classes die (max level 345) and the root word itself dies at L = 11 (K = 45), so by Theorem B there is no ICH of period 55 at all: no exterior, band or lattice with this clock** (COMPUTED + Theorem B); the words with roots of length 9 and 14 are reduced to one tower each (their root words also die at their own length, L = 9 at K = 17 and L = 14 at K = 16, so if the last tower dies these words are decided too); the root-27 word (T = 54) has 3,847,408 interfaces and was not attempted.
- All multiples at once (Corollary T analogue): for clock 0001 the all-L test certifies 22,518 of 22,657 interfaces as birth-free or dead for every L, leaving 139 hard interfaces; no statement for all L. For clock 01 the all-L test (node cap 2e7) certifies 21,729 of 22,601 interfaces (15,059 dead, 6,670 birth-free), 872 are capped (`out/allL/g01b.out`).
- Anything about 196, or about a certificate. Every statement here is an exclusion of a primitive object of a given period (or a reduction to an explicit list of towers), no Lychrel certificate is produced.

**Suggested next steps.** (i) Second-level births: the towers with birth column of exact period L/2 could be re-rooted at their first non-L/2-periodic column, using a list of interfaces of L/2-periodic heads (a finite but large list, and the L/2 result: e.g. "all ICH of period 24 are 12-periodic" bounds how long the L/2-periodic part can last, ≤ 1369 columns for clock 0001). (ii) Better pruning of the heavy towers (their kept sets are millions of nodes). (iii) Run the all-L test on clock 01 and use the hard-interface lists to reach larger L (N72, N84, ...) cheaply.


## 7. Reproduction and files (paths relative to ~/p196_run/r13c on the Studio; mirrored to ~/Desktop/p196_studio/r13c/ without binaries and big dumps)

- `src/khr.cpp` (compiled as `bin/khr*`): BFS of IF(d0), birth enumeration, relative towers; modes `-bulk`, `-rot2` (rotation classes), `-allL` (all-L test), `-runfile` (re-run towers from TSURV lines), `-predict`, `-deaths`. `src/khp.cpp`: khxt + plain Rig(K) test. `src/kh3.cpp`: independent C++ tower checker. `py/ifsat.py`, `py/births_check.py`, `py/khr_check.py`, `py/control_n12.py`: independent checks. `py/collect.py`, `py/mk_results.py`, `assemble_final.py`: tables and this file. `watchdog.sh`, `runq.sh`, `master.sh`, `statusloop.sh`, `side*.sh`, `killat.sh`.
- Typical commands: towers `bin/khr_r3 10 G D0 L -bulk -rot2 -kmax K -nodecap N -sec S -batch 256 -shard i n`; full (non-rot) births with deaths/prediction `bin/khr_r3 10 G D0 L -deaths F -predict KK Fpred`; plain Rig `bin/khp 10 -g G -L L -batch 4096 -exactset -prim D0 -primk K1,K2,...`; all-L test `bin/khr_o 10 G D0 D0 -allL -kmax R -nodecap N -shard i n`; second pass on capped towers `bin/khr_r3 10 G D0 L -runfile LIST -sec S -nodecap N -batch 256`.
- Data: `out/{L16,L24r,L32,L40,N24,N36,N48,N60,CAP54a,CAP56b,CAP55a}/s*.out` (per-tower TSURV lines with the capped towers' interfaces), `out/pass2/*.out` (second pass), `out/allL/*` (all-L test, hard interface list `n12_hard.txt`), `out/CTRL*`, `ctrl/plain_*.err`, `out/N36/pred.txt`, `out/L16/pred.txt`, `ctrl/kh3_N36.out`, `ctrl/pycheck_L16.out`; `NOTES.md` (log), `FINAL.md` (this file, regenerated from parts: `FINAL_head.md`, `FINAL_theory.md`, `FINAL_valid.md`, `FINAL_results.md` (from `py/mk_results.py`), `FINAL_rest.md`).
