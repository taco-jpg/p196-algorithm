# REPORT_203 — Seal constructions, exact carries, 和 the decimal obstruction

Agent **203**, direction **3**. Date: **2026-10-22**. Manuscript proofs; Lean verification: absent.

## Answer in one paragraph

**THEOREM.** The published base-11, base-17, 和 base-26 families admit complete carry proofs with return periods \(6,6,4\), respectively, each increasing both displayed run lengths by one while every intermediate phase remains nonpalindromic. Their common mechanism uses complementary digit runs whose column sum equals \(b-1\); that rule 也 works in decimal. The standard power-of-two family instead requires an exact doubling reset \(2\cdot2^j=b\), which base 10 fails; its decimal specialization \(10998900\) reaches a palindrome after ten steps. A separate counting obstruction shows that any finite collection of the repository's saturated states, which exclude coefficient \(9\), 有 a uniform bound on its number of \(9\)-coefficients; it therefore cannot represent a decimal version of the growing critical-band mechanism. **IDEA / unresolved reconstruction:** the opened original source reports a base-20 example longer than 200 digits but omits the witness, so 这 report supplies no reconstructed base-20 proof. Decimal existence remains open. Complete symbolic proofs, reproducible 1000-step checks, the source limitation, 和 a precise next question follow.

## Scope 和 source record

The mathematical statements labeled **THEOREM** below 有 full arithmetic proofs in 这 report. Numerical checks audit their transcription. **IDEA** labels proposed extensions or an unresolved reconstruction. 没有 **LEAN-VERIFIED** claim for 这 report. 没有 claim concerns a particular decimal orbit other than the explicitly displayed counterexample.

The primary record 是 David Seal's post of January 16, 1996, in the `rec.puzzles` discussion **Numeric Palindromes** [S1]. MathPages reproduces the sporadic seeds 和 representative phase tables [S2]. A longer reproduction includes the regular power-of-two family 和 the author's original caution about preliminary, hand-transcribed results [S3]. The carry proofs below were independently reconstructed from the digit data; the original caution 是 a reason to check every column.

| Base | Source supplies | Reconstruction here | Executed orbit audit |
|---:|---|---|---|
| 11 | Seed family 和 six phases | Complete, every \(n\ge0\) | 1000 steps for each \(n_0=0,1,2\) |
| 17 | Seed family 和 six phases | Complete, every \(n\ge0\) | 1000 steps for each \(n_0=0,1,2\) |
| 20 | Existence report; digits omitted | Unresolved source gap | 没有 claimed witness to test |
| 26 | Seed family 和 four phases | Complete, every \(n\ge0\) | 1000 steps for each \(n_0=0,1,2\) |
| \(2^k\) | Regular family | Complete symbolic proof, \(k\ge1\) | 1000 steps each for \(2,4,8,16,32\) |

**Notation.** Digit words run from most significant digit to units, unless a carry table explicitly says otherwise. A repeated symbol such as \(x^n\) denotes \(n\) copies of a digit; it 不是 exponentiation of its numerical value. Parenthesized expressions in digit strings denote single digits. Alphabet `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ` assigns `A=10`, through `Z=35`. Let \(T_b(w)\) denote ordinary base-\(b\) reversal 和 addition, discarding only leading zeroes of the reversed addend. Every arithmetic operation preserves the actual number's units zeroes.

For units-first indices, the complete local rule is

\[
q_i=d_i+d_{L-1-i},\qquad c_0=0,\qquad
q_i+c_i=e_i+b c_{i+1},\qquad
e_i\in\{0,\ldots,b-1\},\quad c_i\in\{0,1\}.
\]

An outgoing carry at the final column appends a leading digit \(1\). The bound \(q_i+c_i\le2b-1\) proves that these exhaust the carry cases.

## THEOREM: carry-neutral insertion lemma

Let base $b\ge2$. Let $A,B,C$ be finite base-$b$ digit strings, with $|A|=|C|=p$, $A$ starting nonzero. Let digits $x,y$ satisfy $x+y=b-1$. Define $W(n)=A x^n B y^n C$ for $n\ge0$.

Use fixed-width addition on these three blocks, always from units toward the leading end:

1. Add $C+\operatorname{rev}(A)$ with initial carry $0$, yielding width-$p$ output $S$ 和 terminal carry $\alpha$.
2. Add $B+\operatorname{rev}(B)$ with initial carry $\alpha$, yielding width-$|B|$ output $M$ 和 terminal carry $\beta$.
3. Add $A+\operatorname{rev}(C)$ with initial carry $\beta$, yielding width-$p$ output $U$ 和 terminal carry $\gamma$. Define $P=U$ when $\gamma=0$, 和 $P=1U$ when $\gamma=1$.

Define $r=b-1$ when $\alpha=0$ 和 $r=0$ when $\alpha=1$; define $\ell=b-1$ when $\beta=0$ 和 $\ell=0$ when $\beta=1$. Then

$$T_b(W(n))=P\ell^n M r^n S.$$

Proof: Since equal-length outer blocks align under reversal, both variable runs consist entirely of columns with sum $x+y=b-1$. Incoming carry $0$ gives output $b-1$ 和 carry $0$; incoming carry $1$ gives output $0$ 和 carry $1$. These exhaust the possible carry cases, 因为 a sum of 两个 digits plus an incoming binary carry is at most $2b-1$. Iterating the applicable case through each run transmits its carry unchanged. The suffix calculation determines $\alpha$; the right run transmits $\alpha$; the middle calculation determines $\beta$; the left run transmits $\beta$; the prefix calculation determines $\gamma$. The possible final carry appears as the leading digit $1$. 这 gives the displayed equality for every $n$, including $0$.

The lemma 也 works in base 10: complementary digits $0,9$ produce column sum $9$, transmitting incoming carry unchanged. The lemma itself supplies no arithmetic obstruction to decimal examples.

## Definitions for the explicit constructions

Letters `A,...,G` denote digits `10,...,16`. Digit strings below 都 run most-significant first. For each base, define $W_j(n)=A_j x_j^n B_j y_j^n C_j$. Parameters $n\ge0$ are valid. Phase index is $j=0,\ldots,5$.

## THEOREM: base 11 six-step return

$$T_{11}^6(W_0(n))=W_0(n+1).$$

Every intermediate phase 不是 palindrome. Therefore every $W_0(n)$ 是 base-11 Lychrel number.

