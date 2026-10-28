# THEORY.md  (W2 "theory": why no single-band neutral certificate in base 10?)

Labels: PAPER PROOF (complete proof written below; also tested numerically where noted), COMPUTED (exact finite computation,
command given), LEAN-VERIFIED (none claimed by W2), UNDECIDED, CONJECTURE.  Nothing here modifies the GitHub repo.
Notation: b = base, `Hyp`/`cycleOK` as in `lean/P196/Drafts/Agent120NeutralBandCalibration`; "mirror" = `mirror.py` (copy of the exact
Python mirror, passes its selftest).  p = period (number of edges) of an exterior B-cycle, G = Σgam over one period,
n = |B|, m = |C|, u,v = trims into the bands.  All scripts are in `scripts/` (or `own/`), data in `out2/`.

---------------------------------------------------------------------------------------------------------------------------
## 1. Reductions of the format

**1.1 Pair word / template** (given).  N + rev N = val(B ++ (b-1)^g ++ C ++ (b-1)^g ++ rev B), coefficients LSB first.
Hyp needs e1 ≠ e2, i.e. e2 = 1 - e1, where e1 = carry out of B (carry-in 0) and e2 = carry out of C with carry-in e1.

**1.2 Lemma 1 (decoupling, two-sweep form).  [PAPER PROOF; tested: scripts/test_FR.py, 120,000 random words vs mirror]**
Assume Hyp.  Then nextB depends on B alone.  Write n=|B| and define two normalisations of the *same* word B:
forward carries c_{-1}=0, c_i = ⌊(B_i + c_{i-1})/b⌋, F_i = (B_i + c_{i-1}) mod b, e1 = c_{n-1};
backward carries d_n = 1-e1, d_i = ⌊(B_i + d_{i+1})/b⌋, R_i = (B_i + d_{i+1}) mod b, gam = d_0.
Then  gam=0: B'_i = F_i + R_i ;  gam=1: B'_0 = F_0 + 1, B'_i = F_i + R_{i-1} (1≤i<n), B'_n = (b-1)(1-e1) + R_{n-1}.
(Proof: unwind `nextB`, DB = F, rev(DR) = R.)  Consequently a closed cycle of edges has a B-component that is a periodic orbit of the
autonomous map B ↦ B'(trimmed of trailing b-1's); the centre C is *driven* by the stream (e1_t, gam_t) of this orbit and must satisfy
e2(C_t) = 1 - e1_t at every step.  So: **certificate = B-cycle + C-cycle with matching (e1,gam) streams.**

**1.3 Lemma 2 (centre rules).  [PAPER PROOF; tested scripts/tests_lemmas.py L1; own/difftest.py]**
(a) For valid C of length m: e2 = 1-e1 ⟺ (e1=1 and val C ≤ b^m-2) or (e1=0 and val C ≥ b^m).  val C = b^m-1 is a dead state.
    So e1_t is a function of C_t (e1 = [val C < b^m]) – the centre *emits* the same e-stream as B (a constraint, not a freedom).
(b) C_t is a palindrome (image of `nextC` is symmetric, trimming preserves symmetry); odd length ⇒ middle coefficient even.
(c) m' = m + gam - 2v.  Empty C is dead (e1=e2).  Maximal trimming is canonical (a coefficient b-1 at both ends behaves like band).
(d) Closed cycle ⇒ Σu = Σgam and 2Σv = Σgam (so Σgam even) and cycleOK's gain ≥ overflow inequality is automatic:
    **any closed (B,C) cycle is a certificate** (brief; re-derived, uses |nextB| = |B|+gam-u etc).

**1.4 Lemma 3 (parity twist).  [PAPER PROOF]**  Let the exterior B-cycle have *minimal* period p0 and G0 = Σgam over a period.
If G0 is odd then every centre cycle compatible with it has period a multiple of 2·p0, because m_{t+p0} ≡ m_t + G0 (mod 2).
Hence Σgam of a certificate ≡ 0 mod 2 forces k·G0 even (k = number of exterior laps).
*This is the exact reason why the overflow words of the known G=2 certificates are "a short word repeated twice"*: every known certificate
in bases 2,4,8,16,32,11,26 sits on an exterior cycle with G0 = 1 (p0 = 2,3,4,5,6; 3; 2) and the centre has period p = 2·p0 (the centre has a
**Z/2 twist**: its width parity flips after one exterior lap).  [COMPUTED, `scripts/` snippet in NOTES: B-sequences have period p/2 and C-sequences
period p for all of these.]  Exceptions: base 17 (g=100001, G0=2, B-period 6) and base 20 (g=00010001, G0=2, B-period 8, E=01001011 whose
second half is the complement of the first): here the exterior cycle itself already has G0 = 2 and k=1.

