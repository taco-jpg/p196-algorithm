# r14b: K1 for all periods on the decimal period-8 lattices -- local form, healing, rigidity, band-anchored walls

Run directory `~/p196_run/r14b` (compute machine). Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF / UNDECIDED. **No certificate
was found; no centre was found; nothing here is a claim about 196.** K1 itself stays UNDECIDED. Packaging note (round 14): nothing
in this directory is promoted to a results note; see section 12 for why and for the main-session cross-checks.

## 0. Summary

Setting: exactly r12g/FINAL.md sections 1-3, r13b sections 1-2 (frame c_t = h_t - D, fold map F_K, bottom relaxation R_K, accepting state = bottom cell off-lattice, Cyc_acc(K) = states on closed walks of R_K through an accepting state, all periods; Lemma R2 of r13b: Cyc_acc(K) projects into Cyc_acc(K-1)).

New statements (each with exact scope):
1. **PAPER PROOF (Lemma C, section 2; 200,000 random genuine big-integer tests, 0 mismatches):** for non-9 cells reverse-and-add is a radius-1 cellular automaton on pair words: g=1: P'_x = R_x + R_{x-1} (R = digit sum of P), g=0: P'_x = 2(P_x mod 10) + c_{x-1} + c_{x+1} (c = [P>=10]), 9-cells are carry-transparent; the fold is the reflection of a palindromic line, so a centre is a time-periodic reflection-symmetric defect of this CA between the moving lattice and its mirror.
2. **PAPER PROOF (Lemma H, section 3):** the last off-lattice column of a defect can heal in one step only with offset delta = P - L = +-5 at g=0 (carry from above lattice-correct, exactly one of e^L, r^L >= 5) or delta = +-9 at g=1 (carry out wrong by the same sign, digit error cancels); checked against the local sites of rec0 and p12m9.
3. **COMPUTED + Lemma R2 (section 4): rigidity of accepting walks.** For rec0 orbit 0 and every K >= 12 (computed K = 12..19; larger K by R2): accepting states occur only at 8 of the 80 phases: (t,j,par) = (1,15,1), (2,15,1), (3,15,0), (4,15,0) [offsets -2,-4,-4,-9], (5,0,1), (6,0,1) [+4,+9], (5,8,1), (6,8,1) [-4,-9]: three rigid "last gasp" events of duration 2-4 steps. Their bottom cells are nearly unique (rec0 K=19: prefix counts per depth 1,1,1,4,10,29,45,68,...; event (5,8,1): the same up to depth 10). rec1, rec0 orbit 1 (K=16) and rec2 (K=22, orbits 0,1) show the same picture with their own event lists, tables in results/events/. Reading: in every centre of depth >= 12 (rec0, any period) the deepest front event is one of these three events.
4. **COMPUTED (section 4): fragility.** Forbidding a single off-lattice cell value v kills the closure at small K for every v (rec0 orbit 0: emptiness at K(v) = 11,12,7,7,8,5,4,5,5,7,5,5,3,5,8,7,7,11,10 for v = 0..18, all by level 12; table results/forb_rec0_o0.txt): every accepting closed walk of R_K (K >= K(v)) uses the value v on an off-lattice cell of its bottom K(v) cells at some time; in particular every centre of depth >= 12 (rec0, any period) uses all 19 cell values, and every centre of depth >= 7 has an off-lattice 9-cell at some time.
5. **PAPER PROOF + COMPUTED by r14b (Theorem B, section 5, the two-sided direction made concrete; the computed part is NOT confirmed by the main-session code, section 12):** the top-anchored relaxation anchored at an EXACT periodic band B (window directly below B, free below) is a finite computation, and whenever its accepting closure dies at some K0, no maximal band region B of a time-periodic solution can have anything but B below it. For the uniform bands 0, 18, 6/12 and the m=4 bands (1,1,17,17), (1,7,17,11), (0,9,18,9), (5,5,13,13), (6,9,12,9) (all exact m|4 rows with 8-step return except one) the closure dies at K0 <= 3 (two independent codes where checked, big-integer selftests); hence **no centre (any period, any depth, any exterior) has an inner band region of these types**. The bands (1,11,17,7) and the uniform 6-cycle (2,4,8,16,14,10) are "live" (closure keeps growing, 1.8e6 states at K=9), UNDECIDED. (Bands with exact centres exist; the point of Theorem B is that they cannot sit above anything else.)
6. **Two-sided method (section 6):** the exact meet-in-the-middle at a cut column is equivalent to F_{K+k} (no gain per se); the fold-anchored sets are soft (TopCyc(k) projected to its top d cells is all of TopCyc(d) up to 5 %) while the lattice-anchored sets are rigid at the bottom but near-critical in height; the missing piece is a uniform (in K) statement about the middle; no such statement was found. HEURISTIC (not a result): the expected number of exact periodic orbits of period T is about exp(-0.41 T), so no centre is expected unless a structural mechanism exists.

