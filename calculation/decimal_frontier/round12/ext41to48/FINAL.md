# Round 12, agent r12b: decimal exteriors and uniform bands at periods 41–48, the round-11 capped words, and an exact K-head filter

Run on the Studio in ~/p196_run/r12b; paths below are relative to this directory.
Labels: **PAPER PROOF** (argument written out here), **COMPUTED** (exact program output, reproducible with the files listed),
**UNDECIDED** (capped; nothing claimed). Nothing here is LEAN-VERIFIED. No claim about 196.

## 0. Results

1. **Periods 41–48, complete except a short list (COMPUTED + PAPER PROOF).** Every F1 necklace of length T = 41..48 was run:
   169,128,231 words (every count equals `data/f1_b10_p33_60.csv`; primitive and imprimitive). For all of them except the
   UNDECIDED words of §9 there is **no 9-wire exterior and no uniform-band template** of combined period T, of any width / left-end
   height, any stream, any band ({6,12}, the 6-cycle, {0}, {18}, any phase). The word p11^4 (T = 44) carries only the p11 stream.
   Decided: 169,128,227 of 169,128,231 words; UNDECIDED: 4. T = 41, 43, 47 are now covered. 0 accepted streams other than
   repetitions of p11; 0 NEW streams.
2. **Round-11 capped words.** Of the 112 wire words and 1,475 band words left open in round 11, all are now decided except the
   words listed in §5/§9. p11^3 (p33) and p11^4 (p44) carry only the p11 stream; (0001)^9 = N12^3 (p36) carries only N12.
   Still UNDECIDED: 4 words, each as wire and as band: one primitive p34 word, (01)^20, (p21)^2 and N12^4 = (0001)^12 (§5).
3. **New filter (PAPER PROOF).** khx: the K-head graph G_K grown one position at a time, pruned by trim, the SCC period filter
   "period | L" and an **exact closed-walk test** (always on with `-batch`). Its DIES verdict excludes **both** 9-wire exteriors and
   uniform-band templates (Theorem K). Round 11 used the K-head filter for wires only and without the exact test.
4. **Uniqueness by stabilization (PAPER PROOF + COMPUTED, Theorem U).** If the kept graph becomes periodic in K and its
   (9,9)-topped part carries no closed walk except the known stream, every exterior is the known stream. Proved here for clocks
   p11^m (m = 1..5: B-level uniqueness, including p22, which was UNDECIDED in EXTERIOR.md §3b) and **P(9)**: every
   exterior with clock (0001)^9 is N12 repeated (the "missing lemma" of three_divides_r for k = 3). Re-proves P(3).
5. **Transfer to all multiples (PAPER PROOF + COMPUTED, Corollary T).** For 6,700 of the 6,722 primitive F1 roots h with
   |h| ≤ 24 the K-head graph becomes acyclic: no clock h^m, for any m ≥ 1, carries an exterior or a band template.
6. **Bonus, p ≤ 32.** 50 of the 54 UNDECIDED words of EXTERIOR.md §4 die, including the p21 word 001001010101001010101
   (K = 112, confirmed by the independent implementation). Left: (01)^8, (01)^12, (01)^16, (0001)^6 (= N12^2, settled by ReachDisk).

## 1. Method and pipeline

