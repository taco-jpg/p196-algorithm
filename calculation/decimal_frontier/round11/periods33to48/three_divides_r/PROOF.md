# Clock (0001)^r exteriors: 3 | r for every r (proved); "only N12" for 3 | r (open)

Directory: this folder (everything cited below is in it; repo read-only, unchanged).

**Status in one line.** The proposition is proved for every r with 3 ∤ r: there is no exterior, so it holds vacuously. That part is uniform in r and is labelled COMPUTED + PAPER PROOF. For r = 3 it is COMPUTED. For r = 6 it is COMPUTED by others (ReachDisk, premise (B)). For r = 3k with k ≥ 3 it is **UNDECIDED**.

---------------------------------------------------------------------------------------------------------------------------
## 0. Precise statement

*System.* This is the Agent120 exterior map in base 10 (`calculation/neutral_band_search.py`). It maps B ↦ Φ(B) = nextB(B, ·) with e2 = 1 − e1, and then trims trailing 9s. Only e2 enters nextB, so Φ depends on B alone (THEORY Lemma 1). B is a coefficient list over 0..18 with B[0] ≠ 0. The overflow bit is gam(B) ∈ {0,1}. The mirror is in `mirror1000.py`: a one-coefficient centre [0] or [10] realises e2 = 1 − e1.

*Exterior with clock (0001)^r.* This is a sequence B_0, …, B_{4r−1} with Φ(B_t) = B_{t+1}, B_{4r} = B_0, and, after rotating time, gam(B_t) = 1 exactly when t ≡ 3 (mod 4). Equivalently it is a B-cycle with overflow word g = (0001)^r, which is the `bx` notion of EXTERIOR.md; "left-end clock (1000)^r" is the same class read in the other direction. The widths |B_t| may vary with t, and no width bound is assumed.

*N12.* N12 is the unique B-cycle with g = (0001)^3 (`n12_wit.txt`, widths 51..53, e = 101101010010). Its three rotations by 4 steps have e = 101101010010 / 010100101011 / 001010110101.

*N12 repetition.* (B_t) is periodic in t with period 12 and equals a rotation of N12. This forces 3 | r.

**Proposition P(r).** Every exterior with clock (0001)^r is an N12 repetition. No congruence on r is assumed. For 3 ∤ r, P(r) says that no such exterior exists.

---------------------------------------------------------------------------------------------------------------------------
## 1. Theorem A (all r): an exterior with clock (0001)^r forces 3 | r

**Label: PAPER PROOF (Lemmas A1–A4) + COMPUTED (A5: an exhaustive finite-graph computation with no caps, done by two independent implementations).**

*K-head graph G_K (pattern 0001).* This is the graph of EXTERIOR.md §2.5 and repo `py/khead_family.py`.
- Nodes are (x, φ) with x = (x_0..x_{K−1}), x_0 ∈ 1..18, x_i ∈ 0..18, and φ ∈ Z/4.
- For each h ∈ {0,1}, let (y, g) = trans(x, h) and keep the edge (x, φ) → (y, φ+1) when g = pat[φ], with pat = 0001.
- trans uses backward carries H_K = h, H_i = ⌊(x_i + H_{i+1})/10⌋, gives g = H_0, and uses forward carries L_0 = 0, L_{i+1} = ⌊(x_i + L_i)/10⌋. The output is y_i = (x_i + L_i) mod 10 + [g=0: (x_i + H_{i+1}) mod 10; g=1: 1 if i = 0, else (x_{i−1} + H_i) mod 10].

**Lemma A1 (padding). PAPER PROOF.** For any B, Φ(B ++ [9]) = Φ(B) up to trailing 9s, and gam and e1 are unchanged.
- A 9 on top passes the forward carry: (9 + e1) gives carry e1, so e1 is unchanged.
- It also passes the backward carry: d = ⌊(9 + 1 − e1)/10⌋ = 1 − e1. So every F_i, R_i (i < n) and gam = d_0 is unchanged.
- The new top coefficients are 9:
  - gam = 0: F_n + R_n = ((9 + e1) mod 10) + ((10 − e1) mod 10) = 9.
  - gam = 1: F_n = 9(1 − e1) = xd, so position n equals the old top xd + R_{n−1}. The new position n+1 is xd + R_n = 9(1 − e1) + ((10 − e1) mod 10) = 9.