Remaining UNDECIDED: K1 (centres of period >= 160 / 384, depth >= 24 / 28), K2 (a general wall-speed bound), walls to the live bands.

## 1. Notation

Pair word P_x (0..18), n digits, h = ceil(n/2), clock g, carries a_{x+1} = [P_x + a_x >= 10], b_{x-1} = [P_x + b_x >= 10] (b into the mirror of column x), e_x = (P_x + a_x) mod 10, r_x = (P_x + b_x) mod 10, new word P'_x = e_x + r_{x-g} (r12g section 1). c_x = [P_x >= 10], d_x = P_x mod 10, R_x = c_x + d_x (digit sum). Lattice L(t,x) (rec0, rec1: m=20; rec2: m=48), UP = lattice a, DN = lattice b. R_K, F_K as in r12g section 2, phases (t,j,par).

## 2. Lemma C (local form) -- PAPER PROOF

For every cell: if P_x != 9 then [P_x + a_x >= 10] = c_x and [P_x + b_x >= 10] = c_x whatever the incoming carry is (P_x <= 8 gives P_x + carry <= 9; P_x >= 10 gives >= 10); if P_x = 9 the outgoing carry equals the incoming one. Hence a_{x+1} = c_x and b_{x-1} = c_x at non-9 cells, a_{x+1} = a_x, b_{x-1} = b_x at 9-cells; carries are the c-bits of the nearest non-9 cell (below for a, above for b). Also d_x <= 8 at non-9 cells, so d_x + carry <= 9 does not wrap.
- g = 1, P_x, P_{x-1} != 9: e_x + r_{x-1} = (d_x + a_x) + (d_{x-1} + b_{x-1}) = d_x + c_{x-1} + d_{x-1} + c_x = R_x + R_{x-1} (using a_x = c_{x-1}, b_{x-1} = c_x).
- g = 0, P_x != 9: e_x + r_x = (d_x + a_x) + (d_x + b_x) = 2 d_x + a_x + b_x, and a_x = c_{x-1} (if P_{x-1} != 9), b_x = c_{x+1} (if P_{x+1} != 9), giving 2 d_x + c_{x-1} + c_{x+1}.
- g = 0, P_x = 9: e_x + r_x = (9 + a_x) mod 10 + (9 + b_x) mod 10 = 18 - 9(a_x + b_x) (a 9-cell stays 9 iff a_x != b_x).
- Fold: on the unfolded palindromic line P_{n-1-x} = P_x, the b-carries are the a-carries of the mirror positions (b_x = a_{n-1-x}), so every step above is the same local rule applied to the full palindromic line; the top rule of r12g (Din, new middle cell 2 r_{h-1}) is the local rule at the reflection centre (centre site at odd n, centre bond at even n).
Verified: `src/catest.py` (200,000 random N of 4..40 digits, genuine N + rev N): the full new pair word equals the local rule (with 9-transparency) in all 200,000 cases; the R-form on non-9 neighbourhoods: 0 mismatches. QED

Consequence (not used for results): a centre is a time-periodic, reflection-symmetric defect between the lattice L moving outward at speed 1/4 per step (relative to the reflection point) and its mirror. Writing Q = odd-time row, P''_x = 2 (Q_x mod 10) + c(Q_{x-1}) + c(Q_{x+1}), R''_x = digit sum, Q_x = R_x + R_{x-1}: mod 9 the two-step map is R''_x = 2(R_x + R_{x-1}) + (discrete Laplacian of the carries), which is the known linear mod-9 charge.

## 3. Lemma H (healing) -- PAPER PROOF

