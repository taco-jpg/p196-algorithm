# Agent 210 — Direction 0: exact band algebra

Date: 2026-10-22. Source snapshot: `c6902ac6c366ce018e68a810f58b400dda07145a`.

## Answer in one paragraph

Decimal Lychrel existence remains unresolved by 这 report. **THEOREM:** the exact carry/refolding formulas below classify every constant symbol, including the carry-sensitive symbol \(9\), 和 give the complete noncritical bulk cycles. **THEOREM:** pairing consecutive steps without overflow improves the protected-core reserve from \(r-2t\) to \(r-\lceil3t/2\rceil\) for the \(6\leftrightarrow12\) cycle, 和 to \(r-\lceil5t/3\rceil\) for the \(2,4,8,16,14,10\) cycle. **THEOREM:** a pure complementary-band word with maximal runs of length at least \(3\) necessarily creates an additional interface symbol after one step, ruling out closure of 那 entire class under every individual step. Explicit finite-horizon decimal families were checked for \(1000\) steps using independent integer arithmetic, with zero palindromes 和 zero protected-core mismatches. The phase catalog 和 palindrome-preimage characterization already occur in the repository; 这 report credits 那 results, supplies complete written proofs, 和 develops the improved reserve estimates. **IDEA:** the unresolved task remains a bounded interface return with sustainable run lengths. An infinite return 和 a seed valid for every horizon remain missing from 这 finite-horizon estimates.

## Scope, provenance, 和 claim labels

**THEOREM** labels complete written proofs in 这 report. The additions remain unformalized; their status remains **THEOREM**, with complete written proofs. The repository sources below were inspected, 可是 their Lean builds 没有 rerun for 这 documentation change.

| Existing result used or recovered | Inspected source at the pinned snapshot |
|---|---|
| Constant-band normalization, complementary phase algebra, whole-template transition | [TemplateStep.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean), especially `norm_band`, `next_complement`, `actual_template_step` |
| Even phases, period \(2\), eventual period \(6\) | [BulkPhase.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/D20261015Agent3ComplementaryBulkBulkPhase/BulkPhase.lean) |
| Certificate phase parity 和 period divisibility | [CertificatePhases.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificatePhases.lean) |
| Exact palindrome-preimage criterion | [LychrelDigitSums.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/LychrelDigitSums.lean), `no_overflow_palindrome_has_no_carries`, `overflow_palindrome_digit_sums`, 和 their converses |
| Automatic complementary-template safety; earlier \(2k+2\) reserve bound | [NoPalStep.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent109TemplateStepSafety/NoPalStep.lean), `not_stepPal`, `template_orbit_safe` |
| Accepted return certificate implies a palindrome-free infinite orbit | [ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean) |

The bulk cycles 和 automatic safety therefore receive attribution to the existing sources. The quantitative contribution of 这 report consists of the paired-step lemma, its exact exceptional phases, 和 its \(3/2\) 和 \(5/3\) reserve bounds. Priority beyond the inspected repository comparison remains unassessed.

## 1. Definitions

Write the column-sum word from the units end as

\[
q=(q_0,\ldots,q_{L-1}),\qquad 0\le q_i\le18,
\qquad q_i=q_{L-1-i}.
\]

For a positive canonical integer, \(q_0>0\); an odd-length word also needs an even central coefficient. Define

\[
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,
\qquad e_i=q_i+c_i-10c_{i+1},
\qquad\delta=c_L.
\]

