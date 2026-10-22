# Agent #206 — Palindrome conditions 和 the center

## Answer

**THEOREM (complete hand proof):** Every positive decimal reverse-and-add orbit, continued indefinitely, 有 infinitely many states whose central column sum is at most \(9\). Consequently, the entire class of proposed invariants requiring a central column sum at least \(10\) at every phase cannot work. More quantitatively, an initial central sum in \([10,17]\) falls below \(10\) within \(6\) transitions, or within \(5\) for odd initial length; an initial central sum \(18\), with maximal central \(18\)-run of length \(r\), falls below \(10\) within \(5r+6\) transitions. The proof combines exact center transitions, a deficit that doubles except at odd-length overflows, 和 exact erosion of a central \(18\)-run. The report also supplies the complete one-step palindrome criterion, full carry bookkeeping, counterexamples to stronger false statements, 和 reproducible checks over \(3{,}969\) short admissible profiles plus \(14\) sample orbits of \(1{,}000\) transitions each. Decimal Lychrel existence remains unresolved; the result 是 a precise obstruction to a whole class of center-based constructions. The one-step criterion 和 central-run erosion already occur in the repository; the additional contribution here is their combination with the high-center transition inequalities to obtain recurrent low centers. A complete hand proof of the broader theorem follows below; a new Lean formalization remains outstanding.

## 1. Definitions 和 scope

For a positive integer \(n\), write its canonical decimal digits in units-first order:

\[
n=\sum_{i=0}^{L-1}d_i10^i,
\qquad 0\le d_i\le9,
\qquad d_{L-1}>0.
\]

Put

\[
T(n)=n+\operatorname{rev}(n),\qquad
q_i=d_i+d_{L-1-i}.
\]

Thus \(q_i=q_{L-1-i}\), \(0\le q_i\le18\), 和 \(q_0\ge1\). For odd \(L\), the middle coefficient is even. Carries 和 emitted digits satisfy

\[
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,
\qquad
e_i=q_i+c_i-10c_{i+1}.
\tag{1}
\]

Every carry belongs to \(\{0,1\}\). Let \(\gamma=c_L\). For \(\gamma=0\), the next length is \(L\); for \(\gamma=1\), append \(e_L=1\), giving length \(L+1\). The next profile is always formed using the **actual new length**:

\[
q'_i=e_i+e_{L+\gamma-1-i}.
\tag{2}
\]

Define the central coefficient

\[
x(q)=q_{\lfloor(L-1)/2\rfloor}.
\]

For even length, the central coefficients coincide by symmetry, so either gives the same value. A *high center* means \(x\ge10\); a *low center* means \(x\le9\). The terms refer to the input profile, whose safety determines whether the **next** integer is palindromic.

All orbit statements concern ordinary positive integers 和 actual carries. Iteration continues after any palindrome. The argument permits arbitrary actual carry schedules 和 uses neither a palindrome-avoidance premise nor a statistical independence premise.

## 2. THEOREM — Complete one-step palindrome criterion (known)

For every positive decimal integer,

\[
\boxed{
T(n)\text{ is palindromic}
\iff
\bigl(\forall i, q_i\le9\bigr)
\ \lor\
\bigl(\forall i, q_i\in\{0,11\}\bigr).
}
\tag{3}
\]

In the second alternative, positivity forces \(q_0=11\). The alternatives give \(\gamma=0\) 和 \(\gamma=1\), respectively.

这个 criterion already appears as `step_palindrome_iff` in the repository foundation [R1]. Ando 的 paper also states it [R2]. The following direct proof establishes the exact conventions needed here; novelty is unclaimed for (3).

### 2.1. Proof without overflow

Assume \(\gamma=0\). Reflection pairs \(i\) with \(j=L-1-i\). Since \(q_i=q_j\),

\[
e_i-e_j=(c_i-c_j)-10(c_{i+1}-c_{j+1}).
\]

If \(e_i=e_j\), the first difference belongs to \(\{-1,0,1\}\), while the second term belongs to \(\{-10,0,10\}\). The differences 都 vanish. Therefore

\[
c_i=c_{L-1-i},\qquad c_{i+1}=c_{L-i}.
\tag{4}
\]

The second identity at \(i=0\) gives \(c_1=c_L=0\). For \(1\le i<L\), the first identity at \(i-1\), followed by the second at \(i\), gives

