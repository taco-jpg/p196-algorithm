# REPORT_214 — Periodic bands of spatial periods 1–4

Agent: **214**. Direction: **4**. Date: **2026-10-22**.

Repository base inspected: `c6902ac6c366ce018e68a810f58b400dda07145a`.

## Answer in one paragraph

**IDEA — status:** Decimal Lychrel existence remains unresolved by 这 report; the result supplies an obstruction 和 bulk classifications, with finite Lychrel existence 还 open. **THEOREM:** An exactly aligned periodic bulk fixed 点, of any spatial period, must be constant 0, 9, or 18, with opposite directional carries required for constant 9. Every spatial-period-2 band collapses to a constant at an overflow, including bands containing 9. Consequently, fixed-length growing return families made entirely from a fixed number of period-1/2 bands 和 bounded intervening blocks cannot retain an alternating band of unbounded length. The nonconstant period-2 no-overflow dynamics 有 exactly three labelled 10-cycles 和 两 labelled 30-cycles. For the restricted alphabet `{1,...,17} \ {9}`, the forced-overflow bulk map 有 exactly three temporal 2-cycles 和 thirteen temporal 6-cycles of genuine spatial period 3, 和 six temporal 24-cycles of genuine spatial period 4. These latter cycles cannot themselves be actual indefinitely overflowing integer orbits: actual decimal reverse-add permits at most three consecutive overflows. Complete proofs, failed extensions, 和 reproducible 1000-step checks follow. **IDEA — remaining task:** connect mixed overflow/no-overflow bulk phases to returning finite interfaces, a compatible center, positive length growth, 和 a persistent nonsymmetric output.

## 1. Scope, conventions, 和 prior work

**THEOREM — scope of the results below.** The proofs concern arbitrary valid decimal column-sum words. The scope is independent of any particular previously studied seed. Spatial period refers to the length of a repeated coefficient block; temporal period refers to the number of map applications before a labelled block returns. Cycle counts distinguish spatial rotations.

**LEAN-VERIFIED — existing repository results, cited rather than rebuilt here.** The repository already provides stable repeated-block normalization 和 exact period-4 quotient bookkeeping. Relevant inspected sources are:

- [`Agent1PeriodicDigits.lean`](lean/P196/Foundations/Agent1PeriodicDigits.lean): `normalize_periodicWord`, `scan_carry_stable`.
- [`Agent1PeriodicPhase.lean`](lean/P196/Foundations/Agent1PeriodicPhase.lean): `terminalCarry_eq_of_nonNine`, `rawPeriod_eq_phaseImage`.
- [`Agent1PeriodicQuotient.lean`](lean/P196/Foundations/Agent1PeriodicQuotient.lean): `quotient_step_bounded`, `quotient_width_balance`.
- [`Agent1PeriodicPhaseCatalog.lean`](lean/P196/Agent1PeriodicPhaseCatalog/Agent1PeriodicPhaseCatalog.lean): the retained 59-phase, 124-labelled-edge catalog. Its coverage requires initial catalog membership; its domain excludes arbitrary period-4 blocks.
- [`persist_exterior_bulk_collapse.lean`](lean/P196/Drafts/Research/persist_exterior_bulk_collapse.lean): the specific alternating 13/14 collapse to 9, which is a special case of Section 4.
- [`Agent112TwoPhaseObstruction`](lean/P196/Drafts/Agent112TwoPhaseObstruction): temporal alternation of constant bands 6 和 12 at a fixed cut. Its hypotheses differ from the spatial-period-2 statement below.

**IDEA — verification status:** New Lean modules submitted: **0**. The new results carry the label **THEOREM** 因为 complete mathematical proofs are supplied. Numerical checks validate formulas 和 displayed examples; the proofs establish the general statements. The existing Lean definitions establish context, without a claim that the new theorems were checked by Lean.

## 2. THEOREM — exact carries 和 the periodic block maps

Write digits from the units end. For a finite input of length \(L\), let

\[
q_i=d_i+d_{L-1-i},\qquad 0\le q_i\le18,
\]

so \(q_i=q_{L-1-i}\). Define

\[
H(s,c)=\left\lfloor\frac{s+c}{10}\right\rfloor
=\begin{cases}
0,&0\le s\le8,\\
c,&s=9,\\
1,&10\le s\le18,
\end{cases}
\qquad c\in\{0,1\}.
\]

The actual carries 和 emitted digits satisfy

\[
c_0=0,\quad c_{i+1}=H(q_i,c_i),\quad
e_i=q_i+c_i-10c_{i+1},\quad \gamma=c_L.
\]

If \(\gamma=1\), append \(e_L=1\). Put

\[
A_i=c_i,\qquad B_i=c_{L-i}.
\]

Symmetry of \(q\) gives the opposing recurrences

\[
A_{i+1}=H(q_i,A_i),\qquad B_i=H(q_i,B_{i+1}).
\]

For a stabilized cyclic block of spatial period \(p\), indices are modulo \(p\). Define the digits emitted in the 两 directions by

\[
U_i=q_i+A_i-10A_{i+1},\qquad
V_i=q_i+B_{i+1}-10B_i.
\]

The exact interior maps are

\[
\boxed{F_0(q)_i=U_i+V_i},\qquad
\boxed{F_1(q)_i=U_i+V_{i-1}}.
\tag{2.1}
\]

In expanded form,

\[
F_0(q)_i=2q_i+A_i+B_{i+1}-10(A_{i+1}+B_i),
\tag{2.2}
\]

\[
F_1(q)_i=q_i+q_{i-1}+A_i+B_i
 -10(A_{i+1}+B_{i-1}).
\tag{2.3}
\]

