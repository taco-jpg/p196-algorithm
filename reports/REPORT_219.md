# REPORT_219 — Global renormalization 和 the finite-center obstruction

Agent: 219. Direction: 9 (wildcard). Date: 2026-10-22.

## Answer — one paragraph

**THEOREM:** The two-ended decimal limit model admits a continuous reverse-add extension exactly where the mirrored column sums are not eventually \(9\); at every eventually-\(9\) boundary state, its closed graph instead 有 exactly 两个 outputs, distinguished by a carry arriving from the unresolved center. Exactly one output remains on 那 boundary, so an infinite nonpalindromic boundary trajectory exists automatically, without supplying a finite integer. **THEOREM:** A finite positive orbit cannot return with uniformly bounded gaps to a single central run of zeros or nines with uniformly bounded end blocks; a monotone low-block quantity gives the obstruction, including unspecified intermediate phases. **THEOREM:** For one-digit end blocks, every constant-center trajectory reaches a palindrome or exits the class within 两个 transitions. **THEOREM:** Literal binary-to-decimal block simulation 也 encounters exact carry 和 congruence obstructions, with the specified surviving small codes refuted by finite counterexamples. **IDEA:** The remaining constructive target is a finite cycle of the explicit nonsaturated constant-center endpoint system, or another finite center that implements the required boundary carries coherently forever. 这个 report 没有 a decimal Lychrel construction.

## Scope 和 notation

**THEOREM** labels mathematical statements with complete proofs below. Numerical checks corroborate the identities 和 refute specified constructions; finite survival is never used as an infinite-time argument. None of the new statements is labeled **LEAN-VERIFIED**.

Write \(T(n)=n+\operatorname{rev}_{10}(n)\). Ordinary decimal expansions are canonical: the leading digit is nonzero. In a fixed-width block, zeros are retained during reversal. A palindrome means equality of the complete canonical digit word with its reversal.

The proposed new approach retains 两个 infinite endpoint streams 和 identifies the center carry lost by passage to a limit. Sections 3–5 then test whether a bounded finite center/end-block description can implement a return. Section 6 records the obstruction to the motivating binary embedding.

## 1. THEOREM — Complete carry ledger

For a positive integer of length \(L\), let \(d_i\) be its units-first digits,
\[
q_i=d_i+d_{L-1-i},\qquad
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,\qquad
e_i=q_i+c_i-10c_{i+1}.
\]

The complete cases are:

| Column sum | Incoming carry | Output digit | Outgoing carry |
|---|---:|---:|---:|
| \(0\le q_i\le8\) | \(0\) | \(q_i\) | \(0\) |
| \(0\le q_i\le8\) | \(1\) | \(q_i+1\) | \(0\) |
| \(q_i=9\) | \(0\) | \(9\) | \(0\) |
| \(q_i=9\) | \(1\) | \(0\) | \(1\) |
| \(10\le q_i\le18\) | \(0\) | \(q_i-10\) | \(1\) |
| \(10\le q_i\le18\) | \(1\) | \(q_i-9\) | \(1\) |

If \(c_L=0\), the output length is \(L\): its leading digit is \(q_{L-1}+c_{L-1}\ge1\). If \(c_L=1\), the output length is \(L+1\), with new leading digit \(1\). Telescoping every carry gives
\[
T(n)=\sum_{i=0}^{L-1}e_i10^i+c_L10^L
     =\sum_{i=0}^{L-1}q_i10^i.
\tag{1}
\]
In particular,
\[
T(n)\equiv2n\pmod9,\qquad
T(n)\equiv
\begin{cases}
0,&L\text{ even},\\
2n,&L\text{ odd}
\end{cases}\pmod{11}.
\tag{2}
\]

**Proof.** Each row follows by division by \(10\), with \(q_i+c_i\in[0,19]\). In the weighted sum, \(c_i10^i\) cancels the preceding column's \(-10c_i10^{i-1}\); the final carry is restored by \(c_L10^L\). Reducing (1) modulo \(9\) uses \(10\equiv1\). Modulo \(11\), reversal satisfies
\[
\operatorname{rev}_{10}(n)\equiv(-1)^{L-1}n.
\]
These computations include the overflow term.

**THEOREM — Eventual divisibility by \(11\).** Every positive orbit eventually becomes divisible by \(11\), 和 remains divisible thereafter.

**Proof.** Since \(\operatorname{rev}_{10}(n)\ge1\), the orbit strictly increases without bound. Length never decreases 和 increases by at most one per step, so an even input length is eventually visited. Equation (2) makes its successor divisible by \(11\). Either length parity preserves divisibility on subsequent steps.

## 2. THEOREM — Exact two-ended extension 和 its singular boundary

