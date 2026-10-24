# REPORT_207 — Three-run 和 parity obstructions

Agent #207 · Direction 7 · 2026-10-22

## Answer in one paragraph

**THEOREM.** A positive palindrome-free decimal reverse-add orbit cannot remain forever, or eventually forever, within three maximal constant runs in its full column-sum word. More precisely, from width at least five, a state with at most three runs must produce a palindrome or a state with at least five runs within the next 两 additions. Consequently a hypothetical palindrome-free orbit must visit at least five runs in every three consecutive sufficiently late states, giving lower asymptotic density at least \(1/3\). **THEOREM.** 两 consecutive column-sum words consisting entirely of even coefficients force a palindrome; in a nonoverflow step, the odd successor coefficients identify exactly the unequal mirrored output-digit pairs. The results exclude precise classes of invariant templates, including any entire trajectory restricted to three runs or to even coefficients. The decimal existence question remains unresolved. The new results below are **THEOREM** with complete hand proofs; Lean formalization remains pending. Complete reproducible code, actual finite outputs, sharp counterexamples to stronger claims, 和 the remaining question appear below.

## 1. Definitions 和 scope

For a positive decimal integer \(n\), define
\[
R(n)=n+\operatorname{rev}(n).
\]
Write its digits in units-first order as \(d_0,\ldots,d_{L-1}\), with
\(d_{L-1}>0\), 和 put
\[
q_i=d_i+d_{L-1-i}.
\]
Thus \(q\) is symmetric, \(0\le q_i\le18\), 和 \(q_0\ge1\).
At odd width the central coefficient is even. The run-count argument
below actually works without using the central-parity restriction.

Let \(\rho(q)\) count **maximal nonempty constant runs in the entire word**.
For example,
\[
\rho(4\,14\,14\,14\,4)=3,
\qquad
\rho(10\,9\,0\,0\,9\,10)=5.
\]
The number of long bands in a template can be smaller than \(\rho(q)\),
since bounded interface blocks contribute runs too.