**Proof.** Without overflow, the reflected digit is \(e_{L-1-i}\); its coefficient is \(q_i\), incoming carry is \(B_{i+1}\), 和 outgoing carry is \(B_i\). With overflow, the reflected digit is \(e_{L-i}\); for \(1\le i\le L-1\), its coefficient is \(q_{i-1}\), incoming carry is \(B_i\), 和 outgoing carry is \(B_{i-1}\). Substitution gives (2.2) 和 (2.3). The overflow endpoints are handled separately:

\[
q'_0=q'_L=e_0+1=q_0-10c_1+1.
\tag{2.4}
\]

Thus an overflowing step shifts the reflected periodic band by one position. Formula (2.1) includes 那 shift.

For carry stabilization, a coefficient below 9 resets either incoming carry to 0, a coefficient above 9 resets it to 1, 和 coefficient 9 transmits it unchanged. A block containing a non-9 coefficient therefore induces a constant map on the incoming carry bit. After one complete copy, its outgoing carry is the unique cyclic starting carry for every subsequent copy. The reversed block obeys the same explicit reset/transmit rules. A constant-9 block instead preserves each directional entry bit throughout the band; those 两 bits can differ. 这 accounts for every carry case. \(\square\)

**THEOREM — useful specialization without coefficient 9.** Let

\[
s_i=\mathbf1_{\{q_i\ge10\}},\qquad f(q_i)=q_i-9s_i.
\]

Then \(A_i=s_{i-1}\), \(B_i=s_i\), 和

\[
\boxed{F_0(q)_i=2q_i-20s_i+s_{i-1}+s_{i+1}},
\qquad
\boxed{F_1(q)_i=f(q_i)+f(q_{i-1})}.
\tag{2.5}
\]

**Proof.** The outgoing carry of every coefficient is its bit \(s_i\), regardless of the entering bit. Substitute those carries into (2.2) 和 (2.3). In (2.3), the entering contributions \(s_{i-1}+s_i\) reduce the coefficient \(-10\) to \(-9\) at the 两 positions. \(\square\)

## 3. THEOREM — every exactly aligned bulk fixed 点 is constant

For any positive spatial period \(p\), any consistent cyclic directional carries, 和 either \(\gamma\in\{0,1\}\),

\[
F_\gamma(q)=q
\quad\Longrightarrow\quad
q\equiv0,\quad q\equiv9,\quad\text{or}\quad q\equiv18.
\tag{3.1}
\]

The constant-9 case requires opposite directional carries. Conversely, the three listed constant blocks are fixed with their stated compatible carries.

**Proof.** The fixed 点 equation 和 the formula for \(U_i\) give

\[
V_{i-\gamma}=q_i-U_i=10A_{i+1}-A_i.
\]

Every \(V_i\) is a decimal digit. The carry transition \((A_i,A_{i+1})=(0,1)\) would require digit 10; the transition \((1,0)\) would require digit \(-1\). Those digits 都 fall outside the permitted range. Thus \(A_i=a\) is constant, with \(a\in\{0,1\}\), 和 \(V_i=9a\) for every \(i\).

The forward carry condition yields

\[
q_i\le9\quad(a=0),\qquad q_i\ge9\quad(a=1).
\]

The equation for \(V_i\) becomes

\[
q_i=9a-B_{i+1}+10B_i.
\]

Every nonconstant reverse-carry transition is excluded explicitly:

| \(a\) | \((B_{i+1},B_i)\) | Required \(q_i\) | Contradiction |
|---:|---:|---:|---|
| 0 | (1,0) | -1 | \(q_i\ge0\) |
| 0 | (0,1) | 10 | forward carry requires \(q_i\le9\) |
| 1 | (1,0) | 8 | forward carry requires \(q_i\ge9\) |
| 1 | (0,1) | 19 | \(q_i\le18\) |

Therefore \(B_i=b\) is constant 和 \(q_i=9(a+b)\). The compatible pairs are \((a,b)=(0,0)\) for 0, \((0,1),(1,0)\) for 9, 和 \((1,1)\) for 18. Direct substitution gives \(U_i+V_{i-\gamma}=q_i\) in each case. \(\square\)

**IDEA — limitation:** Exact equality in a fixed coordinate alignment is required. A return up to spatial rotation, a multi-step cycle, or a return of finite interfaces needs additional analysis. Constant 9 remains a possible bulk state; its boundary compatibility remains open.

## 4. THEOREM — complete period-2 bulk obstruction 和 cycles

### 4.1 Overflow destroys every genuine period-2 bulk

Let the stabilized word be \((a,b)^\infty\), with \((a,b)\ne(9,9)\). Its unique cyclic carry pair \((\alpha,\beta)\) satisfies

\[
\beta=H(a,\alpha),\qquad \alpha=H(b,\beta).
\]

Let

\[
u=a+\alpha-10\beta,\qquad
v=b+\beta-10\alpha.
\]

Then

\[
\boxed{F_0(a,b)=(2u,2v)},\qquad
\boxed{F_1(a,b)=(u+v,u+v)}.
\tag{4.1}
\]

**Proof with the full carry table.** In period 2, predecessor 和 successor indices agree. The reversed cyclic carry equations are consequently the same equations as the forward equations at corresponding symbols. Uniqueness gives matching directional digits \((u,v)\). A non-overflow step pairs each digit with itself; overflow pairs it with the other digit. The cases, including each placement of 9, are:

| \(a\) | \(b\) | \((\alpha,\beta)\) | \((u,v)\) | Overflow constant |
|---|---|---|---|---|
| \(0\ldots8\) | \(0\ldots8\) | (0,0) | \((a,b)\) | \(a+b\) |
| \(0\ldots8\) | \(10\ldots18\) | (1,0) | \((a+1,b-10)\) | \(a+b-9\) |
| \(10\ldots18\) | \(0\ldots8\) | (0,1) | \((a-10,b+1)\) | \(a+b-9\) |
| \(10\ldots18\) | \(10\ldots18\) | (1,1) | \((a-9,b-9)\) | \(a+b-18\) |
| \(0\ldots8\) | 9 | (0,0) | \((a,9)\) | \(a+9\) |
| 9 | \(0\ldots8\) | (0,0) | \((9,b)\) | \(9+b\) |
| 9 | \(10\ldots18\) | (1,1) | \((0,b-9)\) | \(b-9\) |
| \(10\ldots18\) | 9 | (1,1) | \((a-9,0)\) | \(a-9\) |

