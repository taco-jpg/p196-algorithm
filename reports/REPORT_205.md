# REPORT_205 — Interfaces, finite states, 和 run-length growth

Agent #205 · direction 5 · 2026-10-22

## Answer in 1 paragraph

**没有 decimal Lychrel witness or accepted return certificate.** **THEOREM:** for a realizable exact ordered return with distinct neighboring bands in the six-cycle \(2\to4\to8\to16\to14\to10\to2\), the gain of each mirrored run pair is divisible by an explicit adjacent-interface modulus \(D_j\in\{3,9\}\); all coordinates growing forces \(m\ge36\lceil\sum_jD_j/9\rceil\), 和 complementary bands with the 2 coordinates growing require \(m\ge72\). **THEOREM:** under an exact profile return, complement-reflection symmetry forces an isolated complementary interface to move at half the total width gain, so a returning bounded center leaves the inner band unchanged. **LEAN-VERIFIED:** for a supplied cycle of signed run-length increments, phase lower bounds exist exactly when the total increment in each coordinate is nonnegative; the least initial reserves are explicit prefix-deficit maxima. **THEOREM:** a universally valid affine return on independent mirrored run lengths cannot amplify their variable lengths; an all-growing, order-preserving separated return is a translation. Exact carry formulas, proofs, reproducible numerical identity checks through 1000 steps, 和 the remaining existence question follow. The results restrict interface-return constructions; a compatible safe cycle remains missing.

## Status 和 relation to the existing framework

**LEAN-VERIFIED** below refers only to the new generic arithmetic module `lean/P196/Agent205InterfaceGrowth/CyclicGuards.lean`, compiled with Lean 4.19.0 和 audited at its 7 registered endpoints. **THEOREM** identifies a complete written proof. The multi-band, spatial-symmetry, 和 matrix arguments are written proofs, with Lean formalization remaining outstanding. **IDEA** identifies a proposed use or an unresolved construction task.

The inspected repository baseline is commit `c6902ac6c366ce018e68a810f58b400dda07145a`. Existing results already establish the complementary two-band step identity, certificate soundness, two-band width accounting, the upper overflow budget, 和 six-phase divisibility by 9. The present multi-band theorem extends the charge calculation to arbitrary distinct adjacent six-cycle phases; the new Lean module establishes the converse guard-feasibility direction. Existing results are attributed in the sources section. Strict growth of every run is stronger than what a Lychrel certificate requires: nonnegative gains with at least 1 positive coordinate may suffice once every other checker condition holds.

Throughout, coefficient words are written from units to most significant position. A superscript on a word denotes repetition, 和 \(W^R\) denotes reversal. Symmetry of the coefficient word \(q\) is automatic; palindrome avoidance must be checked on the normalized **digit** word, including the overflow digit.

## THEOREM A — multi-band interface charge quantizes every returning run gain

**THEOREM — written proof.** The existing two-band charge constraints are a special case. The adjacent-band modulus below permits arbitrary ordered six-cycle bands. Lean verification of this theorem remains outstanding.

### Precise hypotheses

Let \(S=\{2,4,8,10,14,16\}\). At phase \(t\), a symmetric column-sum word takes the form

\[
Q_t=B_t s_{1,t}^{n_{1,t}}A_{1,t}s_{2,t}^{n_{2,t}}\cdots A_{r-1,t}s_{r,t}^{n_{r,t}}C_t
s_{r,t}^{n_{r,t}}A_{r-1,t}^{R}\cdots s_{2,t}^{n_{2,t}}A_{1,t}^{R}s_{1,t}^{n_{1,t}}B_t^R.
\]

Here \(r\ge1\), each band coefficient belongs to \(S\), every finite-block coefficient lies in \(\{0,\ldots,18\}\), \(C_t=C_t^R\), 和 every band length is at least 2 wherever the transition is used. Consecutive band coefficients are distinct. Write h_s=1 if s>=10 和 0 otherwise; u_s=s-9h_s; f(s)=2u_s. The bands advance by s_{j,t+1}=f(s_{j,t}). Let gamma_t be the actual final carry in the whole-word addition. Thus gamma_t is determined by the word, never chosen freely.

At every step take the exact raw blocks specified below, then move a suffix of s_{1,t+1} from the exterior into the first run, move prefixes/suffixes of the appropriate adjacent band coefficients out of each interface block, 和 move equally long s_{r,t+1} strips from both ends of the central block into the innermost mirrored runs. Nonmaximal trimming is permitted. Suppose after m>0 steps every finite block 和 every ordered band coefficient returns exactly to its initial value. Suppose the returning length vector is n -> n+v, with v_j integral. This theorem concerns these separated, ordered returns; it asserts neither that such a return exists nor that every conceivable template admits this form.

Put

\[
\Gamma=\sum_{t=0}^{m-1}\gamma_t,\qquad H=2m-\Gamma,
\quad M_i=\frac{9}{\gcd(9,s_{i+1,0}-s_{i,0})}\quad(1\le i<r),
\quad M_0=M_r=9,
\quad D_j=\gcd(M_{j-1},M_j).
\]

Then

\[
6\mid m,\qquad 18\mid\Gamma,\qquad
\Gamma=2\sum_{j=1}^{r}v_j,\qquad D_j\mid v_j.
\tag{1}
\]

Every \(M_i\) 和 \(D_j\) belongs to \(\{3,9\}\). If the return is realized by a positive decimal integer, then 也

\[
2\Gamma\le m.
\tag{2}
\]

Consequently, if the return is realized by a positive decimal integer 和 every run pair grows, \(v_j>0\) for every \(j\), then

\[
m\ge36\left\lceil\frac{\sum_jD_j}{9}\right\rceil.
\tag{3}
\]

If successive band coefficients alternate residue classes 1 和 2 modulo 3, every D_j=9 和

\[
9\mid v_j,\quad v_j\ge9,\quad\Gamma\ge18r,\quad m\ge36r.
\tag{4}
\]

In particular, two complementary six-cycle bands with the 2 run pairs growing require m>=72. Without the alternating-residue hypothesis, distinct adjacent six-cycle coefficients still give 3|v_j 和 m>=36 ceil(r/3) when all run pairs grow.

### 1. Carry accounting on every finite block

For any finite coefficient word W=(w_0,...,w_{k-1}) 和 incoming carry b in {0,1}, set c_0=b 和

\[
c_{i+1}=\lfloor(w_i+c_i)/10\rfloor,
\qquad d_i=w_i+c_i-10c_{i+1}.
\]

All carries are bits 因为 0<=w_i<=18. Write N(W,b)=(D,c_k), where D=(d_0,...,d_{k-1}), 和 K(W,b)=sum_{i=1}^k c_i. Direct summation gives the exact integer identity

\[
\sum D=\sum W+b-c_k-9K(W,b).
\tag{5}
\]

For s in {2,4,8}, \(s+0\) 和 \(s+1\) 都 lie below 10; a column of s resets the carry to 0. For s in {10,14,16}, \(s+0\) 和 \(s+1\) 都 lie between 10 和 19 inclusively; a column of s resets the carry to 1. Therefore a run s^n, n>=1, entered with b produces first digit s+b-10h_s, then n-1 digits u_s, 和 exits with h_s. Every incoming carry case is included.

The six-cycle is 2->4->8->16->14->10->2. Thus an ordered return of any band in S forces 6|m. 也 f(s)=2s modulo 9.

### 2. Exact raw internal block: overflow 0 和 overflow 1

Fix adjacent bands s,t 和 their intervening finite block A. Set