Let \(A=\{0,\ldots,9\}\) 和
\[
X=\{(x,y)\in A^{\mathbb N}\times A^{\mathbb N}:y_0\ne0\}
\]
with the product topology. Here \(x\) is read from the units end 和 \(y\) from the leading end. Embed a finite integer of length \(L\) as
\[
x_i=d_i,\quad y_i=d_{L-1-i}\quad(i<L),\qquad x_i=y_i=0\quad(i\ge L).
\]
Denote these embedded integers by \(E\). For an arbitrary 点 of \(X\), put
\[
q_i=x_i+y_i,\qquad
S=\{(x,y):q_i=9\text{ eventually}\},\qquad D=X\setminus S.
\]

Then \(E\) is dense in \(X\), \(E\subset D\), 和 finite reverse-add extends uniquely 和 continuously to \(D\), as a map into \(X\). At each 点 of \(S\), the closure of the finite reverse-add graph 有 exactly 两个 distinct outputs. Thus \(D\) is exactly the domain where 那 graph gives a unique continuous extension.

### Exact formulas

The low carry is
\[
c_0=0,\qquad c_{i+1}=\left\lfloor(q_i+c_i)/10\right\rfloor,\qquad
u_i=q_i+c_i-10c_{i+1}.
\]
For the high end, \(r_i\) is the carry entering the column at distance \(i\) from the leading end; its outgoing carry is
\[
r_{i-1}=\left\lfloor(q_i+r_i)/10\right\rfloor.
\]
The overflow is \(r_{-1}\).

For a 点 of \(D\), define
\[
j(i)=\min\{j\ge i+1:q_j\ne9\}\qquad(i\ge-1).
\]
Then
\[
r_i=
\begin{cases}
0,&q_{j(i)}\le8,\\
1,&q_{j(i)}\ge10.
\end{cases}
\tag{3}
\]
Put \(h=r_{-1}\), \(v_i=q_i+r_i-10r_{i-1}\). The output is
\[
x'_i=u_i,\qquad
y'=
\begin{cases}
(v_0,v_1,\ldots),&h=0,\\
(1,v_0,v_1,\ldots),&h=1.
\end{cases}
\tag{4}
\]

### Proof

**Density.** Prescribe the first \(k\) digits of each stream. Concatenate the prescribed high prefix, one center digit, 和 the reversed low prefix. 这 gives a canonical integer of length \(2k+1\) in the requested neighborhood. A finite integer 有 \(q_i=0\) eventually, so \(E\subset D\).

**Determination of the high carry.** For \(a\in\{0,1\}\), the complete carry map is
\[
f_q(a)=\left\lfloor(q+a)/10\right\rfloor=
\begin{cases}
0,&q\le8,\\
a,&q=9,\\
1,&q\ge10.
\end{cases}
\]
A \(9\)-column transmits the incoming carry. The first inward non-\(9\) column resets it independently of deeper digits, giving (3).

**Agreement with ordinary integers.** At a finite state, \(q_i=q_{L-1-i}\) for \(i<L\), 和 the zero tail gives \(r_{L-1}=0=c_0\). Recursion gives
\[
r_i=c_{L-1-i}\quad(0\le i<L),\qquad r_{-1}=c_L.
\]
Thus (4) reproduces the ordinary high digits, including overflow. The low recurrence 也 includes the possible overflow at index \(L\), where \(q_L=0\).

**Canonical output.** For \(h=1\), the new leading digit is \(1\). For \(h=0\), it is \(q_0+r_0\in\{1,\ldots,9\}\), since \(q_0\ge y_0\ge1\). No leading-zero convention is hidden.

**Continuity on \(D\).** A finite low output prefix needs finitely many input digits. A finite high output prefix needs finitely many first reset positions \(j(i)\). Fixing the input through those positions fixes the output prefix. Density supplies uniqueness.

**Exactly 两个 outputs on \(S\).** Choose \(J\) with \(q_i=9\) for \(i\ge J\). Each choice \(\tau\in\{0,1\}\) specifies \(r_i=\tau\) for \(i\ge J-1\); recurse outward through the preceding finite prefix. Apply (4) to obtain \(F_\tau(x,y)\).

Each output is a limit of ordinary arithmetic. For \(k\ge J\), use the canonical word
\[
y_0y_1\cdots y_{k-1}\;(9\tau)\;x_{k-1}\cdots x_1x_0.
\tag{5}
\]
Its center column sum is \(0\) for \(\tau=0\), resetting the outgoing carry to \(0\), 和 \(18\) for \(\tau=1\), resetting it to \(1\). The intervening \(9\)-columns transmit 那 choice. Its output prefixes therefore converge to \(F_\tau(x,y)\).

