# REPORT_202 — Arithmetic conditions for complementary bands

Agent #202 · Direction 2 · 2026-10-22

## Answer in one paragraph

**THEOREM / outcome.** Decimal Lychrel existence remains unresolved by 这个 report. A complete obstruction does hold for the class with exactly 2 complementary nonneutral column-sum values throughout the entire word: in base $b\ge3$, every such profile leaves 那 class within $\lceil\log_2 b\rceil$ reverse 和 add steps, 和 这个 bound is sharp; the decimal bound is 4. The only transitions remaining inside 那 class come from words $(c,H,H,c)^r$, where $H=2(b-1)-c$, 和 follow the exact affine rule $c\mapsto2c+1$ until a neutral value or an overflowing interface appears. For long bands with arbitrary bounded interface blocks, the bulk condition instead 是 multiplication by 2 modulo $2(b-1)$; decimal admits a 6-cycle 和 a 2-cycle, so 这 arithmetic supplies no universal decimal obstruction. The regular power-of-2 construction 有 a different exact condition: its doubling phase must hit $2t=b$; decimal overshoots, 和 the smallest displayed decimal transplant reaches a palindrome at step 10. The opened base-11, base-17, 和 base-26 examples use neutral column-sum bands, outside the nonneutral ansatz. Complete carry proofs, source links, executable checks, actual outputs, 和 the remaining global question follow.

## Status, scope, 和 notation

**THEOREM** labels below denote complete paper proofs. No new **LEAN-VERIFIED** claim is made. The repository changes consist of 这个 report 和 its catalog link; no Lean source or certificate instance is added.

Throughout Sections 1–4, digits 和 column sums are indexed from the units end. Set
$$
B=b-1,\qquad M=2B,\qquad
q_i=d_i+d_{L-1-i}.
$$
A positive canonical numeral gives a symmetric word $q$, with $0\le q_i\le M$, $q_0>0$, 和 an even middle coefficient when $L$ is odd. The exact addition uses
$$
\kappa_0=0,\qquad
\kappa_{i+1}=\left\lfloor\frac{q_i+\kappa_i}{b}\right\rfloor,\qquad
e_i=q_i+\kappa_i-b\kappa_{i+1}.
\tag{1}
$$
The carry belongs to $\{0,1\}$. If $\kappa_L=0$, then $L'=L$; if $\kappa_L=1$, append $e_L=1$ 和 use $L'=L+1$. The next column-sum word 是
$$q'_i=e_i+e_{L'-1-i}.$$
这 includes the change of reflection axis after overflow.

A **pure complementary profile** means a symmetric word whose set of occurring values is exactly
$$
\{c,H\},\qquad 1\le c<B,\qquad H=2B-c.
\tag{2}
$$
The values 都 must occur. In particular, no boundary or center coefficients outside 这 pair are allowed. Write $\mathcal P_b$ for 这个 class. It is narrower than the repository template, which permits arbitrary bounded exterior, interface, 和 center blocks.

The term **bulk** means positions remaining inside a long constant run, away from the bounded interface regions. A bulk-cycle claim concerns these interior values only.

## 1. THEOREM — Exact re-folding for globally nonneutral words

Assume $q_i\ne B$ at every position. Define
$$
x_i=\mathbf1_{\{q_i>B\}},\qquad p_i=q_i-Bx_i.
$$
Symmetry gives $x_i=x_{L-1-i}$. Every carry leaving a column is determined by 那 column:
$$\kappa_{i+1}=x_i.$$

### Proof of the carry assertion

If $q_i<B$, then $q_i\le b-2$. For either entering carry,
$q_i+\kappa_i\le b-1$, so the outgoing carry is 0.

If $q_i>B$, then $b\le q_i\le2b-2$. For either entering carry,
$b\le q_i+\kappa_i\le2b-1$, so the outgoing carry is 1.

Consequently,
$$
e_0=q_0-bx_0,\qquad
e_i=q_i-bx_i+x_{i-1}\quad(1\le i<L).
\tag{3}
$$
The final carry 是 $x_{L-1}=x_0$.

### Case A: no overflow, $x_0=0$

