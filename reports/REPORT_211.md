# Agent #211 — Direction 1: finite graphs for separated run templates

## Answer in one paragraph

**THEOREM / scope:** A complete, explicitly bounded finite-graph reduction holds for constant-run templates with a fixed bound on the interface blocks at **every phase**, provided long runs remain separated from those blocks by the quantitative threshold stated below. The graph must retain integer run-length displacements: clipping lengths, even together with arbitrary fixed residue information, fails to define a deterministic quotient. A second complete obstruction shows that a palindrome-free orbit cannot contain 3 consecutive column-sum words whose maximal runs 都有 length at least 3; short interfaces are unavoidable. The report supplies complete carry proofs, an executable symbolic successor 和 decision procedure, 和 1000-step independent arithmetic audits of each concrete numerical example. **没有 decimal Lychrel construction is supplied.** The unrestricted reduction for templates bounded only at return times remains open; the missing hypothesis is identified explicitly. **LEAN-VERIFIED status:** 没有 new Lean formalization is claimed.

## 1. Definitions 和 exact scope

Write \(R(n)=n+\operatorname{rev}_{10}(n)\). For a positive integer with canonical decimal digits \(d_0,\ldots,d_{L-1}\), indexed from the units end, put

\[
q_i=d_i+d_{L-1-i}.
\]

The operation \(T\) in the report acts on the complete column-sum word: normalize \(q\) with decimal carries, append the final carry when present, then fold the resulting digit word against its reversal. Thus \(T(q(n))=q(R(n))\). A symbol such as \(10\), \(14\), or \(16\) inside a displayed word denotes **one column-sum symbol**. The notation \(s^a\) denotes repetition, including the empty word when \(a=0\).

**THEOREM 1 — Realizability.** A finite word \(q\) is the column-sum word of a positive canonical decimal integer exactly when:

\[
L\ge1,\qquad q=q^{\mathrm{rev}},\qquad
0\le q_i\le18,\qquad q_0\ge1,
\]

with the additional condition that the middle symbol is even when \(L\) is odd.

**Proof.** Necessity follows from the definition, the nonzero leading digit, 和 the self-paired middle digit. For sufficiency, for each pair \(i<j=L-1-i\), assign

\[
d_i=\max(0,q_i-9),\qquad d_j=\min(9,q_i).
\]

The digits belong to \(\{0,\ldots,9\}\), their sum equals \(q_i\), 和 \(d_{L-1}=\min(9,q_0)>0\). At an unpaired middle position assign \(d_i=q_i/2\). For \(L=1\), evenness 和 positivity give a nonzero digit directly. The assignments construct the required integer. \(\square\)

Fix integers \(r\ge1\), \(B\ge0\), 和 set

\[
H=B+5.
\]

Define \(\mathcal C_{r,B}\) to consist of realizable words with a decomposition

\[
q=b_0s_1^{n_1}b_1\cdots s_k^{n_k}b_k,
\qquad 1\le k\le r,
\tag{1}
\]

where \(n_i\ge H\), every gap satisfies \(|b_j|\le B\), 和 each displayed band is a **maximal constant run**. The gaps include the exterior blocks. Since \(B<H\), the displayed bands are exactly the maximal runs of length at least \(H\); the decomposition is unique. Symmetry forces

\[
s_i=s_{k+1-i},\quad n_i=n_{k+1-i},\quad
b_j=b_{k-j}^{\mathrm{rev}}.
\]

The decision problem below asks for **existence from some seed**, with every successive column-sum word in \(\mathcal C_{r,B}\). It excludes prescribed-seed reachability, periodic rather than constant bands, 和 a bound imposed only on the return phase. Each requires a separate result.

## 2. THEOREM 2 — Full carry law 和 exact next-palindrome test

Set

\[
c_0=0,\qquad c_{i+1}=f_{q_i}(c_i),\qquad
e_i=q_i+c_i-10c_{i+1},
\]

where

\[
f_s(c)=
\begin{cases}
0,&0\le s\le8,\\
c,&s=9,\\
1,&10\le s\le18.
\end{cases}
\tag{2}
\]

Let \(h=c_L\in\{0,1\}\). If \(h=0\), the digit word 有 length \(L\): its leading column receives \(q_{L-1}+c_{L-1}\ge q_0>0\), so its leading digit remains nonzero. If \(h=1\), append \(e_L=1\), obtaining length \(L+1\).

**Exact folding, \(h=0\):**

\[
T(q)_i=2q_i+c_i+c_{L-1-i}-10(c_{i+1}+c_{L-i}),
\qquad 0\le i<L.
\tag{3}
\]

**Exact folding, \(h=1\):**

\[
T(q)_0=T(q)_L=q_0-10c_1+1,
\tag{4}
\]

\[
T(q)_i=q_i+q_{i-1}+c_i+c_{L-i}
-10(c_{i+1}+c_{L-i+1}),\qquad 1\le i<L.
\tag{5}
\]

Equations \(3\)–\(5\) follow by substituting the emitted digits into the fold. The reflection index is \(L-1-i\) without overflow 和 \(L-i\) with overflow; in the latter case symmetry gives \(q_{L-i}=q_{i-1}\).

The complete next-palindrome criterion is