| Phase | $A_j$ | $x_j$ | $B_j$ | $y_j$ | $C_j$ |
|---|---|---|---|---|---|
| 0 | `1246277` | `A` | `A170352495681825A5026571A506181864A5143171` | `0` | `0872542` |
| 1 | `3698A48` | `0` | `0883768431399986541A1092545899A41337673890` | `A` | `8498963` |
| 2 | `7286895` | `A` | `1757424762898860994812839A1688872685237661` | `0` | `5996816` |
| 3 | `1246277` | `A` | `A331374A51557661297853458882266745249484123` | `0` | `0872542` |
| 4 | `3698A48` | `0` | `2546113376A23184075296A356A3923196843105462` | `A` | `8498963` |
| 5 | `7286895` | `A` | `509012685283646802A6928602A8636492476220905` | `0` | `5996816` |

### Complete fixed-block carry certificate

For each row, $S,M,P$ are the outputs in the lemma. The carry strings list **outgoing carries** from least-significant column to most-significant column. Each digit is checked by $q_i+c_i=e_i+b c_{i+1}$. The three strings give every carry in every fixed block; the lemma gives every carry in every variable run. Initial carries are $0,\alpha,\beta$ respectively.

| Phase | $\alpha,\beta,\gamma$ | suffix carry string | middle carry string | prefix carry string |
|---|---|---|---|---|
| 0 | $0,1,0$ | `0000010` | `100000011110000011001100110000011110000001` | `0100000` |
| 1 | $1,0,0$ | `0111101` | `011011100001111100010010001111100001110110` | `1011110` |
| 2 | $1,0,1$ | `1011111` | `011100011011111011010010110111110110001110` | `0111101` |
| 3 | $0,1,0$ | `0000010` | `1000111100011100011100011110011100011110001` | `0100000` |
| 4 | $1,0,0$ | `0111101` | `0101000011100010011011100110100011100001010` | `1011110` |
| 5 | $1,0,1$ | `1011111` | `1010001100101011100110111001101010011000100` | `0111101` |

| Phase | $P$ | $\ell$ | $M$ | $r$ | $S$ |
|---|---|---|---|---|---|
| 0 | `3698A48` | `0` | `0883768431399986541A1092545899A41337673890` | `A` | `8498963` |
| 1 | `7286895` | `A` | `1757424762898860994812839A1688872685237661` | `0` | `5996816` |
| 2 | `1246277A` | `A` | `331374A51557661297853458882266745249484123` | `0` | `0872542` |
| 3 | `3698A48` | `0` | `2546113376A23184075296A356A3923196843105462` | `A` | `8498963` |
| 4 | `7286895` | `A` | `509012685283646802A6928602A8636492476220905` | `0` | `5996816` |
| 5 | `1246277A` | `A` | `A170352495681825A5026571A506181864A51431710` | `0` | `0872542` |

### Explicit alignment in every transition

- Phase0: raw output is exactly $W_1(n)$.
- Phase1: raw output is exactly $W_2(n)$.
- Phase2: $P=A_3\mathtt{A}$ 和 $B_3=\mathtt{A}M$; hence $P\mathtt{A}^nM=A_3\mathtt{A}^nB_3$, giving $W_3(n)$.
- Phase3: raw output is exactly $W_4(n)$.
- Phase4: raw output is exactly $W_5(n)$.
- Phase5: $P=A_0\mathtt{A}$, $M=B_0\mathtt{0}$, $S=C_0$; therefore output is $A_0\mathtt{A}^{n+1}B_0\mathtt{0}^{n+1}C_0=W_0(n+1)$.


### Nonpalindrome witnesses valid for every run length

Index $k$ is zero-based from the leading end, compared with index $k$ from the trailing end. Listed positions 都 lie inside the fixed outer blocks, hence are independent of $n$.

| Phase | $k$ | leading-side digit | trailing-side digit |
|---|---|---|---|
| 0 | 0 | `1` | `2` |
| 1 | 4 | `A` | `9` |
| 2 | 0 | `7` | `6` |
| 3 | 0 | `1` | `2` |
| 4 | 4 | `A` | `9` |
| 5 | 0 | `7` | `6` |

Induction through the six explicit transitions gives the return equality for all $n$. The witness table rules out a palindrome at every phase of every return cycle. 这 是 complete arithmetic proof, independent of the finite numerical test. Lean verification remains absent.

## THEOREM: base 17 six-step return

$$T_{17}^6(W_0(n))=W_0(n+1).$$

Every intermediate phase 不是 palindrome. Therefore every $W_0(n)$ 是 base-17 Lychrel number.

| Phase | $A_j$ | $x_j$ | $B_j$ | $y_j$ | $C_j$ |
|---|---|---|---|---|---|
| 0 | `10023AB83E3B983CFGEC556G4G010` | `0` | `0FGCG10FG505GF020CGF` | `G` | `GG11G4F655DDGGB299B3D38BB320G` |
| 1 | `10025F52C00F41AFCFDB0AC544020` | `G` | `GGFBD11GF4565EF21DCEG` | `0` | `0021444BB1BDFBEB23F0GC34E5210` |
| 2 | `1128328FB0G16D8ABC7CC4G985221` | `0` | `GEB7E40E3AAB4DG3F8BEF` | `G` | `02258A04BD8CBA7C71F1BE9327211` |
| 3 | `224F561D52E2E8G467G96902GA442` | `0` | `FC5GC80A85448AG8CG6CE` | `G` | `144B02G978G863G8D3E26D055F422` |
| 4 | `449DAB29B5B6B0F7CGG0E1G504884` | `0` | `D7CG8003G98A04008FC8C` | `G` | `3894G501E1FFC8G0A6B4C91BBD844` |
| 5 | `891A55426A5D41EG8FE2B2GAG90G8` | `0` | `8G8EG0080302G7010F7G8` | `G` | `8008GAG3B2FF7GE14D5A71465A088` |

### Complete fixed-block carry certificate

For each row, $S,M,P$ are the outputs in the lemma. The carry strings list **outgoing carries** from least-significant column to most-significant column. Each digit is checked by $q_i+c_i=e_i+b c_{i+1}$. The three strings give every carry in every fixed block; the lemma gives every carry in every variable run. Initial carries are $0,\alpha,\beta$ respectively.