没有 further limits: in any convergent sequence of finite approximants, the carry entering the high column at distance \(J-1\) is a bit. A subsequence keeps 那 bit fixed. Every longer fixed window then agrees with the corresponding \(F_\tau\).

The outputs differ. If any \(q_i\ne9\), the overflow is fixed independently of \(\tau\), while the eventual high output is \(9\) for \(\tau=0\) 和 \(0\) for \(\tau=1\). If every \(q_i=9\), the first output begins with \(9\), while the second begins with \(1\). Hence 没有 continuous extension at any 点 of \(S\).

## 3. THEOREM — Infinite nonpalindromic boundary trajectories are automatic

At a state of \(S\), let \(s\in\{0,1\}\) be the eventual low carry. Its 两个 graph outputs satisfy
\[
x'_i=9(1-s)\text{ eventually},\qquad
y'_i=9(1-\tau)\text{ eventually}.
\]
Exactly one remains in \(S\):
\[
\boxed{\tau=1-s.}
\tag{6}
\]
Iterating 这 selection gives an infinite nonpalindromic trajectory of the **closed graph relation**. None of its states represents a finite integer.

**Proof.** A tail with \(q_i=9\) transmits the low carry \(s\), so its output is \(9+s-10s\). The high output tail is \(9+\tau-10\tau\); adding a leading overflow shifts the high stream without changing its tail. Thus the output pair-sum tail is \(18-9(s+\tau)\), equal to \(9\) exactly in (6).

For finite integers, palindromicity is precisely membership in
\[
\Delta=\{(x,y):x=y\}.
\]
But \(S\cap\Delta=\varnothing\): equality would require \(2x_i=9\) eventually. 也, \(S\cap E=\varnothing\), because finite states 有 pair-sum tail \(0\). The selected trajectory stays in \(S\) forever.

**IDEA — Exact stopping point of the limit approach.** Formula (5) permits a new finite approximation at each time. A finite Lychrel construction instead needs one evolving finite center to supply the required carry \(\tau_t=1-s_t\) at every step. Neither graph closure nor the infinite boundary trajectory supplies 那 compatibility. Even approximation of an entire finite trajectory segment by one finite seed needs a separate argument: composing the closed one-step relation does not establish 那 stronger property. The continuous extension in Section 2 maps into X; forward invariance of D is not asserted. An alternative sufficient route would be a forward-invariant subset of \(D\), disjoint from \(\Delta\), that contains an embedded finite integer.

The \(1000\)-transition test in Section 7 checks 这 distinction explicitly: it validates \(2000\) separate finite one-step realizations of the 两个 branches, without treating them as one finite orbit.

## 4. THEOREM — A single growing saturated center cannot recur with bounded gaps

For \(K\ge1\), define \(C_K^d\) as the positive integers of length \(L>2K\) whose digits at positions \(K,\ldots,L-K-1\) 都 equal \(d\). Put \(M=10^K\). Let \(A_t\) be the leading \(K\)-digit block, \(B_t\) the trailing \(K\)-digit value, 和 \(R_t=\operatorname{rev}_K(A_t)\). Canonical leading digits give
\[
1\le R_t\le M-1.
\]

If \(n_0,\ldots,n_N\in C_K^0\), then
\[
N\le M-1-B_0.
\tag{7}
\]
If \(n_0,\ldots,n_N\in C_K^9\), then
\[
N\le B_0.
\tag{8}
\]
If the states instead belong to \(C_K^0\cup C_K^9\) 和 有 length at least \(2K+2\), the saturated digit cannot switch, 和 \(N\le M-1\).

### Carry proof, including overflow

Summing the lowest \(K\) columns of (1) gives
\[
B_t+R_t=B_{t+1}+Mc_K.
\tag{9}
\]
这 remains exact for either full output length.

For a zero center, \(q_K=0\), so \(e_K=c_K\). Position \(K\) stays inside the output center. Staying in \(C_K^0\) forces \(c_K=0\), hence
\[
B_{t+1}=B_t+R_t\ge B_t+1.
\]
Its upper bound \(M-1\) gives (7).

For a nine center, \(q_K=18\), so \(e_K=8+c_K\). Staying in \(C_K^9\) forces \(c_K=1\), hence
\[
B_{t+1}=B_t+R_t-M\le B_t-1.
\]
Nonnegativity gives (8).

With at least 两个 central positions, column \(K\) resets the next carry to \(0\) in the zero case, so \(e_{K+1}=0\). In the nine case it sets the next carry to \(1\), so \(e_{K+1}=9\). Position \(K+1\) remains central under either output length. Thus switching is impossible.

### THEOREM — Bounded-gap return obstruction

There do not exist fixed \(K,G\ge1\), one positive orbit, 和 infinitely many times
\[
t_0<t_1<\cdots,\qquad t_{j+1}-t_j\le G,
\]
such that every return state belongs to \(C_K^0\cup C_K^9\).