\[
\boxed{
\begin{aligned}
h=0:&\quad e=e^{\mathrm{rev}}
\iff (\forall i)\ q_i\le9,\\
h=1:&\quad e=e^{\mathrm{rev}}
\iff (\forall i)\ q_i\in\{0,11\}.
\end{aligned}}
\tag{6}
\]

### Proof of \(6\), without overflow

Symmetry of the output implies

\[
c_i-c_{L-1-i}=10(c_{i+1}-c_{L-i}).
\]

The left side belongs to \(\{-1,0,1\}\), while the right side belongs to \(\{-10,0,10\}\). Consequently

\[
c_i=c_{L-1-i},\qquad c_{i+1}=c_{L-i}.
\]

Combining the first equality at \(i\) with the second at \(i+1\) gives \(c_{i+2}=c_i\) for \(0\le i\le L-2\). Moreover \(c_0=0\), 和 the second equality at \(i=0\) gives \(c_1=c_L=0\). Every carry vanishes, so \(q_i\le9\). When \(L=1\), the identities \(c_0=c_1=0\) give the conclusion directly.

Conversely, if every \(q_i\le9\), induction from \(c_0=0\) gives zero at every carry position. The emitted word equals the symmetric word \(q\).

### Proof of \(6\), with overflow

Output symmetry requires \(e_0=e_L=1\), so

\[
q_0-10c_1=1.
\]

If \(c_1=0\), then \(q_0=q_{L-1}=1\), making a final carry impossible: the final column receives at most \(1+1=2\). Therefore

\[
q_0=11,\qquad c_1=c_L=1.
\]

For \(k=1,\ldots,L-1\), maintain the induction hypotheses

\[
q_{k-1}=11c_k,\qquad c_{L-k+1}=c_k.
\]

The equality \(e_k=e_{L-k}\) gives

\[
q_k+c_k-10c_{k+1}
=q_{k-1}+c_{L-k}-10c_{L-k+1}
=c_k+c_{L-k},
\]

hence

\[
q_k=10c_{k+1}+c_{L-k}.
\]

Put \(a=c_{k+1}\), \(b=c_{L-k}\). Symmetry of the source gives

\[
b=\mathbf1_{\{q_k+c_{L-k-1}\ge10\}}.
\]

If \(a=0\), then \(q_k=b\le1\), so the last displayed carry must be \(b=0\). Thus \(q_k=0=11a\). If \(a=1\), then \(q_k=10+b\ge10\), forcing \(b=1\), so \(q_k=11=11a\). Each case gives \(b=a\), closing the induction.

For the converse, write \(q_i=11a_i\), where \(a_i\in\{0,1\}\). Positivity at the exterior gives \(a_0=a_{L-1}=1\). Set \(a_{-1}=a_L=0\). Equation \(2\) gives \(c_{i+1}=a_i\), 和 the full digit word is

\[
e_i=a_i+a_{i-1},\qquad 0\le i\le L.
\]

Reflection exchanges the summands, proving symmetry. For \(L=1\), the required value \(q_0=11\) violates realizability's even-center condition, so the overflowing palindrome case is empty. \(\square\)

**Consequence of THEOREM 2.** For a fixed symbol skeleton with positive run lengths, the overflow bit 和 next-palindrome status are independent of those lengths. The carry transfer through any run is independent of its positive length by the idempotence \(f_s\circ f_s=f_s\).

## 3. THEOREM 3 — Exact finite-state transition on separated bands

For a run \(s^n\) entered with carry \(\alpha\), put

\[
\kappa=f_s(\alpha),\qquad
u=s+\alpha-10\kappa,\qquad z=s-9\kappa.
\]

The emitted digit word on that run is exactly

\[
u\,z^{n-1}.
\tag{7}
\]

The first column receives \(\alpha\); every subsequent column receives \(\kappa\), 因为 \(f_s(\kappa)=\kappa\). The final carry is \(\kappa\). Equation \(7\) explicitly covers the reset-to-zero, neutral, 和 reset-to-one cases in \(2\).

Consider a source band on positions \([a,b]\), of length \(n=b-a+1\ge3\), 和 its mirrored band. Let \(\alpha\), \(\beta\) be their respective incoming carries.

For \(s\ne9\), write

\[
\kappa(s)=\mathbf1_{\{s\ge10\}},\qquad F(s)=2s-18\kappa(s).
\]

When \(h=0\), equation \(3\) gives the exact word on \([a,b]\):

\[
\bigl(F(s)+\alpha-\kappa(s)\bigr)
F(s)^{n-2}
\bigl(F(s)+\beta-\kappa(s)\bigr).
\tag{8}
\]

When \(s=9\), the corresponding whole interval is

\[
\bigl(18-9(\alpha+\beta)\bigr)^n.
\tag{9}
\]

Thus, without overflow, the marked interval \([a+1,b-1]\) always gives a constant core of length \(n-2\).

With overflow, for \(a+1\le i\le b\), the adjacent symbols \(q_{i-1},q_i\) equal \(s\). Equation \(5\) gives \(F(s)\) when \(s\ne9\), since the relevant carries inside each mirrored band have stabilized to \(\kappa(s)\). For \(s=9\), the source-direction carries equal \(\alpha\), the reflected-direction carries equal \(\beta\), 和 the output again equals \(18-9(\alpha+\beta)\). The marked core is therefore \([a+1,b]\), of length \(n-1\).