\[
N(A,h_s)=(U,\alpha),\quad N(A^R,h_t)=(V,\beta),
\quad \xi=t+\alpha-10h_t,\quad\eta=s+\beta-10h_s,
\quad K_U=K(A,h_s),\quad K_V=K(A^R,h_t).
\]

Write Z(X,Y) for the coordinatewise sum of equal-length words X 和 Y. Reflection pairs the following exact digit blocks:

\[
I_0=Z([u_s]U[\xi],[\eta]V^R[u_t])\qquad(\gamma=0),
\tag{6a}
\]

\[
I_1=Z(U[\xi],[\eta]V^R)\qquad(\gamma=1).
\tag{6b}
\]

The gamma=1 reflection is shifted by one position 因为 the leading overflow digit is appended. Formula (6b) includes that shift, rather than treating the two cases as identical. The surviving core of every neighboring run is of length \(n-2+\gamma\). These formulas 也 cover A empty.

Let S_A=sum A. By (5), sum U=S_A+h_s-alpha-9K_U 和 sum V=S_A+h_t-beta-9K_V. For gamma=0, summing (6a) gives

\[
\sum I_0=u_s+(S_A+h_s-\alpha-9K_U)+\xi+
\eta+(S_A+h_t-\beta-9K_V)+u_t
=2S_A+2(s+t)-18(h_s+h_t)-9(K_U+K_V).
\tag{7a}
\]

For gamma=1, summing (6b) gives

\[
\sum I_1=(S_A+h_s-\alpha-9K_U)+\xi+
\eta+(S_A+h_t-\beta-9K_V)
=2S_A+s+t-9(h_s+h_t+K_U+K_V).
\tag{7b}
\]

Hence, with a=2-gamma, the exact length 和 modular sum laws are

\[
|I_\gamma|=|A|+a,\qquad
\sum I_\gamma\equiv2\sum A+a(s+t)\pmod9.
\tag{8}
\]

The 2 incoming carries 和 the 2 final carries have been included 和 canceled explicitly. The calculation permits arbitrary adjacent band coefficients; complementarity \(s+t=18\) is optional.

### 3. Exact exterior 和 central blocks

For the exterior B adjacent to s=s_1, set

\[
N(B,0)=(U,\alpha),\quad N(B^R,h_s)=(V,\gamma),
\quad\xi=s+\alpha-10h_s.
\]

The actual whole-word final carry is the displayed gamma 因为 the preceding reflected s-run exits with h_s. The raw exteriors are

\[
E_0=Z(U[\xi],V^R[u_s]),\qquad
E_1=Z(U[\xi],[1]V^R).
\tag{9}
\]

Each is of length \(\lvert B\rvert+1\). Let K_U=K(B,0), K_V=K(B^R,h_s), S_B=sum B. Formula (5) gives sum U=S_B-alpha-9K_U 和 sum V=S_B+h_s-gamma-9K_V. Thus

\[
\sum E_0=2S_B+2s-18h_s-9(K_U+K_V),
\qquad
\sum E_1=2S_B+s-9h_s-9(K_U+K_V).
\tag{10}
\]

The extra leading digit 1 in E_1 cancels the -gamma=-1 term. Therefore

\[
\sum E_\gamma\equiv2\sum B+(2-\gamma)s\pmod9.
\tag{11}
\]

For the symmetric central block C adjacent to s=s_r, set N(C,h_s)=(D,kappa), xi=s+kappa-10h_s, 和 P(W)=Z(W,W^R). The raw centers are

\[
F_0=P([u_s]D[\xi]),\qquad F_1=P(D[\xi]).
\tag{12}
\]

Their lengths are |C|+2 和 |C|+1 respectively. If K=K(C,h_s), then the exact sums are

\[
\sum F_0=2\sum C+4s-36h_s-18K,\qquad
\sum F_1=2\sum C+2s-18h_s-18K.
\tag{13}
\]

This accounts for the center 和 its reflected carries in the 2 cases; the identity permits either parity for the length of \(C\). Ordinary-integer realizability imposes the usual even central coefficient when the full coefficient word is of odd length.

### 4. Closed-block length accounting

At phase t write j_{0,t} for the exterior suffix trim, l_{i,t},r_{i,t} for the left 和 right trims of interface i, 和 k_t for each of the two equal center trims. Let J_0=sum_t j_{0,t}, L_i=sum_t l_{i,t}, R_i=sum_t r_{i,t}, K_*=sum_t k_t. Since every bounded block returns to its original length, (8), (9), 和 (12) give

\[
J_0=m,\qquad L_i+R_i=H,\qquad2K_*=H.
\tag{14}
\]

In particular H 和 Gamma are even. The gain equations are

\[
v_1=-H+m+L_1,\quad
v_j=-H+R_{j-1}+L_j\ (1<j<r),\quad
v_r=-H+R_{r-1}+H/2.
\tag{15}
\]

When r=1 the sole equation is v_1=-H+m+H/2=Gamma/2. Summing (15), using (14), gives Gamma=2 sum_j v_j.

### 5. Exterior clock forces 9|Gamma

Define exterior charge C_t=sum B_t-s_{1,t}|B_t| modulo 9. Removing copies of the successor bulk letter from E_gamma 不 alter this charge. Combining |E_gamma|=|B|+1 with (11) 和 s'=2s modulo 9 gives

\[
C_{t+1}\equiv2C_t-\gamma_t s_{1,t}\pmod9.
\tag{16}
\]

Every s in S is invertible modulo 9. Define Z_t=2s_{1,t}^{-1}C_t modulo 9. Since s_{1,t+1}=2s_{1,t} modulo 9, equation (16) gives Z_{t+1}=Z_t-gamma_t modulo 9. The exterior 和 its phase return, so Z_m=Z_0 和 Gamma=0 modulo 9. Together with evenness, 18|Gamma.

### 6. General interface clock 和 divisibility

At interface i put s_t=s_{i,t}, t_t=s_{i+1,t}, delta_t=t_t-s_t, 和 Q_t=sum A_{i,t}-s_t|A_{i,t}| modulo 9. The raw-block charge from (8) is 2Q_t+a_t delta_t. Left trimming removes zero-charge letters s_{t+1}; right trimming removes r_{i,t} letters of relative charge delta_{t+1}=2delta_t modulo 9. Therefore

\[
Q_{t+1}\equiv2Q_t+\delta_t(a_t-2r_{i,t})\pmod9.
\tag{17}
\]

As delta_t=2^t delta_0 modulo 9, iteration gives

\[
Q_m\equiv2^mQ_0+2^{m-1}\delta_0\sum_{t=0}^{m-1}(a_t-2r_{i,t})\pmod9.
\tag{18}
\]

The ordered bands return, so 6|m 和 2^m=1 modulo 9. The interface block returns, so Q_m=Q_0. Multiplication by 2^{m-1} is invertible modulo 9. Equation (18) therefore gives

\[
\delta_0(H-2R_i)\equiv0\pmod9.
\tag{19}
\]

By the elementary divisibility cancellation rule, M_i=9/gcd(9,delta_0) divides H-2R_i. Since H is even 和 M_i is odd, M_i divides R_i-H/2. From L_i+R_i=H it 也 divides L_i-H/2. Thus

\[
L_i\equiv R_i\equiv H/2\pmod {M_i}.
\tag{20}
\]

For an interior run j, (15) 和 (20) imply v_j=0 modulo gcd(M_{j-1},M_j). For the outermost run, v_1 is congruent to m-H/2=Gamma/2 modulo M_1; Gamma/2 is a multiple of 9, so v_1 is divisible by M_1. For the innermost run, the exact center trim H/2 和 (20) imply M_{r-1}|v_r. The r=1 case was already handled. This proves D_j|v_j with M_0=M_r=9.