Let at time t all cells below x be on-lattice (P_y = L(t,y), y < x), P_x(t) != L(t,x), and let cell x and all cells below be on-lattice at t+1. Put P = P_x(t), L = L(t,x), delta = P - L, alpha = UP (the common ascending carry into x), b = b_x(t), b^ = DN_x; b' = [P + b >= 10] (carry out of x downwards), b^' = DN_{x-1} = [L + b^ >= 10]. Put e = (P+alpha) mod 10, ê = (L+alpha) mod 10, r = (P+b) mod 10, r^ = (L+b^) mod 10.

Case g_t = 0. Then P' = e + r and L' = ê + r^. Mod 2: e + r = 2P + alpha + b = alpha + b, so P' = L' forces b = b^. Then e - ê and r - r^ are both congruent to delta mod 10 and sum to 0, so 2(e - ê) = 0 mod 10, i.e. e - ê in {0,+-5}. e = ê gives delta = 0 mod 10; delta != 0 gives delta = +-10; since the cells below stay on-lattice the carry out of x must equal b^' (at g=0, cell x-1 uses r_{x-1} = (L_{x-1} + b_{x-1}) mod 10, injective in b_{x-1}), but P = L+10 >= 10 has carry 1 while L + b^ <= 9 has carry 0, and P = L-10 <= 8 has carry 0 while L + b^ >= 10 has carry 1: contradiction. So e - ê = +-5 and delta is 5 mod 10; delta = +-15 is impossible (P = L+15 >= 15 has carry out 1, L + b^ <= 3+1 has carry out 0; P = L-15 <= 3 has carry 0, L + b^ >= 15 has carry 1). So delta = +-5, b = b^, and (e - ê, r - r^) = (+5,-5) or (-5,+5): exactly one of ê, r^ is >= 5, and [P + b >= 10] = [L + b >= 10].

Case g_t = 1. Then P' = e + r_{x-1}, r_{x-1} = (L_{x-1} + b') mod 10 and L' = ê + r^_{x-1}, r^_{x-1} = (L_{x-1} + b^') mod 10. Let beta' = b' - b^' (in {-1,0,1}). Then e - ê is congruent to delta and r_{x-1} - r^_{x-1} is congruent to beta' mod 10 and they sum to 0: delta = -beta' mod 10.
- beta' = 0 gives delta = +-10, excluded by the carry-out comparison as above (P = L+10 has carry out 1 but b^' = 0, P = L-10 has carry out 0 but b^' = 1).
- beta' = +1 (carry out of x wrong by +1): delta in {-1, +9, -11}; delta = -1: carry out 1 forces L + b - 1 >= 10... precisely L + b >= 11, so L >= 10, then b^' = [L + b^ >= 10] = 1, contradiction with b^' = 0; delta = -11: P <= 7, no carry, contradiction; delta = +9 remains (requires L + b >= 1 and L + b^ <= 9).
- beta' = -1: symmetric: delta = -9 only (requires L + b^ >= 10, and P + b <= 9, with P = L - 9).
So g_t = 1 healing has delta = +-9 and carry out of x wrong by the same sign, and then necessarily (e, r_{x-1}) differ from (ê, r^_{x-1}) by (-1,+1) (or the wrap pair (+9,-9)) for delta = +9 and by (+1,-1) (or (-9,+9)) for delta = -9, and L_{x-1} != 9 unless the error is absorbed (the wrong carry must not propagate through a 9-cell, otherwise cell x-1 changes). QED