| Phase | $\alpha,\beta,\gamma$ | suffix carry string | middle carry string | prefix carry string |
|---|---|---|---|---|
| 0 | $1,0,1$ | `10000110010110011111001111011` | `01101001100110010110` | `01011110011111001101101100001` |
| 1 | $0,1,0$ | `00001100100100111110011000000` | `111100011000111001111` | `00000001001111100100100110000` |
| 2 | $0,1,0$ | `00000011101001011101100110000` | `111010010111011010111` | `00000110110111010010111000000` |
| 3 | $0,1,0$ | `00010001001011100011011001000` | `110111111000011111011` | `00011001011000111010010001000` |
| 4 | $0,1,0$ | `00111101101010101110100000110` | `101110000111100001101` | `00100000101110101010110111100` |
| 5 | $0,1,1$ | `01010000010100110110101111000` | `010110000000000001011` | `11011110101101100101000001011` |

| Phase | $P$ | $\ell$ | $M$ | $r$ | $S$ |
|---|---|---|---|---|---|
| 0 | `10025F52C00F41AFCFDB0AC544020G` | `G` | `GFBD11GF4565EF21DCEG` | `0` | `0021444BB1BDFBEB23F0GC34E5210` |
| 1 | `1128328FB0G16D8ABC7CC4G985221` | `0` | `GEB7E40E3AAB4DG3F8BEF` | `G` | `02258A04BD8CBA7C71F1BE9327211` |
| 2 | `224F561D52E2E8G467G96902GA442` | `0` | `FC5GC80A85448AG8CG6CE` | `G` | `144B02G978G863G8D3E26D055F422` |
| 3 | `449DAB29B5B6B0F7CGG0E1G504884` | `0` | `D7CG8003G98A04008FC8C` | `G` | `3894G501E1FFC8G0A6B4C91BBD844` |
| 4 | `891A55426A5D41EG8FE2B2GAG90G8` | `0` | `8G8EG0080302G7010F7G8` | `G` | `8008GAG3B2FF7GE14D5A71465A088` |
| 5 | `10023AB83E3B983CFGEC556G4G0100` | `0` | `0FGCG10FG505GF020CGFG` | `G` | `GG11G4F655DDGGB299B3D38BB320G` |

### Explicit alignment in every transition

- Phase0: $P=A_1\mathtt{G}$ 和 $B_1=\mathtt{G}M$; hence $P\mathtt{G}^nM=A_1\mathtt{G}^nB_1$, giving $W_1(n)$.
- Phase1: raw output is exactly $W_2(n)$.
- Phase2: raw output is exactly $W_3(n)$.
- Phase3: raw output is exactly $W_4(n)$.
- Phase4: raw output is exactly $W_5(n)$.
- Phase5: $P=A_0\mathtt{0}$, $M=B_0\mathtt{G}$, $S=C_0$; therefore output is $A_0\mathtt{0}^{n+1}B_0\mathtt{G}^{n+1}C_0=W_0(n+1)$.


### Nonpalindrome witnesses valid for every run length

Index $k$ is zero-based from the leading end, compared with index $k$ from the trailing end. Listed positions 都 lie inside the fixed outer blocks, hence are independent of $n$.

| Phase | $k$ | leading-side digit | trailing-side digit |
|---|---|---|---|
| 0 | 0 | `1` | `G` |
| 1 | 0 | `1` | `0` |
| 2 | 3 | `8` | `7` |
| 3 | 5 | `6` | `5` |
| 4 | 2 | `9` | `8` |
| 5 | 1 | `9` | `8` |

Induction through the six explicit transitions gives the return equality for all $n$. The witness table rules out a palindrome at every phase of every return cycle. 这 是 complete arithmetic proof, independent of the finite numerical test. Lean verification remains absent.


## THEOREM 26: complete reconstruction of the published period-4 family

Use base-26 digits `0123456789ABCDEFGHIJKLMNOP`, with `A=10,...,P=25`, 和 write words most significant digit first. Define, for every integer \(n\ge0\),

\[
\begin{aligned}
X_0(n)&=\texttt{1N5ELA6C}\,\texttt P^n\,\texttt{P6E7}\,\texttt0^n\,\texttt{0D59ME5N},\\
X_1(n)&=\texttt{P2KB4FJD}\,\texttt0^n\,\texttt{6KL6}\,\texttt P^n\,\texttt{CJG5AK2O},\\
X_2(n)&=\texttt{1N5ELA6C}\,\texttt P^n\,\texttt{PDGFD}\,\texttt0^n\,\texttt{0D59ME5N},\\
X_3(n)&=\texttt{P2KB4FJD}\,\texttt0^n\,\texttt{D373C}\,\texttt P^n\,\texttt{CJG5AK2O}.
\end{aligned}
\]

Then \(T_{26}X_j(n)=X_{j+1}(n)\) for \(j=0,1,2\), while \(T_{26}X_3(n)=X_0(n+1)\). None of these words 是 a palindrome: phases 0 和 2 有 unequal outer digits \(1,23\), while phases 1 和 3 有 unequal outer digits \(25,24\). Therefore every \(X_0(n)\) 是 a base-26 Lychrel number.

### Complete carry proof

All table strings below run **from units toward the most significant digit**. Every input template consists of an eight-digit left block, an \(n\)-digit band, a four- or five-digit center, another \(n\)-digit band, 和 an eight-digit right block. Thus the five table regions cover every column without overlap. Each carry string contains the entering carry followed by the outgoing carry after each column. Each row satisfies \(q_i+c_i=e_i+26c_{i+1}\) directly.

Use the following fixed column-sum lists:

\[
E=(24,28,19,36,30,15,19,12),\qquad
F=(49,4,40,21,9,31,38,25).
\]

The right edge 有 column-sum list \(E\) in phases 0 和 2, list \(F\) in phases 1 和 3. The left edge 有 the corresponding reversed list. Every band column 有 sum \(25\). For arbitrary \(n\), a band entered with carry 0 emits \(\texttt P^n\) 和 leaves carry 0; a band entered with carry 1 emits \(\texttt0^n\) 和 leaves carry 1. 这 includes \(n=0\).