For the excluded constant-9 case, let the independently inherited directional carries be \(\alpha,\beta\). The carries 都 remain constant, emitting digits \(9-9\alpha\) 和 \(9-9\beta\). The maps 都 give the constant

\[
18-9(\alpha+\beta)\in\{0,9,18\}.
\]

Thus every period-at-most-2 bulk becomes constant at an overflow. A constant bulk stays constant: its next value is \(2s\) for \(s\le8\), \(2s-18\) for \(s\ge10\), 和 the displayed carry-dependent value for \(s=9\). \(\square\)

### 4.2 Complete nonconstant cycles without overflow

After one \(F_0\) step, every nonconstant period-2 block 有 even coefficients. Write

\[
q=(2d_0,2d_1),\qquad N=d_0+10d_1,\qquad0\le d_0,d_1\le9.
\]

With \(h_j=\lfloor2d_j/10\rfloor\), formula (4.1) gives

\[
d'_0=2d_0-10h_0+h_1,\qquad
d'_1=2d_1-10h_1+h_0,
\]

so

\[
\boxed{N'=2N-99h_1}.
\tag{4.2}
\]

For \(1\le N\le98\), 这 is exactly doubling modulo 99, with the unique representative in 那 interval. The values 0 和 99 are separate fixed 点. The spatial word is constant exactly when \(11\mid N\).

**Proof of the cycle counts.** For \(g=\gcd(N,99)\), its return time is the multiplicative order of 2 modulo \(99/g\). The powers modulo 11 give \(2^5\equiv-1\), \(2^{10}\equiv1\), 和 orders 1 和 2 excluded, hence order 10. Modulo 9, \(2^3\equiv-1\), \(2^6\equiv1\), 和 orders 1 or 2 fail, hence order 6. The Chinese remainder theorem gives orders 10 modulo 33 和 30 modulo 99. Counting residues with each gcd gives:

| \(g\) | Number of residues | Temporal period | Number of labelled cycles | Representatives \(N\) |
|---:|---:|---:|---:|---|
| 9 | 10 | 10 | 1 | 9 |
| 3 | 20 | 10 | 2 | 3, 15 |
| 1 | 60 | 30 | 2 | 1, 5 |

The listed representatives distinguish the cycles: \(5\) cannot be a power of 2 modulo 33 or 99, 因为 \(2^4\equiv5\pmod{11}\) would force an even exponent, while \(5\equiv2\pmod3\) would force an odd exponent. Thus 3 和 15 lie in different gcd-3 cycles, 和 1 和 5 lie in different gcd-1 cycles. The counts leave no further cycles.

The constant nonneutral cycles are

\[
0\to0,\qquad18\to18,\qquad6\to12\to6,
\]

\[
2\to4\to8\to16\to14\to10\to2.
\]

The neutral constant 9 也 有 a fixed branch when its directional carries differ; its other branches lead to 0 or 18. These exhaust recurrent constant states. Since an overflow destroys a nonconstant period-2 block permanently at the bulk level, every nonconstant recurrent period-2 path uses only \(F_0\), so the table exhausts its possible labelled cycles. \(\square\)

### 4.3 A uniform obstruction for finite growing templates

Fix nonnegative integers \(r,B\) 和 a positive integer \(m\). Suppose a valid finite column-sum word is partitioned into at most \(r\) interval bands of spatial period at most 2, together with at most \(B\) other columns. If its next \(m\) reverse-add steps include an overflow, its final column-sum word 有 at most

\[
\boxed{B+r+m(4r+1)}
\tag{4.3}
\]

maximal constant runs.

**Proof.** At each step, trim 两 positions from each end of each current band, retaining indices \([l+2,r_0-2]\) from an interval \([l,r_0]\). If the band 有 at most four positions, retain none. For a nonconstant period-2 band, or a non-9 constant band, every consecutive pair 有 a reset. The exact required carry dependencies are:

| Carry | Sufficient input positions |
|---|---|
| \(A_i\) | \(i-2,i-1\) |
| \(A_{i+1}\) | \(i-1,i\) |
| \(B_i\) | \(i,i+1\) |
| \(B_{i+1}\) | \(i+1,i+2\) |
| \(B_{i-1}\) | \(i-1,i\) |

Every listed position stays in the original band for each retained index. Therefore the finite-word carries equal the cyclic carries on the retained core. Formula (2.3) 也 uses \(q_{i-1}\), which lies inside the same interval. A constant-9 band is handled separately: each directional carry is constant throughout 那 band, so the last case of Section 4.1 applies without a reset.

Before the first overflow, every retained core 还 有 period at most 2. At the first overflow, every retained core becomes constant. Every later retained core remains constant by the explicit constant-band formulas in Section 4.1.

Each step transfers at most \(4r\) core positions into the exceptional part, 和 appends at most one overflow position. After \(m\) steps, the exceptional part therefore 有 at most \(B+m(4r+1)\) positions, while at most \(r\) constant cores remain. Counting each exceptional position as a separate run gives (4.3). \(\square\)

**THEOREM — consequence.** A fixed-\(m\) return family constructed entirely from period-at-most-2 bands 和 uniformly bounded intervening blocks cannot increase total length while retaining a genuine period-2 band whose length is unbounded across the family. Positive length gain forces an overflow during the return. The output then satisfies (4.3), independently of the input exponents. An alternating band of length \(\ell\) with distinct adjacent symbols requires at least \(\ell\) constant runs, contradicting 那 uniform bound as \(\ell\to\infty\).

**IDEA — exact limitation:** Constant-band templates remain outside 这 obstruction. Mixtures containing spatial periods 3 or higher, changing numbers of bands, unbounded interface blocks, 和 return times growing with the parameters 也 remain outside its hypotheses. The theorem excludes an entire essential-period-2 template class, without an assertion about unrestricted Lychrel existence.

## 5. THEOREM — saturated forced-overflow cycles for periods 3 和 4

The scope of **every classification in 这 section** is

\[
q_i\in\{1,\ldots,17\}\setminus\{9\}
\quad\text{at every phase},\qquad q_{t+1}=F_1(q_t).
\tag{5.1}
\]

The endpoints 0 和 18, coefficient 9, 和 mixed schedules containing \(F_0\) are excluded from 这 classification. Set

\[
x_i=q_i-9\mathbf1_{\{q_i\ge10\}}\in\{1,\ldots,8\}.
\]

Equation (2.5) becomes the ordinary integer sum \(q'_i=x_i+x_{i-1}\). Modulo 9,

\[
x'=\mathcal A x,\qquad \mathcal A=I+S,
\tag{5.2}
\]

where \(S\) is cyclic predecessor shift. The output coefficient lies between 2 和 16; it leaves (5.1) exactly when it equals 9, equivalently when a coordinate of \(\mathcal A x\) vanishes modulo 9.

**Proof of the lifting correspondence.** A recurrent residue cycle avoiding zero determines each coefficient word uniquely: take the ordinary integer adjacent sums of the preceding phase's representatives in \(\{1,\ldots,8\}\). Reduction modulo 9 recovers the next residue vector. Conversely, every recurrent coefficient cycle reduces to such a residue cycle. A shorter period of either representation would give the same shorter period of the other by these formulas. Thus recurrent-state counts 和 minimum temporal periods agree. An arbitrary initial coefficient word can 有 one transient step before its unique recurrent lift.

### 5.1 Spatial period 3

Let \(R=x_0+x_1+x_2\pmod9\). Exactly the following residue vectors avoid zero forever:

- \(R=0\pmod9\), with every coordinate nonzero;
- \(R=3\) or \(6\pmod9\), with every coordinate a unit modulo 9.

There are 92 recurrent labelled states: four temporal 2-cycles 和 fourteen temporal 6-cycles. Removing constant bands leaves **three temporal 2-cycles 和 thirteen temporal 6-cycles of genuine spatial period 3**.

**Proof.** Put \(J=I+S+S^2\), the matrix whose entries 都 equal 1. Direct multiplication modulo 9 gives

\[
\mathcal A^2=J+S,\qquad
\mathcal A^3=3J-I,\qquad
\mathcal A^6=I+3J.
\tag{5.3}
\]

Suppose first \(R\not\equiv0\pmod3\). A coordinate of \(x\) or \(\mathcal A x\) vanishes modulo 3. Indeed, if every coordinate of \(x\) is nonzero modulo 3 和 they are equal, their sum is zero modulo 3, contradicting the hypothesis. If those residues differ, a cyclically adjacent unequal pair sums to zero modulo 3. At a phase \(t\) with such a coordinate, (5.3) advances its value by \(3R_t\) every six steps. The total \(R_t\) stays unchanged after those six steps, 和 is nonzero modulo 3. The three values at \(t,t+6,t+12\) therefore include zero modulo 9. Such a vector cannot remain in (5.1).

If \(R\equiv0\pmod3\), (5.3) gives \(\mathcal A^3x=-x\). Consequently the complete avoidance conditions are

\[
x_i\ne0,\qquad R-x_i\ne0,\qquad R+x_i\ne0\pmod9.
\]

When \(R=0\), the conditions reduce to nonzero coordinates. Choose \(x_0,x_1\) in 64 ways, excluding the eight choices with \(x_0+x_1=0\); the sum fixes \(x_2\), giving 56 vectors.

When \(R=3\) or 6, the excluded values are exactly 0, 3, 和 6. Every coordinate must therefore be a unit. Their residues modulo 3 must agree: three residues from \(\{1,2\}\) sum to zero only when they are equal. For either common residue, choosing the first 两 of their three possible lifts fixes the third; 这 gives \(2\cdot3^2=18\) vectors for each total. Hence the count is \(56+18+18=92\).

The identity \(\mathcal A^3x=-x\) excludes odd temporal periods. Solving \(\mathcal A^2x=x\), using \(\mathcal A^2=J+S\), gives \(x_i-x_{i-1}=R\), hence

\[
x=a(1,4,7)\pmod9,\qquad a=1,\ldots,8.
\]

Those eight states form four 2-cycles. The remaining 84 form fourteen 6-cycles. The eight constant states form one 2-cycle 和 one 6-cycle. Since 3 is prime, every remaining spatial period is exactly 3. \(\square\)

One explicit coefficient cycle is

\[
(10,13,7)\xrightarrow{F_1}(8,5,11)
\xrightarrow{F_1}(10,13,7).
\]

### 5.2 Spatial period 4

Every recurrent vector is in the image of \(\mathcal A\), so its alternating sum is zero modulo 9. On 那 subspace define, in \(\mathbb Z/9\mathbb Z\),

\[
M=\frac{x_0+x_1+x_2+x_3}{4},\qquad
U=x_0-x_2,\qquad V=x_1-x_3.
\]

Division by 2 or 4 means multiplication by its inverse modulo 9. Then

\[
x=\left(M+\frac U2,M+\frac V2,M-\frac U2,M-\frac V2\right),
\]

\[
M'=2M,\qquad
\binom{U'}{V'}=D\binom UV,\qquad
D=\begin{pmatrix}1&-1\\1&1\end{pmatrix}.
\tag{5.4}
\]

Call \((U,V)\) primitive when its coordinates are 不都 divisible by 3. Set \(P=UV(U-V)(U+V)\pmod9\). Exactly the following four disjoint classes avoid zero forever:

| Conditions | Recurrent states |
|---|---:|
| \(M\) a unit; \(U,V\in3\mathbb Z/9\mathbb Z\) | 54 |
| \(M=0\); \((U,V)\) primitive; \(P\ne0\) | 48 |
| \(M\in\{3,6\}\); \((U,V)\) primitive; \(P=0\) | 48 |
| \(M\in\{3,6\}\); \(U=V=0\) | 2 |

There are therefore 152 recurrent labelled states: the constant temporal 2-cycle 和 6-cycle, plus **six temporal 24-cycles of genuine spatial period 4**.

**Proof of the matrix periods.** For \(J_0(U,V)=(-V,U)\), direct multiplication gives

\[
D^2=2J_0,\quad D^6=J_0,\quad D^8=7I,\quad D^{24}=I\pmod9.
\]

Modulo 3, the orbit of \((1,0)\) is

\[
(1,0),(1,1),(0,2),(1,2),(2,0),(2,2),(0,1),(2,1),(1,0).
\]

It 有 every nonzero vector modulo 3, so every primitive vector's period is divisible by 8. Since \(D^{8k}=7^k I\) 和 7 有 order 3 modulo 9, a primitive vector 有 exact period 24. A nonzero vector divisible by 3 有 exact period 8.

也 \(P(D(U,V))=-4P(U,V)\). For a primitive vector, exactly one of \(U,V,U-V,U+V\) is divisible by 3. The other three are units, so \(P=0\pmod9\) means 那 factor equals zero modulo 9. Thus the primitive zero set of \(P\) is exactly the four lines \(U=0,V=0,U=V,U=-V\). Each 有 six primitive vectors, with empty primitive intersections: 24 in total. Since primitive periods are 24, these 24 点 form one orbit. The remaining \(81-9-24=48\) primitive vectors 有 \(P\ne0\).

**Proof of every avoidance case.**

1. If \(M\) is a unit 和 \(U,V\) are divisible by 3, every coordinate is congruent to \(M\ne0\pmod3\). Zero is impossible. The count is \(6\cdot9=54\).
2. If \(M\) is a unit 和 \((U,V)\) is primitive, at least one pair \(M\pm U/2\) or \(M\pm V/2\) 有 a coordinate divisible by 3. Under eight steps, a coordinate \(z=M+N\) becomes \(4M+7N=7z-3M\). For \(3\mid z\), 这 is \(z-3M\pmod9\). At eight-step intervals, the mean stays unchanged modulo 3. Thus three such phases include zero. Every vector in 这 case eventually reaches a zero.
3. If \(M=0\) 和 \((U,V)\) is primitive, coordinates are \(\pm U/2,\pm V/2\). The orbit with \(P=0\) meets an axis, giving a zero. An orbit with \(P\ne0\) never meets either axis, since multiplication by \(-4\) preserves nonzero \(P\). Exactly 48 vectors survive.
4. If \(M=3\) or 6 和 \((U,V)\) is primitive with \(P=0\), a value of \(U\) divisible by 3 must equal zero modulo 9; its coordinate pair then equals \(M,M\). A unit \(U\) gives coordinates nonzero modulo 3. The identical explicit alternatives for \(V\) are: \(V=0\) gives \(M,M\), 和 unit \(V\) gives nonzero coordinates modulo 3. Therefore every phase survives. The count is \(2\cdot24=48\).
5. If \(M=3\) or 6 和 \((U,V)\) is primitive with \(P\ne0\), its modulo-3 orbit reaches \(U=0\pmod3\). The condition \(P\ne0\) forces \(U\in\{3,6\}\pmod9\) there. Since \(U/2\in\{3,6\}\), one of \(M+U/2,M-U/2\) equals zero. Every vector in 这 case eventually reaches a zero.
6. If \(M,U,V\) are divisible by 3, a vector initially avoiding zero uses only coordinates 3 和 6. A nonconstant cyclic word 有 an adjacent unequal pair, whose sum is zero modulo 9 at the next step. The constant words 3 和 6 survive; these correspond exactly to \(M\in\{3,6\},U=V=0\). The zero constant word fails.

These cases exhaust the mean 和 difference possibilities. The map on the alternating-sum-zero subspace is invertible: multiplication by 2 和 the matrix \(D\), with determinant 2, are invertible modulo 9. Its surviving states are consequently recurrent.

The eight constant states 有 temporal periods 2 和 6. Every other survivor 有 period 24. A primitive difference already requires 24; a nonzero difference divisible by 3 requires 8, combined with a unit mean of period 6, yielding \(\operatorname{lcm}(8,6)=24\). Thus \((152-8)/24=6\) nonconstant cycles occur. Period 2 cannot occur spatially in a nonconstant recurrent \(F_1\) state, by Section 4.1; their spatial period is therefore exactly 4. \(\square\)

## 6. THEOREM — actual clocks 和 failed extensions

### 6.1 At most three consecutive actual overflows

Let \(a=d_0+d_{L-1}\) be the actual outer coefficient. Overflow requires \(a\ge9\), since the final column receives at most one incoming carry. After an overflow, the new leading digit is 1 和 the new units digit is \(a\bmod10\), so the new outer sum is

\[
a'=1+(a\bmod10).
\]

The cases are explicit:

- \(a=9\) gives \(a'=10\), then an overflow gives 1, which prevents another overflow.
- \(10\le a\le17\) gives \(1\le a'\le8\), which prevents another overflow.
- \(a=18\) gives 9, then 10, then 1 if each permitted overflow occurs.

Thus the maximum is three. It is attained by

\[
9129\to18348\to102729\to1029930\to1429131,
\]

with lengths \(4,5,6,7,7\). Consequently, every forced-\(F_1\) cycle in Section 5 is incompatible with an actual forever-overflowing integer orbit. The displayed example reaches a palindrome at step 11; it fails the Lychrel condition. The script continues it for 1000 steps solely as a numerical check. \(\square\)

### 6.2 Coefficient 9 invalidates the unrestricted alternating-sum extension

For a period-4 block without 9, equation (2.5) gives

\[
F_1(q)_0-F_1(q)_1+F_1(q)_2-F_1(q)_3=0.
\]

Each \(f(q_i)\) occurs once with each sign. Extending 这 identity to blocks containing 9 is false. The explicit counterexample is

\[
q=(10,9,0,0),\quad A=(0,1,1,0),\quad B=(1,0,0,0),
\]

\[
U=(0,0,1,0),\qquad V=(0,9,0,1),\qquad
F_1(q)=(1,0,10,0).
\]

Its alternating sum is 11. The carries satisfy every recurrence from Section 2. Thus the exclusion of 9 in Section 5 is mathematically necessary for its stated linear reduction.

### 6.3 Some saturated blocks leave the alphabet

The proposed extension “every saturated period-3 block stays saturated under \(F_1\)” fails:

\[
(2,4,6)\xrightarrow{F_1}(8,6,10)
\xrightarrow{F_1}(9,14,7).
\]

The second image 有 9. The candidate is rejected at 那 step; the saturated formula cannot be continued past it without switching to the exact directional-carry map.

### 6.4 A period-3 constraint for mixed schedules

For a period-3 block without 9, set \(k=s_0+s_1+s_2\). Formula (2.5) gives

\[
F_0(q)_i=2q_i-21s_i+k,
\]

\[
F_0(q)_i-F_0(q)_j\equiv2(q_i-q_j)\pmod{21},
\qquad
\sum_iF_0(q)_i=2\sum_iq_i-18k.
\]

These follow by writing \(s_{i-1}+s_{i+1}=k-s_i\), then subtracting or summing. After six consecutive \(F_0\) steps whose inputs avoid 9, pairwise differences return modulo 21 因为 \(2^6\equiv1\pmod{21}\). 这 is a necessary congruence, without a sufficient return condition.

## 7. IDEA — sharpest open question

Does there exist a finite family

\[
Q(k)=B\,w^k\,H\,(w^{\mathrm{rev}})^k\,B^{\mathrm{rev}},
\qquad |w|\in\{3,4\},
\]

with \(w\) of genuine spatial period \(|w|\), bounded fixed blocks, valid decimal realizations, 和 integers \(m,g>0\), such that

\[
T^m Q(k)=Q(k+g)
\]

for every sufficiently large \(k\), while every intermediate emitted digit word is nonsymmetric?

Here \(T\) denotes the exact normalize/refold map. Every intermediate overflow bit must come from its entire finite word. Coefficient 9 must retain its actual directional carries. The displayed family would need its intermediate guards 和 exponent updates 都 to close; a cycle of \(w\) alone cannot establish the claim.

For 这 single mirrored-band family, length accounting gives the necessary identity

\[
\#\{\text{overflows during the return}\}=2|w|g.
\]

**THEOREM — necessary lower bound.** Combining 那 identity with at most three consecutive overflows gives

\[
m\ge \left\lceil\frac{8|w|g}{3}\right\rceil.
\]

**Proof.** Write \(C=2|w|g\). Repeating the proposed return \(N\) times gives \(NC\) overflows in \(Nm\) steps. Those overflows need at least \(\lceil NC/3\rceil\) runs, separated by at least \(\lceil NC/3\rceil-1\) non-overflow steps. Thus \(Nm\ge NC+\lceil NC/3\rceil-1\) for every positive \(N\). If \(m<4C/3\), sufficiently large \(N\) contradicts 那 inequality. Therefore \(m\ge\lceil4C/3\rceil\), which gives the displayed bound. In particular, spatial period 3 requires \(m\ge8g\), 和 spatial period 4 requires \(m\ge\lceil32g/3\rceil\). \(\square\)

**IDEA — remaining scope:** The general mixed-clock recurrence classification for periods 3 和 4 remains open in 这 report. The forced-overflow classification in Section 5 supplies exact algebraic information, but its cycles alone cannot meet the finite-word clock requirement. The strongest unconditional construction obstruction obtained here is Section 4.3.

**LEAN-VERIFIED — comparison with prior accounting:** For the existing exact period-4 quotient-return setting, the repository's [`quotient_return_clock_gain`](lean/P196/Agent1PeriodicReturnClock/Agent1PeriodicReturnClock.lean) already supplies the stronger bound \(m\ge16g\). The elementary bound above extends immediately to period 3; the existing period-4 accounting remains stronger.

## 8. IDEA — reproducible numerical validation

The code below uses only Python's standard library. Its tasks are a 361-block period-2 carry audit, 1000-step checks of each displayed cycle representative, independent forward/reverse carry normalization, explicit rejected candidates, 和 the 1000-step ordinary-integer check of 9129. The checks use only the explicitly described small finite sets 和 trajectories. The ordinary-integer check reaches a palindrome; integer-orbit realizability of the periodic bulk cycles remains unestablished.

The code 和 recorded output are included directly so 这 report is self-contained.

### Complete executable check

Save the following block as `check_214.py`, then run `python3 check_214.py`.

```python
#!/usr/bin/env python3
"""Agent 214: finite audits of the proved period-two bulk formulas.

These are periodic interior column-sum maps, not finite integer orbits.
The classification is proved algebraically in REPORT_214.md; this file
checks its formulas and five cycle representatives independently.
"""

from itertools import product


def H(q, carry):
    """Carry after one base-ten column, for 0 <= q <= 18."""
    assert 0 <= q <= 18 and carry in (0, 1)
    return (q + carry) // 10


def periodic_carries(word):
    """Return every (A, B) solving the two directional cyclic recurrences.

    A[i+1] = H(word[i], A[i]); B[i] = H(word[i], B[i+1]).
    Indices are cyclic. An all-nine word permits either carry in each
    direction independently. Every other word synchronizes uniquely.
    """
    word = tuple(word)
    p = len(word)
    assert p > 0 and all(0 <= q <= 18 for q in word)
    forwards, backwards = [], []
    for start in (0, 1):
        A, carry = [], start
        for q in word:
            A.append(carry)
            carry = H(q, carry)
        if carry == start:
            forwards.append(tuple(A))
        B, carry = [None] * p, start
        for i in range(p - 1, -1, -1):
            carry = H(word[i], carry)
            B[i] = carry
        if carry == start:
            backwards.append(tuple(B))
    return tuple(product(forwards, backwards))


def exact_maps(word, A, B):
    """Exact stabilized bulk maps, with h=0 or h=1 global overflow."""
    word = tuple(word)
    p = len(word)
    F0 = tuple(
        2 * word[i] + A[i] + B[(i + 1) % p]
        - 10 * (A[(i + 1) % p] + B[i])
        for i in range(p)
    )
    F1 = tuple(
        word[i] + word[(i - 1) % p] + A[i] + B[i]
        - 10 * (A[(i + 1) % p] + B[(i - 1) % p])
        for i in range(p)
    )
    assert all(0 <= q <= 18 for q in F0 + F1)
    return F0, F1


def audit_period_two():
    carry_cases = 0
    for word in product(range(19), repeat=2):
        cases = periodic_carries(word)
        assert len(cases) == (4 if word == (9, 9) else 1)
        for A, B in cases:
            F0, F1 = exact_maps(word, A, B)
            assert F1[0] == F1[1]
            if word != (9, 9):
                assert B == (A[1], A[0])
                u = word[0] + A[0] - 10 * A[1]
                v = word[1] + A[1] - 10 * A[0]
                assert F0 == (2 * u, 2 * v)
                assert F1 == (u + v, u + v)
            else:
                expected = 18 - 9 * (A[0] + B[0])
                assert F0 == F1 == (expected, expected)
            carry_cases += 1
    print(f"period_two_words=361 directional_carry_cases={carry_cases} PASS")


def audit_cycles():
    for N0, expected_period in ((1, 30), (5, 30), (3, 10), (15, 10), (9, 10)):
        initial = (2 * (N0 % 10), 2 * (N0 // 10))
        word, first_return = initial, None
        for step in range(1, 1001):
            cases = periodic_carries(word)
            assert len(cases) == 1
            word, _ = exact_maps(word, *cases[0])
            residue = pow(2, step, 99) * N0 % 99
            expected = (2 * (residue % 10), 2 * (residue // 10))
            assert word == expected
            if word == initial and first_return is None:
                first_return = step
        assert first_return == expected_period
        print(
            f"N={N0} initial={initial} period={first_return} "
            f"after_1000={word} modular_checks=1000 PASS"
        )


def audit_nine_exception():
    word = (10, 9, 0, 0)
    cases = periodic_carries(word)
    assert cases == (((0, 1, 1, 0), (1, 0, 0, 0)),)
    _, F1 = exact_maps(word, *cases[0])
    assert F1 == (1, 0, 10, 0)
    alternating_sum = F1[0] - F1[1] + F1[2] - F1[3]
    assert alternating_sum == 11
    print(f"nine_exception_input={word} F1={F1} alternating_sum=11 PASS")


def cyclic_digits(word, reverse=False):
    """Normalize a periodic q word, with its unique periodic carry state."""
    assert any(q != 9 for q in word)
    order = list(range(len(word)))
    if reverse:
        order.reverse()
    carry = 0
    for i in order:
        carry = (word[i] + carry) // 10
    start = carry
    digits = [None] * len(word)
    for i in order:
        total = word[i] + carry
        digits[i] = total % 10
        carry = total // 10
    assert carry == start
    return digits


def f1_exact(word):
    left = cyclic_digits(word)
    right = cyclic_digits(word, reverse=True)
    return tuple(left[i] + right[i - 1] for i in range(len(word)))


def f1_saturated(word):
    assert all(0 < q < 18 and q != 9 for q in word)
    x = [q - 9 * int(q >= 10) for q in word]
    result = tuple(x[i] + x[i - 1] for i in range(len(word)))
    assert result == f1_exact(word)
    return result


def check_cycle(seed, expected_period, steps=1000):
    word = seed
    first_return = None
    phases = set()
    for t in range(steps):
        assert all(0 < q < 18 and q != 9 for q in word)
        phases.add(word)
        word = f1_saturated(word)
        if word == seed and first_return is None:
            first_return = t + 1
    assert first_return == expected_period
    assert len(phases) == expected_period
    print(f"seed={seed}; period={first_return}; checked={steps}; final={word}")
    return frozenset(phases)


def check_killed_candidate():
    seed = (2, 4, 6)
    word = seed
    for step in range(1, 3):
        word = f1_saturated(word)
    assert word == (9, 14, 7)
    print(f"rejected saturated candidate={seed}; step=2; state={word}")



def residue_catalog(p):
    """Generate exactly the analytically described classes, not a graph search."""
    states = set()
    if p == 3:
        for total in (0, 3, 6):
            for a, b in product(range(1, 9), repeat=2):
                c = (total-a-b) % 9
                x = (a, b, c)
                if c and (total == 0 or all(z % 3 for z in x)):
                    states.add(x)
    else:
        assert p == 4
        units = (1, 2, 4, 5, 7, 8)
        triples = [(M, U, V) for M in units
                   for U, V in product((0, 3, 6), repeat=2)]
        for U, V in product(range(9), repeat=2):
            if U % 3 == V % 3 == 0:
                continue
            invariant = U*V*(U-V)*(U+V) % 9
            if invariant:
                triples.append((0, U, V))
            else:
                triples.extend((M, U, V) for M in (3, 6))
        triples.extend((M, 0, 0) for M in (3, 6))
        for M, U, V in triples:
            states.add(((M+5*U) % 9, (M+5*V) % 9,
                        (M-5*U) % 9, (M-5*V) % 9))
    assert all(all(x) for x in states)
    return states


def audit_complete_classified_cycles(p):
    residues = residue_catalog(p)
    # A predecessor residue determines the unique integer coefficient lift.
    words = {tuple(x[i]+x[i-1] for i in range(p)) for x in residues}
    expected_counts = {3: {2: 8, 6: 84}, 4: {2: 2, 6: 6, 24: 144}}[p]
    assert len(words) == sum(expected_counts.values())
    counts, checked = {}, {}
    for seed in sorted(words):
        word, first = seed, None
        for t in range(1, 1001):
            word = f1_saturated(word)
            assert word in words
            if first is None and word == seed:
                first = t
        counts[first] = counts.get(first, 0) + 1
        checked[seed] = (first, word)
    assert counts == expected_counts
    print(f'p={p} classified_states={len(words)} '
          f'period_state_counts={dict(sorted(counts.items()))} '
          f'checked_steps_per_state=1000 PASS')
    return checked


def audit_constants():
    for scalar, period in ((0, 1), (18, 1), (6, 2), (2, 6), (9, 1)):
        word, first = (scalar,), None
        for t in range(1, 1001):
            cases = periodic_carries(word)
            if word == (9,):
                A, B = next((A, B) for A, B in cases
                            if A == (0,) and B == (1,))
            else:
                A, B = cases[0]
            word = exact_maps(word, A, B)[t % 2]
            if first is None and word == (scalar,):
                first = t
        assert first == period
        print(f'constant={scalar} period={period} checked=1000 final={word} PASS')


def audit_actual_integer():
    n, first_palindrome = 9129, None
    prefix = [n]
    for t in range(1, 1001):
        n += int(str(n)[::-1])
        if t <= 4:
            prefix.append(n)
        if first_palindrome is None and str(n) == str(n)[::-1]:
            first_palindrome = t
    assert prefix == [9129, 18348, 102729, 1029930, 1429131]
    assert first_palindrome == 11
    print(f'actual_integer_prefix={prefix}')
    print(f'9129: checked=1000 first_palindrome={first_palindrome} '
          f'final_digits={len(str(n))} PASS')


if __name__ == '__main__':
    audit_constants()
    audit_period_two()
    audit_cycles()
    audit_nine_exception()
    records3 = audit_complete_classified_cycles(3)
    records4 = audit_complete_classified_cycles(4)
    for seed in ((10, 13, 7), (7, 3, 8)):
        period, final = records3[seed]
        print(f'seed={seed}; period={period}; checked=1000; final={final}')
    representatives4 = ((8, 8, 5, 5), (11, 14, 11, 8), (8, 11, 10, 7),
                        (11, 8, 7, 10), (11, 11, 10, 10), (15, 16, 15, 14))
    orbits = set()
    for seed in representatives4:
        period, final = records4[seed]
        print(f'seed={seed}; period={period}; checked=1000; final={final}')
        word, phases = seed, set()
        for _ in range(period):
            phases.add(word)
            word = f1_saturated(word)
        orbits.add(frozenset(phases))
    assert len(orbits) == 6
    print('distinct spatial-period-4 cycles checked=6')
    check_killed_candidate()
    audit_actual_integer()
```

### Recorded output

```text
constant=0 period=1 checked=1000 final=(0,) PASS
constant=18 period=1 checked=1000 final=(18,) PASS
constant=6 period=2 checked=1000 final=(6,) PASS
constant=2 period=6 checked=1000 final=(14,) PASS
constant=9 period=1 checked=1000 final=(9,) PASS
period_two_words=361 directional_carry_cases=364 PASS
N=1 initial=(2, 0) period=30 after_1000=(8, 6) modular_checks=1000 PASS
N=5 initial=(10, 0) period=30 after_1000=(2, 14) modular_checks=1000 PASS
N=3 initial=(6, 0) period=10 after_1000=(6, 0) modular_checks=1000 PASS
N=15 initial=(10, 2) period=10 after_1000=(10, 2) modular_checks=1000 PASS
N=9 initial=(18, 0) period=10 after_1000=(18, 0) modular_checks=1000 PASS
nine_exception_input=(10, 9, 0, 0) F1=(1, 0, 10, 0) alternating_sum=11 PASS
p=3 classified_states=92 period_state_counts={2: 8, 6: 84} checked_steps_per_state=1000 PASS
p=4 classified_states=152 period_state_counts={2: 2, 6: 6, 24: 144} checked_steps_per_state=1000 PASS
seed=(10, 13, 7); period=2; checked=1000; final=(10, 13, 7)
seed=(7, 3, 8); period=6; checked=1000; final=(3, 8, 7)
seed=(8, 8, 5, 5); period=24; checked=1000; final=(11, 11, 8, 8)
seed=(11, 14, 11, 8); period=24; checked=1000; final=(5, 8, 5, 2)
seed=(8, 11, 10, 7); period=24; checked=1000; final=(5, 8, 13, 10)
seed=(11, 8, 7, 10); period=24; checked=1000; final=(8, 5, 10, 13)
seed=(11, 11, 10, 10); period=24; checked=1000; final=(8, 8, 4, 4)
seed=(15, 16, 15, 14); period=24; checked=1000; final=(6, 10, 6, 2)
distinct spatial-period-4 cycles checked=6
rejected saturated candidate=(2, 4, 6); step=2; state=(9, 14, 7)
actual_integer_prefix=[9129, 18348, 102729, 1029930, 1429131]
9129: checked=1000 first_palindrome=11 final_digits=424 PASS
```