Checked: the site table of rec0 computed directly from the lattice (72 of 160 (t,j) pairs, all g=1 sites have delta = +-9, g=0 sites have delta = +-5; g=0 sites are exactly (1,2),(3,7),(5,12),(7,17)) agrees with the healing events recorded in the closure at K=12 (the closure's healing events at K=12 are overwhelmingly (>99.9 % of the counts) at the Phi-orbits of (0,0),(0,4),(0,5),(0,13),(0,16),(1,2); `src/heal.py`).

## 4. Rigidity of accepting closed walks (COMPUTED + Lemma R2 of r13b)

Computation: `bin/mc14wd runscc` (the unchanged mc14w closure of the main session plus a dump of the level sets; no change to the rule) on rec0, rec1, rec2 (rec0 o0 K<=19 agreeing with r12g's |Cyc(K)| = 9140287, 19389807, 40126496, 80883639, 160733468 for K=15..19, accepting 416237, 778743, 1564911, 3149706, 5943487; rec2 o0/o1 K<=22 agreeing with r12g's lists). Analysis `bin/acc_prefix` (accepting states per phase and number of distinct bottom-d prefixes). Base-9 control b9r0: the closure contains the Lean-verified centres (exact orbits at K=1,3,5,...; also with FORB=8).

**rec0 orbit 0 (K=19; the same phases for every K=12..19):**
| phase (t,j,par) | event | offset of bottom cell | accepted states K=19 | distinct bottom prefixes depth 1.. |
|---|---|---|---|---|
| (1,15,1) | C | -2 | 939,039 | 1 1 1 4 10 29 45 68 116 256 565 1132 |
| (2,15,1) | C | -4 | 1,184,747 | 1 1 1 4 11 33 46 69 124 287 608 1229 |
| (3,15,0) | C | -4 | 466,204 | 1 1 1 3 6 18 32 48 82 188 390 802 |
| (4,15,0) | C | -9 | 571,101 | 1 1 1 3 6 22 33 48 92 204 426 858 |
| (5,0,1) | A | +4 | 1,227,394 | 1 1 1 3 6 18 33 52 95 234 532 1211 |
| (6,0,1) | A | +9 | 1,553,229 | 1 1 1 3 6 22 35 52 106 261 587 1333 |
| (5,8,1) | B | -4 | 805 | 1 1 1 1 1 1 1 1 1 1 2 3 |
| (6,8,1) | B | -9 | 968 | 1 1 1 1 1 1 1 1 1 1 2 3 |

Accepted phases K: 12 at K=8,10; exactly these 8 for K=12..19 (for every K in 12..19 by direct computation, all K >= 19 by R2). The bottom cell (and in fact the first 3 cells) of an accepting state is unique per phase: (6,6,8) at (1,15,1), (7,12,8) at (5,0,1), (13,6,4,6,13,9,9,9,2,9) at (5,8,1) (the 3 sequence of 9-cells is a carry wire), etc. Event B is the rarest (it dies out of the deepest T=80 walks, r13b). Consequence (COMPUTED + r13b Lemma R1): in any centre of rec0, orbit 0 frame class, of exact depth D >= 12, of any period, the deepest front cell is off-lattice only in these windows of the lap; the other 72 phases have the deepest cell on-lattice. rec0 orbit 1 (K=16) and rec1 orbit 0 (K=16) have the same structure with shifted labels (results/events/rec0_o1_K16.txt, rec1_o0_K16.txt: identical multiset of accepted counts as rec0 o0 under the known shift). rec2 (results/events/rec2_o0_K22.txt, rec2_o1_K22.txt): orbit 0 events at (t,j,par) phases (1..4,17), (1..2,39), (5,6,44), (1..4,47) with bottom cells unique to depth 7 or more (prefix counts at depth 10 between 1 and 11); orbit 1 similar.

**Fragility (COMPUTED, `bin/mc14wy`, FORB=v rejects any off-lattice cell equal to v):** the closure dies at K(v) for every single value v (results/forb_rec0_o0.txt; rec2 partial table results/forb_rec2_o0.txt). Reading: all 19 cell values are needed, and the walks are held together by rigid special configurations; there is no redundancy. In particular FORB=9: every centre of depth >= 7 (rec0, any period) has an off-lattice 9-cell in its bottom 7 cells at some time (9-cells are the only long-range carry transport; the deep rigid walks use 9-wires, e.g. the event B prefix above).

## 5. Band-anchored top relaxation (the two-sided direction, made concrete)

**Definition (exact band above).** An exact band B of spatial period m and time period P on clock g is a table B[t][j] (t in Z/P, j in Z/m), not all (b-1), that is a solution of the pair-word dynamics with its own periodic carries UP_B, DN_B (rows returning after P steps; for clock 10 all rows with spatial period m | 4 and 8-step return were enumerated by brute force over all 19^m rows, src/selfmirror check: m=1: 0, 6, 12, 18 (6 and 12 are the two phases of the 2-cycle), m=4 (up to rotation, besides the uniform ones): (0,9,18,9), (1,1,17,17), (1,7,17,11), (1,11,17,7), (5,5,13,13), (6,9,12,9); additionally the uniform 6-cycle (2,4,8,16,14,10) of time period 6, because the uniform-band update is k -> 2*ds(k) independently of g).

**The relaxation R^B_K (window directly below B).** The frame moves with h as before (e_{t+1} = e_t + dh_t). State: phase (t, je, par) (je = band column directly above the window, je -> je + dh), window = the K cells [e_t - K, e_t). Free inputs: a_in in {0,1} (ascending carry into the window bottom) at every step, r_in in 0..9 at non-shift g = 1 steps (r-digit of the cell below the window). Exact inputs from the band: Din = [B[t][je] + DN_B[t][je] >= 10]. Constraints that the band stays exact: writing EB = (B[t][je] + a_K) mod 10 with a_K the carry out of the window top, RB = (B[t][je] + DN_B[t][je]) mod 10: (g=0) EB + RB = B[t+1][je]; (g=1, no shift) EB + r_{K-1} = B[t+1][je]; (shift) the old band cell becomes the new window top with value EB + r_{K-1}, the band cell above stays exact automatically if B[t][je] != 9 or a_K = UP_B[t][je]; if B[t][je] = 9 we require a_K = UP_B[t][je] (carry transparency would break the band above). Window update: e, r from the two carry chains; new cells e_i + r_{i-g} with r_in at the bottom for g=1 no shift; at shift steps the window shifts up by one, bottom cell leaves. Accepting: window top cell != B[t][je-1] (the value the band would have at that cell).

**Lemma B1 (soundness).** Let a reverse-and-add orbit with overflow g_t = clock satisfy, for all t in a time interval, that the at least m+1 cells directly above a window (moving with the frame) are exactly the band (carries from the band periodic, B[t] values, within the band). Then each step of the window is an edge of R^B_K with a_in, r_in the genuine carry and r-digit from below.
*Proof.* By Lemma C the carry entering the window top from above is determined by the first non-9 band cell above, which is within the band (m+1 cells suffice since B is not all 9); it equals Din. The window update formulas are the definition of P' restricted to the window with carries a from below (a_in is the genuine carry into the window bottom, free in R^B_K) and b from above; the band-exactness constraints are the genuine values of the band cell above the window at t+1 (case analysis exactly as above; at a shift step the band cell above the window becomes the window top cell, and its new value is e + r_{top}; the cell above that one stays on the band by the band's own solution, because the ascending carry into it is UP_B unless B[t][je] = 9, in which case the carry is required to equal UP_B by the constraint). QED.
Validated: `src/bandclo2.py selftest`: 150,000 genuine big-integer steps per band ((1,1,17,17), (0,9,18,9), (5,5,13,13)), band region of width >= 4, g = clock, band exact at both times: the genuine new window is in the successor set in all cases.

