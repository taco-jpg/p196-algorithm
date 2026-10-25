# REPORT_209 — Binary embedding obstructions

Agent: **209**. Direction: **9 (wildcard)**. Date: **2026-10-22**.

**Answer (one paragraph).** Decimal Lychrel witness: **没有**. **THEOREM:** a literal digit substitution of the binary expanding family cannot return with longer runs after any fixed number of decimal steps, once the runs exceed an explicit bound; the result 也 covers constant-digit codeblocks of unequal fixed widths. **THEOREM:** arbitrary uniform decimal codeblocks, of every positive width, cannot reproduce the binary four-phase mechanism one step at a time: four particular transitions at parameter \(n=5\) already give a contradiction, including encodings with leading zeros. The first result uses exact transport of paired constant bands; the second uses a finite modular telescope of reversed leading digits, inspired by a 10-adic endpoint calculation. The report includes complete carry proofs 和 executable 1,000-step controls. **IDEA:** bounded correction blocks, nonconstant codeblocks with changed intermediate phases, 和 altered time scales remain possible; obtaining a compatible expanding return in 那个 larger class remains unresolved.

## 1. Status, scope, 和 provenance

**THEOREM** labels below mean complete written proofs. New **LEAN-VERIFIED** results: **没有**. The numerical controls check formulas 和 expose failed constructions; a finite palindrome-free observation leaves infinite avoidance unresolved.

The mathematical objects in 这个 report concern arbitrary positive integers 和 explicit binary-template images. The repository name identifies the source project only.

Repository audit used commit `c6902ac6c366ce018e68a810f58b400dda07145a`. Existing sources consulted:

- [ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean): the existing conditional return-certificate framework.
- [CoordinateDynamics.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent6CoordinateDynamics/CoordinateDynamics.lean) 和 [CoordinateCycle.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent6CoordinateDynamics/CoordinateCycle.lean): the existing signed exterior-coordinate update 和 closed-cycle cancellation.
- [CylinderNoContinuity.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent112TenadicCylinderImage/CylinderNoContinuity.lean): an existing arithmetic obstruction to ordinary 10-adic continuity.

**IDEA — relationship to earlier results.** The basic telescoping mechanism already occurs in the cited exterior-coordinate results. 这个 report 的 contribution applies the mechanism to literal digit-code embeddings, obtains a uniform finite obstruction independent of the unknown block width, 和 combines it with a separate arbitrary-time obstruction for constant-digit codeblocks. The nowhere-continuity observation belongs to the cited earlier results. The supplied outer-prefix SCC measurement is unnecessary for the proofs.

## 2. Conventions 和 complete decimal carry accounting

Words use most significant digit first unless explicitly described as low-first. Concatenation denotes concatenation of words; \(a^n\) denotes a run of \(n\) copies of digit \(a\). Ordinary powers of integers occur in numeric formulas such as \(10^k\). Define

\[
T_b(N)=N+\operatorname{rev}_b(N).
\]

Reversal uses the canonical representation of the positive integer. Encoding a word as an integer removes its leading zeros. Binary words, decimal words, 和 integer values will be distinguished explicitly.

**THEOREM 1 — carry identity, including overflow.** Take \(N>0\) of decimal width \(L\), with digits \(d_0,\ldots,d_{L-1}\) in low-first order. Set

\[
q_i=d_i+d_{L-1-i},\qquad c_0=0,
\]
\[
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,
\qquad e_i=q_i+c_i-10c_{i+1}.
\]

Then \(c_i\in\{0,1\}\), \(e_i\in\{0,\ldots,9\}\), 和

\[
T_{10}(N)=\sum_{i=0}^{L-1}e_i10^i+c_L10^L.
\tag{1}
\]

The output width 是 \(L+c_L\). For every \(1\le r\le L\), define

\[
H_r(N)=\sum_{i=0}^{r-1}d_{L-1-i}10^i.
\]