**Proof.** First,
\[
T(C_K^d)\subseteq C_{K+1}^d,\qquad d\in\{0,9\},
\tag{10}
\]
whenever the enlarged center is nonempty. Indeed, the output at original positions \(K+1,\ldots,L-K-1\) remains \(d\). If \(L'=L\), the new center is \([K+1,L-K-2]\). If \(L'=L+1\), it is \([K+1,L-K-1]\). Each interval lies in that unchanged output region. No-overflow needs an input center of length at least \(3\); overflow needs at least \(2\).

Set \(H=K+G\). Lengths along a positive orbit eventually exceed \(2H+2\). Starting from any sufficiently late return, apply (10) through its next at most \(G\) transitions. Enlarging the resulting end blocks further to width \(H\) retains a saturated center of length at least \(2\). Consequently every sufficiently late state belongs to \(C_H^0\cup C_H^9\). Its saturated digit cannot switch, 和 its last-\(H\)-digit value moves strictly in one direction forever inside \([0,10^H-1]\), a contradiction.

**THEOREM — Template consequence.** 这 excludes a fixed-period growing return with one central zero/nine run 和 uniformly bounded end blocks, even when intermediate phases are unspecified. Fixed-period return is the special case \(G=m\). Multiple growing bands, nonsaturated central digits, 和 unbounded end blocks are outside 这 obstruction.

## 5. THEOREM — Exact finite-center endpoint system

Let
\[
n=A\,d^k\,B
 =A10^{K+k}+d\frac{10^k-1}{9}10^K+B,
\]
where \(K\ge1\), \(k\ge2\),
\[
10^{K-1}\le A<10^K,\qquad 0\le B<10^K,\qquad 0\le d\le9.
\]
The end blocks 都 occupy exactly \(K\) positions. Define
\[
M=10^K,\quad R=\operatorname{rev}_K(A),\quad P=\operatorname{rev}_K(B),
\]
\[
h=\left\lfloor2d/10\right\rfloor,\qquad g=2d-9h,\qquad S=A+P+h.
\]

The output 有 a uniform center with the same end-block width \(K\) if 和 only if
\[
hM\le B+R<(h+1)M
\tag{11}
\]
和 the applicable row below holds:

| Case | Additional condition | \(A'\) | \(d'\) | \(B'\) | \(k'\) |
|---|---|---|---|---|---|
| \(S<M\) | none | \(S\) | \(g\) | \(B+R-hM\) | \(k\) |
| \(S\ge M\) | \(S\bmod10=g\) | \(\lfloor S/10\rfloor\) | \(g\) | \(B+R-hM\) | \(k+1\) |

**Proof.** The low-block outgoing carry is \(c=\lfloor(B+R)/M\rfloor\). Since \(2d\) is even, a central column 有 outgoing carry \(h\) for either incoming bit. Its first output digit is \(2d+c-10h\); each of the remaining \(k-1\) output digits is \(g\). Since \(k\ge2\), uniformity forces the target digit to be \(g\), 和 then forces \(c=h\), precisely (11).

The high block receives carry \(h\), giving \(S\). If \(S<M\), it occupies its original \(K\) positions. If \(S\ge M\), its lowest digit enters the enlarged central run 和 must equal \(g\); the remaining high block is \(\lfloor S/10\rfloor\). 这 accounts for every digit 和 proves sufficiency as well. Since \(M/10\le S\le2M-1\), the output high blocks 都 canonical.

The central digit cycles are
\[
0\to0,\qquad9\to9,\qquad3\to6\to3,
\]
\[
1\to2\to4\to8\to7\to5\to1.
\tag{12}
\]
There are exactly \(9\cdot10^{2K}\) possible endpoint states \((A,d,B)\), before imposing the transition conditions. These equations define a partial deterministic finite graph; no search through that graph is performed here.

### THEOREM — One-digit end blocks force a palindrome or an exit

If three consecutive states \(n_0,n_1,n_2\) each 有 form \(a\,d^k\,b\) with \(k\ge2\), then \(n_1\) or \(n_2\) is palindromic.

**Proof.** Put \(t=a+b\). For \(d\le4\), (11) forces \(t<10\). 没有 overflow 和
\[
n_1=t\,(2d)^k\,t,
\]
a palindrome.

For \(d\ge5\), (11) forces \(t\ge10\). With \(g=2d-9\), the high sum is \(t+1\in[11,19]\). Its units digit must equal \(g\), so \(t-9=g\), equivalently \(t=2d\). Hence
\[
n_1=1\,g^{k+1}\,(g-1).
\]
For \(g=1\), the next endpoint sum is \(1\), the center doubles without carry, 和 \(n_2=1\,2^{k+1}\,1\), a palindrome. For \(g=3\), the endpoint sum is \(3\), the center doubles without carry, 和 \(n_2=3\,6^{k+1}\,3\), a palindrome. For each of \(g=5,7,9\), the endpoint sum is \(g<10\), so its incoming central carry is \(0\), while the center requires \(1\). The first central output digit differs from the later central digits. Thus \(n_2\) exits the class. These are every possible case.