**Theorem B (PAPER PROOF given a computed emptiness).** Let B be an exact band and K0 >= 1 such that Cyc^B_acc(K0), the set of states of R^B_{K0} lying on a closed walk through an accepting state, is empty. Let O be a centre in the sense of r12g (a periodic orbit of the window map, time-periodic in the frame moving with the fold, over an exterior/lattice L below the frame) such that the cells [h_t - b, h_t) (b >= m+1) coincide with the band B for all t (band phases moving with the frame). Then every cell below is also on the band pattern, which is impossible when the cells below the frame are a lattice L whose rows differ from B: a maximal band region cannot have anything else below it. In particular no centre of a lattice L != B (any period, any depth, any exterior) has an inner band region of type B (of width >= m+1).
*Proof.* Let b be maximal with the band property (the lower edge column e_t = h_t - b maximal region); if the band region does not reach column 0, the cell e_t - 1 is off the band pattern at some time of the period (maximality). The cells below the edge exist; the window of K0 cells directly below the edge (K0 <= the number of cells below, as long as column index >= 1; if fewer cells exist below the claim is trivial) evolves by edges of R^B_{K0} (Lemma B1), and periodicity gives a closed walk through an accepting state: contradiction with Cyc^B_acc(K0) = {}. Hence b reaches column 0. QED

**Computations (results/band2/, results/band/, code src/bandclo2.py, bandclo.py; independent code src/bandind.py (CA form, explicit full enumeration of all 19^K windows, K <= 3)).** All phase orbits (t,je,par) computed for every band (the uniform 6-cycle: 2 offset classes, par 0/1 each).

