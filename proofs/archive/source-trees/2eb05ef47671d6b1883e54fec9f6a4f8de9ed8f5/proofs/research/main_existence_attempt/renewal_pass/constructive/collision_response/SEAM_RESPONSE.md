# Arbitrary-block seam response after finite spacer exhaustion

This is an exact one-update theorem at a zero-gap collision. It extends the earlier high-reset-only seam formula to arbitrary coefficient blocks, including blocks consisting entirely of 9s and unequal isolated overflow clocks. It supplies no recurrent reset and no finite decimal Lychrel witness.

It builds on the external contribution `proofs/contributions/2026-10-14-overlap-gate/SEPARATION_EXHAUSTION.md`, published in commit `b7fa911dc4ca943528f5d28b67f3fbd87c9404ca`, and on the existing arbitrary-motif separation theorem in `main_existence_attempt/return_pass/collision/STATUS.md`. The external stream retains ownership of the remaining `(1,7)` collision/reset search; this note supplies reusable exact algebra.

## 1. Definitions, including the all-9 boundary

All words are low-to-high. Let `W_1,...,W_m` be nonempty words over 0,...,18, with lengths `a_j`, starts `s_1=0`, `s_j=sum_{i<j}a_i`, and total width L. No symmetry is needed for the digit identity.

Normalize each block with incoming carry 0. Let `h_j` be its outgoing carry and let `E_j(x)` be its normalized digit polynomial **including** the terminal digit `h_j*x^(a_j)`. Retain its a_j original columns even if their final coefficients are zero. Define:

* `ell_j`: the number of initial coefficients equal to 9, allowing `ell_j=a_j`;
* `t_j=1` exactly when the whole block consists of 9s;
* `S_ell(x)=1+x+...+x^(ell−1)`, with `S_0=0`.

Each block's incoming-carry transfer is exactly

\[
F_j(c)=h_j+t_jc,\qquad c\in\{0,1\}.
\]

Here `h_j*t_j=0`: an all-9 block has isolated final carry zero and transmits its incoming carry; every other block resets to the same final carry for both inputs. Put

\[
c_1=0,\quad c_{j+1}=F_j(c_j),\quad\gamma=c_{m+1}.
\]

Thus gamma is the **actual** final carry of the concatenation. It must not be replaced by the isolated carry of the last block.

## 2. Universal digit and pair-word identities

Define the raw placed isolated digits and the seam carry-difference mask by

\[
E(x)=\sum_{j=1}^m x^{s_j}E_j(x),\qquad
K(x)=\sum_{j=2}^m c_jx^{s_j}S_{\ell_j}(x).
\]

The actual normalized whole digit polynomial is exactly

\[
\boxed{D(x)=E(x)+(x-10)K(x).} \tag{1}
\]

This includes every shared column, every all-9 block, and the actual terminal digit. E is a raw polynomial sum; a coefficient of E may equal 10 and is not silently normalized.

If the whole concatenation is canonical, its output width is `L+gamma`. Set `d=L+gamma−1` and `rev_d(P)=x^dP(1/x)`. Its next pair word is

\[
\boxed{G(W_1\cdots W_m)=E+\operatorname{rev}_d E
 +(x-10)K+\operatorname{rev}_d((x-10)K).} \tag{2}
\]

**Proof.** At one column, a coefficient <=8 resets both incoming carries to 0; a coefficient >=10 resets both to 1; a coefficient 9 preserves their difference. Therefore actual and isolated outgoing carries differ by the incoming bit precisely on the initial 9-run of the block, and nowhere else. This remains true when the entire block is 9: then the difference persists through its final outgoing carry.

For any coefficient word W, let C(W) record its outgoing carry after each original column, at that column's exponent. The exact telescoping normalization identity is `N(W)=W+(x−10)C(W)`, including its terminal carry. The preceding local observation gives

\[
C(W_1\cdots W_m)-\sum_jx^{s_j}C(W_j)=K.
\]

Subtracting the isolated normalization identities gives (1). Pairing under the actual final width gives (2). No zero gap, reset hypothesis, equal clock, or bounded initial 9-run was used. QED.

For comparison with component pair maps, suppose additionally that each block is symmetric and the list is reflection symmetric. Define the common-clock expression

\[
\mathcal F_\gamma(W)=E_W+x^{|W|+\gamma-1}E_W(1/x).
\]

Then `E+rev_d(E)=sum_j x^(s_j) F_gamma(W_j)`. If the isolated carry of W equals gamma, this is its ordinary G(W). When clocks differ it is **not** G(W): for isolated carry 1 and gamma 0 the local expression includes a term at exponent −1. Internal placement restores its correct whole-word position. Equivalently, (2) can be used directly without any Laurent local expression.

This clock alignment is a separate issue from the 9-run correction. For example, B=(10,10), H=(2) has K=0 at the collision BHB, but the central block must be paired with whole clock 1. The actual next word is `(1,2,3,3,2,1)`. Substituting the isolated center update G(H) instead gives an incorrect placement.

## 3. Complete three-block collision formula

At a separated-family collision write `C=B H B`, with canonical symmetric B,H of widths b,m. Let isolated final carries be e,h; initial 9-run lengths be ell_B,ell_H; and all-9 indicators be t_B,t_H. Then

\[
c_H=e,\qquad c_{B,\mathrm{right}}=h+t_He,
\qquad\gamma=e+t_B(h+t_He),
\]

and

\[
\boxed{
E=(1+x^{b+m})E_B+x^bE_H,\qquad
K=e x^bS_{\ell_H}+(h+t_He)x^{b+m}S_{\ell_B}.
} \tag{3}
\]