Thus \(H_r\) reads the first \(r\) canonical leading digits as low-first digits. The exact cut identity gives

\[
T_{10}(N)-N\equiv H_r(N)\pmod{10^r}.
\tag{2}
\]

**Proof.** Since \(0\le q_i\le18\), induction from \(c_0=0\) gives \(0\le q_i+c_i\le19\), hence precisely the stated carry 和 digit ranges. Multiplying

\[
q_i+c_i=e_i+10c_{i+1}
\]

by \(10^i\), then summing through column \(r-1\), cancels every internal carry 和 leaves

\[
\sum_{i<r}e_i10^i=\sum_{i<r}q_i10^i-c_r10^r.
\tag{3}
\]

At \(r=L\), restoring the terminal carry gives (1). If \(c_L=0\), the top digit remains positive 因为 \(q_{L-1}\ge d_{L-1}\ge1\). If \(c_L=1\), appending that carry supplies a new leading digit \(1\). 这 accounts for the \(2\) possible widths. Reducing (3) modulo \(10^r\) 和 substituting the definition of \(q_i\) proves (2). The carry across the cut contributes exactly \(c_r10^r\), fully accounting for 那个 boundary. \(\square\)

## 3. Constant bands: an arbitrary-time obstruction

**THEOREM 2 — paired-band transport.** Suppose a positive decimal integer of width \(L\) satisfies

\[
d_i=x,\qquad d_{L-1-i}=y\qquad(A\le i\le B),
\]

where \(0\le A\le B<L\) 和 \(0\le x,y\le9\). Write \(s=x+y\). After one step, on the smaller paired interval

\[
A+1\le i\le B-1,
\]

the output low band 和 output high band are constant, with the following exhaustive possibilities:

| Input sum | Output low band | Output high band |
| --- | ---: | ---: |
| \(s\le8\) | \(s\) | \(s\) |
| \(s=9\) | a constant in \(\{0,9\}\) | a constant in \(\{0,9\}\) |
| \(s\ge10\) | \(s-9\) | \(s-9\) |

In the middle row, the constants can differ.

**Proof, with the shifted reflection axis.** On each original physical band, \(q_j=s\). The three carry cases 是:

\[
\begin{array}{c|cc}
q_j & c_j=0 & c_j=1\\ \hline
s\le8 & (e_j,c_{j+1})=(s,0)&(s+1,0)\\
s=9 &(9,0)&(0,1)\\
s\ge10 &(s-10,1)&(s-9,1)
\end{array}
\]

Thus \(s\le8\) resets the carry to zero; \(s\ge10\) resets it to one; \(s=9\) preserves it. A digit following a reset inside the same band consequently equals \(s\) in the first case, or \(s-9\) in the last case. In the middle case the carry is constant throughout each physical band, giving a constant output \(9\) or \(0\).

Let the actual output width be \(L+\varepsilon\), with \(\varepsilon=c_L\in\{0,1\}\). For a surviving low index \(i\), its predecessor \(i-1\) lies in the original low band. The new reflected position 和 its predecessor 是

\[
j'=L+\varepsilon-1-i=(L-1)-(i-\varepsilon),
\]
\[
j'-1=(L-1)-(i-\varepsilon+1).
\]

If \(\varepsilon=0\), their old reflected indices 是 \(i,i+1\), which lie in \([A,B]\). If \(\varepsilon=1\), they 是 \(i-1,i\), which 也 lie in \([A,B]\). Therefore the incoming-carry calculation applies to the new reflected band in each overflow case. The table follows. \(\square\)

**THEOREM 2a — persistent equality.** Once the surviving paired bands agree, equality persists under later contractions while the interval remains nonempty. Indeed, the sum of an equal pair \((u,u)\) equals the even integer \(2u\ne9\), so THEOREM 2 forces another equal pair. If the first paired sum equals \(9\), subsequent bands remain within \(\{0,9\}\): the possible sums \(0,9,18\) produce only the digits. 这个 proof treats the exceptional sum explicitly 和 permits different incoming carries at opposite ends.

