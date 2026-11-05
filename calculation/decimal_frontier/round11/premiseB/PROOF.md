# Premise (B): the reach graph and the Agent120 exterior system

Directory `~/p196_run/r11g/` on the Studio (copy: `~/Desktop/p196_studio/r11g/`). Repo read-only, unchanged; nothing pushed.
Labels: PAPER PROOF / COMPUTED / UNDECIDED only.

**Status in one line.** Premise (B) is a theorem: the WIRE part of the reach graph is the Agent120 exterior system,
exactly, in both directions, height by height (Theorem B, PAPER PROOF; every lemma re-checked exhaustively, 0 mismatches,
COMPUTED). For uniform bands, the target is a different object: a left end under a uniform band that reaches the centre.
It is not an Agent120 object. The direction "template ⇒ reachable" holds, but only at height H **or H+1** (Theorem B').
The strict band acceptance of `reach` is one height late. Exclusions over all heights are unaffected. The band fit heights
that have been reported (13/18, 55/75) are left-end height + 1.

---------------------------------------------------------------------------------------------------------------------------
## 0. The two systems (exact definitions)

Base b ≥ 2. A *column word* is a list over {0..2b−2}. trim(v) removes the trailing entries b−1. pad_H(B) = B ++ (b−1)^{H−|B|}.

**Σ_A (Agent120 exterior; `calculation/neutral_band_search.py`).** The domain is 𝓛 = {B over {0..2b−2} : B = [] or B[0] ≥ 1, last entry ≠ b−1}.
Let e1(B) be the forward carry out of B, and C any centre with e2(B,C) = 1−e1 (hyp). Then Φ(B) = trim(nextB(B,C)) and γ(B) = gam(B,C).
These depend on B only (THEORY Lemma 1). For a clock g ∈ {0,1}^T, an *exterior (T, g, e)* is a sequence (B_t)_{t∈Z/T} in 𝓛
with Φ(B_t) = B_{t+1}, γ(B_t) = g_t and e1(B_t) = e_t. Its width is W = max_t |B_t|. B_T = B_0 is required, so the
minimal period only divides T. Any `cycleOK` certificate projects to an exterior: its B may carry non-maximal trims, and
by A1 below, trimming commutes with the step.

**Σ_R (reach WIRE; `uniform_bands/reach.cpp`, identical rule in `reachmt.cpp`, `reachdisk.cpp`, `bx.cpp`).**
- An *interface* is I = (c, δ, ρ) with c, δ ∈ {0,1}^T and ρ_t ∈ {0..b−1} at the overflow times g_t = 1.
- An edge I_x → I_{x+1} is a T-periodic cell series v_x ∈ {0..2b−2}^{Z/T} together with bits δ'_t that satisfy ⌊(v_x[t]+δ'_t)/b⌋ = δ_t.
  The edge gives c'_t = ⌊(v_x[t]+c_t)/b⌋ and ρ'_t = (v_x[t]+δ'_t) mod b, and
  v_x[t+1] = (v_x[t]+c_t) mod b + (g_t ? ρ_t : ρ'_t).
- The root is (0, g, 1) and cell 0 ≥ 1 at all times. WIRE acceptance is δ = 1−c and ρ_t = (b−1)c_t at the overflow times.
- An *accepting history of height H* is a path root = I_0 → … → I_H with I_H accepting, together with its cell series. Its stream is c(I_H).

**Σ_U (uniform-band templates; the format behind the reach BAND targets).** u is a band value, u ≠ b−1, with
f(u) = 2((u+[u≥b]) mod b), BC(u) = [u≥b], BR(u) = (u+BC) mod b. A *template of height H* is a reverse-and-add orbit
N_t (t ≥ t_0) whose pair words are P(N_t) = E_t u_t^{m_t} rev(E_t), with |E_t| = H, (E_t) T-periodic and m_t ≥ 3.
The condition m_t ≥ 3 is no restriction: a clock with no overflow is impossible (N_t increases at constant length), so
n_t → ∞ and m_t → ∞. Strict reach BAND acceptance at height H is c = δ = BC(u_t), and ρ_t = BR(u_t) at the overflow times.

---------------------------------------------------------------------------------------------------------------------------
## 1. Statements

**Theorem B (PAPER PROOF).** Fix b ≥ 2, T ≥ 1, g, e ∈ {0,1}^T and H ≥ 1. The map v ↦ (trim v[t])_t is a **bijection** from
the accepting reach histories of height H with stream e onto the exteriors (T, g, e) of width ≤ H. Its inverse pads each
B_t to height H. Consequently:
- (B⇐) **exterior ⇒ reachable.** This is the direction every exclusion uses.
- (B⇒) **reachable ⇒ exterior.** Every stream that reach reports is a genuine B-cycle.
- (B=) The BFS height at which reach first reports e equals the minimum, over exteriors (T, g, e), of the width.
  This is the observed "first height = max cycle width".
- COMPLETE with no stream e means no exterior (T, g, e) of **any** width. Port-word "stream:" targets (chain 1) are covered.

**Lemma R (ROT, PAPER PROOF).** Let k be a shift with σ_k g = g. Then σ_k maps edges to edges, fixes the root, and maps
the WIRE set, each stream-target set closed under σ_k, and the band-target set (all phases) onto themselves. Therefore the
orbit BFS reaches exactly the orbits of reachable interfaces, at the same heights.

**Lemma X (bx ≡ reach, PAPER PROOF).** The bx cut state (L, H, Y), its successor rule, its start (0, g, 1) and its
acceptance are the reach interface (c, δ, ρ) with the same rule, symbol for symbol. The state count identities of EQUIV_R8 §C
(bx = reach + 1, the start state) follow.

**Theorem B' (bands, PAPER PROOF).**
- (i) A template of height H with combined period T* = lcm(T, period of u_t) gives an accepting reach path for clock g,
  period T*, at height H+1. It also gives one at height H if c_H(t) = BC(u_t) at every overflow time.
- (ii) Strict acceptance at height H holds iff there is a one-step template move at height H for every band length m ≥ 3.
  This is the soundness used by fits, which still need replay plus the induction.
- **The +1 is real.** For an overflow time, (u+c_H) mod b + ρ_{H−1} = f(u) has a second solution c_H ≠ BC with
  ρ_{H−1} = BR ∓ 1. An example in base 10: E = (18,17), u = 8. Strict acceptance then needs one band cell absorbed into the left end.

---------------------------------------------------------------------------------------------------------------------------
## 2. Proofs

**Lemma 1 (two-sweep form; THEORY §1.2, re-proved).** nextB unwinds as follows. DB = F gives the forward digits.
DR = norm(rev B, e2), whose reversal is R_i = (B_i + d_{i+1}) mod b, with d_n = e2 = 1−e1, d_i = ⌊(B_i+d_{i+1})/b⌋ and
gam = d_0. If gam = 0, then zw(F, R) gives B'_i = F_i + R_i. If gam = 1, then zw(F ++ [xd], [1] ++ R) gives
B'_0 = F_0+1, B'_i = F_i+R_{i−1} and B'_n = (b−1)(1−e1)+R_{n−1}. B = [] gives [b]. ∎

**Lemma A1 (padding; three_divides_r/PROOF.md, re-proved).** A top coefficient b−1 passes both carries: (b−1)+e1 gives
carry e1, and (b−1)+(1−e1) gives carry 1−e1. So e1, γ and every F_i, R_i (i < n) are unchanged, and the new top entries
equal b−1. Hence trim∘nextB∘pad = Φ∘trim. ∎

**Lemma 0 (domain).** Φ maps 𝓛 into 𝓛: if gam = 0, B'_0 = 2B_0+d_1 ≥ 2; if gam = 1, B'_0 = F_0+1 ≥ 1; and [] ↦ [b].
Under padding, B = [] corresponds to cell 0 = b−1 ≥ 1. So the reach root condition "cell 0 ≥ 1 at all times" is exactly
the hyp condition "B[0] ≠ 0", and it never cuts an exterior.

**Lemma S (column step).** Take a column v of height H with v_0 ≥ 1 and a bit g. Run the reach rule at one time step:
c_0 = 0, δ_0 = g, ρ_{−1} = 1, with δ_{x+1} chosen under ⌊(v_x+δ_{x+1})/b⌋ = δ_x. A WIRE-accepting branch exists iff
g = γ(B) and |Φ(B)| ≤ H, where B = trim v. That branch is unique, and it has c_H = e1(B) and v' = pad_H(Φ(B)).

*Proof.*
1. c is the forward carry of v, so c_H = e1(v) = e1(B) by A1.
2. Acceptance fixes δ_H = 1−c_H. The constraint then determines δ_x downward uniquely: δ_x = d_x of Lemma 1. The root
   needs δ_0 = g, so g = d_0 = γ. This gives uniqueness.
3. With ρ = R and F_x = (v_x+c_x) mod b, v'_x is nextB(v)_x for every x < H (ρ_{−1} = 1 is the "+1").
4. If g = 1, nextB(v) has one more entry, (b−1)(1−e1)+R_{H−1}. It equals b−1 iff R_{H−1} = (b−1)e1, which is the ρ condition.
5. So acceptance ⇔ nextB(v) = v' (++ [b−1] if g = 1). By A1 this ⇔ trim v' = Φ(B), |v'| = H, i.e. v' = pad_H Φ(B).
   Conversely, if |Φ(B)| ≤ H, the extra top entry must be b−1, so the ρ condition holds. ∎

**Proof of Theorem B.**
1. The reach DFS couples time t only to time t+1, through v_x[t+1], and to the interface bits at time t. Acceptance is a
   conjunction over t.
2. So a path of height H with cell series v is accepting iff, for every t ∈ Z/T, the column v[t] has an accepting
   one-step branch with bit g_t and output v[t+1].
3. By Lemma S this holds iff, for all t, γ(B_t) = g_t, |B_{t+1}| ≤ H and v[t+1] = pad_H(Φ(B_t)), where B_t = trim v[t].
   That is exactly an exterior of width ≤ H with e_t = c_H(t).
4. The δ bits are forced (Lemma S), so histories correspond one-to-one to cell series. The values stay in 0..2b−2
   automatically, and cell 0 ≥ 1 is Lemma 0. Since pad∘trim = id on these columns, the map is a bijection.
5. (B=) An accepting node maps to itself under a b−1 cell, which is the self-loop (c, 1−c, (b−1)c). It is never reported
   twice, and BFS order gives the minimum. The root is never accepting. ∎

**Proof of Theorem B'.**
1. Write the pair-word step for a symmetric P of length n, with forward carries c_x. Define d_x := c_{n−x}, the mirrored
   carry. Then d_x = ⌊(P_x+d_{x+1})/b⌋ and the digit m_{n−1−x} equals R_x. So P'_x = F_x+R_x, or F_x+R_{x−1} with
   R_{−1} = m_n = 1 at an overflow. The left end therefore obeys the reach rule with root (0, g, 1), and P_0 ≥ 1 because
   of the leading digit.
2. Above the left end, u ≠ b−1 forces the carries: d_H = d_{H+1} = BC (using m ≥ 2), R_H = BR, and an interior band cell
   goes to 2BR = f(u).
3. Template step at a non-overflow time: (u+c_H) mod b + BR = 2BR forces c_H = BC, since u and u+1 differ mod b.
4. At an overflow time, the step is (u+c_H) mod b + ρ_{H−1} = 2BR. The solution c_H ≠ BC is allowed. In that case, take
   cell H (series u_t) into the left end. Its rule holds, and the interface at H+1 is (BC, BC, BR), which is strict
   (m ≥ 3 is needed for d_{H+2}). Periodicity holds with period T*.
5. (ii) is the same computation read backwards. ∎

---------------------------------------------------------------------------------------------------------------------------
## 3. Computations (Studio, nice 10, ≤ 4 threads, < 1 GB; all COMPUTED, 0 mismatches)

| check | script / output | domain | result |
|---|---|---|---|
| Lemma 1, A1, Lemma S, against the repo mirror's own `nextB` (centre chosen with e2 = 1−e1) | `chk_step.py` | every column v of height H: b = 2 (H ≤ 10), 3 (≤ 7), 4 (≤ 6), 5 (≤ 5), 10 (≤ 4), 13 (≤ 3); 459,812 columns | 0 mismatches |
| Theorem B as a count identity: #exteriors of width ≤ h = #reach histories of height h, for every (g, e, h); plus the C++ `reach` binary's stream heights = the model's; plus shift closure (Lemma R) of every reachable layer | `chk_cycles.py` → `chk_cycles*.out` | every clock: b = 2 (T ≤ 8, h ≤ 10), 3 (T ≤ 6, h ≤ 7), 4 (T ≤ 6, h ≤ 6), 5 (T ≤ 4, h ≤ 5), 10 (T ≤ 4, h ≤ 4) | 0 mismatches. Nonzero counts include base 3 p = 5 (width 7) and base 4 p = 3 (widths 2, 6). Base 5 and base 10 are 0 = 0 in the box |
| Lemma S against genuine reverse-and-add on integers: pair word E 9^m C 9^m rev E | `chk_int.py` → `chk_int.out` | b = 3, 4 (H = 4), 10 (H ≤ 3), 13 (H = 2), m = 2..4; 29,994 words | 0 mismatches |
| Theorem B' (i)+(ii) on integers: pair word E u^m rev E | `chk_int.py` | b = 4, 10, 13; every band value; H ≤ 3; m = 3..6 | 0 failures. "Strict only at H+1" occurs: base 4: 1,372; base 10, H = 3: 5,776; base 13: 100. Always at an overflow |
| ROT = 0 vs ROT = 1 (`reachmt`) | `rotchk.sh` → `rotchk.out` | (3,10/20,11100), (4,6,100), (4,12,011001), (10,12,0001), (10,22,p11), (13,10,…) | same streams, targets and heights. Orbit counts as in EQUIV_R8 |
| relaxed band acceptance (Theorem B' (i), exact form) | `src/reach_relax.cpp`, `relax.sh` → `relax.out` | the calibration bands | base 4: 13 → **12**, 18 → **17**. Base 13: 55 → **54**, 75 → **74**. Decimal clock 01 T = 8 and 0001 T = 12: no band either way, COMPLETE |
| mirror self-test | `neutral_band_search.py selftest` | Lean certificates in bases 2..32, 11, 17, 26 | PASSED |

A by-product: base 3, clock 11100, T = 20 has exteriors of period 20 that are not repetitions, first at width 115
(`rotchk.out`). By (B⇒) they are genuine B-cycles.

---------------------------------------------------------------------------------------------------------------------------
## 4. Effect on existing conclusions

- **Upgraded (now unconditional on (B)).** Every statement about 9-wire streams no longer needs (B) and rests only on the
  correctness of the programs (COMPUTED):
  - ReachDisk §1: no stream except N12 twice at (24, 0001);
  - EXTERIOR vs reach census agreement, and the 51 words that reach decides;
  - three_divides_r P(6) "only N12 twice";
  - chain 1 port-word UNREACHABLE for P = 24, 32 and 40. For P = 48 the cone also uses (A).
- **Bands.** All exclusions over all heights (COMPLETE, EMPTY, backward cones) stand, because a template of height H is
  reached at H+1. Height-limited band statements must be read as "no template of left-end height < h−1". The reported fit
  heights are one above the minimal left end (calib: 12/17, 54/74).
- **Scope of "T".** A band exclusion at T covers templates whose combined period lcm(left end, band) equals T. A left end of
  period 7 under the 6-band needs T = 42.
- **Not covered by (B).**
  - Premise (A), the window filter of the cones.
  - Chain 6: whether the m = 8 "cuts" use the reach convention (c_x, δ_x, ρ_{x−1}). Only cycles 0, 1, 50 and 127 were checked.
  - The Lean ↔ Python mirror (self-test only).
  - The centre (`Agent6NineRailCentreRenewal`).
- **No counterexample to (B) exists.** The only discrepancy found is the band height offset above.