The remaining positions are completely determined by the finite gaps 和 the boundary carry bits. Their sizes are:

| Case | Core length | Raw interior gap length | Raw exterior gap length |
| --- | ---: | ---: | ---: |
| \(h=0\) | \(n_i-2\) | \(\lvert b_j\rvert+2\) | \(\lvert b_j\rvert+1\) |
| \(h=1\) | \(n_i-1\) | \(\lvert b_j\rvert+1\) | \(\lvert b_j\rvert+1\) |

Extend every core through adjacent equal symbols until it occupies a maximal output run. If different cores remain distinct, the exact new lengths are

\[
n_i'=n_i+\delta_i,
\tag{10}
\]

where the integer displacement vector \(\delta\) 和 the residual gap words depend only on the finite source skeleton. Explicit bounds are

\[
-2\le\delta_i\le2B+2\quad(h=0),\qquad
-1\le\delta_i\le2B+1\quad(h=1).
\tag{11}
\]

For example, in the first case a core loses \(2\) positions, then can absorb at most \(B+2\) positions from each neighboring raw gap. Exterior bands obey at least as strong a bound. The second case loses \(1\) position 和 can absorb at most \(B+1\) from each side. Merging decisions depend only on the intervening finite words, so they are independent of the lengths too. The argument establishes \(10\) uniformly for symmetric admissible assignments of run lengths. \(\square\)

## 4. THEOREM 4 — Explicit graph, cycle criterion, 和 witness bound

Define

\[
S_B=\sum_{j=0}^{B}19^j=\frac{19^{B+1}-1}{18},
\qquad
N(r,B)=\sum_{k=1}^{r}2^k19^k S_B^{k+1}.
\tag{12}
\]

An explicitly constructible finite directed graph with at most \(N(r,B)\) vertices satisfies:

1. A positive ordinary reverse-add orbit with nonpalindromic outputs at every step, whose column-sum words remain in \(\mathcal C_{r,B}\), exists **if 和 only if** the graph contains a directed cycle with componentwise nonnegative total drift.
2. Such an orbit whose persistent long bands 都 tend to infinity exists **if 和 only if** the graph contains a directed cycle with componentwise strictly positive total drift.
3. A successful cycle can be chosen with period \(m\le N(r,B)\). Its starting band lengths can be chosen at most

\[
H+2N(r,B)+1=B+2N(r,B)+6.
\tag{13}
\]

Starting with the first emitted integer gives a Lychrel seed whenever the successful cycle exists. Its decimal width is at most

\[
r\bigl(B+2N(r,B)+6\bigr)+(r+1)B+1.
\tag{14}
\]

The theorem decides existence within the stated class. A successful cycle instance remains to be found.

### Construction of the graph

For \(k=1,\ldots,r\), a vertex records

\[
v=(s_1,\ldots,s_k; b_0,\ldots,b_k; \varepsilon_1,\ldots,\varepsilon_k),
\]

where \(\varepsilon_i\in\{0,1\}\) records \(n_i\bmod2\). Impose symmetry, maximality, the gap bound, positive exterior, 和 center realizability. The parity vector retains the even-center condition through every width change. Discard invalid descriptions. There are at most \(19^kS_B^{k+1}2^k\) descriptions before discarding, giving \(12\).

Choose the representative lengths

\[
\widehat n_i=H+((\varepsilon_i-H)\bmod2)\in\{H,H+1\}.
\tag{15}
\]

Perform one exact carry step on the representative. Every marked output core 有 length at least \(H-2=B+3\), while every raw gap 有 length at most \(B+2\). Hence the maximal output runs of length **strictly greater than \(B+2\)** are exactly those containing marked cores.

Retain an edge precisely when:

- The representative's emitted digit word is nonpalindromic, using \(6\).
- There are exactly \(k\) output maximal runs longer than \(B+2\), so different marked cores remain distinct.
- Every residual gap 有 length at most \(B\).

The successor records those output run symbols, gaps, 和 length parities. Label the edge by

\[
\delta_i=\widehat n_i'-\widehat n_i.
\]

Theorem 3 makes the successor 和 displacement exact for **every** symmetric length assignment with the recorded parities 和 lengths at least \(H\). A representative output band can be of length \(H-2\) or \(H-1\); that is allowed when constructing the edge. The representative identifies the symbolic identity. Actual iteration later imposes the guard \(n_i\ge H\) at every phase. Rejecting an edge solely 因为 its shortest representative violates the next guard would be an error.

Each vertex 有 at most one outgoing edge. The graph is therefore deterministic, with integer vector weights.

### Necessity: reduction of an actual infinite orbit

Assume an orbit remains in \(\mathcal C_{r,B}\). Every source band produces a core of length at least \(B+3\). Such a core cannot fit in a permitted output gap of length at most \(B\); it must belong to an output long band. Conversely, an output long band cannot arise entirely inside a raw gap of length at most \(B+2<H\). Thus every output long band contains a source core, 和 the long-band count cannot increase.

The count is a positive integer at most \(r\), so after finitely many mergers it stabilizes at some \(k\ge1\). On that tail the core-to-band correspondence is bijective. The exact nonmerging graph applies at every step.

A deterministic infinite path in a finite graph eventually follows a directed cycle. Write its edge weights as \(\delta^{(0)},\ldots,\delta^{(m-1)}\), 和 put