**THEOREM 3 — literal binary digit relabeling cannot yield a return.** Define the canonical decimal word

\[
S_n(a,b)=b\,a\,b^n\,a\,b\,a^n,
\qquad 0\le a,b\le9,\quad a\ne b,\quad b\ne0.
\]

For every

\[
m\ge1,\qquad n\ge2m+3,\qquad g\ge0,
\]

\[
\boxed{T_{10}^{m}(S_n(a,b))\ne S_{n+g}(a,b).}
\tag{4}
\]

**Proof.** Initially, on the paired interval \(I_0=[2,n-1]\), the low digit equals \(a\) 和 the high digit equals \(b\). After \(m\) applications of THEOREM 2, the surviving interval 是

\[
I_m=[2+m,n-1-m].
\]

The bound \(n\ge2m+3\) makes 这个 interval nonempty. In any proposed target \(S_{n+g}(a,b)\), the paired positions 还 contain the distinct digits \(a,b\).

If \(a+b\ne9\), the first step makes the paired bands equal. THEOREM 2a preserves equality through step \(m\), contradicting 那个 target. If \(a+b=9\), the bands after the first step contain only \(0,9\). A distinct return therefore requires \(\{a,b\}=\{0,9\}\). Since \(b\ne0\), the only remaining possibility 是 \(a=0,b=9\).

Every positive decimal reverse-add output ending in \(0\) begins in \(1\). To verify 这个 endpoint fact, its units output satisfies \(e_0=q_0\bmod10=0\). Canonical positivity gives \(1\le q_0\le18\), hence \(q_0=10\). Symmetry gives \(q_{L-1}=10\). At the highest column, incoming carry \(0\) yields \((e_{L-1},c_L)=(0,1)\); incoming carry \(1\) yields \((1,1)\). Either case appends leading digit \(1\). 可是 \(S_{n+g}(0,9)\) begins in \(9\) 和 ends in \(0\). 这 excludes the last possibility 和 proves (4). \(\square\)

**THEOREM 3a — unequal constant-digit codeblocks.** The same conclusion holds asymptotically for substitutions

\[
0\mapsto a^r,\qquad 1\mapsto b^s,
\qquad r,s\ge1,quad a\ne b,quad b\ne0.
\]

For a fixed return time \(m\), it suffices that

\[
rn\ge r+s+2m+1,\qquad sn\ge2m+1.
\]

The initial paired interval becomes

\[
\left[r+s,\ \min(rn-1,r+s+sn-1)\right].
\]

The displayed bounds keep it nonempty after \(m\) contractions. It remains inside the designated target bands when the parameter increases by any \(g\ge0\). The paired-band cases 和 endpoint calculation from THEOREM 3 apply without changing any digit or carry. 这 includes unequal codeblock widths, 可是 requires each codeblock to be a constant-digit run. \(\square\)

## 4. Binary reference mechanism, with every carry

**THEOREM 4 — exact binary four-phase identities.** For \(n\ge2\), define

\[
\begin{aligned}
X_n&=10\,1^n\,01\,0^n,\\
Y_n&=11\,0^{n-2}\,1000\,1^{n-2}\,01,\\
Z_n&=10\,1^n\,01\,0^{n+1},\\
W_n&=11\,0^n\,10\,1^{n-1}\,01.
\end{aligned}
\]

As binary integers,

\[
X_n\xrightarrow{T_2}Y_n\xrightarrow{T_2}Z_n
\xrightarrow{T_2}W_n\xrightarrow{T_2}X_{n+1}.
\tag{5}
\]