---------------------------------------------------------------------------------------------------------------------------
## 2. The lowest-coefficient counter and the density theorem

**2.1 Lemma 4 (counter).  [PAPER PROOF; tested scripts/tests_lemmas.py L2]**  Let x = B_0 ∈ [1,2b-2] and κ = d_1 ∈ {0,1} the backward carry arriving at position 0 from
position 1 (the only information about the rest of B that enters B'_0).  Then
  gam=0 needs x+κ ≤ b-1 and gives x' = 2x+κ ;  gam=1 needs x+κ ≥ b and gives x' = (x mod b)+1.
(Proof from Lemma 1: gam = d_0 = ⌊(x+κ)/b⌋; F_0 = x mod b, R_0 = (x+κ) mod b.  If gam=0 then x ≤ b-1 and B'_0 = F_0 + R_0 = 2x+κ; if gam=1 then B'_0 = F_0 + 1.)

**2.2 Theorem 5 (density).  [PAPER PROOF; per-edge inequalities verified for b=2..130 by scripts/lemma_potentials.py; cycle means by scripts/counter_potential.py]**
In every B-cycle (indeed every cycle of the counter graph), with L = bitlength(b):
  (U)  p ≤ L·G ;      (L)  p ≥ 2G  (for b ≥ 5).
*Proof (U).*  ψ(x) = -⌊log2 x⌋.  A non-overflow edge has ψ' - ψ = -1 exactly (bitlength(2x+κ) = bitlength(x)+1).  An overflow edge with x ≥ b has x = b+j-1,
x' = j ∈ [1,b-1] and ψ'-ψ = ⌊log2(b+j-1)⌋ - ⌊log2 j⌋: for j=1 this is ⌊log2 b⌋ = L-1; for j ≥ 2 it is ≤ (⌊log2 b⌋+1) - 1 = L-1 because b+j-1 < 2b and ⌊log2 j⌋ ≥ 1.
The edge x=b-1 (κ=1) → b has ψ'-ψ = ⌊log2(b-1)⌋ - ⌊log2 b⌋ ≤ 0.  Summing ψ over a cycle: 0 = -(p-G) + Σ_ov(ψ'-ψ) ≤ -(p-G) + G(L-1), i.e. p ≤ L·G.
*Proof (L).*  π(x) = ⌊log2 x⌋.  Non-overflow edge: π' - π = +1 exactly.  Overflow edge with x ≥ b: x' = x-b+1 ≤ x/2 (because x ≤ 2b-2), so π' ≤ π-1.
The single exceptional overflow edge x=b-1 → b (κ=1) is always followed by the forced overflow b → 1; together they change π by -⌊log2(b-1)⌋ ≤ -2 (b≥5).
Summing over a cycle: 0 ≤ (p-G) - G, i.e. p ≥ 2G. ∎
*Remarks.*  (i) For b=10: 2G ≤ p ≤ 4G, zero-runs of the overflow word are ≤ 4 (2^{n-1} ≤ b-1), and the unique saturating counter cycle for (U) is
1→2→5→10→1 (stream (1000)^G); for (L) it is 9↔18 (stream (10)^G).  In base 11 the same bound (U) holds (L=4) with tight cycle 1,2,5,11; in 2^j it is
saturated by the certificates (stream (10^j)^2, p0 = j+1 = L).
(ii) This is a *necessary* condition only.  It does **not** exclude Σgam=2 in base 10 (it allows p ∈ [4,8]); what excludes it is the exact exterior
census below.  So "Σgam ≥ 4 in base 10" is "no exterior cycle with G0 ≤ 2" – a statement about the B-system, not about the counter alone.
This answers the coordinator's remark that base 11 has the same run bound yet a period-6, Σgam=2 certificate.