For distinct even letters of S, a nonzero difference is never divisible by 9, 和 its gcd with 9 is 1 or 3. Consequently M_i is 9 or 3. It is 9 precisely when the two letters differ modulo 3. This proves the claimed specializations.

### 7. Physical overflow budget, with every endpoint case

Let x be the outer column sum of a positive decimal integer. Then x is in {1,...,18}. If x<=8, the overflow is 0 和 the next outer sum is 2x+b for b in {0,1}, the incoming carry at the far outer column. If x=9, b=0 gives overflow 0 和 next outer sum 18, while b=1 gives overflow 和 next outer sum 10. If x>=10, overflow occurs 和 the new outer sum is x-9. The last formula uses the new leading 1 和 the units digit x-10. The resulting bound is already present in `CertificateCarryBudget.lean`; the complete endpoint proof is included here to make the dependence explicit.

Define p(1)=3; p(2)=p(3)=p(10)=2; p(4)=...=p(9)=1; p(11)=...=p(18)=0. The following table lists all possible endpoint transitions 和 p(next)-p(current).

| Current x | Next x | Overflow | Potential difference |
|---|---|---:|---|
| 1 | 2,3 | 0 | -1,-1 |
| 2 | 4,5 | 0 | -1,-1 |
| 3 | 6,7 | 0 | -1,-1 |
| 4 | 8,9 | 0 | 0,0 |
| 5 | 10,11 | 0 | 1,-1 |
| 6 | 12,13 | 0 | -1,-1 |
| 7 | 14,15 | 0 | -1,-1 |
| 8 | 16,17 | 0 | -1,-1 |
| 9 | 18 | 0 | -1 |
| 9 | 10 | 1 | 1 |
| 10 | 1 | 1 | 1 |
| 11 | 2 | 1 | 2 |
| 12 | 3 | 1 | 2 |
| 13 | 4 | 1 | 1 |
| 14 | 5 | 1 | 1 |
| 15 | 6 | 1 | 1 |
| 16 | 7 | 1 | 1 |
| 17 | 8 | 1 | 1 |
| 18 | 9 | 1 | 1 |

Every row satisfies p(next)-p(current)>=2gamma-1. The endpoint returns with the finite exterior 和 phase, so telescoping gives 0>=2Gamma-m. This proves (2).

If every v_j>0, then divisibility yields v_j>=D_j. Let V=sum_jv_j. Equation (1) gives 9|V; hence V>=9 ceil(sum_jD_j/9). Finally m>=2Gamma=4V establishes (3), 和 its stated consequences follow.

### Scope 和 failure modes

The result 不 apply without checking its exact finite-block return hypothesis, actual carry choices, long-run separation, 和 fixed ordered band labels. Repeated adjacent band symbols give gcd(9,0)=9 和 M_i=1, destroying the claimed universal divisibility by 3 at that interface. A bounded defect separating equal long bands falls outside the distinct-neighbor corollary; its existence or success remains unresolved. An interface with adjacent symbols of the same nonzero residue modulo 3 gives M_i=3 rather than 9; claiming every gain is a multiple of 9 in this wider class would be unsupported. Periodic-word bands, 9-bands, merging runs, 和 templates with a growing central block require separate analysis.


## LEAN-VERIFIED B — exact elimination of cyclic run-length guards

Fix \(P>0\), signed integer increments \(a_0,\ldots,a_{P-1}\), 和 integer phase thresholds \(h_i\). Define

\[
S_0=0,\qquad S_i=\sum_{j<i}a_j,\qquad D=S_P.
\]

Then

\[
\exists\ell_0,\ldots,\ell_{P-1}:
\quad h_i\le\ell_i,\quad
\ell_{(i+1)\bmod P}\le\ell_i+a_i
\quad\Longleftrightarrow\quad D\ge0.
\tag{B1}
\]

When the thresholds are natural numbers, the lower bounds can 也 be natural numbers. Define

\[
M=\max_{0\le i<P}(h_i-S_i).
\tag{B2}
\]

This is exactly the least initial value meeting every phase guard in a traversal. If \(D\ge0\), every later traversal 也 satisfies every guard:

\[
h_i\le x+kD+S_i\qquad(k\ge0,\ 0\le i<P,\ x\ge M).
\tag{B3}
\]

### Proof

Summing the cyclic transition inequalities gives \(0\le\sum_i a_i=D\). Conversely, suppose \(D\ge0\), 和 set \(\ell_i=M+S_i\). Definition (B2) gives every threshold. Each nonclosing edge is an equality:

\[
\ell_{i+1}=\ell_i+a_i\qquad(i<P-1).
\]

The closing edge is

\[
\ell_0=M\le M+D=\ell_{P-1}+a_{P-1}.
\]

Any valid initial value must satisfy \(x\ge h_i-S_i\) for every phase, establishing minimality of \(M\). Adding \(kD\ge0\) gives (B3). With natural thresholds, each constructed \(\ell_i\ge h_i\ge0\), so conversion to a natural number preserves every inequality. Independent coordinates are handled by applying this argument to each coordinate.

### THEOREM B.1 — application to the original two-band checker

In the inspected `ReturnCertificate.lean`, the structural word identities, actual carries, 和 `StepPal` are independent of the fields `lo` 和 `lo'`. The only run-length conditions are

\[
\ell_i,\ell'_i\ge2,\qquad
\ell_{i+1}\le\ell_i+a_i,\qquad
\ell'_{i+1}\le\ell'_i+b_i,
\]

where

\[
a_i=\gamma_i-2+j_i+j_{1,i},\qquad
b_i=\gamma_i-2+j_{2,i}+k_i.
\]

Therefore a supplied cyclic state/trim list satisfying **every structural condition** admits lower-bound fields exactly when

\[
\sum_i a_i\ge0,\qquad\sum_i b_i\ge0.
\tag{B4}
\]

The least concrete initial reserves are

\[
G_0=2-\min_{0\le i<P}\sum_{j<i}a_j,\qquad
H_0=2-\min_{0\le i<P}\sum_{j<i}b_j.
\tag{B5}
\]

**Proof.** Rewrite the 2 inequalities in `LocalOK` over integers, apply (B1) independently, 和 insert the resulting natural bounds into copies of the supplied links. All other link fields remain the supplied trim counts. Since those other checker conditions contain neither lower-bound field, they still hold. Equations (B5) are (B2) with constant threshold 2. This checker application is a written proof; the generic arithmetic (B1)–(B3) is the portion compiled in Lean.

### THEOREM B.2 — negative individual increments are permitted

For the abstract 3-phase increment cycle

\[
(2,-1),\quad(-3,2),\quad(2,0),
\]

the total is \((1,1)\), 和 the exact initial reserve for threshold \((2,2)\) is \((3,3)\). Its first traversal is

\[
(3,3)\to(5,2)\to(2,4)\to(4,4).
\]

Every subsequent traversal adds \((1,1)\). Starting at \((2,3)\) instead violates the first coordinate at the second step, yielding \((1,4)\). Thus requiring each increment to be nonnegative would incorrectly reject valid guarded cycles, while checking only the total without the initial reserve can admit an invalid start. This example is an integer-counter example, an abstract counter cycle.

### Formal endpoints