**Proof.** A tuple \((q,c,c',e)\) records column sum, incoming carry, outgoing carry, 和 output digit. The lists below run from units to highest original column. A superscript means repetition; exponent zero gives an empty list. Every listed tuple satisfies \(q+c=e+2c'\). Each list starts with incoming carry zero, 和 consecutive carry values agree.

For \(X_n\), terminal carry \(0\):

\[
\begin{aligned}
&(1,0,0,1),(0,0,0,0),(1,0,0,1)^{n-2},\\
&(2,0,1,0),(1,1,1,0)^2,(2,1,1,1),\\
&(1,1,1,0)^{n-2},(0,1,0,1),(1,0,0,1).
\end{aligned}
\]

For \(Y_n\), terminal carry \(1\):

\[
\begin{aligned}
&(2,0,1,0),(1,1,1,0)^n,(0,1,0,1),(0,0,0,0),\\
&(1,0,0,1)^n,(2,0,1,0).
\end{aligned}
\]

For \(Z_n\), terminal carry \(0\):

\[
\begin{aligned}
&(1,0,0,1),(0,0,0,0),(1,0,0,1)^{n-1},\\
&(2,0,1,0),(0,1,0,1),(2,0,1,0),\\
&(1,1,1,0)^{n-1},(0,1,0,1),(1,0,0,1).
\end{aligned}
\]

For \(W_n\), terminal carry \(1\):

\[
\begin{aligned}
&(2,0,1,0),(1,1,1,0)^n,(0,1,0,1),(2,0,1,0),\\
&(0,1,0,1),(1,0,0,1)^n,(2,0,1,0).
\end{aligned}
\]

Pairing each displayed word with its reversal gives the listed column sums. The lists contain respectively \(2n+4,2n+4,2n+5,2n+5\) columns, exactly the input widths. Reading the output digits from the highest end, 和 appending a final carry precisely in the \(Y_n,W_n\) rows, gives the four successors in (5). Thus every differing carry case appears explicitly.

The words \(X_n,Z_n\) begin with \(1\) 和 end with \(0\). The words \(Y_n,W_n\) begin with \(11\) 和 end with \(01\), so their second digits from opposite ends differ. Every phase therefore avoids palindromes. Induction using (5) supplies an expanding binary orbit, used here as the control mechanism. \(\square\)

## 5. Arbitrary uniform blocks: a finite obstruction

**THEOREM 5 — four arrows exclude every block width.** Let \(A,B\) be decimal words of the same length \(k\ge1\), with at least one nonzero digit between them. Let \(E\) replace each binary \(0\) by \(A\), each binary \(1\) by \(B\), then interpret the result as an ordinary integer. Leading zeros may be removed. At least one of the following four equalities fails:

\[
\begin{aligned}
T_{10}(E(X_5))&=E(Y_5),\\
T_{10}(E(Y_5))&=E(Z_5),\\
T_{10}(E(Z_5))&=E(W_5),\\
T_{10}(E(W_5))&=E(X_6).
\end{aligned}
\tag{6}
\]

An injectivity assumption on \(E\) is unnecessary. The excluded block pair \(A=B=0^k\) would encode every word as zero.

### Proof: finite telescope 和 reversed block values

Put \(D=10^k\), \(r=2k+1\), 和 \(M=10^r=10D^2\). The final \(5k\) digits of \(E(X_5)\) 和 \(E(X_6)\) agree: the matching digits come from \(A^5\) at the right end. Since \(r\le5k\), the endpoints agree modulo \(M\). Assuming the four arrows (6), summing (2) gives

\[
H_r(E(X_5))+H_r(E(Y_5))+H_r(E(Z_5))+H_r(E(W_5))
\equiv0\pmod M.
\tag{7}
\]

For a block \(C=c_0\cdots c_{k-1}\) written left to right, define

\[
v(C)=\sum_{i=0}^{k-1}c_i10^i.
\]

The definition deliberately reads its digits as low-first values. Set \(a=v(A)\), \(b=v(B)\); hence \(0\le a,b<D\).

**THEOREM 5a — periodic-ray arithmetic used in (7).** The rational value of a leading digit ray \(P R R R\cdots\), with nonempty period \(R\), equals

\[
v(P)+\frac{10^{|P|}v(R)}{1-10^{|R|}}.
\tag{8}
\]

Its denominator is coprime to \(10\). Reduction modulo \(10^r\), using the denominator's modular inverse, equals the low-first value of its first \(r\) digits. To verify 这, take enough full periods to cover the \(r\) digits, sum the finite geometric series, 和 observe that the omitted tail is divisible by \(10^r\). 这是 finite modular arithmetic; a continuity assumption about reversal is unnecessary.

### Case 1: \(b>0\)

Let \(z\) be the number of leading zero digits in \(B\). Then \(0\le z<k\) 和 \(10^z\mid b\). Every encoded phase starts with \(B\), so canonicalization removes exactly \(z\) leading zeros in each phase.

Before removal, the stabilized leading rays are \(BAB^\infty\) for \(X,Z\), 和 \(BBA^\infty\) for \(Y,W\). Their values 是

\[
p=b+Da-\frac{D^2b}{D-1},\qquad
q=(1+D)b-\frac{D^2a}{D-1}.
\]

Consequently

\[
p+q=\frac{(D-2)b-Da}{D-1}.
\tag{9}
\]

Removing \(z\) initial zeros divides the low-first values by \(10^z\). 这个 division is exact in their integer numerators. The finite words \(X_5,Z_5\) match the relevant rays through \(7k-z\) digits after trimming; \(Y_5\) matches through \(5k-z\); \(W_5\) through \(7k-z\). Each bound is at least \(r=2k+1\). Therefore the left side of (7) equals, modulo \(M\), the rational number

\[
C=\frac{N}{D-1},\qquad
N=\frac{2((D-2)b-Da)}{10^z}\in\mathbb Z.
\tag{10}
\]

The numerator bound is explicit:

\[
|N|<2D^2<M.
\]

Since \(D-1\) is invertible modulo \(M\), equation (7) implies \(M\mid N\), hence \(N=0\). Thus

\[
Da=(D-2)b.
\]

Since \(\gcd(D,D-2)=2\) 和 \(0<b<D\), the only solution 是

\[
b=D/2,\qquad a=D/2-1.
\]

Restoring the original left-to-right block orientation gives

\[
A=9^{k-1}4,\qquad B=0^{k-1}5.
\tag{11}
\]

The canonical number \(E(X_5)\) consequently begins in \(5\) 和 ends in \(4\). At its units column, \(q_0=9,c_0=0\), giving \(e_0=9,c_1=0\). 可是 \(E(Y_5)\) ends in \(B\), hence in digit \(5\). The first equality in (6) fails, contradicting the assumption.

### Case 2: \(b=0<a\)

Here \(B=0^k\). Let \(z\) count the leading zeros of \(A\), 和 put \(a_*=a/10^z>0\). The \(X,Z\) encodings start with \(BA\), lose \(k+z\) zeros, 和 follow leading ray \(A0^\infty\) after 这个 common adjustment. Its value equals \(a_*\).

The \(Y,W\) encodings start with \(BBA\), lose \(2k+z\) zeros, 和 follow periodic leading ray \(A^\infty\). Its value equals \(-a_* /(D-1)\). The shortest required matching prefix occurs in \(Y_5\): its first three copies of \(A\) give

\[
3k-z\ge2k+1=r.
\]

The other phases give longer matching prefixes. Equation (7) therefore forces

\[
C=\frac{2a_*(D-2)}{D-1}\equiv0\pmod M.
\]

可是 the integer numerator satisfies

\[
0<2a_*(D-2)<2D^2<M,
\]

so the congruence is impossible. Cases 1 和 2 exhaust the nonzero block pairs. 这 completes the proof of THEOREM 5. \(\square\)

**Scope of THEOREM 5.** The four specified intermediate words matter. A bare endpoint identity \(T_{10}^4(E(X_5))=E(X_6)\) with different intermediate words is outside its conclusion. Phase-dependent codes, inserted separator blocks, 和 multiple decimal steps per encoded binary step are 也 outside its conclusion. THEOREM 3 supplies the stronger arbitrary-time result only for its constant-digit class.

## 6. General charge condition 和 exact stopping point

**THEOREM 6 — necessary rational endpoint charge condition.** Consider a family of actual decimal orbit segments of fixed positive length \(m\). Assume that, for each precision \(r\), the first \(r\) high digits at each phase stabilize across sufficiently long family members, 和 the first \(r\) low digits agree at their input 和 returned endpoint. If the phase-high rays are ultimately periodic,

\[
h_t=P_tR_t^\infty\qquad(0\le t<m),
\]

then

\[
\boxed{\sum_{t=0}^{m-1}
\left(v(P_t)+\frac{10^{|P_t|}v(R_t)}{1-10^{|R_t|}}\right)=0.}
\tag{12}
\]

**Proof.** Sum (2) along each finite orbit segment. Endpoint agreement forces the sum of high-prefix values to vanish modulo \(10^r\). Formula (8) expresses the values as rational numbers with denominator coprime to \(10\). A common denominator leaves an integer numerator divisible by every \(10^r\), so the numerator equals zero. 这 proves (12). \(\square\)

**THEOREM 6a — finite detection.** If the sum in (12), reduced to lowest terms, equals \(u/v\ne0\), then its first nonzero decimal-adic residue occurs at

\[
r=1+\min\{v_2(|u|),v_5(|u|)\}.
\]

The denominator is coprime to \(10\), 和 \(10^j\mid u\) exactly when \(j\le\min(v_2(|u|),v_5(|u|))\). Any candidate with the required prefix stabilization through 这个 detecting precision fails. THEOREM 5 adds a uniform numerator bound that makes the fixed parameter \(n=5\) sufficient for every block width.

**IDEA — where the approach stops.** Equation (12) is only necessary. The charge-zero blocks (11) illustrate the gap: they pass the rational cancellation test yet fail the first actual addition. A new construction must satisfy every interface carry 和 the center matching, in addition to charge cancellation. Correcting the endpoints of a \(0/9\) bulk template could evade THEOREM 3's final endpoint contradiction; nonconstant blocks or different intermediate phases could evade THEOREM 5. The observations supply directions for a new certificate.

**IDEA — sharpest open question.** Does there exist a finite family of decimal words built from fixed interface blocks 和 growing periodic runs, with different intermediate phases permitted, such that some fixed \(m\)-step return increases the run-length vector, the high-ray charges sum to zero, 和 every actual phase fails the palindrome test? Within the binary-embedding approach, the first unresolved class uses bounded endpoint/interface corrections or nonconstant codeblocks with a changed time scale. A positive answer requires one explicit finite seed 和 a complete carry-checked return identity; charge balance alone supplies neither.

## 7. Numerical controls: code 和 exact output

**THEOREM 4 control.** The following run executes 1,000 consecutive binary transitions beginning at \(X_2\). It checks every phase word 和 every displayed carry tuple, including the boundary case \(n=2\). The final word 是 \(X_{252}\), of width \(508\); none of the 1,001 observed states is palindromic. The complete proof remains THEOREM 4.

**IDEA (rejected constructions).** The decimal runs test literal reinterpretation, the \(0/9\) substitution, 和 the forced charge-zero blocks of widths \(1,2,3\). Each run continues for 1,000 transitions even after its first palindrome. The \(0/9\) image of \(X_2\) reaches a palindrome at step \(8\), killing that proposed construction. The width-2 和 width-3 charge-zero images remain palindrome-free in this finite run, 可是 their prescribed binary phase transitions already fail; infinite avoidance 和 a return certificate remain unestablished.

The code uses Python 3 和 its standard library. The six prefix checks test the exact rational formulas, including a zero \(B\) block. The samples directly test the stated formulas.

```python
"""Targeted controls for REPORT_209.md; Python 3, standard library only."""
from fractions import Fraction


def shapes(n):
    assert n >= 2
    return (
        "10" + "1" * n + "01" + "0" * n,
        "11" + "0" * (n - 2) + "1000" + "1" * (n - 2) + "01",
        "10" + "1" * n + "01" + "0" * (n + 1),
        "11" + "0" * n + "10" + "1" * (n - 1) + "01",
    )


def step(word, base):
    assert word and word[0] != "0"
    carry = 0
    out, trace = [], []
    for low, high in zip(word[::-1], word):
        q = int(low) + int(high)
        value = q + carry
        trace.append((q, carry, value // base, value % base))
        out.append(str(value % base))
        carry = value // base
    if carry:
        out.append(str(carry))
    return "".join(out[::-1]), trace


def expected_trace(n, phase):
    p = (1, 0, 0, 1)
    z = (0, 0, 0, 0)
    g = (2, 0, 1, 0)
    h = (1, 1, 1, 0)
    u = (2, 1, 1, 1)
    f = (0, 1, 0, 1)
    return (
        [p, z] + [p] * (n - 2) + [g] + [h] * 2
        + [u] + [h] * (n - 2) + [f, p],
        [g] + [h] * n + [f, z] + [p] * n + [g],
        [p, z] + [p] * (n - 1) + [g, f, g]
        + [h] * (n - 1) + [f, p],
        [g] + [h] * n + [f, g, f] + [p] * n + [g],
    )[phase]


def encode(word, zero_block, one_block):
    raw = "".join(zero_block if digit == "0" else one_block for digit in word)
    return raw.lstrip("0") or "0"


def low_value(word):
    return sum(int(digit) * 10 ** index for index, digit in enumerate(word))


def rational_mod(value, modulus):
    return value.numerator * pow(value.denominator, -1, modulus) % modulus


def charge_prefix_check(zero_block, one_block):
    k = len(zero_block)
    assert k == len(one_block)
    D, r = 10 ** k, 2 * k + 1
    modulus = 10 ** r
    a, b = low_value(zero_block), low_value(one_block)
    assert a or b
    encoded = [encode(w, zero_block, one_block) for w in shapes(5)]
    if b:
        z = len(one_block) - len(one_block.lstrip("0"))
        P = Fraction(b + D * a) - Fraction(D * D * b, D - 1)
        Q = Fraction((D + 1) * b) - Fraction(D * D * a, D - 1)
        rays = [P / 10 ** z, Q / 10 ** z] * 2
    else:
        z = len(zero_block) - len(zero_block.lstrip("0"))
        a_star = a // 10 ** z
        rays = [Fraction(a_star), Fraction(-a_star, D - 1)] * 2
    for word, ray in zip(encoded, rays):
        assert low_value(word[:r]) == rational_mod(ray, modulus)
    x6 = encode(shapes(6)[0], zero_block, one_block)
    assert encoded[0][-r:] == x6[-r:]
    M = sum(rays) * (D - 1)
    assert M.denominator == 1 and abs(M) < 2 * D * D < modulus
    if M == 0:
        assert zero_block == "9" * (k - 1) + "4"
        assert one_block == "0" * (k - 1) + "5"
        assert step(encoded[0], 10)[0][-1] == "9"
        assert encoded[1][-1] == "5"
    return M.numerator


word = shapes(2)[0]
palindromes = 0
for t in range(1001):
    n, phase = 2 + t // 4, t % 4
    assert word == shapes(n)[phase]
    palindromes += word == word[::-1]
    if t < 1000:
        word, trace = step(word, 2)
        assert trace == expected_trace(n, phase)
print("binary steps=1000; phases=PASS; carries=PASS; "
      f"palindromes={palindromes}; final=X_252; digits={len(word)}")

samples = (("0", "1"), ("0", "9"), ("4", "5"),
           ("94", "05"), ("994", "005"), ("12", "00"))
for A, B in samples:
    numerator = charge_prefix_check(A, B)
    image = [encode(w, A, B) for w in shapes(5)]
    target = image[1:] + [encode(shapes(6)[0], A, B)]
    failures = [i for i, (source, wanted) in enumerate(zip(image, target))
                if step(source, 10)[0] != wanted]
    print(f"charge A={A} B={B}; numerator={numerator}; "
          f"prefix=PASS; failed_arrows={failures}")

seeds = (
    ("literal_seed", "10110"),
    ("zero_nine_seed", "90990"),
    ("zero_nine_X2", encode(shapes(2)[0], "0", "9")),
    ("forced_k1_X2", encode(shapes(2)[0], "4", "5")),
    ("forced_k2_X2", encode(shapes(2)[0], "94", "05")),
    ("forced_k3_X2", encode(shapes(2)[0], "994", "005")),
)
for name, initial in seeds:
    word, first_hit, first_value = initial, None, None
    for t in range(1001):
        if first_hit is None and word == word[::-1]:
            first_hit, first_value = t, word
        if t < 1000:
            word, _ = step(word, 10)
    print(f"decimal {name}; seed={initial}; steps=1000; "
          f"first_palindrome={first_hit}; value={first_value}; digits={len(word)}")

print("Targeted controls complete; finite observations do not assert infinite avoidance.")
```

Actual output:

```text
binary steps=1000; phases=PASS; carries=PASS; palindromes=0; final=X_252; digits=508
charge A=0 B=1; numerator=16; prefix=PASS; failed_arrows=[0, 1, 2, 3]
charge A=0 B=9; numerator=144; prefix=PASS; failed_arrows=[0, 1, 2, 3]
charge A=4 B=5; numerator=0; prefix=PASS; failed_arrows=[0, 1, 2, 3]
charge A=94 B=05; numerator=0; prefix=PASS; failed_arrows=[0, 1, 2, 3]
charge A=994 B=005; numerator=0; prefix=PASS; failed_arrows=[0, 1, 2, 3]
charge A=12 B=00; numerator=4116; prefix=PASS; failed_arrows=[0, 1, 2, 3]
decimal literal_seed; seed=10110; steps=1000; first_palindrome=1; value=11211; digits=416
decimal zero_nine_seed; seed=90990; steps=1000; first_palindrome=12; value=4964444694; digits=419
decimal zero_nine_X2; seed=90990900; steps=1000; first_palindrome=8; value=88793239788; digits=428
decimal forced_k1_X2; seed=54554544; steps=1000; first_palindrome=24; value=1368598378738958631; digits=431
decimal forced_k2_X2; seed=594050594059494; steps=1000; first_palindrome=None; value=None; digits=444
decimal forced_k3_X2; seed=5994005005994005994994; steps=1000; first_palindrome=None; value=None; digits=439
Targeted controls complete; finite observations do not assert infinite avoidance.
```

## 8. Verification boundary

**THEOREM status.** The proofs above include carry propagation, terminal overflow, shifted reflection, leading-zero canonicalization, 和 each nonzero block case. The independent mathematical audits checked the interval bounds 和 the finite \(n=5\) argument. Formalization of the new statements remains outstanding.

**IDEA status.** Decimal Lychrel existence remains unresolved by 这个 report. The exclusions concern precisely the embedding classes stated in THEOREMS 3 和 5. General decimal templates, periodic bands, 和 satisfiability of the existing return checker remain outside the conclusions.

Repository validation: `python3 tools/verify.py --changed c6902ac6c366ce018e68a810f58b400dda07145a` returned `ALL CHECKS PASSED`. The run scanned 4,823 Lean files 和 287 registered projects; changed Lean modules: `0`, audited endpoints: `0`. Thus 这个 gate checks repository consistency for the report-only change. The new mathematical statements retain written-proof status.