**2.3 Proposition 6 (how few streams are realisable).  [COMPUTED: own/gamlist.cpp, own/gamcount.cpp; independently reproduced by W5 (first-coordinate NFA)]**
Number of cyclic gam-words (necklaces) of length p realisable by the counter graph in base 10:
 p=8:5, 9:9, 10:10, 11:14, 12:22, 16:95, 20:449, 24:2268, 28:11939, 32:64249, 36:351150, 40:1943815 (growth ≈1.5^p).
By G:  p=11: G=3:1, 4:9, 5:4;  p=12: G=3:1, 4:9, 5:11, 6:1.  Hence an exact exterior census needs only these streams (not all 2^p masks).

---------------------------------------------------------------------------------------------------------------------------
## 3. Exterior census (what B-cycles exist)

**3.1 Base 10, G = Σgam ≤ 5, all p ≤ 4G.  [COMPUTED: bin/bauto2 -G n (own copy of repo bauto with popcount filter), out2/ext10_G*.txt]**
Exactly two exterior families: p=11 (G=4, g=11100010000, e=10100110011, |B|=25..29) and p=12 (G=3, g=(1000)^3, three e-streams
101010010101 / 010110101001 / 100101011010 = rotations of ONE B-cycle, |B|=51..53).  G=6: nothing found except that (1000)^6 (p=24) hit the 15M-state cap
(UNDECIDED; it contains the doubled p12 cycle).  Also: no exterior cycle with p ≤ 10, 13–15, 17, 19, 20 (earlier bauto runs, brief).
W5 (own engine `bx`, validated against bauto2) extends this to p ≤ 24 with a handful of capped words – see /home/claude/research/w5_exterior/NOTES.md.

**3.2 Small exterior streams across bases (p ≤ 8, all counter-realisable streams).  [COMPUTED: own/primtable.sh]**
 b=2:(10)^r  3:11100,11101100  4:100,100100,101100  5:10100100  6:(10)^r  7:100,100100  8:10,1000,(1000)^2,(10)^r  9:–  **10:–**  11:100,100100,101010,11000
 12:–  13:–  14:(10)^r  15:–  16:10000  17:10000,110000  18:10000  19:–  20:10,100,1000,(1000)^2,100100,(10)^r  21:–  22:–  23:–  24:10,100,100100,(10)^r  25:–  26:(10)^r
 27–31: 30:(10)^r, others –   32:10,100000,(10)^r.   ("–" = no B-cycle with p ≤ 8.)
G0 = 1 table (exact BFS, own/g01.sh, b ≤ 40; (k) = number of e-words): stream 10: b = 2,6,8,14,20,24,26,30,32,36,38;  100: 4(2),7,11(2),20(2),24,35,39(2);  1000: 8(3),20;  10000: 16(2),17(2),18(2);  100000: 32(2);  nothing in base 10.
 So the G0 = 1 exterior cycles that carry all known G=2 certificates (streams 10, 100, 1000, 10000, 100000) exist in bases 2^j, 6, 7, 8, 11, 14, 16–18, 20, 24, 26, 30, 32 but
**not** in 9, 10, 12, 13, 15, 19, 21, 22, 23, 25, 27, 28, 29, 31.  Base 10 has no B-cycle with G0 ≤ 2 and the first ones are p12 (G0=3) and p11 (G0=4).

**3.3 Reduction (CONDITIONAL).**  Suppose (a) the exterior census is as in 3.1/W5 (only p11, p12 and repetitions for p ≤ 21, no cycle for G0 ≤ 5 except those), and (b) PRs #380/#404/#411/#399
are right that p11 and p12 admit no centre for any repetition count k.  Then every base-10 neutral-band certificate lies over an exterior cycle with G0 ≥ 7 (or
one of the capped words), hence Σgam ≥ 8, and p0 ≥ 14 (more precisely ≥ 22 or a capped word).  (b) is checked partially in §5.  W5 (own engine, validated against bauto2; I did not re-run it) reports at cap 3M states, for p = 17..32, no exterior cycle other than repetitions of p11/p12 and a residue of capped (undecided) words (p18:1, p22:3, p23:1, p24:5, p25:2, p26:3, p27:8, p28:12, p29:13, p30:74, p31:116, p32:185 at that time); granting this, a decimal certificate needs a capped word or p ≥ 33 (so G0 ≥ 9 by the density bound p ≤ 4G).

