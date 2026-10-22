# REPORT_201 — bounded template decidability

Agent **201**; direction **1**, 因为 \((201-200)\bmod 10=1\).

## Answer

**THEOREM.** For every specified finite block bound \(b\), existence of an accepted certificate in the repository's complementary-band `Agent109.Cert` framework with \(|B|,|A|,|C|\le b\) reduces to cycle search in an explicitly bounded finite graph; neither a period bound nor a bound on the certificate's run-length thresholds needs to be assumed. More generally, the same conclusion holds for any explicitly bounded family of constant-run templates with uniform translation links, 和 those links themselves admit an exact finite decision procedure. **THEOREM.** Replacing every sufficiently long run by a capped length does **不** give an exact dynamical quotient, even for a single input run. **IDEA / remaining target.** These results supply a sound decision procedure for specified template classes, but 没有 accepted decimal certificate, 没有 decimal Lychrel integer, 和 没有 theorem bounding the necessary block size across the entire certificate class. The unrestricted decimal existence problem remains unresolved by this report.

Complete paper proofs accompany the new mathematical results below. **The new results 没有 a LEAN-VERIFIED designation.** Repository definitions were inspected at commit `c6902ac6c366ce018e68a810f58b400dda07145a`; 没有 new Lean theorem or modification of the checker accompanies this report.

## 1. Definitions 和 exact scope

Words are written with the units column first. For a column-sum word \(q\), put

\[
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,
\qquad e_i=q_i+c_i-10c_{i+1}.
\]

Append the digit \(1\) exactly when the final carry equals \(1\). Write \(E(q)\) for this entire digit word, 和

\[
T_q(q)=\operatorname{pair}(E(q)),\qquad
\operatorname{pair}(w)_i=w_i+w_{|w|-1-i}.
\]

For an ordinary positive integer with column word \(q\), \(E(q)\) gives its next integer's digits. A column word alone need 不 determine the original integer; it determines the next integer.

The concrete repository template is

\[
Q_s(G,H)=B\,c^G\,A\,(18-c)^H\,C\,(18-c)^H\,
\operatorname{rev}(A)\,c^G\,\operatorname{rev}(B),
\]

where \(s=(c,B,A,C)\), \(c\in\{1,\ldots,17\}\setminus\{9\}\), every block symbol lies in \(\{0,\ldots,18\}\), 和 \(G,H\ge2\). Superscripts on word symbols denote **repetition**, 不 exponentiation of an integer.

The precise concrete decision problem is:

> For a supplied \(b\ge0\), does some nonempty certificate accepted by `Agent109.Cert.check` 有 each state’s three finite blocks bounded in length by \(b\)?

Its period, its trimming values, 和 its lower thresholds are initially unrestricted. This differs from asking whether any bound \(b\) succeeds.

## 2. THEOREM 201.1 — exact carries 和 raw template links

For \(s\in\{0,\ldots,18\}\), a nonempty run \(s^n\), 和 incoming carry \(a\in\{0,1\}\), normalization gives the following complete table. The rightmost column gives the outgoing carry after the whole run.

| Column symbol | Incoming carry | Output digits | Outgoing carry |
|---|---:|---|---:|
| \(0\le s\le8\) | \(0\) | \(s^n\) | \(0\) |
| \(0\le s\le8\) | \(1\) | \((s+1)s^{n-1}\) | \(0\) |
| \(s=9\) | \(0\) | \(9^n\) | \(0\) |
| \(s=9\) | \(1\) | \(0^n\) | \(1\) |
| \(10\le s\le18\) | \(0\) | \((s-10)(s-9)^{n-1}\) | \(1\) |
| \(10\le s\le18\) | \(1\) | \((s-9)^n\) | \(1\) |

### Proof of the table

For \(s\le8,a=0\), every sum equals \(s<10\), so each digit equals \(s\) 和 every carry equals zero. For \(s\le8,a=1\), the first sum \(s+1\le9\) produces digit \(s+1\) 和 resets the carry to zero; the remaining columns 都 produce \(s\). For \(s=9,a=0\), every sum equals \(9\), preserving carry zero. For \(s=9,a=1\), every sum equals \(10\), producing digit zero 和 preserving carry one. For \(s\ge10,a=0\), the first sum \(s\in[10,18]\) produces \(s-10\) 和 carry one; each later sum \(s+1\in[11,19]\) produces \(s-9\) 和 preserves carry one. For \(s\ge10,a=1\), that latter calculation applies at every column. Empty tails when \(n=1\) require zero exceptions.

### Complete bookkeeping for the complementary template

Let \(N(W,a)=(D_W,e_W)\) mean same-length normalization of block \(W\) with incoming carry \(a\), retaining its outgoing carry separately. Put

\[
k(x)=\mathbf1_{x\ge10},\qquad t(x)=x-9k(x),\qquad d=18-c.
\]

For the allowed phases, \(k(c)+k(d)=1\) 和 \(t(c)+t(d)=9\). Define the five block normalizations:

\[
\begin{array}{ll}
(D_B,e_0)=N(B,0), & (D_A,e_1)=N(A,k(c)),\\
(D_C,e_2)=N(C,k(d)), & (D_{RA},e_3)=N(\operatorname{rev}(A),k(d)),\\
(D_{RB},\gamma)=N(\operatorname{rev}(B),k(c)).
\end{array}
\]

