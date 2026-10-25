# REPORT_212 — base arithmetic 和 a decimal template obstruction

**Agent:** #212. **Direction:** 2. **Date:** 2026-10-22.

**Proof status:** THEOREM labels below mean complete written proofs; Lean formalization of the report results remains open. The existing repository was inspected at commit `c6902ac6c366ce018e68a810f58b400dda07145a`.

## Answer in one paragraph

**THEOREM / IDEA —** Decimal Lychrel existence remains unresolved. A precise obstruction is established for the direct decimal version of the regular power-of-2 family: write \(W_b(r)=10(b-1)^r(b-2)(b-1)0^r\), with concatenation of base-\(b\) digits. For every fixed \(m\ge1\), every \(r\ge\max(20,2m-22)\), 和 every \(s\ge2\), \(T_{10}^m(W_{10}(r))\ne W_{10}(s)\). The decisive exact identity is \(T_{10}^{16}(W_{10}(r))=18186663\,0^{r-7}\,585455585\,0^{r-7}\,2566927\): the original critical bands become zero bands whose interiors persist for any fixed further horizon. The power-of-2 construction is reconstructed with complete carry tables; its clean reset requires \(2a=b\) with \(a\) obtained by doubling from \(1\), hence exactly \(b=2^\ell\). Separately, noncritical complementary bulk symbols obey doubling modulo \(2(b-1)\); their periodicity criterion admits decimal cycles, so it leaves general decimal impossibility unresolved. The explicit historical constructions in bases \(11,17,26\) exploit critical \(q=b-1\) bands; the opened source leaves the base-\(20\) seed untranscribed. Numerical checks cover 1000 steps for each explicitly tested family, with code 和 output below. **IDEA:** the remaining task is to construct different bounded interfaces that preserve a growing global template, rather than transplant 这 particular family.

## 1. Definitions 和 exact scope

For a positive integer written canonically in base \(b\), let
\[
T_b(n)=n+\operatorname{rev}_b(n).
\]
Displayed digit words are most significant first. A superscript attached to a digit denotes a repeated run, including the empty run when the exponent is zero; ordinary exponentiation of integers occurs only in algebraic formulas. Each parenthesized expression inside a digit word denotes one digit.

For carry calculations, use units-first digits \(d_0,\ldots,d_{L-1}\), the symmetric column sums
\[
q_i=d_i+d_{L-1-i},\qquad c_0=0,
\]
和 the exact recurrence
\[
c_{i+1}=\left\lfloor\frac{q_i+c_i}{b}\right\rfloor,
\qquad e_i=q_i+c_i-bc_{i+1}.
\tag{1}
\]
The bounds \(0\le q_i\le2b-2\) imply \(c_i\in\{0,1\}\). The final carry \(\gamma=c_L\) determines whether a leading digit \(1\) is appended. The resulting digit word is canonical: the most significant input digit is positive, so either its output digit is positive or it produces an overflow.

The distinction between digit bands 和 column-sum bands matters. The repository's template uses complementary column sums \(c,2(b-1)-c\) with \(c\ne b-1\). The regular family considered here 有 opposite long **digit** runs \(b-1,0\), whose reflected interiors yield the **column sum** \(q=b-1\). 那 critical column propagates its incoming carry. The template classes are different.

## 2. THEOREM — the decimal regular family excludes uniform fixed-time returns

Define
\[
W_r:=W_{10}(r)=10\,9^r\,89\,0^r,
\qquad r\ge2.
\]
Its ordinary integer value 和 width are
\[
W_r=11\cdot10^r(10^{r+2}-1),\qquad |W_r|=2r+4.
\]

**THEOREM.** Put \(R(m)=\max(20,2m-22)\). Then
\[
\boxed{
\forall m\ge1\ \forall r\ge R(m)\ \forall s\ge2,
\qquad T_{10}^m(W_r)\ne W_s.
}
\tag{2}
\]
In particular, fixed integers \(m\ge1,g\ge0\) cannot yield
\[
T_{10}^m(W_r)=W_{r+g}
\]
on an unbounded set of parameters \(r\). Thus 这 entire family fails as a uniform finite-return construction, including returns that pass through additional intermediate shapes.

The quantifiers matter. The theorem leaves open the behavior of any particular finite seed after a time depending on its initial run length. It 也 leaves other decimal templates open. Infinite palindrome avoidance for a decimal seed lies outside the conclusion of (2).

### 2.1. Exact sixteen-step digit identities

For every integer \(r\ge20\), the successive words are the following. The conservative lower bound makes every symbolic interval comparison in the carry certificate valid throughout the entire parameter domain.

| \(t\) | Digit word of \(T_{10}^t(W_r)\), most significant first |
|---:|---|
| 0 | \(10\,9^r\,89\,0^r\) |
| 1 | \(11\,0^{r-2}\,9888\,9^{r-2}\,01\) |
| 2 | \(22\,0^{r-2}\,8777\,9^{r-2}\,12\) |
| 3 | \(44\,0^{r-2}\,6555\,9^{r-2}\,34\) |
| 4 | \(88\,0^{r-2}\,2111\,9^{r-2}\,78\) |
| 5 | \(175\,9^{r-2}\,3224\,0^{r-2}\,66\) |
| 6 | \(836\,0^{r-3}\,35463\,9^{r-3}\,637\) |
| 7 | \(1572\,9^{r-3}\,71917\,0^{r-3}\,275\) |
| 8 | \(7293\,0^{r-4}\,691096\,9^{r-4}\,3026\) |
| 9 | \(13497\,0^{r-4}\,381292\,9^{r-4}\,6953\) |
| 10 | \(49466\,9^{r-5}\,3303123\,0^{r-5}\,76384\) |
| 11 | \(97833\,9^{r-5}\,6516157\,0^{r-5}\,42878\) |
| 12 | \(185658\,0^{r-5}\,4032313\,9^{r-5}\,76757\) |
| 13 | \(943337\,9^{r-6}\,35355354\,0^{r-6}\,833338\) |
| 14 | \(1776675\,9^{r-6}\,80710708\,0^{r-6}\,566687\) |
| 15 | \(9643326\,0^{r-7}\,787727797\,9^{r-7}\,6333458\) |
| 16 | \(18186663\,0^{r-7}\,585455585\,0^{r-7}\,2566927\) |