### THEOREM — Necessary congruences for any growing cycle

Suppose the endpoint graph contains a cycle of period \(p\), with total length gain \(G>0\). Every state on it necessarily satisfies
\[
2A\equiv d\pmod{11},\qquad
B\equiv-(-1)^K A\pmod{11}.
\tag{13}
\]
If the center follows the six-phase cycle in (12), then
\[
6\mid p,\qquad9\mid G.
\tag{14}
\]

**Proof.** The endpoint identities hold for every \(k\ge2\), so the cycle gives \(T^p(N_k)=N_{k+G}\). Modulo \(11\),
\[
N_k\equiv
\begin{cases}
(-1)^K A+B,&k\text{ even},\\
(-1)^K(d-A)+B,&k\text{ odd}.
\end{cases}
\]
Every such positive orbit eventually becomes divisible by \(11\), by Section 1. If \(G\) is odd, successive returns visit 两个 parities. If \(G\) is even, apply 那 fact separately to even 和 odd starting \(k\). The displayed residues 都 must vanish; subtraction gives (13).

The six distinct central phases force \(6\mid p\), so \(2^p\equiv1\pmod9\). Since \(N_k\equiv A+B+kd\pmod9\), the return identity gives \(Gd\equiv0\pmod9\). Each digit of this six-phase cycle is coprime to \(9\), giving \(9\mid G\).

### IDEA — Sharpest constructive question

Does 这 exact endpoint graph, for some \(K\ge2\), contain a directed cycle with:

1. center digits in either nonsaturated cycle of (12);
2. at least one overflow;
3. \(B\ne\operatorname{rev}_K(A)\) at every phase?

Equations (13)–(14) are necessary restrictions.

**THEOREM — Why 这 question suffices.** Such a cycle would produce a decimal Lychrel number: choose any \(k\ge2\), realize its first state as the canonical integer \(A\,d^k\,B\), 和 iterate the exact transition formulas. Every phase is independent of the current run length; overflow increases it, preserving \(k\ge2\). Palindromicity is exactly \(B=\operatorname{rev}_K(A)\), because the center is already symmetric. Condition 3 excludes it forever. 这是 a conditional construction; 这个 report 没有 a cycle witness.

The monotone argument settles the \(0\)- 和 \(9\)-cycles for every \(K\), 和 the preceding case proof settles \(K=1\). For the nonsaturated cycles with \(K\ge2\), the low-block update alternates between addition 和 subtraction of \(M\); its monotonicity disappears. That is the precise unresolved step of 这 finite-template specialization.

## 6. THEOREM — Obstructions to importing the binary template

### A. Exact local carry simulation forces equal radices

Let \(b,B\ge2\), let \(\phi:\{0,\ldots,b-1\}\to\{0,\ldots,B-1\}\) be injective, 和 let \(\sigma:\{0,1\}\to\{0,1\}\). Suppose every addition column satisfies
\[
\phi(x)+\phi(y)+\sigma(c)
=\phi((x+y+c)\bmod b)
+B\sigma\!\left(\left\lfloor(x+y+c)/b\right\rfloor\right).
\tag{15}
\]
Then \(B=b\). The only possibilities are the identity maps 和 the complemented digit/carry maps.

**Proof.** Put \(s_i=\sigma(i)\). The column \((0,0,0)\) gives \(u=\phi(0)=(B-1)s_0\). Carry-free columns give \(\phi(x+y)=\phi(x)+\phi(y)-u\), hence \(\phi(d)=u+vd\). The column \((0,0,1)\) gives \(v=s_1-s_0\). The column \((b-1,1,0)\) gives \(bv=B(s_1-s_0)\). Thus \((B-b)v=0\); injectivity gives \(v\ne0\). With \(B=b\), the bit choices give either \(\phi(d)=d,\sigma(c)=c\), or \(\phi(d)=b-1-d,\sigma(c)=1-c\). Substitution verifies each possibility for either source carry.

For width-\(k\) decimal blocks, the target radix is \(10^k\), excluding 这 exact one-addition simulation of binary columns. Several decimal steps, contextual blocks, 和 a restricted orbit language remain outside this theorem.

### B. Congruences obstruct literal template returns

Use the binary word
\[
X_n=10\,1^n\,01\,0^n,\qquad n\ge2.
\]
The restriction matters: \(X_1=101010_2\) reaches the palindrome \(111111_2\) immediately. The supplied binary four-step pattern is checked from \(X_2\) for \(1000\) steps below.