**3.4 The simplest exterior stream, gam-word 10 (G0 = 1, P = 2), in all bases ≤ 71.  [COMPUTED: own/bauto4, exact BFS, never capped, each run < 0.1 s; and Theorem 9]**
 Exterior B-cycle with gam-word 10 EXISTS for b = 2, 6, 8, 14, 20, 24, 26, 30, 32, 36, 38, 44, 48, 50, 54 and for no other b ≤ 60 (absent: all odd b ≤ 71, all b ≡ 1 mod 3 – including 10 –, and the even b = 12, 18, 42, 56, 60).
 * b ≡ 1 mod 3 (so 3 | b-1): excluded by Theorem 9 (needs E ≡ 0 mod 3, i.e. constant e; BFS: never occurs).  This is the reason base 10 has no Σgam=1 exterior cycle with p0=2.
 * All odd b are absent (computed up to 71, BFS runs die at depth 3…69 with ≤ 263 states): no proof known to me.  Even b ≡ 0,2 mod 3 are "random": 15 of 20 up to 60.
 * For b ≥ 24 where it exists, the lowest columns are rigid: B_t[0] = 2b-3 ↔ b-2 (the counter 2-cycle x = 2b-3, κ=1; in base 10 this is 17 ↔ 8, which exists!), B_t[1] = 4 ↔ b+2, B_t[2] = 2b-12 ↔ b-7, B_t[3] = 21 (b ≤ 44) / 22 (b ≥ 48) ↔ b+10 / b+11; the two phases have lengths n, n+1.  Acceptance depth varies wildly (3…42): after ≈ log2 b columns the digits
   leave the regime B_i = α b + β_i with |β_i| ≪ b and the orbit behaves like a random walk that either dies or hits the top closure.
 So even the counter being fine in base 10 (x = 17 ↔ 8) does not help: the obstruction lives in the higher columns and, for this stream, in the mod 3 arithmetic of Theorem 9.
 * The three shortest base-10 streams all die within a handful of columns (exact BFS, own/bauto4 -v): gam-word 10: 9 states, dies at column 3; 100: 6 states, column 3; 1000: 30 states, column 6.  For comparison (BFS ends when the frontier is empty; accepting e-words found on the way): base 11, stream 100: 67 states, ends at depth 10, 2 accepting e-words; base 8, stream 1000: 36 states, depth 11, 3 e-words; base 20, stream 1000: 222 states, depth 22, 1 e-word.
   Death depths for stream 100 over b = 4…40 range from 2 to 40 (accepting bases 4, 7, 11, 20, 24, 35, 39).
 * **Interpretation (CONJECTURE, supported by the stream-10 columns above):** the BFS has two regimes.  In a *rigid* regime the digits are B_i = α_i b + β_i with α_i ∈ {0,1,2} and β_i a fixed integer sequence independent of b (stream 10: β = -3, 4, -12, 21, ≈-43, …, growing roughly like 2^i);
   this regime ends when |β_i| ≈ b (≈ log2 b columns), after which the orbit is "chaotic" and either dies or hits the top closure at random.  A base is therefore doomed for a given stream when the rigid regime is too short, i.e. the integers β_i already exceed the digit range 0..2b-2 before the
   closure can happen: for stream 10 one needs b ≥ 12 for B_3 = 21 (b = 10 has digit range ≤ 18, and indeed dies at column 3).  No rigorous version exists.

---------------------------------------------------------------------------------------------------------------------------
## 4. Arithmetic and real-number structure of exterior cycles

**4.1 Proposition 7 (mod b+1 charge).  [PAPER PROOF; tested scripts/test_charge.py]**  W(B) := val(rev B)+1 = Σ B_i b^{n-1-i} + 1.  For the untrimmed step B ↦ B':
  gam=0 ⇒ W(B') ≡ 2 W(B) (mod b+1);   gam=1 ⇒ W(B') ≡ 0 (mod b+1).
Trimming trailing (b-1)'s multiplies W by b^u ≡ ±1 so it preserves "W ≡ 0".  Hence **in every B-cycle with G ≥ 1, (b+1) | W(B_t) for all t**, i.e. the alternating sum
Σ_i (-1)^{n-1-i} B_i ≡ -1 (mod b+1).
*Proof.*  Write F, R for the forward/backward normalisations of B (Lemma 1).  From val F = val B - e1 b^n and b ≡ -1 (mod b+1): val(rev F) ≡ (-1)^{n-1} val F ≡ val(rev B) + e1 (using the parity of n).  From the backward sweep, exactly, val(rev R) = val(rev B) + (1-e1) - gam b^n = W - e1 - gam b^n.
gam=0: W' = val rev F + val rev R + 1 ≡ val(rev B)+e1 + W - e1 + 1 = 2W.  gam=1: W' = xd + b·val(rev F) + val(rev R) + b^n + 1 with xd = (b-1)(1-e1) ≡ -2(1-e1) gives 0. ∎
(This is the classical "an even-length reverse-and-add result is divisible by b+1" in the language of the template.)  It prunes but does not by itself exclude anything: the
exterior census already encodes it.

