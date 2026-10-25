# REPORT_215 — Interfaces, global residues, 和 affine run growth

Agent: **215**. Direction: **5**. Date: **2026-10-22**.

## Answer — one paragraph

**THEOREM —** Exact interface bookkeeping gives global residues modulo \(9\) for an arbitrary number of mirrored constant bands. If the outer band symbol 和 every adjacent band difference are invertible modulo \(9\), a closed return must increase each paired band length by a multiple of \(9\); strict growth of \(r\) paired bands therefore requires at least \(18r\) overflows 和 return time \(m\ge36r\). More generally, suffix-gain divisibility gives an explicit sharp lower bound for the necessary arithmetic constraints. **THEOREM —** An integer-affine return valid for every independently sufficiently long run-length vector 有 a nonnegative, length-conserving linear part; if every run grows without bound, the matrix must be a weight-preserving permutation. An exact finite guard test follows. These 是 obstruction 和 conditional classification results. Decimal Lychrel existence remains unresolved here: the missing object 是 a concrete closed interface cycle with admissible growth 和 palindrome avoidance at every phase. The accompanying checks include \(1000\) consecutive ordinary decimal steps; they validate the formulas, without supplying the missing cycle.

## Status 和 scope

**THEOREM** labels below mean complete paper proofs, including explicitly identified applications of existing results. The new statements 没有 Lean formalizations; their status 是 **THEOREM**, with complete paper proofs only. Numerical checks supplement the proofs. Statements labeled **IDEA** remain proposed next steps.

Repository baseline inspected: `c6902ac6c366ce018e68a810f58b400dda07145a`. Existing 2-band normalization, width accounting, carry budgets, 和 scalar affine-family results were inspected before developing these extensions. The report claims neither repository-wide novelty nor a new certificate instance. The task concerns arbitrary decimal seeds 和 templates.

## 1. Model 和 exact carry conventions

Words run from the units column toward the leading column. Write \(W^R\) for reversal, \(|W|\) for length, 和 \(\Sigma W\) for the sum of its entries. Concatenation uses juxtaposition; \(s^n\) denotes \(n\) copies of the symbol \(s\).

A canonical column-sum word \(q\) satisfies:

- entries in \(\{0,\ldots,18\}\);
- \(q=q^R\), with positive outer coefficient;
- an even central coefficient when its length 是 odd.

These conditions give an ordinary decimal realization: for each mirrored pair with sum \(s\), choose the more significant digit \(\min(9,s)\) 和 the less significant digit \(s-\min(9,s)\); at an unpaired center use half its coefficient. The positive outer coefficient makes the leading digit positive.

For normalization, set

\[
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,\qquad
e_i=q_i+c_i-10c_{i+1}.
\]

Every carry belongs to \(\{0,1\}\). Put \(\gamma=c_L\). When \(\gamma=0\), the normalized word 有 length \(L\): its leading digit equals \(q_{L-1}+c_{L-1}>0\). When \(\gamma=1\), append the leading digit \(1\), giving length \(L+1\). Pairing the normalized word with its reversal preserves its length. Thus

\[
|T(q)|-|q|=\gamma.
\tag{1}
\]

For a finite word \(A\), let \(\operatorname{norm}(A,c)=(D,u)\) denote its same-length normalized digits 和 final carry. Let \(K_D\) denote the sum of **every outgoing carry** during the normalization, including the final carry. Summing the column equations gives

\[
\Sigma D=\Sigma A+c-u-9K_D.
\tag{2}
\]

Equation (2) includes the empty-word case: then \(u=c\), \(K_D=0\).

For \(s\ne9\), define

\[
k_s=\mathbf1_{s\ge10},\qquad t_s=s-9k_s,\qquad f(s)=2t_s.
\]

**THEOREM 1 — Constant-band normalization.** For \(n\ge1\) 和 incoming carry \(a\in\{0,1\}\),

\[
\operatorname{norm}(s^n,a)
=\bigl([t_s+a-k_s]t_s^{n-1},\ k_s\bigr)
\quad(s\ne9).
\tag{3}
\]

For \(s\le8\), the first sum \(s+a\le9\), so the outgoing carry resets to \(0\), the first digit equals \(s+a\), 和 subsequent digits equal \(s\). For \(s\ge10\), the first sum lies between \(10\) 和 \(19\), so the carry resets to \(1\), the first digit equals \(s+a-10\), 和 subsequent digits equal \(s-9\). These give the 两 cases of (3).

The excluded symbol follows a different exact rule:

\[
\operatorname{norm}(9^n,0)=(9^n,0),\qquad
\operatorname{norm}(9^n,1)=(0^n,1).
\tag{4}
\]

Thus a long \(9\)-band transmits its incoming carry. The theorems about persistent bands below exclude the symbol; finite interface blocks may contain \(9\) without restriction. \(\square\)

## 2. THEOREM — Exact transition for an arbitrary number of interfaces

Consider

\[
q=B_0s_1^{n_1}B_1s_2^{n_2}\cdots B_{r-1}s_r^{n_r}
C
s_r^{n_r}B_{r-1}^{R}\cdots s_2^{n_2}B_1^{R}s_1^{n_1}B_0^{R},
\tag{5}
\]

where \(r\ge1\), \(n_i\ge2\), \(s_i\ne9\), 和 the word satisfies the canonical conditions above. Set

\[
s_i'=f(s_i),\qquad \varepsilon=2-\gamma.
\]

The raw successor retains the same arrangement, with band lengths \(n_i-\varepsilon\). Its blocks follow the formulas below. \(\operatorname{zipAdd}\) adds equal-length words coordinatewise.

### Exterior block

Put \(s=s_1\), \(B=B_0\). Normalize

\[
\operatorname{norm}(B,0)=(D,u),\qquad
\operatorname{norm}(B^R,k_s)=(E,\gamma).
\]

The latter final carry 是 the actual overflow, 因为 the reflected outer band resets its carry to \(k_s\) before \(B^R\). Define \(v_s=s+u-10k_s\). Then