**khx** (`src/khx.cpp`). For a pattern g (length P) and a set Ls of lengths L (multiples of P; default L = P) it builds the K-head
graph G_K(g) one spatial position at a time. A level-K node is a (kept level-(K−1) node, top digit v) pair; its edge for bit h uses the
parent's edge for bit h' = ⌊(v + h)/b⌋ (projection lemma A3) and the new top digit
y_{K−1} = (v + L_{K−1}) mod b + (g_t ? (x_{K−2} + h') mod b : (v + h) mod b). Each level is pruned by (i) trim, (ii) the SCC filter
"period | some L" (round 11's khead_len filter), (iii) the exact test: from the smallest phase layer, bitset propagation over L/P
laps finds the sources that return to themselves after exactly L steps; with none, the word DIES; otherwise only nodes within one lap
of these sources (both directions) are kept. Without `-batch` the exact test is skipped when the smallest layer has more than 4,096
nodes (the original version written at the start of r12b); with `-batch C` it always runs, sources in batches of C. Options added in
r12b: strengthened `-check`, `-dump FILE`, `-batch C`, `-periods`, `-allm`. Default behaviour is unchanged (verified on 150,000 census
words and on all controls: identical output).

**Pipeline.**
1. `fc_enum 10 p p -list lists/p{p}`, p = 41..48: all F1 necklaces (primitive and imprimitive); counts equal the CSV exactly.
2. Pass 1 (`run_census1.sh`): khx -kmax 400 -nodecap 2e7 -sec 4 on all 169,128,231 words, 16 workers, about 10 minutes.
   66 words survive (§4).
3. Pass 2 (`run_khx_list.sh`): khx -nodecap 1e8 -sec 1800 on the survivors (11 more die). Round-11 open lists were already run the same
   way before the resume (`out/deep/R_*`: 1,502 of 1,532 die).
4. Pass 3 (`run_khxb_list.sh`, khx3 = khx with `-batch 4096`): all 83 remaining words (66 census survivors + 30 round-11 survivors,
   deduplicated), -nodecap 1.2e8 -sec 3600. Pass-1 explosions came from the skipped exact test: with it always on, kept sets stay
   small and most words die (deaths at K up to 1,159).
5. Imprimitive survivors h^m: rerun with the root pattern h and L = m|h| (Lemma K6, `out/fam/`); the last primitive survivor
   (p47) with nodecap 3e8 (`out/pass4/`).
6. Words that carry a known stream: Theorem U (§6). Persistent families: §9. bxb (wire + band acceptance) was run on the p47 word
   (`out/bxb/`): CAPPED at depth 2, as in round 11 for all hard words.

## 2. Soundness of the exact K-head filter (PAPER PROOF)

Notation as in `three_divides_r/PROOF.md` and `round11/premiseB/PROOF.md`. Base b = 10, clock (pattern) g ∈ {0,1}^P, phases t ∈ Z/P.
G_K(g) is the K-head graph: nodes (x, t) with x = (x_0..x_{K−1}), x_0 ∈ 1..2b−2, x_i ∈ 0..2b−2; for h ∈ {0,1} let
(y, γ) = trans(x, h); the edge (x, t) →_h (y, t+1) exists iff γ = g_t. trans is the function of Lemma A2:
H_K = h, H_i = ⌊(x_i + H_{i+1})/b⌋, γ = H_0; L_0 = 0, L_{i+1} = ⌊(x_i + L_i)/b⌋;
y_i = (x_i + L_i) mod b + [γ = 0: (x_i + H_{i+1}) mod b; γ = 1: 1 if i = 0, else (x_{i−1} + H_i) mod b].

**Lemma K1 (reach paths are closed walks).** Let P | T. A reach path of height K from the root (0, g, 1) whose cell series
v_0, …, v_{K−1} are T-periodic gives the closed walk t ↦ ((v_0[t], …, v_{K−1}[t]), t mod P), t ∈ Z/T, of length T in G_K(g),
with bit h_t = δ_K(t).
*Proof.* Compare the reach edge rule (premiseB §0) with trans symbol by symbol. The constraint ⌊(v_x[t] + δ_{x+1}(t))/b⌋ = δ_x(t)
for x = K−1, …, 0 is the downward recursion of H with H_K = δ_K(t) = h_t, so H_x = δ_x(t). The root has δ_0 = g, so γ = H_0 = g_t:
the label condition of the edge. The forward carries c_{x+1} = ⌊(v_x + c_x)/b⌋ with c_0 = 0 are L_x. The partner digits are
ρ_0 = 1 and ρ_x = (v_{x−1} + δ_x) mod b (x ≥ 1), and the new ρ at cut x+1 is (v_x + δ_{x+1}) mod b. Hence the time recursion
v_x[t+1] = (v_x[t] + c_x) mod b + (g_t ? ρ_x : ρ_{x+1}) is exactly y_x. Cells lie in 0..2b−2 and cell 0 ≥ 1 (root condition), so
every column is a node. T-periodicity closes the walk. ∎

**Lemma K2 (wires).** If an exterior (T, g, e) exists (any width W, any e), then G_K(g) has a closed walk of length T for EVERY K ≥ 1.
*Proof.* Theorem B (B⇐) gives, for every H ≥ W, an accepting reach history of height H (pad with 9s). Its prefix of height K ≤ H is a
reach path with T-periodic cells; apply K1. ∎ (Equivalently Lemmas A1, A2 of three_divides_r.)

**Lemma K3 (uniform bands).** If a uniform-band template with clock g (length T = combined period) exists (any left-end height H,
any band value cycle u_t = f^t(u_0), u_t ≠ b−1), then G_K(g) has a closed walk of length T for EVERY K ≥ 1.
*Proof.* Theorem B'(i) gives a reach path with T-periodic cells from the root to the strict band-accepting interface
I_u = (BC(u_t), BC(u_t), BR(u_t)) at height H' ∈ {H, H+1}. I_u has a self-loop: take the cell series v[t] = u_t and δ'_t = BC(u_t).
Since u_t ≠ b−1, ⌊(u_t + BC(u_t))/b⌋ = BC(u_t) (u ≤ b−2 gives 0, u ≥ b gives 1); so the edge constraint holds, c' = BC, ρ' = BR, and
v[t+1] = (u_t + BC) mod b + BR = 2 BR(u_t) = f(u_t) = u_{t+1} at every time (overflow or not, ρ = BR). The new interface is I_u again,
and the cells are T-periodic because the band period divides T. So accepting reach paths exist at every height ≥ H', and their prefixes
at every height ≤ H'. Apply K1. ∎

**Lemma K4 (projection; = A3).** An edge of G_{K+1}, (x, t) →_h (y, t+1), projects to the edge (x[0..K−1], t) →_{h'} (y[0..K−1], t+1)
of G_K with h' = ⌊(x_K + h)/b⌋ and the same label. Hence a closed walk of length L projects to a closed walk of length L.

**Lemma K5 (khx keeps a superset).** khx computes kept sets S_K ⊆ V(G_K): Γ_1 = G_1; Γ_K = induced subgraph of G_K on the children
(z, v), v ∈ 0..2b−2, of S_{K−1}; S_K = result of pruning Γ_K by
 (i) trim (iterated removal of nodes without in- or out-edge),
 (ii) SCC filter (keep the cyclic SCCs whose period divides some L ∈ Ls),
 (iii) exact closure test, when run (always with `-batch C`): t0 = a smallest phase layer; C = sources s ∈ layer t0 with a walk of
      length exactly L from s to s, for some L ∈ Ls (bitset propagation over L/P laps, sources in batches); if C = ∅ the word DIES;
      otherwise keep the nodes reachable from C within ≤ P−1 steps and reaching C within ≤ P−1 steps, then trim.
Then every node of G_K lying on a closed walk of length L ∈ Ls belongs to S_K.
*Proof.* Induction on K. Let W be such a closed walk in G_K. By K4 its projection is a closed L-walk in G_{K−1}, so (induction) its
nodes are in S_{K−1}; hence W lies in Γ_K. No pruning step removes a node of W: (i) each node of W has an in- and an out-edge on W;
(ii) W lies in one SCC, whose period divides every cycle length, in particular L; (iii) the phase advances by one per step and L ≥ P,
so W visits layer t0; every visit s returns to itself after exactly L steps (rotate W), so s ∈ C; every node of W is reached from the
previous visit within ≤ P−1 steps and reaches the next visit within ≤ P−1 steps. ∎

**Theorem K.** If khx (any version, any options) prints DIES at level K for pattern g and length set Ls, then for every L ∈ Ls there is
no 9-wire exterior and no uniform-band template (any band, any phase, any left-end height) with clock g^{L/P}, of any width.
*Proof.* S_K = ∅, so by K5 G_K(g) has no closed walk of length L; contradiction with K2 / K3. ∎

**Lemma K6 (root pattern).** If g = h^m, then (x, t) ↦ (x, t mod |h|) maps G_K(g) onto G_K(h) edge by edge (same trans, same
labels). So a closed walk of length L = m|h| in G_K(g) gives one in G_K(h), and khx run on the pattern h with Ls = {m|h|} is a valid
test for the clock g. It is the stronger form in practice: the one-lap refinement of step (iii) is tighter for the shorter pattern
(example: (001010101)^5 explodes at K = 16 with the 45-phase pattern but dies at K = 106 with the 9-phase pattern).

Remarks.
- SURVIVES (kmax / nodecap / time) claims nothing.
- Rotation (necklace) symmetry: G_K(σg) ≅ G_K(g) by t ↦ t+1, so one representative per necklace suffices (fc_enum lists).
- khx DIES at K ⇔ (if (iii) ran at level K) no closed walk of length L in G_K ⇔ (K1 + Lemma X) the bx BFS layer K is empty.
  This is why khx and bx3 agree on the death depth of every word V1 tested; khx is cheaper because it stores time-local nodes
  (a sum over phases) instead of global cut states (a product over phases).
- The filter is blind to the TOP boundary (h is free at level K). It cannot exclude a clock that has closed walks at every K
  without an exterior (example: (01)^4, where bx saturates at depth 88 but G_K(01) keeps an 8-cycle SCC at every K).

**Corollary T (transfer to multiples).** Run khx with `-allm` (keep every cyclic SCC, no exact test; this is the admissible set for
Ls = all multiples of P). If at some level K the kept SCCs have periods q_1, …, q_r, then a clock h^m (any m ≥ 1) with an exterior or a
band template needs q_i | m·|h| for some i. If the kept set is empty, no clock h^m carries one, for every m.
*Proof.* A closed walk of length m|h| in G_K lies in a cyclic SCC whose period divides m|h|; K2/K3/K4/K5 with Ls = {m|h|}. ∎

**Negative results (recorded, not filters).**
- Charge mod 9 (PAPER PROOF, short): b ≡ 1 (mod 9) and the carries telescope, so every edge satisfies
  Σ_i y_i ≡ 2 Σ_i x_i + β (mod 9) with β = h − L_K at a non-overflow step and β = H_{K−1} − x_{K−1} − L_K at an overflow: β depends
  only on the TOP of the window. This identity holds on every walk, so it can never remove a closed walk; around a closed walk it only
  links Σ x at one time with the top boundary. With a 9-wire on top, β = 1 − 2e_t and one gets exactly the known e-closure
  (`f1_charge_mod9_count.py`). So charge mod 9 gives no condition on g and no filter beyond khx.
- Forward-bisimulation quotient of the kept graph (attributes (t, lc, top digit at overflow phases)): only 11–16 % fewer nodes on a
  p41 survivor (py/bisim.py); not used.

## 3. Validation (COMPUTED)

| check | what | result | files |
|---|---|---|---|
| F1 lists | fc_enum counts p = 41..48 vs `data/f1_b10_p33_60.csv` (independent semigroup count) | all 8 totals and primitive counts equal | `logs/fc_enum_p*.log`, `out/census/summary_p*.json` |
| controls | positive (must SURVIVE to the cap): p11, p12 (N12), p22, p11^3, N12^2, (01)^4, base 13 band {8,16} clock 1010010000, base 4 wire+band 011001, base 11 001 / 001001, 17 100001, 26 01, 20 00010001, 2/4/8/16/32, base 3 11100; negative (must DIE): 01 L=36 (K=3), 0001 L=16/20/28 (K = 13/6/10 = bx depths), 0001 L=40 (Theorem A) | all as required, for khx, khx3 (-batch) and the final build | `ctrl/khx_controls.out`, `ctrl/khx3_controls_*.out` |
| -check | every built edge vs direct `trans`, every ABSENT wanted edge must have a pruned projection (strengthened in r12b) | 1,402 sampled words (≤ 200 per p = 33..40 and 200 V1 kills), 7.85M edges + 1.96M absent edges, 0 fails | `ctrl/khx_check.out` |
| V1 | khx (kmax 15) on all 5,400,712 round-11 words p = 33..40 vs the bx3 census | 5,394,669 bx3-EXHAUSTED words: khx dies at exactly the bx3 depth (all of them); of the 6,043 bx3-capped words khx kills 5,889 | `logs/val.log`, `out/val/cap_*.txt` |
| V2 | independent engine: bx3 `-layered K+1` (layer-by-layer BFS) on the 5,889 V1 kills | 5,517 EXHAUSTED at depth = khx K, 372 layer-capped, 0 disagreements | `out/val/lay/L_s*.out` |
| V3 | independent re-implementation `src/kh2.cpp` (string windows + hash map, full-window trans for every edge, Kosaraju, EXACT closed-walk set) vs khx on 1,734 words (death K from 2 to 135; 1,515 deep round-11 deaths) | SCC-mode kept counts equal at EVERY level; exact death level identical for all 1,734 | `out/v3/part*.cmp` |
| V4a | khx3 `-batch 4096` vs kh2 exact on the same 1,734 words | identical death level for all 1,734 | `ctrl/v4a.out` |
| V5 | kh2 exact on the deaths found after the resume (pass 2/3, p ≤ 32 bonus, census deaths with K ≥ 40) | see §3a | `out/v5/*.v5` |
| replay | exact big-integer replay (`py/verify_ext.py`, `bx -w -nosym`) of the streams that Theorem U leaves: p11 and N12 | both VERIFIED | `out/replay/verify_known.out` |
| provenance | final `src/khx.cpp` (default options) vs the binary used in pass 1, 150,000 census words | identical output | NOTES.md |

### 3a. V5 and V6 (independent kh2 on the new verdicts)

- V5: kh2 exact on deaths found after the resume. 67 census pass-1 deaths with K ≥ 40 (K up to 121): 67 identical. 38 deaths
  from passes 2–3 and the p ≤ 32 bonus with a widest level ≤ 6M nodes (K up to 403): 37 identical, 1 kh2 timeout (K = 74 of 303,
  23.7M nodes), 0 contradictions. The 40 remaining deep deaths (widest level 6M–109M nodes) are too large for kh2 within 40 minutes
  and rest on khx alone (V1–V4, controls, `-check`). (`out/v5/cd*.v5`, `out/v5/ns*.v5`, `out/v5/old/`)
- V6: 2,000 random census words (250 per p = 41..48): pass-1 khx and kh2 exact give the same death level for all 2,000 (`ctrl/v6.out`).

## 4. Census at periods 41–48 (COMPUTED; exclusions by Theorem K)

Every row covers ALL F1 necklaces of length T (primitive and imprimitive). "Deep DIES" = killed in pass 2, 3 or 4 (or with the
root pattern, Lemma K6). For even T the same DIES verdict also excludes every uniform-band template with combined period T
(Theorem K); for odd T no uniform band has odd combined period ({6,12} and the 6-cycle need an even T, and {0}, {18} are excluded
for every clock by E2ExtremeUniformIsolation), and Theorem K excludes them anyway for the words that die.

| p = T | F1 words | primitive | pass-1 DIES | pass-1 survivors | deep DIES | known stream only (Thm U) | UNDECIDED | decided | uniform bands |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| 41 | 2986594 | 2986594 | 2986592 | 2 | 2 | 0 | 0 | 2986594 | no odd-period band |
| 42 | 4591827 | 4591120 | 4591824 | 3 | 2 | 0 | 1 | 4591826 | decided = same words (Thm K, U), open: 1 |
| 43 | 7063492 | 7063492 | 7063484 | 8 | 8 | 0 | 0 | 7063492 | no odd-period band |
| 44 | 10871983 | 10870982 | 10871975 | 8 | 7 | 1 | 0 | 10871983 | decided = same words (Thm K, U), open: 0 |
| 45 | 16741885 | 16741816 | 16741882 | 3 | 3 | 0 | 0 | 16741885 | no odd-period band |
| 46 | 25794960 | 25793457 | 25794947 | 13 | 13 | 0 | 0 | 25794960 | decided = same words (Thm K, U), open: 0 |
| 47 | 39760190 | 39760190 | 39760177 | 13 | 12 | 0 | 1 | 39760189 | no odd-period band |
| 48 | 61317300 | 61314942 | 61317284 | 16 | 14 | 0 | 2 | 61317298 | decided = same words (Thm K, U), open: 2 |
| all | 169128231 | 169122593 | 169128165 | 66 | 61 | 1 | 4 | 169128227 | |

- Pass-1 death levels: p48 has 60,847,444 deaths at K = 2, 449,137 at K = 3, …, max K = 84 (`out/census/summary_p*.json`).
- Deep deaths reach K = 1,159 (p44 00001010101010101001010100111000100010000111, 1,790 s, 106M nodes at the widest level) and
  K = 821 (p46 (00001010101010100100111)^2).
- T = 41, 43, 47 had never been run; they are now complete except the single p47 word of §9.

## 5. The round-11 capped words (COMPUTED + PAPER PROOF)

Round 11 left 112 wire words (110 after Theorem A) and 1,475 band words open (`r11ref/final_open_*.txt`). Before the resume,
khx (exact test skipped above 4,096 sources) at nodecap 1e8 killed 1,502 of their 1,532 distinct words (`out/deep/R_*`); pass 3
(khx3 `-batch`) and the root-pattern runs killed the rest except the words below. Per word: `out/r11_status.txt`.

| list | words | DIES (Theorem K) | known stream only (Theorem U) | UNDECIDED |
|---|--:|--:|--:|--:|
| wire (incl. (0001)^10, (0001)^11 of Theorem A) | 112 | 105 | 3: p11^3 (p33), N12^3 = (0001)^9 (p36), p11^4 (p44) | 4 |
| band | 1,475 | 1,469 | 2: (0001)^9 (p36), p11^4 (p44) — no band at all | 4 |

Still UNDECIDED from round 11: p34 0001010101001001010101001010100101, (01)^20 (p40), (p21)^2 (p42) and N12^4 = (0001)^12 (p48), each open both as wire and as band (§9).

## 6. Repetitions of known streams: uniqueness by stabilization (Theorem U; PAPER PROOF + COMPUTED)

The K-head filter can never kill a clock that carries an exterior, but the *shape* of the kept set can prove uniqueness.
kept_K is the khx3 kept set at level K (pattern g, length L), with node attributes (phase, top digit x_{K−1}, forward carry L_K out of
the window) and labelled edges (bit h). TOP99_K = kept nodes whose two top digits are (9, 9). TOPUU_K = kept nodes whose two top
digits are (u, u) for a uniform band value u ∈ {0, 18, 6, 12, 2, 4, 8, 16, 14, 10}, with only the edges along which the top digit
follows u ↦ f(u).

**Lemma S (stabilization).** The candidate graph Γ_{K+1} (children of kept_K), with its attributes and the parent's top digit, is a
function of the attributed graph kept_K: the child (j, v) has the phase of j, top digit v, carry [v + L_K(j) ≥ b], parent digit
x_{K−1}(j), and for bit h the edge to (o_{h'}(j), y), h' = [v + h ≥ b], y = (v + L_K(j)) mod b + (g_t ? (x_{K−1}(j) + h') mod b :
(v + h) mod b) (Lemma K4 in incremental form). khx's pruning is a function of the graph and its phases. Hence a phase- and
attribute-preserving isomorphism kept_{K0} ≅ kept_{K0+d} propagates to kept_{K0+r} ≅ kept_{K0+r+jd} (r ≥ 1, j ≥ 0), and these maps
also preserve the parent's top digit, so they map TOP99 to TOP99 and TOPUU to TOPUU. ∎

**Theorem U.** Let S be a known exterior with clock g and period L. Suppose that for some K0 and d ≥ 1
 (a) kept_{K0} ≅ kept_{K0+d} (isomorphism found by colour refinement and verified edge by edge), and
 (b) for r = 1..d the nodes of TOP99_{K0+r} on a closed L-walk inside TOP99_{K0+r} are exactly the padded nodes of S and of its
     clock-preserving time rotations, and TOPUU_{K0+r} contains no closed L-walk.
Then every 9-wire exterior with clock g is a time rotation of S (B-level, any width), and no uniform-band template has clock g.
*Proof.* By Lemma S the numbers in (b) are the same at every level K ≥ K0+1. For K > width(S) + 1 the padded rotations of S are
closed L-walks inside TOP99_K, so they ARE its closed-walk part. An exterior X of width W gives at level K = max(K0+1, W+2) a closed
L-walk (Lemma K2) whose nodes all have top digits (9, 9); so its windows are padded rotations of S, and since K > W, X is a rotation
of S. A band template of left-end height H gives at K ≥ max(K0+1, H+3) a closed L-walk whose two top cells are (u_t, u_t) with
u_{t+1} = f(u_t) (Lemma K3, band self-loop): a closed L-walk inside TOPUU_K, which does not exist. ∎
The same proof with S = ∅ ("the closed part of TOP99 is empty") excludes every exterior and every band for a clock that khx can never
kill; no word of this round reached a periodic kept set without a known stream, so this form was not needed.

Checks (`py/kstruct.py`, `py/wire_unique.py`; dumps and witnesses in `out/uniq/`; witnesses from `bx3 -w -nosym`, replayed in §3):

| clock | pattern, L | K0, d | kept (per level) | closed part of TOP99 | TOPUU | verdict |
|---|---|---|---|---|---|---|
| p11 = 00001110001 | p11, 11 | 300, 1 | 22 = 11 padded p11 + 11 top perturbations | 11 = padded p11 | 0 | unique (agrees with bx `-count`) |
| p11^2 (p22) | p11, 22 | 300, 1 | 22 | 11 = padded p11 | 0 | **B-level unique** (was UNDECIDED, EXTERIOR §3b) |
| p11^3 (p33) | p11, 33 | 300, 1 | 22 | 11 = padded p11 | 0 | **only p11 repeated; no band** |
| p11^4 (p44) | p11, 44 | 300, 1 | 22 | 11 = padded p11 | 0 | **only p11 repeated; no band** |
| p11^5 (T = 55, bonus) | p11, 55 | 300, 1 | 22 | 11 = padded p11 | 0 | only p11 repeated; no band (p11^6 run stopped, not claimed) |
| (0001)^3 (N12) | 000100010001, 12 | 300, 3 | 2245 / 1046 / 1730 | 36 = N12 and its 4- and 8-step rotations | 0 | re-proves P(3) (bx_r3) |
| (0001)^9 = N12^3 | 0001, 36 | 400, 3 | 60805 / 56407 / 58562 | 12 = padded N12 (all rotations) | 0 | **P(9): only N12 repeated; no band** |

For p11 the kept set at K = 300, 301 is EXACTLY {padded p11} ∪ {padded p11 with top digit replaced by w_t}, w = (15, 10, 0, 2, 5, 15,
5, 15, 11, 2, 5) (`wire_unique.py`: RESULT PASS for L = 11, 22, 33, 44, 55). For p11^4 the pattern-g run (44 phases) shows the same
shape: 88 = 2 × 44 kept nodes at K = 5000.

**Where it stops.** N12^2 = (0001)^6 (L = 24): the kept set fluctuates between 1.3·10^5 and 2.7·10^5 nodes without period up to
K = 800 (`out/n12/L24.log`). Every closed 24-walk doubled is a closed 48-walk, so the L = 48 kept set contains it: Theorem U cannot
settle N12^4 = (0001)^12 with these runs (the L = 48 run was stopped at K = 44, 1.8M kept nodes). P(6) keeps its ReachDisk proof; P(12)
is UNDECIDED. (01)^{4j}: the kept set grows exponentially (L = 8: 247,256 nodes at K = 150), no stabilization. (p21)^2: no known
stream, but its kept set (0.4M–1.6M nodes up to K = 671) never became periodic, so neither Theorem K nor the S = ∅ form of Theorem U
applies yet.

## 7. Transfer to all multiples (Corollary T; PAPER PROOF + COMPUTED)

`run_allm.sh` runs `khx3p -allm -periods` (keep every cyclic SCC, no exact test, i.e. the admissible set for "L = any multiple of
|h|") on every primitive F1 root h with |h| ≤ 24 (6,722 words, from `fc_enum 10 2 24`).
- **6,700 roots become acyclic** (at K = 2..30; 5,979 already at K = 2): for every m ≥ 1 no clock h^m carries a 9-wire exterior or
  a uniform-band template (`out/allm/r0*.out`).
- 22 roots keep cycles up to the cap (6M nodes): 01, 0001, 0000111, 000100011, 001010101, 00001110001 (p11), 00010010111,
  000100100011, 00100101010101, 0000111000100111, 0000111000110001, 00001010100100111, 001001010101010101, 0001010001010100111,
  00001110001000110001, 00001110001001110001, 001001010101001010101 (p21), 001010101010101010101, 0001000101010010100011,
  00001010101010100100111, 000100010101010011100011, 001001010100100101010101. For three of them the surviving SCC periods
  restrict m: 0000111 and 0000111000100111 need m even, 01 needs 4 | m (the 8 | p theorem).
- Scope: the statement is per root h listed (F1-accepted at length |h|); a power h^m can be F1-accepted when h is not.

## 8. Bonus: the UNDECIDED words of EXTERIOR.md §4 (p ≤ 32)

khx3 `-batch 4096` (nodecap 8e7, 30 min) on the 54 words that EXTERIOR.md §4 lists as UNDECIDED (`out/le32/`): **50 DIE**
(K from 5 to 435), among them the p21 word 001001010101001010101 (K = 112, max level 411,578 nodes; kh2 exact also dies at K = 112).
Survivors: (01)^8, (01)^12, (01)^16 (the persistent (01) family) and (0001)^6 = N12^2 (time cap at K = 475;
"only N12 twice" is the ReachDisk result). Some of the 54 had been settled since by other methods; this is an independent proof.

## 9. UNDECIDED words (nothing claimed; wire AND band open for each even T)

| T | word | type | why open |
|--:|---|---|---|
| 34 | 0001010101001001010101001010100101 | primitive (round 11) | khx3 survives to K = 1,781 (3,600 s); kept set 0.6M–3.6M, fluctuating and slowly growing, no period |
| 40 | (01)^20 | (01)^{4j} family (round 11) | G_K(01) keeps 8-periodic walks at every K ((01)^4 has closed walks at every K although bx saturates without a stream); kept set grows exponentially; root-pattern run L = 40 stopped at K = 60 (1.09M kept, growing) |
| 42 | (001001010101001010101)^2 = (p21)^2 | imprimitive (round 11 + census) | root p21 dies at L = 21 (K = 112) but L = 42 survives to K = 671 (time), kept 0.4M–1.6M, no period |
| 47 | 00010001000110001100010010001010100101000100011 | primitive (census) | pass 4 (khx3, nodecap 3e8), two runs: survives to K = 588 (about 3,300 s each); kept 2.5M–7M nodes, fluctuating (dip to 2.5M at K = 548, back to 3.5M); bxb CAPPED at depth 2 (42.6M states) |
| 48 | (0001)^12 = N12^4 | N12 family (round 11 + census) | N12^4 is an exterior, so khx cannot die; the L = 24 part of the kept set does not stabilise (§6): P(12) open |
| 48 | (01)^24 | (01)^{4j} family (census) | as (01)^20; root-pattern run L = 48 stopped at K = 26 (1.39M kept, growing) |

For p ≤ 32 the remaining open words are (01)^8, (01)^12, (01)^16 and N12^2 = (0001)^6 (§8).
`out/final_open.txt` and `out/r11_status.txt` are the machine-readable lists.

**Next steps suggested by the data.** (i) The (01)^{4j} and N12^j families need a top-boundary argument, not a K-head one: their
kept sets keep walks that never reach a 9-wire or band top; a backward (top-down) automaton intersected with the stabilised kept
graph is the natural tool. (ii) For the p34, p47 and (p21)^2 words, a better exact-test anchor (the layer of smallest SCC cut instead of the
smallest phase layer) or a 3–4× leaner node layout (implicit phase, no reverse CSR) would allow nodecap 1e9 within 40 GB.

## 10. Labels and what is NOT claimed

- Every DIES is COMPUTED (khx output) and turns into an exclusion by Theorem K (PAPER PROOF, Lemmas K1–K5 on top of Theorem B,
  Theorem B' and Lemma X of `round11/premiseB/PROOF.md` and Lemmas A1–A3 of `three_divides_r/PROOF.md`). The wire part is
  unconditional. The band part covers exactly the uniform-band templates of Σ_U (premiseB §0), any band value cycle, any phase, any
  left-end height, combined period = |g|. Non-uniform bands, centres, and anything about 196 are not claimed.
- Theorem U results (p11^m, m ≤ 5; P(3); P(9)) are PAPER PROOF + COMPUTED (khx3 dumps + `kstruct.py`).
- Corollary T results: PAPER PROOF + COMPUTED, per listed root.
- UNDECIDED (§9): nothing is claimed for them; in particular not for N12^4, (01)^{4j}, (p21)^2.
- SURVIVES is never used as evidence for an exterior. 0 accepted streams were found apart from the known p11 and N12 streams;
  0 NEW. The two known streams were replayed with exact integers.
- Not Lean-checked. Premise (A) of ReachDisk is not used anywhere here.

## 11. Files (this directory; binaries not included)

- Sources: `src/khx.cpp` (final; default options = the pass-1 binary; the binaries `khx`, `khx3`, `khx3p` of the logs are
  builds of successive versions of this file, `c++ -O3 -std=c++17 -o khx src/khx.cpp`), `src/kh2.cpp` (independent checker).
  bx.cpp, bxb.cpp, fc_enum.cpp are unchanged copies of `../../round11/periods33to48/src/` and are not repeated here.
- Scripts: `run_census1.sh`, `run_khx_list.sh`, `run_khxb_list.sh`, `run_allm.sh`, `run_val.sh`, `run_layered_check.sh`, `rr_split.sh`,
  `bg.sh`, `watchdog.sh`, `ctrl/*.sh` (written for ~/p196_run/r12b on the Studio); Python: `py/census_summary.py`, `py/final_r12b.py`,
  `py/kstruct.py`, `py/wire_unique.py`, `py/dump_wire_diff.py`, `py/bisim.py`, `py/val_cmp.py`, `py/verify_ext.py`,
  `py/f1_charge_mod9_count.py`.
- Results: `out/final_table.md`, `out/final_open.txt` (UNDECIDED, census), `out/r11_status.txt` (every round-11 open word),
  `out/census/summary_p*.json`, `out/census/surv_p*.txt`, `out/allm.tgz` (transfer), `out/val_lay.tgz` (V2), `out/uniq/` (Theorem U:
  khx lines, witnesses, the p11 dumps; `kstruct_rerun.log` = kstruct/wire_unique re-run on the existing dumps, 2026-11-10),
  `out/replay/`, `out/bxb/`, `ctrl/*.out` (controls, V4a, V6, main-session check `ctrl/main_check_*`), `logs/*.log`.
  Packed in `logs.tar.gz`: `out/pass2/`, `out/pass3/`, `out/pass4/`, `out/fam/`, `out/deep/`, `out/le32/`, `out/n12/`, `out/v3/`,
  `out/v5/`, `out/v6/`.
- Not copied (regenerable): `lists/` (fc_enum, 1 minute), the per-word census outputs `out/census/p*_s*.khx.gz` (10 minutes, 1 GB),
  `out/val/`, and the N12 dumps of `out/uniq/` (60 MB each; `khx3p 10 -g 0001 -L 36 -batch 4096 -kmax K -dump F` for K = 400..403,
  `-L 12` for K = 300..303).
- Theorem U check: `python3 py/kstruct.py --wit out/uniq/n12_wit.txt --L 36 n12_L36_K400.dump n12_L36_K403.dump n12_L36_K401.dump
  n12_L36_K402.dump` (ISO FOUND, closed TOP99 part = 12 padded N12 nodes, TOPUU 0 at K = 401..403); p11: `ctrl/p11m.sh`.
