# S37: finite-window pumping for a cyclic seam family

**Label: PAPER PROOF, conditional all-width lemma.** This is not a decimal Lychrel certificate. No physical T* seam has passed the complete endpoint-return conditions.

## Theorem

Fix integers `Q >= 2`, `K >= 2d`, and `d >= 1`. Let `B,W,U` be fixed coefficient words, with `B[0] > 0`, `|W|=9`, `|U|=3`, and all coefficients in `0..18`. For each residue `r` modulo `d`, let `J_r,C_r` be finite words, with all `J_r` having one common length and all `C_r` having one common length. Each `C_r` is palindromic; if it has odd length, its midpoint coefficient is even. Define

`P(q,k) = H(q,k) ++ C_(k mod d) ++ reverse(H(q,k))`,

`H(q,k) = B ++ W^q ++ J_(k mod d) ++ U^k`.

Choose interior lower-half cuts `a_W = |B| + i_W |W|` and `a_U = |B| + Q|W| + |J_r| + i_U |U|`, with `0 < i_W < Q` and `0 < i_U < K`. At each cut, the reflected upper cut at phase `t` is `b_t = |P_t| - a`.

For each `j=0,...,d-1`, run the **exact 120-step ordinary decimal orbit** from `P(Q,K+j)`. Require:

1. The complete endpoint pairword is exactly `P(Q,K+j+5)`, including all exterior, junction, centre, length and phase data. Its overflow clock is the required rooted clock `1000` repeated 30 times.
2. Every phase input pairword has at least one odd coefficient. Such a coefficient certifies nonpalindromicity.
3. At both cuts, for every one of the 120 phase transitions, the inserted block and its reversal return their incoming carries to themselves. If that phase has overflow `gamma=1`, also require the exact lag digit equality `D[b_t] = H[0]`, where `D` is the normalized digit word and `H` is the normalized `reverse(V)` block at its actual high-side carry. Propagate the inserted word by `V'[i]=L[i]+H[m-1-i]` when `gamma=0`, and `V'[i]=L[i]+H[(-i) mod m]` when `gamma=1`. At phase 120 the propagated `W` block must equal `W`, and the propagated `U^d` block must equal `U^d`.

Then, for **all independent integers** `q >= Q` and `k >= K`, the exact 120-step pairword return `P(q,k) -> P(q,k+5)` holds, the overflow clock is unchanged, and every intermediate phase is nonpalindromic. In particular, any canonical positive source realizing `P(Q,K)` has a palindrome-free ordinary orbit for all time. The finite window is exactly `q=Q`, `k=K,...,K+d-1`; the carry-port hypotheses, not adjacent width samples, justify extrapolation.

## Proof

Let `F(P)` be the pairword of the decimal digits obtained by normalizing the coefficient word `P`. For a canonical symmetric pairword of a positive integer `n`, `F(P)` is exactly the pairword of `n + reverse(n)`.

**Two-cut insertion lemma.** Let `P` be a symmetric coefficient word of length `n`, and insert `r` copies of a word `V` at a lower cut `a` and `r` copies of `reverse(V)` at its mirror cut `b=n-a`. Write `D=norm(P)`, and let `c_a,c_b` be the carries entering the two cuts. If normalizing `V` from `c_a` exits with carry `c_a`, and normalizing `reverse(V)` from `c_b` exits with carry `c_b`, then these repeated insertions do not change the normalized digits outside the inserted blocks or either terminal overflow. This follows by the deterministic schoolbook carry recurrence, copy by copy.

If `gamma=0`, the mirrored partner of lower inserted digit `L[i]` is `H[m-1-i]`. If `gamma=1`, the normalized word has one extra leading digit, so the first lower inserted digit is paired with the original upper seam digit `D[b]`; the equality `D[b]=H[0]` is exactly what makes the shifted pairword insertion valid. The remaining partners are `H[(-i) mod m]`. Thus `F` maps the inserted copies to copies of the displayed successor block `V'`. These conditions are sufficient for every integer `r>=0`, not merely a bounded number of insertions. Distinct nonoverlapping symmetric cuts compose: a carry-resetting insertion leaves the carry entering the other cut unchanged, and each `gamma=1` lag equality is unchanged as a digit value when its index shifts.

Apply the lemma at both cuts at each of the 120 phases. The propagated inserted words return to `W` and `U^d` after 120 phases, so arbitrary insertions of `W` and `U^d` commute with the whole 120-step edge and with its endpoint equality. Hence the edge checked at `q=Q,k=K+j` also holds for every `q=Q+x,k=K+j+dy`, for arbitrary `x,y>=0`. The `d` representatives cover all `k>=K`; the seam phase is unchanged by adding `d` to `k`, and the checked endpoint already uses the correct phase `(k+5) mod d`. This proves the universal return.

The source guards make every `P(q,k)` a canonical positive pairword. Every pumped intermediate phase retains all coefficients of its base phase outside the inserted intervals, so a base odd coefficient remains an odd coefficient after pumping. Therefore no intermediate state is a palindrome. Repeating the 120-step return increases `k` by five forever, proving the conditional all-time conclusion.

## Executable checker and scope

`calculation/new_structures/S37/pump_window.py` implements the exact finite-window checker, including independent Python-big-integer replay at every phase, both carry ports, overflow-one lag checks, endpoint equality, and odd-coefficient guards. It refuses to certify a candidate when any hypothesis fails. `test_ports.py` runs 40,000 deterministic random local controls for the insertion identity; this is a regression test, not a substitute for the proof above. Run `bash calculation/new_structures/S37/run_checks.sh`.

The finite checker has so far rejected tested near-miss seams because their complete 120-step endpoint pairwords fail to return. Consequently this theorem closes the **conditional cyclic-seam pumping step**, but does not supply the missing physical regenerative seam and does not establish decimal Lychrel existence.