Replace bit \(0\) by a fixed width-\(k\) decimal block \(A\), 和 bit \(1\) by \(B\), whose leading digit is nonzero. Let the resulting integer be \(E_n\), with \(D_0=10^k\). Direct summation of the one-positions gives
\[
E_n=A\sum_{j=0}^{2n+3}D_0^j+(B-A)C_n(D_0),
\]
\[
C_n(D_0)=D_0^{2n+3}
+\sum_{j=n+2}^{2n+1}D_0^j+D_0^n
=(D_0^2-D_0+1)D_0^n\sum_{j=0}^{n+1}D_0^j.
\tag{16}
\]
There are \(n+2\) blocks of each kind. Therefore
\[
E_n\equiv(n+2)(A+B)\pmod9.
\tag{17}
\]
For odd \(k\),
\[
E_n\equiv0\ (n\text{ even}),\qquad
E_n\equiv-3(B-A)\ (n\text{ odd})\pmod{11};
\tag{18}
\]
for even \(k\),
\[
E_n\equiv(n+2)(A+B)\pmod{11}.
\tag{19}
\]
These follow from \(D_0\equiv-1\) or \(1\pmod{11}\) in (16).

Suppose fixed \(m,g\ge1\) satisfy \(T^m(E_n)=E_{n+g}\) for every sufficiently 大 \(n\). Every source is of even decimal length. By (2), every positive-time output is divisible by \(11\). Equations (18)–(19) force
\[
A\equiv B\pmod{11}\quad(k\text{ odd}),\qquad
A+B\equiv0\pmod{11}\quad(k\text{ even}).
\tag{20}
\]
Equation (17), applied at consecutive parameters 和 subtracted, 也 gives
\[
(2^m-1)(A+B)\equiv0\pmod9,\qquad g(A+B)\equiv0\pmod9.
\tag{21}
\]
For \(k=1\), (20) forces equal digits. Thus every nontrivial single-digit substitution fails on an eventual full parameter tail, regardless of macrostep length or parameter increment.

**Scope.** Restricting to even parameters 和 an even increment avoids (18). For increment \(2\), subtracting the equations at parameters differing by \(2\) still gives (21), since \(2\) is invertible modulo \(9\). A nontrivial single-digit code then satisfies \(A=a,B=9-a\), \(a=0,\ldots,8\). A reversal-compatible width-\(2\) code consists of palindromic blocks \(A=11a,B=11b\); increment \(1\) forces \(a+b=9\).

### C. THEOREM — Finite counterexamples kill the specified small-code returns

For every one of those nine width-\(1\) complementary codes, the orbit of \(E_2\) never reaches \(E_4\). For every one of the nine width-\(2\) palindromic complementary codes, the orbit of \(E_2\) never reaches \(E_3\).

**Finite proof.** The reproducible calculation in Section 7 provides, for each code, consecutive iterates \(U=T^{r-1}(E_2)\), \(V=T^r(E_2)\) with
\[
U<E_{2+g}<V.
\tag{22}
\]
For every positive \(n\), \(T(n)>n\), so the iterates from a fixed positive seed strictly increase. Earlier iterates are at most \(U\), 和 later iterates are at least \(V\). Thus no macrostep length reaches 那 target. The strict brackets are printed in full; each addition is checked by individual carries 和 direct integer reversal.

For example, width \(2\), \(A=00,B=99\), gives
\[
T^9(9900999900990000)=65320178222288202345
<99009999990099000000
<T^{10}(9900999900990000)=119640466444575304701.
\]
These counterexamples concern families required to include parameter \(2\). They do not exclude a separately established eventual family beginning at an arbitrary larger threshold, wider blocks, or contextual encodings.

## 7. Reproducible validation

**THEOREM — Finite validation statements.** Executing the self-contained Python code below gives the output printed afterward. Its construction tests include:

- \(1000\) transitions of the critical boundary selection, checked against \(2000\) separate finite one-step realizations.
- \(1000\) ordinary decimal steps for each of \(18\) specified proposed encodings, including after any palindrome; every target-return claim fails within \(12\) steps.
- \(1800\) short instances of the one-digit-end-block theorem, with zero counterexamples.
- \(1000\) binary reference steps, including \(250\) four-step returns.

A `None` palindrome result means only that no palindrome occurred in the tested \(1000\) steps. 这不是 a Lychrel assertion. The boundary test never asserts the existence of one finite seed following its \(1000\) selected transitions.

### Code