\[
B_{0,\rm raw}=
\begin{cases}
\operatorname{zipAdd}(D[v_s],E^R[t_s]),&\gamma=0,\\
\operatorname{zipAdd}(D[v_s],[1]E^R),&\gamma=1.
\end{cases}
\tag{6}
\]

In each case \(|B_{0,\rm raw}|=|B_0|+1\).

### Interior block

For an interface \(A=B_j\) between \(a=s_j\) 和 \(b=s_{j+1}\), normalize

\[
\operatorname{norm}(A,k_a)=(D,u),\qquad
\operatorname{norm}(A^R,k_b)=(E,v).
\]

The entrance digits into the following bands are

\[
v_b=b+u-10k_b,\qquad v_a=a+v-10k_a.
\]

Then

\[
A_{\rm raw}=
\begin{cases}
\operatorname{zipAdd}([t_a]D[v_b],[v_a]E^R[t_b]),&\gamma=0,\\
\operatorname{zipAdd}(D[v_b],[v_a]E^R),&\gamma=1.
\end{cases}
\tag{7}
\]

Its length equals \(|A|+\varepsilon\).

### Central block

Put \(s=s_r\) 和 \(\operatorname{norm}(C,k_s)=(D,u)\). With \(v_s=s+u-10k_s\),

\[
C_{\rm raw}=
\begin{cases}
\operatorname{pair}([t_s]D[v_s]),&\gamma=0,\\
\operatorname{pair}(D[v_s]),&\gamma=1.
\end{cases}
\tag{8}
\]

Its length equals \(|C|+\varepsilon\).

### Proof of the whole-word alignment

Equation (3) identifies the first digit of each band 和 its remaining constant tail. If \(\gamma=0\), reflection retains the original width. At an exterior, its 两 boundary strings 有 length \(|B_0|+1\), as in (6). At an interior interface, allocating one stable digit from each adjacent band produces the 两 strings of length \(|A|+2\) in (7). At the center, allocating the stable digit 和 entrance digit produces the length-\(|C|+2\) string in (8). The residual mirrored constant tails each 有 length \(n_i-2\).

If \(\gamma=1\), the appended leading \(1\) shifts reflected alignment by one column. The exterior strings become \(D[v_s]\) 和 \([1]E^R\). Each interior pair becomes \(D[v_b]\) 和 \([v_a]E^R\), of length \(|A|+1\). The central string becomes \(D[v_s]\), of length \(|C|+1\). The residual tails each 有 length \(n_i-1\). Each displayed pair 有 equal length, so coordinatewise pairing concatenates the raw blocks 和 constant bands exactly. The partition accounts for every column in each overflow case. \(\square\)

### Legal trimming 和 the affine length map

A transition may redistribute actual band letters by literal equalities

