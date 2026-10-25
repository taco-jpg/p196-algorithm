# REPORT_208 — return-certificate satisfiability audit

Agent 208 · direction 8 · 2026-10-22

Inspected revision: `c6902ac6c366ce018e68a810f58b400dda07145a`.
Branch: `gpt/208-certificate-audit`.

## Answer in one paragraph

**LEAN-VERIFIED / THEOREM.** Decimal Lychrel existence remains unresolved. The audit gives an exact reduction of the existing checker: with the states 和 four trimming counts fixed, some choice of lower bounds passes the original checker **iff** the exact structural return equations hold 和 both total band gains are nonnegative. The palindrome guard follows from an existing theorem, whose authorship is retained. A new finite interface obstruction excludes every accepted certificate whose interface blocks remain of length at most 2; therefore an accepted certificate must contain an interface of length at least 3. Complete mathematical proofs below 也 give componentwise minimal lower bounds bounded by `2P`, establish that signed transfers between the same blocks 和 bands do not enlarge existential satisfiability, 和 describe a sound extension with independent band phases. An explicit added state family passes the one-step safety test 可是 its tested representative reaches a palindrome at step 2, within a completed 1000-step run. No accepted return certificate or infinite decimal construction is supplied.

## 1. Scope, labels, source ownership

**LEAN-VERIFIED** denotes statements compiled in Lean 4.19.0 with only `propext`, `Classical.choice`, 和 `Quot.sound` permitted. **THEOREM** denotes a complete mathematical proof supplied here; it does not imply a new Lean formalization. **IDEA** denotes a proposed next research target. Numerical controls support implementation checks; they do not establish infinite avoidance.

| Status | Result | Ownership |
|---|---|---|
| LEAN-VERIFIED | Exact original-checker equivalence after lower-bound synthesis | New: `CertificateBounds208` |
| LEAN-VERIFIED | Every accepted certificate contains an interface of length at least 3 | New: `CertificateInterface208` |
| LEAN-VERIFIED | Complementary templates automatically fail `StepPal` | Existing: `Agent109.NoPal.not_stepPal`; imported directly |
| LEAN-VERIFIED | Accepted certificates automatically admit an ordinary realization | Existing: `CertificateToLychrel`; imported directly |
| THEOREM | Componentwise least cyclic bounds, with sharp abstract ceiling `2P` | Full proof in §4 |
| THEOREM | Signed padding transfers preserve existential satisfiability | Full carry proof in §6 |
| THEOREM | Conditional soundness of independent band phases | Full carry proof in §7 |

Primary inspected sources:

- [Original checker](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean): `LocalOK`, `check`, `certificate_sound`.
- [Exact carry formulas](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean): `data`, `Br`, `Ar`, `Cr`, `stepWord_template`, `actual_template_step`.
- [Existing automatic step safety](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent109TemplateStepSafety/NoPalStep.lean).
- [Existing gain accounting](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateAccounting.lean).
- [Existing ordinary realization](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleHeads.lean).
- [Existing exterior padding identity](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent6CertificateCoordinateAudit/ExteriorNormalization.lean): `Agent116.Exterior.Br_append_replicate`.

The reported new modules preserve the original checker. The requested draft uses a separate branch.

## 2. Exact data being audited

Write words from the units end. For a legal phase

\[
c\in\{1,\ldots,17\}\setminus\{9\},\qquad d=18-c,
\]

the template is

\[
Q_s(G,H)=B\,c^G\,A\,d^H\,C\,d^H\,A^R\,c^G\,B^R,
\quad s=(c,B,A,C).
\]

Here `x^m` means a word of `m` repeated coefficients, not exponentiation of an integer. Every coefficient in the finite blocks lies between 0 和 18. The parameters satisfy `G,H >= 2`.

Set

\[
\kappa=\mathbf1_{c\ge10},\quad \lambda=\mathbf1_{d\ge10}=1-\kappa,
\quad t=c-9\kappa,\quad v=d-9\lambda=9-t.
\]

Normalization of a word with an incoming carry returns its same-length digit word 和 terminal carry. The complete finite data are

\[
\begin{array}{lll}
(D_B,e_0)=N(B,0), &(D_A,e_1)=N(A,\kappa), &(D_C,e_2)=N(C,\lambda),\\
(D_{RA},e_3)=N(A^R,\lambda), &(D_{RB},\gamma)=N(B^R,\kappa).
\end{array}
\]

The entrance digits are

\[
u_0=t+e_0-\kappa,\quad u_1=v+e_1-\lambda,
\quad u_2=v+e_2-\lambda,\quad u_3=t+e_3-\kappa.
\]

All terminal carries are bits. With `zipAdd` denoting componentwise addition, the raw successor blocks use the following complete case table:

| `gamma` | `L_B` | `R_B` | `L_A` | `R_A` | `W_C` |
|---|---|---|---|---|---|
| 0 | `DB u0` | `reverse(DRB) t` | `t DA u1` | `u3 reverse(DRA) v` | `v DC u2` |
| 1 | `DB u0` | `1 reverse(DRB)` | `DA u1` | `u3 reverse(DRA)` | `DC u2` |

Then

\[
B_r=L_B+R_B,\qquad A_r=L_A+R_A,\qquad C_r=W_C+(W_C)^R.
\]

**LEAN-VERIFIED — existing transition identity.** The next pair word is

