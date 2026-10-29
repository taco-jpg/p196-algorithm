# Q05: Rooted T* renewal obstruction unification

**Label: PAPER PROOF (necessary-condition theorem).** This is not a decimal Lychrel certificate, a global no-go, or a claim that the T* search is exhausted.

**Exact missing-lemma contribution:** the T* finite-interface return graph must carry centre-length parity as a state, with parity toggling exactly on each physical overflow; consequently every fixed-centre-length-per-phase 120-step route is impossible.

## 1. Target and definitions

Use the rooted phase-indexed T* family from docs/FOCUS_SWARM.md:

\[
P_t=H_t\,C_t\,H_t^R,\qquad
H_t=B_t\,W_t^{q_t}\,J_t\,U_t^{k_t},
\]

where \(|B_t|=34\), \(|W_t|=9\), \(|U_t|=3\), \(C_t=C_t^R\), and every \(P_t\) is the canonical pair-coefficient word of a positive decimal integer. The phase rows \(B_t,W_t,U_t\) may change in content, but their lengths remain fixed. Let \(\gamma_t\in\{0,1\}\) be the **actual** overflow of the ordinary decimal addition \(n_{t+1}=n_t+\operatorname{rev}_{10}(n_t)\), not a freely assigned label.

The target macro has 120 steps and overflow word
\[
g=(100010001000)^{10},
\]
so \(\sum_{t=0}^{119}\gamma_t=30\).

## 2. New theorem: the centre-parity cocycle

**Theorem.** For every exact physical T* edge whose source and target both have the displayed template form,

\[
\boxed{\gamma_t=
18(q_{t+1}-q_t)
+2(|J_{t+1}|-|J_t|)
+6(k_{t+1}-k_t)
+(|C_{t+1}|-|C_t|).}
\tag{1}
\]

Consequently,
\[
\boxed{|C_{t+1}|\equiv |C_t|+\gamma_t\pmod 2.}
\tag{2}
\]

In particular, the centre-length parity is not a free search bit: it flips on every overflow phase and stays unchanged on every non-overflow phase. Over one T* macro it flips exactly 30 times and returns to its initial parity. Any proposed edge path that keeps the centre length (or even just its parity) fixed at every phase is impossible.

**Proof.** The template length is
\[
L_t=2(34+9q_t+|J_t|+3k_t)+|C_t|.
\]
For a canonical positive decimal integer, adding its reversal increases the digit length by exactly the actual final carry: \(L_{t+1}-L_t=\gamma_t\). Subtract the two displayed expressions for \(L\) to obtain (1). Every term except \(|C_{t+1}|-|C_t|\) is even, giving (2). The 120-bit clock has a one exactly at phases \(t\equiv0\pmod4\), hence exactly 30 parity flips. No assumption about the coefficient values in \(J_t,C_t\), the U3 rotation, or a chosen carry schedule is used. \(\square\)

## 3. Unified necessary-condition theorem

The following are simultaneous obligations on any proposed all-time T* cycle. They unify the repository's five broad obstruction families without pretending that any one obstruction rules out every possible template.

1. **Run drift.** Every unbounded run-length coordinate must have nonnegative net drift over a closed macro, and at least one coordinate must grow. A negative coordinate eventually falls below any fixed admissibility threshold under repeated cycling. This is the strict-drift obstruction in reports/REPORT_208.md and reports/REPORT_218.md.

2. **Physical, not guessed, carries.** Decimal carry across coefficient \(x\) is \(T_x(c)=\lfloor(x+c)/10\rfloor\). If \(x\ne9\), then \(T_x(0)=T_x(1)\): that coefficient erases any incoming carry distinction. A candidate may not treat carry ports as independent repair controls. The U3 first-contact table in reports/Q03TStarU3FirstContact.md gives the exact physically admissible contact gates and their emitted difference packets.