- This is THEORY §1.3(c). Check (`check_khead_trans.py`): 20,000 random words plus N12, 0 mismatches.

**Lemma A2 (K-head restriction). PAPER PROOF.** Let B be padded with 9s to width ≥ K, and let h = d_K be the backward carry into position K−1 (d_n = 1 − e1, d_i = ⌊(B_i + d_{i+1})/10⌋). Then trans(B[0..K−1], h) = (Φ(B)[0..K−1], gam(B)), where Φ(B) is also padded.
- Proof: this is the two-sweep form of THEORY Lemma 1 (B'_i = F_i + R_i, or F_0 + 1 and F_i + R_{i−1} when gam = 1). Here F_i needs B_0..B_i and the forward carries (L). R_i = (B_i + d_{i+1}) mod 10, and d_{i+1} for i < K is a function of B_{i+1..K−1} and d_K (H).
- Check (`check_khead_trans.py` → `check_khead_trans.out`): 477,915 (B, K) pairs with K ≤ width and 808,047 padded pairs with K up to width + 11, against the exact mirror. **0 mismatches.**

*Consequence.* Let (B_t) be an exterior with clock (0001)^r. Pad every B_t with 9s to a common width ≥ K. By A1 and A2, t ↦ (B_t[0..K−1], t mod 4) is a closed walk of length 4r in G_K, for every K ≥ 1.

**Lemma A3 (projection). PAPER PROOF.** If (x, φ) → (y, φ+1) is an edge of G_{K+1} with bit h, then (x[0..K−1], φ) → (y[0..K−1], φ+1) is an edge of G_K with bit h' = ⌊(x_K + h)/10⌋. This holds because trans computes H downward, and y_i for i < K uses only x_{0..K−1}, L_{0..K−1} and H_{0..K}, with H_K = h'.

**Lemma A4 (filter). PAPER PROOF.** Define S_1 = all nodes of G_1. Define S_K as the nodes of the subgraph of G_K on S_{K−1} × {0..18} that lie in a cyclic SCC whose period (the gcd of its cycle lengths) is **not** divisible by 12. Then every closed walk in G_K of length L with 12 ∤ L lies in S_K.
- Induction on K: the projection of the walk (A3) is a closed walk of the same length, so it lies in S_{K−1}. The walk itself therefore lies in the candidate subgraph, inside one cyclic SCC of period q with q | L, so 12 ∤ q.

**A5 (computation). COMPUTED, exhaustive, no caps.** S_37 = ∅. The node counts |S_K| for K = 1..37 are:

4, 11, 62, 161, 332, 775, 2011, 7879, 22806, 68609, 207157, 4963, 8501, 20667, 37914, 63442, 110878, 169595, 195440, 118904, **56814 (K=21: SCC periods 76, 76, 152)**, 66240, …, 1162041 (K=30), …, 9494, 333, **0 (K=37)**.

- **Implementation 1:** `khead4.cpp`, run as `./khead4 40 0001 -1 12 1` → `khead4_0001_not12.out`. It uses C++, string keys and an iterative Tarjan SCC.
- **Implementation 2:** `khead_not12_np.py`, run as `python3 khead_not12_np.py 40 0001 12` → `khead_not12_np.out`. It uses numpy-vectorised trans, sorted void keys, scipy strong components and BFS periods.
- **The two outputs agree at every K.** Unfiltered, khead4 reproduces the repo's K-head counts 4, 11, 62, 161, 332, 795, 2011, 7879, 23243 (EXTERIOR §2.5) in `khead4_0001.out`, which also gives the full graph up to K = 15.
- **Controls** (`controls.out`, same code):
  - Positive: base 11, pattern 001, MOD 2, and base 26, pattern 10, MOD 4. Both bases have real exteriors of odd/short period, and their families survive through K = 14 and K = 7 respectively (stopped for memory).
  - Negative: base 10, pattern 01, MOD 8 dies at K = 3. This matches the repo theorem "2G = p ⇒ 8 | p".
- **Consistency with bx** (`bx_small_r.out`, my build of repo `src/bx.cpp`): (0001)^r is EXHAUSTED for r = 1, 2, 4, 5, 7, 8. The BFS dies at depths 6, 13, 13, 6, 10, 13.

**Theorem A.** If an exterior with clock (0001)^r exists, then 3 | r.

*Proof.* The exterior gives a closed walk of length 4r in G_37 (consequence of A1 and A2). If 12 ∤ 4r, A4 puts this walk in S_37, and S_37 = ∅ by A5. Hence 12 | 4r. ∎

**Corollary.** P(r) holds for every r ≢ 0 (mod 3).
- For chain 1, the branches r ≡ 1 and r ≡ 2 (mod 3) close for all r. They no longer need r ≥ 19 or r ≥ 38.
- The "19" is visible in the data: for 21 ≤ K ≤ 36, every surviving non-12 SCC has period 76 = 4·19 or 152. So up to 36 heads only 19 | r was possible (r = 19 ≡ 1, r = 38 ≡ 2). This matches the known thresholds. The family dies at K = 37.

---------------------------------------------------------------------------------------------------------------------------
## 2. The case 3 | r

- **P(3): COMPUTED** (`bx_r3.out`). `bx 10 -g 000100010001 -nosym` gives ACCEPT with exactly the three e-words above, at width 53, BFS saturated at depth 71. `-count 75 -nosym` gives exactly one B-history per e at every depth ≥ 53. So the only exteriors are the three 4-step rotations of N12.
- **P(6): COMPUTED by others, not re-run here.** ReachDisk §1/§2 has clock 0001, T = 24 COMPLETE with 6.6·10^9 orbits and height 1346: only N12 twice. This holds under its premise (B) (reach ≡ Agent120 exterior). Here `bx` alone is capped (EXTERIOR: 40M states, width ≤ 46).
- **P(9), P(12), … : UNDECIDED.** ReachDisk at P = 48 is only a backward cone to the port-word targets, not an exterior census, so it does not establish P(12). P = 36 is not covered by any complete run I found.

**Why the method of §1 cannot finish 3 | r (a barrier, not a proof).**
- N12 padded with 9s is a closed walk of length 12 in G_K for every K. So any "period-not-divisible-by-M" filter must stop at M = 12.
- Non-N12 walks of length 12k are numerous at large K. The full graph has an SCC of period 12 with 12.2M nodes at K = 15 (`khead4_0001.out`). For k = 2, new cut states appear up to depth 1346 (ReachDisk), and up to depth ≥ 46 in `bx`. So no small-K argument separates N12^k from other length-12k walks. Any proof must use the top boundary (acceptance / closure of the whole width).

**Exact missing lemma (UNDECIDED).** For k ≥ 3, Φ^12 restricted to the domain where the clock is (0001)^3 has no periodic orbit of length k other than the fixed points N12 (three rotations).

One reduction is available (PAPER PROOF, elementary, unused). Take the first spatial cut j at which the cut word of the exterior stops being 12-periodic. The cut word at j−1 is u^k, where u is a cut state reachable for P = 12 (bx: 136,653 states in the non-quotiented run). So every counterexample "desynchronises" from one of these finitely many states u. However, the continuation from u^k is again the full P = 12k search, so this gives no finite reduction yet.

---------------------------------------------------------------------------------------------------------------------------
## 3. Side note (tool bug, small)

For g = (0001)^3, `bx -w` prints a witness that is **not** a B-cycle under the mirror with `-first`, with `-first -nosym`, and with default flags. Only `-w -nosym` gives the correct N12. The p11 witness is correct in all modes. ACCEPT and EXHAUSTED verdicts are unaffected. However, repo `py/verify_ext.py` uses `-first`, so it would report FAILED on p12.

## 4. Files

| file | content |
|---|---|
| `mirror1000.py` | exterior map Φ (imports the repo mirror), padding check |
| `check_khead_trans.py` / `.out` | Lemma A1/A2 checks, 0 mismatches |
| `khead4.cpp`, `khead4_0001.out`, `khead4_0001_not12.out` | full graph K ≤ 15; filtered run, dies at K=37 |
| `khead_not12_np.py`, `khead_not12_np.out` | independent implementation, identical counts, dies at K=37 |
| `controls.out` | positive (base 11, 26) and negative (base 10, (01)) controls |
| `bx_small_r.out`, `bx_r3.out`, `n12_wit.txt` | bx runs r = 1, 2, 4, 5, 7, 8 (EXHAUSTED); r = 3 (N12 only, 1 history per e); the N12 witness |
| `d12/khead_dump.txt` | K=12 node dump with SCC id and period |