| band (row at t=0) | spatial m | time period | orbits | smallest K with Cyc^B_acc(K) empty (per orbit) | status |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 2 | 1,1 | dead |
| 18 | 1 | 1 | 2 | 1,1 | dead |
| 6 / 12 (2-cycle) | 1 | 2 | 2 x 2 | 1,1,1,1 | dead |
| (1,1,17,17) | 4 | 8 | 4 | 3,3,2,1 | dead (independent bandind agrees on all counts K=1..3) |
| (1,7,17,11) | 4 | 8 | 4 | 2,2,2,2 | dead |
| (0,9,18,9) | 4 | 8 | 4 | 1,3,3,2 (bandclo2 and bandind agree on all counts K=1..3) | dead |
| (5,5,13,13) | 4 | 8 | 4 | 3,3,2,1 (bandclo2; bandind agrees: K=2 counts 48,54,0,0, K=3 all 0) | dead |
| (6,9,12,9) | 4 | 8 | 4 | 1,3,3,2 (bandclo2; bandind agrees: K=2 counts 0,48,54,0, K=3 all 0) | dead |
| (1,11,17,7) | 4 | 8 | 4 | not empty up to K=9 at least (orbit 0: 1,802,838 states at K=9, x3.6 per level) | live, UNDECIDED |
| (2,4,8,16,14,10) uniform 6-cycle | 1 | 6 | 2 x 2 | not empty up to K=9 at least (1,798,578 states at K=9, x3.3 per level) | live, UNDECIDED |

(For rec0 as the band above, i.e. "what can sit below a rec0 lattice", the closure grows like the bottom relaxation of a lattice: 143, 275, 540, 1128, 2275, 4931, 12930 at K = 1..7, so lattices are live.) Consequence for K1: every centre of rec0, rec1, rec2 (or any exterior/lattice), of any period and depth, has no inner region consisting of a dead band of width >= m + 1 (Theorem B). This excludes the "simplest conceivable" centres (rec0 + wall + uniform band 0, 18, or the 2-cycle; rec0 + wall + band (1,1,17,17) etc.), for all periods. The live bands remain.

Control caveats: no positive control exists for a genuine wall (none known); the soundness of R^B_K is by proof + the big-integer selftest; the closure code is validated by the independent bandind.py and by the agreement of bandclo.py/bandclo2.py on the uniform bands.

## 6. The two-sided method: what is needed, and why it does not close

Let the top window of k cells (exact fold, free inputs from below: a_in, r_in; TopCyc(k) of r12g) and the bottom window of K cells (R_K) share a cut. A centre of depth K + k is exactly a closed walk in the product of R_K and the top relaxation T_k with matched interface letters (Din, topv against b_out, e_out; a_out, r_out against a_in, r_in): this product is deterministic in the exact case (it IS F_{K+k}), so "meet in the middle" computes nothing new unless it is uniform in K. What a uniform statement needs: either (1) a language L_bot containing the interface words at height K of every R_K (all K) that is disjoint from the top language, or (2) a monovariant/charge crossing the cut. Findings:
- The top sets are soft: projecting TopCyc(k) to its top d cells gives counts 232, 3896, 58192, 772576, 9708344, 123287536 (k = 6, d = 1..6) versus |TopCyc(d)| = 232, 3896, 61464, 819952, 10371912, 123287536: the fold-anchored set of the top d cells does not shrink with depth (no rigidity from the top, exactly as expected from "bands with exact centres exist"). COMPUTED (r12g data/top, src topproj).
- The bottom sets are rigid at the bottom (section 4) but the tower of level sets is not a regular language of bounded width: the minimal DFA of Cyc(K) has per-depth widths growing like the set itself (src dawg.cpp; K=14: 655,703 nodes against 4.27M states; bottom-to-top widths 80, 88, 122, 186, 322, 682, 1533, 3427, 7697, 17964, 43448, 109829, 269131, 201114), so no finite-state description in K has been found.
- Linear charges mod 9 and 11 (the only ones of the form z^x with z = 10, 1/10 mod p; PAPER remark: they are exactly the kernel of (z-10)(1-10z)) can be carried across the cut as an extra state component, but both relaxations have ample freedom, so they give no obstruction (r13b section 8 and r12a).
- The exact closure at the cut with the lattice replaced by the mirror lattice is trivial (it is R_K again by reflection); the only case in which the top side is rigid is when the top side is an exact band: Theorem B above.
Reduction statement: K1 for rec0/rec1 is equivalent to "for every D >= 24 the exact fold map F_D has no periodic orbit through one of the rigid accepting events of section 4 (with its bottom prefix)", for rec2 the same with D >= 28 (with its events). Everything beyond that is UNDECIDED.