**4.1b Theorem 9 (mod b-1 charge and closure).  [PAPER PROOF; tested: scripts/test_mod_bm1.py (146,268 random steps, bases 3..20, 0 violations), test_mod_bm1_cert.py (all 9 known certificates), check_closure.py (388 exterior-cycle witnesses from W1+W2 data, 86 with non-trivial gcd, 0 violations)]**
Let s(B) = Σ_i B_i (plain coefficient sum) and ε = 1 - 2 e1 ∈ {±1}.  For every autonomous B-step (gam = 0 or 1, trimmed or not)
      **s(B') ≡ 2 s(B) + 1 - 2 e1   (mod b-1).**
*Proof.*  Forward sweep: B_i + c_{i-1} = F_i + b c_i gives ΣF = ΣB - e1 - (b-1) Σc_i.  Backward sweep (d_n = 1-e1, d_0 = gam): ΣR = ΣB + (1-e1) - gam - (b-1) Σd_i.
gam=0: B' = F+R so ΣB' ≡ 2ΣB + 1 - 2e1.  gam=1: ΣB' = ΣF + ΣR + 1 + (b-1)(1-e1) ≡ (ΣB - e1) + (ΣB - e1) + 1 (since ΣR ≡ ΣB - e1 when gam=1).  Trimming trailing (b-1)'s changes ΣB by a multiple of b-1. ∎
(Equivalent statement for the whole number: N_{t+1} = N_t + rev N_t ≡ 2 N_t mod b-1, so the pair-word coefficient sum σ_t = 2s(B_t) + s(C_t) (the bands contribute 0) satisfies σ_{t+1} ≡ 2σ_t; subtracting twice the B-law gives the C-law
 s(C_{t+1}) ≡ 2 s(C_t) - 2ε_t (mod b-1).  Both laws verified on every edge of all 9 known certificates.)
**Corollary 9a (closure condition).**  Let an exterior B-cycle have period P (any multiple of the minimal period) and e-word e_0…e_{P-1}; put E = Σ_t e_t 2^{P-1-t} (e_0 most significant).  Iterating the law P times and using Σ_t 2^{P-1-t}(1-2e_t) = (2^P - 1) - 2E:
      (2^P - 1)(s(B_0) + 1) ≡ 2E (mod b-1)   ⟹   **gcd(2^P - 1, b-1) divides E.**
(The gcd is odd, so the factor 2 is irrelevant; the condition is invariant under rotating the cycle since E_{t+1} ≡ 2E_t mod 2^P - 1.)  Same condition for a centre cycle of period P' (C-law), and it is implied for k laps by the condition for one lap, so it adds nothing new for the centre.
**Consequences.**  (1) Base 10 (b-1 = 9): P odd ⟹ no condition; P ≡ 2,4 (mod 6) ⟹ E ≡ 0 (mod 3) i.e. #{t even: e_t=1} ≡ #{t odd: e_t=1} (mod 3); 6 | P ⟹ E ≡ 0 (mod 9).  The p12 cycles (P=12) have E = 2709, 1449, 2394, all ≡ 0 mod 9 (non-trivially satisfied); p11 (P=11) is unconstrained.
(2) A cycle of minimal period 2 (gam-word (10)^r, P = 2) in a base b ≡ 1 (mod 3) must have E ≡ 0 (mod 3), i.e. e constant (E ∈ {0,3}).  Exact BFS finds NO exterior cycle with gam-word 10 for any b ≡ 1 mod 3 up to 71 (in particular b = 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, …), so the law **explains the absence of the Σgam = 1 / p0 = 2 stream in base 10** (modulo the computed fact that e is never constant for this stream; see 3.4).
(3) General form for the G0 = 1 streams 10^{P-1}: if (2^P - 1) | (b - 1) the condition forces E ∈ {0, 2^P - 1}, i.e. constant e.  P=2: b ≡ 1 mod 3; P=3: 7 | b-1 (b = 8, 15, 22, 29, 36, …); P=4: 15 | b-1 (16, 31, …); P=5: 31 | b-1 (32, 63, …); P=6: 63 | b-1 (64, …).
    Table check (own/g01.sh, exact BFS, b ≤ 40): stream 100 absent in 8, 15, 22, 29, 36 (present in 4, 7, 11, 20, 24, 35, 39); 1000 absent in 16, 31 (present in 8, 20); 10000 absent in 32 (present in 16, 17, 18).  No exception found.
    In base 10 (b-1 = 9): only the stream 10 is killed this way; for P = 4 (stream 1000) gcd(15, 9) = 3 so the tight stream only needs E ∈ {0,3,6,9,12,15}.
(4) It does NOT depend on the centre, hence it is a statement about the B-system alone, and it is a genuinely arithmetic reason (order of 2 modulo divisors of b-1) why bases with b-1 divisible by 3 (4, 7, 10, 13, 16, …) are "harder" for even periods; base 10 has b-1 = 9, the most restrictive case (3^2).
(5) For odd b (b-1 even) the law also gives s(B_t) ≡ 1 (mod 2) for all t, and mod 2^k (2^k ∥ b-1) s(B_{t+1}) ≡ Σ_{j<k} 2^j (1 - 2 e_{t-j}) : the digit sum of B mod 2^k is a function of the last k carries.
*Limits.*  This is a necessary condition only; it prunes about 2/3 of the even-period e-words in base 10 but cannot by itself exclude any gam-word.

**4.2 Proposition 8 (scalar recurrence).  [PAPER PROOF; tested exactly with Fractions: scripts/test_scalar.py (bases 3,10,11), scripts/real_dyn.py (p11, p12)]**
Let V(B) = Σ_{i<n} B_i b^{-i} + b^{1-n} (= value of B ++ (b-1)^∞; invariant under trimming).  With forward carries c_i extended by e1 through the band,
κ(B) = Σ_{i≥0} c_i b^{-1-i} ∈ [0, 1/(b-1)]:
   **V(B') = (1 + b^{-gam}) V(B) − (b²−1) κ(B).**
(Interpretation: V = h + ℓ where h = leading-digit real of N, ℓ = low-digit mirror real; h' = V/b^{gam}, ℓ' = V − (b²−1)κ.)  The product of step ratios V_t/h_t over a cycle equals b^G
**identically** (telescoping, h_{t+1} = V_t / b^{gam_t}) – it is a tautology, not a constraint.  Defect (b²−1)κ ∈ [0, b+1] is NOT small, so the "ρ = ℓ/h ≈ 1, 2^p ≈ 10^G"
heuristic is false: in the p11 cycle ρ ranges over 0.34 … 9.05 (ratios V/h from 1.34 to 10.05), in p12 ρ ∈ {0.99, 0.53, 0.93, 0.68} per quarter-period.
Interesting structure (COMPUTED): the p12 cycle is a period-3 orbit of the 4-step return map near a quasi-fixed point (h at t=0,4,8: 5.282, 5.233, 5.244) – the lowest two columns of B
are exactly 4-periodic (10,1,2,5 | 4,5,11,2) and the period-12 twist starts at column 2 (see out2/p12_w.txt; same phenomenon in base 20: the lowest 9 columns of B are 4-periodic).

**4.3 Row/column picture.**  Writing the exterior cycle as the array B_t[k] (k = column = position) the lowest-coefficient counter is column 0; every later column is a function of the previous column's
carries and a guess of the backward carries (bauto's "position automaton").  The expected structure is a "tight" counter 1,2,5,10 for p=4G and a 9↔18 counter for p=2G; BFS state counts explode exactly for
these two extreme families (e.g. (1000)^6: >17M states at depth 16; (10)^8: >2.5M) – these are the capped words of W5's census.  Whether an infinite family (1000)^r or (10)^r can occur is the main
open exterior problem (CONJECTURE: (1000)^r has a B-cycle only for r=3 (and multiples), (10)^r none).

---------------------------------------------------------------------------------------------------------------------------
## 5. The centre: independent check of the "all-k" exclusions for p11 and p12 (Q3)

**5.1 What the PRs claim** (#411 agent-113 required-coefficient construction; #404 agent-111 independent delayed-output construction, both give the same minimal DFA of 13,876 states / 470,714 edges;
#380 agent-111 MDD for k=3; #399 agent-118 for p12 with k even): the layer-by-layer cut languages L_j (alphabet = time-segments of the stream with local carries, words of length 2k) satisfy L_5 = L_6 and the
tails (width 1, 2, odd, even midpoints) are empty, for all k.  #411 additionally has an independent C++ checker verifying T0(L0) ⊆ I, T(I) ⊆ I and the empty tails (13,876-state invariant I).

**5.2 My independent checks (do not use any of their code or model).**
(i) [COMPUTED] own/cfg.cpp: exhaustive forward simulation of the *true* lap map on all trimmed palindromic centres of width ≤ W, written from the Lean mirror definition (nextC, DC, hyp, maximal trim).
    Differential test against the exact mirror: own/difftest.py, 440,000 random single-phase cases (all 11 phases of p11), 0 mismatches.  Positive controls: it finds the known centres in bases 2,4,8,16,32.
    Result (run to completion, 71.8M states each, own/cfg_W12.out): **no centre cycle of the p11 lap map (any repetition count k, any trim schedule via maximal-trim canonical form) with all phase-0 widths ≤ 12**; 46,565 lap-survivors with image ≤ 12, cyclic core empty, no start survives 3 laps (296 survive 2).
    Same for p12 (lap of 12 phases, G=3; cycles of even length only): widths ≤ 12, 65,044 lap-survivors, none survives 3 laps (192 survive 2).
(ii) [COMPUTED] survival statistics (own/surv.cpp): the number of consecutive phases a width-m centre survives (true dynamics, any width) – maximum over all states of width m for the p11 driver:
    m=1..10: 6,10,15,15,17,16,19,19,22,22 phases.  Over a full lap-survivor, nearly all die in the second lap (52,603 survive 1 lap, 24 survive 2, none 3 for m ≤ 10).  Survival grows like ≈1.5·m + O(1):
    a light-cone picture – the outer layers behave like the infinite-width time-periodic "pseudo-solution" and the signal from the fold (centre) reaches the outside in time ∝ m.
    This is consistent with, and a concrete reading of, the PRs' statement that cut languages are non-empty at every depth but the central fold is never satisfiable.
(iii) [COMPUTED] reproduction of the PR computations on this machine with their own code (own/bin/a113_regular, a113_check): #411 engine: p11 NO_CENTERS_ALL_REPETITIONS, j* = 5, per-depth counts 35/83/243/563/755/755 (k=1), 960,601 and 752,450,435 (k=2,3), DFA 13,876 states / 470,714 edges, 127,361,537 ops, 7.6 s, 200 MB;
    their independent checker on the generated invariant (6.6 MB text): VERIFIED_INVARIANT, all 7 obligations PASS, 10,173,487 charged ops, 232,168 peak product states; test_p11_regular.py: 52,550 tuple memberships PASS;
    #404 (agent-111, different implementation): status none, all positive repetitions, j* = 5, 6.2 s; #399 (agent-118, p12): status none, all repetitions all widths, fixed at layer 6, 14 tail checks, peak 19,258 states, 79,132,872 ops, 2.1 s.
    Positive controls with the #411 engine: base 2 (centre width 2), base 4 (width 2), base 26 (width 5) accepted; base 11 (centre width ≈ 42) is out of reach for it (edge cap at depth 14) – undecided there, not a failure.
(iv) [COMPUTED, repo tool] cauto_fast agrees for k=1,2 (p11: none; p12 k=2: none).  Base 11 control: cauto_fast finds the centre for e=011011,g=001001 in 0.1 s at m0 = 42…75.

**5.3 Assessment.**  The all-k, all-width claim rests on (1) the one-layer local relation (taken from `cauto_fast`) – corroborated by my semantic differential test of single phases and by (i) at
all widths ≤ 10–12; (2) the regular-language transducer model – corroborated by their 52,550-tuple exact comparison and by two independent implementations producing the *same* minimal DFA;
(3) the inductive invariant, which is checked by a separate checker.  I found no inconsistency.  What I could **not** do independently: re-derive the transducer (cyclic first/current coefficient closure,
tail layers) from scratch.  Label for the unbounded claim: **PAPER+COMPUTED by the PR authors, corroborated here at widths ≤ 10 (≤12 pending) for all k; not Lean-verified.**

---------------------------------------------------------------------------------------------------------------------------
## 6. Centres versus exterior cycles in other bases (Q2, Q5)

**6.1** Even where exterior cycles are plentiful, centres are rare.  [COMPUTED: scripts/q2b.py, q2d.py with cauto_fast, all widths; out2/q2d_all.txt]
 base 4: exterior g=100 has two B-cycles (e=100 and e=010): only e=100 has a centre (k=2); e=010 none for k=2,4;  g=101100 (p0=6, G0=3): none for k=2.
 base 8: g=1000: e=1000 centre (k=2); e=0100, e=0110: none for k=2,4; g=10, e=01: none k=2,4.   base 7: g=100: none (k=2,4).   base 6: g=10 (p0=2), (10)^r: none.   base 14: (10)^r: none.
 base 11: g=100: e=101 centre at k=2 (the known certificate; widths 42…75), e=100 none for k=2,4,6; g=11000 (G0=2): none for k=1,2; (10)^3 (G0=3) k=2: undecided (cauto_fast timeout).
 **6.1b Status of the all-k batch (Q2e).**  The queued heavy job (PR #411 engine over every primitive exterior (g,e), p ≤ 8, 16 bases: scripts/q2e_batch.sh, ready to run, ≈ 25 min) starved twice in the heavy lottery (8 waiters, killed at the 30-min background limit) and did NOT run.
 Light-cap substitute (scripts/q2e_light.py, 12 s / 700 MB per call, out2/q2e_light_*.txt): base 16 g=10000 e=10000 (the known certificate) accepted (centre width 2); all other cases in bases 6, 11, 14, 16 hit the state/edge caps (UNDECIDED, not "none").  So the Q2 table above rests on cauto_fast (k ≤ 6) and the earlier engine runs in bases 4, 8 only.
 → Σgam=4 or 6 *primitive* centres were not found in any of these (repetition of a Σgam=2 certificate trivially gives Σgam=4,6, but no new ones).  (See out2/q2d_all.txt for the full list when finished.)
**6.2 Base 20 vs base 10 (Q5).**  The PR #356 certificate: p=8, E=01001011, G=00010001 (Σgam=2, G0=2), Σu=2, Σv=1; |B| = 90/91, |C| = 25..27; the lowest 9 coefficients of B_t are 4-periodic
(B_t[i] = B_{t+4}[i], i ≤ 8) and the half-period twist (complemented E) appears above them.  In base 10 the analogous stream (1000)^2 has **no exterior cycle** (G=2 census), and the nearest
exterior cycles (p12=(1000)^3: columns 0,1 exactly 4-periodic, twist from column 2) are not G0 ≤ 2.  The base-20 centre has width ≈ B/3.5, base 11's centre is 42..43 wide with |B| only 7.

---------------------------------------------------------------------------------------------------------------------------
## 7. What is proved, what is not (summary for the coordinator)

* PAPER PROOF (+tests): decoupling/two-sweep form; centre rules; parity twist (explains the squares); 2G ≤ p ≤ L·G; mod-(b+1) lemma; **mod-(b-1) charge law and closure condition gcd(2^P-1,b-1) | E (Theorem 9; explains why the Σgam=1, p0=2 exterior stream is absent in base 10 and in every b ≡ 1 mod 3, and constrains every even-period exterior e-word in base 10 mod 3 / mod 9)**; scalar recurrence; tautology of the ratio product; refutation of the ρ≈1 heuristic.
* COMPUTED: exact exterior census (G ≤ 5 complete, G = 6 minus (1000)^6); realisable-stream counts; small-stream table over bases; brute-force centre exclusion for p11/p12 (all repetition counts) with phase-0 widths ≤ 12; reproduction of the PR #411/#404/#399 numbers; stream-10 table over b ≤ 71.
* CONDITIONAL REDUCTION: if the PR claims hold, a base-10 certificate needs an exterior cycle with Σgam over a period ≥ 7 (so Σgam ≥ 8) – see §3.3.
* UNDECIDED: (1000)^r and (10)^r families for r ≥ 4 / r ≥ 5; exterior streams p ≥ 25; unbounded-width centres beyond the PRs' own proof.
* CONJECTURE: tight (1000)^r exterior cycles exist only for 3 | r; no (10)^r.