### 2.2. Complete carry certificate for the sixteen steps

For a constant column sum \(q\) repeated \(n\ge1\) times, with incoming carry \(c\), recurrence (1) gives exactly the following cases in decimal:

| Column condition | First output digit | Remaining \(n-1\) digits | Outgoing carries throughout |
|---|---:|---:|---:|
| \(0\le q\le8\) | \(q+c\) | \(q\) | \(0\) |
| \(q=9,c=0\) | \(9\) | \(9\) | \(0\) |
| \(q=9,c=1\) | \(0\) | \(0\) | \(1\) |
| \(10\le q\le18\) | \(q+c-10\) | \(q-9\) | \(1\) |

For the first case, \(q+c\le9\), forcing carry zero immediately. For the second 和 third cases, adding the incoming bit either yields \(9\) or \(10\), preserving 那 bit. For the last case, \(10\le q+c\le19\), forcing carry one immediately; subsequent columns therefore output \(q+1-10=q-9\). The four cases exhaust every column; none assumes an overflow bit in advance.

The next listing gives every outgoing carry \(c_1,\ldots,c_L\) in units-first order. Its last bit is the actual overflow. Each line was checked against its input 和 output digit words by the symbolic verifier in Section 6.

```text
step  0 ->  1: exact; carries 0^(r) 1^(r+2) 0^(2)
step  1 ->  2: exact; carries 0^(r) 1^(r+2) 0^(2)
step  2 ->  3: exact; carries 0^(r) 1^(r+2) 0^(2)
step  3 ->  4: exact; carries 0^(r) 1^(r+2) 0^(2)
step  4 ->  5: exact; carries 1^(r) 0^(r+2) 1^(2)
step  5 ->  6: exact; carries 0^(1) 1^(1) 0^(r-2) 1^(1) 0^(3) 1^(r-2) 0^(1) 1^(1) 0^(1)
step  6 ->  7: exact; carries 1^(1) 0^(1) 1^(r-2) 0^(1) 1^(1) 0^(1) 1^(1) 0^(r-2) 1^(1) 0^(1) 1^(1)
step  7 ->  8: exact; carries 0^(1) 1^(2) 0^(r-3) 1^(1) 0^(1) 1^(2) 0^(1) 1^(r-3) 0^(2) 1^(1) 0^(1)
step  8 ->  9: exact; carries 1^(1) 0^(r-1) 1^(2) 0^(2) 1^(r-2) 0^(3) 1^(1)
step  9 -> 10: exact; carries 0^(2) 1^(r-2) 0^(1) 1^(2) 0^(1) 1^(2) 0^(r-4) 1^(3) 0^(2)
step 10 -> 11: exact; carries 0^(1) 1^(1) 0^(1) 1^(r-3) 0^(r+2) 1^(2) 0^(1) 1^(1) 0^(1)
step 11 -> 12: exact; carries 1^(3) 0^(r-3) 1^(2) 0^(1) 1^(1) 0^(1) 1^(r-3) 0^(2) 1^(3)
step 12 -> 13: exact; carries 0^(1) 1^(r-1) 0^(r+2) 1^(5) 0^(1)
step 13 -> 14: exact; carries 1^(1) 0^(4) 1^(r-5) 0^(1) 1^(1) 0^(1) 1^(2) 0^(1) 1^(1) 0^(r-5) 1^(1) 0^(4) 1^(1)
step 14 -> 15: exact; carries 0^(1) 1^(5) 0^(r-6) 1^(1) 0^(7) 1^(r-6) 0^(1) 1^(5) 0^(1)
step 15 -> 16: exact; carries 1^(2) 0^(4) 1^(r-2) 0^(1) 1^(r-2) 0^(4) 1^(2)
ALL 16 SYMBOLIC IDENTITIES VERIFIED FOR EVERY INTEGER r >= 20
```

The verifier represents each run length as an affine integer \(ar+b\). An affine expression is nonnegative for every \(r\ge20\) precisely when its slope is nonnegative 和 its value at \(20\) is nonnegative. Therefore its interval alignment checks are universal inequalities, rather than evaluations at a selected run length. Reversing a run word reverses its run order; aligning it with the original gives the exact symmetric column sums. The four carry cases above normalize each aligned interval, including the incoming bit of its first column. Splitting finite blocks into one-column intervals accounts for every boundary. Finally, equality is checked by aligning the entire computed output with the proposed next word. 这 establishes every displayed identity for every integer \(r\ge20\).

In ordinary algebra, the last row is equivalently
\[
T_{10}^{16}(W_r)
=1818666300\,10^{2r}+585455585\,10^r+2566927.
\tag{3}
\]

### 2.3. THEOREM — finite propagation of a zero band

Suppose an actual symmetric decimal column-sum word of length \(L\) satisfies
\[
q_i=0\qquad(a\le i\le z).
\]
The next folded word satisfies
\[
q'_i=0\qquad(a+1\le i\le z-1),
\tag{4}
\]
whenever that interval is nonempty.

**Proof with each overflow case.** A zero column always sends out carry zero, since \(\lfloor c_i/10\rfloor=0\) for \(c_i\in\{0,1\}\). Thus \(q_{i-1}=q_i=0\) forces \(c_i=0\) 和 \(e_i=0\).