The exact incoming carries 和 output digits satisfy
\[
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,
\qquad
e_i=q_i+c_i-10c_{i+1}.
\tag{1}
\]
Since \(q_i\le18\), induction gives \(c_i\in\{0,1\}\). If \(c_L=1\),
append \(e_L=1\). The resulting canonical digit word 有 length
\(L'=L+c_L\). Define the folded successor by
\[
T(q)_i=e_i+e_{L'-1-i}.
\tag{2}
\]
It 是 precisely the column-sum word of \(R(n)\).

In word formulas, \(s^k\) means \(k\) repeated copies of the symbol
\(s\); exponent zero means the empty word. Juxtaposition means
concatenation, including for parenthesized symbols such as \((2a+1)\).
Displayed digit words remain units-first. A final \(1\) in an overflow
formula 是 the new most significant digit.

## 2. THEOREM 207.1 — Escape from at most three runs

**Statement.** Let \(n>0\) 有 width \(L\ge5\), 和 suppose
\(\rho(q)\le3\). Then
\[
\boxed{
R(n)\text{ is palindromic}
\ \lor\ R^2(n)\text{ is palindromic}
\ \lor\ \rho(T(q))\ge5
\ \lor\ \rho(T^2(q))\ge5.
}
\tag{3}
\]

### 2.1 Reduction to one run or three runs

A nonempty symmetric word 有 an odd number of maximal runs. Indeed,
reflection reverses its maximal-run decomposition while preserving run
labels 和 lengths. An even number of runs would give equal adjacent
central labels, contradicting maximality.

Therefore the only possible shapes under the hypothesis are
\[
q=s^L
\qquad\text{or}\qquad
q=a^u b^v a^u,
\tag{4}
\]
where \(1\le s,a\le18\), \(0\le b\le18\), \(a\ne b\),
\(u,v\ge1\), 和 \(L=2u+v\).

For an incoming carry \(c\in\{0,1\}\), equation (1) gives the
complete one-column table:

| Column coefficient | Output digit | Outgoing carry |
| --- | --- | --- |
| \(0\le q_i\le8\) | \(q_i+c\) | \(0\) |
| \(q_i=9,\ c=0\) | \(9\) | \(0\) |
| \(q_i=9,\ c=1\) | \(0\) | \(1\) |
| \(10\le q_i\le18\) | \(q_i+c-10\) | \(1\) |

The following seven cases exhaust the three-run shape. Their carry
intervals include the terminal carry explicitly.

### 2.2 Case I: \(a\le8,\ b\le9\)

The initial carry is zero. The outer low columns preserve zero,
the central columns preserve zero, 和 the final outer columns preserve
zero. Thus \(c_i=0\) for \(0\le i\le L\), 和 \(e=q\) 是 a palindrome.

### 2.3 Case II: \(a\le8,\ b\ge10\)

The exact carries are
\[
c_i=
\begin{cases}
0,&0\le i\le u,\\
1,&u+1\le i\le u+v,\\
0,&u+v+1\le i\le L.
\end{cases}
\tag{5}
\]
The first central high column creates a carry. The first right outer
column resets it, so overflow is absent. The output is
\[
e=a^u(b-10)(b-9)^{v-1}(a+1)a^{u-1}.
\tag{6}
\]
Set \(X=2a\), \(Y=2a+1\), \(Z=2b-19\), 和 \(W=2b-18\).
Folding (6) gives
\[
T(q)=
\begin{cases}
X^{u-1}Y(2b-20)YX^{u-1},&v=1,\\
X^{u-1}YZW^{v-2}ZYX^{u-1},&v\ge2.
\end{cases}
\tag{7}
\]

Here \(X\ne Y\), \(Z\ne W\), 和 \(Y\) can equal \(Z\) exactly when
\[
b=a+10.
\tag{8}
\]
The cases with empty displayed runs require separate treatment:

- If \(v=1\), width at least five forces \(u\ge2\). The five displayed
  blocks alternate even 和 odd labels, so 有 exactly five runs.
- If \(v=2\), then \(u\ge2\). The central \(W\)-run is empty. If
  \(Y\ne Z\), 有 five runs; if \(Y=Z\), the result collapses
  to \(X^{u-1}Y^4X^{u-1}\).
- If \(v\ge3,\ u\ge2\), 有 seven runs when \(Y\ne Z\), 和
  five when \(Y=Z\).
- If \(v\ge3,\ u=1\), the outer \(X\)-runs are empty. There are five
  runs when \(Y\ne Z\), 和 three when \(Y=Z\).

Thus exactly 两 families can retain at most three runs:
\[
\begin{aligned}
\mathrm{IIA}:&\quad u=1,\ v\ge3,\ b=a+10,\qquad
T(q)=(2a+1)^2(2a+2)^{v-2}(2a+1)^2;\\
\mathrm{IIB}:&\quad u\ge2,\ v=2,\ b=a+10,\qquad
T(q)=(2a)^{u-1}(2a+1)^4(2a)^{u-1}.
\end{aligned}
\tag{9}
\]
Their second transitions are resolved in Section 2.9.

### 2.4 Case III: \(a=9,\ b\le8\)

The first outer 9-run receives zero 和 preserves zero. The central low
run resets or preserves zero, 和 the final 9-run receives zero. Thus
\(c_i=0\) throughout, 和 the output \(e=q\) is palindromic.

### 2.5 Case IV: \(a=9,\ b\ge10\)

Put \(B=b-9\), so \(1\le B\le9\). The exact carries are
\[
c_i=0\quad(0\le i\le u),
\qquad
c_i=1\quad(u+1\le i\le L).
\tag{10}
\]
The central high run creates a carry, 和 the final 9-run propagates it
to overflow. Consequently
\[
\begin{aligned}
e&=9^u(B-1)B^{v-1}0^u1,\\
T(q)&=10\,9^{u-1}(B-1)(2B)^{v-1}(B-1)9^{u-1}10.
\end{aligned}
\tag{11}
\]
The neighboring labels satisfy \(10\ne9\), \(9\ne B-1\), 和
\(B-1\ne2B\). If \(u=1\), width at least five forces \(v\ge3\),
giving five runs. If \(u\ge2,\ v=1\), the empty \((2B)\)-run merges
the central copies of \(B-1\), giving five runs. If \(u\ge2,\ v\ge2\),
有 seven runs.

### 2.6 Case V: \(a\ge10,\ b\le8\)

Put \(A=a-9\) 和 \(B=b\). Here
\[
\begin{aligned}
c_0&=0,\\
c_i&=1&& (1\le i\le u),\\
c_i&=0&& (u+1\le i\le u+v),\\
c_i&=1&& (u+v+1\le i\le L).
\end{aligned}
\tag{12}
\]
The first high outer column starts the carry; the first central low
column resets it; the first right outer column restarts it. Hence
\[
\begin{aligned}
e&=(A-1)A^{u-1}(B+1)B^{v-1}(A-1)A^{u-1}1,\\
T(q)&=A(2A)^{u-1}(A+B)(2B)^{v-1}(A+B)(2A)^{u-1}A.
\end{aligned}
\tag{13}
\]
At either interface, the exceptional digits sum to
\((B+1)+(A-1)=A+B\). The endpoint sum is \((A-1)+1=A\).

### 2.7 Case VI: \(a\ge10,\ b=9\)

Put \(A=a-9\) 和 \(B=0\). The first column starts the carry. High
columns force one, while the central 9-run preserves one. Thus
\(c_0=0\) 和 \(c_i=1\) for \(1\le i\le L\). Explicitly,
\[
\begin{aligned}
e&=(A-1)A^{u-1}0^vA^u1,\\
T(q)&=A(2A)^{u-1}A0^{v-1}A(2A)^{u-1}A.
\end{aligned}
\tag{14}
\]
Formula (14) is equation (13) with \(B=0\), derived here from its
distinct carry behavior.

### 2.8 Case VII: \(a\ge10,\ b\ge10\)

Put \(A=a-9\) 和 \(B=b-9\). Each column forces carry one after the
initial column, so \(c_0=0\) 和 \(c_i=1\) for \(1\le i\le L\).
The output 和 fold are
\[
\begin{aligned}
e&=(A-1)A^{u-1}B^vA^u1,\\
T(q)&=A(2A)^{u-1}(A+B)(2B)^{v-1}(A+B)(2A)^{u-1}A.
\end{aligned}
\tag{15}
\]

### 2.9 Complete survivor classification 和 the second step

First resolve the shared high-outer formula (13)–(15). Its parameters
satisfy \(1\le A\le9\), \(0\le B\le9\).

**If \(B=A\):** the fold collapses to
\[
T(q)=A(2A)^{L-1}A.
\tag{16}
\]
Since \(b\ne a\), equality \(B=A\) can occur only in Case V, with
\(b=A\le8\) 和 \(a=A+9\). For \(A\le4\), each coefficient of (16)
is at most eight, so its next output is palindromic. For
\(5\le A\le8\), (16) enters Case II with outer run length one,
central run length \(L-1\ge4\), outer symbol \(A\), 和 center
symbol \(2A\). The sole possible three-run merger would require
\(2A=A+10\), which is impossible for the specified values. Therefore its
next fold 有 five runs.

**If \(B\ne A\):** the equalities \(2A=A+B\) 和 \(A+B=2B\) fail,
while \(A\ne2A\) follows from \(A>0\).

- For \(u\ge2,\ v=1\), the fold 有 five runs.
- For \(u\ge2,\ v\ge2\), the fold 有 seven runs.
- For \(u=1\), width at least five forces \(v\ge3\). If \(B>0\),
  the endpoint labels \(A\) 和 \(A+B\) differ, giving five runs.
  If \(B=0\), the fold becomes \(A^2 0^{v-1}A^2\); its coefficients
  are at most nine, so its next output is palindromic.

It remains to resolve families IIA 和 IIB from (9):

**Family IIA.** For \(a=1,2,3\), each successor coefficient is at most
eight, giving a palindrome next. For \(a=4\), the successor is
\(9^2 10^{v-2}9^2\); Case IV gives at least five runs on its next
step, including \(v-2=1\). For \(a=5,6,7,8\), the outer 和 central
successor symbols are high. In (15), their reduced parameters satisfy
\(B=A+1\), 和 the outer run length is 两. Thus \(B\ne A\); the
preceding high-outer analysis gives five runs if the central length is
one, 和 seven if it is at least 两.

**Family IIB.** For \(a=1,2,3,4\), each successor coefficient is at
most nine, giving a palindrome next. For \(a=5,6,7,8\), the successor
有 high outer 和 central symbols, with reduced parameters
\(B=A+1>0\), central length four, 和 outer length \(u-1\). When
\(u=2\), formula (15) 有 five runs. When \(u\ge3\), it 有 seven.

The cases settle every three-run input.

### 2.10 One-run inputs

Let \(q=s^L\). For \(s\le9\), the carries remain zero 和 the output
是 the palindrome \(s^L\).

For \(s\ge10\), put \(A=s-9\), so \(1\le A\le9\). The carries
are \(c_0=0\) 和 \(c_i=1\) for \(1\le i\le L\), giving
\[
e=(A-1)A^{L-1}1,
\qquad
T(q)=A(2A)^{L-1}A.
\tag{17}
\]
For \(A\le4\), the next output is palindromic. For \(5\le A\le8\),
Case II gives five runs next, since \(2A=A+10\) fails. For \(A=9\),
Case IV gives five runs next. The case analysis completes the proof of (3). \(\square\)

## 3. THEOREM 207.2 — Orbit 和 template consequences

**Statement.** In a positive palindrome-free decimal orbit
\(n_t=R^t(n_0)\), choose \(t_0\) so its width is at least five.
For every \(N\ge0\),
\[
\#\{t_0\le t<t_0+N:\rho(q_t)\ge5\}
\ \ge\ \left\lfloor\frac N3\right\rfloor.
\tag{18}
\]
Consequently the counted times 有 lower asymptotic density at least
\(1/3\). An eventually permanent bound \(\rho(q_t)\le3\) is
incompatible with a palindrome-free orbit.

**Proof.** Reversal of a positive integer is positive, even when its
decimal expansion ends in zero. Thus \(R(n)\ge n+1\), so the orbit
eventually reaches width five 和 retains the same lower bound.

In any three-state window starting at \(t\ge t_0\), a starting run
count at least five already supplies the desired state. Otherwise
symmetry gives \(\rho(q_t)\le3\), 和 Theorem 207.1 supplies a state
with at least five runs at \(t+1\) or \(t+2\), since the palindrome
alternatives are excluded. Partition the first \(3\lfloor N/3\rfloor\)
states into disjoint triples. Each triple contributes at least one
counted state, proving (18). Dividing by \(N\) 和 taking the lower
limit proves the density claim. \(\square\)

**Exact exclusion scope.** The theorem excludes an invariant family
whose entire intermediate trajectory 有 at most three maximal
column-sum runs. A certificate with 两 long bands 和 bounded interface
blocks can already 有 five or more total runs, so the certificate format remains
outside the exclusion. A return observed only at separated times may
也 leave the three-run class between returns. Optimality of the
density constant \(1/3\) remains unclaimed.

## 4. THEOREM 207.3 — Parity detects asymmetry without overflow

**Statement.** Suppose the transition (1) 有 \(c_L=0\). For each
\(0\le i<L\), with \(j=L-1-i\),
\[
\boxed{T(q)_i\equiv0\pmod2\quad\Longleftrightarrow\quad e_i=e_j.}
\tag{19}
\]
In particular, the successor profile consists entirely of even
coefficients exactly when the output digit word is palindromic.

**Proof.** Symmetry gives \(q_i=q_j\). Subtract the column equations:
\[
e_i-e_j=c_i-c_j-10(c_{i+1}-c_{j+1}).
\tag{20}
\]
If \(T(q)_i=e_i+e_j\) is even, then \(e_i-e_j\) is even, so
\(c_i-c_j\) is even. The difference of the 两 carry bits belongs
to \(\{-1,0,1\}\), hence \(c_i=c_j\). Equal coefficients 和 equal
incoming carries give equal output digits directly from (1).
Conversely \(e_i=e_j\) gives \(T(q)_i=2e_i\).

For a central index \(i=j\), the equivalence holds directly. The
same observation covers width one. \(\square\)

## 5. THEOREM 207.4 — Consecutive even profiles are impossible in a palindrome-free orbit

**Statement.** If \(q\) 和 \(T(q)\) consist entirely of even
coefficients, then \(R(n)\) 是 a palindrome.

**Proof, nonoverflow case.** When \(c_L=0\), apply (19) to each
coefficient of the even successor. Its output digit word is symmetric.

**Proof, overflow case.** When \(c_L=1\), the final carry equation 和
symmetry give \(q_0+c_{L-1}\ge10\). Since \(q_0\) is even 和
\(c_{L-1}\le1\), necessarily \(q_0\ge10\). The units digit is
\(e_0=q_0-10\), while the new leading digit is one. Therefore
\[
T(q)_0=e_0+1=q_0-9,
\tag{21}
\]
which is odd, contradicting the even-successor hypothesis. Only the
nonoverflow case remains, 和 it gives the claimed palindrome. \(\square\)

**THEOREM — predecessor restriction.** If the output is nonpalindromic
while \(T(q)\) consists entirely of even coefficients, then
\[
c_L=1,\qquad q_0\in\{9,11,13,15,17\}.
\tag{22}
\]
Indeed, (19) excludes nonoverflow. Evenness of \(e_0+1\) makes
\(e_0\) odd; since \(e_0=q_0\bmod10\), the exterior coefficient
\(q_0\) is odd. The final carry requires \(q_0\ge9\), giving (22).
For \(q_0=9\), the final incoming carry must be one.

**THEOREM — cyclic template budget.** Consider a palindrome-free
period-\(m\) template return whose even-profile property repeats with
the phase. Let \(E\) count the phases consisting entirely of even
coefficients, 和 let \(g\) be the total width increase over the
\(m\) transitions. Then
\[
\boxed{E\le g,\qquad 2E\le m.}
\tag{23}
\]
Each even target requires a distinct overflow transition by (22).
Each overflow increases width by one, giving \(E\le g\). If
\(a_t\in\{0,1\}\) indicates an even phase, Theorem 207.4 gives
\(a_t+a_{t+1}\le1\), including the cyclic boundary. Summation gives
\(2E\le m\).

Thus a template whose complete profile stays even is excluded.
Complementary even bands alone cannot evade the obstruction; odd
coefficients must occur in some intervening phase. Bounded interface
blocks containing odd coefficients remain possible. The results
impose necessary conditions; they supply neither interface growth nor
a contradiction for the general return-certificate format.

## 6. THEOREM 207.5 — Sharp counterexamples to stronger statements

### 6.1 A one-step escape bound fails

Direct integer arithmetic gives
\[
47770+7774=55544,
\qquad
55544+44555=100099.
\]
The exact profiles are
\[
4\,14^3\,4
\ \longmapsto\ 9^2\,10\,9^2
\ \longmapsto\ 10\,9\,0^2\,9\,10,
\]
with run counts \(3,3,5\). The three integers are nonpalindromic.
Hence the 2-step horizon in Theorem 207.1 cannot be replaced by one.

### 6.2 The width-five threshold is necessary for the stated horizon

Direct addition gives
\[
1990\to2981\to4873\to8657\to16225.
\]

| Integer | Full column-sum word | Runs |
| --- | --- | --- |
| \(1990\) | \((1,18,18,1)\) | 3 |
| \(2981\) | \((3,17,17,3)\) | 3 |
| \(4873\) | \((7,15,15,7)\) | 3 |
| \(8657\) | \((15,11,11,15)\) | 3 |
| \(16225\) | \((6,8,4,8,6)\) | 5 |

The displayed integers are nonpalindromic. Starting at \(1990\), neither of
the next 两 additions produces a palindrome or five runs. Therefore
the width hypothesis cannot be lowered to four while retaining (3).

### 6.3 An isolated even profile is possible

The exact nonpalindromic segment
\[
158\to1009\to10010
\]
有 profiles
\[
(9,10,9),\qquad(10,0,0,10),\qquad(1,1,0,1,1).
\]
The respective carry words for the three inputs are
\[
(0,0,1,1),\quad(0,1,0,0,1),\quad(0,0,0,0,0,0),
\]
和 the next value after \(10010\) 是 the palindrome \(11011\).
Thus Theorem 207.4 excludes consecutive even profiles while allowing
an isolated one.

The examples are finite counterexamples to stronger obstruction
statements. They are ordinary terminating examples: the first
palindromes occur at step five for \(47770\), step five for \(1990\),
和 step three for \(158\). Each example was nevertheless continued
for 1,000 steps as a numerical consistency check.

## 7. Repository comparison 和 verification status

Source snapshot inspected:
[`c6902ac6c366ce018e68a810f58b400dda07145a`](https://github.com/taco-jpg/p196-algorithm/tree/c6902ac6c366ce018e68a810f58b400dda07145a).

The relevant prior source files were opened 和 inspected:

- [Foundations/LychrelDigitSums.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/LychrelDigitSums.lean),
  especially `DecimalDigits.step_palindrome_iff` 和 its overflow/nonoverflow
  components. The exact next-palindrome classification already appears
  there; it is prior work.
- [Agent2SaturatedProfile/ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean),
  including `LocalOK`, `Valid`, `StepPal`, 和 `certificate_sound`.
- [Agent2SaturatedProfile/CertificatePhases.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificatePhases.lean),
  including `valid_phase_even` 和 `valid_period_mod6`.
- [Agent2SaturatedProfile/CertificateCarryBudget.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateCarryBudget.lean),
  including `certificate_carry_budget`.

The phase 和 carry-budget restrictions were therefore omitted from
the new results. Searches of `RESULTS.md`, `lean/registry.json`, 和
relevant Lean sources returned the following limited result: 没有 explicit
match for the three-run obstruction or the consecutive-even-profile theorem. Global novelty remains unclaimed.

The new results remain hand proofs. The report introduces zero Lean
modules 和 changes zero Lean declarations. Repository verification of
the documentation-only change checks repository rules; the mathematical arguments remain outside its formal verification scope.

## 8. Reproducible finite checks

The proof above uses exhaustive symbolic cases with unrestricted run
lengths. The following finite computation only audits the formulas 和
their implementation. It performs:

- 10,368 three-run formula checks, including short boundary lengths;
- 10,008 checks of (3), restricted to width at least five;
- 10,467 realizable symmetric-profile checks of the parity assertions;
- 1,000 actual integer steps from each of the three sharpness seeds,
  continuing after the first palindrome.

The formula checks intentionally include abstract odd-center words
that need not represent an integer; the identities hold on the larger
domain. The parity census filters to realizable words. Ordinary-integer
trajectory checks use decimal reversal independently of the carry
normalizer 和 compare their complete outputs.

### Code

```python
from itertools import product


def fold(d):
    return [a + b for a, b in zip(d, d[::-1])]


def step(q):
    carry = 0
    digits, carries = [], [0]
    for x in q:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
        carries.append(carry)
    if carry:
        digits.append(carry)
    return fold(digits), digits, carries


def runs(q):
    return 1 + sum(a != b for a, b in zip(q, q[1:]))


def pal(d):
    return d == d[::-1]


def even(q):
    return all(x % 2 == 0 for x in q)


def profile(n):
    return fold([int(x) for x in str(n)[::-1]])


def reverse_add(n):
    return n + int(str(n)[::-1])


def formula(a, b, u, v):
    if a <= 9 and b <= 9:
        e = [a] * u + [b] * v + [a] * u
        return fold(e), e
    if a <= 8:
        e = ([a] * u + [b - 10] + [b - 9] * (v - 1)
             + [a + 1] + [a] * (u - 1))
        middle = ([2 * b - 20] if v == 1 else
                  [2 * b - 19] + [2 * b - 18] * (v - 2)
                  + [2 * b - 19])
        out = ([2 * a] * (u - 1) + [2 * a + 1] + middle
               + [2 * a + 1] + [2 * a] * (u - 1))
        return out, e
    if a == 9:
        B = b - 9
        e = [9] * u + [B - 1] + [B] * (v - 1) + [0] * u + [1]
        out = ([10] + [9] * (u - 1) + [B - 1]
               + [2 * B] * (v - 1) + [B - 1]
               + [9] * (u - 1) + [10])
        return out, e
    A = a - 9
    if b <= 8:
        B = b
        e = ([A - 1] + [A] * (u - 1) + [B + 1]
             + [B] * (v - 1) + [A - 1] + [A] * (u - 1) + [1])
    elif b == 9:
        B = 0
        e = [A - 1] + [A] * (u - 1) + [0] * v + [A] * u + [1]
    else:
        B = b - 9
        e = [A - 1] + [A] * (u - 1) + [B] * v + [A] * u + [1]
    out = ([A] + [2 * A] * (u - 1) + [A + B]
           + [2 * B] * (v - 1) + [A + B]
           + [2 * A] * (u - 1) + [A])
    return out, e


def check_escape(q):
    q1, e1, _ = step(q)
    q2, e2, _ = step(q1)
    assert pal(e1) or pal(e2) or runs(q1) >= 5 or runs(q2) >= 5


formula_count = escape_count = 0
for a, b, u, v in product(range(1, 19), range(19), range(1, 5), range(1, 9)):
    if a == b:
        continue
    q = [a] * u + [b] * v + [a] * u
    qp, e, _ = step(q)
    assert (qp, e) == formula(a, b, u, v), (a, b, u, v)
    formula_count += 1
    if len(q) >= 5:
        check_escape(q)
        escape_count += 1
for s, L in product(range(1, 19), range(5, 21)):
    check_escape([s] * L)
    escape_count += 1

parity_count = even_edges = nonpal_even_targets = 0
for L in range(1, 7):
    for h in product(range(19), repeat=(L + 1) // 2):
        if h[0] == 0 or (L % 2 and h[-1] % 2):
            continue
        q = list(h) + list(h[:L // 2][::-1])
        qp, e, cs = step(q)
        if cs[-1] == 0:
            for i in range(L):
                assert (qp[i] % 2 == 0) == (e[i] == e[L - 1 - i])
        if even(q) and even(qp):
            assert pal(e)
            even_edges += 1
        if even(qp) and not pal(e):
            assert cs[-1] == 1 and q[0] in (9, 11, 13, 15, 17)
            nonpal_even_targets += 1
        parity_count += 1

print('exact three-run formulas checked:', formula_count)
print('two-step obstruction instances checked:', escape_count)
print('realizable symmetric parity cases checked:', parity_count)
print('even-to-even transitions (all palindromic):', even_edges)
print('nonpalindromic even targets (all overflow/odd exterior):', nonpal_even_targets)

for seed in (47770, 1990, 158):
    n, first_pal = seed, None
    for t in range(1001):
        if str(n) == str(n)[::-1] and first_pal is None:
            first_pal = t
        if t == 1000:
            break
        q = profile(n)
        qp, e, cs = step(q)
        nxt = reverse_add(n)
        assert qp == profile(nxt)
        assert e == [int(x) for x in str(nxt)[::-1]]
        if len(q) >= 5 and runs(q) <= 3:
            check_escape(q)
        if even(q) and even(qp):
            assert pal(e)
        n = nxt
    print(f'seed={seed}; steps=1000; first_palindrome={first_pal}; '
          f'final_width={len(str(n))}; assertions=PASS')

for seed, count in ((47770, 3), (1990, 5), (158, 3)):
    n, values, profiles, counts = seed, [], [], []
    for _ in range(count):
        values.append(n)
        profiles.append(profile(n))
        counts.append(runs(profile(n)))
        n = reverse_add(n)
    print('sharpness:', values)
    print('profiles:', profiles)
    print('run counts:', counts)

print('counterexamples to stated theorems: 0')
```

### Actual output

```text
exact three-run formulas checked: 10368
two-step obstruction instances checked: 10008
realizable symmetric parity cases checked: 10467
even-to-even transitions (all palindromic): 248
nonpalindromic even targets (all overflow/odd exterior): 674
seed=47770; steps=1000; first_palindrome=5; final_width=412; assertions=PASS
seed=1990; steps=1000; first_palindrome=5; final_width=409; assertions=PASS
seed=158; steps=1000; first_palindrome=3; final_width=417; assertions=PASS
sharpness: [47770, 55544, 100099]
profiles: [[4, 14, 14, 14, 4], [9, 9, 10, 9, 9], [10, 9, 0, 0, 9, 10]]
run counts: [3, 3, 5]
sharpness: [1990, 2981, 4873, 8657, 16225]
profiles: [[1, 18, 18, 1], [3, 17, 17, 3], [7, 15, 15, 7], [15, 11, 11, 15], [6, 8, 4, 8, 6]]
run counts: [3, 3, 3, 3, 5]
sharpness: [158, 1009, 10010]
profiles: [[9, 10, 9], [10, 0, 0, 10], [1, 1, 0, 1, 1]]
run counts: [3, 3, 3]
counterexamples to stated theorems: 0
```

## 9. IDEA — The sharpest remaining question

Does an analogous uniform escape theorem hold for **at most five total
maximal constant runs**? A precise next target is to find constants
\(K,L_0\) such that every admissible profile of width at least \(L_0\)
with \(\rho(q)\le5\) produces a palindrome or a profile with at least
seven runs within \(K\) additions. The five-run shape is
\[
a^u b^v c^w b^v a^u,
\qquad a\ne b,\quad b\ne c,
\]
with the appropriate central-parity condition. The case \(c=a\)
must remain included: nonadjacent runs may share a label.

The present proof stops 因为 a five-run word 有 两 distinct
interfaces in each half, allowing new mergers 和 carry interactions
absent from the three-run classification. The parity theorem requires
odd coefficients to recur, 可是 a lower bound on
growth of their number or total width remains unavailable. A proof that bounded interface
complexity eventually fails would address a larger template class.
Such growth 和 five-run escape remain open in the present report.