\[
\Delta=\sum_{j=0}^{m-1}\delta^{(j)}.
\tag{16}
\]

Successive visits to its starting vertex 有 length vectors

\[
\boldsymbol n,\quad \boldsymbol n+\Delta,\quad
\boldsymbol n+2\Delta,\ldots.
\]

Any negative coordinate of \(\Delta\) eventually violates \(n_i\ge H\). Hence \(\Delta_i\ge0\) for every coordinate. If every persistent band tends to infinity, every \(\Delta_i>0\).

### Sufficiency: padding one cycle into an ordinary infinite orbit

Suppose a graph cycle satisfies \(\Delta\ge0\). Define the prefix displacements

\[
P_i(t)=\sum_{j=0}^{t-1}\delta_i^{(j)},\qquad 0\le t\le m.
\]

For each coordinate choose the smallest integer with the required starting parity satisfying

\[
n_i\ge H-\min_{0\le t\le m}P_i(t).
\tag{17}
\]

Mirrored coordinates 有 equal displacements 和 equal starting parities, so the choices respect symmetry. Each edge displacement is at least \(-2\), giving

\[
H\le n_i\le H+2m+1\le H+2N(r,B)+1.
\]

At lap \(a\ge0\), phase \(t\), the actual length is

\[
n_i+P_i(t)+a\Delta_i\ge H.
\]

The carry identities therefore remain applicable for every lap. Each emitted digit word is nonpalindromic by the graph's safety check. Theorem 1 supplies an ordinary initial integer realizing the starting column word; its first emitted integer is itself nonpalindromic 和 continues with nonpalindromic iterates forever. The seed shift addresses time zero without requiring the chosen initial realizer itself to be nonpalindromic.

If every \(\Delta_i>0\), each persistent run grows without bound. Conversely, a zero coordinate stays bounded along the repeated cycle, establishing the strict-growth equivalence. Equation \(14\) follows by summing the starting band lengths, the \(k+1\) gaps, 和 the possible first overflow. \(\square\)

### THEOREM 4A — Drift conservation 和 elementary cycle exclusions

For a vertex \(v\), put \(G(v)=\sum_j|b_j|\). Each edge satisfies

