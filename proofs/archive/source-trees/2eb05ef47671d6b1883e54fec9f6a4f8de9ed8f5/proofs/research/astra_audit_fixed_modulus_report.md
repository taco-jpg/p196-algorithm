# Independent proof audit: exact-length palindrome residues

Date: 2026-10-13. Task 7 of the requested Astra research team.

**Verdict.** The exact-length residue theorem in
`astra_modular_fixed_modulus_theorem.md` is correct with its stated bound,
including every modulus and every length above the bound. Its corollary
excluding a nonempty, forward-invariant, palindrome-free set whose membership
depends only on exact decimal length and a fixed residue is also correct.
These are genuine elementary theorems; finite controls are not needed to
justify their universal quantifiers. They do not prove existence or
nonexistence of a finite decimal Lychrel number.

No substantive proof gap was found. Two presentation refinements are worth
making: explicitly formulate the saturation meaning of “membership depends
only on,” and limit the extension to truncated valuations to a **fixed finite
list of primes and fixed finite caps**. The latter qualification is needed
to reduce those data to a single fixed modulus.

## Scope and quantifiers

Let \(M\) be any positive integer and write uniquely
\[
M=u q,\qquad u=2^\alpha5^\beta,\qquad \gcd(q,10)=1.
\]
Let \(k=\max(1,\alpha,\beta)\). For \(q>1\), let
\(r=\operatorname{ord}_q(10)\); for \(q=1\), set \(r=1\). Let
\(B=2k+4qr\). The theorem is quantified over **every integer residue
representative** \(a\) and **every integer length** \(L\ge B\), not just
a length subsequence. It asserts that there exists an ordinary positive
\(L\)-digit palindrome \(P\equiv a\pmod M\) exactly when
\[
\neg(10\mid M\text{ and }10\mid a),
\qquad
L\text{ even}\Longrightarrow\gcd(M,11)\mid a.
\]
Both conditions are invariant under changing the representative \(a\).
The first uses \(10\mid a\) only when \(10\mid M\); the second uses a
divisor of \(M\).

For the corollary, “membership depends only on” must mean
\[
\ell(x)=\ell(y),\quad x\equiv y\pmod M
\quad\Longrightarrow\quad (x\in S\iff y\in S)
\]
for all positive integers \(x,y\). No computability, regularity, periodicity,
or uniformity in the length-dependent allowed residue sets is assumed.

## Adversarial checks

### The fixed suffix exists

The assertion \(u\mid10^k\) holds because \(\alpha,\beta\le k\). Start
with \(A_0\in\{0,\ldots,u-1\}\) congruent to \(a\) modulo \(u\).
If \(10\nmid A_0\), use \(A=A_0\). Otherwise use \(A=A_0+u\).

If \(10\mid u\), then \(10\mid M\), so compatibility ensures
\(10\nmid a\) and hence \(10\nmid A_0\). Thus addition is only required
when \(10\nmid u\). In that case \(u\) is \(1\), a power of \(2\), or
a power of \(5\), so \(10\nmid u\) and \(2u\le10^k\). Consequently
\[
0<A_0+u<2u\le10^k,\qquad 10\nmid(A_0+u).
\]
This also handles \(u=1\), when the procedure chooses \(A=1\).
The suffix therefore has a nonzero units digit, even if its zero-padded
\(k\)-digit representation has leading zeros.

Reflecting that suffix into the high \(k\) places gives a nonzero leading
digit. There is no overlap because \(L\ge B>2k\). All other nonzero
contributions are above position \(k-1\), so the resulting palindrome
\(C\) satisfies \(C\equiv A\equiv a\pmod u\).

### All interior pairs are distinct and free

The proposed low-side intervals are
\[
I_0=[k,k+qr-1],\qquad I_1=[k+qr,k+2qr-1].
\]
Their largest index satisfies
\[
k+2qr-1\le\left\lfloor\frac{L-2}{2}\right\rfloor.
\]
Thus every chosen index lies strictly below the middle, and its reflection
lies strictly above it. Distinct low-side indices give disjoint pairs. The
lower bound \(i\ge k\) also places both entries outside the fixed outer
blocks. The middle digit at odd length can simply remain zero.