| Phase | Region | Column sums, in carry order | Carry string | Output digits, in carry order |
|---:|---|---|---|---|
| 0 | Right edge | \(E\) | `001011000` | `O2KA5GJC` |
| 0 | Right band | \(25^n\) | \(0^{n+1}\) | \(\texttt P^n\) |
| 0 | Center | \((32,20,20,32)\) | `01001` | `6LK6` |
| 0 | Left band | \(25^n\) | \(1^{n+1}\) | \(\texttt0^n\) |
| 0 | Left edge | \((12,19,15,30,36,19,28,24)\) | `100011010` | `DJF4BK2P` |
| 1 | Right edge | \(F\) | `010100111` | `N5EM95D0` |
| 1 | Right band | \(25^n\) | \(1^{n+1}\) | \(\texttt0^n\) |
| 1 | Center | \((12,41,41,12)\) | `10110` | `DFGD` |
| 1 | Left band | \(25^n\) | \(0^{n+1}\) | \(\texttt P^n\) |
| 1 | Left edge | \((25,38,31,9,21,40,4,49)\) | `001100101` | `PC6ALE5N` |
| 2 | Right edge | \(E\) | `001011000` | `O2KA5GJC` |
| 2 | Right band | \(25^n\) | \(0^{n+1}\) | \(\texttt P^n\) |
| 2 | Center | \((38,28,32,28,38)\) | `011111` | `C373D` |
| 2 | Left band | \(25^n\) | \(1^{n+1}\) | \(\texttt0^n\) |
| 2 | Left edge | \((12,19,15,30,36,19,28,24)\) | `100011010` | `DJF4BK2P` |
| 3 | Right edge | \(F\) | `010100111` | `N5EM95D0` |
| 3 | Right band | \(25^n\) | \(1^{n+1}\) | \(\texttt0^n\) |
| 3 | Center | \((25,6,14,6,25)\) | `110000` | `07E6P` |
| 3 | Left band | \(25^n\) | \(0^{n+1}\) | \(\texttt P^n\) |
| 3 | Left edge | \((25,38,31,9,21,40,4,49)\) | `001100101` | `PC6ALE5N` |

Phases 0 和 2 finish with carry 0, so reversing the table output directly gives \(X_1(n)\) 和 \(X_3(n)\), respectively. Phase 1 finishes with carry 1; its most significant output is `1N5ELA6CP`, followed by \(\texttt P^n\), `DGFD`, \(\texttt0^n\), 和 `0D59ME5N`. Write \(A=\texttt{1N5ELA6C}\). The exact identity \(A\texttt P\texttt P^n\texttt{DGFD}=A\texttt P^n\texttt{PDGFD}\) gives \(X_2(n)\). Phase 3 finishes with carry 1; its output is `1N5ELA6CP`, \(\texttt P^n\), `P6E70`, \(\texttt0^n\), 和 `0D59ME5N`. Regrouping gives \(\texttt{1N5ELA6C}\,\texttt P^{n+1}\,\texttt{P6E7}\,\texttt0^{n+1}\,\texttt{0D59ME5N}=X_0(n+1)\). 这 proves all four identities for every \(n\ge0\), hence the theorem by induction.


## THEOREM R: complete regular-family cycle

Digits below are written most significant first. A parenthesized expression denotes one digit. Let \(b=2^k\), \(k\ge1\), \(h=b-1\), 和 \(r\ge2\). Define

\[
W_r=10\,h^r\,(b-2)h\,0^r,
\qquad
W'_r=10\,h^r\,(b-2)h\,0^{r+1}.
\]

For \(1\le a<b\), define

\[
V_a(r)=aa\,0^{r-2}\,(b-a)(b-a-1)^3\,h^{r-2}\,(a-1)a.
\]

For \(1\le a<b/2\), define

\[
U_a(r)=aa\,0^{r-1}\,(b-a)(b-2a-1)(b-a-1)\,h^{r-1}\,(a-1)a.
\]

Finally, with \(a=b/2\), define

\[
H(r)=aa\,0^{r-1}\,(a-1)h(a-1)\,h^{r-1}\,(a-1)a.
\]

Displayed digits 都 lie in \([0,b-1]\) under their stated domains. The parameter \(a\) runs through powers of two in each half. With the first sequence indexed by \(a=2^j\), \(0\le j<k\), 和 the second by \(0\le j<k-1\), the exact phase sequence reads

\[
W_r\to \bigl(V_{2^j}(r)\bigr)_{j=0}^{k-1}
\to W'_r
\to \bigl(U_{2^j}(r)\bigr)_{j=0}^{k-2}\to H
\to W_{r+1}.
\]