**Heuristic (NOT a result).** Per frame shift the fold-exact condition determines one new top cell (factor 1/10) and the free carry bits at g=0 steps (2 per 4 steps), so P(fold-exact) ~ exp(-T(ln10/4 + ln2/2)) = exp(-0.92 T) for a walk of length T, while the number of closed T-walks of R_K is about exp(0.514 T) (r13b W(K,80) saturates at 6.9e17 = e^{41.1}, K >= 12): expected number of exact orbits ~ exp(-0.41 T), summable over T >= 80 and over depths (at T=80 of order 1e-14 per depth). This is why none are expected unless a special mechanism exists; it is not a proof.

**Sideways structure (observation, not used for any result):** a closed T-walk of R_K extends to level K+1 by choosing, independently for each frame-shift segment of 4 steps, a new-cell history: start value v in 0..9 (+ the carried r-digit), 2 free carry bits at the two g=0 steps, the constraint that its digit at the end of the segment is the prescribed one (1/10) and that its carry-out equals the prescribed bit at the two g=0 steps (1/4): mean number of fillings per segment 40/40 = 1, the product over T/4 segments: critical in mean, with many walks extinct at the next level. (Derivation only; not used.)

## 7. Why the all-period closure dies on p11/p12 (d=11, d=12) but not on clock 10 (observations)

- For the clock-1000 lattice W0 (p12m9) the level sets at K=1..5 are of the same size as rec0's (K=5: 3546 vs 3476), and level 6 is abruptly empty of accepting states: at K=6 the 6194 accepting candidates split into 952 with an infinite future and 575 with an infinite past, with no overlap (disjoint), whereas for rec0 the corresponding numbers at K=6 are 8360 candidates, 1645, 2892, overlap 731 (these are Cyc_acc(6)). COMPUTED (`src/w0k6.py p12m9 5 p12_o0`; candidates and core trim from the K=5 level files). So the death at K=6 is a rigid incompatibility of the possible pasts and futures of an off-lattice bottom cell, not a slow decay. I did not find a one-line reason beyond this. The rec0 family is on the other side of this threshold for all K <= 19 (growth factor 2.0-2.2 per level, sideways near-critical: each new column has on average about one closed-time extension, section 6).
- Every value of the cell is needed for the closure (section 4), so the sets are held by a rigid web of special configurations; nothing like a "free" variable (e.g. all-9-wire choice) is available on clock 10 at small depth, unlike the p11/p12 9-wires which die completely instead.

## 8. What failed / negative results (scope stated)

- A local front-speed lemma (K2): impossible by r13b (fronts advance at 1/4 in R_K up to K=44 at T=80); the healing lemma and the event tables quantify but do not bound the mean speed.
- Regular-language (minimal automaton) description of Cyc(K) in K: no bounded width (section 6).
- T=160: unchanged (E_acc(K,160) = Cyc(K) for small K; no new computation attempted here).
- Forward iteration beyond the r12g depths: not attempted (cost x2 per level; budget 6 threads, 30 GB; finite-horizon, not progress).
- Nonlinear conservation laws: not found (no systematic search completed); the fragility result suggests none of small range.
- No centre, no candidate centre, no wall to a live band was found (no such search was finished; none of the computations here produces a centre).

## 9. UNDECIDED

K1 (centres of period >= 160 and depth >= 24 for rec0/rec1, period >= 384 and depth >= 28 for rec2; the SCC lattices r14a treats separately); K2 (wall speed); walls below the live bands (1,11,17,7) and the uniform 6-cycle; whether Cyc_acc(K) dies at some K for rec0 or rec2 (all-period closure; it has not died up to K = 19 / 22).

## 10. Files (~/p196_run/r14b)

- src/: mc14wd.cpp (mc14w of main session + level dump), mc14wy.cpp (+ forbidden value), acc_prefix.cpp, dawg.cpp, topproj.cpp, r14.py (reference rule, own code), bandclo.py, bandclo2.py (band-anchored closure + selftest), bandind.py (independent check), scc_tools.py.
- data/: rec0_o0/K*.bin (K<=19 level sets), rec2_o0, rec2_o1, rec0_o1, rec1_o0 (dumps), p12_o0. results/: events/ (accepting event tables), forb_rec0_o0.txt, forb_rec2_o0.txt, band/, band2/ (closure outputs). logs/.
- Reproduce: `bin/mc14wd runscc <lat> <orbit> 19 4 0` (DUMPDIR set), `bin/acc_prefix <lat> data/rec0_o0/K19.bin 12`; `python3 src/bandclo2.py 1,1,17,17 14`; selftests: `python3 src/bandclo2.py 1,1,17,17 500000 selftest`; independent: `python3 src/bandind.py 1,1,17,17 3`.