Every interval of \(qr\) consecutive integers contains exactly \(q\)
representatives of each class modulo \(r\). In \(I_0\) select the indices
congruent to \(0\); in \(I_1\) select those congruent to \(1\). These
are two disjoint pools of \(q\) pairs each. When \(r=1\), the residue
labels coincide, but the pools remain disjoint. No assumption that those
two residue classes are distinct is being made.

### The common divisor is exactly the stated one

Use the unreduced integers
\[
c_0=1+10^{L-1},\qquad c_1=10+10^{L-2}.
\]
The low/high pair weight is \(10^i+10^{L-1-i}\). Periodicity of powers of
\(10\) modulo \(q\) makes its residue \(c_0\) or \(c_1\) on the
respective pool. All exponents are nonnegative because \(L\ge B\ge6\).

The identity
\[
10c_1-c_0=99
\]
implies that \(d=\gcd(q,c_0,c_1)\) divides \(99=9\cdot11\).
But \(c_0\equiv2\pmod3\), so \(3\nmid d\), and hence \(d\mid11\).
For even \(L\), both \(c_0\) and \(c_1\) are divisible by \(11\).
For odd \(L\), \(c_0\equiv2\pmod{11}\). Therefore
\[
d=\begin{cases}\gcd(q,11),&L\text{ even},\\1,&L\text{ odd}.\end{cases}
\]
This proves the exact gcd, not merely one direction of divisibility.
It excludes any extra \(11\)-adic obstruction: even if \(11^h\mid q\),
the gcd of the two weights with \(q\) has at most one factor of \(11\).

For \(r=1\), \(q\mid9\), so \(q\in\{1,3,9\}\). Both weights are
\(2\pmod q\), which generates every residue because \(q\) is odd.
The equality above therefore remains correct in this degenerate case.

### Coefficient realizability does not exceed digit capacity

The subgroup generated by \(c_0,c_1\) modulo \(q\) consists of the
multiples of \(d\). This follows directly from Bézout's identity applied
to \(q,c_0,c_1\). The target \(a-C\) is a multiple of \(d\): there is
nothing to show if \(d=1\), and if \(d=11\), compatibility gives
\(11\mid a\) while the even-length palindrome \(C\) gives \(11\mid C\).
Here \(\gcd(M,11)=\gcd(q,11)\), since \(\gcd(u,11)=1\).

An integer coefficient solution can be reduced independently modulo \(q\),
giving \(0\le x,y<q\) with
\(xc_0+yc_1\equiv a-C\pmod q\). Turning on exactly \(x\) pairs in the
first pool and \(y\) pairs in the second implements these coefficients
using only digits \(0,1\). Each pool has \(q\) places, so capacity is
sufficient; no carries arise because all positions are distinct. Every
modified position is at least \(k\), preserving the congruence modulo
\(u\). The two congruences combine because \(\gcd(u,q)=1\).

When \(q=1\), no interior adjustment is necessary. Taking \(x=y=0\)
avoids relying on any multiplicative order or modular inverse modulo one.

### Width growth supplies the needed orbit state

For an ordinary positive \(L\)-digit integer \(n\), its reversal is a
positive integer below \(10^L\), even when \(n\) ends in zero. Hence
\[
n<T(n)=n+\operatorname{rev}_{10}(n)<2\cdot10^L<10^{L+1}.
\]
The iterates form a strictly increasing integer sequence, hence are
unbounded. Their lengths are nondecreasing, unbounded, and increase by at
most one at each step. In particular they visit every sufficiently large
integer length, and therefore an even length. No implicit growth-rate
assumption is needed.

Writing \(n=\sum_{i=0}^{L-1}d_i10^i\), trailing zero digits do not prevent
the integer identity
\(\operatorname{rev}_{10}(n)=\sum_{i=0}^{L-1}d_i10^{L-1-i}\).
Reduction modulo \(11\) gives
\[
\operatorname{rev}_{10}(n)\equiv(-1)^{L-1}n\pmod{11}.
\]
Thus an even-length input yields a multiple of \(11\); after that, all
future iterates remain divisible by \(11\), regardless of parity.

If \(10\mid n\), the units digit of \(T(n)\) is the nonzero leading
digit of \(n\). Therefore \(10\nmid T(n)\). Once the orbit has acquired
divisibility by \(11\) and length at least \(B\), take its current member
if it is not divisible by \(10\), and otherwise take the next member.
This supplies all three needed properties simultaneously. There is no
unstated requirement to find an odd length with a particular units digit.