\[
c_{i-1}=c_{L-i}=c_{i+1}.
\]

Starting from \(c_0=c_1=0\), every carry vanishes. Equation (1) then gives \(q_i\le9\) for every column. The length-one boundary also follows from \(c_0=c_L=0\).

Conversely, if every \(q_i\le9\), induction in (1) gives every carry zero. Then \(e_i=q_i\), 和 the output is symmetric.

### 2.2. Proof with overflow

Assume \(\gamma=1\). Reflection pairs \(i\) with \(L-i\), rather than \(L-1-i\). Palindromicity forces \(e_0=e_L=1\), hence \(q_0\in\{1,11\}\). If \(q_0=1\), symmetry would give

\[
c_L=\left\lfloor\frac{1+c_{L-1}}{10}\right\rfloor=0,
\]

contradicting overflow. Thus \(q_0=11\), 和 \(c_1=c_L=1\).

For the induction, suppose \(1\le i<L\),

\[
q_{i-1}=11s,\qquad c_i=c_{L-i+1}=s,\qquad s\in\{0,1\}.
\]

因为 \(q_{L-i}=q_{i-1}\),

\[
e_{L-i}=q_{i-1}+c_{L-i}-10c_{L-i+1}=s+c_{L-i}.
\]

Consequently \(e_i=e_{L-i}\) implies

\[
q_i=10c_{i+1}+c_{L-i}.
\tag{5}
\]

The carries in (5) 都 leave columns whose sum is \(q_i\), since \(q_{L-i-1}=q_i\). Equation (5) restricts \(q_i\) to \(\{0,1,10,11\}\). Every case is explicit:

| Candidate \(q_i\) | Actual outgoing carries | Right side of (5) | Outcome |
|---:|---|---:|---|
| \(0\) | \(0,0\) | \(0\) | allowed |
| \(1\) | \(0,0\) | \(0\) | contradiction |
| \(10\) | \(1,1\) | \(11\) | contradiction |
| \(11\) | \(1,1\) | \(11\) | allowed |

Thus \(q_i\in\{0,11\}\), with \(c_{i+1}=c_{L-i}=q_i/11\), completing the induction.

For the converse, write \(q_i=11s_i\), where \(s_i\in\{0,1\}\), \(s_i=s_{L-1-i}\), 和 \(s_0=1\). A zero column resets its outgoing carry to zero; an eleven column sets it to one. Hence \(c_{i+1}=s_i\). Define \(s_{-1}=s_L=0\). All output digits, including the final overflow digit, satisfy

\[
e_i=s_i+s_{i-1}\qquad(0\le i\le L).
\]

Reflection of the symmetric binary word gives \(e_i=e_{L-i}\). 这 completes the proof of (3).

### 2.3. THEOREM — Exact safety witnesses

Negating (3) gives

\[
\boxed{
T(n)\text{ is nonpalindromic}
\iff
(\exists i:\ q_i\ge10)
\ \land\
(\exists j:\ q_j\notin\{0,11\}).
}
\tag{6}
\]

The witnesses may occupy different positions. A single coefficient in

\[
\{10,12,13,14,15,16,17,18\}
\tag{7}
\]

satisfies the requirements simultaneously. At odd length, a high central coefficient automatically belongs to (7), 因为 it is even. At even length, a central coefficient \(11\) alone is insufficient.

For an overflow palindrome with odd input length, the central coefficient must equal \(0\): the center is even, 和 the only even member of \(\{0,11\}\) is zero.

## 3. THEOREM — Exact center transitions above the threshold

Assume \(x\ge10\). Every high column forces outgoing carry one. The following calculations cover every length parity 和 overflow case.

### 3.1. Even length \(L=2k\)

The central coefficients are \(q_{k-1}=q_k=x\). Write \(a=c_{k-1}\). Then

\[
c_k=c_{k+1}=1,\qquad
e_{k-1}=x+a-10,\qquad e_k=x-9.
\]

Without overflow, the new center is the sum of the displayed digits:

\[
\boxed{x'=2x+a-19.}
\tag{8}
\]

With overflow, the new length is \(2k+1\), so \(e_k\) is the unique central digit:

\[
\boxed{x'=2e_k=2x-18.}
\tag{9}
\]

Since \(a\le1\), the cases 都 give \(x'\le2x-18\le x\).

### 3.2. Odd length \(L=2k+1\ge3\), without overflow

Write \(a=c_k\). The center emits \(e_k=x+a-10\), giving

\[
\boxed{x'=2x+2a-20\le2x-18\le x.}
\tag{10}
\]

### 3.3. Odd length \(L=2k+1\ge3\), with overflow

Let \(y=q_{k-1}=q_{k+1}\), 和 let \(a=c_k\). The new central digits are \(e_k,e_{k+1}\). Since \(c_{k+1}=1\),

\[
x'=x+y+a-9-10\left\lfloor\frac{y+1}{10}\right\rfloor.
\]

The incoming central carry is constrained by the preceding column \(y\):

| Neighbor \(y\) | Incoming carry \(a\) | \(e_k\) | \(e_{k+1}\) | New center \(x'\) |
|---|---:|---:|---:|---:|
| \(0\le y\le8\) | \(0\) | \(x-10\) | \(y+1\) | \(x+y-9\) |
| \(y=9\) | \(0\) or \(1\) | \(x+a-10\) | \(0\) | \(x+a-10\) |
| \(10\le y\le18\) | \(1\) | \(x-9\) | \(y-9\) | \(x+y-18\) |

Every entry gives \(x'\le x\). Equality can occur only in the final row with \(y=18\). Such a transition changes the length from odd to even.

### 3.4. Length one

Here \(x=2d_0\). If \(x\ge10\), overflow occurs, 和 the output digits are \(x-10,1\). Therefore

\[
\boxed{x'=x-9\le9.}
\tag{11}
\]

### 3.5. Consequences

The complete table gives

\[
\boxed{x\ge10\Longrightarrow x'\le x.}
\tag{12}
\]

Moreover,

\[
\boxed{
x\ge10\ \land\ (L\text{ even or }\gamma=0)
\Longrightarrow 18-x'\ge2(18-x).
}
\tag{13}
\]

The qualification \(x\ge10\) is essential. Low centers can later increase; Section 8 gives an explicit counterexample to unrestricted monotonicity.

## 4. THEOREM — Bounds on consecutive overflow choices

Let \(p=q_0\). Positivity gives \(1\le p\le18\).

### 4.1. At most four consecutive transitions without overflow

If \(\gamma=0\), then \(p\le9\), 和 (1)–(2) give

\[
p'=e_0+e_{L-1}=2p+c_{L-1}\ge2p.
\tag{14}
\]

After four consecutive such transitions, the outer coefficient is at least \(16\), which forces overflow on the next transition. Thus every block of five transitions contains an overflow. In particular, the \(r\)-th overflow occurs by transition \(5r\).

### 4.2. At most three consecutive overflows

Overflow requires \(p\ge9\), 和

\[
p'=e_0+1=
\begin{cases}
10,&p=9,\\
p-9,&10\le p\le18.
\end{cases}
\tag{15}
\]

For \(10\le p\le17\), the successor satisfies \(p'\le8\), forcing a transition without overflow. Starting from \(p=9\), an overflow gives \(10\), whose next overflow gives \(1\). Starting from \(p=18\), the longest possible overflow chain is

\[
18\longrightarrow9\longrightarrow10\longrightarrow1.
\]

The final value forces a transition without overflow. The cases exhaust \(p\in\{9,\ldots,18\}\); four consecutive overflows are impossible.

## 5. THEOREM — A high center below \(18\) escapes within six transitions

Suppose \(10\le x_0\le17\). Then

\[
\boxed{\exists t\in\{1,\ldots,6\}:\ x_t\le9.}
\tag{16}
\]

For odd initial length, the upper bound improves to \(5\).

**Proof.** Assume the center remains high during the interval under consideration, 和 put \(\delta_t=18-x_t\). By (12), the deficit cannot decrease. Call a transition \(D\) when its source length is even or its overflow bit equals zero. Equation (13) gives \(\delta_{t+1}\ge2\delta_t\) on every \(D\). The remaining type \(S\) means odd source length with overflow. An \(S\) produces even length, so consecutive \(S\)'s are impossible.

For even initial length, \(\delta_0\ge1\), 和 the first transition is \(D\). If the center remained high through transition \(6\), the deficit would remain at most \(8\), allowing at most three \(D\)'s. A six-letter sequence starting with \(D\), without consecutive \(S\)'s, 和 with at most three \(D\)'s must be

\[
D,S,D,S,D,S.
\]

Every \(S\) overflows. Every displayed \(D\) starts at even length 和 must end at odd length to permit the following \(S\), so it also overflows. 这 would give six consecutive overflows, contradicting Section 4.2. Therefore some center by time \(6\) is low.

For odd initial length, center parity gives \(x_0\le16\), hence \(\delta_0\ge2\). Remaining high through five transitions would allow at most \(2\) occurrences of \(D\). Avoiding consecutive \(S\)'s forces

\[
S,D,S,D,S.
\]

The same parity bookkeeping forces every displayed transition to overflow, contradicting Section 4.2. Thus a low center occurs by time \(5\). Length one already exits in a single transition by (11). The bounds are upper bounds; sharpness for actual integer orbits is unclaimed.

## 6. THEOREM — Exact erosion of the saturated central run (known lemma)

Suppose \(x=18\). Let \([u,v]\) be the maximal central interval of \(18\)'s, so

\[
u+v=L-1,\qquad r=v-u+1\ge1.
\]

Let \(a=c_u\). If \(r'\) denotes the length of the successor 的 maximal central \(18\)-run, with \(r'=0\) when its center differs from \(18\), then

\[
\boxed{
r'=
\begin{cases}
r,&\gamma=0,\ a=1,\\
\max(r-2,0),&\gamma=0,\ a=0,\\
r-1,&\gamma=1.
\end{cases}}
\tag{17}
\]

The repository already contains the tracked central-run law as `RunAncestry.central_run_step`, together with a stronger general ancestry extinction bound [R3]. The following proof makes the actual-center boundary cases explicit.

### 6.1. The run fills the whole word

If \(u=0\), then \(q=18^L\), \(a=0\), 和 overflow is forced. The output digits, in units-first order, are

\[
(8,\underbrace{9,\ldots,9}_{L-1},1).
\]

After re-folding at length \(L+1\), the outer coefficients equal \(9\), 和 the central coefficients equal \(18\) at precisely the \(L-1\) interior positions. Thus \(r'=L-1=r-1\). For \(L=1\), the new profile is \((9,9)\), giving \(r'=0\).

### 6.2. A proper central run

Assume \(u>0\), 和 put

\[
s=q_{u-1}=q_{v+1}\ne18.
\]

Across the run, the first column emits \(8+a\), sets carry one, 和 every later column emits \(9\):

\[
e_u=8+a,\qquad e_{u+1}=\cdots=e_v=9.
\tag{18}
\]

**Without overflow, \(a=0\):** For \(r\ge2\), the reflected boundary sums become \(17\), while the interior remains \(18\), leaving \(\max(r-2,0)\) central positions. For \(r=1\), the new center equals \(16\), also giving zero. The non-\(18\) boundary positions prevent any extension or merger into a larger central run.

**Without overflow, \(a=1\):** The existing run remains entirely \(18\). To test extension, let \(b=c_{u-1}\). The neighbor cases are:

| Neighbor \(s\) | Carry restriction | Successor coefficient immediately outside the run |
|---|---|---:|
| \(0\le s\le8\) | forces \(a=0\) | excluded here |
| \(s=9\) | \(a=1\) forces \(b=1\) | \(0+0=0\) |
| \(10\le s\le17\) | \(a=1\), \(b\in\{0,1\}\) | \(2s+b-19\le16\) |

Thus the run cannot extend, 和 \(r'=r\).

**With overflow:** Reflection shifts from \(i\leftrightarrow L-1-i\) to \(i\leftrightarrow L-i\). The interval \([u+1,v]\) is central 和 consists of \(18\)'s, of length \(r-1\). Its neighboring coefficient is \(e_u+e_{v+1}\). The full boundary calculation is

\[
e_u+e_{v+1}=
\begin{cases}
s+9,&0\le s\le8\quad(a=0),\\
8+a,&s=9,\\
s,&10\le s\le17\quad(a=1).
\end{cases}
\]

Every value is below \(18\), preventing extension. For \(r=1\), the empty interval corresponds to a successor center below \(18\); the displayed calculation still applies. Hence \(r'=r-1\), completing every case of (17).

### 6.3. THEOREM — Finite lifetime of a saturated center

As long as the center stays \(18\), equation (17) tracks its actual maximal central run: the length never increases, 和 each overflow removes one position. Section 4.1 supplies an overflow in every five transitions. Therefore

\[
\boxed{x_0=18\Longrightarrow
\exists\,1\le t\le5r:\ x_t\le17.}
\tag{19}
\]

The argument is independent of any invariant outer-prefix assumption. Its outer-coefficient calculation supplies only a frequency bound; the central-run erosion is the global structural ingredient.

## 7. THEOREM — Low centers recur in every positive orbit

Let \(n_t=T^t(n_0)\), with \(n_0>0\), 和 let \(x_t\) denote the central coefficient of its actual profile. Then

\[
\boxed{\forall t_0\in\mathbb N\ \exists t\ge t_0:\ x_t\le9.}
\tag{20}
\]

**Proof.** At any starting time, a low center already satisfies the conclusion. A center in \([10,17]\) reaches a low center within six transitions by (16). For a center \(18\), (19) gives a center at most \(17\) within \(5r\) transitions; if that center remains high, apply (16). Thus a low center occurs within \(5r+6\) transitions. The argument can restart at arbitrary \(t_0\), establishing (20).

In particular, there are infinitely many low-center states. At any qualifying odd-length state, the evenness of the central coefficient sharpens \(x_t\le9\) to \(x_t\le8\), equivalently a middle decimal digit at most \(4\). The refinement requires odd length at the qualifying state; the parity of infinitely many qualifying states remains unspecified.

### 7.1. THEOREM — Obstruction for templates

Every positive integer orbit violates

\[
x_t\ge10\qquad\text{for every }t\ge t_0
\]

for any finite \(t_0\). Therefore a finite return certificate cannot realize an infinite ordinary orbit while requiring the physical central coefficient to stay high at **every** intermediate phase. In particular, the stronger permanent condition \(x_t\in\{10,12,13,14,15,16,17,18\}\) cannot work.

这个 obstruction concerns every actual transition, including intermediate transitions between returns. It allows a high center at return times if intervening phases contain low centers. It also allows larger central blocks whose safety witness changes position, 和 templates whose outer or interface coefficients provide the required high witness during low-center phases. Equation (20) alone implies nothing about the existence of a palindrome: condition (6) concerns the whole profile.

## 8. THEOREM — Explicit counterexamples to stronger claims

**A high center alone can permit the next palindrome.** The integer \(56\) 有 profile \((11,11)\), carries \((0,1,1)\), 和 next value \(121\). The exceptional coefficient \(11\) cannot supply the required witnesses simultaneously in (6).

**Initial central protection can fail.** Starting from \(95\),

\[
95\longrightarrow154\longrightarrow605\longrightarrow1111,
\]

with central coefficients

\[
14\longrightarrow10\longrightarrow0\longrightarrow2.
\]

The first \(2\) input profiles 有 a center in (7), 可是 the next input profile is \((11,0,11)\), producing the palindrome \(1111\). 这 directly refutes permanent protection inferred from a high starting center.

**Center monotonicity is restricted to high centers.** The step \(18\to99\) takes central coefficient \(9\) to \(18\). Equation (12) cannot be extended to low input centers.

**An odd overflow can preserve a high center.** The step \(989\to1978\) takes central coefficient \(16\) to \(16\), with neighboring coefficient \(18\). Strict decrease at every high-center step would therefore be false; the parity change is needed in the deficit argument.

## 9. THEOREM — One-step certification by an isolated center block

Let \(C\) be a finite symmetric center block with coefficients in \([0,18]\), 和 with an even central coefficient when its length is odd. Consider all admissible symmetric profile completions containing \(C\) as their central block, allowing unrestricted outer coefficients.

Every completion gives a nonpalindromic next output **if 和 only if** \(C\) contains a coefficient at least \(10\) 和 a coefficient outside \(\{0,11\}\).

**Proof.** Sufficiency is (6). For necessity, if \(C\) lacks any coefficient at least \(10\), the completion \((2)\,C\,(2)\) contains only coefficients at most \(9\), so its next output is palindromic. If every coefficient of \(C\) belongs to \(\{0,11\}\), the completion \((11)\,C\,(11)\) also gives a palindromic next output. Each completion is realizable: for an outer coefficient \(s>0\), choose the leading digit \(\min(9,s)\) 和 the units digit \(s-\min(9,s)\); split each inner mirrored coefficient into digits at most \(9\), 和 halve the even center when present. Thus the necessity cases refer to actual positive integers.

For the single central coefficient, permanent satisfaction is excluded by (20). Larger center blocks remain an open direction 因为 their witness can move away from the exact center.

## 10. Validation: code 和 recorded output

The computations below test the exact identities 和 look for counterexamples to the stated finite bounds. Their scope is finite identity validation. The mathematical proofs above are independent of the finite coverage.

The short-profile check enumerates all admissible symmetric profiles of lengths \(1\) through \(5\): \(9+18+180+342+3420=3969\). Each profile is realized as an actual decimal integer; ordinary integer reversal independently checks the profile implementation. The trajectory checks execute \(1000\) transitions for each of \(14\) named samples, continuing after palindromes, 和 test every complete bounded center window within each trace. The long sample with \(25\) consecutive digits \(9\) checks erosion over a larger central block.

`first_pal=None` below means that the finite run encountered zero palindromes through the checked endpoint; infinite-time behavior remains unasserted. Time zero is included in `first_pal`, so an initially palindromic sample reports zero. The examples serve as validation controls; a Lychrel construction remains outstanding.

### Reproduction

Save the Python block below as `agent206_validation.py` 和 execute `python3 agent206_validation.py`. It uses only the Python standard library. The recorded output is included immediately after the code.

```python
#!/usr/bin/env python3
"""Finite checks of Agent 206's identities; no existence search."""
from itertools import product


def step(n):
    return n + int(str(n)[::-1])


def profile(n):
    d = [int(v) for v in str(n)[::-1]]
    return [a + b for a, b in zip(d, d[::-1])]


def normalize(q):
    c, e = [0], []
    for s in q:
        total = s + c[-1]
        c.append(total // 10)
        e.append(total % 10)
    if c[-1]:
        e.append(1)
    return e, c, [a + b for a, b in zip(e, e[::-1])]


def center(q):
    return q[(len(q) - 1) // 2]


def central_run(q, symbol=18):
    left, right = (len(q) - 1) // 2, len(q) // 2
    if q[left] != symbol or q[right] != symbol:
        return 0, left
    while left and q[left - 1] == symbol:
        left -= 1
        right += 1
    return right - left + 1, left


def realize(q):
    """A canonical decimal integer with exactly this admissible profile."""
    d = [0] * len(q)
    for i in range(len(q) // 2):
        high = min(9, q[i])
        d[len(q) - 1 - i], d[i] = high, q[i] - high
    if len(q) % 2:
        d[len(q) // 2] = q[len(q) // 2] // 2
    n = sum(v * 10**i for i, v in enumerate(d))
    assert n > 0 and profile(n) == q
    return n


def admissible_profiles(length):
    for h in product(range(19), repeat=(length + 1) // 2):
        if h[0] == 0 or (length % 2 and h[-1] % 2):
            continue
        yield list(h) + list(h[:-1] if length % 2 else h)[::-1]


def check_local(q):
    e, c, nxt = normalize(q)
    length, x, overflow = len(q), center(q), c[-1]
    expected_pal = max(q) < 10 or all(v in (0, 11) for v in q)
    assert (e == e[::-1]) == expected_pal
    if x >= 10:
        if length == 1:
            assert overflow == 1
            expected_x = x - 9
        elif length % 2 == 0:
            a = c[length // 2 - 1]
            expected_x = 2 * x - 18 if overflow else 2 * x + a - 19
        else:
            k, a = length // 2, c[length // 2]
            y = q[k - 1]
            if not overflow:
                expected_x = 2 * x + 2 * a - 20
            elif y <= 8:
                assert a == 0
                expected_x = x + y - 9
            elif y == 9:
                expected_x = x + a - 10
            else:
                assert a == 1
                expected_x = x + y - 18
        assert center(nxt) == expected_x <= x
        if not overflow or length % 2 == 0:
            assert center(nxt) <= 2 * x - 18
    r, left = central_run(q)
    if r:
        expected_r = r - 1 if overflow else (r if c[left] else max(r - 2, 0))
        assert central_run(nxt)[0] == expected_r
    p = q[0]
    if overflow:
        assert p >= 9 and nxt[0] == (10 if p == 9 else p - 9)
    else:
        assert 1 <= p <= 9 and nxt[0] == 2 * p + c[length - 1]
    return e, c, nxt


def escape_bound(q):
    x = center(q)
    if x < 10:
        return 0
    if x < 18:
        return 5 if len(q) % 2 else 6
    return 5 * central_run(q)[0] + 6


def first_low(q, bound):
    for t in range(bound + 1):
        if center(q) < 10:
            return t
        q = normalize(q)[2]
    raise AssertionError("high-center escape bound failed")


def finite_checks():
    count = high = saturated = 0
    for length in range(1, 6):
        for q in admissible_profiles(length):
            count += 1
            high += center(q) >= 10
            saturated += center(q) == 18
            e, c, nxt = check_local(q)
            n = realize(q)
            actual = step(n)
            assert profile(actual) == nxt
            assert actual == sum(v * 10**i for i, v in enumerate(e))
            first_low(q, escape_bound(q))
    print(f"profiles={count}; high_centers={high}; saturated_centers={saturated}")
    print("palindrome criterion, center transitions, run erosion, integer bridge, escape bounds: PASS")


def trajectory(seed, steps=1000):
    n, centers, lengths, first_pal = seed, [], [], None
    carries, run_data, first_low_time = [], [], None
    for t in range(steps):
        q = profile(n)
        centers.append(center(q))
        lengths.append(len(q))
        run_data.append(central_run(q)[0])
        if first_pal is None and str(n) == str(n)[::-1]:
            first_pal = t
        if first_low_time is None and center(q) < 10:
            first_low_time = t
        e, c, nxt = check_local(q)
        carries.append(c[-1])
        n_next = step(n)
        assert nxt == profile(n_next)
        n = n_next
    centers.append(center(profile(n)))
    for t in range(steps):
        if centers[t] < 10:
            continue
        bound = (5 * run_data[t] + 6 if centers[t] == 18
                 else 5 if lengths[t] % 2 else 6)
        if t + bound <= steps:
            assert any(x < 10 for x in centers[t + 1:t + bound + 1])
    assert all(any(carries[t:t + 5]) for t in range(steps - 4))
    assert all(not all(carries[t:t + 4]) for t in range(steps - 3))
    if first_low_time is None and centers[-1] < 10:
        first_low_time = steps
    if first_pal is None and str(n) == str(n)[::-1]:
        first_pal = steps
    print(f"seed={seed}; steps={steps}; first_low={first_low_time}; "
          f"first_pal={first_pal}; final_digits={len(str(n))}; PASS")


def explicit_counterexamples():
    n = 95
    trace = []
    for _ in range(5):
        trace.append((n, center(profile(n))))
        n = step(n)
    print("false permanent-high-center claim:", trace)
    for n in (56, 605, 879, 989, 109991):
        q = profile(n)
        e, c, nxt = normalize(q)
        print(f"one_step n={n}; q={q}; carries={c}; "
              f"next={step(n)}; next_center={center(nxt)}")


if __name__ == "__main__":
    finite_checks()
    explicit_counterexamples()
    seeds = (19, 56, 65, 75, 85, 95, 89, 109, 879, 989,
             9999, 109991, 1999992, int("1" + "9" * 25 + "2"))
    for seed in seeds:
        trajectory(seed)
    print("trajectory_steps=14000; all checks PASS")
```

```text
profiles=3969; high_centers=1976; saturated_centers=380
palindrome criterion, center transitions, run erosion, integer bridge, escape bounds: PASS
false permanent-high-center claim: [(95, 14), (154, 10), (605, 0), (1111, 2), (2222, 4)]
one_step n=56; q=[11, 11]; carries=[0, 1, 1]; next=121; next_center=4
one_step n=605; q=[11, 0, 11]; carries=[0, 1, 0, 1]; next=1111; next_center=2
one_step n=879; q=[17, 14, 17]; carries=[0, 1, 1, 1]; next=1857; next_center=13
one_step n=989; q=[18, 16, 18]; carries=[0, 1, 1, 1]; next=1978; next_center=16
one_step n=109991; q=[2, 9, 18, 18, 9, 2]; carries=[0, 0, 0, 1, 1, 1, 0]; next=309892; next_center=17
seed=19; steps=1000; first_low=1; first_pal=2; final_digits=399; PASS
seed=56; steps=1000; first_low=1; first_pal=1; final_digits=399; PASS
seed=65; steps=1000; first_low=1; first_pal=1; final_digits=399; PASS
seed=75; steps=1000; first_low=1; first_pal=2; final_digits=416; PASS
seed=85; steps=1000; first_low=1; first_pal=2; final_digits=399; PASS
seed=95; steps=1000; first_low=2; first_pal=3; final_digits=419; PASS
seed=89; steps=1000; first_low=4; first_pal=24; final_digits=399; PASS
seed=109; steps=1000; first_low=0; first_pal=2; final_digits=420; PASS
seed=879; steps=1000; first_low=2; first_pal=None; final_digits=427; PASS
seed=989; steps=1000; first_low=4; first_pal=0; final_digits=407; PASS
seed=9999; steps=1000; first_low=8; first_pal=0; final_digits=428; PASS
seed=109991; steps=1000; first_low=4; first_pal=15; final_digits=410; PASS
seed=1999992; steps=1000; first_low=9; first_pal=None; final_digits=411; PASS
seed=199999999999999999999999992; steps=1000; first_low=40; first_pal=None; final_digits=443; PASS
trajectory_steps=14000; all checks PASS
```

## 11. Relation to existing work 和 verification status

The inspected repository snapshot was `c6902ac6c366ce018e68a810f58b400dda07145a`.

| Component | Existing source or status |
|---|---|
| Exact one-step palindrome characterization | Already in [R1]; also stated in [R2] |
| Exact central \(0/18\)-run erosion | Already in [R3], `RunAncestry.central_run_step` |
| General tracked-run extinction | [R3] already supplies `extinct_uniform` with bound \(4r+1\); the self-contained \(5r\) center bound here is intentionally simpler |
| High-center inequalities 和 six/five-transition escape | Complete hand proofs in Sections 3–5 |
| Infinitely recurring low centers | Complete hand proof in Section 7 |
| New Lean formalization of the broad theorem | Outstanding; the new results carry the THEOREM hand-proof label |
| Accepted return certificate yielding existence | None supplied |

The repository 的 return-certificate machinery [R4] requires safety at every intermediate phase. The current obstruction excludes the additional restriction that each phase obtains its high witness from the physical center. Satisfiability of the existing general checker remains open.

The source inspection gives attribution, rather than a claim that all prior modules were rebuilt during the present task. The changes consist of the report 和 its result-index entry. The repository 的 required changed-file verification is recorded with the draft PR; a successful documentation-only check leaves formal certification of the new hand proof outstanding.

### Sources opened 和 inspected

- **[R1]** Repository foundation, [`step_palindrome_iff`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/LychrelDigitSums.lean). The exact integer criterion includes the positive leading digit, the \(2\) carry cases, 和 outer coefficient \(11\) in the overflow alternative.
- **[R2]** Ando, *Carry Asymmetry, Palindrome Characterization, and Conditional Non-Convergence in the Reverse-and-Add Process*, February 2026, [paper source](https://github.com/nkc-daiki/196-carry-asymmetry/blob/main/paper.tex), Section 3.2. The source was opened; only its one-step characterization is used here. The proof in Section 2 is independently supplied in full.
- **[R3]** [`AncestryExtinction.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent7RunPopulationRenewal/AncestryExtinction.lean), including `RunAncestry.central_run_step`, `extinct_uniform`, 和 `orbit_ancestry_extinct`; its dependency [`RunAncestry.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent1PeriodicEighteenReturn/RunAncestry.lean) defines the exact tracked descendant.
- **[R4]** [`ReturnCertificate.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean) 和 [`AdmissibleCenters.lean`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleCenters.lean). The modules retain actual template normalization 和 inherited center admissibility; neither supplies an accepted example in the report.

## 12. IDEA — Sharpest remaining center question

The exact center cannot remain the high witness. The next smallest possibility permits the witness to move within the central \(3\) coefficients at odd length or central \(4\) coefficients at even length. Define

\[
W_1(L)=\{i:0\le i<L,\ |2i-(L-1)|\le3\}.
\]

**Open question:** Does there exist a positive nonpalindromic seed \(n\) whose actual orbit satisfies, for every \(t\ge0\),

\[
\max_{i\in W_1(L_t)}q_{t,i}\ge10,
\qquad
\exists j\in W_1(L_t):q_{t,j}\notin\{0,11\}?
\tag{21}
\]

A positive answer, with a finite return template establishing the actual carry transitions 和 growth of the separating runs, would supply the required palindrome avoidance by (6). An obstruction for the wider window would exclude another precise class. In either direction, the center 的 mandatory low phases must be handled explicitly: a cycle of center symbols alone, without its incoming carry constraints 和 interface evolution, is insufficient.