Every carry here belongs to \(\{0,1\}\). The four band-entry digits are

\[
u_0=c+e_0-10k(c),\quad u_1=d+e_1-10k(d),\quad
u_2=d+e_2-10k(d),\quad u_3=c+e_3-10k(c).
\]

Before a possible overflow digit, the complete output is

\[
D_B\,u_0\,t(c)^{G-1}\,D_A\,u_1\,t(d)^{H-1}\,D_C\,
u_2\,t(d)^{H-1}\,D_{RA}\,u_3\,t(c)^{G-1}\,D_{RB}.
\]

Thus carries through the center 和 两 个 reflected blocks 都 are fixed by the displayed normalizations; none is freely chosen.

Write \(X\oplus Y\) for entrywise addition of equal-length words. Direct re-folding gives:

| Raw block | \(\gamma=0\) | \(\gamma=1\) |
|---|---|---|
| \(B_r\) | \((D_Bu_0)\oplus(\operatorname{rev}(D_{RB})t(c))\) | \((D_Bu_0)\oplus(1\operatorname{rev}(D_{RB}))\) |
| \(A_r\) | \((t(c)D_Au_1)\oplus(u_3\operatorname{rev}(D_{RA})t(d))\) | \((D_Au_1)\oplus(u_3\operatorname{rev}(D_{RA}))\) |
| \(C_r\) | \(\operatorname{pair}(t(d)D_Cu_2)\) | \(\operatorname{pair}(D_Cu_2)\) |

For \(\gamma=0\), remove the indicated endpoint digit from each end of every normalized band. Its remaining length is \(G-2\) or \(H-2\); mirrored digits in each remaining band add to \(2t(c)\) or \(2t(d)\). The first column of the table pairs the five remaining finite pieces, including the entire center. For \(\gamma=1\), the appended leading digit shifts the reflected alignment by one. The second column pairs the left exterior with that leading one, leaves bulk lengths \(G-1,H-1\), 和 pairs the shifted interface 和 center pieces. The paired pieces in either column 都有 equal lengths. Since \(2t(d)=18-2t(c)\), 两 个 cases give the exact identity

\[
T_q(Q_s(G,H))=
Q_{(2t(c),B_r,A_r,C_r)}(G-2+\gamma,H-2+\gamma).
\tag{1}
\]

In particular,

\[
|B_r|=|B|+1,\qquad
|A_r|=|A|+2-\gamma,\qquad
|C_r|=|C|+2-\gamma.
\tag{2}
\]

These formulas agree with the inspected definitions 和 theorem `stepWord_template` in [TemplateStep.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean). The proof here includes 两 个 overflow cases independently.

## 3. THEOREM 201.2 — finite control graph for the existing checker

Fix \(b\ge0\), 和 set

\[
S_b=\sum_{a=0}^{b}19^a=\frac{19^{b+1}-1}{18},\quad
N_b=16S_b^3,\quad E_b=N_b(b+3)^4,\quad D_b=2b+2.
\tag{3}
\]

Construct the following finite directed multigraph \(\mathcal G_b\).

A vertex is any syntactically valid state \(s=(c,B,A,C)\) with each of the three block lengths at most \(b\). For each such state compute the actual \(\gamma,B_r,A_r,C_r\) from Section 2. A candidate edge chooses nonnegative trims \(j,j_1,j_2,k\) 和 succeeds exactly when