Together with (1) and (2), this is the exact first post-collision update. If B is not all 9, gamma=e. If B is all 9, e=0 and gamma=h. These are exhaustive cases, not an assumed clock agreement.

The all-9 boundary is substantive. Take `B=(9,9)`, `H=(18)`. Then e=0, h=1, gamma=1, `K=x³+x⁴`, and

```
E=(9,9,8,10,9),
D=(9,9,8,0,0,1),
G(BHB)=(10,9,8,8,9,10).
```

The leading digit in D is created by the seam correction. Using gamma=e would give the wrong output width.

## 4. Exact consequences, rather than a presumed reset

Let `M(P)=P(1)` denote coefficient mass. In the next formula, G(W_j) means formal pairing of the isolated normalized digits at their prescribed width `a_j+h_j`. For a canonical individual block this is its ordinary component update; for arbitrary nonsymmetric blocks or blocks with zero end coefficients it is only this formal pairing, not an assertion about an ordinary component orbit. Since K has nonnegative coefficients,

\[
\boxed{M(G(W_1\cdots W_m))
=\sum_jM(G(W_j))-18\sum_{j\ge2}c_j\ell_j.} \tag{4}
\]

Consequently the common-clock independent pair expression `R=E+rev_d(E)` is exact **if and only if** K=0, equivalently every motif entered with carry 1 has initial 9-run length zero. If K is nonzero, its pair correction has strictly negative mass and cannot cancel with its reflection. This is an all-word iff criterion; it does not assume fixed repair radius.

For BHB, the mass loss is precisely `18*(e*ell_H+(h+t_H*e)*ell_B)`. The correction has support only in each active initial 9-run and the immediately following column, plus their whole-word reflections. An all-9 block passes the carry into the next block; the recurrence for c handles arbitrarily many such blocks.

There is a realizable positive safety consequence: **K nonzero alone implies that the next ordinary output is nonpalindromic**, whenever the whole input is a canonical pair word. A palindrome predecessor has either all coefficients at most 9, or only coefficients 0 and 11 with outside coefficient 11. The former class never generates an incoming carry; the latter has no initial-nine run. Either therefore forces K=0 under every partition. The example 99900 -> 100899 above instantiates the contrapositive. The [full Lean bridge](../../lean/raw_symmetry/RawSymmetryObstruction.lean), theorem `numeric_nonzero_defect_safe`, proves this for actual ordinary decimal steps. It supplies one safe step, with no assertion that an active seam regenerates indefinitely.

The initially considered safety shortcut, symmetric E with nonzero K, has now been proved **impossible on the canonical whole-pair-word domain, under every block partition**. The independent [raw-symmetry proof](../../seam_audit/METHOD_AND_PROOF.md) establishes the stronger equivalence: E is symmetric in the actual output width if and only if D is palindromic, and either condition forces K=0. Without overflow the whole coefficients are all at most 9; with overflow they are all 0 or 11, with outer coefficient 11. Thus raw E symmetry identifies the palindrome-predecessor class and cannot certify safety at a canonical collision.

The conditional algebraic implication itself is valid for nonsymmetric coefficient inputs, and two such examples are retained by the audit. Its premise has no instance in the intended canonical domain. The exact earlier uninstantiated proposal is preserved in [the report snapshot](../../seam_audit/source_SEAM_RESPONSE_snapshot.md); the main seam identity and mass criterion above do not use it. The independent audit replays every original control and every partition of every canonical whole word of widths one through five, with 58,221 complete partition records. The unrestricted result follows from the written all-width proof, not from this finite census.

## 5. Application to the externally proved (1,7) exhaustion theorem

The external separated representation starts with

`B_0=(1,1), H_0=(1,8,14,8,1), g_0=r−1`.

For r>=2 it reaches an exact zero gap by its proved time `tau(r)<=4r−3`. At that time use its actual finite blocks `B_tau,H_tau` in (3). Equations (1)–(3) then determine `G^(tau+1)(Q_r)` exactly, including the actual final clock and every seam interaction. For r=1 the same formula applies directly at time zero.

This is a rigorous bridge from the external separation theorem to coupled collision dynamics. The blocks and K are finite, but their subsequent evolution is not shown to close under a finite substitution or a parameter-reset map. Controlling those later coupled states remains the external stream's open recurrence task.

## Verification and formalization scope

`seam_response.py` is the complete deterministic control program and writes `seam_response.json`. Its checks compare (1) with ordinary integer evaluation and decimal conversion, and (2) with ordinary integer reverse-and-add on a canonical realization. It includes exhaustive short three-block cases, deterministic arbitrary finite lists with all-9 blocks, and the two mixed-clock examples above. Finite controls audit the formulas; the proof is the arbitrary-word carry argument.

The sibling [IncomingCarrySensitivity.lean](../../lean/incoming_carry/IncomingCarrySensitivity.lean) supplies independently compiled local sensitivity and suffix-translation lemmas, including `actual_block_outgoing_run` and `actual_block_output_defect`. Its fresh audit is tracked by the formalization branch. This note does not claim that the polynomial seam theorem itself has been compiled in Lean.

The completed control record contains 2,737 cases: 729 exhaustive short BHB partitions, 1,000 arbitrary lists, 1,000 symmetric lists, five arbitrarily chosen long all-9-chain boundary examples, and three named mixed-clock examples. There are 1,767 canonical ordinary-integer controls and 645 nonzero-correction cases. The conditional symmetric-E/nonzero-K antecedent occurs in 0 recorded cases. Every input and response is retained in `seam_response_cases.json.gz` (123,244 bytes), with the full content hash in `seam_response.json`.