## Concise self-contained proof

An ordinary positive palindrome cannot end in zero, and an even-length
palindrome is divisible by \(11\). This proves necessity of the two
conditions.

For sufficiency, choose \(0<A<10^k\), \(10\nmid A\), and
\(A\equiv a\pmod u\) by the suffix procedure proved above. Put the
zero-padded \(k\)-digit block for \(A\) at the low end and its reflection
at the high end, filling every remaining place with zero. The result
\(C\) is a positive \(L\)-digit palindrome and \(C\equiv a\pmod u\).

The bound \(L\ge2k+4qr\) supplies the two disjoint interior pools just
described, each containing \(q\) mirrored pairs. Their weights modulo
\(q\) are respectively \(c_0=1+10^{L-1}\) and
\(c_1=10+10^{L-2}\). Since \(10c_1-c_0=99\),
\(c_0\equiv2\pmod3\), and \(10\equiv-1\pmod{11}\),
\[
\gcd(q,c_0,c_1)=
\begin{cases}\gcd(q,11),&L\text{ even},\\1,&L\text{ odd}.\end{cases}
\]
The compatibility assumptions imply that this gcd divides \(a-C\).
Bézout's identity therefore supplies \(0\le x,y<q\) such that
\(xc_0+yc_1\equiv a-C\pmod q\). Put digit \(1\) in \(x\) mirrored
pairs of the first pool and \(y\) of the second. The resulting palindrome
\(P\) has exact length \(L\), satisfies \(P\equiv a\pmod q\), and
still satisfies \(P\equiv a\pmod u\). Therefore
\(P\equiv a\pmod M\). If \(q=1\), use \(P=C\).

Now suppose a nonempty set \(S\) has membership determined by exact length
and residue modulo a fixed \(M\), is closed under \(T\), and contains no
positive palindrome. Start an orbit at any member of \(S\). The growth and
modulo-\(11\) arguments above give an iterate \(n\in S\) with
\(\ell(n)\ge B\), \(11\mid n\), and \(10\nmid n\). Its length and
residue satisfy the theorem's compatibility conditions. A palindrome
\(P\) therefore has the same exact length and residue as \(n\).
The membership hypothesis forces \(P\in S\), a contradiction. This proves
the corollary.

## Companion code and finite evidence

I inspected `astra_modular_palindrome_builder.py` and its recorded results.
The implementation matches the proof. In particular:

- `residue % u` chooses the required nonnegative suffix representative.
- The `q == 1` return occurs before modular inverse calculations.
- The second pool uses `1 % r`, so order one is handled correctly.
- The linear congruence solver handles `c1 == 0 (mod q)` by allowing
  `reduced_q == 1` and setting the second coefficient to zero.
- Streaming evaluation and direct digit checks verify ordinary finite
  palindromes, with no huge-integer conversion or infinite-word semantics.
- The code reduces its weights modulo `q`; the exact integer identity in
  the written proof uses their unreduced representatives. This difference
  is harmless because the gcd with `q` and all congruences are unchanged.

The recorded results report 2,370 compatible constructions, 90 incompatible
rejections, and 142 selected constructions, including \(q=1\), \(r=1\),
and powers of \(11\) through \(1331\). I also inspected the root's
separate residue-support results for moduli \(1\) through \(300\) and
lengths through \(80\). These are consistency checks; the proof above
establishes the infinite range. I did not rerun or modify the canonical
builder, controls, or Lean files.

## Extension and boundary audit

1. A finite collection of fixed congruence tests reduces to the least common
   multiple of its moduli, so the corollary covers arbitrary combinations
   of those tests with exact length.
2. A fixed finite list of truncated valuations
   \(\min(v_p(n),e_p)\), with each \(e_p\) fixed and finite, is determined
   by a single fixed modulus \(\prod_p p^{e_p}\). The qualifier “finite
   list” matters: all prime valuations at once determine the integer.
3. Length modulo a fixed period is weaker information than exact length.
   Length-dependent allowed residues may already be completely arbitrary.
4. The proof still works if residue saturation is assumed only above a fixed
   length threshold, provided the nonempty forward orbit reaches that
   region. It also works for a closed set confined to sufficiently large
   lengths.