\[
\begin{aligned}
B_{0,\rm raw}&=B_0'(s_1')^{j_0},\\
B_{j,\rm raw}&=(s_j')^{\alpha_j}B_j'(s_{j+1}')^{\beta_j}
&& (1\le j<r),\\
C_{\rm raw}&=(s_r')^\kappa C'(s_r')^\kappa.
\end{aligned}
\tag{9}
\]

Define \(\beta_0=j_0\) 和 \(\alpha_r=\kappa\). The exact update 是

\[
\boxed{n_i'=n_i-\varepsilon+\beta_{i-1}+\alpha_i.}
\tag{10}
\]

The block-length updates are

\[
\begin{aligned}
|B_0'|&=|B_0|+1-j_0,\\
|B_j'|&=|B_j|+\varepsilon-\alpha_j-\beta_j,\\
|C'|&=|C|+\varepsilon-2\kappa.
\end{aligned}
\tag{11}
\]

They follow by taking lengths in (6)–(9). In particular, fixing a finite interface transition fixes an integer **translation** of the run-length vector. Arbitrarily chosen carry bits or trim counts 不 define an edge: equations (6)–(9) must hold literally.

## 3. THEOREM — Global interface residues

### Interior charge: exact integer identity

For the interface in (7), put \(\ell=|A|\), 和 let \(K_D,K_E\) be its 两 outgoing-carry sums. Equation (2) gives

\[
\Sigma D=\Sigma A+k_a-u-9K_D,\qquad
\Sigma E=\Sigma A+k_b-v-9K_E.
\]

For \(\gamma=0\), summing the first line of (7) adds \(t_a+v_b+v_a+t_b\). Substitution gives

\[
\Sigma A_{\rm raw}
=2\Sigma A+2(a+b)-9[2(k_a+k_b)+K_D+K_E].
\]

For \(\gamma=1\), summing the second line adds \(v_b+v_a\), giving

\[
\Sigma A_{\rm raw}
=2\Sigma A+(a+b)-9[k_a+k_b+K_D+K_E].
\]

Consequently, for

\[
Q=2\Sigma A-(a+b)|A|,
\]

the cases 都 give the exact integer identity

\[
Q_{\rm raw}=2Q+18[(k_a+k_b)\ell-K_D-K_E].
\tag{12}
\]

Removing the actual prefix \((a')^\alpha\) 和 suffix \((b')^\beta\) in (9) gives

\[
Q_{\rm raw}=Q'+(a'-b')(\alpha-\beta).
\tag{13}
\]

### The global length term

For interface \(B_j\), let \(M_j\) be the full centered subword inside its 两 reflected copies:

\[
M_j=2\sum_{i=j+1}^r n_i+
2\sum_{i=j+1}^{r-1}|B_i|+|C|.
\]

In the raw step, the \(r-j\) paired bands lose \(2(r-j)\varepsilon\) positions; their \(r-j-1\) paired internal blocks gain \(2(r-j-1)\varepsilon\); the center gains \(\varepsilon\). The net change equals \(-\varepsilon\). Trimming internal boundaries preserves the centered length, while \(\beta_j\) moves into it from each outer interface. Therefore

\[
M_j'=M_j-\varepsilon+2\beta_j.
\]

Writing \(H_j=|B_j|+M_j\), equation (11) gives

\[
H_j'=H_j-(\alpha_j-\beta_j).
\tag{14}
\]

### Interior invariant

If \(\gcd(s_j-s_{j+1},9)=1\), define

\[
\boxed{
I_j=(s_j-s_{j+1})^{-1}
\bigl[2\Sigma B_j-(s_j+s_{j+1})|B_j|\bigr]
-\bigl(|B_j|+M_j\bigr)\pmod9.
}
\tag{15}
\]

Inverses here are residues modulo \(9\). Since \(a'-b'\equiv2(a-b)\pmod9\), equations (12)–(14) give

\[
I_j'\equiv
(a-b)^{-1}Q-(\alpha_j-\beta_j)
-[H_j-(\alpha_j-\beta_j)]
\equiv I_j\pmod9.
\]

Thus \(I_j\) remains invariant at every legal step. It explicitly includes the length of the entire inner region.

### Exterior invariant

For (6), equation (2) gives

\[
\Sigma D=\Sigma B-u-9K_D,\qquad
\Sigma E=\Sigma B+k_s-\gamma-9K_E.
\]

When \(\gamma=0\), adding \(v_s+t_s\) gives \(2\Sigma B+2t_s-9(K_D+K_E)\). When \(\gamma=1\), adding \(v_s+1\) gives \(2\Sigma B+t_s-9(K_D+K_E)\). With \(R=\Sigma B-s|B|\), the cases 都 yield

\[
R_{\rm raw}=2R-\gamma s+
9[(2|B|+\gamma)k_s-K_D-K_E].
\tag{16}
\]

Trimming a suffix of the new band symbol preserves the charge, so \(R'\equiv2R-\gamma s\pmod9\). If \(\gcd(s_1,9)=1\), equation (1) shows that

\[
\boxed{
J=2s_1^{-1}\bigl(\Sigma B_0-s_1|B_0|\bigr)+|q|\pmod9
}
\tag{17}
\]

remains invariant: \(2(2s)^{-1}(2R-\gamma s)+|q|+\gamma=2s^{-1}R+|q|\) modulo \(9\). \(\square\)

## 4. THEOREM — Growth residues 和 sharp arithmetic budgets

Suppose an \(m\)-step legal return restores every symbol 和 finite block in (5), with

\[
n_i\longmapsto n_i+\delta_i.
\]

Let \(K\) count its actual overflows. Width accounting gives

\[
\boxed{K=2\sum_{i=1}^r\delta_i.}
\tag{18}
\]

For a unit adjacent difference, (15) implies

\[
\sum_{i=j+1}^r\delta_i\equiv0\pmod9,
\tag{19}
\]

因为 its charge 和 finite-block length return, while its centered length changes by twice the suffix sum. For a unit outer symbol, (17) implies \(K\equiv0\pmod9\), hence \(\sum_i\delta_i\equiv0\pmod9\). Subtracting successive suffix congruences establishes

\[
\boxed{
\gcd(s_1,9)=1,\quad
\gcd(s_j-s_{j+1},9)=1\ (1\le j<r)
\quad\Longrightarrow\quad
9\mid\delta_i\ (1\le i\le r).
}
\tag{20}
\]

The statement needs neither a guessed carry sequence nor an unproved bound on interface widths.

### Carry budget, with every outer-column case displayed

Let \(a=q_0\in\{1,\ldots,18\}\) 和 let \(e\in\{0,1\}\) be the carry entering the leading column. Exact outer evolution gives

\[
\gamma=\left\lfloor\frac{a+e}{10}\right\rfloor,\qquad
a'=\begin{cases}2a+e,&\gamma=0,\\a\bmod10+1,&\gamma=1.\end{cases}
\tag{21}
\]

For \(\gamma=0\), the endpoint digits 都 come from the original outer coefficient; for \(\gamma=1\), the units digit pairs with the appended \(1\). Define the potential \(h\) by the complete table. The last columns give the slack \(1-2\gamma+h(a)-h(a')\), evaluated using (21).

| \(a\) | \(h(a)\) | slack for \(e=0\) | slack for \(e=1\) |
|---:|---:|---:|---:|
| 1 | 0 | 1 | 1 |
| 2 | 0 | 0 | 1 |
| 3 | 0 | 0 | 0 |
| 4 | 1 | 1 | 0 |
| 5 | 0 | 0 | 0 |
| 6 | 1 | 1 | 0 |
| 7 | 1 | 1 | 0 |
| 8 | 1 | 0 | 0 |
| 9 | 2 | 0 | 0 |
| 10 | 1 | 0 | 0 |
| 11 | 1 | 0 | 0 |
| 12 | 1 | 0 | 0 |
| 13 | 2 | 0 | 0 |
| 14 | 1 | 0 | 0 |
| 15 | 2 | 0 | 0 |
| 16 | 2 | 0 | 0 |
| 17 | 2 | 0 | 0 |
| 18 | 3 | 0 | 0 |

Every slack 是 nonnegative. Summing around a return of the outer coefficient cancels the potentials 和 gives

\[
2K\le m.
\tag{22}
\]

Combining (18), (20), 和 (22), strict growth of every paired band gives

\[
\boxed{\delta_i\ge9,\qquad K\ge18r,\qquad m\ge36r.}
\tag{23}
\]

For complementary bands \(c,18-c\) with \(c\in\{2,4,8,10,14,16\}\), the unit hypotheses 都 hold. Thus strict growth of the 两 paired bands requires \(m\ge72\). The existing repository already records the separate 2-band gain divisibilities; (15)–(23) extend the mechanism to arbitrary \(r\).

### Nonunit differences: an exact suffix-divisibility system

Assume \(6\mid m\), allowing arbitrary noncritical band symbols. The condition holds automatically if any returning label lies in the six-cycle

\[
2\to4\to8\to16\to14\to10\to2.
\]

Write \(A_j=\sum_{t<m}\alpha_{j,t}\), \(B_j=\sum_{t<m}\beta_{j,t}\) for trim totals in the present paragraph only. Iterating (12)–(13) modulo \(9\), multiplying step \(t\) by \(2^{-(t+1)}\), 和 using \(2^m\equiv1\pmod9\) gives

\[
(s_j-s_{j+1})(A_j-B_j)\equiv0\pmod9.
\]

Equation (14), summed over the return, gives

\[
A_j-B_j=-2\sum_{i=j+1}^r\delta_i.
\]

Iterating (16) with the same inverse powers gives \(s_1K\equiv0\pmod9\). Therefore, for suffix gains \(R_j=\sum_{i=j}^r\delta_i\),

\[
s_1R_1\equiv0\pmod9,\qquad
(s_{j-1}-s_j)R_j\equiv0\pmod9\quad(2\le j\le r).
\tag{24}
\]

Without \(6\mid m\), the telescoping charge retains an extra term involving \((1-2^{-m})Q_0\); (24) cannot simply be imposed. In particular, the \(6,12\) phase cycle requires separate treatment.

Set

\[
D_1=\frac9{\gcd(s_1,9)},\qquad
D_j=\frac9{\gcd(s_{j-1}-s_j,9)}\quad(2\le j\le r).
\]

Then (24) says exactly \(D_j\mid R_j\). If \(\delta_i>0\), define recursively

\[
R_{r+1}^*=0,\qquad
R_j^*=D_j\left(\left\lfloor\frac{R_{j+1}^*}{D_j}\right\rfloor+1\right).
\tag{25}
\]

**THEOREM —** Every positive gain vector satisfying (24) satisfies \(R_j\ge R_j^*\). The differences \(\delta_j^*=R_j^*-R_{j+1}^*\) themselves satisfy these arithmetic constraints, so \(R_1^*\) 是 their exact minimum total gain.

**Proof.** Positivity gives \(R_j>R_{j+1}\). Formula (25) chooses the smallest multiple of \(D_j\) strictly above the next suffix. Descending induction gives the lower bound. Conversely, the selected suffixes are strictly decreasing outward-to-inward 和 satisfy the required divisibility; their differences therefore give a positive permissible arithmetic vector. The argument establishes arithmetic optimality only, without asserting a decimal realization. \(\square\)

Consequently

\[
\boxed{m\ge4R_1^*.}
\tag{26}
\]

| Ordered band symbols | \((D_j)\) | Minimal arithmetic gains | Basic period lower bound |
|---|---|---|---:|
| \((2)\) | \((9)\) | \((9)\) | 36 |
| \((2,6)\) | \((9,9)\) | \((9,9)\) | 72 |
| \((2,8)\) | \((9,3)\) | \((6,3)\) | 36 |
| \((2,6,10)\) | \((9,9,9)\) | \((9,9,9)\) | 108 |
| \((2,8,14)\) | \((9,3,3)\) | \((3,3,3)\) | 36 |

### THEOREM — Additional saturation corollary from an existing repository result

The inspected theorem `P196.Agent4.Saturation.saturated_closed_prefix_period` establishes \(8\mid m\) for a closed three-column prefix path at equality \(2K=m\). Its published finite-prefix relation 和 theorem are in `PrefixModel.lean` 和 `SaturationTheorem.lean`. The direct whole-word application 是 `P196.Agent4.WholeWord.actual_saturated_prefix_return` in `WholeWordBridge.lean`. The report reuses those existing statements; their Lean proofs were inspected without rerunning them.

To supply the exact bridge, put \(p_t=(q_t(0),q_t(1),q_t(2))\) 和 \(e_t=c_t(L_t-3)\). The existing `iterPairs_prefix_evolution` gives \(\operatorname{advance}(p_t,e_t)=(p_{t+1},\gamma_t)\). Section 1 supplies admissibility; width monotonicity preserves \(L_t\ge3\). Prefix closure gives \(p_m=p_0\), 和 saturation gives \(2L_m=2L_0+m\), exactly the hypotheses of `actual_saturated_prefix_return`.

For a return in (5), the three-column prefix returns whenever \(|B_0|+\min(n_1,n_1+\delta_1)\ge3\). For strict growth, \(|B_0|+n_1\ge3\) suffices. A uniform positive-drift return can start with such a band length; an indefinitely repeatable strictly growing return eventually reaches it. Under the additional prefix-closure condition, equality in (23) forces \(8\mid36r\). Odd \(r\) therefore excludes equality. A returning label must be even, since every value of \(f\) 是 even. The even unit labels are exactly \(2,4,8,10,14,16\), whose displayed \(f\)-cycle has period \(6\). Therefore \(6\mid m\), giving

\[
m\ge
\begin{cases}
36r+6,&r\text{ odd},\\
36r,&r\text{ even}.
\end{cases}
\tag{27}
\]

Equality in \(m\ge4R_1^*\) forces \(K=2R_1^*\) 和 \(2K=m\), including the rows with nonunit adjacent differences. The first, third, 和 fifth rows of the table therefore strengthen to \(42\), 和 the fourth to \(114\), under the same prefix-closure condition. Even \(r\) remains compatible with equality at the stated arithmetic level.

## 5. THEOREM — Finite interface states 和 exact translation guards

Fix \(r\) 和 a finite-block cap \(H\). Put \(S_H=\sum_{j=0}^H19^j\). An upper bound on the number of label/block states 是

\[
18^r S_H^{r+1}
\tag{28}
\]

for states of type (5): \(r\) noncritical symbols, \(r\) finite exterior/interface blocks, 和 one center. Canonicality 和 central symmetry can only reduce the count.

Compute each raw successor using (6)–(8), enumerate the finitely many literal trims (9), 和 retain only successor blocks within the cap. Each retained edge carries its actual overflow, the translation vector from (10), 和 the input guard \(n_i\ge2\). The bound (28) requires a supplied cap; it establishes neither a universal cap nor existence of a cycle.

The next normalized digit word admits the equal-length mirrored block partition used in the proof of (6)–(8). Its intervening constant digit runs occur with matching lengths. Reversing it therefore preserves those runs, 和 equality with its reversal reduces to equality of each finite block with the reversal of its opposite block, plus central-block symmetry. Splitting concatenations at the matched segment lengths proves both implications. Hence next-output palindromicity depends only on the interface state; it can be tested exactly with \(n_1=\cdots=n_r=2\).

Consider a specified closed edge sequence with length increments \(d_0,\ldots,d_{m-1}\). Define

\[
p_0=0,\quad p_j=\sum_{t<j}d_t,\quad \Delta=p_m.
\]

After \(k\) complete traversals, phase \(j\) 有 lengths

\[
n^{(k,j)}=n^{(0)}+k\Delta+p_j.
\tag{29}
\]

**THEOREM —** Some finite initial vector permits indefinite traversal with every phase guard \(n_i\ge2\) exactly when \(\Delta_i\ge0\) for every coordinate. A sufficient initial vector, coordinatewise minimal for the guard, 是

\[
n_i^{(0)}=2-\min_{0\le j<m}p_{j,i}.
\tag{30}
\]

If \(\Delta_i<0\), equation (29) eventually violates the guard at phase zero for any finite initial length. If \(\Delta_i\ge0\), (30) 和 (29) preserve every phase guard. Every run tends to infinity exactly when every \(\Delta_i>0\). \(\square\)

If each retained edge additionally fails its exact palindrome test, a canonical realization of the initial template gives an infinite palindrome-free ordinary orbit starting after its first step. The implication follows by induction from the whole-word identities 和 the finite guards. The report 没有 such a closed edge sequence.

## 6. THEOREM — General affine returns cannot amplify every independent run

Let \(W(x)\), \(x\in\mathbb Z_{\ge0}^r\), be canonical templates with

\[
|W(x)|=B+w^{\mathsf T}x,\qquad w_i\in\mathbb Z_{>0}.
\]

For constant mirrored bands \(w_i=2\); repeated blocks may give other positive weights. Suppose, for every independent integer vector \(x\ge N\),

\[
T^m(W(x))=W(Ax+b),\qquad Ax+b\ge0,
\tag{31}
\]

where \(m\ge1\), \(A\) 和 \(b\) are integer-valued.

Then

\[
\boxed{A\ge0,\qquad w^{\mathsf T}A=w^{\mathsf T},\qquad
0\le w^{\mathsf T}b\le m.}
\tag{32}
\]

**Proof.** Equation (1), summed \(m\) times, gives

\[
0\le w^{\mathsf T}(A-I)x+w^{\mathsf T}b\le m.
\]

Increasing an individual coordinate \(x_j\) independently forces its coefficient to vanish: a positive coefficient violates the upper bound; a negative coefficient violates the lower bound. The argument establishes length conservation 和 the bound on \(w^{\mathsf T}b\). If \(A_{ij}<0\), increasing only \(x_j\) eventually makes \((Ax+b)_i<0\), contradicting (31). \(\square\)

### Graph classification

Draw an edge \(j\to i\) when \(A_{ij}>0\). Weighted conservation says

\[
w_j=\sum_iw_iA_{ij}.
\tag{33}
\]

Every column 有 an outgoing edge. An edge gives \(w_i\le w_j\). Along a directed cycle the inequalities force equal weights. Its cycle edge then consumes the whole right-hand side of (33), so its coefficient equals \(1\), 和 every other entry in the column equals \(0\). Thus directed cycles are disjoint, closed permutation components.

Vertices outside those cycles form an acyclic transient part. A path of length at least \(r\) cannot end at a transient vertex: it would repeat a vertex, enter a cycle, 和 subsequently be unable to leave. Hence a transient row of \(A^t\) vanishes for \(t\ge r\). Using

\[
x_t=A^tx_0+\sum_{j=0}^{t-1}A^jb,
\]

every transient coordinate becomes constant by time \(r\).

Therefore

\[
\boxed{\text{If every run length is unbounded, }A
\text{ must be a weight-preserving permutation matrix.}}
\tag{34}
\]

The classification excludes genuine branching or merging from a uniform affine return that grows every independent run. It allows transient coordinates when only some runs grow.

For a permutation cycle \(C\), let \(\Delta_C=\sum_{i\in C}b_i\). Each coordinate on \(C\) gains \(\Delta_C\) after \(|C|\) returns. Positive \(\Delta_C\) gives divergence to infinity, zero gives periodicity, 和 negative \(\Delta_C\) eventually makes the coordinate negative. Thus every run grows exactly when every cycle drift 是 positive, subject to the guards.

### THEOREM — Finite guard test

For any conserved nonnegative integer matrix in (32), let \(u=r\), 和 let \(p\) be the least common multiple of its directed cycle lengths. The graph classification gives \(A^{u+p}=A^u\). Set

\[
D=\sum_{j=u}^{u+p-1}A^jb.
\]

For \(t\ge u\),

\[
x_{t+p}-x_t
=(A^{t+p}-A^t)x_0+\sum_{j=t}^{t+p-1}A^jb=D,
\]

因为 the first term vanishes 和 the second sums one full period. In particular,

\[
x_{u+s+np}=x_{u+s}+nD
\quad(0\le s<p,\ n\ge0).
\tag{35}
\]

For a proven guard polyhedron \(Gx\ge h\), indefinite guard preservation holds exactly when

\[
\boxed{
Gx_t\ge h\quad(0\le t<u+p),\qquad GD\ge0.
}
\tag{36}
\]

Sufficiency follows from (35). If a row of \(GD\) 是 negative, the guard eventually fails along each residue class. The criterion applies **after** the exact return identity 和 its guards are established; it cannot turn an arbitrary proposed matrix into a decimal construction.

### Counterexamples to stronger, false claims

**THEOREM — Positive total drift alone is insufficient.** The translation \((x,y)\mapsto(x-1,y+2)\) increases total length, yet its first coordinate becomes negative from \((10,10)\) at return \(11\).

**THEOREM — Positive individual offsets are unnecessary for permutations.** The map \((x,y)\mapsto(y+2,x-1)\) gains \((1,1)\) after 两 returns. Starting from \((10,10)\), the coordinates 都 stay positive 和 diverge.

**THEOREM — The independent-tail hypothesis is essential.** The signed map

\[
(x,y)\mapsto(2x-y+1,-x+2y+1)
\]

sends \((n,n)\) to \((n+1,n+1)\), despite negative matrix entries 和 an eigenvalue \(3\). It fails the independent orthant hypothesis; (34) cannot be inferred from an identity known only along a correlated ray. These examples 是 algebraic controls, without claimed reverse 和 add realizations.

## 7. Executed validation

The reproducible program 是 [`calculation/agent215_interface_checks.py`](calculation/agent215_interface_checks.py), reproduced in full below. It uses Python's standard library. Run:

```sh
python3 calculation/agent215_interface_checks.py
```

The checks test explicit identities; they 不 perform seed searches. They cover every incoming-carry possibility for each constant symbol, \(1000\) small generated canonical templates, actual ordinary-integer addition, palindrome-test independence of band lengths, literal trimming, global residues, 和 \(1000\) consecutive steps of one explicitly defined large template. The latter starts with phases \((2,4,2)\), blocks \([1,9,10]\), \([7,9,11]\), \([4,9,12]\), center \([8,6,8]\), 和 lengths \((2002,2003,2004)\). The realization follows section 1 exactly.

**THEOREM — Finite validation facts.** The executed output below records exact finite checks only. In the long calibration, raw interface blocks grow 和 protected runs shrink. Consequently, its \(1000\) nonpalindromic outputs 不 supply a returning template or an infinite avoidance theorem.

```text
normalization: 114 symbol/carry/length cases passed
templates: 1000 seeded cases passed; J checks=678; I checks=1015
orbit calibration: 1000 exact steps passed; width 12039->12443; overflows=404; palindromic outputs=0
orbit final: protected lengths=[406, 407, 408]; block lengths=[1003, 1599, 1599]; center length=1599
orbit scope: raw blocks grew; protected runs shrank; no returning construction is claimed
outer potential: all 36 exact transitions passed
outer potential slacks, a=1..18: [(1, 1), (0, 1), (0, 0), (1, 0), (0, 0), (1, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
algebra, 1000 steps: transient=(1019, 1); permutation=(510, 510); ray-only=(1010, 1010)
positive total drift counterexample: first negative coordinate at return 11; endpoint=(-990, 2010)
arithmetic only: phases=[2]; D=[9]; min gains=[9]; base period bound=36
arithmetic only: phases=[2, 6]; D=[9, 9]; min gains=[9, 9]; base period bound=72
arithmetic only: phases=[2, 8]; D=[9, 3]; min gains=[6, 3]; base period bound=36
arithmetic only: phases=[2, 6, 10]; D=[9, 9, 9]; min gains=[9, 9, 9]; base period bound=108
arithmetic only: phases=[2, 8, 14]; D=[9, 3, 3]; min gains=[3, 3, 3]; base period bound=36
guard formula, 1000 steps: u=7; p=6; D=(6, 6, 6, 6, 6, 0, 0); endpoint=(1050, 1031, 1033, 1018, 1056, 1, 2)
guard counterexample: finite prefix passes; drift=-6; first failure=52
ALL AGENT 215 CHECKS PASSED
```

The weighted matrix control additionally exercises transient branching, cycles of lengths \(2\) 和 \(3\), signed offsets, 和 every residue in (35). A guard passes the entire prescribed finite prefix but fails at return \(52\), demonstrating 为什么 the \(GD\ge0\) condition in (36) cannot be omitted.

Repository validation: `python3 tools/verify.py --changed` returned `ALL CHECKS PASSED`. The repository rules check covered 4823 Lean files 和 287 registered projects. The changed-file scope contained 0 Lean modules 和 0 axiom-audit endpoints; the command therefore supplies repository consistency validation, without a new Lean verification of the paper proofs.

## 8. Source relationship 和 the sharpest remaining question

Primary repository sources inspected, pinned to the baseline commit:

- [`TemplateStep.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean): existing exact complementary 2-band transition.
- [`ReturnCertificate.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean): literal trimming, output-palindrome test, 和 conditional certificate soundness.
- [`CertificateCharge.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateCharge.lean) 和 [`CertificateConsequences.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateConsequences.lean): prior 2-band charge 和 gain divisibilities. Those special cases are credited here rather than presented as new.
- [`PeriodObstructions.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/PeriodObstructions.lean): the existing outer potential reused in the fully displayed table.
- [`SaturationTheorem.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/SaturationTheorem.lean): the existing saturated three-column period restriction used only for (27).
- [`WholeWordBridge.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/WholeWordBridge.lean): the exact actual-prefix evolution 和 actual saturated-prefix return theorem supplying the application to (5).
- [`Agent105ReturnTimeBound.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent105AffineComponents/Agent105ReturnTimeBound.lean) 和 the `Agent102AffineRuns` / `Agent105UniformSafeReturn` entries in `lean/registry.json`: existing scalar affine closure 和 return-time results. The multivariable independent-tail classification in section 6 uses a different hypothesis 和 conclusion.

**IDEA — Sharp next question.** For the complementary six-cycle bands, does an actual finite interface cycle exist with

\[
\boxed{m=72,\qquad (\delta_1,\delta_2)=(9,9),\qquad K=36,}
\]

with literal transitions at every phase, guarded run lengths, a canonical realization, 和 failure of the exact next-output palindrome test at every phase? These 是 the smallest simultaneous positive gains 和 return time surviving the displayed arithmetic 和 saturated-prefix restrictions for the 2-band class. Feasibility remains open here. A counterexample to a proposed cycle must be reported as rejection of the cycle, even if its numerical budget satisfies every congruence.

For wider searches, (15), (17), 和 (25) supply residue filters before interface exploration; (30) or (36) supplies a complete run-length guard check after a candidate return is obtained. The unresolved step remains finding the actual safe return.

## Appendix — Complete reproducible code

```python
#!/usr/bin/env python3
"""Focused checks for REPORT_215.md; this does not search for Lychrel seeds."""
from dataclasses import dataclass
from math import gcd
import random
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def norm(word, incoming=0):
    digits, carry, carry_sum = [], incoming, 0
    for symbol in word:
        digit, carry = (symbol + carry) % 10, (symbol + carry) // 10
        digits.append(digit)
        carry_sum += carry
    return digits, carry, carry_sum


def pair(word):
    return [a + b for a, b in zip(word, reversed(word))]


def zipper(left, right):
    assert len(left) == len(right)
    return [a + b for a, b in zip(left, right)]


def stable(symbol):
    assert 0 <= symbol <= 18 and symbol != 9
    carry = int(symbol >= 10)
    return carry, symbol - 9 * carry


@dataclass
class State:
    phases: list
    blocks: list
    center: list
    lengths: list

    def expand(self):
        half = []
        for block, symbol, size in zip(self.blocks, self.phases, self.lengths):
            half.extend(block)
            half.extend([symbol] * size)
        return half + self.center + half[::-1]

    def width(self):
        return 2 * (sum(map(len, self.blocks)) + sum(self.lengths)) + len(self.center)


def raw_step(state):
    """The exact general-r block formulas, with all outgoing carries summed."""
    assert min(state.lengths) >= 2
    phases, blocks, center = state.phases, state.blocks, state.center
    r = len(phases)
    k = [stable(s)[0] for s in phases]
    t = [stable(s)[1] for s in phases]
    following = [2 * z for z in t]
    d, u, kd = norm(blocks[0], 0)
    e, gamma, ke = norm(blocks[0][::-1], k[0])
    entrance = phases[0] + u - 10 * k[0]
    right = e[::-1] + [t[0]] if gamma == 0 else [1] + e[::-1]
    out = [zipper(d + [entrance], right)]
    epsilon = 2 - gamma
    assert sum(out[0]) == 2 * sum(blocks[0]) + epsilon * t[0] - 9 * (kd + ke)
    for j in range(1, r):
        a, b, block = phases[j - 1], phases[j], blocks[j]
        ka, kb, ta, tb = k[j - 1], k[j], t[j - 1], t[j]
        d, u, kd = norm(block, ka)
        e, v, ke = norm(block[::-1], kb)
        left = d + [b + u - 10 * kb]
        right = [a + v - 10 * ka] + e[::-1]
        if gamma == 0:
            left, right = [ta] + left, right + [tb]
        raw = zipper(left, right)
        assert len(raw) == len(block) + epsilon
        assert sum(raw) == 2 * sum(block) + epsilon * (a + b) - 9 * (
            epsilon * (ka + kb) + kd + ke)
        charge = 2 * sum(block) - (a + b) * len(block)
        raw_charge = 2 * sum(raw) - (following[j - 1] + following[j]) * len(raw)
        assert raw_charge == 2 * charge + 18 * ((ka + kb) * len(block) - kd - ke)
        out.append(raw)
    d, u, kd = norm(center, k[-1])
    central_digits = d + [phases[-1] + u - 10 * k[-1]]
    if gamma == 0:
        central_digits = [t[-1]] + central_digits
    central = pair(central_digits)
    assert len(central) == len(center) + epsilon
    assert sum(central) == 2 * sum(center) + epsilon * following[-1] - 18 * kd
    result = State(following, out, central, [n - epsilon for n in state.lengths])
    assert result.width() == state.width() + gamma
    return result, gamma


def trim(state):
    """Move actual end letters to adjacent bands; no guessed transitions."""
    phases = state.phases[:]
    blocks = [b[:] for b in state.blocks]
    center, lengths = state.center[:], state.lengths[:]
    while blocks[0] and blocks[0][-1] == phases[0]:
        blocks[0].pop()
        lengths[0] += 1
    for j in range(1, len(phases)):
        while blocks[j] and blocks[j][0] == phases[j - 1]:
            blocks[j].pop(0)
            lengths[j - 1] += 1
        while blocks[j] and blocks[j][-1] == phases[j]:
            blocks[j].pop()
            lengths[j] += 1
    while len(center) >= 2 and center[0] == center[-1] == phases[-1]:
        center = center[1:-1]
        lengths[-1] += 1
    return State(phases, blocks, center, lengths)


def invariants(state):
    result = {}
    s, b = state.phases[0], state.blocks[0]
    if gcd(s, 9) == 1:
        result["J"] = (2 * pow(s, -1, 9) * (sum(b) - s * len(b)) + state.width()) % 9
    for j in range(1, len(state.phases)):
        a, b = state.phases[j - 1:j + 1]
        difference = a - b
        if gcd(difference, 9) != 1:
            continue
        block = state.blocks[j]
        inner = 2 * sum(state.lengths[j:]) + 2 * sum(map(len, state.blocks[j + 1:])) + len(state.center)
        charge = 2 * sum(block) - (a + b) * len(block)
        result[f"I{j}"] = (pow(difference, -1, 9) * charge - len(block) - inner) % 9
    return result


def realize(q):
    assert q and q == q[::-1] and q[0] > 0
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[-1 - i] = min(9, q[i])
        d[i] = q[i] - d[-1 - i]
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        d[len(q) // 2] = q[len(q) // 2] // 2
    assert pair(d) == q and d[-1] > 0
    return int("".join(map(str, d[::-1])))


def check_normalization():
    count = 0
    for s in range(19):
        for incoming in range(2):
            for length in (1, 2, 7):
                digits, outgoing, _ = norm([s] * length, incoming)
                if s == 9:
                    expected, last = [9 * (1 - incoming)] * length, incoming
                else:
                    k, t = stable(s)
                    expected, last = [t + incoming - k] + [t] * (length - 1), k
                assert (digits, outgoing) == (expected, last)
                count += 1
    print(f"normalization: {count} symbol/carry/length cases passed")


def check_templates():
    rng = random.Random(215)
    alphabet = [s for s in range(19) if s != 9]
    invariant_counts = {"J": 0, "I": 0}
    for _ in range(1000):
        r = rng.randrange(1, 5)
        phases = [rng.choice(alphabet) for _ in range(r)]
        blocks = [[rng.randrange(19) for _ in range(rng.randrange(6))] for _ in range(r)]
        if blocks[0]:
            blocks[0][0] = rng.randrange(1, 19)
        elif phases[0] == 0:
            blocks[0] = [1]
        half = [rng.randrange(19) for _ in range(rng.randrange(4))]
        middle = [2 * rng.randrange(10)] if rng.randrange(2) else []
        state = State(phases, blocks, half + middle + half[::-1], [rng.randrange(2, 14) for _ in range(r)])
        q = state.expand()
        old = invariants(state)
        raw, gamma = raw_step(state)
        digits, actual_gamma, _ = norm(q)
        output = digits + ([1] if actual_gamma else [])
        assert gamma == actual_gamma and pair(output) == raw.expand()
        short = State(phases, blocks, state.center, [2] * r)
        short_digits, short_gamma, _ = norm(short.expand())
        short_output = short_digits + ([1] if short_gamma else [])
        assert short_gamma == gamma
        assert (output == output[::-1]) == (short_output == short_output[::-1])
        canonical = trim(raw)
        assert canonical.expand() == raw.expand()
        assert old == invariants(canonical)
        invariant_counts["J"] += int("J" in old)
        invariant_counts["I"] += sum(key.startswith("I") for key in old)
        integer = realize(q)
        integer += int(str(integer)[::-1])
        assert list(map(int, str(integer)[::-1])) == output
    print(f"templates: 1000 seeded cases passed; J checks={invariant_counts['J']}; I checks={invariant_counts['I']}")


def check_long_orbit():
    state = State([2, 4, 2], [[1, 9, 10], [7, 9, 11], [4, 9, 12]], [8, 6, 8], [2002, 2003, 2004])
    integer = realize(state.expand())
    start_width = state.width()
    initial_invariants = invariants(state)
    overflows, palindromes = 0, 0
    for _ in range(1000):
        old_width = state.width()
        raw, gamma = raw_step(state)
        integer += int(str(integer)[::-1])
        digits = list(map(int, str(integer)[::-1]))
        assert pair(digits) == raw.expand()
        assert len(digits) == old_width + gamma
        assert invariants(raw) == initial_invariants
        palindromes += int(digits == digits[::-1])
        overflows += gamma
        state = raw
    print(f"orbit calibration: 1000 exact steps passed; width {start_width}->{state.width()}; overflows={overflows}; palindromic outputs={palindromes}")
    print(f"orbit final: protected lengths={state.lengths}; block lengths={list(map(len, state.blocks))}; center length={len(state.center)}")
    print("orbit scope: raw blocks grew; protected runs shrank; no returning construction is claimed")


def check_outer_potential():
    h = [0, 0, 0, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 3]
    rows = []
    for a in range(1, 19):
        slacks = []
        for incoming in range(2):
            gamma = (a + incoming) // 10
            following = 2 * a + incoming if gamma == 0 else a % 10 + 1
            slack = 1 - 2 * gamma + h[a] - h[following]
            assert slack >= 0
            slacks.append(slack)
        rows.append(tuple(slacks))
    print("outer potential: all 36 exact transitions passed")
    print(f"outer potential slacks, a=1..18: {rows}")


def minimum_gains(phases):
    divisors = [9 // gcd(phases[0], 9)] + [9 // gcd(a - b, 9) for a, b in zip(phases, phases[1:])]
    suffix, gains = 0, [0] * len(phases)
    for j in reversed(range(len(phases))):
        current = divisors[j] * (suffix // divisors[j] + 1)
        gains[j], suffix = current - suffix, current
    return divisors, gains, suffix


def check_algebra():
    transient = permutation = ray = (10, 10)
    for _ in range(1000):
        x, y = transient
        transient = (x + y, 1)
        x, y = permutation
        permutation = (y + 2, x - 1)
        x, y = ray
        ray = (2 * x - y + 1, -x + 2 * y + 1)
        assert min(transient + permutation + ray) > 0
    print(f"algebra, 1000 steps: transient={transient}; permutation={permutation}; ray-only={ray}")
    x = (10, 10)
    first_failure = None
    for step in range(1, 1001):
        x = (x[0] - 1, x[1] + 2)
        if x[0] < 0 and first_failure is None:
            first_failure = step
    print(f"positive total drift counterexample: first negative coordinate at return {first_failure}; endpoint={x}")
    for phases in ([2], [2, 6], [2, 8], [2, 6, 10], [2, 8, 14]):
        divisors, gains, total = minimum_gains(phases)
        print(f"arithmetic only: phases={phases}; D={divisors}; min gains={gains}; base period bound={4 * total}")


def check_guard_formula():
    matrix = [
        [0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    weights = (1, 1, 2, 2, 2, 3, 6)
    offset = (3, -2, -4, 5, 1, -3, 2)
    u, period = 7, 6

    def multiply(vector):
        return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)

    def add(left, right):
        return tuple(a + b for a, b in zip(left, right))

    assert tuple(sum(weights[i] * matrix[i][j] for i in range(7)) for j in range(7)) == weights
    drift, vector = (0,) * 7, offset
    for t in range(u + period):
        if t >= u:
            drift = add(drift, vector)
        vector = multiply(vector)
    values = [(10, 12, 14, 16, 18, 20, 22)]
    for _ in range(1000):
        values.append(add(multiply(values[-1]), offset))
    for residue in range(period):
        for n in range((1000 - u - residue) // period + 1):
            assert values[u + residue + n * period] == tuple(
                x + n * d for x, d in zip(values[u + residue], drift))
    assert min(min(x) for x in values) > 0
    assert all(x[5] - x[0] >= -100 for x in values[:u + period])
    failure = next(t for t, x in enumerate(values) if x[5] - x[0] < -100)
    print(f"guard formula, 1000 steps: u={u}; p={period}; D={drift}; endpoint={values[-1]}")
    print(f"guard counterexample: finite prefix passes; drift=-6; first failure={failure}")


def main():
    check_normalization()
    check_templates()
    check_long_orbit()
    check_outer_potential()
    check_algebra()
    check_guard_formula()
    print("ALL AGENT 215 CHECKS PASSED")


if __name__ == "__main__":
    main()
```