If \(\gamma=0\), the next width is \(L\), 和
\[
q'_i=e_i+e_{L-1-i}.
\]
For \(i\in[a+1,z-1]\), the equalities \(q_{i-1}=q_i=0\) give \(e_i=0\). Setting \(j=L-1-i\), symmetry gives \(q_j=q_i=0\) 和 \(q_{j-1}=q_{i+1}=0\), so \(e_j=0\). Hence \(q'_i=0\).

If \(\gamma=1\), the next width is \(L+1\), 和 for the interior positions
\[
q'_i=e_i+e_{L-i}.
\]
For \(i\in[a+1,z]\), the equalities \(q_{i-1}=q_i=0\) again give \(e_i=0\). Setting \(j=L-i\), symmetry gives \(q_j=q_{i-1}=0\) 和 \(q_{j-1}=q_i=0\), so \(e_j=0\). Thus 这 overflow case preserves the larger interval \([a+1,z]\), in particular the interval in (4). The appended leading digit is outside the interior positions.

Induction gives a protected zero interval \([a+h,z-h]\) after \(h\) further steps, whenever nonempty. 这 deduction uses actual carries 和 allows an arbitrary sequence of overflows.

### 2.4. Completion of the obstruction proof

At time \(16\), the units-side fixed block in (3) 有 length \(7\), 和 the most significant fixed block 有 length \(8\). The low zero-digit run occupies positions \([7,r-1]\). Reflection of the high zero-digit run occupies \([8,r]\) in the low indexing. Their intersection yields
\[
q_i^{(16)}=0\qquad(8\le i\le r-1).
\]
For \(m=16+h\), (4) retains zeros on
\[
[8+h,r-1-h],
\]
an interval of length \(r-8-2h\). The bound \(r\ge2m-22=2h+10\) leaves at least \(2\) adjacent zero coefficients.

But direct folding gives, for every \(s\ge2\),
\[
q(W_s)=
1,0,9^{s-2},18,17,17,18,9^{s-2},0,1.
\tag{5}
\]
Its zero coefficients are isolated, including \(s=2\), when the runs of nines are empty. Therefore the words cannot agree for \(m\ge16\).

For \(1\le m\le15\), the exact table gives units digits
\[
1,2,4,8,6,7,5,6,3,4,8,7,8,7,8,
\]
each positive, whereas \(W_s\) ends in zero. The cases complete (2). A slightly sharper bound \(\max(20,2m-23)\) follows by retaining one zero, using width monotonicity to obtain \(s\ge r\), 和 comparing its index with the interval \([2,s-1]\) of nines in (5). The stated bound avoids that extra alignment argument.

## 3. THEOREM — arithmetic of noncritical complementary bulk symbols

Put \(N=b-1\), \(M=2N\), 和 let \(s\in\{1,\ldots,2N-1\}\setminus\{N\}\). A constant run with incoming carry \(\alpha\in\{0,1\}\) 有 the following complete normalization:

| Symbol | First output digit | Subsequent output digits | Outgoing carry |
|---|---:|---:|---:|
| \(s<N\) | \(s+\alpha\) | \(s\) | \(0\) |
| \(s=N,\alpha=0\) | \(N\) | \(N\) | \(0\) |
| \(s=N,\alpha=1\) | \(0\) | \(0\) | \(1\) |
| \(s>N\) | \(s+\alpha-b\) | \(s-N\) | \(1\) |

The first 和 last rows reset their carry in one column. Away from a run boundary, re-folding therefore yields
\[
F_b(s)=
\begin{cases}
2s,&s<N,\\
2s-2N,&s>N,
\end{cases}
\qquad F_b(s)\equiv2s\pmod{2N}.
\tag{6}
\]
Without overflow, the three equal neighboring column sums \(q_{i-1}=q_i=q_{i+1}=s\) guarantee saturation at the paired output positions \(i,L-1-i\). With overflow, the \(2\) equal column sums \(q_{i-1}=q_i=s\) guarantee saturation at positions \(i,L-i\): symmetry identifies their predecessors with the same \(2\) columns. Hence the interior interval trimmed by one position at each end obeys (6) in each case. 这 is a bulk statement with an explicit boundary reserve.

Write \(M=2^a u\), with \(u\) odd. A noncritical symbol lies on a periodic bulk cycle exactly when \(2^a\mid s\). Indeed, an \(m\)-step labeled return requires
\[
M\mid(2^m-1)s.
\tag{7}
\]
因为 \(2^m-1\) is odd, necessity follows. Conversely, if \(2^a\mid s\), multiplication by \(2\) permutes the nonzero residues after division by \(2^a\) modulo \(u\). The resulting orbit avoids \(N\), since \(v_2(N)=a-1\), 和 avoids zero. Its least labeled period is
\[
\operatorname{ord}_{M/\gcd(M,s)}(2).
\]
Consequently,
\[
\boxed{
\text{a noncritical periodic interior bulk exists}
\iff\operatorname{oddpart}(b-1)>1.
}
\tag{8}
\]
For an unordered complementary pair, replace the congruence \(2^m\equiv1\) by \(2^m\equiv\pm1\) modulo \(M/\gcd(M,s)\).

| Base | Periodic noncritical bulk | Implication for the requested comparison |
|---|---|---|
| \(2\) | Empty interior alphabet | The binary construction uses the critical symbol |
| \(2^k,\ k\ge2\) | Exists, since \(b-1\) is odd 和 exceeds \(1\) | Bulk compatibility alone is weaker than a return construction |
| \(10\) | \(2\to4\to8\to16\to14\to10\to2\), 和 \(6\leftrightarrow12\) | Decimal passes the bulk criterion |
| \(11\) | \(4\to8\to16\to12\to4\) | Labeled period \(4\) |
| \(17\) | Absent, since \(b-1=16\) | The known critical-band example uses a different mechanism |
| \(20\) | Labeled period \(18\) | Bulk arithmetic is compatible |
| \(26\) | Labeled periods \(4,20\) | Bulk arithmetic is compatible |

The decimal cycles in 这 table already appear in the repository. The base-general derivation clarifies the scope; it supplies neither returning interfaces nor an accepted decimal return certificate.

## 4. THEOREM / source comparison — the regular reset condition 和 the sporadic bases

Appendix A reconstructs the regular family with complete carry tables. Its result is
\[
\boxed{
b=2^\ell\quad\Longrightarrow\quad
T_b^{2\ell+2}(W_b(r))=W_b(r+1)\quad(r\ge2).
}
\tag{9}
\]
Every intermediate phase is nonpalindromic. The exact regular doubling/reset scheme reaches its clean reset iff \(b=2^\ell\): its parameter starts at \(a=1\), doubles while \(2a<b\), 和 resets at \(2a=b\). Base \(10\) instead takes \(a=1,2,4,8\), yielding
\[
T_{10}^5(W_{10}(r))=175\,9^{r-2}\,3224\,0^{r-2}\,66.
\tag{10}
\]
The stronger theorem in Section 2 follows 这 overshoot through subsequent phases 和 excludes every uniform fixed-time return of 这 family.

The opened primary-source reproductions of David Seal's January 1996 post give the regular family 和 explicit sporadic templates for bases \(11,17,26\). The base-\(20\) entry reports a seed exceeding 200 digits without displaying it. The source 也 flags possible transcription errors; Section 7 therefore checks the displayed words directly. [S1, S2]

| Bases | Regular dyadic reset | Explicit source template used in the checks |
|---|---|---|
| \(2^\ell\) | Closes, with period \(2\ell+2\) | \(W_b(n+2)\) |
| \(11\) | Fails | Sporadic period \(6\) |
| \(17\) | Fails | Sporadic period \(6\) |
| \(20\) | Fails | Seed omitted from the opened source |
| \(26\) | Fails | Sporadic period \(4\) |

**THEOREM, from the explicit source words.** The displayed growing opposite digit runs for \(2^\ell,11,17,26\) are \(b-1\) 和 \(0\); reflected interior positions therefore 有 \(q=b-1\). At 这 column sum, incoming carry \(0\) produces digit \(b-1\) 和 outgoing carry \(0\), while incoming carry \(1\) produces digit \(0\) 和 outgoing carry \(1\). Base \(10\) 有 这 same carry transfer. Thus a blanket obstruction based on the noncritical bulk map lacks support from the sporadic examples. The base-\(20\) mechanism remains unaudited here 因为 its seed was omitted. [S1, S2]

## 5. IDEA — relation to the repository 和 the sharp remaining question

At the inspected commit, `lean/P196/Agent2SaturatedProfile/TemplateStep.lean` defines
\[
B\,c^g\,A\,(18-c)^h\,C\,(18-c)^h\,
A^{\mathrm{rev}}\,c^g\,B^{\mathrm{rev}},
\qquad1\le c\le17,\quad c\ne9.
\]
The exact-return checker 也 requires finite-block identities, valid length updates, 和 failure of its palindrome predicate. The present report leaves the checker conditions unresolved. The new obstruction concerns the separate critical-band family \(W_{10}(r)\), rather than the full checker domain.

Existing source results were checked for overlap before writing 这 report: decimal phase cycles appear in the saturated-profile modules; charge 和 period restrictions occur in `CertificateCharge.lean`, `CertificateConsequences.lean`, the `Agent412Agent412` draft modules, 和 `Agent112SmallPeriodObstruction/SmallPeriodObstruction.lean`. The restrictions are prior work. The report contains written proofs; Lean formalization remains open. [R1–R4]

**IDEA — sharp open question.** Do there exist bounded digit words \(A,M,C\), a positive integer \(g\), 和 a finite period \(p\), such that
\[
V(r)=A\,9^r\,M\,0^r\,C,
\qquad T_{10}^p(V(r))=V(r+g)
\]
for every sufficiently large \(r\), with every intermediate phase asymmetric? For 这 restricted question, the new obstruction identifies a concrete failure to avoid: protected zero column-sum bands that persist inside the would-be returning critical bands. A successful construction must control the entire interface 和 center evolution through its return, including 那 possible change of bulk symbol.

## 6. Exact symbolic verification code 和 output

Save 这 first code block as `symbolic_certificate.py` 和 run `python3 symbolic_certificate.py`. It establishes the sixteen universal identities by affine arithmetic, rather than scanning seed integers. Its complete output is printed in Section 2.2. 这 is a written finite symbolic certificate with an executable checker; Lean formalization remains open.

```python
"""Exact affine-run verification for all integer r >= 20; no sampling."""
from dataclasses import dataclass

RMIN = 20

@dataclass(frozen=True)
class Aff:
    a: int
    b: int
    def __add__(self, other): return Aff(self.a + other.a, self.b + other.b)
    def __sub__(self, other): return Aff(self.a - other.a, self.b - other.b)
    def at(self, r): return self.a * r + self.b

ZERO, ONE = Aff(0,0), Aff(0,1)

def nonnegative(x):
    return x.a >= 0 and x.at(RMIN) >= 0

def compare(x, y):
    if x == y: return 0
    d = x-y
    if nonnegative(d): return 1
    if nonnegative(ZERO-d): return -1
    raise AssertionError(("order changes on the claimed domain",x,y))

def append(w,d,n):
    assert nonnegative(n), n
    if n == ZERO: return
    if w and w[-1][0] == d:
        w[-1] = (d,w[-1][1]+n)
    else:
        w.append((d,n))

def fixed(w,s):
    for d in s: append(w,int(d),ONE)

# MSF words: H, p^(r-k), M, q^(r-k), L.
PATTERNS = [
    ("10",9,0,"89",0,""),
    ("11",0,2,"9888",9,"01"),
    ("22",0,2,"8777",9,"12"),
    ("44",0,2,"6555",9,"34"),
    ("88",0,2,"2111",9,"78"),
    ("175",9,2,"3224",0,"66"),
    ("836",0,3,"35463",9,"637"),
    ("1572",9,3,"71917",0,"275"),
    ("7293",0,4,"691096",9,"3026"),
    ("13497",0,4,"381292",9,"6953"),
    ("49466",9,5,"3303123",0,"76384"),
    ("97833",9,5,"6516157",0,"42878"),
    ("185658",0,5,"4032313",9,"76757"),
    ("943337",9,6,"35355354",0,"833338"),
    ("1776675",9,6,"80710708",0,"566687"),
    ("9643326",0,7,"787727797",9,"6333458"),
    ("18186663",0,7,"585455585",0,"2566927"),
]

def word(p):
    H,d,k,M,e,L = p
    out=[]
    fixed(out,H);append(out,d,Aff(1,-k));fixed(out,M)
    append(out,e,Aff(1,-k));fixed(out,L)
    return out

def aligned(a,b):
    a=list(a);b=list(b);i=j=0
    while i<len(a) and j<len(b):
        x,n=a[i];y,m=b[j];z=compare(n,m)
        length=n if z<=0 else m
        yield x,y,length
        if z<=0:i+=1
        else:a[i]=(x,n-length)
        if z>=0:j+=1
        else:b[j]=(y,m-length)
    assert i==len(a) and j==len(b)

def reverse_add(w):
    # w is MSF. The paired traversal below starts at the units column.
    out=[];carries=[];c=0
    for x,y,n in aligned(w[::-1],w):
        q=x+y
        if q<9:
            append(out,q+c,ONE);append(out,q,n-ONE)
            c=0
        elif q==9:
            append(out,9 if c==0 else 0,n)
        else:
            append(out,q+c-10,ONE);append(out,q-9,n-ONE)
            c=1
        append(carries,c,n)
    if c:append(out,1,ONE)
    return out[::-1],carries

def equal(a,b):
    return all(x==y for x,y,n in aligned(a,b))

def show_aff(n):
    if n.a==0:return str(n.b)
    s="r" if n.a==1 else str(n.a)+"r"
    return s+(f"{n.b:+d}" if n.b else "")

if __name__ == "__main__":
    for t in range(16):
        got,cs=reverse_add(word(PATTERNS[t]))
        assert equal(got,word(PATTERNS[t+1])),t
        print(f"step {t:2d} -> {t+1:2d}: exact; carries "+" ".join(f"{d}^({show_aff(n)})" for d,n in cs))
    print("ALL 16 SYMBOLIC IDENTITIES VERIFIED FOR EVERY INTEGER r >= 20")
```

## 7. Numerical checks: explicit families for 1000 steps

The following code checks the general carry identities on 3162 small parameter cases, then runs each explicit construction for 1000 ordinary reverse-add steps. The small checks test the symbolic formulas; they are supplementary to the proofs. At each completed period, the exact proposed template equality is tested. The palindrome test covers every positive iterate through step 1000. Additional decimal checks use \(W_{10}(8)\), \(W_{10}(20)\), 和 \(W_{10}(40)\); the observations are finite with infinite-orbit behavior left open.

Save as `verify_known.py` 和 run `python3 verify_known.py`.

```python
#!/usr/bin/env python3
"""Small independent checks of explicit identities; no seed search."""

CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def parse(s):
    return [CHARS.index(x) for x in s]


def step(ds, base):
    carry = 0
    out = []
    for left, right in zip(reversed(ds), ds):
        carry, digit = divmod(left + right + carry, base)
        out.append(digit)
    if carry:
        out.append(carry)
    return out[::-1]


def W(base, k):
    B = base - 1
    return [1, 0] + [B] * k + [base - 2, B] + [0] * k


def W_tilde(base, k):
    return W(base, k) + [0]


def P(base, a, r):
    B = base - 1
    return ([a, a] + [0] * r + [base - a] + [base - a - 1] * 3
            + [B] * r + [a - 1, a])


def Q(base, a, r):
    B = base - 1
    h = int(2 * a >= base)
    middle = [base - a - h, base - 2 * a - 1 + base * h, base - a - 1]
    return [a, a] + [0] * r + middle + [B] * r + [a - 1, a]


def P_overshoot(base, a, r):
    B = base - 1
    z = 2 * a - base
    u = 2 * base - 2 * a
    return ([1, z + 1, z - 1] + [B] * r
            + [u - 1, u - 2, u - 2, u] + [0] * r + [z, z])


def Q_overshoot(base, a, r):
    B = base - 1
    z = 2 * a - base
    K = 2 * base - 2 * a - 2
    M = 4 * base - 4 * a - 2
    mu = M // base
    return ([1, z + 1, z - 1] + [B] * r
            + [K + mu, M - base * mu, K + 1] + [0] * r + [z, z])


def check_identities():
    checks = 0
    for base in range(2, 33):
        for r in (0, 1, 3):
            assert step(W(base, r + 2), base) == P(base, 1, r)
            assert step(W_tilde(base, r + 1), base) == Q(base, 1, r)
            checks += 2
            for a in range(1, base):
                if 2 * a < base:
                    p_target = P(base, 2 * a, r)
                    q_target = Q(base, 2 * a, r)
                elif 2 * a == base:
                    p_target = W_tilde(base, r + 2)
                    q_target = W(base, r + 2)
                else:
                    p_target = P_overshoot(base, a, r)
                    q_target = Q_overshoot(base, a, r)
                assert step(P(base, a, r), base) == p_target, (base, a, r, "P")
                assert step(Q(base, a, r), base) == q_target, (base, a, r, "Q")
                checks += 2
    print(f"Explicit identity spot checks: {checks}; failures: 0")


def sporadic(base, n):
    if base == 11:
        return parse("1246277" + "A" * n
                     + "A170352495681825A5026571A506181864A5143171"
                     + "0" * n + "0872542")
    if base == 17:
        return parse("10023AB83E3B983CFGEC556G4G010" + "0" * n
                     + "0FGCG10FG505GF020CGF" + "G" * n
                     + "GG11G4F655DDGGB299B3D38BB320G")
    if base == 26:
        return parse("1N5ELA6C" + "P" * n + "P6E7" + "0" * n + "0D59ME5N")
    raise ValueError(base)


def test_1000(base, period, template):
    ds = template(2)
    start_len = len(ds)
    failed_returns, palindromes, returns = [], [], 0
    for t in range(1, 1001):
        ds = step(ds, base)
        if ds == ds[::-1]:
            palindromes.append(t)
        if t % period == 0:
            returns += 1
            if ds != template(2 + t // period):
                failed_returns.append(t)
    print(f"base={base} period={period} steps=1000 start_len={start_len} "
          f"final_len={len(ds)} return_checks={returns} "
          f"failed_returns={failed_returns} palindromes={palindromes}")


def decimal_counterexample():
    ds = W(10, 8)
    palindromes = []
    clean_returns = []
    for t in range(1, 1001):
        ds = step(ds, 10)
        if t == 5:
            print("decimal W(10,8), t=5:", "".join(map(str, ds)))
            assert ds == P_overshoot(10, 8, 6)
        if ds == ds[::-1]:
            palindromes.append(t)
        if len(ds) >= 8 and len(ds) % 2 == 0:
            k = (len(ds) - 4) // 2
            if ds == W(10, k):
                clean_returns.append((t, k))
    print(f"decimal W(10,8): steps=1000 final_len={len(ds)} "
          f"palindromes={palindromes} exact_W_returns={clean_returns}")


if __name__ == "__main__":
    check_identities()
    for exponent in range(1, 6):
        base = 2 ** exponent
        test_1000(base, 2 * exponent + 2, lambda n, b=base: W(b, n + 2))
    for base, period in ((11, 6), (17, 6), (26, 4)):
        test_1000(base, period, lambda n, b=base: sporadic(b, n))
    decimal_counterexample()

    # Additional decimal instances within the symbolic theorem's domain.
    for r in (20, 40):
        ds = W(10, r)
        palindromes, returns = [], []
        for t in range(1, 1001):
            ds = step(ds, 10)
            if t == 16:
                target = parse("18186663" + "0" * (r-7) + "585455585"
                               + "0" * (r-7) + "2566927")
                assert ds == target
                q = [x+y for x, y in zip(ds[::-1], ds)]
                assert q[8:r] == [0] * (r-8)
            if ds == ds[::-1]:
                palindromes.append(t)
            if len(ds) % 2 == 0:
                s = (len(ds)-4) // 2
                if s >= 2 and ds == W(10, s):
                    returns.append((t, s))
        print(f"decimal W(10,{r}): steps=1000 final_len={len(ds)} "
              f"palindromes={palindromes} exact_W_returns={returns}")
```

Exact output:

```text
Explicit identity spot checks: 3162; failures: 0
base=2 period=4 steps=1000 start_len=12 final_len=512 return_checks=250 failed_returns=[] palindromes=[]
base=4 period=6 steps=1000 start_len=12 final_len=345 return_checks=166 failed_returns=[] palindromes=[]
base=8 period=8 steps=1000 start_len=12 final_len=262 return_checks=125 failed_returns=[] palindromes=[]
base=16 period=10 steps=1000 start_len=12 final_len=212 return_checks=100 failed_returns=[] palindromes=[]
base=32 period=12 steps=1000 start_len=12 final_len=178 return_checks=83 failed_returns=[] palindromes=[]
base=11 period=6 steps=1000 start_len=60 final_len=393 return_checks=166 failed_returns=[] palindromes=[]
base=17 period=6 steps=1000 start_len=82 final_len=415 return_checks=166 failed_returns=[] palindromes=[]
base=26 period=4 steps=1000 start_len=24 final_len=524 return_checks=250 failed_returns=[] palindromes=[]
decimal W(10,8), t=5: 175999999322400000066
decimal W(10,8): steps=1000 final_len=440 palindromes=[] exact_W_returns=[]
decimal W(10,20): steps=1000 final_len=459 palindromes=[] exact_W_returns=[]
decimal W(10,40): steps=1000 final_len=507 palindromes=[] exact_W_returns=[]
```

For the sporadic bases \(11,17,26\), 这 section supplies source-transcription checks, rather than new universal parameter proofs of their historical constructions. The power-of-2 result 有 the complete proof in Appendix A. The decimal obstruction 有 the complete proof in Section 2. The finite decimal trajectories yield neither a Lychrel witness nor a counterexample to eventual palindrome formation.

## Appendix A. Complete general-base carry proof for the regular family


Write digits most-significant first. A superscript on a digit denotes repetition, including an empty word when its exponent is 0. Let \(b\ge2\), \(B=b-1\), 和 define

\[
W_b(k)=10B^k(b-2)B0^k,\qquad
\widetilde W_b(k)=10B^k(b-2)B0^{k+1}.
\]

For \(1\le a<b\), \(r\ge0\), define

\[
P_a(r)=aa0^r(b-a)(b-a-1)^3B^r(a-1)a.
\]

Let \(h_a=0\) when \(2a<b\), 和 \(h_a=1\) when \(2a\ge b\). Define

\[
Q_a(r)=aa0^r(b-a-h_a)(b-2a-1+bh_a)(b-a-1)B^r(a-1)a.
\]

Every parenthesized expression is one digit. The displayed expressions 都 lie in \([0,b-1]\). The following identities hold:

\[
T(W_b(k))=P_1(k-2)\quad(k\ge2),
\qquad
T(\widetilde W_b(k))=Q_1(k-1)\quad(k\ge1).
\]

When \(2a<b\),

\[
T(P_a(r))=P_{2a}(r),\qquad T(Q_a(r))=Q_{2a}(r).
\]

When \(2a=b\),

\[
T(P_a(r))=\widetilde W_b(r+2),\qquad
T(Q_a(r))=W_b(r+2).
\]

When \(2a>b\), put \(z=2a-b\), \(u=2b-2a\), \(K=u-2\), \(M=2u-2\), 和 \(\mu=\lfloor M/b\rfloor\in\{0,1\}\). Then

\[
T(P_a(r))=1(z+1)(z-1)B^r(u-1)(u-2)^2u0^rzz,
\]

\[
T(Q_a(r))=1(z+1)(z-1)B^r(K+\mu)(M-b\mu)(K+1)0^rzz.
\]

Consequently, for \(b=2^\ell\), \(\ell\ge1\),

\[
T^{2\ell+2}(W_b(k))=W_b(k+1)\qquad(k\ge2).
\]

Every intermediate word is nonpalindromic. The exact regular \(2\)-stage doubling/reset mechanism reaches its reset branch from \(a=1\) iff \(b\) is a power of 2.

The last statement concerns the specified phase mechanism. Later returns of a non-power-of-2 seed through other phases remain open at 这 stage of the argument.

### A.1. Complete carry verification

Carries run from the units end. Every table below is therefore read top to bottom from units toward the most-significant end. A row labelled \(B^r\) means \(r\) consecutive copies of the stated transition. If \(r=0\), omit 那 row; its incoming 和 outgoing carries coincide, so subsequent rows 都 remain valid. When the last carry is 1, append leading digit 1.

### Starting \(W_b(k)\), \(k=r+2\)

Its symmetric column-sum word, read from either end, is

\[
[1,0,B^r,2B,2B-1,2B-1,2B,B^r,0,1].
\]

| Column sum | Incoming carry | Output digit | Outgoing carry |
|---|---:|---:|---:|
| \(1\) | 0 | 1 | 0 |
| \(0\) | 0 | 0 | 0 |
| \(B^r\) | 0 | \(B^r\) | 0 |
| \(2B\) | 0 | \(b-2\) | 1 |
| \(2B-1\) | 1 | \(b-2\) | 1 |
| \(2B-1\) | 1 | \(b-2\) | 1 |
| \(2B\) | 1 | \(B\) | 1 |
| \(B^r\) | 1 | \(0^r\) | 1 |
| \(0\) | 1 | 1 | 0 |
| \(1\) | 0 | 1 | 0 |

Reverse the output column to obtain \(P_1(r)\). The arithmetic equalities include \(b=2\).

### Starting \(\widetilde W_b(k)\), \(k=r+1\)

The symmetric column sums are

\[
[1,0,B^r,2B,2B-2,2B,B^r,0,1].
\]

The first rows \(1,0,B^r\) output \(1,0,B^r\), with carry 0. The near \(2B\) column outputs \(b-2\) with carry 1. The remaining central columns 有 the following complete split:

| Base | Column sum | Incoming carry | Output digit | Outgoing carry |
|---|---|---:|---:|---:|
| \(b\ge3\) | \(2B-2\) | 1 | \(b-3\) | 1 |
| \(b\ge3\) | \(2B\) | 1 | \(B\) | 1 |
| \(b=2\) | \(2B-2=0\) | 1 | 1 | 0 |
| \(b=2\) | \(2B=2\) | 0 | 0 | 1 |

In each base case, the remaining \(B^r\) run outputs \(0^r\) with carry 1; column 0 outputs 1 with carry 0; final column 1 outputs 1 with carry 0. For \(b\ge3\), the middle output is \((b-1)(b-3)(b-2)\). For \(b=2\), it is \(010\). The expressions give exactly the \(2\) cases of \(Q_1(r)\).

### \(P_a(r)\): column sums

Set \(H=2b-2a-1\), \(G=2b-2a-2\). The column sums are

\[
[2a,2a-1,B^r,H,G,G,H,B^r,2a-1,2a].
\]

#### Case \(2a<b\)

| Column sum | Incoming | Output | Outgoing |
|---|---:|---:|---:|
| \(2a\) | 0 | \(2a\) | 0 |
| \(2a-1\) | 0 | \(2a-1\) | 0 |
| \(B^r\) | 0 | \(B^r\) | 0 |
| \(H\) | 0 | \(b-2a-1\) | 1 |
| \(G\) | 1 | \(b-2a-1\) | 1 |
| \(G\) | 1 | \(b-2a-1\) | 1 |
| \(H\) | 1 | \(b-2a\) | 1 |
| \(B^r\) | 1 | \(0^r\) | 1 |
| \(2a-1\) | 1 | \(2a\) | 0 |
| \(2a\) | 0 | \(2a\) | 0 |

The result is \(P_{2a}(r)\).

#### Case \(2a=b\)

Here \(H=B\), \(G=b-2\).

| Column sum | Incoming | Output | Outgoing |
|---|---:|---:|---:|
| \(b\) | 0 | 0 | 1 |
| \(B\) | 1 | 0 | 1 |
| \(B^r\) | 1 | \(0^r\) | 1 |
| \(B\) | 1 | 0 | 1 |
| \(b-2\) | 1 | \(B\) | 0 |
| \(b-2\) | 0 | \(b-2\) | 0 |
| \(B\) | 0 | \(B\) | 0 |
| \(B^r\) | 0 | \(B^r\) | 0 |
| \(B\) | 0 | \(B\) | 0 |
| \(b\) | 0 | 0 | 1 |

Append leading 1. The resulting word is \(10B^{r+2}(b-2)B0^{r+3}\).

#### Case \(2a>b\)

Here \(H=u-1\), \(G=u-2\), \(z\ge1\).

| Column sum | Incoming | Output | Outgoing |
|---|---:|---:|---:|
| \(2a\) | 0 | \(z\) | 1 |
| \(2a-1\) | 1 | \(z\) | 1 |
| \(B^r\) | 1 | \(0^r\) | 1 |
| \(u-1\) | 1 | \(u\) | 0 |
| \(u-2\) | 0 | \(u-2\) | 0 |
| \(u-2\) | 0 | \(u-2\) | 0 |
| \(u-1\) | 0 | \(u-1\) | 0 |
| \(B^r\) | 0 | \(B^r\) | 0 |
| \(2a-1\) | 0 | \(z-1\) | 1 |
| \(2a\) | 1 | \(z+1\) | 1 |

Append leading 1. 这 yields the overshoot formula. In particular, its final digit \(z\) is positive, whereas \(\widetilde W\) ends in 0.

### \(Q_a(r)\), case \(2a<b\)

Here \(h_a=0\). Set \(H=2b-2a-1\), \(J=2b-4a-2\). The column sums are

\[
[2a,2a-1,B^r,H,J,H,B^r,2a-1,2a].
\]

The initial \(2a,2a-1,B^r\) columns output \(2a,2a-1,B^r\) with carry 0. The near \(H\) column outputs \(b-2a-1\) with carry 1. The central split is:

| Condition | Column sum | Incoming | Output | Outgoing |
|---|---|---:|---:|---:|
| \(4a<b\) | \(J\) | 1 | \(b-4a-1\) | 1 |
| \(4a<b\) | \(H\) | 1 | \(b-2a\) | 1 |
| \(4a\ge b\) | \(J\) | 1 | \(2b-4a-1\) | 0 |
| \(4a\ge b\) | \(H\) | 0 | \(b-2a-1\) | 1 |

The next \(B^r\) run outputs \(0^r\) with carry 1; column \(2a-1\) outputs \(2a\) with carry 0; column \(2a\) outputs \(2a\) with carry 0. For \(4a<b\), the middle word is \((b-2a)(b-4a-1)(b-2a-1)\). For \(4a\ge b\), it is \((b-2a-1)(2b-4a-1)(b-2a-1)\). The expressions give exactly the \(2\) definitions of \(Q_{2a}(r)\).

### \(Q_a(r)\), case \(2a=b\)

Now its middle digits are \((a-1)B(a-1)\), giving column sums

\[
[b,B,B^r,b-2,2B,b-2,B^r,B,b].
\]

| Column sum | Incoming | Output | Outgoing |
|---|---:|---:|---:|
| \(b\) | 0 | 0 | 1 |
| \(B\) | 1 | 0 | 1 |
| \(B^r\) | 1 | \(0^r\) | 1 |
| \(b-2\) | 1 | \(B\) | 0 |
| \(2B\) | 0 | \(b-2\) | 1 |
| \(b-2\) | 1 | \(B\) | 0 |
| \(B^r\) | 0 | \(B^r\) | 0 |
| \(B\) | 0 | \(B\) | 0 |
| \(b\) | 0 | 0 | 1 |

Append leading 1. The output is \(W_b(r+2)\).

### \(Q_a(r)\), case \(2a>b\)

Here the column sums are

\[
[2a,2a-1,B^r,K,M,K,B^r,2a-1,2a].
\]

| Column sum | Incoming | Output | Outgoing |
|---|---:|---:|---:|
| \(2a\) | 0 | \(z\) | 1 |
| \(2a-1\) | 1 | \(z\) | 1 |
| \(B^r\) | 1 | \(0^r\) | 1 |
| \(K\) | 1 | \(K+1\) | 0 |
| \(M\) | 0 | \(M-b\mu\) | \(\mu\) |
| \(K\) | \(\mu\) | \(K+\mu\) | 0 |
| \(B^r\) | 0 | \(B^r\) | 0 |
| \(2a-1\) | 0 | \(z-1\) | 1 |
| \(2a\) | 1 | \(z+1\) | 1 |

Each value of \(\mu\) is covered by the exact quotient/remainder definition; \(0\le K+\mu<b\). Append leading 1.

### A.2. THEOREM: iteration 和 nonpalindromicity

If \(b=2^\ell\), the phases are

\[
W_b(k)\to P_1(k-2)\to P_2(k-2)\to\cdots\to P_{b/2}(k-2)
\to\widetilde W_b(k)
\to Q_1(k-1)\to\cdots\to Q_{b/2}(k-1)\to W_b(k+1).
\]

The first stage takes \(\ell+1\) steps 和 the second stage takes \(\ell+1\) steps. Words \(W\) 和 \(\widetilde W\) begin with 1 和 end with 0. Words \(P_a\) 和 \(Q_a\) 有 second digit \(a\) 和 penultimate digit \(a-1\). Hence every displayed word fails the palindrome test. Iterating the identities establishes an infinite nonpalindromic orbit.

Conversely, starting at \(P_1\), the parameter is doubled until the first \(2a\ge b\). Equality occurs exactly when \(b\) is a power of 2. For every other base, \(2a>b\), 和 the overshoot formula 有 positive units digit. Thus it differs from the prescribed \(\widetilde W\) reset. The same arithmetic condition governs the \(Q\) stage. Later orbits after leaving the displayed phases remain open in 这 argument.

### A.3. THEOREM: the first decimal overshoot

For \(b=10\), the successive parameters are \(a=1,2,4,8\). The first reset attempt is therefore the overshoot case \(a=8\), with \(z=6\), \(u=4\). For every \(k\ge2\),

\[
T^5(W_{10}(k))=175\,9^{k-2}\,3224\,0^{k-2}\,66.
\]

这 differs from \(\widetilde W_{10}(k)\), whose units digit is 0. For \(k=8\), the exact fifth iterate is `175999999322400000066`.

## Sources opened 和 repository provenance

- **S1.** David Seal, January 1996 `rec.puzzles` post, reproduced at [p196.org](https://www.p196.org/html/papers1.html). Regular family 和 sporadic starting words; base-20 transcription omitted.
- **S2.** [MathPages reproduction with representative cycles](https://www.mathpages.com/home/dseal.htm).
- **R1.** [Exact template transition](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean).
- **R2.** [Return checker](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean).
- **R3.** [Existing charge identities](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateCharge.lean) 和 [existing certificate consequences](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateConsequences.lean).
- **R4.** [Existing unrestricted small-period obstructions](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent112SmallPeriodObstruction/SmallPeriodObstruction.lean).