## 11. Run status

All runs of this route finished on 2026-11-08 (22:28 UTC). On the live bands the closure simply did not die within the time
limit: (1,11,17,7) nonempty up to K = 9 (1,802,838 states at orbit 0, K = 9; K = 10 not completed), uniform 6-cycle nonempty up to
K = 9 (1,798,578 states). Nothing is claimed beyond this. The level-set dumps (`data/`, 10 GB) are not shipped.

## 12. Main-session checks and packaging decision (round 14)

Third code `mainchk/` (main session; `mainchk/chk14b.sh` -> `mainchk/chk14b.out`):
- **Accepting phases of rec0 orbit 0 (section 4):** `mc14p.cpp` (= mc14w + a phase histogram) finds exactly the 8 phases
  (5,8,1), (6,8,1), (1,15,1), (2,15,1), (3,15,0), (4,15,0), (5,0,1), (6,0,1) at every K = 12..17, and |Cyc_acc(16)| = 19,389,807,
  accepting 778,743 (= r12g). Agrees.
- **Fragility (section 4), plain Python `pyforb.py`:** K(v) for v = 12, 6, 5, 7, 8, 10, 11, 13, 9 = 3, 4, 5, 5, 5, 5, 5, 5, 7, as in
  `results/forb_rec0_o0.txt`. Agrees.
- **Band-anchored closure (section 5), `bandchk.py` (written from the definition, full enumeration, K <= 3): DISAGREES.** Per-orbit
  death levels: (1,1,17,17) 1,3,2,1 (r14b: 3,3,2,1); (0,9,18,9) 1,1,3,2 (r14b: 1,3,3,2); (5,5,13,13) 1,3,2,1 (r14b: 3,3,2,1, K = 1
  counts 0/32/20/0 against r14b's 24/32/20/0); (6,9,12,9) 1,1,3,2 (r14b: 1,3,3,2); (1,7,17,11) 1,1,1,1 (r14b: 2,2,2,2); and
  (1,11,17,7) dead at K = 1 in all four orbits (r14b: live, 48 states per orbit at K = 1). The two codes of r14b (`bandclo2.py`,
  `bandind.py`) agree with each other. One visible difference: `bandchk.py` takes the descending carry into the band cell above the
  window as `DN[t][j+1]` (its comment: DN[t][c] is the carry out of c); the cause was not established. The big-integer soundness selftest of `bandclo2.py` quoted in section 5 has no
  shipped log. Theorem B's computed part is therefore UNDECIDED until the conventions are reconciled and a selftest log exists.

Decision (AGENTS.md section 4): no results note from this route.
- Lemma C (local CA form, 9-cells carry-transparent) restates the known local form of the step (e.g. `reports/AgentW30OddFiveCarrier.md`
  "piecewise-affine cellular automaton on 9-free interior words"); not new.
- Lemma H (healing offsets +-5 at g = 0, +-9 at g = 1) is exactly stated and proved (section 3), but it is a one-step local fact
  that does not bound the front speed (K2) or decide K1 (section 8 says so); kept here as a lemma for later use.
- Rigidity and fragility (section 4) are finite-K computations (agreeing with the main-session code) that sharpen the K1 reduction
  but decide nothing for all depths.
- Theorem B (band-anchored walls): computed part disputed, see above.

Reproduction (from `~/p196_run/r14b`): `bin/mc14wd runscc <lat> <orbit> 19 4 0` (env DUMPDIR), `bin/acc_prefix <lat>
data/rec0_o0/K19.bin 12`, `bin/mc14wy` (env FORB=v, otherwise as mc14wd), `python3 src/bandclo2.py 1,1,17,17 14`, `python3 src/bandclo2.py
1,1,17,17 500000 selftest`, `python3 src/bandind.py 1,1,17,17 3`, `python3 src/catest.py`, `python3 src/heal.py`; main-session
checks: `bash mainchk/chk14b.sh` (expects the round-13 lattice `rec0.txt`, in `../r14a_lattices/lat/`). C++ built with
`clang++ -O3 -std=c++17 -pthread`.