Pad with $x_{-1}=x_L=0$. Equation (3), symmetry, 和 the unchanged reflection axis give, at every position including the 2 endpoints,
$$
\boxed{q'_i=2q_i-2b\,x_i+x_{i-1}+x_{i+1}.}
\tag{4}
$$
At $i=0$ 这是 $q'_0=2q_0+x_1$; the opposite endpoint gives the same value. For $L=1$, both padded neighbors are 0, giving $q'_0=2q_0$.

### Case B: overflow, $x_0=1$

The new endpoint pairs with the appended leading digit:
$$
\boxed{q'_0=q'_L=q_0-b+1=p_0.}
\tag{5}
$$
For $1\le i\le L-1$, the reflected partner is $L-i$. Since
$q_{L-i}=q_{i-1}$, $x_{L-i}=x_{i-1}$, 和 $x_{L-i-1}=x_i$,
$$
\begin{aligned}
q'_i
&=(q_i-bx_i+x_{i-1})
 +(q_{i-1}-bx_{i-1}+x_i)\\
&=q_i+q_{i-1}-(b-1)(x_i+x_{i-1})\\
&=\boxed{p_i+p_{i-1}.}
\end{aligned}
\tag{6}
$$
For $L=1$, the interior range is empty 和 (5) supplies the entire new word.

At a complementary interface the values of $p$ are
$$p(c)=c,\qquad p(H)=B-c.$$
Thus every such interface in an overflowing step creates exactly the neutral coefficient
$$\boxed{c+(B-c)=B.}\tag{7}$$

## 2. THEOREM — Complete characterization of pure-to-pure transitions

Let $q\in\mathcal P_b$. Its successor $q'$ belongs to $\mathcal P_b$ **exactly when** there are integers $r\ge1$ 和 $1\le c<B$ such that
$$
q=(c,H,H,c)^r,\qquad H=2B-c,\qquad 2c+1\ne B.
\tag{8}
$$
In 那 case there is no overflow, 和 the full successor is
$$
\boxed{
q'=(2c+1,\ 2B-2c-1,\ 2B-2c-1,\ 2c+1)^r.
}
\tag{9}
$$
The new endpoints may be the high member of their pair.

### Necessity: the overflowing case

If $q_0=H$, the step overflows. 因为 both $c$ 和 $H$ occur, at least one adjacent pair changes value. Equation (7) gives a coefficient $B$ in $q'$. A member of $\mathcal P_b$ 没有 $B$. Therefore an overflowing pure profile cannot 有 a pure successor.

### Necessity: the nonoverflowing case

It remains to consider $q_0=c$, so $x_0=x_{L-1}=0$. Let $j$ be the first high position. It exists 因为 $q$ is nonconstant, 和 $j\ge1$. At $i=j-1$, both $x_i$ 和 $x_{i-1}$ are 0, while $x_{i+1}=1$; for $j=1$, the left value is the padded $x_{-1}=0$. Equation (4) gives
$$q'_{j-1}=2c+1,$$
an odd coefficient.

The members of a complementary output pair sum to $2B$, an even number, so they 有 the same parity. If $q'$ uses exactly 那 pair, every coefficient of $q'$ must therefore be odd. Equation (4) then requires
$$
x_{i-1}+x_{i+1}\equiv1\pmod2
\quad(0\le i<L).
$$
The summands 都 are bits, so the exact relation is
$$x_{i+1}=1-x_{i-1}.\tag{10}$$
Starting from $x_{-1}=x_0=0$, the recurrence forces
$$
x_0,x_1,x_2,x_3,x_4,\ldots
=0,1,1,0,0,1,1,0,\ldots.
$$
The right endpoint conditions are $x_{L-1}=x_L=0$. In 这个 period-4 sequence, consecutive zeros occur at indices congruent to $(3,0)$ modulo 4. Hence $L=4r$. 这 excludes every odd length 和 length 2 without suppressing a boundary case. The resulting input 是 precisely $(c,H,H,c)^r$.

### Sufficiency 和 the neutral exception

For the forced bit pattern, $x_{i-1}+x_{i+1}=1$ at every position. At a low column, (4) gives $2c+1$. At a high column it gives
$$
2H-2b+1=2B-2c-1.
$$
The values 都 lie in $[1,2B-1]$, 和 their sum is $2B$. They are distinct 和 nonneutral exactly when $2c+1\ne B$, proving (9).

If $2c+1=B$, the output values 都 equal $B$. The successor leaves $\mathcal P_b$ 因为 it is constant neutral. 这 exception occurs in some bases 和 must be retained.

**THEOREM / immediate consequence.** A pure profile with a constant run of length at least 3 cannot 有 a pure successor. Every admissible word in (8) 有 maximal constant-run length at most 2.

## 3. THEOREM — Sharp escape bound in every base

For $b\ge3$, define
$$K=\min\{j\in\mathbb N:2^j\ge b\}=\lceil\log_2 b\rceil.$$
Every orbit starting with a profile in $\mathcal P_b$ leaves $\mathcal P_b$ at some step $E\le K$. 这 concerns departure from the profile class; it makes no claim that the departure itself produces a palindrome.

### Proof 和 exact exit time

An initially high endpoint, or any word 不 of the form $(c,H,H,c)^r$, exits at the first step. For a word of 那 form, the following formula includes the neutral exception.

While the endpoint remains low 和 the successor remains pure, (9) gives
$$a_{t+1}=2a_t+1,\qquad a_0=c,$$
hence
$$a_t=2^t(c+1)-1.\tag{11}$$
Let
$$k=\min\{j\ge1:2^j(c+1)\ge b\}.$$

There are 2 separate cases.

- If $2^k(c+1)=b$, then $a_k=B$. Section 2's neutral exception occurs at step $k$, so $E=k$.
- If $2^k(c+1)>b$, then $a_k>B$. The profile at step $k$ still uses a nonneutral complementary pair, with its high member at both ends. It therefore exits at the next overflowing step by (7), so $E=k+1$.

因为 $c+1\ge2$ 和 $2^K\ge b$, $k\le K-1$ follows, giving $E\le K$ in either case.

### Sharpness, with ordinary integer witnesses

If $b\ge3$ 不是 a power of 2, choose $c=1$. Then $k=K-1$ 和 the threshold is strict, so $E=K$.

If $b=2^K$ with $K\ge2$, choose $c=2$. The inequalities
$$3\cdot2^{K-2}<b<3\cdot2^{K-1}$$
give $k=K-1$ with a strict threshold, again $E=K$.

For $r=1$, the 4-digit canonical numeral
$$[c,B,B-c,0]_b$$
realizes the required column word $(c,2B-c,2B-c,c)$. Thus sharpness concerns actual integer trajectories, 不 merely abstract symmetric words. For $b=2$, $\mathcal P_b$ is empty.

### Decimal specialization

The sharp chain of column-sum profiles is
$$
\begin{aligned}
(1,17,17,1)&\longmapsto(3,15,15,3)\\
&\longmapsto(7,11,11,7)\\
&\longmapsto(15,3,3,15)\\
&\longmapsto(6,9,6,9,6).
\end{aligned}
\tag{12}
$$
The first 4 profiles are pure complementary profiles; the fifth 有 9. The ordinary witness 是
$$1980\to2871\to4653\to8217\to15345\to69696.$$
Its first palindrome occurs at step 5. It is an escape-bound witness, 不是 a proposed Lychrel number.

The concrete decimal period-4 block transitions already appear in the repository's [phase catalog][R3]. The general finite-word characterization 和 sharp exit theorem for every base above are presented with a direct proof; no claim of exhaustive literature novelty is made.

## 4. THEOREM — Exact arithmetic of recurrent nonneutral bulk bands

The obstruction in Sections 2–3 depends on forbidding exceptional interface coefficients. Once bounded blocks are allowed, the bulk dynamics is different from the affine pure-profile rule.

### The complete scalar transition

For a long constant column-sum run with value $s$:
$$
G_B(s)=
\begin{cases}
\{2s\},&0\le s<B,\\
\{0,B,2B\},&s=B,\\
\{2(s-B)\},&B<s\le2B.
\end{cases}
\tag{13}
$$
For $s\ne B$, write $F_B(s)$ for its unique output.

**Proof.** A low column forces outgoing carry 0, so every interior digit after the first position of its run is $s$. A high column forces outgoing carry 1, so every such digit is $s+1-b=s-B$. Each reflected pair gives the stated doubled value. For a neutral column, entering carry 0 yields digit $B$ 和 outgoing carry 0; entering carry 1 yields digit 0 和 outgoing carry 1. Each run therefore retains its entering carry. Reflected neutral runs give pair sums 0, $B$, or $2B$.

Overflow shifts a reflection partner by one position. Removing a bounded boundary strip keeps both partners inside the corresponding constant runs. Iterating for any fixed number of steps still discards only bounded strips. Thus these formulas impose necessary conditions on returns with arbitrarily long runs; they 不 claim full-word closure.

The set $\{0,B,2B\}$ is closed under these interior transitions: 0 和 $2B$ are fixed, while $B$ maps only into 这个 set. Therefore an interior nonneutral returning bulk cannot pass through the neutral value.

For $0<c<M$, $c\ne B$,
$$
F_B(c)\equiv2c\pmod M,\qquad
F_B(M-c)=M-F_B(c).
\tag{14}
$$

### Recurrent symbols 和 periods

Factor
$$M=2^v u,\qquad u\text{ odd},\qquad v\ge1.$$
An interior nonneutral symbol is periodic exactly when
$$\boxed{2^v\mid c.}\tag{15}$$
For such a symbol, set
$$d=\frac{M}{\gcd(M,c)}.$$
Then $d>1$ is odd. Its primitive labeled period 是
$$\boxed{\operatorname{ord}_d(2),}\tag{16}$$
while the unordered complementary pair 有 primitive period
$$\boxed{\min\{m\ge1:2^m\equiv\pm1\pmod d\}.}\tag{17}$$

**Proof.** A labeled return requires $M\mid(2^m-1)c$. 因为 $2^m-1$ is odd, $2^v\mid c$ is necessary. Under 那 divisibility, division by $\gcd(M,c)$ reduces the condition exactly to $2^m\equiv1\pmod d$. The residue 2 is invertible modulo the odd integer $d$, giving a finite period 和 the exact minimum (16). A return swapping the labels replaces $1$ by $-1$, giving (17); the factor $2^m+1$ is also odd. These cycles avoid 0 和 $B$, 因为 every cycle value is divisible by $2^v$, while $B=2^{v-1}u$ is 不, 和 a nonzero residue cannot reach 0 under an invertible map modulo $d$.

Consequently a nontrivial recurrent interior band exists exactly when $u>1$, equivalently when $b-1$ 不是 a power of 2. If $u=1$, the only multiples of $2^v=M$ in $[0,M]$ are the endpoints. If $u>1$, the choice $c=2^v$ gives an interior recurrent symbol.

### Comparison with the requested bases

The periods in 这个 table concern **bulk values**, 不 entire integer trajectories.

| Base $b$ | $M$ | Recurrent interior values | Primitive labeled periods | Primitive unordered-pair periods |
|---|---:|---|---|---|
| 10 | 18 | $2,4,6,8,10,12,14,16$ | 6 for $d=9$; 2 for $d=3$ | 3; 1 |
| 11 | 20 | $4,8,12,16$ | 4 | 2 |
| 17 | 32 | None | None | None |
| 20 | 38 | Every even value from 2 through 36 | 18 | 9 |
| 26 | 50 | Every even value from 2 through 48 | 20 for $d=25$; 4 for $d=5$ | 10; 2 |
| $2^a,\ a\ge2$ | $2(2^a-1)$ | Every interior even value | Divisors of $a$ | Given by (17) |
| 2 | 2 | None | None | None |

The small exact cycles supporting the finite entries are included in the code output below. For $b=2^a$, every denominator $d$ divides $2^a-1$, so $2^a\equiv1\pmod d$, establishing the stated divisibility of the period.

In decimal, the complete recurrent interior cycles are
$$
2\to4\to8\to16\to14\to10\to2,
\qquad 6\to12\to6.
\tag{18}
$$
Thus a labeled return retaining the bulk phase requires $6\mid m$ on the first cycle or $2\mid m$ on the second. Allowing a swap of the complementary band labels reduces these conditions to $3\mid m$ or no additional positive-period restriction. Existing decimal phase restrictions are already present in [CertificatePhases.lean][R2]; the general-base classification explains their arithmetic.

**THEOREM / scope conclusion.** Bulk arithmetic alone supplies no obstruction excluding decimal. Base 17, rather than base 10, 有 no recurrent interior nonneutral bulk under (13). 这 不 contradict a base-17 construction using neutral bands.

## 5. THEOREM — The regular doubling/reset itinerary requires a power-of-2 base

这 section reconstructs the known regular family from [Seal's posting][S1] 和 derives the exact obstruction to its displayed itinerary. Words in 这个 section are **most-significant first**, 和 an exponent on a digit denotes repetition. Set $U=b-1$, $k\ge2$, 和 define
$$
N_k=10\,U^k(b-2)U\,0^k,\qquad Q_k=N_k0.
$$
For $1\le t<b$, put
$$
P_t=tt\,0^{k-2}(b-t)(b-t-1)^3U^{k-2}(t-1)t,
$$
$$
R_t=tt\,0^{k-1}C_tU^{k-1}(t-1)t,
$$
where
$$
C_t=
\begin{cases}
(b-t)(b-2t-1)(b-t-1),&2t<b,\\
(b-t-1)(2b-2t-1)(b-t-1),&2t\ge b.
\end{cases}
$$
Parenthesized expressions each denote one digit.

The exact transitions 是
$$
T(N_k)=P_1,\qquad T(Q_k)=R_1,
$$
$$
2t<b\Longrightarrow
\bigl(T(P_t)=P_{2t}\ \land\ T(R_t)=R_{2t}\bigr),
$$
$$
2t=b\Longrightarrow
\bigl(T(P_t)=Q_k\ \land\ T(R_t)=N_{k+1}\bigr).
\tag{19}
$$
Appendix A gives the complete carry calculations, including the cases $b=2$, $4t\ge b$, 和 $2t>b$.

For $b=2^a$, these transitions give the known identity
$$
\boxed{T^{2a+2}(N_k)=N_{k+1}.}
\tag{20}
$$
Every intermediate word is nonpalindromic: $N,Q$ begin with 1 和 end with 0; $P,R$ begin with $tt$ 和 end with $(t-1)t$. Thus (20), with induction on the cycles, gives an infinite nonpalindromic orbit in these bases.

### Exact failure in every nonpower base

The first reset requires
$$\boxed{2t=b.}\tag{21}$$
Necessity already follows from the units digit: $P_t$ 有 units digit $t$, so the next units digit is $2t\bmod b$. A reset to $Q_k$ requires units digit 0. 因为 $2\le2t\le2b-2$, the only possible positive multiple of $b$ is $b$.

The parameter starts at 1 和 doubles. Let $j$ be minimal with $2^j\ge b$. If $b$ 不是 a power of 2, the first threshold is a strict overshoot. Write $s=2^j-b$, so $1\le s\le b-2$. Appendix A gives the exact overshoot word
$$
1(s+1)(s-1)\,U^{k-2}
(b-s-1)(b-s-2)^2(b-s)\,0^{k-2}ss.
\tag{22}
$$
It begins with unequal nonzero digits $1,s+1$. Every $N$ or $Q$ begins with $10$, while every $P$ or $R$ begins with equal digits. Thus (22) belongs to none of these 4 regular phase families, for any admissible parameters.

这 establishes the exact obstruction for the displayed itinerary. A later excursion returning to the family, or a different bounded interface construction, remains outside 这个 theorem.

### Decimal counterexample

In base 10, the first phase parameters are $1,2,4,8$; the units sum then becomes 16. Equation (22) gives
$$175\,9^{k-2}\,3224\,0^{k-2}\,66.$$
For $k=2$, the actual orbit is
$$
\begin{aligned}
10998900&\to11988801\to22877712\to44655534\\
&\to88211178\to175322466\to839546037\\
&\to1570191975\to7362102726\to13634115363\\
&\to49985258994.
\end{aligned}
\tag{23}
$$
The final number is a palindrome, 和 the preceding 10 displayed states are nonpalindromic. Thus the naive claim that 这个 entire regular family gives decimal Lychrel numbers is false. Equation (23) 不 establish termination for every other $k$.

## 6. Source comparison 和 repository implications

**THEOREM / source-template distinction.** In the explicit base-11, base-17, 和 base-26 examples from [Seal's cycle tables][S2], the growing digit runs are 0 和 $b-1$ in mirrored locations. Their column-sum bulk is therefore $0+(b-1)=b-1$, neutral. Consequently these examples are outside both $\mathcal P_b$ 和 the repository's nonneutral bulk-phase restriction.

**IDEA / evidence boundary.** The same opened posting reports a base-20 construction but omits its more-than-200-digit witness. 这个 report independently checks the base-20 bulk arithmetic, but supplies no reconstructed base-20 template or 1000-step base-20 construction test. The explicit sporadic templates at bases 4, 11, 17, 和 26 were each tested for 1000 steps, including every completed return identity. These finite checks are reported as validation of the transcribed templates; no infinite conclusion for those sporadic examples is inferred solely from a finite run.

The regular family is known mathematics. The repository already 有 a general neutral-template checker 和 concrete power-of-2 instances in [A120Template.lean][R4], [A120Certificate.lean][R5], 和 [A120PowerTwo.lean][R6]. Its concrete instances cover bases 2, 4, 8, 16, 和 32. No new neutral checker is needed for 这个 report.

**THEOREM / certificate scope.** [ReturnCertificate.lean][R1] permits bounded finite blocks in a shape
$$
B_{\rm ext}\,c^g\,A\,(18-c)^h\,C\,
(18-c)^h\,A^{\rm rev}\,c^g\,B_{\rm ext}^{\rm rev}.
$$
Its phase condition is $1\le c\le17$, $c\ne9$. Sections 2–3 forbid every coefficient outside the complementary pair throughout the full word, a restriction absent from 这个 checker. The obstruction therefore supplies no contradiction to its satisfiability. The neutral-band source examples also 不 instantiate 那 particular checker; the separate A120 framework handles neutral bands.

## 7. Reproducible verification

The complete code 和 its output are embedded in Appendix B. It uses direct integer digit addition, an independent whole-integer arithmetic cross-check, small scalar cycles, 和 a bounded check of the pure-profile theorem. It performs no long-orbit candidate search.

The 1000-step construction checks test both palindrome avoidance at every observed state 和 the exact return word at every completed cycle. For the refuted decimal examples, execution continues after the first palindrome only to record the requested 1000 additions; the proposed nonpalindromic property already fails at 那 first hit.

Observed results: 2,508 realizable pure profiles, 146 pure-to-pure transitions, zero classification mismatches; 492 regular-family identities 和 192 overshoot identities passed. The 9 nondecimal construction tests each completed 1,000 additions. The decimal sharpness witness first reached a palindrome at step 5; the regular-family transplant first reached one at step 10.

The finite validation cannot promote an unproved infinite claim. Sections 1–5 supply the relevant complete proofs; the computations test transcription, boundary cases, 和 explicit counterexamples.

## 8. IDEA — Sharpest remaining question

Can some finite cyclic list of decimal interface blocks close around either
$$
c=6\leftrightarrow12
\quad\text{or}\quad
c=2\to4\to8\to16\to14\to10\to2,
$$
with compatible center behavior, nonnegative cumulative increments for every long band, 和 the checker's nonpalindrome condition at each phase?

Equivalently, can the exact interface defects forced by (4)–(7) be absorbed into bounded blocks that return while the runs grow? The pure-profile theorem requires those blocks to play an essential role. It gives no upper bound on their necessary size 和 no proof that they cannot return.

A separate open route uses neutral decimal bands in the existing A120 framework. The regular power-of-2 reset fails there, but the sporadic constructions in other bases demonstrate that different finite blocks can support different itineraries. No claim of a general arithmetic characterization of bases admitting Lychrel numbers is made.

---

## Appendix A — Complete carries for the regular family

### Carry proof of $N_k\to P_1$

Carry processing is from the units end. Its column-sum word, in 那 order, is

$$1,0,U^{k-2},2U,2U-1,2U-1,2U,U^{k-2},0,1.$$

Incoming carry is initially 0. The first 2 columns output 1,0 和 carry 0. Each first-band $U$ outputs $U$ 和 preserves carry 0. The 4 central-column totals are $2b-2,2b-2,2b-2,2b-1$, 因为 the first creates carry 1 和 the next three receive it. Their outputs are $(b-2),(b-2),(b-2),U$, each with outgoing carry 1. Each second-band $U$ receives carry 1, outputs 0 和 preserves carry 1. The penultimate column 有 sum $0+1$, outputs 1 和 clears the carry. The last column outputs 1 with no overflow. Reversing the resulting output word gives $P_1$. Empty bands at $k=2$ preserve the entering carry.

### Carry proof of $P_t$ transitions

The units-first column sums are

$$2t,2t-1,U^{k-2},A,B,B,A,U^{k-2},2t-1,2t,$$

where $A=2b-2t-1$, $B=2b-2t-2$.

**Case $2t<b$.** The first 2 outputs are $2t,2t-1$, with carry 0. Each first-band $U$ outputs $U$, carry 0. The four center totals are $A,B+1,B+1,A+1$; each is at least $b$. Their outputs are $(b-2t-1)^3,(b-2t)$, each with carry 1. Each second-band $U$ outputs 0 with carry 1. The penultimate total is $(2t-1)+1=2t<b$, so it outputs $2t$ 和 clears the carry. The last column outputs $2t$ with no overflow. 这是 precisely $P_{2t}$.

**Case $2t=b$.** The first column outputs 0 with carry 1. The second column 和 first $U$ band output 0 with carry 1. The four center sums are $b-1,b-2,b-2,b-1$. Their successive (incoming carry, output, outgoing carry) triples are

$$ (1,0,1),\quad(1,b-1,0),\quad(0,b-2,0),\quad(0,b-1,0). $$

The second $U$ band outputs $U$ with carry 0. The penultimate column outputs $U$ with carry 0. The last column outputs 0 with carry 1, producing an additional leading 1. The resulting most-significant-first word is exactly $Q_k$.

**Case $2t>b$.** Put $s=2t-b$, so $1\le s\le b-2$. The first 2 columns output $s,s$ with carry 1. The first $U$ band outputs zeros with carry 1. The four central sum values before incoming carry are $b-s-1,b-s-2,b-s-2,b-s-1$. The first receives carry 1, outputs $b-s$, 和 clears carry; the next three output $b-s-2,b-s-2,b-s-1$ with carry 0. The second $U$ band outputs $U$ with carry 0. The penultimate column outputs $s-1$ with carry 1; the last outputs $s+1$ with carry 1 和 appends a leading 1. Thus

$$T(P_t)=1(s+1)(s-1)\,U^{k-2}\,(b-s-1)(b-s-2)^2(b-s)\,0^{k-2}\,ss.$$

Its units digit is $s\ne0$, so it cannot equal $Q_k$ or any $N_j$.

### Carry proof of $Q_k\to R_1$

The units-first column sums are

$$1,0,U^{k-1},2U,2U-2,2U,U^{k-1},0,1.$$

The initial 1,0 和 first $U$ band emit those same digits with carry 0. The first central column outputs $b-2$ 和 sets carry 1.

- If $b\ge3$, the middle total is $2b-3\ge b$, output $b-3$, carry 1. The last central total is $2b-1$, output $U$, carry 1.
- If $b=2$, the middle total is 1, output 1, carry 0. The last central total is 2, output 0, carry 1.

The second $U$ band outputs zeros with carry 1. The penultimate column outputs 1 和 clears the carry. The last column outputs 1. These are exactly the 2 branches of $R_1$.

### Carry proof of $R_t\to R_{2t}$ when $2t<b$

The input uses the first center branch. Its units-first column sums are

$$2t,2t-1,U^{k-1},A,D,A,U^{k-1},2t-1,2t,$$

with $A=2b-2t-1$ 和 $D=2b-4t-2$. The first 2 columns 和 first band emit $2t,2t-1,U^{k-1}$ with carry 0. The first center column emits $b-2t-1$, carry 1.

- If $4t<b$, the middle total $D+1=2b-4t-1$ is at least $b$, so its output is $b-4t-1$, carry 1. The last center output is $b-2t$, carry 1.
- If $4t\ge b$, the middle total $2b-4t-1$ is below $b$ 和 nonnegative, so it outputs 那 value 和 clears carry. The last center column emits $b-2t-1$, carry 1.

The second band emits zeros, carry 1. The penultimate total $2t$ emits $2t$ 和 clears carry. The last column emits $2t$ without overflow. The 2 center-output cases give exactly the respective branches of $R_{2t}$.

### Carry proof of $R_t\to N_{k+1}$ when $2t=b$

Here $t=b/2$ 和 the center is $(t-1)U(t-1)$. The units-first column sums are

$$b,b-1,U^{k-1},b-2,2b-2,b-2,U^{k-1},b-1,b.$$

The first 2 columns 和 first band output zeros with carry 1. The first center total is $b-1$, output $U$, carry 0. The middle total is $2b-2$, output $b-2$, carry 1. The last center total is $b-1$, output $U$, carry 0. The second band 和 penultimate column output $U$ with carry 0. The last column outputs 0 with overflow 1. 这是 $N_{k+1}$.

## Appendix B — Complete code 和 actual output

Save the following code as `agent202_checks.py`, then run `python3 agent202_checks.py`. Python 3 和 its standard library suffice.

```python
"""Direct digit checks of published Seal templates; no seed search.

Sources:
https://www.mathpages.com/home/dseal.htm
https://www.p196.org/html/papers1.html

Digits are stored most-significant first.  All arithmetic is integer-only.
"""

from __future__ import annotations

import json

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def parse(word: str) -> list[int]:
    return [DIGITS.index(x.lower()) for x in word if not x.isspace()]


def value(word, base):
    total = 0
    for digit in word:
        total = base * total + digit
    return total


def step(word: list[int], base: int) -> list[int]:
    carry = 0
    result = []
    for digit, opposite in zip(reversed(word), word):
        carry, output = divmod(digit + opposite + carry, base)
        result.append(output)
    if carry:
        result.append(carry)
    answer = result[::-1]
    assert value(answer, base) == value(word, base) + value(word[::-1], base)
    return answer


def regular(base: int, k: int) -> list[int]:
    return [1, 0] + [base - 1] * k + [base - 2, base - 1] + [0] * k


def seal(base: int, n: int) -> list[int]:
    if base == 4:
        return parse("1033202000232" + "2" * n + "2302333113230")
    if base == 11:
        return parse("1246277" + "a" * n + "a170352495681825a5026571a506181864a5143171" + "0" * n + "0872542")
    if base == 17:
        return parse("10023ab83e3b983cfgec556g4g010" + "0" * n + "0fgcg10fg505gf020cgf" + "g" * n + "gg11g4f655ddggb299b3d38bb320g")
    if base == 26:
        return parse("1n5ela6c" + "p" * n + "p6e7" + "0" * n + "0d59me5n")
    raise ValueError(base)


def check_return(factory, base: int, start: int, period: int, growth: int):
    word = factory(base, start)
    initial_len = len(word)
    completed_returns = 0
    for index in range(1, 1001):
        assert word != word[::-1], (base, "palindrome at", index - 1)
        word = step(word, base)
        if index % period == 0:
            expected = factory(base, start + growth * (index // period))
            assert word == expected, (base, "return failure at", index)
            completed_returns += 1
    assert word != word[::-1], (base, "palindrome at", 1000)
    return {
        "base": base,
        "steps": 1000,
        "palindromes": 0,
        "return_period": period,
        "parameter_growth": growth,
        "checked_returns": completed_returns,
        "initial_digits": initial_len,
        "final_digits": len(word),
    }


def p_word(base: int, k: int, t: int):
    return [t, t] + [0] * (k - 2) + [base - t] + [base - t - 1] * 3 + [base - 1] * (k - 2) + [t - 1, t]


def q_word(base: int, k: int):
    return regular(base, k) + [0]


def r_word(base: int, k: int, t: int):
    if 2 * t < base:
        center = [base - t, base - 2 * t - 1, base - t - 1]
    else:
        center = [base - t - 1, 2 * base - 2 * t - 1, base - t - 1]
    return [t, t] + [0] * (k - 1) + center + [base - 1] * (k - 1) + [t - 1, t]


def check_local_identities():
    count = 0
    for base in (2, 4, 8, 10, 11, 16, 17, 20, 26, 32):
        for k in (2, 3, 5):
            assert step(regular(base, k), base) == p_word(base, k, 1)
            assert step(q_word(base, k), base) == r_word(base, k, 1)
            count += 2
            for t in range(1, base):
                if 2 * t < base:
                    assert step(p_word(base, k, t), base) == p_word(base, k, 2 * t)
                    assert step(r_word(base, k, t), base) == r_word(base, k, 2 * t)
                    count += 2
                if 2 * t == base:
                    assert step(p_word(base, k, t), base) == q_word(base, k)
                    assert step(r_word(base, k, t), base) == regular(base, k + 1)
                    count += 2
    return count


def check_known():
    result = {"published_sporadic_templates": [], "power_two_regular_templates": []}
    for base, period, growth in [(4, 6, 3), (11, 6, 1), (17, 6, 1), (26, 4, 1)]:
        result["published_sporadic_templates"].append(check_return(seal, base, 2, period, growth))
    for exponent in range(1, 6):
        base = 2 ** exponent
        result["power_two_regular_templates"].append(check_return(regular, base, 2, 2 * exponent + 2, 1))
    result["local_identity_checks"] = check_local_identities()
    base = 10
    k = 4
    word = regular(base, k)
    trajectory = ["".join(DIGITS[x] for x in word)]
    for index in range(5):
        word = step(word, base)
        trajectory.append("".join(DIGITS[x] for x in word))
    result["decimal_first_reset_failure"] = {
        "k": k,
        "trajectory": trajectory,
        "reset_target": "".join(DIGITS[x] for x in q_word(base, k)),
        "failure_step": 5,
        "reason": "P_8 has units sum 16, hence output units 6; the reset target has units 0.",
    }
    word = regular(10, 2)
    first_palindrome = None
    short_trajectory = []
    for index in range(1001):
        if index <= 10:
            short_trajectory.append("".join(DIGITS[x] for x in word))
        if word == word[::-1] and first_palindrome is None:
            first_palindrome = index
        if index < 1000:
            word = step(word, 10)
    assert first_palindrome == 10
    result["decimal_regular_family_refutation"] = {
        "base": 10,
        "k": 2,
        "steps": 1000,
        "first_palindrome_step": first_palindrome,
        "trajectory_through_first_palindrome": short_trajectory,
        "final_digits": len(word),
        "qualification": "The routine continues after the first palindrome only to meet the 1000-step audit; the claimed Lychrel property already fails at step 10.",
    }
    return result



"""Finite verification of the pure complementary-band theorem; no seed search."""

from itertools import product
import json


def next_q(q, base):
    """Normalize the supplied symmetric column sums, then re-fold."""
    carry = 0
    digits = []
    for column_sum in q:
        total = column_sum + carry
        digits.append(total % base)
        carry = total // base
    if carry:
        digits.append(carry)
    return tuple(a + z for a, z in zip(digits, reversed(digits)))


def pure(q, base):
    values = set(q)
    return (
        len(values) == 2
        and min(values) > 0
        and max(values) < 2 * (base - 1)
        and sum(values) == 2 * (base - 1)
    )


def check_pure():
    count = successes = 0
    bases = (3, 4, 10, 11, 17, 20, 26)
    for base in bases:
        B = base - 1
        for c in range(1, B):
            high = 2 * B - c
            for length in range(2, 9):
                for half in product((c, high), repeat=(length + 1) // 2):
                    q = half + half[: length // 2][::-1]
                    if len(set(q)) != 2:
                        continue
                    if length % 2 and q[length // 2] % 2:
                        continue  # Odd central sum is not a digit-pair word.
                    actual = next_q(q, base)
                    digits = [0] * length
                    for i in range(length // 2):
                        digits[i] = min(q[i], B)
                        digits[length - 1 - i] = max(0, q[i] - B)
                    if length % 2:
                        digits[length // 2] = q[length // 2] // 2
                    assert tuple(a + z for a, z in zip(digits, digits[::-1])) == q
                    output_digits = step(digits, base)
                    assert actual == tuple(a + z for a, z in zip(output_digits, output_digits[::-1]))
                    x = [int(v > B) for v in q]
                    if x[0] == 0:
                        padded = [0] + x + [0]
                        formula = tuple(2*q[i] - 2*base*x[i] + padded[i] + padded[i+2] for i in range(length))
                    else:
                        p = [v - B*h for v, h in zip(q, x)]
                        formula = (p[0],) + tuple(p[i] + p[i-1] for i in range(1, length)) + (p[0],)
                    assert actual == formula
                    predicted_pure = (
                        length % 4 == 0
                        and q == (c, high, high, c) * (length // 4)
                        and 2 * c + 1 != B
                    )
                    assert pure(actual, base) == predicted_pure, (
                        base, c, q, actual, predicted_pure
                    )
                    count += 1
                    if predicted_pure:
                        predicted = (
                            2 * c + 1,
                            2 * B - 2 * c - 1,
                            2 * B - 2 * c - 1,
                            2 * c + 1,
                        ) * (length // 4)
                        assert actual == predicted
                        successes += 1

    sharp_cases = []
    for base in bases:
        c = 2 if base & (base - 1) == 0 else 1
        B = base - 1
        q = (c, 2 * B - c, 2 * B - c, c)
        initial = q
        exit_step = 0
        while pure(q, base):
            exit_step += 1
            q = next_q(q, base)
        bound = (base - 1).bit_length()  # Exact ceil(log_2(base)).
        assert exit_step == bound
        sharp_cases.append({
            "base": base,
            "initial_q": initial,
            "exit_step": exit_step,
            "sharp_bound": bound,
            "first_outside_q": q,
        })

    n = 1980
    first_palindrome = None
    prefix = [n]
    for iteration in range(1, 1001):
        n += int(str(n)[::-1])
        if iteration <= 5:
            prefix.append(n)
        if first_palindrome is None and str(n) == str(n)[::-1]:
            first_palindrome = iteration
    assert first_palindrome == 5

    result = {
        "purpose": "finite theorem check, not a candidate search",
        "classification": {
            "bases": bases,
            "lengths": [2, 8],
            "realizable_symmetric_words": count,
            "pure_to_pure_transitions": successes,
            "classification_mismatches": 0,
        },
        "sharp_exit_cases": sharp_cases,
        "decimal_sharpness_witness": {
            "seed": 1980,
            "steps_run": 1000,
            "prefix": prefix,
            "first_palindrome_step": first_palindrome,
            "digits_after_1000_steps": len(str(n)),
            "is_a_lychrel_construction": False,
        },
    }
    assert count == 2508 and successes == 146
    return result



def bulk_cycles(base):
    B, M = base - 1, 2 * (base - 1)
    seen, cycles = set(), []
    for c in range(1, M):
        if c == B or c in seen:
            continue
        path, index, x = [], {}, c
        while x not in (0, B) and x not in index and x not in seen:
            index[x] = len(path)
            path.append(x)
            x = (2*x) % M
        if x in index:
            cycles.append(path[index[x]:])
        seen.update(path)
    # Verify the exact divisibility characterization over this tiny alphabet.
    power = M & -M
    actual = {c for cycle in cycles for c in cycle}
    expected = {c for c in range(1, M) if c % power == 0}
    assert actual == expected
    return cycles


def check_overshoot():
    count = 0
    for base in (2, 4, 8, 10, 11, 16, 17, 20, 26, 32):
        for k in (2, 3, 5):
            for t in range(1, base):
                if 2*t > base:
                    s = 2*t - base
                    expected = [1, s+1, s-1] + [base-1]*(k-2) + [base-s-1, base-s-2, base-s-2, base-s] + [0]*(k-2) + [s, s]
                    assert step(p_word(base, k, t), base) == expected
                    count += 1
    return count


def main():
    known = check_known()
    pure_result = check_pure()
    print('Every digit addition also matched independent whole-integer addition.')
    for name in ('published_sporadic_templates', 'power_two_regular_templates'):
        for row in known[name]:
            print(name, json.dumps(row, separators=(',', ':')))
    print('local_regular_identities', known['local_identity_checks'])
    print('local_overshoot_identities', check_overshoot())
    print('decimal_reset_failure', json.dumps(known['decimal_first_reset_failure'], separators=(',', ':')))
    print('decimal_refutation', json.dumps(known['decimal_regular_family_refutation'], separators=(',', ':')))
    print('pure_classification', json.dumps(pure_result['classification'], separators=(',', ':')))
    for row in pure_result['sharp_exit_cases']:
        print('sharp_exit', json.dumps(row, separators=(',', ':')))
    print('decimal_sharpness', json.dumps(pure_result['decimal_sharpness_witness'], separators=(',', ':')))
    for base in (2, 4, 8, 10, 11, 16, 17, 20, 26, 32):
        print('bulk_cycles', base, bulk_cycles(base))


if __name__ == '__main__':
    main()
```

### Actual output

```text
Every digit addition also matched independent whole-integer addition.
published_sporadic_templates {"base":4,"steps":1000,"palindromes":0,"return_period":6,"parameter_growth":3,"checked_returns":166,"initial_digits":28,"final_digits":528}
published_sporadic_templates {"base":11,"steps":1000,"palindromes":0,"return_period":6,"parameter_growth":1,"checked_returns":166,"initial_digits":60,"final_digits":393}
published_sporadic_templates {"base":17,"steps":1000,"palindromes":0,"return_period":6,"parameter_growth":1,"checked_returns":166,"initial_digits":82,"final_digits":415}
published_sporadic_templates {"base":26,"steps":1000,"palindromes":0,"return_period":4,"parameter_growth":1,"checked_returns":250,"initial_digits":24,"final_digits":524}
power_two_regular_templates {"base":2,"steps":1000,"palindromes":0,"return_period":4,"parameter_growth":1,"checked_returns":250,"initial_digits":8,"final_digits":508}
power_two_regular_templates {"base":4,"steps":1000,"palindromes":0,"return_period":6,"parameter_growth":1,"checked_returns":166,"initial_digits":8,"final_digits":341}
power_two_regular_templates {"base":8,"steps":1000,"palindromes":0,"return_period":8,"parameter_growth":1,"checked_returns":125,"initial_digits":8,"final_digits":258}
power_two_regular_templates {"base":16,"steps":1000,"palindromes":0,"return_period":10,"parameter_growth":1,"checked_returns":100,"initial_digits":8,"final_digits":208}
power_two_regular_templates {"base":32,"steps":1000,"palindromes":0,"return_period":12,"parameter_growth":1,"checked_returns":83,"initial_digits":8,"final_digits":174}
local_regular_identities 492
local_overshoot_identities 192
decimal_reset_failure {"k":4,"trajectory":["109999890000","110098889901","220087779912","440065559934","880021119978","1759932240066"],"reset_target":"1099998900000","failure_step":5,"reason":"P_8 has units sum 16, hence output units 6; the reset target has units 0."}
decimal_refutation {"base":10,"k":2,"steps":1000,"first_palindrome_step":10,"trajectory_through_first_palindrome":["10998900","11988801","22877712","44655534","88211178","175322466","839546037","1570191975","7362102726","13634115363","49985258994"],"final_digits":415,"qualification":"The routine continues after the first palindrome only to meet the 1000-step audit; the claimed Lychrel property already fails at step 10."}
pure_classification {"bases":[3,4,10,11,17,20,26],"lengths":[2,8],"realizable_symmetric_words":2508,"pure_to_pure_transitions":146,"classification_mismatches":0}
sharp_exit {"base":3,"initial_q":[1,3,3,1],"exit_step":2,"sharp_bound":2,"first_outside_q":[1,2,2,2,1]}
sharp_exit {"base":4,"initial_q":[2,4,4,2],"exit_step":2,"sharp_bound":2,"first_outside_q":[2,3,2,3,2]}
sharp_exit {"base":10,"initial_q":[1,17,17,1],"exit_step":4,"sharp_bound":4,"first_outside_q":[6,9,6,9,6]}
sharp_exit {"base":11,"initial_q":[1,19,19,1],"exit_step":4,"sharp_bound":4,"first_outside_q":[5,10,10,10,5]}
sharp_exit {"base":17,"initial_q":[1,31,31,1],"exit_step":5,"sharp_bound":5,"first_outside_q":[15,16,2,16,15]}
sharp_exit {"base":20,"initial_q":[1,37,37,1],"exit_step":5,"sharp_bound":5,"first_outside_q":[12,19,14,19,12]}
sharp_exit {"base":26,"initial_q":[1,49,49,1],"exit_step":5,"sharp_bound":5,"first_outside_q":[6,25,38,25,6]}
decimal_sharpness {"seed":1980,"steps_run":1000,"prefix":[1980,2871,4653,8217,15345,69696],"first_palindrome_step":5,"digits_after_1000_steps":417,"is_a_lychrel_construction":false}
bulk_cycles 2 []
bulk_cycles 4 [[2, 4]]
bulk_cycles 8 [[2, 4, 8], [6, 12, 10]]
bulk_cycles 10 [[2, 4, 8, 16, 14, 10], [6, 12]]
bulk_cycles 11 [[4, 8, 16, 12]]
bulk_cycles 16 [[2, 4, 8, 16], [6, 12, 24, 18], [10, 20], [14, 28, 26, 22]]
bulk_cycles 17 []
bulk_cycles 20 [[2, 4, 8, 16, 32, 26, 14, 28, 18, 36, 34, 30, 22, 6, 12, 24, 10, 20]]
bulk_cycles 26 [[2, 4, 8, 16, 32, 14, 28, 6, 12, 24, 48, 46, 42, 34, 18, 36, 22, 44, 38, 26], [10, 20, 40, 30]]
bulk_cycles 32 [[2, 4, 8, 16, 32], [6, 12, 24, 48, 34], [10, 20, 40, 18, 36], [14, 28, 56, 50, 38], [22, 44, 26, 52, 42], [30, 60, 58, 54, 46]]
```

## References actually inspected

[S1]: https://www.p196.org/html/papers1.html
[S2]: https://www.mathpages.com/home/dseal.htm
[R1]: https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean
[R2]: https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificatePhases.lean
[R3]: https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent1PeriodicPhaseCatalog/Agent1PeriodicPhaseCatalog.lean
[R4]: https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean
[R5]: https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean
[R6]: https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean

- **[S1][S1]:** David J. Seal's January 1996 posting, reproduced at p196.org; regular power-of-2 family 和 sporadic examples. The posting itself describes its original transcription as preliminary.
- **[S2][S2]:** David J. Seal's sporadic examples 和 displayed cycle tables, reproduced at MathPages.
- **R1–R6:** Repository sources at commit `c6902ac6c366ce018e68a810f58b400dda07145a`. These identify existing scope 和 prior decimal phase edges. Source inspection is distinct from recompiling their Lean theorems.