```python
from dataclasses import dataclass


def step(n):
    d = [int(ch) for ch in str(n)[::-1]]
    out = []
    carry = 0
    for i in range(len(d)):
        q = d[i] + d[-1 - i]
        carry, digit = divmod(q + carry, 10)
        assert carry in (0, 1) and 0 <= digit <= 9
        out.append(digit)
    if carry:
        out.append(carry)
    result = int(''.join(map(str, out[::-1])))
    assert result == n + int(str(n)[::-1])
    assert result % 9 == 2 * n % 9
    assert result % 11 == ((0 if len(d) % 2 == 0 else 2) * n) % 11
    return result


@dataclass(frozen=True)
class Stream:
    prefix: tuple
    tail: int

    def at(self, i):
        return self.prefix[i] if i < len(self.prefix) else self.tail


def normal(prefix, tail):
    p = list(prefix)
    while p and p[-1] == tail:
        p.pop()
    return Stream(tuple(p), tail)


def branch(x, y, tau):
    m = max(len(x.prefix), len(y.prefix))
    assert x.tail + y.tail == 9
    q = [x.at(i) + y.at(i) for i in range(m)]
    carry = 0
    low = []
    for a in q:
        low.append((a + carry) % 10)
        carry = (a + carry) // 10
    low_tail = 9 if carry == 0 else 0
    high = [0] * m
    r = tau
    for i in range(m - 1, -1, -1):
        high[i] = (q[i] + r) % 10
        r = (q[i] + r) // 10
    if r:
        high.insert(0, 1)
    high_tail = 9 if tau == 0 else 0
    return normal(low, low_tail), normal(high, high_tail), carry


def check_boundary():
    x, y = Stream((), 0), Stream((), 9)
    checks = max_width = 0
    for _ in range(1000):
        m = max(len(x.prefix), len(y.prefix))
        k = m + 3
        for tau in (0, 1):
            xx, yy, low_carry = branch(x, y, tau)
            high = ''.join(str(y.at(i)) for i in range(k))
            low = ''.join(str(x.at(i)) for i in reversed(range(k)))
            n = int(high + str(9 * tau) + low)
            result = str(step(n))
            assert result[:k] == ''.join(str(yy.at(i)) for i in range(k))
            assert result[-k:][::-1] == ''.join(
                str(xx.at(i)) for i in range(k)
            )
            checks += 1
        x, y, _ = branch(x, y, 1 - low_carry)
        assert x.tail + y.tail == 9 and x.tail != y.tail
        assert y.at(0) != 0
        max_width = max(max_width, len(x.prefix), len(y.prefix))
    print('symbolic_boundary_steps = 1000')
    print('finite_one_step_branch_checks =', checks)
    print('nonpalindromic_boundary_states = 1001')
    print('maximum_finite_boundary_width =', max_width)
    print('final_low_tail =', x.tail)
    print('final_high_tail =', y.tail)
    print('finite_seed_with_1000_steps = NOT CLAIMED')


def encoded(a, n, width):
    word = '10' + '1' * n + '01' + '0' * n
    return int(''.join(
        str(a if ch == '0' else 9 - a) * width for ch in word
    ))


def check_encodings():
    rows = []
    for width, jump, macro in ((1, 2, 8), (2, 1, 4)):
        print('width', width, 'parameter_jump', jump,
              'columns: a crossing first_pal digits1000 hit fixed_macro_equal')
        for a in range(9):
            n = encoded(a, 2, width)
            target = encoded(a, 2 + jump, width)
            crossing = pal = hit = None
            fixed = False
            for t in range(1, 1001):
                before = n
                n = step(n)
                if t == macro:
                    fixed = n == target
                if n == target:
                    hit = t
                if crossing is None and n > target:
                    crossing = t
                    assert before < target < n
                    rows.append((width, a, t, before, target, n))
                if pal is None and str(n) == str(n)[::-1]:
                    pal = t
            print(a, crossing, pal, len(str(n)), hit, fixed)
    print('strict_crossings: width a r T^(r-1)(seed) target T^r(seed)')
    for row in rows:
        print(*row)


def uniform_one_cap(n):
    s = str(n)
    return len(s) >= 4 and len(set(s[1:-1])) == 1


def check_one_cap():
    checks = uniform_next = uniform_three = failures = 0
    for k in (2, 3):
        for a in range(1, 10):
            for b in range(10):
                for d in range(10):
                    n = int(str(a) + str(d) * k + str(b))
                    n1, n2 = step(n), step(step(n))
                    checks += 1
                    if uniform_one_cap(n1):
                        uniform_next += 1
                    if uniform_one_cap(n1) and uniform_one_cap(n2):
                        uniform_three += 1
                        if str(n1) != str(n1)[::-1] and str(n2) != str(n2)[::-1]:
                            failures += 1
    assert failures == 0
    print('K1 triples checked:', checks)
    print('Uniform-center next states:', uniform_next)
    print('Uniform-center triples:', uniform_three)
    print('Counterexamples to palindrome-or-exit theorem:', failures)


def check_binary_reference():
    n = int('10110100', 2)
    parameter = 2
    for t in range(1, 1001):
        word = bin(n)[2:]
        n += int(word[::-1], 2)
        assert bin(n)[2:] != bin(n)[2:][::-1]
        if t % 4 == 0:
            parameter += 1
            assert bin(n)[2:] == '10' + '1' * parameter + '01' + '0' * parameter
    print('binary_reference_steps = 1000')
    print('binary_four_step_returns_checked = 250')
    print('binary_final_parameter =', parameter)


check_boundary()
check_encodings()
check_one_cap()
check_binary_reference()
```

