# REPORT_220 — Exact constant-band algebra

**Agent:** 220. **Direction:** 0. **Date:** 2026-10-22.

**Answer — THEOREM, with scope.** The exact decimal band dynamics admit a complete carry calculation: regular symbols follow the bulk map \(F(s)=2s\) for \(s<9\), \(F(s)=2s-18\) for \(s>9\); their only cycles have lengths \(1,2,6\). A band of length \(\ell\) retains a certified core of length \(\ell-2m+K_m\) after \(m\) steps, where \(K_m\) counts overflows. The resulting obstructions exclude an infinite palindrome-avoiding orbit whose consecutive column words remain entirely even, 和 exclude every fixed-time return family with an unbounded central \(9\)-band. An internal \(9\)-spacer with opposite carry classes at its flanks loses exactly one position on overflow, giving an explicit absorption budget for growth. Initial complementary flanks alone fail to preserve that condition; an exact counterexample reaches a palindrome at step \(2\). These are scoped obstruction 和 bookkeeping results. Decimal Lychrel existence remains unresolved by this report: an actual growing, palindrome-avoiding finite-interface return remains missing. The executable appendix checks the identities 和 six specified integer trajectories for \(1000\) steps each.

## Scope, notation, 和 source attribution

The result label **THEOREM** means a complete written proof appears below. Formal-verification status of this report: written proofs 和 Python checks; a new Lean proof artifact is absent. Finite computations are reported as evidence for implementation checks, never as a substitute for an infinite argument.

Digits 和 column words are indexed from the units end. For a positive canonical integer with digit list \(d\) of length \(L\), write

\[
q_i=d_i+d_{L-1-i},\qquad
c_0=0,\qquad c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,
\qquad e_i=q_i+c_i-10c_{i+1}.
\]