| Endpoint in `Agent205.CyclicGuards` | Exact scope |
|---|---|
| `reserve_le_iff` | Maximum prefix deficit |
| `initial_reserve_iff` | Least initial reserve for a positive cycle |
| `cyclic_bounds_iff_nonnegative` | Integer lower-bound feasibility iff nonnegative total |
| `constant_threshold_iff` | Constant-threshold specialization |
| `every_traversal_guard` | Every phase in every subsequent traversal |
| `two_coordinates_iff` | Independent pairs of coordinates |
| `natural_bounds_iff` | Natural thresholds 和 bounds with signed increments |

## THEOREM C — affine returns cannot amplify independent run lengths

Suppose a fixed, realizable template contains \(r\) independent mirrored constant-run parameters, with physical width

\[
L(n)=C+2\sum_{j=1}^r n_j.
\]

Assume an exact \(m\)-step return takes integral affine form

\[
n'=An+b
\]

throughout a complete integer orthant \(n_j\ge N_j\), 和 every output run length is nonnegative there. Then

\[
A_{ij}\ge0,\qquad \sum_i A_{ij}=1.
\tag{C1}
\]

Thus each column of \(A\) is a standard basis vector. If every output coordinate tends to infinity along \(n=t\mathbf1\), or every coordinate diverges under indefinite return iteration, then \(A\) is a permutation matrix. If the assignment of persistent long intervals to output intervals 也 preserves their order, then \(A=I\): the return is a translation \(n'=n+b\).

### Proof

If \(A_{ij}<0\), holding all other input coordinates fixed 和 sending \(n_j\) to infinity makes output coordinate \(i\) negative. This contradicts its assumed nonnegativity. A positive decimal step changes width by 0 or 1, so

\[
0\le2\mathbf1^T(A-I)n+2\mathbf1^Tb\le m
\]

throughout the orthant. Varying each independent coordinate forces its coefficient to vanish, giving the column sums in (C1). Integrality then makes each column a single unit vector. Growth on the diagonal ray excludes zero rows. Divergence under return iteration 也 excludes a zero row, since that coordinate would equal the constant \(b_i\) at every returned state. A square matrix with 1 unit per column 和 every row nonzero is a permutation. The only order-preserving permutation is the identity. ∎

The complete-orthant premise is essential. A formula valid only on a coupled chamber or a single parameter ray 不 support the independent-coordinate argument. Collisions or mergers can reduce the number of genuinely growing parameters.

### THEOREM C.1 — full guard criterion for a permutation return

Let \(F(x)=Px+b\), where \(P\) is a permutation matrix of order \(p\). Put

\[
d_r=\sum_{j=0}^{r-1}P^jb,\qquad V=d_p.
\]

Then \(PV=V\) 和

\[
F^{kp+r}(x)=P^rx+d_r+kV\qquad(0\le r<p).
\tag{C2}
\]

Suppose a guard region \(D=\{x:Gx\ge h\}\) guarantees the exact return formula **including every intermediate step**. The returned orbit remains in this certified region forever exactly when

\[
P^rx+d_r\in D\quad(0\le r<p),\qquad GV\ge0.
\tag{C3}
\]

Every coordinate tends to infinity exactly when every coordinate of \(V\) is positive. For a permutation cycle \(C_0\) of length \(\ell\),

\[
V_i=\frac p\ell\sum_{j\in C_0}b_j\qquad(i\in C_0).
\]

**Proof.** Compose the affine formula \(p\) times, then use \(P^p=I\) 和 \(PV=V\) to obtain (C2). Along each residue class modulo \(p\), each guard is an affine function of \(k\). It holds for every \(k\ge0\) exactly when its initial value satisfies the guard 和 its slope is nonnegative. The divergence statement follows from the same arithmetic rays. ∎

Congruence conditions must be included in the finite phase or checked separately. A proof that the guards ensure palindrome avoidance remains a separate obligation; (C3) applies only after the supplied guard region has been shown to guarantee all required conditions.

## Interface operators 和 spatial obstructions

### Definitions

All finite words use units-first coordinates. Put

\[
f_s(a)=\left\lfloor\frac{s+a}{10}\right\rfloor,
\qquad g_s(a)=s+a-10f_s(a),\qquad a\in\{0,1\}.
\]

For \(s\ne9\), put \(h_s=\mathbf1_{s\ge10}\) 和
\(D_s=s-9h_s\). The complete carry table reads

| Symbol | \(f_s(0)\) | \(f_s(1)\) | \(g_s(0)\) | \(g_s(1)\) |
|---|---:|---:|---:|---:|
| \(0\le s\le8\) | 0 | 0 | \(s\) | \(s+1\) |
| \(s=9\) | 0 | 1 | 9 | 0 |
| \(10\le s\le18\) | 1 | 1 | \(s-10\) | \(s-9\) |

## THEOREM D1 — exact finite run rewrite

Let \(q\) be a symmetric word of length \(L\), with carries
\(c_0=0\), \(c_{i+1}=f_{q_i}(c_i)\), 和 overflow bit
\(\delta=c_L\). Write the maximal runs as
\(s_1^{n_1}\cdots s_r^{n_r}\). For each run, let \(a_j\) be the
incoming carry in a scan from the left, 和 \(b_j\) the incoming carry
in a scan from the right, each scan starting at 0 outside the word.

When \(\delta=0\), replace each run independently as follows:

\[
9^n\longmapsto\bigl(18-9(a+b)\bigr)^n;
\]

\[
s^1\longmapsto[g_s(a)+g_s(b)]\quad(s\ne9);
\]

\[
s^n\longmapsto
[g_s(a)+D_s]\;(2D_s)^{n-2}\;[D_s+g_s(b)]
\quad(s\ne9,\ n\ge2).
\]

When \(\delta=1\), the output starts 和 ends with
\(E=g_{s_1}(0)+1\). Each run contributes an interior block of
length \(n_j-1\), labeled

\[
B_j=\begin{cases}
2D_{s_j},&s_j\ne9,\\
18-9(a_j+b_j),&s_j=9.
\end{cases}
\]

Between consecutive runs \(t=s_{j-1}\) 和 \(s=s_j\), insert the
single symbol

\[
I_j=g_s(f_t(a_{j-1}))+g_t(f_s(b_j)).
\]

Thus the complete output reads

\[
E\;B_1^{n_1-1}\;I_2\;B_2^{n_2-1}\cdots
I_r\;B_r^{n_r-1}\;E.
\]

All adjacent equal output symbols may subsequently be merged.

### Proof

Define \(\rho_i=c_{L-1-i}\). Symmetry of \(q\) gives
\(\rho_{L-1}=0\) 和
\(\rho_{i-1}=f_{q_i}(\rho_i)\), so \(\rho_i\) equals the incoming
carry from the right. The digit produced at position \(i\) equals
\(e_i=g_{q_i}(c_i)\).

For \(\delta=0\), folding pairs positions \(i\) 和 \(L-1-i\), hence

\[
q'_i=g_{q_i}(c_i)+g_{q_i}(\rho_i).
\]

If \(s\le8\), the first processed symbol sets the outgoing carry to
0, regardless of the incoming bit. If \(s\ge10\), the first processed
symbol sets the outgoing carry to 1, regardless of the incoming bit.
Consequently, on a non9 run of length at least 2, the first cell sees
carry pair \((a,h_s)\), the last cell sees \((h_s,b)\), 和 each strictly
interior cell sees \((h_s,h_s)\). Since \(g_s(h_s)=D_s\), the stated
formula follows. A singleton sees \((a,b)\). For \(s=9\), the carry
persists throughout the run, so each cell sees \((a,b)\). The table gives
\(g_9(a)+g_9(b)=18-9(a+b)\). These cover all cases.

For \(\delta=1\), the added digit occupies position \(L\), so the
endpoints of the folded word equal \(1+e_0=E\). At an interior output
position \(1\le i\le L-1\), symmetry gives \(q_{L-i}=q_{i-1}\), hence

\[
q'_i=g_{q_i}(c_i)+g_{q_{i-1}}(\rho_{i-1}).
\]

If the bond between \(i-1\) 和 \(i\) lies inside a non9 run, each carry
has already passed through a copy of that symbol, so the output equals
\(2D_s\). If the bond lies inside a 9-run, the unchanged incoming bits
give \(18-9(a+b)\). At a bond between runs \(t,s\), the left carry equals
\(f_t(a_{j-1})\), 和 the right carry equals \(f_s(b_j)\), giving \(I_j\).
There are \(L-r\) internal bonds, \(r-1\) between-run bonds, 和 2 endpoints,
so all \(L+1\) output positions are accounted for. ∎

### Explicit interface cases

For adjacent non9 symbols, the overflow interface simplifies to

\[
I(t,s)=D_t+D_s=t+s-9(h_t+h_s).
\]

For \(\delta=0\), an interface between non9 runs of length at least 2
changes the last cell of \(t\) 和 first cell of \(s\) to

\[
\bigl[2D_t+h_s-h_t\bigr]
\bigl[2D_s+h_t-h_s\bigr].
\]

The four type cases read

| \(t\)-type | \(s\)-type | Last \(t\)-cell | First \(s\)-cell |
|---|---|---:|---:|
| low | low | \(2t\) | \(2s\) |
| low | high | \(2t+1\) | \(2s-19\) |
| high | low | \(2t-19\) | \(2s+1\) |
| high | high | \(2t-18\) | \(2s-18\) |

For an overflow interface \(9\to s\ne9\), with carry \(a\) entering
the 9-run from the left,

\[
I(9,s)=\begin{cases}9+s+a,&s\le8,\\s-10+a,&s\ge10.\end{cases}
\]

For \(t\ne9\to9\), with carry \(b\) entering the 9-run from the right,

\[
I(t,9)=\begin{cases}t+9+b,&t\le8,\\t-10+b,&t\ge10.\end{cases}
\]

Adjacent maximal 9-runs cannot occur. Their artificial split would
contribute the same bulk symbol \(18-9(a+b)\).

## THEOREM D2 — a carry-memory obstruction to bounded-radius locality

For every positive \(n,m,r\), the symmetric words

\[
q=8^n9^m10^r9^m8^n,
\qquad \widetilde q=8^n9^m8^r9^m8^n
\]

give overflow 0. Their corresponding 9-runs map respectively to
\(9^m\) 和 \(18^m\). Thus a distant reset can change every output cell
of an arbitrarily long 9-run. A finite-state interface description must
retain the directional carry bits; bounded geometric radius alone fails.

### Proof

Each outside 8-run resets to 0, so the final carry equals 0. In \(q\),
the left 9-run receives carries \((0,1)\), since the middle 10-run resets
to 1. In \(\widetilde q\), the left 9-run receives \((0,0)\). Theorem D1
gives 9 和 18 respectively. Reflection gives the stated right-run
outputs. The central symbol, when present, equals 10 or 8 和 therefore
satisfies the required even-parity condition for realizability as a folded decimal word. ∎

## THEOREM D3 — exact reflection law for isolated interfaces

Let \(u:\mathbb Z\to\{0,\ldots,18\}\) be constant \(A\ne9\) sufficiently
far left 和 constant \(B\ne9\) sufficiently far right. Define unique
left 和 right carry fields by

\[
\ell_{i+1}=f_{u_i}(\ell_i),\qquad
r_{i-1}=f_{u_i}(r_i),
\]

with stable tail values \(h_A\) 和 \(h_B\). Define

\[
(U_0u)_i=g_{u_i}(\ell_i)+g_{u_i}(r_i),
\]

\[
(U_1u)_i=g_{u_i}(\ell_i)+g_{u_{i-1}}(r_{i-1}).
\]

For translation \((S_vu)_i=u_{i-v}\) 和 reflection \((Ru)_i=u_{-i}\),

\[
U_\delta S_v=S_vU_\delta,
\qquad U_\delta R=S_\delta R U_\delta.
\]

Consequently, for any itinerary \(\delta_0,\ldots,\delta_{m-1}\), put
\(U=U_{\delta_{m-1}}\cdots U_{\delta_0}\) 和
\(O=\sum_t\delta_t\). Then

\[
UR=S_ORU.
\]

If \(Uu=S_vu\), then

\[
U(Ru)=S_{O-v}(Ru).
\]

### Proof

The non9 tails reset the carries, making the carry fields uniquely
defined. Translating the input translates each carry field, which gives
the first identity directly. Reflection exchanges the carry fields.
Thus

\[
(U_0Ru)_i=g_{u_{-i}}(r_{-i})+g_{u_{-i}}(\ell_{-i})
=(RU_0u)_i.
\]

For the other mode,

\[
\begin{aligned}
(U_1Ru)_i
&=g_{u_{-i}}(r_{-i})+g_{u_{1-i}}(\ell_{1-i})\\
&=(U_1u)_{1-i}=(S_1RU_1u)_i.
\end{aligned}
\]

Moving translations through consecutive updates proves
\(UR=S_ORU\). Finally \(RS_v=S_{-v}R\), so
\(URu=S_ORUu=S_OR S_vu=S_{O-v}Ru\). ∎

### Isolation condition

The theorem applies inside a finite word whenever separate interface
cores stay separated by non9 bulk during the chosen itinerary. A concrete
sufficient initial separation equals \(2m+3\) constant symbols between
cores, including separation from the outside caps.

To verify this bound, suppose a profile differs from its constant tails
only on \([a,b)\). In mode 0, positions \(i\le a-2\) see the left stable
carry from each side, 和 positions \(i\ge b+1\) see the right stable
carry from each side. Therefore the updated core lies in
\([a-1,b+1)\). In mode 1, positions \(i\le a-1\) pair two left-tail
symbols, 和 positions \(i\ge b+1\) pair two right-tail symbols, so the
updated core lies in \([a,b+1)\). The new bulk symbols equal
\(F(s)=2D_s\), always even 和 therefore unequal to 9. Each boundary
can consequently advance toward the next interface by at most 1 per
step. A gap of \(2m+3\) leaves at least 3 reset symbols after \(m\)
steps. The carries supplied to each core consequently agree with its
infinite-tail model throughout the itinerary.

## THEOREM D4 — repeated-interface obstruction

Consider a finite return template with fixed interface cores 和 constant
non9 long bands, separated throughout an \(m\)-step itinerary as above.
Suppose the 2 oriented interface profiles 有 distinct tail symbols 和 are translates of the same
profile \(u\), 和 that \(Uu=S_vu\). If their marked cuts begin at
\(p<q\), the returning cuts occur at \(p+v<q+v\). Their separation
therefore stays constant.

Suppose, additionally, the region between those cuts contains at least 1 complete long run 和 consists of fixed
bounded blocks 和 complete long-run lengths \(n_1,\ldots,n_k\), with
the same fixed block lengths upon return. Then

\[
\sum_{j=1}^k\Delta n_j=0.
\]

In particular, nonnegative drift for every intervening long run forces
zero drift for every such run. Strict growth of every long run excludes
repeated oriented returning interface states.

### Proof

Translation covariance gives
\(U(S_pu)=S_{p+v}u\) 和 \(U(S_qu)=S_{q+v}u\). Isolation identifies these
profiles with their finite-word neighborhoods. The distance between the
corresponding cuts changes by \((q+v)-(p+v)-(q-p)=0\). The fixed pieces
contribute the same constant to this distance before 和 after return,
leaving the displayed sum. A sum of nonnegative integers equals 0 only
when every summand equals 0. ∎

The cuts can be chosen canonically: for \(A\ne B\), place the cut at the
first position differing from the left-tail symbol \(A\). Translation
moves this cut by the translation amount. Using this same definition
upon return prevents any arbitrary reallocation of interface symbols
to adjacent long runs.

## THEOREM D5 — homogeneous alternating two-band obstruction

Assume the return template uses alternating distinct non9 bands
\(A,B,A,B,\ldots\), every \(A\to B\) interface 有 profile \(u\), every
\(B\to A\) interface 有 the reflected profile \(Ru\), 和 the profiles
return after the common itinerary. Let \(Uu=S_vu\) 和 let the itinerary
contain \(O\) overflows. With fixed core sizes upon return, the drift
of an internal \(B\)-run equals \(O-2v\); the drift of an internal
\(A\)-run equals \(2v-O\).

Consequently, a template containing internal runs of each band type
cannot make every long run grow strictly on return. If those internal
run drifts are required to be nonnegative, they must all equal 0.
For a symmetric alternating word, this obstruction applies to 5 or
more long runs under the homogeneous-interface hypothesis.

A 3-run \(A/B/A\) template with fixed returning outside caps escapes
this obstruction. Its necessary drift vector equals

\[
(\Delta n_A^{\rm left},\Delta n_B,\Delta n_A^{\rm right})
=(v,O-2v,v).
\]

Strict growth therefore requires \(0<v<O/2\), hence \(O\ge3\).
These conditions alone 不 establish existence of such a template. This single central-run example allows its length parity to change; the paired-run template in theorem A instead returns a fixed central block 和 forces even \(\Gamma\).

### Proof

Theorem D3 gives velocities \(v\) for \(A\to B\) 和 \(O-v\) for
\(B\to A\). The distance between consecutive returning cuts changes
by right-cut velocity minus left-cut velocity. Fixed core contributions
cancel. A \(B\)-run lies between cuts of the first 和 second type, giving
\((O-v)-v=O-2v\). An internal \(A\)-run lies between cuts of the second
和 first type, giving \(v-(O-v)=2v-O\). The two quantities are negatives
of each other. A symmetric alternating word starts 和 ends with the
same band; 5 or more runs place each type internally.

For 3 runs, the left outside cap keeps its origin fixed, so the first
cut displacement contributes \(v\) to the left outer run. Symmetry
gives the same right outer drift. The middle drift remains \(O-2v\).
An integer strictly between 0 和 \(O/2\) requires \(O\ge3\). ∎

## THEOREM D6 — finite interface dictionary under an explicit width bound

Fix distinct non9 tail symbols \(A,B\) at a phase. Normalize each profile
so that its bounded core occupies \([0,k)\), its left tail 有 symbol
\(A\), 和 its right tail 有 symbol \(B\). Strip any leading \(A\) 和
trailing \(B\) from that core. For an imposed bound \(k\le H\), the
number of possible oriented profiles for a fixed unordered tail pair
不 exceed

\[
N_H=2\sum_{k=0}^H19^k.
\]

The stable tails determine all carry bits, so extra carry-state factors
are unnecessary here. If a cyclic list of \(p\) tail phases, retaining distinct tails throughout, is included
in the state, \(pN_H+1\) states suffice, including an escape state for
updates exceeding width \(H\). Each accepted transition 也 records
the integer shift introduced by normalizing the updated core.

### Proof

For each orientation 和 each length \(k\), at most \(19^k\) words
represent normalized cores. The normalization restriction only decreases
this count. The carry table uniquely computes an update from the core,
the tail symbols, 和 the chosen overflow mode. A result wider than \(H\)
goes to the escape state; an accepted result supplies another listed profile
和 a unique normalization displacement. This proves the bound.

For complementary bands \(c,18-c\) with \(c\notin\{0,9,18\}\), the
non9 bulk map enters one of

\[
2\to4\to8\to16\to14\to10\to2,
\qquad 6\to12\to6.
\]

Direct substitution in \(F(s)=2(s-9h_s)\) gives every displayed transition. Odd initial
bulk symbols enter an even phase after 1 step 和 cannot occur in an exact
positive-length return cycle of these isolated constant bands.

The width bound \(H\) remains a hypothesis. The finite dictionary
不 establish that all actual interfaces remain bounded, nor that
a local interface cycle is compatible with the outside caps 和 center.

## THEOREM D7 — complement-reflection forces zero inner growth

For a two-sided profile, define \((Cu)_i=18-u_i\). Then

\[
U_\delta C=CU_\delta.
\]

Suppose a complementary-band interface satisfies

\[
CRu=S_ku
\]

for some integer \(k\), 和 returns under an itinerary with \(O\)
overflows as \(Uu=S_vu\). Then

\[
2v=O.
\]

An odd value of \(O\) consequently excludes such an exact interface
return. An even value forces the interface to travel at exactly the
center displacement per return.

### Proof

For \(s\in\{0,\ldots,18\}\) 和 \(a\in\{0,1\}\), direct division
of \(19-(s+a)\) by 10 gives

\[
f_{18-s}(1-a)=1-f_s(a),
\qquad
g_{18-s}(1-a)=9-g_s(a).
\]

For completeness, if \(s+a\le9\), the first carry equals 0 和 its
complemented carry equals 1; the complemented digit equals
\(19-(s+a)-10=9-(s+a)\). If \(s+a\ge10\), the first carry equals 1
和 its complemented carry equals 0; the complemented digit equals
\(19-(s+a)=9-((s+a)-10)\). These two cases cover the whole range.

Complementing the input therefore complements the carry fields, 和
each digit term becomes 9 minus its original value. Each output sum
becomes 18 minus its original value, which proves commutation with
\(C\) in mode 0 和 in mode 1.

Theorem D3 then gives \(UCR=S_OCRU\). Applying \(U\) to the symmetry
identity in two ways yields

\[
UCRu=US_ku=S_{k+v}u,
\]

\[
UCRu=S_OCRS_vu=S_{O-v}CRu=S_{O-v+k}u.
\]

A profile with distinct eventual tail symbols cannot equal a nonzero
translate of itself: a nonzero translation period would propagate one
constant tail throughout the word, contradicting the other tail.
Thus \(k+v=O-v+k\), giving \(2v=O\). ∎

### Sharp-interface special case

The profile \(u_i=c\) for \(i<0\), \(u_i=18-c\) for \(i\ge0\), with
\(c\ne9\), satisfies \(CRu=S_1u\). Therefore any return of a sharp
complementary interface travels at velocity \(O/2\). This 不 assert
that a sharp-interface return exists.

### Paired-template corollary

Consider the symmetric template

\[
W(G,H)=P\,c^G\,A\,d^H\,Z\,d^H\,A^R\,c^G\,P^R,
\qquad d=18-c,
\]

where \(P,A,Z\) are fixed finite words, \(Z=Z^R\), 和 \(c,d\ne9\).
Suppose an \(m\)-step return preserves all bounded words 和 returns
the long bands without collisions. Let \(O\) count the overflows.
If the isolated left interface \(c^\infty A d^\infty\) satisfies the
complement-reflection symmetry of Theorem D7, then

\[
\Delta G=O/2,\qquad \Delta H=0.
\]

Indeed, the position of the left interface changes by \(\Delta G=v\),
因为 its preceding cap 和 its internal anchor offset return
unchanged. The whole length changes by \(2\Delta G+2\Delta H=O\).
Theorem D7 forces \(v=O/2\), hence \(\Delta H=0\). Equivalently,
the returned center moves by \(O/2\), exactly matching the interface,
so their separating band gains zero length.

This excludes simultaneous strict growth of the paired inner 和 outer
bands for this symmetry class. Positive total growth, a return with a
fixed inner band, 和 other interface symmetry classes remain possible
under this result.


## THEOREM E — finite validation records 和 reproducible code

The following computations check the exact identities against independent implementations. The 1000-step arithmetic orbits continue after their first palindrome. Every tested arithmetic seed reaches a palindrome; none supplies a Lychrel witness. These records support implementation fidelity; the infinite statements above depend on their written proofs or the indicated Lean proof.

### Compressed run model: executed output

```text
LOCAL_CARRY_IDENTITIES 76/76 PASS
SYMMETRIC_WORD_IDENTITIES 1000/1000 PASS modes=[495, 505]
ARITHMETIC_ORBIT seed=89 steps=1000 PASS first_palindrome=24 digits=399 overflows=397
ARITHMETIC_ORBIT seed=349 steps=1000 PASS first_palindrome=3 digits=428 overflows=425
ARITHMETIC_ORBIT seed=10001 steps=1000 PASS first_palindrome=0 digits=418 overflows=413
These are identity checks; no seed is claimed to be Lychrel.
```

The 1000 symmetric-word tests are deterministic tests of the transition identity using random seed 205; they 不 search for long-lived seeds or return certificates. The 3 arithmetic checks each execute 1000 actual decimal steps. In particular, treating any of these samples as a Lychrel construction would be refuted by the reported palindrome time.

Save the following complete code as `interface_model.py`, then run `python3 interface_model.py`:

```python
"""Run-compressed Agent 205 carry/refold model.

All words are in units-first order. This module is independent of the
repository and is intended for validating exact identities, not searching.
"""
from itertools import groupby
from random import Random


def carry(s, a):
    return int(s + a >= 10)


def digit(s, a):
    return (s + a) % 10


def compress(q):
    return [(s, len(list(items))) for s, items in groupby(q)]


def expand(runs):
    return [s for s, n in runs for _ in range(n)]


def run_step(runs):
    """Return (normalized RLE of T(q), overflow bit) for symmetric q.

    Counts are positive; singletons and runs of 9 are fully supported.
    The input and output remain compressed throughout this implementation.
    """
    assert runs and all(0 <= s <= 18 and n >= 1 for s, n in runs)
    assert runs == runs[::-1]
    assert all(runs[j][0] != runs[j+1][0] for j in range(len(runs)-1))
    r = len(runs)
    left = [0] * r
    right = [0] * r
    a = 0
    for j, (s, n) in enumerate(runs):
        left[j] = a
        # Carry maps are idempotent: constant 0, identity, or constant 1.
        a = carry(s, a)
    overflow = a
    a = 0
    for j in range(r - 1, -1, -1):
        s, n = runs[j]
        right[j] = a
        a = carry(s, a)
    out = []

    def append(s, n=1):
        if n <= 0:
            return
        assert 0 <= s <= 18
        if out and out[-1][0] == s:
            out[-1] = (s, out[-1][1] + n)
        else:
            out.append((s, n))

    if overflow == 0:
        for j, (s, n) in enumerate(runs):
            a, b = left[j], right[j]
            if s == 9:
                append(18 - 9 * (a + b), n)
            elif n == 1:
                append(digit(s, a) + digit(s, b))
            else:
                h = int(s >= 10)
                stable_digit = s - 9 * h
                append(digit(s, a) + stable_digit)
                append(2 * stable_digit, n - 2)
                append(stable_digit + digit(s, b))
    else:
        endpoint = digit(runs[0][0], 0) + 1
        append(endpoint)
        for j, (s, n) in enumerate(runs):
            if j:
                t = runs[j - 1][0]
                left_out = carry(t, left[j - 1])
                right_out = carry(s, right[j])
                append(digit(s, left_out) + digit(t, right_out))
            if s == 9:
                bulk = 18 - 9 * (left[j] + right[j])
            else:
                bulk = 2 * (s - 9 * int(s >= 10))
            append(bulk, n - 1)
        append(endpoint)
    assert out == out[::-1]
    assert sum(n for _, n in out) == sum(n for _, n in runs) + overflow
    return out, overflow


def direct_step(q):
    a = 0
    digits = []
    for s in q:
        digits.append((s + a) % 10)
        a = (s + a) // 10
    if a:
        digits.append(a)
    return [x + y for x, y in zip(digits, digits[::-1])], a


def q_from_n(n):
    digits = [int(c) for c in str(n)[::-1]]
    return [x + y for x, y in zip(digits, digits[::-1])]


def verify():
    count = 0
    for s in range(19):
        for a in (0, 1):
            for b in (0, 1):
                expected = (2*s+a+b if s < 9 else
                            18-9*(a+b) if s == 9 else
                            2*s-20+a+b)
                assert digit(s, a) + digit(s, b) == expected
                count += 1
    print(f"LOCAL_CARRY_IDENTITIES {count}/76 PASS")

    rng = Random(205)
    overflow_counts = [0, 0]
    for _ in range(1000):
        half = [rng.randrange(19) for _ in range(rng.randrange(1, 18))]
        half[0] = rng.randrange(1, 19)
        half = [s for s in half for _ in range(rng.randrange(1, 6))]
        center = [2*rng.randrange(10)] if rng.randrange(2) else []
        q = half + center + half[::-1]
        expected, delta = direct_step(q)
        got, got_delta = run_step(compress(q))
        assert expand(got) == expected and got_delta == delta
        overflow_counts[delta] += 1
    print(f"SYMMETRIC_WORD_IDENTITIES 1000/1000 PASS modes={overflow_counts}")

    for seed in (89, 349, 10001):
        n = seed
        runs = compress(q_from_n(n))
        first_palindrome = 0 if str(n) == str(n)[::-1] else None
        total_overflows = 0
        for step in range(1, 1001):
            runs, delta = run_step(runs)
            total_overflows += delta
            n += int(str(n)[::-1])
            assert expand(runs) == q_from_n(n), (seed, step)
            if first_palindrome is None and str(n) == str(n)[::-1]:
                first_palindrome = step
        print(f"ARITHMETIC_ORBIT seed={seed} steps=1000 PASS "
              f"first_palindrome={first_palindrome} "
              f"digits={len(str(n))} overflows={total_overflows}")
    print("These are identity checks; no seed is claimed to be Lychrel.")


if __name__ == '__main__':
    verify()
```

### Raw exterior, interface, 和 center identities: executed output

```text
Whole-word raw-block identities: 240/240 PASS
No-overflow cases: 120; overflow cases: 120
Exact exterior, interface, center length and sum identities: PASS
```

The selected cases include empty blocks, 9-runs inside finite blocks, positive exterior realizability, even centers, different same-residue phases, 和 different-residue phases. This bounded calculation tests the closed formulas; the proof above quantifies over arbitrary finite blocks. Save this independent code as `check_interface_charge.py`, then run `python3 check_interface_charge.py`:

```python
from itertools import product


def norm(word, carry):
    out, count = [], 0
    for x in word:
        x += carry
        carry, digit = divmod(x, 10)
        count += carry
        out.append(digit)
    return out, carry, count


def h(s):
    return int(s >= 10)


def u(s):
    return s - 9 * h(s)


def z(a, b):
    assert len(a) == len(b)
    return [x + y for x, y in zip(a, b)]


def pair(a):
    return z(a, a[::-1])


def raw_exterior(B, s):
    U, alpha, KU = norm(B, 0)
    V, gamma, KV = norm(B[::-1], h(s))
    xi = s + alpha - 10 * h(s)
    E = z(U + [xi], V[::-1] + [u(s)]) if not gamma else z(U + [xi], [1] + V[::-1])
    assert len(E) == len(B) + 1
    assert sum(E) == 2 * sum(B) + (2-gamma)*s - 9*((2-gamma)*h(s)+KU+KV)
    return E, gamma


def raw_interface(A, s, t, gamma):
    U, alpha, KU = norm(A, h(s))
    V, beta, KV = norm(A[::-1], h(t))
    xi, eta = t + alpha - 10*h(t), s + beta - 10*h(s)
    I = z([u(s)] + U + [xi], [eta] + V[::-1] + [u(t)]) if not gamma else z(U + [xi], [eta] + V[::-1])
    a = 2-gamma
    assert len(I) == len(A)+a
    assert sum(I) == 2*sum(A)+a*(s+t)-9*(a*(h(s)+h(t))+KU+KV)
    return I


def raw_center(C, s, gamma):
    assert C == C[::-1]
    D, kappa, K = norm(C, h(s))
    xi = s + kappa - 10*h(s)
    F = pair([u(s)] + D + [xi]) if not gamma else pair(D + [xi])
    a = 2-gamma
    assert len(F) == len(C)+a
    assert sum(F) == 2*sum(C)+2*a*s-18*a*h(s)-18*K
    return F


def shape(B, A, C, s, t, n, m):
    return B+[s]*n+A+[t]*m+C+[t]*m+A[::-1]+[s]*n+B[::-1]


cases = 0
overflow_cases = [0, 0]
for (s, t), B, A, C in product(
    [(2,4), (2,8), (10,14), (16,2), (4,10)],
    [[3], [12], [9,2], [9,14]],
    [[], [9], [9,9], [0,18,9]],
    [[], [8], [9,2,9]],
):
    old = shape(B, A, C, s, t, 5, 7)
    digits, gamma, _ = norm(old, 0)
    actual = pair(digits+([1] if gamma else []))
    E, exterior_gamma = raw_exterior(B, s)
    assert gamma == exterior_gamma
    I = raw_interface(A, s, t, gamma)
    F = raw_center(C, t, gamma)
    predicted = shape(E, I, F, 2*u(s), 2*u(t), 5-2+gamma, 7-2+gamma)
    assert actual == predicted
    overflow_cases[gamma] += 1
    cases += 1

print(f'Whole-word raw-block identities: {cases}/{cases} PASS')
print(f'No-overflow cases: {overflow_cases[0]}; overflow cases: {overflow_cases[1]}')
print('Exact exterior, interface, center length and sum identities: PASS')

```

### Guard reserve: executed 1000-step check 和 failing smaller reserve

```python
a = [(2, -1), (-3, 2), (2, 0)]
x = [3, 3]
minimum = min(x)
for t in range(1000):
    dx = a[t % 3]
    x = [x[0] + dx[0], x[1] + dx[1]]
    minimum = min(minimum, *x)
    assert min(x) >= 2
print(f"ABSTRACT_GUARD steps=1000 PASS final={tuple(x)} minimum={minimum}")
y = [2, 3]
for t, dx in enumerate(a, 1):
    y = [y[0] + dx[0], y[1] + dx[1]]
    if min(y) < 2:
        print(f"INSUFFICIENT_RESERVE first_failure_step={t} state={tuple(y)}")
        break
```

```text
ABSTRACT_GUARD steps=1000 PASS final=(338, 335) minimum=2
INSUFFICIENT_RESERVE first_failure_step=2 state=(1, 4)
```

### Lean verification

The module uses only `Std`, with dependencies restricted to the pinned core distribution. The source passes the repository scan forbidding `sorry`, `admit`, custom `axiom`, 和 `native_decide`. The permitted axiom audit for every registered endpoint returns exactly the existing repository allowlist:

```text
'Agent205.CyclicGuards.reserve_le_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent205.CyclicGuards.initial_reserve_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent205.CyclicGuards.cyclic_bounds_iff_nonnegative' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent205.CyclicGuards.constant_threshold_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent205.CyclicGuards.every_traversal_guard' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent205.CyclicGuards.two_coordinates_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent205.CyclicGuards.natural_bounds_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Repository verification is run with the pinned Lean 4.19.0 compiler:

```bash
python3 tools/verify.py --changed
```

Executed repository verification output:

```text
[rules] 4824 Lean files, 288 projects, OK
[changed] against origin/main: 1 new/changed Lean file(s); building 1 module(s); auditing 1 project(s)
[build] up to 1 Lean file(s) at a time
✔ [2/2] Built P196.Agent205InterfaceGrowth.CyclicGuards
Build completed successfully.
[build] OK
[axioms] 7 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

A separate run with CPU affinity restricted to 1 core completed successfully:

```text
exit_code=0
single_core=0
elapsed_seconds=0.824
peak_rss_kib=461976
```

The measured peak is approximately 451 MiB, below the repository limit of 8 GiB; elapsed time is below its 20-minute limit. The final pre-push gate is rerun after updating the local base.

## IDEA — the remaining construction question

The finite-state route becomes concrete only after an explicit interface-width bound is imposed. Each accepted edge must carry its **actual** overflow mode, exact block identity, run-length increment, 和 phase safety test. A local interface cycle alone omits cap/center compatibility. The finite dictionary theorem 不 establish a width bound for arbitrary trajectories, 和 the guard theorem 不 manufacture a structural cycle.

The sharpest question remaining from this direction is:

> Does a realizable complementary six-phase template admit a bounded exact return with a complement-reflection-asymmetric interface, compatible returning exterior 和 symmetric center, \(\Delta G>0\), \(\Delta H>0\), 和 every intermediate normalized whole digit word nonpalindromic?

The necessary conditions obtained here are

\[
m\ge72,\qquad
9\mid\Delta G,\quad9\mid\Delta H,\qquad
\Gamma=2(\Delta G+\Delta H),\qquad
0<v=\Delta G<\Gamma/2.
\]

A positive answer would still require explicit finite words, the complete overflow itinerary, exact trim identities, 和 verified phase safety. After those structural data exist, theorem B supplies the lower-bound fields 和 the existing certificate framework supplies the final ordinary-integer bridge. The weaker search with \(\Delta G\ge0\), \(\Delta H\ge0\), 和 at least 1 positive gain remains relevant: the obstructions to strict growth of the **2** coordinates 不 exclude it.

## Sources opened 和 attribution

All repository links below are pinned to the inspected baseline. These are sources for the existing definitions 和 imported background. Formal status of the new results is specified separately above.

- [Exact template normalizer 和 ordinary-integer bridge: TemplateStep.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean).
- [Original state, trim, `LocalOK`, safety, 和 soundness definitions: ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean).
- [Existing complementary two-band length identities 和 necessity of nonnegative total gains: CertificateAccounting.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateAccounting.lean).
- [Existing two-band charge clocks: CertificateCharge.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateCharge.lean).
- [Existing physical overflow budget: CertificateCarryBudget.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateCarryBudget.lean).
- [Existing two-band six-phase divisibility 和 period restrictions: CertificateConsequences.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateConsequences.lean).
- [Existing positive symbolic-value growth: SymbolicGrowth.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/SymbolicGrowth.lean).
- [New Lean source in this change: CyclicGuards.lean](lean/P196/Agent205InterfaceGrowth/CyclicGuards.lean).