\[
\begin{aligned}
c'&=2t(c),\\
B_r&=B'(c')^j,\\
A_r&=(c')^{j_1}A'(18-c')^{j_2},\\
C_r&=(18-c')^k C'(18-c')^k,
\end{aligned}
\tag{4}
\]

the remaining blocks satisfy the bound \(b\), 和 the source's finite `StepPal` test is false. The edge weight is the integer vector

\[
\delta=(\gamma+j+j_1-2,\ \gamma+j_2+k-2).
\tag{5}
\]

The exact word update on that edge is

\[
T_q(Q_s(G,H))=Q_{s'}((G,H)+\delta)
\]

whenever the source bands are at least \(2\). To keep the next phase in the same domain, require its bands to be at least \(2\) as well.

### Proof of finiteness 和 completeness for the checker

There are \(16\) phases 和 at most \(S_b\) choices for each block, giving at most \(N_b\) vertices. Equation (2) forces

\[
j\le b+1,\qquad j_1+j_2\le b+2-\gamma,\qquad
2k\le b+2-\gamma.
\tag{6}
\]

Therefore every relevant trim lies in \(\{0,\ldots,b+2\}\). Each trim tuple determines at most one target by deleting the stated prefixes 和 suffixes, so there are at most \(E_b\) edges. This includes every trim that can occur in the original checker; 没有 arbitrary trim cutoff was imposed.

Equation (5) gives

\[
-2\le\delta_1\le2b+1,\qquad
-2\le\delta_2\le b+\left\lfloor\frac{b+2}{2}\right\rfloor.
\]

For the first upper bound, use \(j\le b+1\) 和 \(j_1\le b+2-\gamma\). For the second, use \(j_2\le b+2-\gamma\) 和 \(k\le\lfloor(b+2-\gamma)/2\rfloor\). Thus \(|\delta_i|\le D_b\), including \(b=0\).

To verify the safety guard explicitly, when \(\gamma=0\) the five finite digit pieces are

\[
X_1=D_Bu_0,\quad X_2=t(c)D_Au_1,\quad
X_3=t(d)D_Cu_2,\quad X_4=t(d)D_{RA}u_3,\quad X_5=t(c)D_{RB}.
\]

When \(\gamma=1\), they are

\[
X_1=D_Bu_0,\quad X_2=D_Au_1,\quad
X_3=D_Cu_2,\quad X_4=D_{RA}u_3,\quad X_5=D_{RB}1.
\]

In each case the intervening constant bands appear with mirrored lengths, \(|X_1|=|X_5|\), 和 \(|X_2|=|X_4|\). Comparing the complete output with its reverse, cancel the equal-length exterior pieces, then the equal constant bands, then the interfaces. The output is a palindrome exactly when

\[
X_1=\operatorname{rev}(X_5),\quad
X_2=\operatorname{rev}(X_4),\quad
X_3=\operatorname{rev}(X_3).
\tag{7}
\]

These are precisely the finite `StepPal` tests. They remain independent of \(G,H\).

Comparing (4)–(7) with [the inspected `LocalOK` definition](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean), the conditions except the lower thresholds 都 are 现在 represented by exact graph edges. The remaining conditions are exactly

\[
\lambda_i\ge(2,2),\qquad
\lambda_{i+1}\le\lambda_i+\delta_i
\tag{8}
\]

with phase indices read cyclically. Conversely, graph edges 和 thresholds satisfying (8) reconstruct every conjunct of `LocalOK`. This establishes the claimed correspondence with the existing checker.

## 4. THEOREM 201.3 — cyclic lower thresholds can be eliminated exactly

For a closed walk with successive integer weights \(\delta_0,\ldots,\delta_{p-1}\), thresholds satisfying (8) exist **if 和 only if**

\[
\Delta:=\sum_{i=0}^{p-1}\delta_i\ge0
\quad\text{coordinatewise}.
\tag{9}
\]

### Proof

Summing (8) around the cycle cancels every threshold 和 yields \(0\le\Delta\).

For the converse put \(s_0=0\), \(s_i=\sum_{a<i}\delta_a\). In each coordinate \(j\), choose

\[
\lambda_{0,j}=2-\min_{0\le i<p}s_{i,j},\qquad
\lambda_{i,j}=\lambda_{0,j}+s_{i,j}.
\tag{10}
\]

The minimum is at most zero 因为 \(s_0=0\); every threshold is at least \(2\). The inequalities except the final cyclic one 都 是 equalities. The final inequality is \(\lambda_0\le\lambda_0+\Delta\), exactly (9).

Thus existence of a bounded-block accepted certificate is equivalent to existence of a nonempty closed walk in \(\mathcal G_b\) with nonnegative total weight. A topological strongly connected component alone is insufficient.

For example, a single abstract self-loop of weight \(-1\) can be followed from counter \(5\), with floor \(2\), only three times. Conversely, at one abstract vertex the loops with weights \((2,-1)\) 和 \((-1,2)\) each fail separately, while their concatenation 有 weight \((1,1)\). Consequently **closed walks**, including combinations of simple cycles, must be considered. These are counter-system examples, 不 asserted decimal template edges.

## 5. THEOREM 201.4 — an explicit bound on the required closed walk

Let a finite directed multigraph 有 at most \(N\) vertices 和 \(E\) edges, with integer weights in \([-D,D]^r\). Put

\[
M=\max(1,D),\qquad L=((E+1)M)^{E+1}.
\tag{11}
\]

If a nonempty closed walk of nonnegative total weight exists, such a walk exists with at most \(L\) edges. The same bound holds with either additional requirement: some coordinate of the total weight is positive; or every coordinate is positive.

### Complete proof

Take a witness closed walk 和 let \(S\) be its edge support, of size \(s\le E\). The support is strongly connected: following the original cyclic walk supplies a directed route between any visited vertices. Let \(m_a\ge1\) be its edge multiplicities, \(A\) its incidence matrix, 和 \(W\) the matrix with edge weights as columns. Then

\[
Am=0,\qquad Wm\ge0.
\]

Consider real variables \(x\in\mathbb R^s,t\in\mathbb R\), subject to

\[
Ax=0,\quad \sum_a x_a=1,\quad Wx\ge0,\quad x_a\ge t\ (a\in S),\quad t\ge0.
\tag{12}
\]

Normalize \(m\) by its sum. Its coordinates 都 are positive, so (12) is feasible with \(t>0\). The feasible set is compact, since \(0\le x_a\le1\) 和 \(0\le t\le1/s\). Maximize \(t\); its maximum is positive. An extreme point attaining the maximum exists: within the compact maximizing face, successively optimize each coordinate; the resulting unique point cannot be a nontrivial midpoint of feasible points, 因为 each successive optimum would be shared by 两 个 endpoints.

At that point select \(p=s+1\) linearly independent active constraint normals. Such a selection exists: otherwise a nonzero vector orthogonal to every active normal permits sufficiently small perturbations in 两 个 directions while preserving each active constraint 和 the strict slack in every inactive constraint, contradicting extremality. The selected equalities form a nonsingular integer matrix \(F\), with integer right-hand side. Every entry of \(F\) 有 absolute value at most \(M\).

Cramer's rule makes each coordinate integral after multiplication by \(K=|\det F|\). The determinant expansion gives

\[
1\le K\le p!M^p\le(pM)^p\le((E+1)M)^{E+1}=L.
\tag{13}
\]

Set \(k_a=Kx_a\). Since \(Kt\) is a positive integer, \(k_a\ge1\) for every edge. Moreover

\[
Ak=0,\qquad Wk\ge0,\qquad \sum_a k_a=K.
\]

Replace each edge \(a\in S\) by \(k_a\) directed copies. The resulting graph is balanced at every vertex 和 retains strongly connected support. It admits an Euler circuit: start following unused edges. Balance prevents a trail from terminating at a vertex other than its start. If unused edges remain after a closed trail, strong connectivity gives a vertex on the existing trail with an unused outgoing edge: along a path toward any unused edge, the first unused edge leaves an already visited vertex. Follow another closed trail from there 和 splice it into the existing one. Each splice consumes edges; finiteness ends the procedure with every edge used. The resulting closed walk 有 length \(K\le L\) 和 total weight \(Wk\ge0\).

For positivity in a specified coordinate \(j\), add \((Wx)_j\ge t\) to (12). An original strictly positive witness 还 gives a feasible positive \(t\). After scaling, \((Wk)_j\ge Kt\ge1\). For positivity in every coordinate, add \((Wx)_j\ge t\) for each \(j\). The number of variables 和 the matrix-entry bound remain unchanged. For positivity in some coordinate, use the coordinate made positive by the original witness, or finitely enumerate the \(r\) choices. This establishes every stated version.

## 6. THEOREM 201.5 — explicitly bounded graph decision for the original certificate class

Use (3), 和 define

\[
L_b=((E_b+1)D_b)^{E_b+1}.
\tag{14}
\]

The bounded-block certificate problem from Section 1 有 a positive answer if 和 only if \(\mathcal G_b\) 有 a nonnegative closed walk of length at most \(L_b\). When the answer is positive, thresholds can be chosen with

\[
\lambda_0=(2+D_bL_b,2+D_bL_b),\qquad
2\le\lambda_{i,j}\le2+2D_bL_b.
\tag{15}
\]

An explicit finite graph for the decision 有 at most

\[
\boxed{N_b^2(L_b+1)(2D_bL_b+1)^2}
\tag{16}
\]

vertices.

### Proof 和 construction

The equivalence follows from Sections 3–5. For a walk of length \(p\le L_b\), each prefix weight lies in \([-D_bL_b,D_bL_b]^2\). Taking \(\lambda_i=\lambda_0+s_i\) gives (15) 和 satisfies the final inequality 因为 the total weight is nonnegative.

For the finite graph use vertices

\[
(v_0,v,k,z),\quad v_0,v\in V(\mathcal G_b),\quad
0\le k\le L_b,\quad z\in[-D_bL_b,D_bL_b]^2\cap\mathbb Z^2.
\]

An original edge advances \(v\), increases \(k\) by one, 和 adds its weight to \(z\), provided \(k<L_b\) 和 the new accumulated weight remains in the box. Start at \((v_0,v_0,0,0)\). A state accepts when \(v=v_0,k\ge1,z\ge0\). Add a reset edge from each accepting state to \((v_0,v_0,0,0)\). Non-reset edges 都 strictly increase \(k\), so every directed cycle contains a reset; between resets it gives exactly a nonnegative closed walk of length at most \(L_b\). Conversely every such walk yields a directed cycle. Counting the choices gives (16). This is literal finite cycle search, retaining the entire relevant accumulated drift.

The bound is an existence/termination bound, 不 a proposed practical enumeration size. The equivalent circulation feasibility problem (12), considered on possible strongly connected edge supports, is a more practical symbolic formulation.

**THEOREM / connection to decimal existence.** A cycle accepted by this procedure reconstructs a certificate accepted by the original checker. The existing [certificate-to-integer interface](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleHeads.lean), `Agent112.Admissibility.certificate_existence_of_check`, then supplies an ordinary positive integer with 没有 palindromic iterate. This report establishes a decision procedure for that certificate class; it supplies 没有 accepting instance.

### THEOREM 201.5a — the empty-block class cannot return

The graph \(\mathcal G_0\) contains zero edges. Consequently, an accepted certificate cannot 有 \(B=A=C=\varnothing\) at every phase, regardless of its period or its lower thresholds.

For \(1\le c\le8\), the empty-block normalization gives \(\gamma=0\), \(c'=2c\), 和

\[
A_r=(2c+1,\ 17-2c).
\]

An empty target \(A'\) would require \(A_r=(c')^{j_1}(18-c')^{j_2}\). Every symbol of the latter word is even; the symbols of \(A_r\) 都 are odd. This rules out every trim choice in this case.

For \(10\le c\le17\), put \(a=c-9\in\{1,\ldots,8\}\). The empty-block normalization gives \(\gamma=1\), \(c'=2a\), 和 \(B_r=(a)\). An empty target \(B'\) requires \((a)=(2a)^j\). Equality of lengths forces \(j=1\); equality of symbols then forces \(a=2a\), contradicting \(a\ge1\). These 两 cases exhaust the allowed phases.

## 7. THEOREM 201.6 — general bounded uniform-translation templates

For general \(r\ge1\), specify finite bounds \(B\ge0,H\ge1,D\ge0\). Let

\[
Q_v(x)=P_v(x)C_v\operatorname{rev}(P_v(x)),\qquad
P_v(x)=B_{v,0}a_{v,1}^{x_1}B_{v,1}\cdots a_{v,r}^{x_r}B_{v,r}.
\tag{17}
\]

Letters 都 lie in \(\{0,\ldots,18\}\); fixed blocks 都有 length at most \(B\); \(x_j\ge H\). Require the center to be symmetric with an even central symbol when its length is odd, 和 require a positive exterior symbol. These conditions make every instantiated column word realizable by ordinary decimal digits: for each reflected pair of column value \(a\), assign low digit \(a-\min(9,a)\) 和 high digit \(\min(9,a)\); assign the central column divided by \(2\) at an odd center. The high exterior digit is positive.

A uniform edge \((v,w,\delta)\), \(\|\delta\|_\infty\le D\), means the exact identity

\[
T_q(Q_v(x))=Q_w(x+\delta)
\quad\text{for every }x_j\ge H+\max(0,-\delta_j).
\tag{18}
\]

Each vertex must 也 certify that \(E(Q_v(x))\) is nonpalindromic for every \(x\ge H\). These are universal conditions on the entire indicated region, 不 fits to finitely sampled parameters.

Existence of an infinite orbit within this bounded uniform-translation class is decidable by explicitly bounded finite graphs. Before filtering, the number of template states 和 edges is at most

\[
N=19^r\left(\sum_{a=0}^{B}19^a\right)^{r+2},\qquad
E=N^2(2D+1)^r.
\tag{19}
\]

### Proof: exact finite generation of the edges

Split each fixed block into its individual columns. Put \(F=(2r+3)B\), \(p=2r+F\). Formula (17) 有 at most \(p\) nonempty constant input segments. The six carry cases from Section 2 give an output segmentation with at most \(2p+1\) fixed-symbol segments, including possible overflow. Segment lengths are \(1,x_j\), or \(x_j-1\); zero-length tails are permitted. 因为 input runs 都 are nonempty, the incoming carry at every segment 和 the final overflow \(\varepsilon\) are independent of the lengths. Segment endpoints are affine integer functions of \(x\). The total output length is

\[
L'(x)=2\sum_jx_j+f_v+\varepsilon,
\]

where \(f_v\) counts the fixed columns in \(Q_v\).

First test target length equality, namely

\[
f_v+\varepsilon=f_w+2\sum_j\delta_j.
\]

If it fails, every parameter vector is a counterexample to (18). If it holds, an unequal column can be witnessed by three segments: output segment \(a\), reflected output segment \(b\), 和 target segment \(c\). Write their index intervals as

\[
[A_a(x),B_a(x)),\quad
[L'(x)-B_b(x),L'(x)-A_b(x)),\quad
[C_c(x),D_c(x)).
\]

For a triple with symbol sum \(e_a+e_b\ne q_c\), a mismatching index exists exactly when some integer \(i\ge0\) satisfies membership in each of the three intervals. This gives **six integer linear inequalities**. Shift \(x_j=H+\max(0,-\delta_j)+y_j\), \(y_j\ge0\). The finite graph procedure in Section 8 decides each such conjunction. Every actual mismatch belongs to one of these triples, 和 every solution of a triple gives an actual mismatch. Thus absence of any such solution decides (18) exactly. Empty segments automatically contribute 没有 solution.

For uniform safety, 两 个 differently labeled output segments \(a,b\) give unequal mirrored digits precisely when

\[
A_a<B_a,\quad A_b<B_b,\quad A_a+A_b<L',\quad L'<B_a+B_b.
\tag{20}
\]

The first inequalities require nonempty intervals; the last ones require reflected overlap. Since endpoints 都 are integers, strict overlap contains an integer index. Therefore a palindrome occurs exactly when, for every differently labeled pair, at least one inequality in (20) fails. This is a finite Boolean combination of integer linear inequalities in \(x\). Shift \(x=H+y\), expand into finitely many conjunctions, 和 apply Section 8. A satisfying assignment gives a palindrome counterexample; absence of one establishes uniform safety. If 没有 differently labeled pair exists, the output is constant 和 every parameter satisfies the palindrome formula.

This completes effective graph generation 和 proves (19). It does 不 assume that a finite carry machine alone gives a finite dynamical quotient.

### Proof: infinite orbit versus a bounded growing return

For a graph of exact translations with only the source 和 target lower-bound guards, a nonnegative closed walk can be repeated forever from sufficiently large initial counters. To require growth in every band, test positive displacement in every coordinate; to require unbounded total length, test nonnegative nonzero displacement. Section 5 gives the same bound (11) for 两 个 versions, 和 Section 6's construction uses at most

\[
N^2(L+1)(2DL+1)^r
\]

vertices.

For unbounded total length, the accepting condition includes \(z\ge0\) 和 \(z\ne0\); for growth of every band, it includes \(z_j>0\) for each \(j\). Here \(r\) counts independent mirrored run pairs; the displayed word contains \(2r\) variable run slots.

Conversely, an infinite ordinary positive reverse-add orbit 有 unbounded values: reversal of a positive integer is positive, so each step strictly increases the integer. Therefore its lengths, 和 hence its counter vectors within a finite template family, cannot stay in a finite set. Some control vertex occurs with infinitely many distinct counter vectors. Any infinite sequence in \(\mathbb N^r\) contains an earlier vector coordinatewise at most a later one: for one coordinate, either some value occurs infinitely often or an infinite increasing subsequence can be selected; retain a nondecreasing subsequence in the first coordinate 和 induct on the remaining coordinates. Apply this to the pairwise distinct vectors at that vertex. The intervening closed walk 有 nonnegative nonzero displacement. Section 5 bounds its length.

Safety concerns the **next** digit output. For a successful cycle, realize its initial column word as an integer, then choose its first output as the Lychrel seed. Every iterate of that seed is nonpalindromic by the vertex safety tests. 没有 claim about the original representative's own palindromicity is needed.

**IDEA / scope boundary.** This is a complete decision procedure for the stated \((r,B,H,D)\)-bounded uniform-translation class. It does 不 establish that every orbit described informally by “\(r\) runs + bounded blocks” admits such a representation. In particular, length-comparison guards, disappearing runs, newly created runs, unrestricted merging of counters, 和 unbounded shifts require additional arguments. For the concrete checker of Sections 1–6, \(H=2\) 和 \(D=D_b\) were derived rather than left as extra assumptions.

## 8. THEOREM 201.7 — explicit finite arithmetic graph used in Section 7

Given an integer matrix \(A\in\mathbb Z^{m\times d}\) 和 vector \(b\in\mathbb Z^m\), define

\[
M_j=\max\left(|b_j|,\sum_{\ell=1}^{d}|A_{j\ell}|\right),\qquad
R=\prod_{j=1}^{m}(2M_j+1).
\]

The existence of \(z\in\mathbb N^d\) satisfying \(Az=b\) is equivalent to reachability of zero from \(b\) in the finite graph with states

\[
p\in\prod_j([-M_j,M_j]\cap\mathbb Z)
\]

和 edges, for each binary vector \(u\in\{0,1\}^d\),

\[
p\longrightarrow\frac{p-Au}{2}
\]

whenever every coordinate is integral. If a solution exists, one exists with every coordinate less than \(2^R\).

### Complete proof

Each edge stays inside the box 因为

\[
\left|\frac{p_j-(Au)_j}{2}\right|
\le\frac{M_j+\sum_\ell|A_{j\ell}|}{2}\le M_j.
\]

If \(z=\sum_{k=0}^{t-1}2^ku_k\) satisfies \(Az=b\), use a common binary length for the coordinates 和 define

\[
p_k=\frac{b-A\sum_{h<k}2^hu_h}{2^k}.
\]

The remaining binary tail makes every \(p_k\) integral. Then \(p_0=b,p_t=0\), 和 \(p_{k+1}=(p_k-Au_k)/2\). The box estimate keeps this whole path in the finite graph. Conversely, multiply the recurrence along any accepting path by the successive powers of \(2\); telescoping gives \(b=A\sum_k2^ku_k\), a nonnegative integer solution. When \(b=0\), the empty path encodes \(z=0\).

A shortest accepting path cannot repeat a state: deleting the intervening loop leaves an accepting path. Thus it 有 at most \(R-1\) edges, so its encoded coordinates are less than \(2^R\). This is an explicit termination 和 witness bound, including negative matrix entries 和 negative right-hand sides.

For inequalities \(Az\le b\), introduce nonnegative integer slack variables 和 solve \([A\ I](z,s)=b\). Convert strict inequalities using integrality; for example \(a\cdot z<b\) becomes \(a\cdot z\le b-1\). Negation is handled by reversing sign 和 subtracting one. A finite Boolean combination becomes a finite disjunction of conjunctions. Apply the construction to each conjunction. This supplies the exact finite arithmetic procedure used above, without an unproved cutoff or an external arithmetic oracle.

## 9. THEOREM 201.8 — every fixed independent run cap fails

For every integer \(K\ge2\), cap each maximal run length \(n\) to \(\min(n,K)\), retaining its entire symbol sequence. This operation fails to give an exact one-step quotient of \(T_q\).

### Proof 和 counterexample

Use the symmetric valid column words \((10)^K\) 和 \((10)^{K+1}\). Each can be realized by the corresponding number of decimal digits \(5\). Their capped run descriptions coincide. Section 2's carry table gives

\[
E((10)^n)=0\,1^{n-1}\,1,
\qquad T_q((10)^n)=1\,2^{n-1}\,1.
\]

The final \(1\) in the first word is the overflow digit. In the folded word, each interior pair adds to \(2\), 和 the 两 exterior columns equal \(1\). Thus the successor middle lengths for the 两 inputs cap to \(K-1\) 和 \(K\), respectively. The abstract successors differ despite identical abstract inputs. This holds for every proposed fixed cap.

The 两 个 inputs 都 reach a palindrome after 两 reverse-add steps: after the first step the new column word contains only \(1,2\), so normalization of that symmetric word uses carry zero in every column 和 gives a palindrome. This counterexample invalidates the capping construction; it does 不 establish undecidability of bounded template existence.

## 10. Validation code 和 observed output

**THEOREM / validation scope.** The proofs above do 不 rely on numerical orbit sampling. The accompanying program checks the carry formulas, 两 个 overflow cases of the raw identity, the finite palindrome test, 和 the cap counterexample. It 也 repeats the explicitly abstract growing closed walk for \(1000\) laps, 和 compares direct integer reverse-add against carry/fold implementations for \(1000\) steps of one prescribed realization of \((10)^4\). That integer reaches a palindrome at time \(2\), as required by Section 9; it is **不** a Lychrel construction.

Run:

```bash
python3 calculation/agent201_template_checks.py
```

Observed output:

```text
carry cases: 114 passed
raw identity, block lengths, palindrome test: 864 passed; overflow counts={0: 504, 1: 360}
empty-block obstruction: all 16 phases passed
run-cap obstruction: K=2,3,7,20 passed
K=3 outputs: ((1, 1), (2, 2), (1, 1)) ((1, 1), (2, 3), (1, 1))
negative-drift self-loop: starting at 5 with floor 2 allows 3 steps
abstract growing closed walk: 1000 laps, 2000 edges; final=[1003, 1003]; coordinate minima=[3, 2]
decimal implementation check: seed=9911; 1000 steps passed; first positive-time palindrome=2; final digits=437
```

The full executable source appears in Appendix A, 和 separately at `calculation/agent201_template_checks.py`. 没有 large seed enumeration or period search was used.

The supplied executable validates the displayed identities 和 examples. A complete implementation of the bounded certificate decision procedure remains separate work.

## 11. Sharpest open question

**IDEA — next exact target.** Does any finite \(b\) give the graph \(\mathcal G_b\) a closed walk with componentwise nonnegative total weight? A positive answer yields an accepted original certificate through Sections 3–6. A negative answer for one specified \(b\) excludes that entire bounded-block certificate class, with 没有 period or lower-threshold loophole. A negative answer for every \(b\) requires a new uniform obstruction; running larger finite searches alone does 不 supply it.

**IDEA — broader completeness question.** Can every forever-valid bounded-run template orbit be represented by finitely many independent-counter phases with uniformly bounded translations 和 only lower-bound guards? Section 7 resolves the decision problem once those hypotheses are established. It does 不 establish that representation theorem.

## 12. Sources inspected 和 verification status

The source links below are pinned to the inspected commit, so later changes do 不 alter this report's references.

| Source | Role in this report |
|---|---|
| [TemplateStep.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean) | Exact definitions of normalization, raw blocks, phase update, 和 whole-template identity |
| [ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean) | `State`, `Link`, `StepPal`, `LocalOK`, 和 original checker semantics |
| [AdmissibleCenters.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleCenters.lean) | Existing center realizability interface |
| [AdmissibleHeads.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleHeads.lean) | Existing `certificate_existence_of_check` endpoint |
| [Agent102AffineDecision.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent102AffineRuns/Agent102AffineDecision.lean) | Prior static affine-word decision work; this report adds a bounded closed-walk argument |
| [Agent105AffineOrbit.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent105UniformSafeReturn/Agent105AffineOrbit.lean) | Prior fixed-time affine closure; a fixed-time statement alone does 不 bound certificate period |

**THEOREM / status.** The new results are paper mathematics with the displayed proofs, plus the recorded targeted checks. A changed-files repository check for this report does 不 recompile or independently re-audit the unchanged Lean dependency chain. 没有 result in this report is promoted to LEAN-VERIFIED.

The required repository check completed successfully:

```text
[rules] 4823 Lean files, 287 projects, OK
[changed] against origin/main: 0 new/changed Lean file(s); building 0 module(s); auditing 0 project(s)
[build] up to 1 Lean file(s) at a time
[build] OK
[axioms] 0 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

## Appendix A. Complete validation program

```python
#!/usr/bin/env python3
"""Targeted checks for REPORT_201.md; no seed search or existence claim."""

from itertools import product


def norm(word, carry=0):
    out = []
    for symbol in word:
        total = symbol + carry
        out.append(total % 10)
        carry = total // 10
    return out, carry


def normalize(word):
    out, carry = norm(word)
    return out + ([carry] if carry else [])


def pair(word):
    return [a + b for a, b in zip(word, reversed(word))]


def folded_step(word):
    return pair(normalize(word))


def template(c, B, A, C, G, H):
    assert G >= 0 and H >= 0
    left = B + [c] * G + A + [18 - c] * H
    return left + C + left[::-1]


def raw(c, B, A, C):
    kc, kd = int(c >= 10), int(18 - c >= 10)
    t, v = c - 9 * kc, 18 - c - 9 * kd
    DB, e0 = norm(B, 0)
    DA, e1 = norm(A, kc)
    DC, e2 = norm(C, kd)
    DRA, e3 = norm(A[::-1], kd)
    DRB, gamma = norm(B[::-1], kc)
    u0 = c + e0 - 10 * kc
    u1 = 18 - c + e1 - 10 * kd
    u2 = 18 - c + e2 - 10 * kd
    u3 = c + e3 - 10 * kc
    add = lambda a, b: [x + y for x, y in zip(a, b)]
    if gamma == 0:
        Br = add(DB + [u0], DRB[::-1] + [t])
        Ar = add([t] + DA + [u1], [u3] + DRA[::-1] + [v])
        Cr = pair([v] + DC + [u2])
        blocks = (DB + [u0], [t] + DA + [u1],
                  [v] + DC + [u2], [v] + DRA + [u3], [t] + DRB)
    else:
        assert gamma == 1
        Br = add(DB + [u0], [1] + DRB[::-1])
        Ar = add(DA + [u1], [u3] + DRA[::-1])
        Cr = pair(DC + [u2])
        blocks = (DB + [u0], DA + [u1], DC + [u2],
                  DRA + [u3], DRB + [1])
    X1, X2, X3, X4, X5 = blocks
    step_pal = X1 == X5[::-1] and X2 == X4[::-1] and X3 == X3[::-1]
    return 2 * t, Br, Ar, Cr, gamma, step_pal


def run_lengths(word):
    out = []
    for x in word:
        if out and out[-1][0] == x:
            out[-1] = (x, out[-1][1] + 1)
        else:
            out.append((x, 1))
    return out


def cap(word, threshold):
    return tuple((x, min(n, threshold)) for x, n in run_lengths(word))


def realize(q):
    assert q == q[::-1] and q[0] > 0
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[i] = q[i] - min(9, q[i])
        d[-1 - i] = min(9, q[i])
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        d[len(q) // 2] = q[len(q) // 2] // 2
    assert pair(d) == q and d[-1] > 0
    return sum(x * 10**i for i, x in enumerate(d))


def digits(n):
    return [int(x) for x in str(n)[::-1]]


def main():
    count = 0
    for s, incoming, length in product(range(19), range(2), (1, 2, 7)):
        out, terminal = norm([s] * length, incoming)
        if s <= 8:
            expected, last = [s + incoming] + [s] * (length - 1), 0
        elif s == 9:
            expected, last = [9 * (1 - incoming)] * length, incoming
        else:
            expected = [s + incoming - 10] + [s - 9] * (length - 1)
            last = 1
        assert (out, terminal) == (expected, last)
        count += 1
    print(f"carry cases: {count} passed")

    scenarios = (
        ([], [], []),
        ([1], [9], [0]),
        ([10], [9, 10], [18]),
        ([9, 0, 18], [8, 9, 10], [2, 8, 2]),
        ([0], [18], [0, 0]),
        ([18, 9], [0, 9, 18], [10, 4, 10]),
    )
    count = 0
    overflow_counts = {0: 0, 1: 0}
    for c, blocks, G, H in product(
            [x for x in range(1, 18) if x != 9], scenarios, (2, 3, 7), (2, 3, 7)):
        B, A, C = blocks
        nxt, Br, Ar, Cr, gamma, step_pal = raw(c, B, A, C)
        q = template(c, B, A, C, G, H)
        assert folded_step(q) == template(nxt, Br, Ar, Cr, G - 2 + gamma, H - 2 + gamma)
        assert len(Br) == len(B) + 1
        assert len(Ar) == len(A) + 2 - gamma
        assert len(Cr) == len(C) + 2 - gamma
        e = normalize(q)
        assert step_pal == (e == e[::-1])
        count += 1
        overflow_counts[gamma] += 1
    print(f"raw identity, block lengths, palindrome test: {count} passed; "
          f"overflow counts={overflow_counts}")

    for c in [x for x in range(1, 18) if x != 9]:
        nxt, Br, Ar, Cr, gamma, step_pal = raw(c, [], [], [])
        if c <= 8:
            assert gamma == 0 and nxt == 2 * c
            assert Ar == [2 * c + 1, 17 - 2 * c]
            assert all(x % 2 == 1 for x in Ar)
            assert nxt % 2 == 0 and (18 - nxt) % 2 == 0
        else:
            a = c - 9
            assert gamma == 1 and nxt == 2 * a and Br == [a]
            assert Br != [nxt]
    print("empty-block obstruction: all 16 phases passed")

    for K in (2, 3, 7, 20):
        a, b = [10] * K, [10] * (K + 1)
        assert cap(a, K) == cap(b, K)
        assert folded_step(a) == [1] + [2] * (K - 1) + [1]
        assert folded_step(b) == [1] + [2] * K + [1]
        assert cap(folded_step(a), K) != cap(folded_step(b), K)
    print("run-cap obstruction: K=2,3,7,20 passed")
    print("K=3 outputs:", cap(folded_step([10] * 3), 3),
          cap(folded_step([10] * 4), 3))

    # A topological cycle alone cannot certify indefinitely viable counters.
    decrement = 5
    admissible_steps = 0
    while decrement - 1 >= 2:
        decrement -= 1
        admissible_steps += 1
    assert admissible_steps == 3
    print("negative-drift self-loop: starting at 5 with floor 2 allows 3 steps")

    # Neither one-edge cycle is viable forever, but their concatenation grows.
    abstract = [3, 3]
    minimum = abstract[:]
    for _ in range(1000):
        for delta in ((2, -1), (-1, 2)):
            abstract = [a + d for a, d in zip(abstract, delta)]
            minimum = [min(a, b) for a, b in zip(minimum, abstract)]
            assert min(abstract) >= 2
    assert abstract == [1003, 1003]
    print(f"abstract growing closed walk: 1000 laps, 2000 edges; "
          f"final={abstract}; coordinate minima={minimum}")

    # No decimal Lychrel construction is claimed. This is one prescribed
    # canonical realization, used to compare two exact implementations.
    q = [10] * 4
    n = realize(q)
    initial = n
    first_palindrome = None
    for t in range(1001):
        ds = digits(n)
        if t > 0 and ds == ds[::-1] and first_palindrome is None:
            first_palindrome = t
        if t == 1000:
            break
        expected = n + int(str(n)[::-1])
        assert normalize(pair(ds)) == digits(expected)
        assert folded_step(pair(ds)) == pair(digits(expected))
        n = expected
    print(f"decimal implementation check: seed={initial}; 1000 steps passed; "
          f"first positive-time palindrome={first_palindrome}; final digits={len(str(n))}")


if __name__ == "__main__":
    main()
```