\[
\sum_i\delta_i+G(v')-G(v)=h,
\]

因为 the total word length increases exactly by its overflow bit. Summing around a cycle gives

\[
\boxed{\sum_i\Delta_i=\sum_{j=0}^{m-1}h_j\le m.}
\tag{18}
\]

Returning parities force every \(\Delta_i\) to be even. Consequently a cycle with strict growth of every \(k\) bands satisfies \(m\ge2k\).

A realizable zero-drift cycle is impossible. It would repeat the same column-sum word after \(m>0\) steps. A complete column-sum word uniquely determines the next integer, so the ordinary orbit would satisfy \(n_{m+1}=n_1\). However, \(R(n)>n\) for every positive integer \(n\), since its reversed integer is positive. Contradiction. \(\square\)

### THEOREM 4B — Bulk-symbol pruning

For a nonneutral persistent band, the bulk symbol follows \(F(s)=2s\) for \(s\le8\), 和 \(F(s)=2s-18\) for \(s\ge10\). Its cycles are exactly

\[
(0),\quad(18),\quad(6,12),\quad(2,4,8,16,14,10).
\]

To check completeness, a nonneutral odd symbol becomes even at the first step; the displayed cycles account for every even symbol in \(\{0,2,\ldots,18\}\). A 9-band either stays 9 with \(\alpha+\beta=1\), or enters the fixed symbol 0 or 18 permanently. A central 9-band cannot stay 9: its mirrored run is itself, so \(\alpha=\beta\). The stated bulk cycles can prune cycle candidates; the conservative bound \(12\) remains valid without pruning. \(\square\)

## 5. THEOREM 5 — Short interfaces are unavoidable every 3 phases

Let \(\mathcal D_3\) be the realizable symmetric column-sum words whose every maximal constant run 有 length at least \(3\). If \(q\in\mathcal D_3\) 和 the next ordinary output is nonpalindromic, then

\[
\boxed{T(q)\notin\mathcal D_3\quad\text{or}\quad
T^2(q)\notin\mathcal D_3.}
\tag{19}
\]

Thus every 3 consecutive column-sum words of a palindrome-free orbit include a maximal run of length \(1\) or \(2\). In particular, the graph from Theorem 4 没有 directed cycles when \(B=0\), for every \(r\).

### Proof: overflow

Call \(0,\ldots,8\) low, \(9\) neutral, 和 \(10,\ldots,18\) high. Let \(s=q_0\). An overflowing transition excludes a low outer symbol, since the last column would reset the carry to zero.

For a high outer symbol, equations \(4\)–\(5\) give

\[
T(q)_0=s-9,\qquad T(q)_1=2s-18.
\]

The values differ 因为 \(s-9>0\). Therefore the first maximal output run is a singleton.

For a neutral outer symbol, the first 9-run receives carry 0. Its mirrored final 9-run receives carry 1, as required for overflow. Hence

\[
T(q)_0=10,\qquad T(q)_1=9,
\]

again giving a singleton. Therefore every overflowing transition leaves \(\mathcal D_3\).

### Proof: without overflow 和 a direct low/high interface

Assume \(q'=T(q)\in\mathcal D_3\). The preceding paragraph forces \(h=0\). By \(6\), safety requires some high symbol. The outermost nonneutral run must be low: a high outermost nonneutral run would, by symmetry, send carry 1 into the final outer 9-run, or itself be the final run, forcing overflow. An entirely neutral word produces a palindrome.

There is therefore a low-to-high change in the sequence obtained by omitting neutral runs. Between the relevant low run \(\ell^a\) 和 high run \(u^c\), either the runs are adjacent or a single maximal 9-run intervenes.

In the adjacent case, equation \(8\) gives the boundary values

\[
2\ell+1,\qquad 2u-19.
\]

The adjacent interior cores 有 even values \(2\ell\), \(2u-18\), 和 positive lengths 因为 the source run lengths are at least 3. The odd boundary values therefore form maximal output runs of length at most \(2\), whether they agree or differ. The short run contradicts \(q'\in\mathcal D_3\).

### Proof: a neutral bridge 和 the second transition

The remaining case is

\[
\ell^a\,9^b\,u^c,
\qquad \ell\le8,\quad u\ge10.
\]

The neutral run receives carry 0 from the low run. Its mirrored run receives carry 1 from the mirrored high run. Equation \(9\) makes the neutral output identically 9. The adjoining boundary values are \(2\ell+1\) 和 \(2u-19\). Each would be an isolated odd symbol unless it equaled 9, 因为 the neighboring nonneutral interior cores are even 和 nonempty. Membership of \(q'\) in \(\mathcal D_3\) therefore forces

\[
2\ell+1=9,\qquad 2u-19=9,
\]

so \(\ell=4\), \(u=14\). The word \(q'\) consequently contains consecutive maximal runs with symbols \(8,9,10\), each of length at least 3.

If the next transition overflows, the endpoint argument already gives a singleton. If it 没有 overflow, the neutral bridge again 有 bulk 9, while the neighboring boundary values become

\[
2(8)+1=17,\qquad 2(10)-19=1.
\]

The adjoining cores 有 even symbols 16 和 2 和 positive lengths. Thus 17 和 1 occur as isolated maximal runs. In either overflow case, \(T(q')\notin\mathcal D_3\). \(\square\)

For the graph corollary, any hypothetical 2-edge path can be realized by sufficiently padding its starting bands so that the 3 successive words remain above \(H\). When \(B=0\), those words belong to \(\mathcal D_3\), contradicting \(19\). Thus even a negative-drift cycle is impossible; the graph 没有 2-edge directed path.

### THEOREM 5A — The 2-transition exit bound is attained

The exact finite example is

\[
4^4\,9^3\,14^5\,9^3\,4^4
\longmapsto
8^3\,9^5\,10^3\,9^5\,8^3
\]

\[
\longmapsto
16^2\,17\,9^5\,1\,2\,1\,9^5\,17\,16^2.
\tag{20}
\]

For the first step, the consecutive run entry carries are \((0,0,0,1,1)\), the exit carries are \((0,0,1,1,0)\), 和 the emitted digit word is

\[
4^4\,9^3\,4\,5^4\,0^3\,5\,4^3.
\]

For the second step, the consecutive run entry carries are again \((0,0,0,1,1)\), the exit carries are \((0,0,1,1,0)\), 和 the emitted word is

\[
8^3\,9^5\,0\,1^2\,0^5\,9\,8^2.
\]

Neither step overflows. Folding the displayed digits gives \(20\). The first 2 column-sum words belong to \(\mathcal D_3\); the third contains singleton runs. Each source contains a high symbol, so \(6\) confirms that each emitted integer is nonpalindromic. An ordinary realizer of the first word is \(4444999997550000000\), included in the 1000-step audit below. The example establishes sharpness of the number of transitions; optimality of the run-length threshold is unclaimed. \(\square\)

## 6. THEOREM 6 — Clipping plus fixed residues cannot be an exact quotient

Let \(C_{K,M}(q)\) record the maximal-run symbol sequence 和, for each run length \(n\), the pair

\[
(\min(n,K),\ n\bmod M),\qquad K,M\ge1.
\]

For every \(K,M\ge1\), there exist positive nonpalindromic integer realizers with column words \(q,\widetilde q\) satisfying

\[
C_{K,M}(q)=C_{K,M}(\widetilde q),\qquad
C_{K,M}(T(q))\ne C_{K,M}(T(\widetilde q)).
\tag{21}
\]

Consequently an exact deterministic quotient of the specified form is impossible, even if parity or any other fixed modulus is retained.

### Exact family 和 complete carry table

For \(a\ge1\), \(b\ge2\), put \(q=10^a8^b10^a\), of length \(L=2a+b\). The complete addition is:

| Position | \(q_i\) | Incoming carry | Emitted digit | Outgoing carry |
| --- | ---: | ---: | ---: | ---: |
| \(i=0\) | 10 | 0 | 0 | 1 |
| \(1\le i<a\) | 10 | 1 | 1 | 1 |
| \(i=a\) | 8 | 1 | 9 | 0 |
| \(a<i<a+b\) | 8 | 0 | 8 | 0 |
| \(i=a+b\) | 10 | 0 | 0 | 1 |
| \(a+b<i<L\) | 10 | 1 | 1 | 1 |
| Overflow \(i=L\) | — | 1 | 1 | — |

Empty ranges contribute zero digits. Thus

\[
e=0\,1^{a-1}\,9\,8^{b-1}\,0\,1^a.
\]

The new reflection index is \(L-i\), giving every case of the fold:

| \(i\) | \(e_i\) | \(e_{L-i}\) | \(T(q)_i\) |
| --- | ---: | ---: | ---: |
| \(0\) | 0 | 1 | 1 |
| \(1\le i<a\) | 1 | 1 | 2 |
| \(a\) | 9 | 0 | 9 |
| \(a<i<a+b\) | 8 | 8 | 16 |
| \(a+b\) | 0 | 9 | 9 |
| \(a+b<i<L\) | 1 | 1 | 2 |
| \(L\) | 1 | 0 | 1 |

Therefore

\[
\boxed{T(10^a8^b10^a)=1\,2^{a-1}\,9\,16^{b-1}\,9\,2^{a-1}\,1.}
\tag{22}
\]

An ordinary nonpalindromic realizer, written most-significant digit first, is

\[
N(a,b)=\overline{9\,5^{a-1}\,4^b\,5^{a-1}\,1}.
\]

Every outer-band pair sums to 10; every central pair sums to 8. The outer digits 9 和 1 differ.

For \(K\ge2\), take \(a=K\) versus \(a=K+M\), 和 \(b=K+2\). The input clipped lengths 和 residues agree. The output 2-runs 有 lengths \(K-1\) versus \(K+M-1\); the clipped lengths differ. For \(K=1\), use \(a=1\) versus \(a=1+M\), 和 \(b=3\). The first output lacks 2-runs, while the second contains them, so the output symbol sequences differ. The argument establishes \(21\) in every case. \(\square\)

**Scope of THEOREM 6.** The obstruction concerns a saturated-length quotient. It leaves the weighted graph of Theorem 4 intact: that graph retains exact translations 和 explicitly checks the possibility of repeating their guards. Mere recurrence of a finite description cannot replace the sign test on \(\Delta\).

## 7. Verification record 和 executable code

**Finite verification record.** The audit checks the \(38\) symbol/carry cases, \(36\) clipping-plus-residue counterexamples, \(24\) symbolic translation instances drawn from \(6\) accepted skeletons, the complete finite example \(20\), 和 \(1000\) ordinary steps for each of \(3\) explicit integer realizers. Each numerical trajectory independently compares integer reversal/addition with the column-sum implementation 和 the exact palindrome criterion. A finite absence of palindromes establishes only the tested interval. The full graph enumeration is supplied as an algorithm but was **never invoked** in this investigation.

Copy the following block to `agent211_check.py`, then run `python3 agent211_check.py`. It uses only the Python standard library.

```python
#!/usr/bin/env python3
"""Agent 211: exact symbolic transitions and small independent audits.

No graph enumeration or candidate-orbit search runs by default.
"""
from dataclasses import dataclass
from hashlib import sha256
from itertools import product


def admissible(q):
    return (bool(q) and q[0] > 0 and q == q[::-1]
            and all(0 <= s <= 18 for s in q)
            and (len(q) % 2 == 0 or q[len(q)//2] % 2 == 0))


def normalize(q):
    carries, digits = [0], []
    for s in q:
        v = s + carries[-1]
        digits.append(v % 10)
        carries.append(v // 10)
    h = carries[-1]
    if h:
        digits.append(h)
    return digits, carries, h


def qstep(q):
    digits, carries, h = normalize(q)
    folded = [a+b for a, b in zip(digits, digits[::-1])]
    return folded, digits, carries, h


def step_palindrome(q, h):
    if h == 0:
        return all(s <= 9 for s in q)
    return all(s in (0, 11) for s in q)


def columns(n):
    d = [int(c) for c in str(n)[::-1]]
    return [a+b for a, b in zip(d, d[::-1])]


def intervals(q):
    out = []
    for i, s in enumerate(q):
        if out and out[-1][0] == s:
            out[-1] = (s, out[-1][1], i+1)
        else:
            out.append((s, i, i+1))
    return out


def rle(q):
    return [(s, b-a) for s, a, b in intervals(q)]


@dataclass(frozen=True)
class State:
    symbols: tuple
    gaps: tuple
    parities: tuple


def expand(state, lengths):
    q = list(state.gaps[0])
    for s, n, gap in zip(state.symbols, lengths, state.gaps[1:]):
        q.extend([s]*n)
        q.extend(gap)
    return q


def extract(q, cutoff):
    """Designate exactly the maximal runs whose lengths exceed cutoff."""
    bands = [(s, a, b) for s, a, b in intervals(q) if b-a > cutoff]
    if not bands:
        return None, ()
    gaps, end = [], 0
    for _, a, b in bands:
        gaps.append(tuple(q[end:a]))
        end = b
    gaps.append(tuple(q[end:]))
    lengths = tuple(b-a for _, a, b in bands)
    state = State(tuple(s for s, _, _ in bands), tuple(gaps),
                  tuple(n % 2 for n in lengths))
    return state, lengths


def representative(state, B):
    H = B+5
    lengths = tuple(H + (p-H) % 2 for p in state.parities)
    return expand(state, lengths), lengths


def valid_state(state, B):
    k = len(state.symbols)
    if not (k > 0 and len(state.gaps) == k+1
            and len(state.parities) == k
            and all(p in (0, 1) for p in state.parities)
            and all(len(g) <= B for g in state.gaps)):
        return False
    q, _ = representative(state, B)
    return admissible(q) and extract(q, B+4)[0] == state


@dataclass(frozen=True)
class Edge:
    target: State
    drift: tuple
    overflow: int


def successor(state, B):
    """Exact nonmerging symbolic edge; guards are n_i >= H at each phase."""
    assert valid_state(state, B)
    q, lengths = representative(state, B)
    qp, digits, _, h = qstep(q)
    pal = step_palindrome(q, h)
    assert pal == (digits == digits[::-1])
    if pal:
        return None, "palindrome"
    # The source core lengths are >= B+3; all raw gaps are <= B+2.
    target, out_lengths = extract(qp, B+2)
    if target is None or len(target.symbols) != len(state.symbols):
        return None, "merged"
    if any(len(g) > B for g in target.gaps):
        return None, "gap"
    assert valid_state(target, B)
    drift = tuple(y-x for x, y in zip(lengths, out_lengths))
    assert all(-2 <= d <= 2*B+4 for d in drift)
    assert (sum(drift) + sum(map(len, target.gaps))
            - sum(map(len, state.gaps)) == h)
    return Edge(target, drift, h), "edge"


def vertices(k, B):
    """Finite complete enumeration; provided for the reduction, not run below."""
    words = [w for j in range(B+1) for w in product(range(19), repeat=j)]
    for symbols in product(range(19), repeat=k):
        for gaps in product(words, repeat=k+1):
            for parities in product((0, 1), repeat=k):
                state = State(symbols, gaps, parities)
                if valid_state(state, B):
                    yield state


def decide(r, B, strictly_growing=False):
    """Finite decision algorithm. Astronomical bounds: not invoked in audits."""
    for k in range(1, r+1):
        done = set()
        for start in vertices(k, B):
            if start in done:
                continue
            path, edges, where = [], [], {}
            state = start
            while state not in done and state not in where:
                where[state] = len(path)
                path.append(state)
                edge, _ = successor(state, B)
                if edge is None:
                    state = None
                    break
                edges.append(edge)
                state = edge.target
            if state in where:
                first = where[state]
                cycle = path[first:]
                used = edges[first:]
                total = tuple(sum(e.drift[i] for e in used) for i in range(k))
                ok = all(d > 0 if strictly_growing else d >= 0 for d in total)
                if ok:
                    return cycle, used, total
            done.update(path)
    return None


def audit():
    for s in range(19):
        for c in (0, 1):
            f = lambda z: (s+z)//10
            assert f(f(c)) == f(c)
    print("carry idempotence: 38/38")

    for K in range(1, 13):
        for M in (1, 2, 5):
            a, b = K, K+2
            inputs = [[10]*j + [8]*b + [10]*j for j in (a, a+M)]
            clip = lambda q: [(s, min(n, K), n % M) for s, n in rle(q)]
            assert clip(inputs[0]) == clip(inputs[1])
            outputs = []
            for j, q in zip((a, a+M), inputs):
                expected = ([1] + [2]*(j-1) + [9] + [16]*(b-1)
                            + [9] + [2]*(j-1) + [1])
                assert qstep(q)[0] == expected
                outputs.append(expected)
            assert clip(outputs[0]) != clip(outputs[1])
    print("clipping-plus-residue counterexamples: K=1..12, M=1,2,5; 36/36")

    B = 2
    cases = [
        State((10, 8, 10), ((), (), (), ()), (0, 0, 0)),
        State((4, 9, 14, 9, 4), ((), (), (), (), (), ()), (0,)*5),
        State((10, 9, 8, 9, 10), ((), (), (), (), (), ()), (0,)*5),
        State((18,), ((1,), (1,)), (0,)),
        State((9,), ((10,), (10,)), (0,)),
        State((9, 9), ((), (10,), ()), (0, 0)),
        State((9, 9), ((10,), (0, 0), (10,)), (0, 0)),
        State((1, 6, 1), ((), (), (), ()), (0, 0, 0)),
    ]
    tested, accepted = 0, 0
    for case_id, state in enumerate(cases):
        assert valid_state(state, B)
        edge, reason = successor(state, B)
        print("representative", case_id, reason,
              None if edge is None else edge.drift)
        if edge is None:
            continue
        accepted += 1
        _, base = representative(state, B)
        k = len(base)
        for pad in (0, 2, 6, 20):
            lengths = tuple(n+pad+2*min(i, k-1-i) for i, n in enumerate(base))
            q = expand(state, lengths)
            assert admissible(q)
            qp, digits, _, h = qstep(q)
            assert h == edge.overflow
            assert not step_palindrome(q, h)
            assert digits != digits[::-1]
            predicted = expand(edge.target, tuple(n+d for n, d in zip(lengths, edge.drift)))
            assert qp == predicted
            tested += 1
    print("symbolic translation checks:", tested, "from", accepted, "accepted states")

    q0 = [4]*4 + [9]*3 + [14]*5 + [9]*3 + [4]*4
    q1 = [8]*3 + [9]*5 + [10]*3 + [9]*5 + [8]*3
    q2 = [16]*2 + [17] + [9]*5 + [1, 2, 1] + [9]*5 + [17] + [16]*2
    for t, (q, expected) in enumerate(((q0, q1), (q1, q2))):
        actual, digits, _, _ = qstep(q)
        assert actual == expected and digits != digits[::-1]
        print("short-run obstruction phase", t, rle(q))
    print("short-run obstruction phase", 2, rle(q2))
    controls = [(int("9" + "5"*(a-1) + "4"*b + "5"*(a-1) + "1"),
                 [10]*a + [8]*b + [10]*a) for a, b in ((3, 6), (4, 6))]
    controls.append((4444999997550000000, q0))
    for seed, initial_q in controls:
        n, q = seed, initial_q
        assert columns(n) == q
        first_palindrome = None
        for t in range(1, 1001):
            qp, digits, _, h = qstep(q)
            n += int(str(n)[::-1])
            assert qp == columns(n), (seed, t)
            assert digits == [int(c) for c in str(n)[::-1]], (seed, t)
            actual_pal = str(n) == str(n)[::-1]
            assert step_palindrome(q, h) == actual_pal, (seed, t)
            if actual_pal and first_palindrome is None:
                first_palindrome = t
            q = qp
        print("seed", seed, "steps", 1000, "column_matches", 1000,
              "palindrome_test_matches", 1000, "first_palindrome", first_palindrome,
              "final_digits", len(str(n)), "final_sha256", sha256(str(n).encode()).hexdigest())
    print("ALL AUDITS PASSED; no infinite-survival claim")


if __name__ == "__main__":
    audit()
```

Exact output:

```text
carry idempotence: 38/38
clipping-plus-residue counterexamples: K=1..12, M=1,2,5; 36/36
representative 0 edge (-1, -1, -1)
representative 1 edge (-1, 2, -2, 2, -1)
representative 2 edge (-1, -1, -1, -1, -1)
representative 3 edge (-2,)
representative 4 edge (-1,)
representative 5 edge (-1, -1)
representative 6 gap None
representative 7 palindrome None
symbolic translation checks: 24 from 6 accepted states
short-run obstruction phase 0 [(4, 4), (9, 3), (14, 5), (9, 3), (4, 4)]
short-run obstruction phase 1 [(8, 3), (9, 5), (10, 3), (9, 5), (8, 3)]
short-run obstruction phase 2 [(16, 2), (17, 1), (9, 5), (1, 1), (2, 1), (1, 1), (9, 5), (17, 1), (16, 2)]
seed 955444444551 steps 1000 column_matches 1000 palindrome_test_matches 1000 first_palindrome None final_digits 421 final_sha256 6b74ab18de7abef893759b4b36dfdf6343c5fdbca6f7355c605b5ac2ae140790
seed 95554444445551 steps 1000 column_matches 1000 palindrome_test_matches 1000 first_palindrome None final_digits 433 final_sha256 4e6592a0221340ccb2b6da633c2faa37cb998b5c5cdc76450c76bf7be9a58662
seed 4444999997550000000 steps 1000 column_matches 1000 palindrome_test_matches 1000 first_palindrome None final_digits 424 final_sha256 f9c785309222160b727b851c0ea6d15e99de5ad7478431b69fb74eaad5672d32
ALL AUDITS PASSED; no infinite-survival claim
```

## 8. Existing repository interfaces

**IDEA — integration, with inspected source references.** The graph construction is a new prose reduction in this report; the carry definitions agree with the existing whole-word model in [PeriodObstructions.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/PeriodObstructions.lean). The existing [ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean) supplies the narrower complementary-band certificate interface; its introductory scope explicitly retains certificate existence as a premise. A future Lean implementation of the finite graph should import the existing normalization 和 ordinary-word bridge, rather than duplicate them.

The inspected [Agent102AffineBoundary.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent102AffineBoundary/Agent102AffineBoundary.lean) already records failure of a template-independent equality cutoff for general affine run words. The inspected [Agent105UniformReturnPlain.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent105UniformIntegerReturn/Agent105UniformReturnPlain.lean) 和 its entries in [RESULTS.md](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/RESULTS.md) concern uniformizing returns within an already supplied affine family. A separate finite catalogue is still required when indexing only by \(r,B\). Priority for the supporting carry identities or elementary cycle-drift argument is unclaimed.

**LEAN-VERIFIED status:** the newly stated graph 和 short-interface theorems 都有 complete prose proofs here; Lean formalization remains future work. Existing source files 和 theorem registries remain unchanged.

## 9. IDEA — Sharpest open question

**Can one compute a bound \(B_*(r,B_0)\), independent of the unknown return period, such that whenever a strictly growing constant-run return exists with at most \(r\) long runs 和 return-phase blocks of length at most \(B_0\), some such return keeps every intermediate block bounded by \(B_*(r,B_0)\)?**

A positive answer, together with a precise canonical treatment of persistent versus bounded runs, would turn Theorem 4 into the desired finite decision for the return-phase-bounded template class. An estimate depending on the unknown period, such as \(B_0+2m\), is insufficient for that conclusion. More broadly, a bound on the number of syntactically designated runs permits repeated visits to states where some runs are short; obtaining an eventual uniformly separated representation with a computable bound remains open. Theorem 5 shows that finite interface blocks must remain part of any viable invariant. The next mathematical target is control of those interfaces, rather than erasure of their length information.