5. For a length-dependent modulus \(M(L)\), the written necessary
   inequality is correct at every sufficiently late orbit state not
   divisible by \(10\). It does not prove that a modulus growing faster
   than the displayed bound can supply an invariant.
6. The theorem concerns saturation of **whole length-and-residue classes**.
   Sharing a class with a palindrome does not mean that the actual orbit
   visits that palindrome. The theorem cannot rule out a Lychrel orbit
   itself, whose membership need not be saturated in those classes.
7. No claim of publication novelty follows. The bound is sufficient and
   deliberately nonoptimal; it is not a lower bound on the length at which
   residue saturation begins.

The note's separate 10-adic counterexample is also valid. For fixed positive
\(n\) of length \(\ell\), \(j\ge\ell\), and \(1\le c\le9\),
\[
\operatorname{rev}_{10}(n+c10^j)
=c+10^{j-\ell+1}\operatorname{rev}_{10}(n).
\]
Thus the inputs converge 10-adically to \(n\), while their reverse-and-add
images converge to \(n+c\). Choose \(c\) different from the leading digit
of \(n\), which is \(\operatorname{rev}_{10}(n)\bmod10\); then the latter
limit differs from \(T(n)\). Ordinary reverse-and-add therefore has no
continuous extension to all 10-adic integers agreeing at every positive
finite integer. This is not an obstruction to every possible enlarged
digit-state space.

## Primary-source check and novelty wording

I independently reopened the original Harminc–Soták publisher PDF:

- M. Harminc and R. Soták, *Palindromic Numbers in Arithmetic Progressions*,
  Fibonacci Quarterly 36(3) (1998), 259–262.
  <https://www.fq.math.ca/Scanned/36-3/harminc.pdf>

Its Theorem B confirms that a nonconstant positive decimal arithmetic
progression has infinitely many palindromes exactly when its initial term
and difference are not both divisible by \(10\). Thus the attribution in
the theorem note is accurate. This prior result already yields the no-trap
corollary for membership depending only on a fixed residue, using the fact
that a forward orbit cannot remain entirely divisible by \(10\).

I also reopened the primary Banks–Hart–Sakata preprint:

- W. D. Banks, D. N. Hart, and M. Sakata, *Almost All Palindromes Are
  Composite*, Proposition 4.2.
  <https://arxiv.org/pdf/math/0405056>

For \(\gcd(q,990)=1\), its exact-length discrepancy estimate is strictly
smaller than the expected positive count once
\(L\ge10+2q^2\log q\). Hence every residue occurs at each such length.
This confirms that substantial exact-length saturation cases are prior art.
The full all-moduli support statement audited here is a valid independent
derivation; neither this audit nor a bounded literature search establishes
that it is new.

Fresh web retrieval references for the parent, which should reopen a source
before citing it in a root response: `turn105view0` (Harminc–Soták),
`turn105view1` and `turn106view0` (Banks–Hart–Sakata, including Proposition
4.2). No external source is required for the elementary proof above.

## Research status

There is a complete proof of an obstruction to one broad certificate
class. There is no finite decimal Lychrel witness, no proof that every
orbit hits a palindrome, and no Lean formalization of this new arithmetic
theorem supplied by this audit. No explicit proposed construction requiring
an additional audit was received before this report was completed.

## Addendum: classification of residue-determined reversal

The subsequently added Section 6 of the theorem note is also correct:
for a fixed positive \(M\), the residue
\(\operatorname{rev}_{10}(n)\bmod M\) is a function of
\((\ell(n),n\bmod M)\) for all positive \(n\) if and only if
\(M\mid99\). The same necessity holds when the function is required only
at every sufficiently large length. The residue of \(T(n)\) has the same
classification because the input residue is already known.

Here is a self-contained proof, including the long-length quantifier.

If \(M\mid99\), then \(10^2\equiv1\pmod M\). For an \(L\)-digit
expansion \(n=\sum d_i10^i\), termwise comparison gives
\[
\operatorname{rev}_{10}(n)
 =\sum_i d_i10^{L-1-i}
 \equiv10^{L-1}\sum_i d_i10^i
 =10^{L-1}n\pmod M.
\]
Thus the reverse residue is determined. The residue of \(T(n)\) is
\(2n\) at odd input length and \(11n\) at even input length.