3. **First-contact repair must exceed the adjacent-only class.** Under the hypotheses of the deep-U3 first-contact theorem, changing the contact coefficient and its mirror plus only the immediately adjacent coefficient and its mirror cannot make the successor pairwords agree through the adjacent site. The complete local proof and exact scope are results/Q03TStarAdjacentCellRepairNoGo.md. This rules out that one-edge repair rule, not arbitrary wider or moving repairs and not a path that explicitly allows a later nonlocal compensation.

4. **A finite monotone reservoir cannot renew itself.** For the symmetric central-zero corridor of width \(z_t>0\), the exact one-step law is \(z_{t+1}+\gamma_t\le z_t\). If the corridor stays positive through a 120-step macro, then \(z_{120}+30\le z_0\), contradicting a closed return \(z_{120}=z_0\). A homogeneous 9-band is also not a same-sector regenerative reservoir: the exact carry map sends its tracked interior into the even-only sector instead of restoring 9 (results/AgentY12NeutralNineIrreversibility.md; its bounded-sector hypothesis must be retained).

5. **Extreme uniform bands are not rooted alternatives.** The base-10 theorem results/ExtremeUniformIsolation10.md proves that the uniform cut targets 0 and 18 have only their constant predecessor trajectory for every overflow word; they are not reachable from the physical position-0 root. A candidate cannot repair T* by silently switching to one of those unrooted uniform bands.

6. **Centre parity must be explicit.** Equation (2) is the new all-phase bridge: even- and odd-length centre states cannot be collapsed into a single stationary state when the physical overflow clock contains ones.

**Corollary (escape criterion).** A T* construction with a negative-drift run is excluded; a route whose required one-edge first-contact closure is adjacent-only is excluded under Q03's stated hypotheses; a positive central-zero corridor cannot be a closed reservoir; and a rooted certificate cannot use an extreme uniform 0/18 band as an alternative bulk. Thus a surviving candidate must exhibit (i) a physically closed two-ended carry/overflow path, (ii) nonnegative drift in every unbounded coordinate, (iii) a non-adjacent, wider, or moving compensation whenever its first-contact packet requires repair, (iv) a genuinely replenished non-extreme reservoir if it uses a reservoir, and (v) the centre-parity transitions forced by (2). These are necessary conditions only; they do not exclude a path that allows transient mismatch and later active compensation, and they do not imply that a candidate exists.

## 4. Independent ordinary-integer controls

calculation/new_structures/Q05/verify_parity_cocycle.py constructs canonical T* source integers from the rooted B34/W9 data with \(U=(9,6,12)\), \(J=[5]\), \(C=[10]\). For each \(q=20,40,80,160\), \(k=5q\), it compares Python arbitrary-precision \(n+\operatorname{rev}(n)\) against an independently implemented schoolbook digit-array addition for all 120 edges. It checks the exact overflow clock, digit-length change, folded-pair symmetry, and carry-mass identity \(S_{t+1}=2S_t-18K_t\), where \(K_t\) counts all carry bits including overflow.

| \(q\) | \(k\) | Initial digits | Digits after 120 edges | Overflow count | Edge checks |
|---:|---:|---:|---:|---:|---:|
| 20 | 100 | 1,031 | 1,061 | 30 | 120 |
| 40 | 200 | 1,991 | 2,021 | 30 | 120 |
| 80 | 400 | 3,911 | 3,941 | 30 | 120 |
| 160 | 800 | 7,751 | 7,781 | 30 | 120 |

These are semantic controls for the identities, **not** finite-horizon survival evidence, not a seam return, and not a Lychrel claim. The separate all-width mod-81 carry gate in docs/EPOCH_INVARIANTS.md remains an existing result, not claimed as new here.

## 5. Exact remaining gap

The remaining T* problem is still to construct or finitely exclude a **rooted, all-width 120-edge physical interface return** \(P(q,k;J,U,C)\to P(q,k+5;J,U,C)\), with the complete seam and centre restored, both carries and overflow state actual, and every intermediate phase non-palindromic. The present theorem removes stationary-centre-length paths and compiles the other obstruction gates; it does not decide the remaining moving-centre / active-seam cases.