\[
T(Q_s(G,H))=Q_{F(s)}(G+\gamma-2,H+\gamma-2),
\quad F(s)=(2t,B_r,A_r,C_r).
\]

An original trimming link requires

\[
\begin{aligned}
B_r&=B'\,(c')^j,\\
A_r&=(c')^{j_1}A'(d')^{j_2},\\
C_r&=(d')^kC'(d')^k,
\end{aligned}
\qquad c'=2t,\quad d'=18-c'.
\]

Its exact signed parameter increments are

\[
\delta_i=\gamma_i+j_i+j_{1i}-2,
\qquad \epsilon_i=\gamma_i+j_{2i}+k_i-2.
\]

The local lower bounds obey

\[
\ell_i,\eta_i\ge2,\qquad
\ell_{i+1}\le\ell_i+\delta_i,\quad
\eta_{i+1}\le\eta_i+\epsilon_i,
\]

with indices modulo the positive period `P`.

## 3. LEAN-VERIFIED — safety is already automatic

**Statement, existing theorem.** For legal `c` 和 bounded `B,A`,

\[
\neg\operatorname{StepPal}(c,B,A,C)
\]

for arbitrary `C`. The new audit imports `Agent109.NoPal.not_stepPal`; the following proof explains its carry mechanism.

Let `S(W)` be the coefficient sum. A column with value `x` 和 incoming carry `e` has output digit `r` 和 outgoing carry `f`, where `x+e=r+10f`. Modulo 9, `r+f = x+e`. Summing across a block cancels the internal carries, giving

\[
S(N(W,e)_{\rm digits})+N(W,e)_{\rm carry}
\equiv S(W)+e\pmod9.
\]

Consequently,

\[
\begin{aligned}
S(D_B)&\equiv S(B)-e_0,&S(D_{RB})&\equiv S(B)+\kappa-\gamma,\\
S(D_A)&\equiv S(A)+\kappa-e_1,&S(D_{RA})&\equiv S(A)+\lambda-e_3.
\end{aligned}
\]

**Case `gamma=0`.** A palindrome requires `L_A=R_A`. Their sums reduce to

\[
S(L_A)\equiv S(A)+9+\kappa-\lambda,
\quad S(R_A)\equiv S(A)+9+\lambda-\kappa.
\]

Equality therefore requires `2(lambda-kappa)=0 mod 9`. For `kappa=0`, the left side equals 2; for `kappa=1`, it equals -2. Neither residue equals 0.

**Case `gamma=1`.** The exterior equality `L_B=R_B` requires

\[
S(B)+t-\kappa\equiv S(B)+\kappa\pmod9,
\quad\text{hence }t\equiv2\kappa\pmod9.
\]

The interface equality requires

\[
t-v+2(\lambda-\kappa)
=2t-9+2-4\kappa\equiv0\pmod9.
\]

Substituting the exterior congruence gives `2=0 mod 9`, a contradiction. More explicitly, `kappa=0` would already require `t=0 mod 9` despite `1<=t<=8`; `kappa=1` forces `t=2`, after which the interface difference is -7, again residue 2.

Both terminal-carry cases fail. The central equality was unnecessary. Thus searching central blocks to force the original safety guard cannot supply the missing return; safety holds already whenever the protected complementary bands survive.

## 4. Exact elimination of the lower-bound fields

### 4.1 LEAN-VERIFIED — equivalence for the unchanged checker

Define `StructuralValid` to retain exactly the original phase, boundedness, successor-phase, 和 block-trimming clauses, with a nonempty cycle. Define `withBounds` to preserve the states 和 all four trimming counts while replacing only `lo,lo'`.

The new endpoint is:

```lean
Agent208.CertificateBounds.bounds_exist_iff

(∃ b h : Nat → Nat, check (withBounds cert b h) = true) ↔
  StructuralValid cert ∧ 0 ≤ totalG cert ∧ 0 ≤ totalH cert
```

**Proof.** For one coordinate, write

\[
S_0=0,\quad S_i=\sum_{j<i}\delta_j,\quad
D=S_P,\quad m=\min_{0\le i\le P}S_i.
\]

If `D>=0`, set `ell_i=2+S_i-m` for `0<=i<P`. Each bound is a natural number at least 2. For `i<P-1`,

\[
\ell_{i+1}=\ell_i+\delta_i.
\]

At the closing edge,

\[
\ell_{P-1}+\delta_{P-1}-\ell_0=D\ge0.
\]

Conversely, summing any feasible cyclic inequalities cancels every bound 和 yields `D>=0`. Apply the same proof independently to `epsilon`. The safety clause follows from §3. All remaining clauses are precisely `StructuralValid`, proving the equivalence.

The implementation computes the prefix minimum recursively. Its `Int.toNat` conversion is justified by a nonnegativity proof. It neither changes decimal semantics nor weakens the original Boolean checker.

**LEAN-VERIFIED — reduced existence criterion.** The additional endpoint

```lean
theorem structural_cycle_existence (cert : Certificate)
    (hs : StructuralValid cert)
    (hG : 0 ≤ totalG cert) (hH : 0 ≤ totalH cert) :
    ∃ m, ∀ k, ¬ Palindrome (orbit m k)
```

composes the new synthesis with the existing ordinary-integer bridge. Its hypotheses still require the missing structural cycle.

### 4.2 THEOREM — componentwise least bounds, with ceiling `2P`

For any cyclic integer gains `delta_i>=-2` with total `D>=0`, define

\[
S_i(k)=\sum_{r=0}^{k-1}\delta_{i+r\bmod P},\qquad
\ell_i^*=2+\max_{0\le k<P}(-S_i(k)).
\]

Then these are the componentwise least feasible bounds, with

\[
2\le\ell_i^*\le2P.
\]

**Proof.** Put `A_i=max_{0<=k<P}(-S_i(k))`. For `k<P-1`,

\[
-S_{i+1}(k)=\delta_i-S_i(k+1)\le\delta_i+A_i.
\]

For the remaining value `k=P-1`,

\[
-S_{i+1}(P-1)=\delta_i-D\le\delta_i\le\delta_i+A_i.
\]

Thus `A_(i+1)<=A_i+delta_i`, proving feasibility. The empty prefix gives `A_i>=0`. Every prefix satisfies `S_i(k)>=-2k`, giving `A_i<=2(P-1)`.

For minimality, iterate any feasible bounds for `k` edges:

\[
\ell_i+S_i(k)\ge\ell_{i+k}\ge2.
\]

Taking the maximum of `2-S_i(k)` gives `ell_i>=ell_i*`.

Sharpness for abstract gain data follows from `P-1` successive gains -2 followed by `2(P-1)`: the first minimal bound equals `2P`. This example asserts feasibility of gain data only; it does not assert structural realizability as a return certificate. The executable Lean prefix-floor construction above is a convenient feasible construction; it is not asserted to equal this componentwise minimum.

**THEOREM — correlated length domains cannot rescue negative drift.** On any fixed repeated cycle, `G_(nP)=G_0+nD`. If `D<0`, every finite starting value eventually falls below 2, irrespective of any correlation with the other band. This is an obstruction to an infinite traversal itself, not merely to rectangular lower-bound domains.

## 5. Interface obstructions

### 5.1 THEOREM — a direct carry obstruction for interfaces of length at most 1

Every path respecting the exact interface formula leaves the class `|A|<=1` within at most 2 transitions, even if the terminal carry is freely chosen on each edge. This statement covers every legal phase, including odd phases.

**Empty interface.** For `A=[]`, the raw interface is

\[
\begin{cases}
[c'+\lambda-\kappa,\ d'+\kappa-\lambda],&\gamma=0,\\
[9],&\gamma=1.
\end{cases}
\]

In the first case neither endpoint equals its permitted trim symbol, 因为 `lambda-kappa` is either 1 or -1. The resulting length is 2. In the second case the resulting singleton is 9; the permitted trim symbols are even, so it remains `[9]`.

**Singleton interface.** Let `A=[a]`, `0<=a<=18`, with

\[
e=\lfloor(a+\kappa)/10\rfloor,
\quad f=\lfloor(a+\lambda)/10\rfloor.
\]

For `gamma=0`, the raw word is

\[
[c'+f-\kappa,\ 2a+1-10(e+f),\ d'+e-\lambda].
\]

The middle coefficient is odd, whereas both trim symbols are even. Thus a trim cannot pass the middle from either end. A residual length at most 1 would require removal of both endpoint letters, hence `f=kappa` 和 `e=lambda`. For `kappa=0`, these require `a<=8` 和 `a>=10`; for `kappa=1`, they require `a>=10` 和 `a<=8`. Both possibilities are contradictory.

For `gamma=1`, the raw word is

\[
[a+t+f-10e,\ a+v+e-10f].
\]

The complete coefficient cases are:

| Input range | Carries `(e,f)` | Raw word | A trim leaving length at most 1 |
|---|---|---|---|
| `a<=8` | `(0,0)` | `[a+t,a+v]` | Left trim requires `a=t`; right trim requires `a=v`; residual `[9]` |
| `a=9`, `kappa=0` | `(0,1)` | `[t+10,v-1]` | Neither permitted endpoint matches |
| `a=9`, `kappa=1` | `(1,0)` | `[t-1,v+10]` | Neither permitted endpoint matches |
| `a>=10` | `(1,1)` | `[a+t-9,a+v-9]` | Left trim requires `a=t+9`; right trim requires `a=v+9`; residual `[9]` |

Since `t+v=9`, simultaneous left 和 right matching would force `t=v`, impossible for integers. Every transition staying within the cap therefore lands at `[9]`. The `a=9` rows exclude a further capped transition for `gamma=1`; the preceding no-overflow calculation excludes it for `gamma=0`. This proves the obstruction with every carry case accounted for.

### 5.2 LEAN-VERIFIED — every accepted certificate needs an interface of length at least 3

The stronger cap-2 obstruction uses a finite rank certificate for the exact interface formula. It allows either terminal-carry bit at every edge, independently of the exterior. Every cyclic original certificate has an even phase, since each phase is its predecessor's doubled stable digit. Hence the complete state set is

\[
\mathcal V=
\{2,4,6,8,10,12,14,16\}\times
\bigl(\{[]\}\cup\{[a]:0\le a\le18\}\cup
\{[a,b]:0\le a,b\le18\}\bigr),
\]

containing `8(1+19+19^2)=3048` states.

**Exact edge definition.** From `(c,A)`, choose `gamma in {0,1}`, compute `Ar` from the case table in §2, 和 allow every literal decomposition

\[
A_r=(c')^{j_1}A'(d')^{j_2},\qquad |A'|\le2.
\]

Since `|A_r|<=4`, each trim count lies between 0 和 4. This covers maximal trims, nonmaximal trims, empty words, 和 every bounded interface of length at most 2. It adds possible carry choices; therefore an obstruction in this graph applies to actual certificates.

The supplied finite rank `r(c,A)` satisfies

\[
r(c',A')<r(c,A)
\]

on every such edge. Lean checks the finite rank data with kernel evaluation, then lifts the result to unrestricted natural trimming counts by the raw-length bound. On a hypothetical certificate with every `|A_i|<=2`, rank would strictly decrease around a nonempty cycle, returning to its initial value. This contradiction proves

\[
\operatorname{check}(\mathrm{cert})=\mathrm{true}
\quad\Longrightarrow\quad
\exists i<P:\ |A_i|\ge3.
\]

The local conjecture control gives survivor counts

```text
3048, 1248, 666, 350, 214, 112, 78, 52, 14, 0
```

for paths admitting at least `0,1,...,9` further edges. This is a small finite interface calculation, followed by verification of a decreasing rank; it is not a numerical search through integer seeds. Exterior widths, center widths, cycle period, band lengths, 和 choices of lower bounds remain unrestricted.

## 6. THEOREM — signed transfers between the same blocks 和 bands do not help

Define padding by

\[
P_{b,a,r,k}(c,B,A,C)=
(c,\ Bc^b,\ c^aAd^r,\ d^kCd^k).
\]

### 6.1 Exact padding covariance

For every nonnegative padding vector `z`,

\[
F(P_z(s))=P_z(F(s)),
\]

where the right side uses the successor letters `c',d'`. The terminal carry 和 `StepPal` remain unchanged.

**Carry proof.** For any legal coefficient `x`, put `k_x=1_(x>=10)`, `t_x=x-9k_x`, 和 `a_x(e)=x+e-10k_x`.

- If `x<=8`, an incoming bit `e` produces first digit `x+e` 和 outgoing carry 0; every remaining run digit is `x` with carry 0.
- If `x>=10`, the first digit is `x+e-10` with outgoing carry 1; every remaining run digit is `x-9` with carry 1.

If `N(W,e)=(D,h)`, the augmented suffix identity is

\[
D_{Wx^m,e}\,[a_x(h_{Wx^m,e})]
=D\,[a_x(h)]\,t_x^m.\tag{A}
\]

For `m=0`, both expressions coincide. For `m>=1`, the appended run contributes `a_x(h)` followed by `m-1` copies of `t_x`, ends with carry `k_x`, 和 contributes final augmented digit `a_x(k_x)=t_x`. Stable prefixing gives

\[
N(x^mW,k_x)=(t_x^mD_{W,k_x},h_{W,k_x}).\tag{B}
\]

For the exterior, (A) gives `L_B -> L_B t^b`; (B) gives `DRB -> t^b DRB`, preserving `gamma`. When `gamma=0`, `R_B` becomes `reverse(DRB)t^b t=R_B t^b`. When `gamma=1`, it becomes `1 reverse(DRB)t^b=R_B t^b`. Adding the arms gives `Br -> Br (2t)^b` in both cases.

For the interface, (A) 和 (B) give

\[
\begin{aligned}
D_{A,\mathrm{pad}}u_{1,\mathrm{pad}}
 &=t^aD_Au_1v^r,\\
u_{3,\mathrm{pad}}D_{RA,\mathrm{pad}}^R
 &=t^au_3D_{RA}^Rv^r.
\end{aligned}
\]

When `gamma=0`, the additional initial `t` in `L_A` commutes with `t^a`; the additional final `v` in `R_A` commutes with `v^r`. Each arm becomes `t^a (old arm) v^r`. When `gamma=1`, the displayed identities give that result directly. Thus `Ar -> (2t)^a Ar (2v)^r`.

For the center, `DC_pad u2_pad=v^k DC u2 v^k`. When `gamma=0`, its preceding `v` commutes with the initial `v^k`, giving `W_C -> v^k W_C v^k`. When `gamma=1`, the augmented identity already gives the same transformation. Pairing therefore gives `Cr -> (2v)^k Cr (2v)^k`.

In each carry case, `StepPal` means `L_B=R_B`, `L_A=R_A`, 和 `W_C^R=W_C`. Equal prefix/suffix cancellation proves equivalence before 和 after padding. No ordinary realization or center symmetry was assumed.

### 6.2 Exact equivalence with signed padding links

Permit generalized links

\[
P_{p_i}(F(s_i))=P_{q_i}(s_{i+1}),\qquad p_i,q_i\in\mathbb N^4.
\]

Their signed outer increment is

\[
\delta_i=\gamma_i-2+
(q_{i,B}+q_{i,A_L})-(p_{i,B}+p_{i,A_L}),
\]

with inner increment obtained by replacing `B,A_L` by `A_R,C`. Suppose the exact phase/boundedness conditions hold around a nonempty cycle 和 both total gains are nonnegative. Then an accepted original certificate exists with the same period.

**Proof.** Strip the maximal suffix `c^b` from `B`, maximal prefix `c^a` 和 suffix `d^r` from `A`, 和 maximal equal `d`-layers from both ends of `C`. The interface removals do not interfere 因为 `c!=d`. Center stripping stops at an empty word, a singleton, or at least one endpoint different from `d`. This gives a unique canonical decomposition `s_i=P_(r_i)(u_i)`.

Padding covariance gives `F(s_i)=P_(r_i)(F(u_i))`. Taking canonical cores of the signed-link equality forces the core of `F(u_i)` to equal `u_(i+1)`. Hence

\[
F(u_i)=P_{w_i}(u_{i+1})
\]

for a nonnegative vector `w_i`, precisely an original trimming link. Uniqueness of the padding vectors gives

\[
r_i+w_i+p_i=r_{i+1}+q_i.
\]

Write `b_i=r_(i,B)+r_(i,A_L)` 和 `h_i=r_(i,A_R)+r_(i,C)`. If `Delta_i,E_i` are the original gains of the core link, then

\[
\delta_i=\Delta_i+b_i-b_{i+1},\qquad
\epsilon_i=E_i+h_i-h_{i+1}.
\]

The extra differences telescope, preserving both total gains. Theorem §4 supplies the original lower bounds. Phases 和 boundedness survive stripping; safety follows from §3, or independently from padding invariance. Thus every original `LocalOK` clause holds. The reverse implication uses `p_i=0` 和 `q_i` equal to the original trimming vector.

This equivalence covers fixed complementary phase order 和 the displayed padding relation. Band swaps, disappearance of protected bands, phase-9 carry relays, 和 replacement by periodic bulk words lie outside its scope. The theorem identifies a specific ineffective relaxation; it does not exclude broader template frameworks.

**THEOREM — the interface obstruction survives canonicalization.** Normalize any accepted original certificate by the maximal removals above. The proof constructs another accepted original certificate on its canonical cores. Applying §5.2 to that certificate shows that some canonical interface still has length at least 3. Thus merely padding a shorter interface with its neighboring band letters cannot evade the obstruction.

## 7. THEOREM — a sound extension with independent phases

Replace `(c,18-c)` by independent legal phases `(a,b)`:

\[
Q_{a,b;B,A,C}(G,H)=B\,a^G A\,b^H C\,b^H A^R a^G B^R.
\]

Use `k_a=1_(a>=10)`, `k_b=1_(b>=10)`, `t=a-9k_a`, `v=b-9k_b`. The finite carry data become

\[
N(B,0),\quad N(A,k_a),\quad N(C,k_b),\quad
N(A^R,k_b),\quad N(B^R,k_a),
\]

with entrance digits

\[
u_0=a+e_0-10k_a,\quad u_1=b+e_1-10k_b,\quad
u_2=b+e_2-10k_b,\quad u_3=a+e_3-10k_a.
\]

Use the complete case table in §2 with these independent values. Define

\[
\mathrm{StepPal}_2(s)\iff
(L_B=R_B)\land(L_A=R_A)\land(W_C^R=W_C).
\]

For `G,H>=2`, the exact successor identity is

\[
T(Q_s(G,H))=Q_{2t,2v;B_r,A_r,C_r}(G+\gamma-2,H+\gamma-2).
\]

**Proof with both carry alignments.** Normalization gives

```text
DB (u0 t^(G-1)) DA (u1 v^(H-1)) DC
   (u2 v^(H-1)) DRA (u3 t^(G-1)) DRB
```

followed by `[1]` exactly when `gamma=1`. For `gamma=0`, regroup using the first row of the case table; the intervening run lengths are `G-2,H-2,H-2,G-2`. For `gamma=1`, regroup using its second row; the lengths are `G-1,H-1,H-1,G-1`, with the leading overflow digit incorporated into the right exterior block. In each case, the five finite blocks have mirrored lengths. Pairing them gives the raw blocks 和 doubles each bulk digit, proving the identity. The same equal-length decomposition shows that the normalized digit word is symmetric iff `StepPal_2` holds. Complementarity was unnecessary for these steps. The maps `x -> 2x` for `x<=8` 和 `x -> 2x-18` for `x>=10` preserve the legal phase set.

**Conditional soundness.** Require a cyclic list with both phase updates, exact trims, `not StepPal_2` at every row, 和 the original lower-bound inequalities. 也 require an explicit first-state ordinary realization

\[
\operatorname{pairWord}(n)=Q_{s_0}(G,H),\qquad
G\ge\ell_0,\quad H\ge\eta_0.
\]

The exact step identity 和 trimming equations propagate the representation 和 its bounds. The initial realization starts the induction; every successor supplies the next actual realization. The local safety test excludes every successor palindrome. Therefore every ordinary iterate of `step(n)`, including time 0, is nonpalindromic.

Automatic admissibility from the complementary checker is not assumed for this extension. The explicit realization hypothesis remains essential to the stated proof. The repository already contains broader affine-run results; this is a concrete extension of the audited checker, not a claim of novelty for the general affine framework.

### Strict added family; counterexample to indefinite safety

**THEOREM.** Take `a=2,b=4,B=[10],A=C=[]`, with `G,H>=2`. The pair word is symmetric, bounded, positive at both ends, 和 of even length, so it has an ordinary realization. The next output has units digit 0 和 a new leading digit 1, hence is nonpalindromic. Its alphabet `{2,4,10}` contains no legal complementary pair `{c,18-c}`; therefore it cannot be represented by an original complementary template with both protected band lengths at least 2.

**THEOREM — the entire family fails on the next step.** The first raw successor has phases `(4,8)` 和 finite blocks

\[
B_r=[1,3],\qquad A_r=[6],\qquad C_r=[8],
\]

with residual band lengths `G-1,H-1`. Every coefficient of this symmetric pair word is at most 8. Normalization with incoming carry 0 therefore has carry 0 in every column 和 returns the symmetric word itself. The second ordinary output is a palindrome. This rules out the whole displayed family as an infinite construction.

For `G=H=2`, a completed 1000-step control gave:

```text
pair word: [10, 2, 2, 4, 4, 4, 4, 2, 2, 10]
seed: 9224400001
step 1: 10224444230
step 2: 13468886431
step 3: 26937772862
steps executed: 1000
first palindrome: (2, 13468886431)
final digit count: 415
```

The counterexample invalidates any indefinite-safety claim for this family. It leaves the conditional extension theorem intact, while demonstrating why the independent-phase checker must retain its explicit safety guard.

## 8. Verification, reproducible controls, limits

Verification records 和 executable control code follow below. The exact structural cycle remains missing. The reported controls do not supply one.

### 8.1 New formal endpoints

The proof sources are:

- `lean/P196/CertificateBounds208/BoundSynthesis.lean`
- `lean/P196/CertificateInterface208/InterfaceRanks.lean`
- `lean/P196/CertificateInterface208/RankLifting.lean`
- `lean/P196/CertificateInterface208/CertificateInterface.lean`

The first file supplies `cyclic_bounds_iff`, `synthesize_valid`, `bounds_exist_iff`, 和 `structural_cycle_existence`. The interface files contain the exact rank data, local coverage proof, 和 original-checker obstruction. The verification gate is `python3 tools/verify.py --changed`; its actual output is recorded after the control code.

### 8.2 Finite-horizon control of the original carry model

An explicit complementary template starts with

```text
c=2
B=[11,9,0,18,4]
A=[9,9,10,0]
C=[3,18,3]
G=H=2002
```

The digit split used below realizes its symmetric pair word as an ordinary positive integer. Each of 1000 steps compares the finite raw carry formulas with an independently computed ordinary integer addition, verifies the exact pair word, 和 checks nonpalindromicity. The large initial bands provide a finite reserve; no cyclic return is claimed.

Actual output:

```json
{"carry_counts": [592, 408], "cyclic_return_claimed": false, "final_bands": [410, 410], "final_digits": 8437, "final_integer_sha256": "d1071d48cfe229837c7f3f8500df2b3739656bec350f72fa3ecbd8c4aab3253b", "final_state_lengths": [1005, 1596, 1595], "palindromic_outputs": 0, "seed_digits": 8029, "steps": 1000, "test": "finite_horizon_control"}
{"final_length": 337, "gains": [-2, -2, 5], "minimal_bounds": [6, 4, 2], "test": "scalar_bound_control", "updates": 1000}
{"final_length": 340, "gains": [5, -2, -2], "minimal_bounds": [2, 6, 4], "test": "scalar_bound_control", "updates": 1000}
{"final_length": 4, "gains": [-2, 2], "minimal_bounds": [4, 2], "test": "scalar_bound_control", "updates": 1000}
{"final_length": 2, "gains": [0], "minimal_bounds": [2], "test": "scalar_bound_control", "updates": 1000}
{"final_length": 16, "gains": [-2, -2, -2, -2, -2, -2, -2, -2, 16], "minimal_bounds": [18, 16, 14, 12, 10, 8, 6, 4, 2], "test": "scalar_bound_control", "updates": 1000}
```

### 8.3 Executable original-model control

```python
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)

def norm(word, carry):
    out = []
    for value in word:
        out.append((value + carry) % 10)
        carry = (value + carry) // 10
    return out, carry

def pair(word):
    return [a + b for a, b in zip(word, reversed(word))]

def raw(c, B, A, C):
    d, k = 18 - c, int(c >= 10)
    l = 1 - k
    t, v = c - 9*k, d - 9*l
    DB, e0 = norm(B, 0)
    DA, e1 = norm(A, k)
    DC, e2 = norm(C, l)
    RA, e3 = norm(A[::-1], l)
    RB, gamma = norm(B[::-1], k)
    u0, u1 = t + e0 - k, v + e1 - l
    u2, u3 = v + e2 - l, t + e3 - k
    add = lambda x, y: [a+b for a,b in zip(x,y)]
    if gamma == 0:
        Br = add(DB+[u0], RB[::-1]+[t])
        Ar = add([t]+DA+[u1], [u3]+RA[::-1]+[v])
        Cr = pair([v]+DC+[u2])
        pal = (([t]+RB)[::-1] == DB+[u0]
               and ([v]+RA+[u3])[::-1] == [t]+DA+[u1]
               and ([v]+DC+[u2])[::-1] == [v]+DC+[u2])
    else:
        Br = add(DB+[u0], [1]+RB[::-1])
        Ar = add(DA+[u1], [u3]+RA[::-1])
        Cr = pair(DC+[u2])
        pal = ((RB+[1])[::-1] == DB+[u0]
               and (RA+[u3])[::-1] == DA+[u1]
               and (DC+[u2])[::-1] == DC+[u2])
    return (2*t, Br, Ar, Cr), gamma, pal

def template(state, G, H):
    c, B, A, C = state
    d = 18-c
    return B+[c]*G+A+[d]*H+C+[d]*H+A[::-1]+[c]*G+B[::-1]

def realize(q):
    assert q == q[::-1] and q[0] > 0
    D = [0]*len(q)
    for i in range(len(q)//2):
        D[i], D[-1-i] = max(0,q[i]-9), min(9,q[i])
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        D[len(q)//2] = q[len(q)//2]//2
    assert pair(D) == q and D[-1] > 0
    return int(''.join(map(str,D[::-1])))

def minimal_bounds(gains):
    P = len(gains)
    assert P > 0 and sum(gains) >= 0
    out = []
    for i in range(P):
        subtotal = 0
        worst = 0
        for r in range(P-1):
            subtotal += gains[(i+r) % P]
            worst = min(worst, subtotal)
        out.append(2-worst)
    assert all(out[(i+1) % P] <= out[i]+gains[i] for i in range(P))
    return out

def main():
    # An explicit finite-horizon control, not a cyclic return candidate.
    state = (2, [11,9,0,18,4], [9,9,10,0], [3,18,3])
    G = H = 2002
    q = template(state,G,H)
    n = realize(q)
    seed_digits = len(str(n))
    counts = [0,0]
    for step in range(1,1001):
        assert G >= 2 and H >= 2
        successor, gamma, pal = raw(*state)
        assert not pal
        digits, actual_gamma = norm(q,0)
        assert actual_gamma == gamma
        if gamma:
            digits.append(gamma)
        n = n + int(str(n)[::-1])
        assert [int(x) for x in str(n)[::-1]] == digits
        assert digits != digits[::-1]
        G += gamma-2
        H += gamma-2
        state = successor
        q = template(state,G,H)
        assert pair(digits) == q
        counts[gamma] += 1
    print(json.dumps({
        'test':'finite_horizon_control', 'steps':1000,
        'seed_digits':seed_digits, 'final_digits':len(str(n)),
        'palindromic_outputs':0, 'carry_counts':counts,
        'final_bands':[G,H],
        'final_state_lengths':[len(x) for x in state[1:]],
        'final_integer_sha256':hashlib.sha256(str(n).encode()).hexdigest(),
        'cyclic_return_claimed':False
    },sort_keys=True))
    for gains in ([-2,-2,5], [5,-2,-2], [-2,2], [0], [-2]*8+[16]):
        b = minimal_bounds(gains)
        assert max(b) <= 2*len(gains)
        x = b[0]
        for step in range(1000):
            i = step % len(gains)
            assert x >= b[i]
            x += gains[i]
        print(json.dumps({'test':'scalar_bound_control','gains':gains,
              'minimal_bounds':b,'updates':1000,'final_length':x},sort_keys=True))

if __name__ == '__main__':
    main()
```

### 8.4 Executable finite interface check

```python
"""Independent finite check of the complementary-interface cap-two obstruction.
No integer reverse-and-add trajectories or seeds are searched.
"""
from itertools import product
from collections import Counter

def scan(word, carry):
    digits = []
    for x in word:
        digits.append((x + carry) % 10)
        carry = (x + carry) // 10
    return digits, carry

def raw_interface(c, word, gamma):
    d, kc = 18 - c, int(c >= 10)
    kd = 1 - kc
    t, u = c - 9 * kc, d - 9 * kd
    left, e1 = scan(word, kc)
    right, e3 = scan(word[::-1], kd)
    x1, x3 = d + e1 - 10 * kd, c + e3 - 10 * kc
    if gamma == 0:
        low, high = [t] + left + [x1], [x3] + right[::-1] + [u]
    else:
        low, high = left + [x1], [x3] + right[::-1]
    assert len(low) == len(high)
    return tuple(x + y for x, y in zip(low, high))

words = [()] + [(a,) for a in range(19)] + list(product(range(19), repeat=2))
nodes = [(c, word) for c in range(2, 18, 2) for word in words]
edges = {node: [] for node in nodes}
checked = 0
for c, word in nodes:
    cp = 2 * (c - 9 * (c >= 10))
    for gamma in (0, 1):
        raw = raw_interface(c, word, gamma)
        for j in range(5):
            for k in range(5):
                checked += 1
                if j + k > len(raw):
                    continue
                middle = raw[j:len(raw) - k]
                if len(middle) <= 2 and raw == (cp,) * j + middle + (18 - cp,) * k:
                    edges[c, word].append(((cp, middle), gamma, j, k))

ranks, active = {}, set()
def rank(node):
    if node in ranks:
        return ranks[node]
    if node in active:
        raise AssertionError(("cycle", node))
    active.add(node)
    value = max((rank(target) + 1 for target, *_ in edges[node]), default=0)
    active.remove(node)
    ranks[node] = value
    return value

for node in nodes:
    rank(node)
assert all(ranks[target] < ranks[source]
           for source in nodes for target, *_ in edges[source])
print("nodes", len(nodes))
print("candidate_trim_checks", checked)
print("retained_edges", sum(map(len, edges.values())))
print("rank_histogram", sorted(Counter(ranks.values()).items()))
print("maximum_path_edges", max(ranks.values()))
print("closed_walks", 0)
path = [(2, (6,)), (4, (13,13)), (8, (8,9)), (16, (18,0)),
        (14, (17,1)), (10, (15,3)), (2, (11,7)), (4, (4,9)), (8, (14,4))]
for source, target in zip(path, path[1:]):
    assert any(v == target for v, *_ in edges[source])
print("eight_edge_control_ranks", [ranks[node] for node in path])
```

Actual output:

```text
nodes 3048
candidate_trim_checks 152400
retained_edges 1840
rank_histogram [(0, 1800), (1, 582), (2, 316), (3, 136), (4, 102), (5, 34), (6, 26), (7, 38), (8, 14)]
maximum_path_edges 8
closed_walks 0
eight_edge_control_ranks [8, 7, 6, 5, 4, 3, 2, 1, 0]
```

### 8.5 Executable independent-phase counterexample

```python
def realize(q):
    assert q == q[::-1]
    D=[0]*len(q)
    for i in range(len(q)//2):
        D[i]=q[i]-min(9,q[i])
        D[-1-i]=min(9,q[i])
    if len(q)%2:
        assert q[len(q)//2]%2==0
        D[len(q)//2]=q[len(q)//2]//2
    assert D[-1]>0 and all(0<=x<=9 for x in D)
    assert [D[i]+D[-1-i] for i in range(len(D))]==q
    return sum(x*10**i for i,x in enumerate(D))

a,b,g,h=2,4,2,2
q=[10]+[a]*g+[b]*h+[b]*h+[a]*g+[10]
n=realize(q)
print('pair word:',q)
print('seed:',n)
first_palindrome=None
for step in range(1,1001):
    s=str(n)
    n+=int(s[::-1])
    s=str(n)
    if step<=3:
        print(f'step {step}: {n}')
    if first_palindrome is None and s==s[::-1]:
        first_palindrome=(step,n)
print('steps executed:',1000)
print('first palindrome:',first_palindrome)
print('final digit count:',len(str(n)))
```

### 8.6 Executable padding identity control

```python
from itertools import product

def norm(W,e):
    D=[]
    for x in W:
        D.append((x+e)%10)
        e=(x+e)//10
    return D,e

def raw(c,B,A,C):
    d=18-c; kc=int(c>=10); kd=int(d>=10); t=c-9*kc; v=d-9*kd
    DB,e0=norm(B,0); DA,e1=norm(A,kc); DC,e2=norm(C,kd); DRA,e3=norm(A[::-1],kd); DRB,g=norm(B[::-1],kc)
    u0=c+e0-10*kc; u1=d+e1-10*kd; u2=d+e2-10*kd; u3=c+e3-10*kc
    z=lambda X,Y:[x+y for x,y in zip(X,Y)]
    Br=z(DB+[u0], DRB[::-1]+[t] if g==0 else [1]+DRB[::-1])
    Ar=z([t]+DA+[u1], [u3]+DRA[::-1]+[v]) if g==0 else z(DA+[u1],[u3]+DRA[::-1])
    W=([v] if g==0 else [])+DC+[u2]
    Cr=z(W,W[::-1])
    return Br,Ar,Cr,g

samples=[[],[0],[9],[18],[1,9],[9,18],[0,10,9],[18,9,8]]
count=0
for c in [1,2,4,6,8,10,12,14,16,17]:
    d=18-c; cp=2*(c-9*(c>=10));dp=18-cp
    for B,A,C in product(samples,repeat=3):
        x=raw(c,B,A,C)
        for b,a,r,k in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(2,3,2,1)]:
            y=raw(c,B+[c]*b,[c]*a+A+[d]*r,[d]*k+C+[d]*k)
            want=(x[0]+[cp]*b,[cp]*a+x[1]+[dp]*r,[dp]*k+x[2]+[dp]*k,x[3])
            assert y==want,(c,B,A,C,(b,a,r,k),x,y,want)
            count+=1
print(f'padding identities: {count} exact local checks; all passed')
```

Actual output:

```text
padding identities: 25600 exact local checks; all passed
```

### 8.7 Formal verification record

**LEAN-VERIFIED — final repository gate.** With Lean 4.19.0, one Lean worker, 和 the unchanged repository verifier:

```text
$ LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
[rules] 4827 Lean files, 289 projects, OK
[changed] against origin/main: 4 new/changed Lean file(s); building 4 module(s); auditing 2 project(s)
[build] up to 1 Lean file(s) at a time
Build completed successfully.
[build] OK
[axioms] 9 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The four new modules are registered under `CertificateBounds208` 和 `CertificateInterface208`. All nine registered endpoints use only the permitted standard axioms `propext`, `Classical.choice`, 和 `Quot.sound`; there are no `sorry`, `admit`, custom axioms, or `native_decide` in the new proofs. This was the required changed-files gate, including the repository-wide rules scan, not a fresh rebuild of every existing module.

The largest individual new-module build was the finite interface-rank verification: 211.327 seconds, peak resident memory 5,013,136 KiB, with one Lean worker. This is below the repository limits of 20 minutes 和 8 GiB per module. The finite graph calculation supplies an exact decreasing-rank witness; the bounds, carry, padding, 和 counterexample arguments above are independent mathematical arguments. No finite orbit experiment is used to infer an infinite orbit.

## 9. Audit conclusion 和 sharpest open question

**THEOREM — exact remaining obligation.** The original acceptance problem reduces to a nonempty cycle satisfying the unchanged exact block equations with

\[
\sum_i(\gamma_i+j_i+j_{1i}-2)\ge0,
\qquad
\sum_i(\gamma_i+j_{2i}+k_i-2)\ge0.
\]

The lower-bound search 和 local palindrome test can be removed from that search without changing acceptance feasibility. Interfaces uniformly bounded by 2 are excluded. Signed changes of the same block boundaries cannot alter existential feasibility.

**IDEA — sharp next question.** Does a canonical structural cycle with an interface of length at least 3 satisfy both gain inequalities, or does an invariant of the exact interface/core dynamics exclude every such cycle? The finite cap-2 rank does not answer the unbounded question. A sound independent-phase or periodic-band extension changes the represented mathematical class, 可是 its structural return 和 all-step safety obligations still require an actual witness.

No global satisfiability or global impossibility conclusion is asserted.