Conversely, suppose that reversal residues are determined in this way at
every length above some threshold. If a prime \(p\in\{2,5\}\) divides
\(M\), choose an admissible length \(L\) with \(10^{L-1}\ge M\).
Each interval
\[
[10^{L-1},2\cdot10^{L-1}-1],\qquad
[2\cdot10^{L-1},3\cdot10^{L-1}-1]
\]
contains a representative of any selected class modulo \(M\), because
each contains at least \(M\) consecutive integers. Choose \(x,y\) in
these two intervals with \(x\equiv y\pmod M\). They have equal length,
but their leading digits are respectively \(1,2\), so their reversals
are respectively \(1,2\pmod p\). This contradicts the asserted
determinacy. Therefore \(\gcd(M,10)=1\).

Now choose an admissible \(L\ge3\) so large that all four numbers
\[
n=10^{L-1}+9,\quad n+1,\quad n+M,\quad n+M+1
\]
have length \(L\). This is possible with arbitrarily large \(L\) since
\(M\) is fixed. The number \(n\) ends in exactly one \(9\); incrementing
it changes the units digit from \(9\) to \(0\) and the tens digit from
\(0\) to \(1\). Thus
\[
\operatorname{rev}_{10}(n+1)-\operatorname{rev}_{10}(n)
=10^{L-2}-9\cdot10^{L-1}.
\]
Since \(10\nmid M\), the number \(n+M\) does not end in \(9\).
Its increment changes only the units digit, so
\[
\operatorname{rev}_{10}(n+M+1)-\operatorname{rev}_{10}(n+M)
=10^{L-1}.
\]
These formulas are identities of ordinary integers even when the reversed
word begins in zero; zero leading digits simply contribute zero.
The input pairs \(n,n+M\) and \(n+1,n+M+1\) respectively have equal
residues and equal lengths. Determinacy therefore makes the displayed
increments equal modulo \(M\), giving
\(M\mid99\cdot10^{L-2}\). Coprimality with \(10\) gives \(M\mid99\).

**Interpretation boundary.** This is a classification of the output
**residue**, not of a deterministic update of the full pair
\((\ell(n),n\bmod M)\). Even when \(M\mid99\), the output length need
not be determined by that pair. For example, at \(M=99\), both \(100\)
and \(991\) have length \(3\) and residue \(1\), whereas
\(T(100)=101\) has length \(3\) and \(T(991)=1190\) has length \(4\).
The exact statement in Section 6 respects this boundary; calling it an
autonomous quotient of the full length-and-residue state would not.

## Addendum: sharp uniform entry into divisibility by eleven

The further theorem \(11\mid T^6(n)\) for every positive integer \(n\)
is correct, and the constant six is optimal for unrestricted continued
positive-integer iteration. At a step without width growth, let \(q_0\)
be the input's leading digit plus units digit (twice that digit at width
one). The final column has no outgoing carry, so \(q_0\le9\); therefore
the units column also has no outgoing carry. The output's units digit is
\(q_0\), and its leading digit is \(q_0+c\ge q_0\), where \(c\) is
the incoming carry to the final column, taken as zero at width one. The
next outer sum is consequently at least \(2q_0\). Four consecutive steps
without width growth give outer sum at least \(16\), so the fifth step
must overflow. Thus width increases within five steps from every positive
input. If the starting width is odd, its first increase reaches even width
because a step increases width by at most one; the following step, no
later than step six, is divisible by \(11\). An even starting width gives
divisibility at the first step. Divisibility then persists by
\(\operatorname{rev}_{10}(n)\equiv(-1)^{\ell(n)-1}n\pmod{11}\).
Sharpness is witnessed by
\[
100,\ 101,\ 202,\ 404,\ 808,\ 1616,\ 7777,
\]
whose residues modulo \(11\) are respectively
\(1,2,4,8,5,10,0\). This is a divisibility-entry theorem, not a bound on
the first palindrome time; the sharpness witness already reaches a
palindrome at step one. The proof applies to continuing the specified
map \(T\) after a palindrome as well as before one. This audit confirms
the mathematics; the separate agent's Lean implementation was still in
progress when this paragraph was written.