Append \(e_L=1\) when \(\delta=1\). The new word \(T(q)=q'\) 有 length \(L+\delta\), with

\[
q'_i=e_i+e_{L+\delta-1-i}.
\]

The notation \(s^r\) denotes a word with \(r\) copies of the symbol \(s\); arithmetic exponentiation uses its ordinary meaning outside word-power notation. Decimal digit concatenations below explicitly use most-significant-first order. A *protected core* means a specified interval on which a constant symbol can be guaranteed; maximality remains unnecessary.

## 2. THEOREM — Complete carry table 和 constant-run formulas

Every carry belongs to \(\{0,1\}\), by induction from \(c_0=0\) 和 the bound \(q_i+c_i\le19\). The complete table follows directly from division by \(10\):

| Symbol \(s\) | Incoming carry | Outgoing carry | Output digit |
|---|---:|---:|---:|
| \(0\le s\le8\) | \(0\) | \(0\) | \(s\) |
| \(0\le s\le8\) | \(1\) | \(0\) | \(s+1\) |
| \(9\) | \(0\) | \(0\) | \(9\) |
| \(9\) | \(1\) | \(1\) | \(0\) |
| \(10\le s\le18\) | \(0\) | \(1\) | \(s-10\) |
| \(10\le s\le18\) | \(1\) | \(1\) | \(s-9\) |

For \(s\ne9\), put

\[
h(s)=\begin{cases}0,&s\le8,\\1,&s\ge10,\end{cases}
\qquad a(s)=s-9h(s),\qquad F(s)=2a(s).
\]

Suppose \(q_i=s\) on \([A,B]\), 和 let

\[
A^*=L-1-B,\qquad B^*=L-1-A,
\qquad u=c_A,\qquad v=c_{A^*}.
\]

### Noncritical run, \(s\ne9\)

The first column resets the outgoing carry to \(h(s)\). Its digit equals

\[
e_A=a(s)+u-h(s),
\]

while every later digit through \(B\) equals \(a(s)\). Applying the table to the reflected run gives its first digit \(a(s)+v-h(s)\) 和 its later digits \(a(s)\).

For **\(\delta=0\)**, re-folding pairs \(i\) with \(L-1-i\), giving the exact identity

\[
\boxed{
q'_i=F(s)+(u-h(s))\mathbf1_{i=A}
             +(v-h(s))\mathbf1_{i=B}
\quad(A\le i\le B).
}
\tag{1}
\]

When \(A=B\), the 两 corrections occur at the same position; they must be added.

For **overflow**, re-folding pairs \(i\) with \(L-i\). If \(A+1\le i\le B\), then \(i>A\) 和 \(L-i>A^*\), so the 两 digits lie past the first column of their respective runs. Therefore

\[
\boxed{q'_i=F(s)\quad(A+1\le i\le B).}
\tag{2}
\]

### Critical run, \(s=9\)

A \(9\)-column preserves the incoming carry. Thus the original run emits \(9(1-u)\) throughout, 和 the reflected run emits \(9(1-v)\) throughout. Consequently

\[
\boxed{q'_i=18-9(u+v)}
\tag{3}
\]

on \([A,B]\) without overflow, 和 on \([A+1,B]\) with overflow. The three possible outputs 是 \(18,9,0\). A function of the symbol \(9\) alone cannot encode 这 possibilities. A central self-reflected \(9\)-run satisfies \(u=v\), so its bulk becomes \(18\) or \(0\). Distinct reflected runs can carry opposite bits 和 retain the symbol \(9\). 这 exhausts the carry cases. \(\square\)

## 3. THEOREM — Exact interface 和 endpoint algebra

### 3.1 \(\delta=0\), with a word avoiding \(9\)

Let \(h_i=h(q_i)\), with virtual values \(h_{-1}=h_L=0\). The carry resets imply

\[
e_i=q_i+h_{i-1}-10h_i.
\]

Symmetry gives the reflected digit

\[
e_{L-1-i}=q_i+h_{i+1}-10h_i.
\]

At the external positions, the virtual zero agrees with the initial carry; the terminal carry also equals zero in 这 branch. Hence

\[
\boxed{q'_i=F(q_i)+h_{i-1}-2h_i+h_{i+1}.}
\tag{4}
\]

Thus the correction to the bulk map equals a discrete second difference of the high/low indicator.

### 3.2 Overflow, including every critical interface case

For \(1\le i\le L-1\), write

\[
t=q_{i-1},\qquad s=q_i,\qquad u=c_i,\qquad v=c_{L-i}.
\]

Symmetry gives \(q_{L-i}=t\). The exact table follows:

| Left symbol \(t\) | Right symbol \(s\) | Re-folded value \(q'_i\) |
|---|---|---|
| \(t\ne9\) | \(s\ne9\) | \(a(t)+a(s)\) |
| \(t=9\) | \(s\ne9\) | \(s+9+u-19h(s)\) |
| \(t\ne9\) | \(s=9\) | \(t+9+v-19h(t)\) |
| \(t=9\) | \(s=9\) | \(18-9(u+v)\) |

**Proof of the four rows.** In the first row, the incoming carries at the output positions equal \(h(t),h(s)\), 和 their outgoing carries equal \(h(s),h(t)\). Summing the digits gives

\[
s+h(t)-10h(s)+t+h(s)-10h(t)=a(s)+a(t).
\]

In the second row, the \(s\)-digit equals \(s+u-10h(s)\). Its reflected \(9\)-digit receives carry \(h(s)\), giving \(9-9h(s)\); their sum gives the displayed value. In the third row, the \(9\)-digit receives carry \(h(t)\), giving \(9-9h(t)\), while the reflected \(t\)-digit equals \(t+v-10h(t)\). In the fourth row the digits equal \(9-9u\) 和 \(9-9v\). The four rows exhaust the cases.

The external coefficients satisfy

\[
\boxed{
q'_0=q'_L=e_0+1=q_0+1-10c_1
=\begin{cases}
q_0-9,&q_0\ge10,\\
10,&q_0=9.
\end{cases}}
\tag{5}
\]

The case \(q_0\le8\) cannot overflow: the last column equals \(q_0\) 和 resets its outgoing carry to zero. For a word avoiding \(9\), formulas (5) 和 the first interface row reduce to

\[
q'_0=q'_L=a(q_0),\qquad
q'_i=a(q_{i-1})+a(q_i)\quad(1\le i\le L-1).
\tag{6}
\]

Remote \(9\)-runs 不 affect the first interface row when its 两 adjacent symbols avoid \(9\). \(\square\)

## 4. THEOREM — Complete bulk dynamics 和 phase obstructions

The symbol map 有 the following complete table:

| Symbol \(s\) | Stable digit \(a(s)\) | Bulk image \(F(s)\) |
|---|---|---|
| \(0\) | \(0\) | \(0\) |
| \(1\) | \(1\) | \(2\) |
| \(2\) | \(2\) | \(4\) |
| \(3\) | \(3\) | \(6\) |
| \(4\) | \(4\) | \(8\) |
| \(5\) | \(5\) | \(10\) |
| \(6\) | \(6\) | \(12\) |
| \(7\) | \(7\) | \(14\) |
| \(8\) | \(8\) | \(16\) |
| \(9\) | Carry-dependent | \(18-9(u+v)\) |
| \(10\) | \(1\) | \(2\) |
| \(11\) | \(2\) | \(4\) |
| \(12\) | \(3\) | \(6\) |
| \(13\) | \(4\) | \(8\) |
| \(14\) | \(5\) | \(10\) |
| \(15\) | \(6\) | \(12\) |
| \(16\) | \(7\) | \(14\) |
| \(17\) | \(8\) | \(16\) |
| \(18\) | \(9\) | \(18\) |

The complete cycle list:

\[
(0),\qquad (18),\qquad (6,12),\qquad (2,4,8,16,14,10).
\tag{7}
\]

Every odd noncritical symbol enters an even cycle after one step. The displayed table exhausts the \(18\) noncritical symbols, giving a complete finite classification rather than a conjectural pattern.

For any \(m\ge0\), repeated substitution yields

\[
\boxed{
F^m(s)=2^m s-18\sum_{j=0}^{m-1}2^{m-1-j}h(F^j(s)).
}
\tag{8}
\]

For \(1\le s\le17\), \(s\ne9\), each iterate remains in 那 interval 和 equals the least positive residue of \(2^m s\pmod{18}\). The equation follows by induction: multiplying the expression for \(m\) by \(2\) 和 subtracting \(18h(F^m(s))\) gives the expression for \(m+1\).

For \(0\le s\le8\), its complement \(18-s\) lies in \([10,18]\), so

\[
F(18-s)=2(18-s)-18=18-2s=18-F(s).
\]

For \(10\le s\le18\), the complement lies in \([0,8]\), so

\[
F(18-s)=2(18-s)=18-(2s-18)=18-F(s).
\]

Thus complementary phases remain complementary.

An ordered return of a designated surviving bulk label requires \(F^m(s)=s\). An odd noncritical phase cannot return. A \(6\) or \(12\) phase requires \(2\mid m\); a phase in the other nontrivial cycle requires \(6\mid m\). Allowing an unordered complementary pair changes the label requirement to arbitrary \(m\) for \(\{6,12\}\), 和 \(3\mid m\) for the other pairs. 这 statements concern label return only; interface return 和 run-length return remain separate requirements. \(\square\)

## 5. THEOREM — Improved protected-core reserve

### 5.1 Generic propagation

Let \(N_0(t)\) count the steps without overflow among the first \(t\) steps. An initial noncritical run \(s\) on \([A,B]\) retains the protected core

\[
\boxed{[A+t,\ B-N_0(t)]}
\tag{9}
\]

with symbol \(F^t(s)\), whenever 那 interval remains nonempty. Its length equals

\[
r-t-N_0(t)=r-2N_0(t)-N_1(t)\ge r-2t.
\]

**Proof.** A step without overflow removes one boundary position at each end by (1). An overflowing step removes the left boundary position by (2). The image of a noncritical symbol remains noncritical. Induction adds 那 endpoint changes. The lengths decrease with each step, so a nonempty final interval ensures the necessary earlier intervals existed. \(\square\)

### 5.2 Paired-step improvement, with sharp exceptional phases

Suppose \(r\ge3\), \(s\notin\{4,9,14\}\), 和 the next 两 steps 都 satisfy \(\delta=0\). Then

\[
\boxed{q^{(2)}_i=F^2(s)\quad(A+1\le i\le B-1).}
\tag{10}
\]

Thus the 两 steps together consume one cell at each end, rather than the generic allowance of 两 cells.

**Proof with every endpoint case.** After the first step, the interior equals \(F(s)\). Since \(r\ge3\), the endpoint formulas from (1) separate:

\[
q'_A=F(s)+u-h(s),\qquad q'_B=F(s)+v-h(s),
\qquad u,v\in\{0,1\}.
\]

For \(0\le s\le8\), each endpoint lies in \(\{2s,2s+1\}\). For \(10\le s\le18\), each endpoint lies in \(\{2s-19,2s-18\}\). The reset classes:

| Starting phase | Possible endpoint values after one step | Reset behavior |
|---|---|---|
| \(s=0,1,2,3\) | \(2s,2s+1\) | 都 below \(9\), matching \(F(s)\) |
| \(s=4\) | \(8,9\) | \(9\) can retain an external carry |
| \(s=5,6,7,8\) | \(2s,2s+1\) | 都 above \(9\), matching \(F(s)\) |
| \(s=10,11,12,13\) | \(2s-19,2s-18\) | 都 below \(9\), matching \(F(s)\) |
| \(s=14\) | \(9,10\) | \(9\) can retain an external carry |
| \(s=15,16,17,18\) | \(2s-19,2s-18\) | 都 above \(9\), matching \(F(s)\) |

Outside \(4,14\), each endpoint therefore resets its outgoing carry to \(h(F(s))\). During the second step, every cell of the first-step interior receives 那 stabilized carry. Its reflected cell receives the same stabilized carry, including at the 两 ends of the interior. The 两 output digits each equal \(a(F(s))\), giving \(F^2(s)\). \(\square\)

**THEOREM — The exceptions cannot be removed.** 这 realizable symmetric words give counterexamples; indices start at zero:

\[
\begin{aligned}
[1,16,4,4,4,4,4,4,16,1]
&\longmapsto[3,12,9,8,8,8,8,9,12,3]\\
&\longmapsto[7,4,9,17,16,16,17,9,4,7],
\end{aligned}
\]

\[
\begin{aligned}
[1,2,14,14,14,14,14,14,2,1]
&\longmapsto[2,5,9,10,10,10,10,9,5,2]\\
&\longmapsto[4,11,9,1,2,2,1,9,11,4].
\end{aligned}
\]

The carry table directly gives terminal carry zero in each displayed transition. The original run occupies indices \(2,\ldots,7\). At indices \(3,6\), the second output equals \(17\) instead of \(F^2(4)=16\), or \(1\) instead of \(F^2(14)=2\). 这 counterexamples refute the unrestricted paired-step claim.

### 5.3 Exact accounting for selected pairs

Select \(M\) disjoint chronological pairs of steps of type \(00\), each beginning in a bulk phase outside \(\{4,14\}\). Apply (10) on 那 pairs 和 (1)–(2) elsewhere. Then the resulting core occupies

\[
\boxed{[A+t-M,\ B-N_0(t)+M]}
\tag{11}
\]

with length

\[
\boxed{r-t-N_0(t)+2M.}
\tag{12}
\]

Each selected pair saves one cell at each end relative to (9). For a nonempty resulting core, a selected pair begins with length at least \(3\), as required in (10). Its intermediate first-step core equals its pair-end core in position, so the intermediate core remains nonempty. The proof uses a block decomposition of each actual finite overflow word; ordinary-orbit realization of abstract schedules remains outside the theorem.

### 5.4 Uniform \(3/2\) reserve for \(0,6,12,18\)

这 cycles never encounter \(4\) or \(14\). In each maximal zero block of length \(k\), pair successive zeros 和 take

\[
M=\sum\left\lfloor\frac{k}{2}\right\rfloor,
\qquad U=N_0-2M.
\]

The number \(U\) counts odd-length zero blocks. There cannot be more such blocks than zero steps, or more than \(N_1+1\) blocks in total. Therefore

\[
U\le\min(N_0,N_1+1)
\le\left\lfloor\frac{t+1}{2}\right\rfloor.
\]

Equation (12) gives

\[
\boxed{\text{protected length}\ \ge r-\left\lceil\frac{3t}{2}\right\rceil.}
\tag{13}
\]

The guaranteed length decreases by \(2\) on a first zero, by \(0\) on its paired second zero, 和 by \(1\) on overflow. Positive final length therefore also ensures the earlier paired-step applications 有 valid positive cores.

### 5.5 Uniform \(5/3\) reserve for the other even cycle

Along \((2,4,8,16,14,10)\), the exceptional phases \(4,14\) occur three steps apart. Partition the chronological step positions into triples, followed by a remainder of length \(0,1,2\).

Within a triple containing at most 两 zero steps, leave them unpaired: at most 两 zeros remain unmatched. In a triple \(000\), the 两 adjacent possible pair-start positions cannot 都 begin at an exceptional phase. Select an eligible pair, leaving one unmatched zero. The selection gives disjoint pairs across different triples.

Consequently

\[
N_0-2M\le2\left\lfloor\frac t3\right\rfloor+(t\bmod3)
=\left\lceil\frac{2t}{3}\right\rceil.
\]

Using (12) gives

\[
\boxed{\text{protected length}\ \ge r-\left\lceil\frac{5t}{3}\right\rceil.}
\tag{14}
\]

The estimate holds for every starting phase in 那 cycle. Neither (13) nor (14) asserts an optimal erosion rate. A phase-dependent maximum matching of eligible \(00\) pairs can give a larger protected core on an actual trajectory. \(\square\)

## 6. THEOREM — Interface-free complementary closure cannot work

Fix \(1\le c\le8\), with \(H=18-c\). Consider adjacent runs of \(c,H\), each of length at least \(2\).

For a **low-to-high interface without overflow**, the final low column receives carry \(0\) on its original side 和 carry \(1\) on its reflected side. Its re-folded value equals \(c+(c+1)=2c+1\). The first high column receives carries \(0,1\), giving \((H-10)+(H-9)=17-2c\).

For a **high-to-low interface without overflow**, the final high column receives carries \(1,0\), giving \(17-2c\). The first low column receives carries \(1,0\), giving \(2c+1\).

For an **overflowing low-to-high interface**, the high digit receives carry \(0\), 和 the reflected low digit receives carry \(1\), giving \((H-10)+(c+1)=9\). For an **overflowing high-to-low interface**, the low digit receives carry \(1\), 和 the reflected high digit receives carry \(0\), again giving \((c+1)+(H-10)=9\).

The bulk values 是 the distinct even numbers \(2c,18-2c\). The interface values remain odd when \(\delta=0\), 和 equal \(9\) with overflow. Therefore:

> **THEOREM.** A symmetric word using precisely \(c,18-c\), containing the 两 symbols, 和 having every maximal run of length at least \(3\), produces at least three distinct symbols after one step.

**Proof of the final assertion.** Each run retains a nonempty bulk core by (1) or (2), so the 两 distinct even bulk symbols 都 occur. An interface contributes a symbol outside 那 pair by the four carry cases above. \(\square\)

这 rules out a class closed under each individual step using only pure complementary bands 和 zero-width interfaces. It 不 rule out a multi-step return allowing intermediate finite defect blocks.

**THEOREM — A broader symbol-only obstruction.** For any word avoiding \(9\), with \(\delta=0\), exact componentwise evolution \(q'_i=F(q_i)\) at every position forces \(q_i\le8\) everywhere 和 therefore gives a palindromic digit output.

**Proof.** By (4), the first differences of \(h_i\) must be constant. The boundary conditions \(h_{-1}=h_L=0\) force 那 constant to equal zero, hence \(h_i=0\) everywhere. Every carry then equals zero, so the output word equals the symmetric word \(q\). Conversely, coefficients at most \(8\) give zero carries 和 exact componentwise evolution. \(\square\)

## 7. THEOREM — Exact palindrome condition 和 finite-horizon families

### 7.1 Existing palindrome criterion, with a complete carry proof

For a symmetric column word with \(q_0>0\), the canonical digit output forms a palindrome exactly when

\[
\boxed{
(\forall i,\ q_i\le9)
\quad\text{or}\quad
(q_0=11\ \land\ \forall i,\ q_i\in\{0,11\}).
}
\tag{15}
\]

**THEOREM — The positive outer coefficient matters for canonical output.** The artificial word \(q=(0,1,0)\) emits the symmetric fixed-width word \(010\), whereas its canonical integer output \(10\) fails symmetry. 这 direct calculation refutes an extension of the canonical-output statement omitting \(q_0>0\). For arbitrary symmetric coefficient words, (15) instead characterizes symmetry of the raw fixed-width emitted word. With \(q_0>0\), the final original-column digit remains positive when \(\delta=0\), while overflow appends a leading \(1\), so raw output 和 canonical output agree.

**\(\delta=0\), necessity.** Starting with \(c_0=c_L=0\), suppose inward induction has reached \(c_i=c_{L-i}=0\). Symmetry of input 和 output gives

\[
q_i-10c_{i+1}=e_i=e_{L-1-i}=q_i+c_{L-1-i}.
\]

Thus \(10c_{i+1}+c_{L-1-i}=0\), forcing each carry to vanish. Induction reaches the center 和 covers every carry. Hence \(q_i=e_i\le9\).

**\(\delta=0\), sufficiency.** If every \(q_i\le9\), induction from \(c_0=0\) gives zero carries throughout. The output equals the symmetric word \(q\).

**Overflow, necessity.** Palindromic endpoints require \(e_0=e_L=1\), so \(q_0\in\{1,11\}\). The value \(1\) cannot produce a terminal carry 因为 \(q_{L-1}=1\). Thus \(q_0=11\).

Suppose \(q_{i-1}\in\{0,11\}\), 和 put \(b=q_{i-1}/11\). A \(0\)-column resets its outgoing carry to zero; an \(11\)-column resets it to one. Therefore

\[
c_i=c_{L-i+1}=b.
\]

Equality of output digits at \(i,L-i\) gives

\[
q_i+b-10c_{i+1}
=q_{i-1}+c_{L-i}-10b=b+c_{L-i},
\]

so

\[
q_i=10c_{i+1}+c_{L-i}\in\{0,1,10,11\}.
\]

For \(q_i=0\), the 两 reflected columns emit zero carries, consistent with the equation. For \(q_i=1\), 那 carries also equal zero, contradicting \(q_i=1\). For \(q_i=10\), the 两 outgoing carries equal one, forcing the right side to equal \(11\), a contradiction. For \(q_i=11\), 那 carries equal one 和 the equation holds. Induction therefore restricts every coefficient to \(0\) or \(11\).

**Overflow, sufficiency.** Write \(q_i=11b_i\), where \(b_i\in\{0,1\}\), \(b_i=b_{L-1-i}\), 和 \(b_0=1\). Carry resetting gives

\[
e_0=e_L=1,\qquad e_i=b_i+b_{i-1}\quad(1\le i\le L-1).
\]

Then \(e_{L-i}=b_{i-1}+b_i=e_i\), proving symmetry. \(\square\)

**THEOREM — Safety from complementary coefficients.** If \(q\) contains \(c\) 和 \(18-c\), with \(1\le c\le17\), \(c\ne9\), its next output cannot be a palindrome. One coefficient lies above \(9\), excluding the first branch of (15), while the other lies in \(\{1,\ldots,8\}\), excluding the second branch. Run length, interface content, 和 center location 不 enter 这 one-step argument. \(\square\)

### 7.2 Explicit families 和 their quantifiers

For \(c\in\{2,6\}\), define the positive integer by most-significant-first decimal concatenation

\[
N_{c,r}=\overline{c^r\,9^r\,(9-c)^r\,0^r}.
\tag{16}
\]

The leading digit equals \(c>0\), 和 the units digit equals zero, so the initial integer cannot be palindromic. Direct pairing gives its units-first column word

\[
q^{(0)}=c^r\,(18-c)^{2r}\,c^r.
\]

**THEOREM.** For every integer \(T\ge0\), the choices

\[
\begin{aligned}
c=6:&\qquad r\ge\left\lceil\frac{3T}{2}\right\rceil+1,\\
c=2:&\qquad r\ge\left\lceil\frac{5T}{3}\right\rceil+1
\end{aligned}
\tag{17}
\]

guarantee nonpalindromic orbit values at every time \(0,1,\ldots,T+1\).

**Proof.** Equations (13)–(14) preserve nonempty cores of each initial complementary band through time \(T\). The middle band begins with length \(2r\), so the same sufficient reserve applies to it. Complementarity persists under \(F\). At each time \(0\le t\le T\), the safety corollary excludes a palindrome at the next time. The initial value was excluded separately by its unequal endpoint digits. \(\square\)

For the reported checks, \(T=1000\), with \(r=1501\) for \(c=6\), 和 \(r=1668\) for \(c=2\). The numerical runs check times \(0\) through \(1000\); the written theorem additionally covers time \(1001\).

The quantifier supplied here 有 the form

\[
\forall T\ \exists N_T\ \forall t\le T+1:\quad
\operatorname{RA}^t(N_T)\ne\operatorname{rev}(\operatorname{RA}^t(N_T)).
\]

Decimal Lychrel existence requires

\[
\exists N\ \forall t\ge0:\quad
\operatorname{RA}^t(N)\ne\operatorname{rev}(\operatorname{RA}^t(N)).
\]

The first statement 不 imply the second. The constructed starting integers grow with the chosen horizon; a fixed finite starting word remains missing when the horizon tends to infinity.

## 8. Reproducible validation of the THEOREMS

The complete Python program below performs tests of the derived formulas. It checks:

- The raw fixed-width emitted-word symmetry criterion on every symmetric coefficient word of lengths \(1\) through \(6\): \(14478\) words, including artificial center-parity cases 和 zero outer coefficients. The canonical integer theorem retains \(q_0>0\).
- The exact run 和 interface formulas on the \(10467\) positive realizable words in 那 set.
- The paired-step lemma on \(288\) bounded test contexts, plus the explicit failures at \(4,14\).
- The pairing bound on \(20460\) short abstract binary schedules. 这 checks a combinatorial inequality; ordinary-orbit realizability of 那 schedules remains unasserted.
- Each family from (16) for \(1000\) steps, comparing the column implementation with direct Python integer reverse-add arithmetic at every step, 和 checking the designated protected intervals.

| Family | Initial digits | Digits at time \(1000\) | Overflow steps | Eligible \(00\) pairs | Minimum checked protected width | Palindromes at times \(0\ldots1000\) |
|---|---:|---:|---:|---:|---:|---:|
| \(6/12,\ r=1501\) | \(6004\) | \(6423\) | \(419\) | \(156\) | \(232\) | \(0\) |
| \(2/16,\ r=1668\) | \(6672\) | \(7079\) | \(407\) | \(135\) | \(345\) | \(0\) |

The widths in the table use the actual schedule 和 selected pairs via (12); the schedule-independent bounds in (17) only guarantee width at least one. The tests produced zero counterexamples to the stated theorems. The counterexamples to the stronger, unrestricted paired-step claim appear explicitly above 和 in the output below.

### Complete runnable code

Save the following code as `agent210_checks.py`, then execute `python3 agent210_checks.py` with Python 3.11 or later.

```python
#!/usr/bin/env python3
"""Agent 210: tests of derived formulas, with no candidate search."""
from hashlib import sha256
from itertools import product
from math import ceil
import sys

sys.set_int_max_str_digits(0)


def step(q):
    c, e = [0], []
    for s in q:
        carry, digit = divmod(s + c[-1], 10)
        c.append(carry)
        e.append(digit)
    if c[-1]:
        e.append(1)
    return [a + b for a, b in zip(e, reversed(e))], c, e


def h(s):
    assert s != 9
    return int(s >= 10)


def a(s):
    return s - 9 * h(s)


def f(s):
    return 2 * a(s)


def pair(n):
    d = [int(x) for x in reversed(str(n))]
    return [a + b for a, b in zip(d, reversed(d))]


def small_formula_checks():
    total = real = runs = interfaces = pals = overpals = 0
    for L in range(1, 7):
        for half in product(range(19), repeat=(L + 1) // 2):
            q = list(half) + list(half[:L // 2][::-1])
            qp, c, e = step(q)
            predicted = max(q) <= 9 or (q[0] == 11 and set(q) <= {0, 11})
            assert (e == e[::-1]) == predicted
            total += 1
            pals += predicted
            overpals += predicted and c[-1] == 1
            if q[0] == 0 or (L % 2 and q[L // 2] % 2):
                continue
            real += 1
            left = 0
            while left < L:
                right = left
                while right + 1 < L and q[right + 1] == q[left]:
                    right += 1
                s, u, v = q[left], c[left], c[L - 1 - right]
                if s == 9:
                    for i in range(left + c[-1], right + 1):
                        assert qp[i] == 18 - 9 * (u + v)
                elif c[-1]:
                    assert all(qp[i] == f(s) for i in range(left + 1, right + 1))
                else:
                    for i in range(left, right + 1):
                        assert qp[i] == (f(s) + (u-h(s))*(i == left)
                                         + (v-h(s))*(i == right))
                runs += 1
                left = right + 1
            if c[-1]:
                assert qp[0] == qp[-1] == q[0] + 1 - 10*c[1]
                for i in range(1, L):
                    t, s, u, v = q[i-1], q[i], c[i], c[L-i]
                    if t != 9 and s != 9:
                        expected = a(t) + a(s)
                    elif t == 9 and s != 9:
                        expected = s + 9 + u - 19*h(s)
                    elif t != 9 and s == 9:
                        expected = t + 9 + v - 19*h(t)
                    else:
                        expected = 18 - 9*(u+v)
                    assert qp[i] == expected
                    interfaces += 1
            elif 9 not in q:
                hs = [0] + [h(s) for s in q] + [0]
                assert qp == [f(s) + hs[i] + hs[i+2] - 2*hs[i+1]
                              for i, s in enumerate(q)]
    print(f"symmetric_words={total}; realizable_positive={real}; palindromes={pals}; overflow_palindromes={overpals}")
    print(f"run_instances={runs}; overflow_interfaces={interfaces}; failures=0")


def paired_step_checks():
    count = 0
    for s in range(19):
        if s in (4, 9, 14):
            continue
        for u in (0, 5, 9, 10, 16, 18):
            for v in (0, 9, 18):
                q = [1, v, u] + [s]*8 + [u, v, 1]
                q1, c1, _ = step(q)
                q2, c2, _ = step(q1)
                if c1[-1] == c2[-1] == 0:
                    assert q2[4:10] == [f(f(s))]*6
                    count += 1
    print(f"two_no_overflow_refinement_checks={count}; failures=0")
    for s, u in ((4, 16), (14, 2)):
        q = [1, u] + [s]*6 + [u, 1]
        q1, c1, _ = step(q)
        q2, c2, _ = step(q1)
        assert c1[-1] == c2[-1] == 0
        assert q2[3] != f(f(s)) and q2[6] != f(f(s))
        print(f"exception={s}; q0={q}; q1={q1}; q2={q2}; deltas=(0,0)")


def matching_checks():
    checked = 0
    for initial in (0, 2, 4, 6, 8, 10, 12, 14, 16, 18):
        for length in range(1, 11):
            for deltas in product((0, 1), repeat=length):
                phase, pending, pairs, zeros = initial, None, 0, 0
                for j, delta in enumerate(deltas):
                    if delta == 0:
                        zeros += 1
                        if pending is not None and pending[0] == j-1 and pending[1] not in (4, 14):
                            pairs += 1
                            pending = None
                        else:
                            pending = (j, phase)
                    else:
                        pending = None
                    phase = f(phase)
                loss = length + zeros - 2*pairs
                bound = ((3*length + 1)//2 if initial in (0, 6, 12, 18)
                         else (5*length + 2)//3)
                assert loss <= bound, (initial, deltas, loss, bound)
                checked += 1
    print(f"finite_schedule_bound_checks={checked}; failures=0")


def long_orbit(initial, r, horizon=1000):
    # Decimal digits, most significant first. This realizes complementary bands.
    seed_digits = str(initial)*r + "9"*r + str(9-initial)*r + "0"*r
    n = int(seed_digits)
    q = pair(n)
    other = 18-initial
    assert q == [initial]*r + [other]*(2*r) + [initial]*r
    assert seed_digits != seed_digits[::-1]
    intervals = [(0, r-1, initial), (r, 3*r-1, other), (3*r, 4*r-1, initial)]
    zeros = overflows = pairs = 0
    pending = None
    phase = initial
    smallest = r
    for j in range(horizon):
        qp, carries, output = step(q)
        delta = carries[-1]
        assert output != output[::-1]
        if delta == 0:
            zeros += 1
            if pending is not None and pending[0] == j-1 and pending[1] not in (4, 14):
                pairs += 1
                pending = None
            else:
                pending = (j, phase)
        else:
            overflows += 1
            pending = None
        phase = f(phase)
        t = j+1
        intervals = [(left, right, f(s)) for left, right, s in intervals]
        for left, right, s in intervals:
            lo = left + t - pairs
            hi = right - zeros + pairs
            assert lo <= hi
            assert all(x == s for x in qp[lo:hi+1]), (initial, t, lo, hi, s)
            smallest = min(smallest, hi-lo+1)
        # Independent integer arithmetic, not the column-sum implementation.
        n += int(str(n)[::-1])
        assert pair(n) == qp
        assert str(n) != str(n)[::-1]
        q = qp
    final_digits = str(n)
    print(f"family={initial}/{18-initial}; r={r}; steps={horizon}; initial_digits={4*r}; final_digits={len(final_digits)}")
    print(f"no_overflow={zeros}; overflow={overflows}; paired_00={pairs}; minimum_protected_width={smallest}; palindromes_times_0_to_{horizon}=0")
    print(f"final_integer_sha256={sha256(final_digits.encode()).hexdigest()}; arithmetic_and_core_failures=0")


if __name__ == "__main__":
    small_formula_checks()
    paired_step_checks()
    matching_checks()
    long_orbit(6, 1501)
    long_orbit(2, 1668)
```

### Actual output

```text
symmetric_words=14478; realizable_positive=10467; palindromes=2234; overflow_palindromes=14
run_instances=49041; overflow_interfaces=25104; failures=0
two_no_overflow_refinement_checks=288; failures=0
exception=4; q0=[1, 16, 4, 4, 4, 4, 4, 4, 16, 1]; q1=[3, 12, 9, 8, 8, 8, 8, 9, 12, 3]; q2=[7, 4, 9, 17, 16, 16, 17, 9, 4, 7]; deltas=(0,0)
exception=14; q0=[1, 2, 14, 14, 14, 14, 14, 14, 2, 1]; q1=[2, 5, 9, 10, 10, 10, 10, 9, 5, 2]; q2=[4, 11, 9, 1, 2, 2, 1, 9, 11, 4]; deltas=(0,0)
finite_schedule_bound_checks=20460; failures=0
family=6/12; r=1501; steps=1000; initial_digits=6004; final_digits=6423
no_overflow=581; overflow=419; paired_00=156; minimum_protected_width=232; palindromes_times_0_to_1000=0
final_integer_sha256=f94b80406753a0654bdf1b495736b5cf5262bdcb59a1fbc65f8d6499bde7e2d5; arithmetic_and_core_failures=0
family=2/16; r=1668; steps=1000; initial_digits=6672; final_digits=7079
no_overflow=593; overflow=407; paired_00=135; minimum_protected_width=345; palindromes_times_0_to_1000=0
final_integer_sha256=0ae84422487512a676aaafa48d25dc56f60808edcbf5f68b0f39732a70485ace; arithmetic_and_core_failures=0
```

## 9. IDEA — Sharpest open question

Can a finite set of realizable complementary-band states, with bounded exterior, interface, 和 center blocks, return under the exact carry-aware transition while keeping every intermediate band positive 和 returning the band-length vector with nonnegative net increments, at least one strictly positive?

For the \(6/12\) phases, the designated phase period must be even. For the other cycle, it must be divisible by \(6\). 这 basic phase conditions give weaker restrictions than the existing full certificate conditions: under the original admissibility conditions, [CertificateSaturation.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateSaturation.lean) already gives period at least \(42\) in the six-phase case. A phase-period calculation alone therefore 不 license a short full return.

The interface theorem identifies the necessary extra symbols: odd defects on a step without overflow, 和 \(9\) at an overflowing complementary interface. The critical-run formula identifies their retained carry state. The reserve theorem reduces the amount of initially long band needed for a finite check. A closed, sustainable interface system remains missing. An accepted certificate 和 a decimal Lychrel witness remain missing.