### Exact output

```text
symbolic_boundary_steps = 1000
finite_one_step_branch_checks = 2000
nonpalindromic_boundary_states = 1001
maximum_finite_boundary_width = 387
final_low_tail = 0
final_high_tail = 9
finite_seed_with_1000_steps = NOT CLAIMED
width 1 parameter_jump 2 columns: a crossing first_pal digits1000 hit fixed_macro_equal
0 11 8 428 None False
1 12 5 432 None False
2 10 None 420 None False
3 9 16 421 None False
4 11 24 431 None False
5 10 None 429 None False
6 9 15 424 None False
7 12 None 426 None False
8 10 None 414 None False
width 2 parameter_jump 1 columns: a crossing first_pal digits1000 hit fixed_macro_equal
0 10 None 422 None False
1 10 None 434 None False
2 10 None 431 None False
3 10 19 430 None False
4 9 None 433 None False
5 10 None 444 None False
6 10 None 437 None False
7 10 None 439 None False
8 9 32 421 None False
strict_crossings: width a r T^(r-1)(seed) target T^r(seed)
1 0 11 853561165347 909999090000 1597122330705
1 1 12 594855668484 818888181111 1079722226979
1 2 10 656092181745 727777272222 1203273472401
1 3 9 105494959449 636666363333 1050454453950
1 4 11 456300014544 545555454444 901710018198
1 5 10 175468375467 454444545555 940042240038
1 6 9 107831712879 363333636666 1086048851580
1 7 12 149094500841 272222727777 297099991782
1 8 10 97871917968 181111818888 184843835847
2 0 10 65320178222288202345 99009999990099000000 119640466444575304701
2 1 10 52876992788730066924 88118888881188111111 95842996577460034749
2 2 10 65567731689712677645 77227777772277222222 120245353488326454201
2 3 10 51941997189170014014 66336666663366333333 92983004387349928929
2 4 9 15857999092910007594 55445555554455444444 65428001022009983445
2 5 10 16125981506942984325 44554444445544555555 68474906467461936486
2 6 10 15840197707176919494 33663333336633666666 65332164877956024345
2 7 10 15912596602077842205 22772222227722777777 66137473622747364156
2 8 9 8199892507151890017 11881111118811888888 15300874024204879935
K1 triples checked: 1800
Uniform-center next states: 500
Uniform-center triples: 120
Counterexamples to palindrome-or-exit theorem: 0
binary_reference_steps = 1000
binary_four_step_returns_checked = 250
binary_final_parameter = 252
```

## 8. Repository integration 和 verification status

The existing conditional return-certificate source was inspected at commit `c6902ac6c366ce018e68a810f58b400dda07145a`:

- [ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean), including `check_sound`, `certificate_sound`, 和 `certificate_existence`.
- [RESULTS.md](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/RESULTS.md) 和 [registry](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/registry.json), searched for overlapping statements.
- [Contributor instructions](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/AGENTS.md) 和 [verification script](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/tools/verify.py).

这个 report 没有 a new Lean theorem or certificate instance. Its exact endpoint construction is a separate, conditional one-band specialization; it does not assert satisfaction or impossibility of the repository's full two-band checker.

The requested integration is a draft PR on `gpt/219-block-renormalization`. The current task's explicit branch/PR instruction takes precedence over the older contributor instruction requesting direct commits. The report 和 its separate unformalized index entry are the only proposed repository changes.

### Repository check

Command: `python3 tools/verify.py --changed` after refreshing 和 rebasing onto `origin/main`.

```text
[rules] 4823 Lean files, 287 projects, OK
[changed] against origin/main: 0 new/changed Lean file(s); building 0 module(s); auditing 0 project(s)
[build] up to 1 Lean file(s) at a time
[build] OK
[axioms] 0 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The repository source-rule scan passed. Because the changes consist of Markdown, this invocation compiled zero Lean modules 和 audited zero theorem endpoints. Its success does not formally verify the new mathematical proofs; their status remains **THEOREM**, with written proofs 和 reproducible finite checks.