For \(b=2\), omit the \(U\)-terms: \(W'_r\to H\). Hence

\[
T_b^{2(k+1)}(W_r)=W_{r+1}.
\]

Every phase fails palindromicity: \(W_r,W'_r\) start with 1 和 end with 0; every \(V,U,H\) phase 有 second digit \(a\) from the left 和 second digit \(a-1\) from the right. Thus every \(W_r\) 有 a palindrome-free forward orbit.

### Full carry convention

The tables 都 scan **units to most significant digit**. Each entry \(z/c\) records output digit \(z\) 和 outgoing carry \(c\); the incoming carry comes from the preceding row, initially zero. For a row \(h^t\), each of the \(t\) columns repeats the displayed transition. Such a row may be empty; its incoming carry then passes unchanged. The table therefore covers \(r=2\) without an omitted boundary case.

### Transition W to V

Put \(t=r-2\). The exact symmetric column-sum blocks for \(W_r\), in scan order, are the first column below.

| Column sum | Output/carry |
|---|---|
| \(1\) | \(1/0\) |
| \(0\) | \(0/0\) |
| \(h^t\) | \(h/0\) in every column |
| \(2h\) | \((b-2)/1\) |
| \(2b-3\) | \((b-2)/1\) |
| \(2b-3\) | \((b-2)/1\) |
| \(2h\) | \(h/1\) |
| \(h^t\) | \(0/1\) in every column |
| \(0\) | \(1/0\) |
| \(1\) | \(1/0\) |

Reading the output in reverse order gives \(V_1(r)\), with 没有 overflow.

### V doubling, exact reset, 和 strict overshoot

For arbitrary \(1\le a<b\), the exact column sums of \(V_a(r)\) are

\[
(2a),(2a-1),h^t,(2b-2a-1),(2b-2a-2),(2b-2a-2),
(2b-2a-1),h^t,(2a-1),(2a).
\]

The following table covers every regime. In the last column put \(\delta=2a-b\), so \(1\le\delta\le b-2\).

| Column | \(2a<b\) | \(2a=b\) | \(2a>b\) |
|---|---|---|---|
| \(2a\) | \(2a/0\) | \(0/1\) | \(\delta/1\) |
| \(2a-1\) | \((2a-1)/0\) | \(0/1\) | \(\delta/1\) |
| \(h^t\) | \(h/0\) | \(0/1\) | \(0/1\) |
| \(2b-2a-1\) | \((b-2a-1)/1\) | \(0/1\) | \((b-\delta)/0\) |
| \(2b-2a-2\) | \((b-2a-1)/1\) | \(h/0\) | \((b-\delta-2)/0\) |
| \(2b-2a-2\) | \((b-2a-1)/1\) | \((b-2)/0\) | \((b-\delta-2)/0\) |
| \(2b-2a-1\) | \((b-2a)/1\) | \(h/0\) | \((b-\delta-1)/0\) |
| \(h^t\) | \(0/1\) | \(h/0\) | \(h/0\) |
| \(2a-1\) | \(2a/0\) | \(h/0\) | \((\delta-1)/1\) |
| \(2a\) | \(2a/0\) | \(0/1\) | \((\delta+1)/1\) |
| Extra leading digit | none | \(1\) | \(1\) |

Thus \(T_b(V_a)=V_{2a}\) when \(2a<b\), whereas \(T_b(V_{b/2})=W'_r\). The strict-overshoot output, valid for every base 和 every \(b/2<a<b\), reads

\[
1(\delta+1)(\delta-1)h^{r-2}
(b-\delta-1)(b-\delta-2)^2(b-\delta)
0^{r-2}\delta\delta.
\tag{O}
\]

### W' to the second half

Put \(s=r-1\). The column sums of \(W'_r\) are

\[
1,0,h^s,2h,2b-4,2h,h^s,0,1.
\]

| Column sum | \(b\ge4\) | \(b=2\) |
|---|---|---|
| \(1\) | \(1/0\) | \(1/0\) |
| \(0\) | \(0/0\) | \(0/0\) |
| \(h^s\) | \(h/0\) | \(1/0\) |
| \(2h\) | \((b-2)/1\) | \(0/1\) |
| \(2b-4\) | \((b-3)/1\) | \(1/0\) |
| \(2h\) | \(h/1\) | \(0/1\) |
| \(h^s\) | \(0/1\) | \(0/1\) |
| \(0\) | \(1/0\) | \(1/0\) |
| \(1\) | \(1/0\) | \(1/0\) |

这 gives \(U_1\) for \(b\ge4\), 和 \(H\) for \(b=2\).

### U doubling, including the middle carry change

In the power-of-two orbit, a phase \(U_a\) satisfies either \(4a<b\) or \(4a=b\). Its exact column sums are

\[
2a,2a-1,h^s,2b-2a-1,2b-4a-2,2b-2a-1,h^s,2a-1,2a.
\]

| Column sum | \(4a<b\) | \(4a=b\) |
|---|---|---|
| \(2a\) | \(2a/0\) | \(2a/0\) |
| \(2a-1\) | \((2a-1)/0\) | \((2a-1)/0\) |
| \(h^s\) | \(h/0\) | \(h/0\) |
| \(2b-2a-1\) | \((b-2a-1)/1\) | \((2a-1)/1\) |
| \(2b-4a-2\) | \((b-4a-1)/1\) | \(h/0\) |
| \(2b-2a-1\) | \((b-2a)/1\) | \((2a-1)/1\) |
| \(h^s\) | \(0/1\) | \(0/1\) |
| \(2a-1\) | \(2a/0\) | \(2a/0\) |
| \(2a\) | \(2a/0\) | \(2a/0\) |

The outputs are respectively \(U_{2a}\) 和 \(H\). 没有 overflow occurs.

### Final H reset

For \(a=b/2\), the column sums of \(H\) are

\[
b,h,h^s,b-2,2h,b-2,h^s,h,b.
\]

| Column sum | Output/carry |
|---|---|
| \(b\) | \(0/1\) |
| \(h\) | \(0/1\) |
| \(h^s\) | \(0/1\) |
| \(b-2\) | \(h/0\) |
| \(2h\) | \((b-2)/1\) |
| \(b-2\) | \(h/0\) |
| \(h^s\) | \(h/0\) |
| \(h\) | \(h/0\) |
| \(b\) | \(0/1\) |
| Extra leading digit | \(1\) |

Reading the output yields \(W_{r+1}\). The tables establish the entire cycle for all \(r\ge2\).

## THEOREM O: exact obstruction to 这 reset recipe

现在 let \(b\ge2\) be arbitrary. Starting from \(W_r\), the orbit reaches \(V_1,V_2,V_4,\ldots\), until the first \(a=2^j\) with \(2a\ge b\). If \(2a=b\), the exact reset occurs. If \(2a>b\), formula (O) 有 second digit \(\delta+1\ge2\), whereas every \(W'_r\) 有 second digit 0. Therefore the unchanged first-overflow reset occurs **if 和 only if** \(b\) 是 power of two.

For decimal, the successive parameters are \(a=1,2,4,8\). The last transition 有 \(\delta=6\), hence the second digit becomes 7. It cannot be the required reset. 这 theorem identifies the exact arithmetic hypothesis violated by base 10: the required equality \(2\cdot2^j=b\). It 不 assert that no later return can exist.

## THEOREM C: explicit decimal counterexample

The decimal specialization with \(r=2\) follows 这 exact integer sequence:

```text
0 10998900
1 11988801
2 22877712
3 44655534
4 88211178
5 175322466
6 839546037
7 1570191975
8 7362102726
9 13634115363
10 49985258994 (palindrome)
```

Thus direct substitution of \(b=10\) into the starting family 不 supply an unconditional Lychrel construction. It would be false to infer that every longer-run specialization terminates: tests below 不 establish that.


## THEOREM F: bounded critical coefficients in the saturated framework

这 section concerns the exact definitions at repository snapshot `c6902ac6c366ce018e68a810f58b400dda07145a`, especially `Agent109.template`, `Phase`, 和 `norm_band` [R1], together with `LocalOK` 和 the actual-step invariant of the return checker [R2]. It establishes a representational obstruction; it makes no claim that all certificates are unsatisfiable.

For a coefficient word \(q\), let \(N_9(q)\) count its entries equal to \(9\). The repository's saturated shape is

\[
Q(c,B,A,C,g,h)=B\,c^g\,A\,(18-c)^h\,C\,(18-c)^h\,A^R\,c^g\,B^R,
\]

with \(1\le c\le17\) 和 \(c\ne9\). Then

\[
\boxed{N_9(Q)=2N_9(B)+2N_9(A)+N_9(C)
\le2|B|+2|A|+|C|.}
\tag{F1}
\]

**Proof.** Each entry of either \(c\)-run differs from \(9\) by the phase hypothesis. Each entry of either \((18-c)\)-run differs from \(9\), 因为 \(18-c=9\) would imply \(c=9\). Thus the four variable runs 都 contribute zero to \(N_9\). Counts add under concatenation, 和 reversal preserves counts. The fixed blocks therefore give exactly the displayed sum. A count cannot exceed its block length, giving the inequality. 这 proves every case, including zero-length runs.

For any finite nonempty set of permitted states, define

\[
K_{\max}=\max_s\{2|B_s|+2|A_s|+|C_s|\}.
\]

Every coefficient word represented by those states 有 \(N_9\le K_{\max}\), independent of its run lengths, phase, or segmentation.

Now consider any canonical decimal digit family

\[
Z(n)=P\,x^n\,M\,y^n\,R,
\qquad |P|=|R|,\quad x+y=9.
\]

Its reflected digit sums contain the 两个 bands \(9^n\), hence

\[
\boxed{N_9(\operatorname{pair}(Z(n)))\ge2n.}
\tag{F2}
\]

**Proof.** Equal outer-block lengths align the left variable run exactly with the reversed right variable run. Each aligned pair sums to \(x+y=9\). The other variable run gives another disjoint block of \(n\) such columns. Their combined contribution is \(2n\); the fixed blocks can only add more. For \(2n>K_{\max}\), (F1) 和 (F2) contradict any proposed representation in that finite state set.

Consequently, an actual orbit with an unbounded number of critical \(9\)-coefficients cannot remain in finitely many saturated states of 这 form. The growing critical-band mechanism reconstructed above would 有 exactly 这 obstruction in a decimal realization. Changing the state index or moving the segment boundaries 不 affect the count argument.

**Checker scope.** `LocalOK` requires `Phase s.c`. Its actual-step bridge represents the next actual pair word by the next listed state's template, so any orbit covered by the finite return certificate inherits the eventual bound above. The existential predecessor in the invariant 不 evade the argument: after an invariant step, the current integer supplies the predecessor 和 its actual pair word is represented. 这 excludes a particular mechanism from the present finite framework; other bounded-\(N_9\) mechanisms remain possible.

## THEOREM G: admitting coefficient 9 requires a different carry rule

The existing saturated-band formula resets the carry to `kOf x`, where `kOf 9 = 0`. Removing its hypothesis \(x\ne9\) gives a false statement. At one column with incoming carry \(1\),

\[
\operatorname{norm}([9],1)=([0],1),
\]

whereas the unrestricted existing conclusion would give \(([10],0)\). The first equality follows from \(9+1=0+10\cdot1\); the second follows by substituting \(x=9,m=0,e=1\) into the claimed saturated formula. Both the output digit 和 outgoing carry would be wrong.

The correct critical branch, for \(e\in\{0,1\}\), is

\[
\boxed{\operatorname{norm}(9^m,e)
=\bigl((9(1-e))^m,e\bigr).}
\tag{G}
\]

**Proof.** For \(m=0\), the output block is empty 和 the carry stays \(e\). For a nonempty block, incoming \(0\) yields \(9+0=9+10\cdot0\); incoming \(1\) yields \(9+1=0+10\cdot1\). Each transition preserves its entering carry. Induction on the remaining columns proves the formula. 这两个 cases exhaust the binary carry domain.

## THEOREM H: the center condition in the sporadic mechanism

In the insertion lemma, the 两个 emitted bulk digits are \(\ell=(b-1)(1-\beta)\) 和 \(r=(b-1)(1-\alpha)\). They remain complementary precisely when

\[
\ell+r=b-1\quad\Longleftrightarrow\quad\alpha+\beta=1.
\]

**Proof.** Their sum equals \((b-1)(2-\alpha-\beta)\). Since \(b-1>0\), equality to \(b-1\) is equivalent to the stated binary-carry equation. 这 proves all four possible carry pairs at once by an exact identity: \((0,0)\) yields \(2b-2\), \((0,1)\) yields \(b-1\), \((1,0)\) yields \(b-1\), 和 \((1,1)\) yields \(0\). Every listed sporadic transition satisfies the middle 两个 cases. A bounded regrouping of fixed blocks cannot alter the bulk digit in an arbitrarily long run.

Thus the finite center must send the particular carry arriving from the right band to the opposite carry for the left band. 这 condition, together with the endpoint blocks, overflow, 和 exact phase closure, isolates the mechanism. Its algebra 不 single out base 10.

## IDEA: what can be transferred to decimal

The power-of-two proof needs the special equality \(b=2^{j+1}\). The sporadic proofs need a complete cycle of the finite block additions in the insertion lemma, with \(\alpha+\beta=1\), consistent overflow, growing runs, 和 a nonpalindrome witness at every phase. Base 10 satisfies the neutral-band identity; a decimal instance of the latter finite closure remains missing. The absence of a known instance supplies no impossibility theorem.

A sound extension of the saturated checker would retain the actual incoming carry through each critical-\(9\) band, derive new fixed-block 和 re-folding transitions from that carry, 和 only then establish the enlarged return checker's soundness. Deleting `c != 9` alone cannot work, as Theorem G shows. 这是 an extension proposal; it 不是 completed formalization.

## IDEA: base-20 source limitation

The original author explicitly reports a growing base-20 word longer than 200 digits while withholding its digit string [S1]. Both opened reproductions preserve that omission [S2, S3]. Targeted searches found repetitions of 这 report, without an additional explicit witness. Therefore base 20 remains an unresolved reconstruction in 这 document: neither a seed, a return period, a carry table, nor a 1000-step verification is supplied. 这 是 limitation of the located evidence, not a disproof of the reported base-20 construction.

## Numerical audit: reproducible code 和 actual output

The following single Python program contains all data needed for the displayed sporadic families, the regular-family checks, the decimal counterexample, 和 the critical-band check. It performs no search for seeds. Each addition is checked independently against integer evaluation. The infinite statements follow from the symbolic carry proofs; the finite run 是 transcription audit. The decimal output `None` means only that no palindrome appeared in the tested 1000 steps. The base-20 entry in the short branch sample checks a regular-family algebraic identity only; it 不是 base-20 Lychrel witness.

Save the block as `verify_agent203.py`, then run `python3 verify_agent203.py`.

```python
"""Agent 203: deterministic certificate checks; no seed search."""
from hashlib import sha256

D = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DATA = {11: [('1246277', 'A', 'A170352495681825A5026571A506181864A5143171', '0', '0872542'),
      ('3698A48', '0', '0883768431399986541A1092545899A41337673890', 'A', '8498963'),
      ('7286895', 'A', '1757424762898860994812839A1688872685237661', '0', '5996816'),
      ('1246277', 'A', 'A331374A51557661297853458882266745249484123', '0', '0872542'),
      ('3698A48', '0', '2546113376A23184075296A356A3923196843105462', 'A', '8498963'),
      ('7286895', 'A', '509012685283646802A6928602A8636492476220905', '0', '5996816')],
 17: [('10023AB83E3B983CFGEC556G4G010',
       '0',
       '0FGCG10FG505GF020CGF',
       'G',
       'GG11G4F655DDGGB299B3D38BB320G'),
      ('10025F52C00F41AFCFDB0AC544020',
       'G',
       'GGFBD11GF4565EF21DCEG',
       '0',
       '0021444BB1BDFBEB23F0GC34E5210'),
      ('1128328FB0G16D8ABC7CC4G985221',
       '0',
       'GEB7E40E3AAB4DG3F8BEF',
       'G',
       '02258A04BD8CBA7C71F1BE9327211'),
      ('224F561D52E2E8G467G96902GA442',
       '0',
       'FC5GC80A85448AG8CG6CE',
       'G',
       '144B02G978G863G8D3E26D055F422'),
      ('449DAB29B5B6B0F7CGG0E1G504884',
       '0',
       'D7CG8003G98A04008FC8C',
       'G',
       '3894G501E1FFC8G0A6B4C91BBD844'),
      ('891A55426A5D41EG8FE2B2GAG90G8',
       '0',
       '8G8EG0080302G7010F7G8',
       'G',
       '8008GAG3B2FF7GE14D5A71465A088')],
 26: [('1N5ELA6C', 'P', 'P6E7', '0', '0D59ME5N'),
      ('P2KB4FJD', '0', '6KL6', 'P', 'CJG5AK2O'),
      ('1N5ELA6C', 'P', 'PDGFD', '0', '0D59ME5N'),
      ('P2KB4FJD', '0', 'D373C', 'P', 'CJG5AK2O')]}


def value(digits, base):
    result = 0
    for digit in digits:
        assert 0 <= digit < base
        result = result * base + digit
    return result


def add_digits(digits, base):
    assert digits and digits[0] != 0
    output, carry = [], 0
    for left, right in zip(digits, reversed(digits)):
        q = left + right
        next_carry, digit = divmod(q + carry, base)
        assert carry in (0, 1) and next_carry in (0, 1)
        assert q + carry == digit + base * next_carry
        output.append(digit)
        carry = next_carry
    if carry:
        output.append(carry)
    output.reverse()
    assert value(output, base) == value(digits, base) + value(digits[::-1], base)
    return output


def word(phase, n):
    a, x, middle, y, c = phase
    return [D.index(s) for s in a + x*n + middle + y*n + c]


def block_add(u, v, base, incoming):
    assert len(u) == len(v)
    out, trace, carry = [], [], incoming
    for x, y in zip(reversed(u), reversed(v)):
        q = D.index(x) + D.index(y)
        nxt, digit = divmod(q + carry, base)
        assert q + carry == digit + base*nxt
        assert nxt in (0, 1)
        out.append(D[digit])
        trace.append(str(nxt))
        carry = nxt
    return ''.join(out[::-1]), carry, ''.join(trace)


def sporadic_checks():
    for base, phases in DATA.items():
        period = len(phases)
        for j, (a, x, middle, y, c) in enumerate(phases):
            assert len(a) == len(c)
            assert D.index(x) + D.index(y) == base-1
            suffix, alpha, ts = block_add(c, a[::-1], base, 0)
            mid, beta, tm = block_add(middle, middle[::-1], base, alpha)
            prefix, gamma, tp = block_add(a, c[::-1], base, beta)
            prefix = ('1' if gamma else '') + prefix
            ell = '0' if beta else D[base-1]
            right = '0' if alpha else D[base-1]
            assert alpha != beta
            for n in (0, 1, 2, 5):
                raw = prefix + ell*n + mid + right*n + suffix
                target = word(phases[(j+1) % period], n + (j+1 == period))
                assert [D.index(s) for s in raw] == target
                assert add_digits(word(phases[j], n), base) == target
        for n0 in (0, 1, 2):
            digits = word(phases[0], n0)
            for step in range(1001):
                assert digits == word(phases[step % period], n0 + step//period)
                assert digits != digits[::-1]
                if step < 1000:
                    digits = add_digits(digits, base)
            encoded = ''.join(D[d] for d in digits)
            print(f'sporadic base={base} n0={n0} steps=1000 '
                  f'palindromes=0 phase_checks=1001 integer_checks=1000 '
                  f'final_digits={len(digits)} final_phase={1000 % period} '
                  f'final_n={n0 + 1000//period} sha256={sha256(encoded.encode()).hexdigest()}')


def W(base, r):
    return [1, 0] + [base-1]*r + [base-2, base-1] + [0]*r


def V(base, r, a):
    return ([a, a] + [0]*(r-2) + [base-a] + [base-a-1]*3
            + [base-1]*(r-2) + [a-1, a])


def U_or_H(base, r, a):
    middle = ([a-1, base-1, a-1] if 2*a == base
              else [base-a, base-2*a-1, base-a-1])
    return [a, a] + [0]*(r-1) + middle + [base-1]*(r-1) + [a-1, a]


def regular_phases(base, k, r):
    return ([W(base, r)] + [V(base, r, 2**j) for j in range(k)]
            + [W(base, r) + [0]]
            + [U_or_H(base, r, 2**j) for j in range(k)])


def regular_checks():
    for base, k in ((2, 1), (4, 2), (8, 3), (16, 4), (32, 5)):
        digits, period = W(base, 2), 2*(k+1)
        for step in range(1001):
            cycles, phase = divmod(step, period)
            assert digits == regular_phases(base, k, 2+cycles)[phase]
            assert digits != digits[::-1]
            if step < 1000:
                digits = add_digits(digits, base)
        print(f'regular base={base} steps=1000 palindromes=0 '
              f'phase_checks=1001 integer_checks=1000 final_digits={len(digits)}')
    for r in (2, 3, 4, 5):
        digits, first = W(10, r), None
        for step in range(1, 1001):
            digits = add_digits(digits, 10)
            if first is None and digits == digits[::-1]:
                first = step
        if r == 2:
            assert first == 10
        print(f'decimal r={r} steps=1000 first_palindrome={first} '
              f'integer_checks=1000 final_digits={len(digits)}')
    for base in (2, 3, 4, 5, 8, 10, 11, 16, 17, 20, 26, 32):
        for r in (2, 3, 5):
            assert add_digits(W(base, r), base) == V(base, r, 1)
            a = 1
            while 2*a < base:
                assert add_digits(V(base, r, a), base) == V(base, r, 2*a)
                a *= 2
            if 2*a == base:
                expected = W(base, r) + [0]
            else:
                delta = 2*a-base
                expected = ([1, delta+1, delta-1] + [base-1]*(r-2)
                            + [base-delta-1] + [base-delta-2]*2
                            + [base-delta] + [0]*(r-2) + [delta, delta])
            assert add_digits(V(base, r, a), base) == expected
    print('selected symbolic-branch checks: PASS')


def framework_check():
    assert block_add('9', '0', 10, 1)[:2] == ('0', 1)
    for e in (0, 1):
        for m in (0, 1, 2, 10):
            out, carry, _ = block_add('9'*m, '0'*m, 10, e)
            assert out == ('9' if e == 0 else '0')*m and carry == e
    print('critical-9 normalization checks: PASS; norm([9],1)=([0],1)')


if __name__ == '__main__':
    sporadic_checks()
    regular_checks()
    framework_check()
```

### Executed output

```text
sporadic base=11 n0=0 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=389 final_phase=4 final_n=166 sha256=c6ef4303e0cd07dc00de7292f28bec6889310361bded8a490deb572271592865
sporadic base=11 n0=1 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=391 final_phase=4 final_n=167 sha256=084d2b7b2399d6157510fdf66cb0dd3162ae9d8271752db75f95fd6e664e86d6
sporadic base=11 n0=2 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=393 final_phase=4 final_n=168 sha256=44cee966ebfd3751ca7b2088a909b12340718dfa328e055399c7fe3a58d58f36
sporadic base=17 n0=0 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=411 final_phase=4 final_n=166 sha256=ec9c5ca2033fedf772ffaafbab4da334c6479c76dd0417ffaa265d5d59142a11
sporadic base=17 n0=1 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=413 final_phase=4 final_n=167 sha256=bcb62de8004ee4dc8702f2f0725e8f4b21bfe34a06d6fa01a39b1f8ca585c23e
sporadic base=17 n0=2 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=415 final_phase=4 final_n=168 sha256=a05090663836d912ca502472bb0139cb86223f9598c8fc757a1669365096f4f5
sporadic base=26 n0=0 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=520 final_phase=0 final_n=250 sha256=3cf433f6125130ed41119342be5ee2f276a3be17e956e87e574840527241ae69
sporadic base=26 n0=1 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=522 final_phase=0 final_n=251 sha256=59a384d2e5545329391f9bacd4247a7405f31c21e99ce247ba4556f16442d36b
sporadic base=26 n0=2 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=524 final_phase=0 final_n=252 sha256=f133f2da8c842dd50afc09961fb1e0c86bc4edbd7b8553b8b1cc9a37e73d59fd
regular base=2 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=508
regular base=4 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=341
regular base=8 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=258
regular base=16 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=208
regular base=32 steps=1000 palindromes=0 phase_checks=1001 integer_checks=1000 final_digits=174
decimal r=2 steps=1000 first_palindrome=10 integer_checks=1000 final_digits=415
decimal r=3 steps=1000 first_palindrome=None integer_checks=1000 final_digits=416
decimal r=4 steps=1000 first_palindrome=None integer_checks=1000 final_digits=421
decimal r=5 steps=1000 first_palindrome=None integer_checks=1000 final_digits=412
selected symbolic-branch checks: PASS
critical-9 normalization checks: PASS; norm([9],1)=([0],1)
```

## IDEA: sharpest open question

Do there exist a finite number \(m\) of decimal digit templates

\[
Z_j(n)=A_j x_j^n B_j y_j^n C_j,
\qquad |A_j|=|C_j|,\quad \{x_j,y_j\}=\{0,9\},
\]

nonnegative integers \(\delta_j\), 和 a threshold \(n_*\), such that

\[
T_{10}(Z_j(n))=Z_{j+1\pmod m}(n+\delta_j)
\quad(n\ge n_*),
\qquad \sum_{j=0}^{m-1}\delta_j>0,
\]

with a fixed unequal reflected digit pair at every phase?

The insertion lemma makes every proposed transition an explicit finite block/carry identity plus a run-regrouping identity. Theorem F shows why 这 exact question requires a critical-band extension beyond the current saturated phase domain. A positive instance would give some decimal Lychrel number by induction; a complete impossibility proof for 这 stated class would 也 be a precise result. Neither direction is established here. Recovering the omitted base-20 witness remains a separate source question.

## References opened 和 repository definitions inspected

- **[S1]** David Seal, original post, January 16, 1996, in [Numeric Palindromes, rec.puzzles](https://groups.google.com/g/rec.puzzles/c/QFHJ2AJq4gw). Primary record for the family announcements 和 explicit base-20 omission.
- **[S2]** [David Seal's sporadic constructions, reproduced by MathPages](https://www.mathpages.com/home/dseal.htm). Contains the base-11, base-17, 和 base-26 seed templates 和 phase tables.
- **[S3]** [Longer reproduction of Seal's post](https://www.p196.org/html/papers1.html). Contains the regular-family examples, author caveat, 和 the same base-20 omission.
- **[S4]** Kevin Brown, [Digit Reversal Sums Leading to Palindromes](https://www.mathpages.com/home/kmath004/kmath004.htm). Context for the power-of-two period; the proof here uses the explicit column arithmetic above.
- **[R1]** [`TemplateStep.lean`, inspected snapshot](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean). Definitions `template`, `Phase`, `norm`, `kOf`, `tOf`; the hypothesis of `norm_band`.
- **[R2]** [`ReturnCertificate.lean`, inspected snapshot](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean). Definitions `State`, `LocalOK`, `check`, 和 the actual-orbit invariant/step bridge.

The source digit templates are mathematical data. The carry proofs, complete case analysis, count obstruction, 和 numerical audits in 这 report reconstruct 和 check those data. Novelty remains unclaimed for the historical constructions or the elementary carry identities.