Let \(\varepsilon=c_L\). If \(\varepsilon=1\), append \(e_L=1\). The new width is \(L'=L+\varepsilon\), 和

\[
T(q)_i=e_i+e_{L'-1-i}.
\]

Thus \(T\) acts on folded column words; the corresponding integer operation is \(R(n)=n+\operatorname{rev}(n)\). A palindrome at the output means \(e=e^{\mathrm{rev}}\). Notation \(s^r\) denotes a word containing \(r\) copies of the symbol \(s\), with commas separating symbols that exceed \(9\).

**THEOREM — realization used in the checks.** A nonempty symmetric word with entries in \([0,18]\), positive outer entry, 和 an even middle entry when its length is odd is realized by a positive canonical decimal integer. For each pair \(i<j=L-1-i\), set \(d_j=\min(9,q_i)\), \(d_i=q_i-d_j\); at an unpaired middle index set \(d_i=q_i/2\). These digits belong to \([0,9]\), their pair sums equal \(q\), 和 the leading digit is positive. This gives the explicit realization used by the appendix.

**Source attribution.** The baseline inspected was commit `c6902ac6c366ce018e68a810f58b400dda07145a`. The nontrivial regular-band arithmetic 和 phase cycles already occur in [BulkPhase.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/D20261015Agent3ComplementaryBulkBulkPhase/BulkPhase.lean), particularly `carry_reset`, `steady_digit`, `complementary_digits`, `even_phase_period_six`, 和 `period_two_iff`. The first-column defect 和 constant tail already occur as `norm_band` in [TemplateStep.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean). The checked-certificate framework already contains `valid_phase_even` 和 `valid_period_mod6` in [CertificatePhases.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificatePhases.lean). The report credits these facts as existing work. Its additional packaging is the exact whole-word formulas, protected-core bound, even-state obstruction, central-\(9\) return obstruction, 和 precise spacer erosion/absorption law. Historical novelty beyond the inspected sources is unclaimed.

## THEOREM 1 — Every constant run, including its first carry

For a column sum \(s\in\{0,\ldots,18\}\) 和 incoming carry \(x\in\{0,1\}\), let

\[
\kappa_s(x)=
\begin{cases}
0,&s\le8,\\
x,&s=9,\\
1,&s\ge10.
\end{cases}
\]

The complete column table is:

| Symbol class | Incoming carry | Output digit | Outgoing carry |
|---|---:|---:|---:|
| \(0\le s\le8\) | \(0\) | \(s\) | \(0\) |
| \(0\le s\le8\) | \(1\) | \(s+1\) | \(0\) |
| \(s=9\) | \(0\) | \(9\) | \(0\) |
| \(s=9\) | \(1\) | \(0\) | \(1\) |
| \(10\le s\le18\) | \(0\) | \(s-10\) | \(1\) |
| \(10\le s\le18\) | \(1\) | \(s-9\) | \(1\) |

Define

\[
u_x=s-9\kappa_s(x),\qquad \delta_x=x-\kappa_s(x).
\]

A run \(s^r\), \(r\ge1\), entered with carry \(x\), produces the exact digit word

\[
\boxed{(u_x+\delta_x)\,u_x^{r-1}.}
\]

**Proof.** In the low case the first digit is \(s+x\), the carry resets to \(0\), 和 subsequent digits are \(s\). In the high case the first digit is \(s+x-10\), the carry resets to \(1\), 和 subsequent digits are \(s-9\). For \(s=9\), carry \(0\) gives only digits \(9\), while carry \(1\) gives only digits \(0\). These are precisely the displayed expression. Each row comes directly from quotient 和 remainder upon division of \(s+x\) by \(10\). This includes \(r=1\), when the tail is empty. \(\square\)

## THEOREM 2 — Refolding the run, with both width cases

Suppose the symmetric input word contains the reflected constant intervals

\[
I=[a,a+r-1],\qquad J=[A,A+r-1],\qquad A=L-a-r.
\]

Let \(x=c_a\), \(y=c_A\), 和 use Theorem 1 to define \(u_x,u_y,\delta_x,\delta_y\).

If \(\varepsilon=0\), then for \(0\le k<r\),

\[
\boxed{T(q)_{a+k}=u_x+u_y+
\delta_x\mathbf1_{k=0}+\delta_y\mathbf1_{k=r-1}.}
\]

If \(\varepsilon=1\), then for \(1\le k<r\),

\[
\boxed{T(q)_{a+k}=u_x+u_y.}
\]

**Proof, unchanged width.** Reflection takes \(a+k\) to \(A+r-1-k\). The first digit receives its transient correction exactly when \(k=0\); the reflected digit receives its transient correction exactly when \(k=r-1\). Adding gives the first identity. When \(r=1\), both corrections occur in the same coefficient. A central run satisfies \(I=J\), hence \(x=y\), 和 the identical formula applies.

**Proof, overflow.** Reflection takes \(a+k\) to \(A+r-k\). For \(1\le k<r\), both positions lie strictly after the first position of their respective input runs. Their transient corrections vanish, giving the second identity. The positions omitted from that interval involve a neighboring run or the appended leading digit. In particular, \(T(q)_0=T(q)_L=e_0+1\). \(\square\)

## THEOREM 3 — Exact whole-word boundary formulas away from \(9\)

Assume \(q_i\ne9\) throughout the input. Set

\[
h_i=\mathbf1_{q_i\ge10},\qquad u_i=q_i-9h_i,\qquad F(q_i)=2u_i.
\]

Then \(c_{i+1}=h_i\). Symmetry gives \(\varepsilon=h_{L-1}=h_0\).

### Case \(\varepsilon=0\): a discrete second difference

Set \(h_{-1}=h_L=0\). Then

\[
\boxed{T(q)_i=F(q_i)+h_{i-1}+h_{i+1}-2h_i,
\quad 0\le i<L.}
\]

**Proof.** The normalized digit is
\(e_i=q_i+h_{i-1}-10h_i\), with \(h_{-1}=0\) at the units endpoint. For an interior reflection \(j=L-1-i\), symmetry gives \(q_j=q_i\), \(h_j=h_i\), 和 \(h_{j-1}=h_{i+1}\). Therefore

\[
e_i+e_j=2q_i+h_{i-1}+h_{i+1}-20h_i
=F(q_i)+h_{i-1}+h_{i+1}-2h_i.
\]

For \(L\ge2\), the endpoint value is \(e_0+e_{L-1}=2q_0+h_1\), since \(h_0=h_{L-1}=0\); symmetry gives the identical value at the other endpoint. For \(L=1\), both exterior indicators are \(0\), 和 \(T(q)_0=2q_0\). Thus the formula covers every position.

For a run \(s^r\), \(r\ge2\), with adjacent symbols \(p,t\), its endpoint corrections are \(h(p)-h(s)\) 和 \(h(t)-h(s)\). Its interior consists of \(F(s)\). For \(r=1\), the corrections add in the single coefficient. Exterior ghost indicators are used at word endpoints.

### Case \(\varepsilon=1\): an adjacent-sum formula

Then

\[
\boxed{
T(q)_0=u_0,\qquad
T(q)_i=u_{i-1}+u_i\ (1\le i<L),\qquad
T(q)_L=u_{L-1}.
}
\]

**Proof.** At the outer pair, \(e_0=q_0-10\), \(e_L=1\), hence \(T(q)_0=q_0-9=u_0\). Reflection gives \(T(q)_L=u_{L-1}=u_0\). At an interior position, symmetry yields

\[
\begin{aligned}
e_i&=q_i+h_{i-1}-10h_i,\\
e_{L-i}&=q_{i-1}+h_i-10h_{i-1}.
\end{aligned}
\]

Their sum is \(u_i+u_{i-1}\). For \(L=1\), the interior index range is empty, leaving exactly the correctly computed outer pair. \(\square\)

Consequently, a direct interface \(p\mid s\) creates exactly \(u(p)+u(s)\) in an overflowing step. A run of length \(r\) supplies \(r-1\) adjacent equal pairs with output \(F(s)\). The reset-only hypothesis must be rechecked before applying this whole-word identity at another step: interfaces can create \(9\).

For complementary symbols \(a\in\{1,\ldots,8\}\), \(b=18-a\), the overflow interface value is exactly \(a+(b-9)=9\). At a direct interface in a step without overflow, with both neighboring runs of length at least \(2\), the affected coefficients are \(2a+1\) 和 \(17-2a\). For \(a=4,b=14\), these are both \(9\).

## THEOREM 4 — Protected cores, phase cycles, 和 return restrictions

For every \(s\ne9\), define

\[
F(s)=\begin{cases}2s,&0\le s\le8,\\2s-18,&10\le s\le18.\end{cases}
\]

If \(q=s\) on \([a,b]\), then \(T(q)=F(s)\) on

\[
\boxed{[a+1,b-1+\varepsilon].}
\]

This assertion permits arbitrary symbols, including \(9\), outside the designated interval.

**Proof, unchanged width.** For \(a+1\le i\le b-1\), the columns at \(i-1,i,i+1\) equal \(s\). Both the digit at \(i\) 和 the reflected digit at \(L-1-i\) receive the reset carry \(h(s)\), because the columns immediately preceding them are \(q_{i-1}\) 和 \(q_{i+1}\). Their sum is \(2(s-9h(s))=F(s)\).

**Proof, overflow.** For \(a+1\le i\le b\), the relevant input columns are \(q_{i-1}=q_i=s\). The reflected output digit lies at \(L-i\), whose input symbol is \(q_{i-1}\) 和 whose preceding input symbol is \(q_i\). Each output digit again equals \(s-9h(s)\). This gives the claimed interval.

Every \(F(s)\) is even, hence differs from \(9\). Induction therefore applies without assumptions about the exterior. If \(K_m\) counts overflows in the first \(m\) steps, the certified interval after \(m\) steps is

\[
\boxed{[a+m,b-m+K_m],\qquad
\ell_m=\ell-2m+K_m,\qquad
q^{(m)}=F^m(s)\text{ on that interval}.}
\]

The assertion applies while the interval is nonempty. Each step increases its left endpoint by \(1\); its right endpoint decreases by \(1\) without overflow 和 remains fixed with overflow. This proves the formula. It is a guarantee for the designated core, rather than a claim that the complete maximal run always loses exactly that many positions.

The one-step bounds are sharp:

\[
(1,10,2,2,2,10,1)\xrightarrow{\varepsilon=0}(3,0,5,4,5,0,3),
\]
\[
(10,2,2,2,10)\xrightarrow{\varepsilon=1}(1,3,4,4,3,1).
\]

In the first example only the middle position of the original \(2^3\) run attains \(F(2)=4\); in the second example exactly the guaranteed pair does.

### Complete symbol map

The cycles are

\[
0\to0,\qquad18\to18,\qquad6\to12\to6,
\]
\[
2\to4\to8\to16\to14\to10\to2.
\]

The remaining regular symbols enter those cycles after \(1\) step:

| \(s\) | \(1\) | \(3\) | \(5\) | \(7\) | \(11\) | \(13\) | \(15\) | \(17\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| \(F(s)\) | \(2\) | \(6\) | \(10\) | \(14\) | \(4\) | \(8\) | \(12\) | \(16\) |

**Proof of completeness.** Substitution into the displayed formula gives every arrow. The cycles contain every even symbol in \([0,18]\); the table contains every odd symbol except \(9\). Thus every regular symbol is accounted for. \(\square\)

**Return corollary.** Consider a family with a designated band whose length tends to infinity, a fixed positive return time \(m\), 和 bounded displacement of the designated band's endpoints between the source 和 target family members. If the returned band carries the same label \(s\ne9\), then \(F^m(s)=s\).

**Proof.** For sufficiently long bands, the protected core intersects the returned designated interval. On that intersection its value is both \(F^m(s)\) 和 \(s\). Hence the values agree. The bounded displacement hypothesis holds for affine run lengths under a fixed translation of the length parameters. \(\square\)

It follows that odd regular labels cannot occur at a returning phase; labels \(6,12\) require \(2\mid m\); labels \(2,4,8,10,14,16\) require \(6\mid m\). The fixed labels \(0,18\) impose neither divisibility condition. If only an unordered complementary pair is recorded, the information is weaker: \(\{2,16\}\to\{4,14\}\to\{8,10\}\to\{2,16\}\), 和 \(\{6,12\}\) returns as a set after one step. Such label exchange is distinct from returning an ordered template.

**General even-base corollary.** For an even base \(b\), put \(h=b-1\). The regular bulk map is \(F_b(s)=2s\) for \(s<h\), 和 \(F_b(s)=2s-2h\) for \(s>h\). For \(s=2r\), \(1\le r<h\),

\[
F_b(2r)=2(2r\bmod h),\qquad
\text{period}(2r)=\operatorname{ord}_{h/\gcd(r,h)}(2).
\]

**Proof.** The carry table from Theorem 1 replaces \(9,10\) by \(h,b\). Substitution gives the displayed residue formula. Because \(h\) is odd, multiplication by \(2\) is invertible modulo \(h\). A return after \(m\) steps means \((2^m-1)r\equiv0\pmod h\), equivalent to \(2^m\equiv1\pmod{h/\gcd(r,h)}\). The endpoints \(0,2h\) are separate fixed points. This is a bulk classification, with no conclusion about finite decimal existence. \(\square\)

## THEOREM 5 — Consecutive entirely even column states force a palindrome

Suppose each entry of \(q\) is even. Then

\[
\boxed{T(q)\text{ is entrywise even}\iff q_i\le8\text{ for every }i.}
\]

Under these equivalent conditions, the decimal output \(R(n)\) is a palindrome.

**Proof.** Since \(q\) is entrywise even, it avoids \(9\), 和 Theorem 3 applies.

If the step overflows, then \(T(q)_0=q_0-9\) is odd, contradicting an entirely even next word.

For a step without overflow, \(h_0=0\). If \(L=1\), the single input entry is therefore at most \(8\). If \(L\ge2\), endpoint parity gives \(T(q)_0\equiv h_1\pmod2\), hence \(h_1=0\). At each interior position,

\[
T(q)_i\equiv h_{i-1}+h_{i+1}\pmod2.
\]

Evenness forces \(h_{i+1}=h_{i-1}\), since the indicators lie in \(\{0,1\}\). Starting from \(h_0=h_1=0\), induction forces every \(h_i=0\). Thus every input entry is at most \(8\).

Conversely, if every input entry is even 和 at most \(8\), each carry is \(0\), so \(e=q\). The output digit word is symmetric 和 its folded word is \(2q\), which is entirely even. \(\square\)

**Obstruction.** A palindrome-avoiding trajectory cannot contain a transition in which both successive column words are entirely even. In particular, a template whose allowed symbols remain entirely even at every phase cannot give a Lychrel construction. This leaves open templates with even bulk bands 和 odd coefficients in bounded interface blocks. Those blocks carry an essential obligation that the bulk cycles alone omit.

## THEOREM 6 — Exceptional \(9\)-bands 和 the central-band obstruction

For reflected \(9\)-runs entered with carries \(x,y\), Theorem 2 gives the bulk value

\[
\boxed{G(x,y)=9(2-x-y).}
\]

It occupies the entire run without overflow 和 the interval with its first position removed under overflow.

For an internal maximal \(9\)-run with neighboring non-\(9\) symbols \(p,t\), the entering carries are

\[
x=h(p),\qquad y=h(t).
\]

The second identity follows because the symbol preceding the reflected run is \(t\). Hence the full table is:

| Left flank class | Right flank class | Bulk image |
|---|---|---:|
| \(p\le8\) | \(t\le8\) | \(18\) |
| \(p\le8\) | \(t\ge10\) | \(9\) |
| \(p\ge10\) | \(t\le8\) | \(9\) |
| \(p\ge10\) | \(t\ge10\) | \(0\) |

**Proof.** For \(s=9\), \(\delta_x=\delta_y=0\), \(u_x=9(1-x)\), 和 \(u_y=9(1-y)\). Theorem 2 gives the formula at every stated position. Each neighboring non-\(9\) symbol resets the entering carry to its own high/low indicator. Substitution of the four possible indicator pairs gives the table. \(\square\)

**Central-band corollary.** Suppose \([a,b]\) is central, meaning \(a+b=L-1\), 和 consists of \(r\) copies of \(9\). Its reflected run is itself, so \(x=y\). Its image therefore contains a central core consisting entirely of \(0\) or entirely of \(18\).

For any fixed \(m\ge1\) 和 \(r>2m\), the word after \(m\) steps contains a nonempty central core of that same extreme symbol. Consequently it cannot contain a central \(9\)-run.

**Proof.** After the first step, retain the conservative core \([a+1,b-1+\varepsilon_1]\), whose value is \(0\) or \(18\). Theorem 4 propagates it through the remaining steps, since both values are fixed points of \(F\). Its interval is \([a+m,b-m+K_m]\), of positive length \(r-2m+K_m\). The sum of its endpoints is \(L-1+K_m=L_m-1\), so it is central in the new word. Any central \(9\)-run would overlap this nonempty central constant interval, contradicting its value. \(\square\)

This excludes a fixed-time return family with an unbounded central \(9\)-band, irrespective of how its exterior bounded blocks are chosen. For a noncentral returning \(9\)-band, a phase that sends its protected bulk to \(0\) or \(18\) likewise prevents a bounded-displacement return to \(9\) in fixed finite time. A persistent \(9\)-band therefore needs opposite paired entering carries at every phase while it remains a designated unbounded band.

## THEOREM 7 — Exact erosion 和 absorption budget for a \(9\)-spacer

Let \([a,b]\) be a maximal internal \(9\)-run of length \(N\ge2\), with non-\(9\) flanks \(p=q_{a-1}\), \(t=q_{b+1}\). Assume opposite carry classes:

\[
A=h(p),\qquad B=h(t),\qquad A+B=1.
\]

On an overflow step, its next maximal \(9\)-run is exactly

\[
\boxed{[a+1,b],\qquad N'=N-1,}
\]

with adjacent symbols \(H(p),H(t)\), where

\[
H(s)=\begin{cases}s+10,&s\le8,\\s-10,&s\ge10.\end{cases}
\]

**Proof with boundary carries.** Write \(D(s,z)=(s+z)\bmod10\). The interior coefficients are \(D(9,A)+D(9,B)=9\). At the left boundary, the reflected neighboring column is \(p\) entered with carry \(B\); at the right boundary, \(t\) is entered with carry \(A\). Thus

\[
\begin{aligned}
T(q)_a
&=D(9,A)+D(p,B)\\
&=9(1-A)+p+B-10A\\
&=p+10-20A=H(p),\\
T(q)_{b+1}
&=D(t,A)+D(9,B)\\
&=t+A-10B+9(1-B)\\
&=t+10-20B=H(t).
\end{aligned}
\]

For low \(s\), \(H(s)\in[10,18]\); for high \(s\), \(H(s)\in[0,8]\). Neither boundary is \(9\), establishing maximality. The carry classes flip, so the new flanks remain opposite. This proof covers both orientations \((A,B)=(0,1)\) 和 \((1,0)\). \(\square\)

For completeness, without the opposite-class assumption the overflow boundary values adjoining a maximal internal \(9\)-run are

\[
\boxed{T(q)_a=p+9+B-19A,\qquad
T(q)_{b+1}=t+9+A-19B.}
\]

They follow from the same digit sums before substituting \(A+B=1\). The interior is \(9(2-A-B)\).

**Conditional growth budget.** Suppose the tracked maximal spacer retains opposite flank classes at every intermediate phase, with length at least \(2\) immediately before each overflow 和 a nonempty descendant interval throughout the tracked evolution. A step without overflow preserves its entire current interval; let \(g_{\mathrm L},g_{\mathrm R}\ge0\) count newly absorbed \(9\)-positions immediately outside it. Summing the exact per-step changes gives

\[
\boxed{
N_m-N_0=-K_m+
\sum_{\varepsilon_j=0}(g_{\mathrm L,j}+g_{\mathrm R,j}).
}
\]

Therefore positive spacer growth requires more positions absorbed during steps without overflow than the number of overflow steps. A growing full-template return must establish this budget from actual boundary blocks 和 must separately establish persistence of the opposite-flank condition. Equality of left 和 right absorption is an additional condition, rather than a consequence of merely having opposite flanks.

There is real absorption: the finite symmetric word

\[
4^2\,9^3\,14^3\,9^3\,4^2
\xrightarrow{\varepsilon=0}
8\,9^5\,10\,9^5\,8
\]

grows each spacer by \(2\). The carry entering the first \(9\)-run is \(0\), entering the reflected run is \(1\); the adjacent \(4\)-column gives \(4+5=9\), 和 the adjacent \(14\)-column gives \(4+5=9\). The outer retained \(4\)-pair gives \(8\), 和 the middle retained \(14\)-pair gives \(10\). These values establish the displayed whole word. This is a single-step identity; the new finite fronts must be tracked at later phases.

## THEOREM 8 — Exact counterexamples to unguarded extensions

### Counterexample: a bulk cycle with an immediate palindrome

The nonpalindromic integer \(15\) has folded column word \((6,6)\), whose regular symbol follows the bulk cycle \(6\leftrightarrow12\). Yet \(15+51=66\) is immediately palindromic. The carries are \((0,0,0)\), 和 the output digits are \((6,6)\). Thus periodic regular symbols alone cannot supply the safety part of a return certificate.

### Counterexample: complementary flanks disappear

Consider the valid symmetric column word

\[
q=1,0,4,9^3,14,0,2,0,14,9^3,4,0,1.
\]

The respective flank pairs are initially \((4,14)\) 和 \((14,4)\). Nevertheless,

\[
q\xrightarrow{\varepsilon=0}
2,0,9^4,8,1,4,1,8,9^4,0,2
\]

\[
\xrightarrow{\varepsilon=0}
4,0,18^4,16,2,8,2,16,18^4,0,4.
\]

The full first carry vector, including the initial 和 terminal carries, is

\[
(0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,0),
\]

和 its output digit vector is

\[
(1,0,4,9,9,9,4,1,2,0,4,0,0,0,5,0,1).
\]

Refolding gives the displayed first successor. Its spacers have low/low flanks \((0,8)\) 和 \((8,0)\). Every symbol of that successor is at most \(9\), so the next carry vector consists of \(18\) zeros. The next digit word equals that symmetric input column word; the integer reaches a palindrome at step \(2\), 和 its folded word is the displayed doubled word.

**Scope of the refutation.** The claim that initial complementary flanks suffice for perpetual spacer persistence is false. Theorem 7 requires its guard at each intermediate phase. The code continues this rejected example for the full \(1000\) steps; continuation after the first palindrome serves only to check the arithmetic implementation.

## Numerical checks: purpose 和 interpretation

The appendix performs bounded identity checks, followed by six explicitly specified trajectories. It searches neither a large seed space nor a large template space.

- Every realizable symmetric column word of length at most \(6\) is checked against the applicable reflected-run identities: \(10{,}467\) words 和 \(32{,}160\) run positions.
- The whole-word reset formulas are checked on \(9{,}070\) words; the entirely even obstruction is checked on \(1{,}998\) words.
- Overflow boundaries adjoining \(9\)-runs are checked at \(693\) positions.
- Six explicit integer trajectories are continued for \(1000\) steps. At each step, direct integer addition with decimal reversal is compared with the digit/carry implementation. Protected intervals are checked wherever nonempty.

For the long-band checks let \(r=2004\). Their initial column words are

\[
2^r16^{2r}2^r,\qquad
6^r12^{2r}6^r,\qquad
12^2 9^r12^2,\qquad
2^2 9^r16^4 9^r2^2.
\]

The code's `realize` function specifies each seed exactly; short hashes identify the generated decimal strings without printing thousands of digits.

| Check | Steps | First palindrome through step \(1000\) | Final protected cores, as (symbol, length) |
|---|---:|---:|---|
| `six_phase` | 1000 | none observed | \((14,411),(4,2415),(14,411)\) |
| `two_phase` | 1000 | none observed | \((6,423),(12,2427),(6,423)\) |
| `central_nine` | 1000 | \(2\) | \((0,418)\) |
| `paired_nines` | 1000 | none observed | \((0,411),(0,411)\) |
| `rejected_bulk_only_15` | 1000 | \(1\) | exhausted |
| `rejected_spacer_guard` | 1000 | \(2\) | exhausted |

These finite non-hits establish only the reported finite checks. In particular, the `paired_nines` example loses its neutral bulk: its surviving protected cores are \(0\), despite the absence of a palindrome within the checked window. None of the listed trajectories supplies a growing return identity.

## IDEA — The sharp remaining question

Can fixed finite boundary blocks be chosen so that, after a positive return time \(m\), the complete symmetric word returns with every designated long-run length increased, while every intermediate digit output is nonsymmetric? For an ordered template containing a nontrivial regular band, the period must respect the \(2\)- or \(6\)-cycle above. If a noncentral \(9\)-spacer is used, its actual flank guard must persist at every phase 和 its absorption must exceed its overflow loss. An unbounded central \(9\)-band is excluded. A solution must therefore give the full finite-front return, its run-length translation, 和 its intermediate palindrome guards; bulk periodicity leaves precisely those obligations unresolved.

## Reproducible code 和 actual output

Run the following Python 3 program. It uses only the standard library. The finite cases are formula verification; the six long trajectories are fixed diagnostic inputs.

```python
from itertools import product
from hashlib import sha256
import sys

sys.set_int_max_str_digits(0)


def step(q):
    carries, digits = [0], []
    for s in q:
        v = s + carries[-1]
        digits.append(v % 10)
        carries.append(v // 10)
    if carries[-1]:
        digits.append(1)
    folded = [x + y for x, y in zip(digits, reversed(digits))]
    return folded, carries, digits


def regular_formula(q):
    h = [int(s >= 10) for s in q]
    u = [s - 9 * a for s, a in zip(q, h)]
    if h[0]:
        return [u[0]] + [u[i - 1] + u[i] for i in range(1, len(q))] + [u[-1]]
    hp = [0] + h + [0]
    return [2 * u[i] + hp[i] + hp[i + 2] - 2 * h[i] for i in range(len(q))]


def runs(q):
    a = 0
    while a < len(q):
        b = a
        while b + 1 < len(q) and q[b + 1] == q[a]:
            b += 1
        yield a, b, q[a]
        a = b + 1


def bulk(s):
    assert s != 9
    return 2 * s if s < 9 else 2 * s - 18


words = regular = positions = even_words = spacer_checks = 0
for length in range(1, 7):
    for half in product(range(19), repeat=(length + 1) // 2):
        if half[0] == 0 or (length % 2 and half[-1] % 2):
            continue
        q = list(half) + list(reversed(half[:length // 2]))
        qp, c, e = step(q)
        words += 1
        if 9 not in q:
            assert qp == regular_formula(q), q
            regular += 1
        if all(s % 2 == 0 for s in q):
            condition = all(s <= 8 for s in q)
            assert all(s % 2 == 0 for s in qp) == condition, q
            if condition:
                assert e == e[::-1]
            even_words += 1
        for a, b, s in runs(q):
            r, A = b - a + 1, length - 1 - b
            x, y = c[a], c[A]
            kx = x if s == 9 else int(s >= 10)
            ky = y if s == 9 else int(s >= 10)
            ux, uy = s - 9 * kx, s - 9 * ky
            dx, dy = x - kx, y - ky
            if c[-1]:
                for k in range(1, r):
                    assert qp[a + k] == ux + uy
                    positions += 1
            else:
                for k in range(r):
                    assert qp[a + k] == ux + uy + dx * (k == 0) + dy * (k == r - 1)
                    positions += 1
            if s == 9 and a > 0 and b + 1 < length and c[-1]:
                p, t = q[a - 1], q[b + 1]
                px, ty = int(p >= 10), int(t >= 10)
                assert qp[a] == p + 9 + ty - 19 * px
                assert qp[b + 1] == t + 9 + px - 19 * ty
                if px + ty == 1:
                    assert qp[a] != 9 and qp[b + 1] != 9
                    assert qp[a + 1:b + 1] == [9] * (r - 1)
                spacer_checks += 1

print(f"Finite identities: words={words}, regular={regular}, run_positions={positions}")
print(f"Even-state obstruction: words={even_words}")
print(f"Overflow interfaces adjoining 9-runs: checks={spacer_checks}")

for s in range(19):
    if s != 9:
        v = bulk(s)
        for _ in range(6):
            v = bulk(v)
        assert v == bulk(s)
print("Regular phase table: all 18 symbols passed F^7(s)=F(s)")


def realize(q):
    assert q == q[::-1] and q[0] > 0
    d = [0] * len(q)
    for i in range(len(q) // 2):
        j = len(q) - 1 - i
        d[j] = min(q[i], 9)
        d[i] = q[i] - d[j]
    if len(q) % 2:
        i = len(q) // 2
        assert q[i] % 2 == 0
        d[i] = q[i] // 2
    n = int("".join(map(str, reversed(d))))
    assert [x + y for x, y in zip(d, reversed(d))] == q
    return n


def orbit_check(label, n, expected_q=None):
    text = str(n)
    d = [int(x) for x in reversed(text)]
    q = [x + y for x, y in zip(d, reversed(d))]
    if expected_q is not None:
        assert q == expected_q
    protected = [list(v) for v in runs(q)]
    initial_width = len(q)
    initial_digest = sha256(text.encode()).hexdigest()[:16]
    first_palindrome = 0 if text == text[::-1] else None
    overflows = 0
    core_checks = 0
    for time in range(1, 1001):
        qp, c, e = step(q)
        predicted_cores = []
        for a, b, s in protected:
            if a > b:
                continue
            assert q[a:b + 1] == [s] * (b - a + 1)
            if s == 9:
                s_next = 9 * (2 - c[a] - c[len(q) - 1 - b])
            else:
                s_next = bulk(s)
            aa, bb = a + 1, b - 1 + c[-1]
            if aa <= bb:
                assert qp[aa:bb + 1] == [s_next] * (bb - aa + 1)
                predicted_cores.append([aa, bb, s_next])
                core_checks += 1
        n_next = n + int(text[::-1])
        next_text = str(n_next)
        assert "".join(map(str, reversed(e))) == next_text
        if first_palindrome is None and next_text == next_text[::-1]:
            first_palindrome = time
        overflows += c[-1]
        n, text, q, protected = n_next, next_text, qp, predicted_cores
    assert len(q) == initial_width + overflows
    cores = [(s, b - a + 1) for a, b, s in protected]
    print(
        f"{label}: steps=1000, initial_digits={initial_width}, "
        f"final_digits={len(q)}, overflows={overflows}, "
        f"first_palindrome={first_palindrome}, core_checks={core_checks}, "
        f"cores={cores}, seed_sha256_16={initial_digest}, "
        f"final_sha256_16={sha256(text.encode()).hexdigest()[:16]}"
    )


R = 2004
cases = [
    ("six_phase", [2] * R + [16] * (2 * R) + [2] * R),
    ("two_phase", [6] * R + [12] * (2 * R) + [6] * R),
    ("central_nine", [12] * 2 + [9] * R + [12] * 2),
    ("paired_nines", [2] * 2 + [9] * R + [16] * 4 + [9] * R + [2] * 2),
]
for label, q in cases:
    orbit_check(label, realize(q), q)
orbit_check("rejected_bulk_only_15", 15)
bad_spacer = [1, 0, 4] + [9] * 3 + [14, 0, 2, 0, 14] + [9] * 3 + [4, 0, 1]
orbit_check("rejected_spacer_guard", realize(bad_spacer), bad_spacer)
trace = bad_spacer
for time in range(3):
    print(f"Rejected spacer trace t={time}: q={trace}")
    trace, _, _ = step(trace)

for q in ([2, 10, 2], [4, 4, 14, 14, 4, 4], [14, 14, 4, 4, 14, 14]):
    qp, c, e = step(list(q))
    print(f"Example: q={q}, e_units_first={e}, overflow={c[-1]}, q_next={qp}")
for q, expected in (
    ([1, 10, 2, 2, 2, 10, 1], [3, 0, 5, 4, 5, 0, 3]),
    ([10, 2, 2, 2, 10], [1, 3, 4, 4, 3, 1]),
    ([4] * 2 + [9] * 3 + [14] * 3 + [9] * 3 + [4] * 2,
     [8] + [9] * 5 + [10] + [9] * 5 + [8]),
):
    assert step(q)[0] == expected
print("Sharp core bounds and spacer-growth witnesses: passed")
print("PASS: finite identities and all six 1000-step integer checks")
```

**Actual output:**

```text
Finite identities: words=10467, regular=9070, run_positions=32160
Even-state obstruction: words=1998
Overflow interfaces adjoining 9-runs: checks=693
Regular phase table: all 18 symbols passed F^7(s)=F(s)
six_phase: steps=1000, initial_digits=8016, final_digits=8423, overflows=407, first_palindrome=None, core_checks=3000, cores=[(14, 411), (4, 2415), (14, 411)], seed_sha256_16=e51e814b9151888e, final_sha256_16=d8a4c6ff706bfebd
two_phase: steps=1000, initial_digits=8016, final_digits=8435, overflows=419, first_palindrome=None, core_checks=3000, cores=[(6, 423), (12, 2427), (6, 423)], seed_sha256_16=3ae528056d74915e, final_sha256_16=40cc6901990c6be4
central_nine: steps=1000, initial_digits=2008, final_digits=2422, overflows=414, first_palindrome=2, core_checks=1002, cores=[(0, 418)], seed_sha256_16=09611954e562f534, final_sha256_16=888dde38c27bd15c
paired_nines: steps=1000, initial_digits=4016, final_digits=4423, overflows=407, first_palindrome=None, core_checks=2001, cores=[(0, 411), (0, 411)], seed_sha256_16=f49dee59e910e503, final_sha256_16=716985f941aee631
rejected_bulk_only_15: steps=1000, initial_digits=2, final_digits=416, overflows=414, first_palindrome=1, core_checks=0, cores=[], seed_sha256_16=e629fa6598d73276, final_sha256_16=86578a35ae39e625
rejected_spacer_guard: steps=1000, initial_digits=17, final_digits=432, overflows=415, first_palindrome=2, core_checks=2, cores=[], seed_sha256_16=44a50ab8c6c0557e, final_sha256_16=b4df20317318e1cc
Rejected spacer trace t=0: q=[1, 0, 4, 9, 9, 9, 14, 0, 2, 0, 14, 9, 9, 9, 4, 0, 1]
Rejected spacer trace t=1: q=[2, 0, 9, 9, 9, 9, 8, 1, 4, 1, 8, 9, 9, 9, 9, 0, 2]
Rejected spacer trace t=2: q=[4, 0, 18, 18, 18, 18, 16, 2, 8, 2, 16, 18, 18, 18, 18, 0, 4]
Example: q=[2, 10, 2], e_units_first=[2, 0, 3], overflow=0, q_next=[5, 0, 5]
Example: q=[4, 4, 14, 14, 4, 4], e_units_first=[4, 4, 4, 5, 5, 4], overflow=0, q_next=[8, 9, 9, 9, 9, 8]
Example: q=[14, 14, 4, 4, 14, 14], e_units_first=[4, 5, 5, 4, 4, 5, 1], overflow=1, q_next=[5, 10, 9, 8, 9, 10, 5]
Sharp core bounds and spacer-growth witnesses: passed
PASS: finite identities and all six 1000-step integer checks
```
