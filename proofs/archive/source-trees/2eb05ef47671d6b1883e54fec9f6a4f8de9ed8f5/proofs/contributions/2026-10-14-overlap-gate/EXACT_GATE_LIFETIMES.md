# Exact lifetimes of four delayed-overlap gate cores

This note extends the two-step identities in
[`VARIABLE_OVERLAP_AND_GATE.md`](../../research/main_existence_attempt/correlation_pass/constructive/VARIABLE_OVERLAP_AND_GATE.md).
It proves finite first-hit times, not recurrence, Lychrel existence, or a
claim about the orbit of 196. It does not alter the existing gate theorem.

## Result

Let all words be written from least to most significant coefficient. Set

\[
A_{r,u,v}=(1,0^r,u,v,v,u,0^r,1),\qquad
Q_{r,u,v}=(1+x)A_{r,u,v},\qquad r\ge1.
\]

For every ordinary decimal integer whose pair-sum word is \(Q_{r,u,v}\),
the following are its **exact first positive palindrome times**:

| Core \((u,v)\) | Spacer range | First positive palindrome time | Status |
|---|---|---:|---|
| \((1,5)\) | Every \(r\ge1\) | 3 | Previously proved |
| \((2,5)\) | Every \(r\ge1\) | 4 | Proved here |
| \((2,6)\) | Every \(r\ge1\) | 4 | Proved here |
| \((3,5)\) | Every \(r\ge1\) | 4 | Proved here |
| \((1,6)\) | Every \(r\ge5\) | 11 | Proved here |

Thus increasing the spacer indefinitely cannot create arbitrarily long
palindrome delays within any of these five core families. This does not
classify the entire remaining \((1,7)\) family or the four short-spacer
instances \((u,v)=(1,6), r\in\{1,2,3,4\}\).

Write \(N(Q)\) for the complete ordinary digit normalization, including a
final overflow digit, and
\(G(Q)=N(Q)+\operatorname{rev}(N(Q))\). The ordinary successor of every
realization of \(Q\) is the same integer, with digit word \(N(Q)\).
Consequently it suffices to identify the first \(t\ge0\) for which
\(N(G^t(Q))\) is palindromic; its ordinary first-hit time is \(t+1\).

## Three cores terminate at the fourth addition

For \((u,v)\in\{(2,5),(2,6),(3,5)\}\), put \(z=u+v\). The existing gate
identities give the first three pair words:

\[
\begin{aligned}
Q_0&=(1,1,0^{r-1},u,z,2v,z,u,0^{r-1},1,1),\\
Q_1&=(2,2,0^{r-1},2u,2z+1,4v-20,2z+1,2u,0^{r-1},2,2),\\
Q_2&=(4,4,0^{r-1},4u+1,4z-18,8v-38,4z-18,4u+1,0^{r-1},4,4).
\end{aligned}
\]

The third pair update is exactly the following coefficient polynomial:

\[
Q_3=8(1+x+x^{2r+5}+x^{2r+6})+x^rH_{u,v}(x),
\]

where:

| Core | Coefficients of \(H\), low to high | Outgoing-carry positions in \(N(Q_2)\) |
|---|---|---|
| \((2,5)\) | \((1,9,0,6,0,9,1)\) | \(r+2,r+4,r+5\) |
| \((2,6)\) | \((1,9,9,2,9,9,1)\) | \(r+2,r+3,r+4,r+5\) |
| \((3,5)\) | \((1,7,9,6,9,7,1)\) | \(r+1,r+2,r+4,r+5\) |

These carry lists follow directly by normalizing the displayed five-term
core of \(Q_2\); the carry after the core is absorbed by the following zero
or, when \(r=1\), by the first outside coefficient 4. The other outside
coefficient is 4, so no final overflow is possible. Pairing the resulting
digits gives the formula for \(Q_3\).

Every coefficient of \(Q_3\) is at most 9. For \(r\ge2\), the central and
outside terms have disjoint support. At \(r=1\), the only overlaps add the
two end coefficients 1 of \(H\) to the adjacent outside coefficients 8,
giving 9. Thus \(N(Q_3)=Q_3\) is a palindrome for every \(r\ge1\).

For completeness, a symmetric pair word with **no final overflow** has a
palindromic normalization if and only if it has no carries at all. Indeed,
write

\[
d_i=q_i+c_i-10c_{i+1},\qquad c_0=c_n=0,\quad c_i\in\{0,1\}.
\]

Symmetry of both \(q\) and \(d\), with \(j=n-1-i\), implies

\[
c_i-c_j=10(c_{i+1}-c_{j+1}).
\]

The two sides can agree only when both are zero. Starting at the two ends
therefore forces all carries to be zero. The converse is immediate.

Each of \(Q_0,Q_1,Q_2\) above has an internal coefficient greater than 9
and outside coefficients less than 9. Hence it has at least one carry,
but no final overflow. Their normalizations are nonpalindromic. This proves
that the first positive palindrome time is exactly 4.

## The \((1,6)\) core terminates at the eleventh addition for every \(r\ge5\)

For the following table, juxtaposition denotes concatenation and
\(B^R\) means the reversed word. Define

\[
Q_t=B_t\,0^{r-e_t}\,H_t\,0^{r-e_t}\,B_t^R.
\]

All exponents are nonnegative for \(r\ge5\). These are exact pair words:

| \(t\) | \(B_t\) | \(e_t\) | \(H_t\) |
|---:|---|---:|---|
| 0 | \((1,1)\) | 1 | \((1,7,12,7,1)\) |
| 1 | \((2,2)\) | 1 | \((2,15,4,15,2)\) |
| 2 | \((4,4)\) | 1 | \((5,10,10,10,5)\) |
| 3 | \((8,8)\) | 1 | \((11,1,2,1,11)\) |
| 4 | \((16,16)\) | 2 | \((1,2,3,4,3,2,1)\) |
| 5 | \((7,14,7)\) | 3 | \((1,3,5,7,7,5,3,1)\) |
| 6 | \((15,8,15)\) | 3 | \((2,6,10,14,14,10,6,2)\) |
| 7 | \((6,14,14,6)\) | 4 | \((2,8,7,6,10,6,7,8,2)\) |
| 8 | \((13,9,9,13)\) | 4 | \((4,16,14,13,0,13,14,16,4)\) |
| 9 | \((4,4,0,4,4)\) | 5 | \((4,11,12,9,4,4,9,12,11,4)\) |
| 10 | \((8,8,0,8,8)\) | 5 | \((9,3,5,9,9,9,9,5,3,9)\) |

Here are complete normalization certificates for the table. In row \(t\),
let \(S_t=L_t\cup(r+M_t)\cup(2r+R_t)\), put
\(C_t(x)=\sum_{i\in S_t}x^i\), and set

\[
D_t(x)=Q_t(x)+(x-10)C_t(x).
\]

The column \(k_t\) means \(\deg D_t=2r+k_t\).

| \(t\) | \(L_t\) | \(M_t\) | \(R_t\) | \(k_t\) |
|---:|---|---|---|---:|
| 0 | \(\varnothing\) | \(\{3\}\) | \(\varnothing\) | 6 |
| 1 | \(\varnothing\) | \(\{2,4\}\) | \(\varnothing\) | 6 |
| 2 | \(\varnothing\) | \(\{2,3,4\}\) | \(\varnothing\) | 6 |
| 3 | \(\varnothing\) | \(\{1,5\}\) | \(\varnothing\) | 6 |
| 4 | \(\{0,1\}\) | \(\varnothing\) | \(\{5,6\}\) | 7 |
| 5 | \(\{1\}\) | \(\varnothing\) | \(\{6\}\) | 7 |
| 6 | \(\{0,2\}\) | \(\{2,3,4,5\}\) | \(\{5,7\}\) | 8 |
| 7 | \(\{1,2\}\) | \(\{4\}\) | \(\{6,7\}\) | 8 |
| 8 | \(\{0,1,2,3\}\) | \(\{1,2,3,5,6,7\}\) | \(\{5,6,7,8\}\) | 9 |
| 9 | \(\varnothing\) | \(\{1,2,3,7,8\}\) | \(\varnothing\) | 9 |
| 10 | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | 9 |

Expanding these finite polynomials verifies that every coefficient of
\(D_t\) is a decimal digit and its leading digit is nonzero for every
\(r\ge5\). Since \(D_t(10)=Q_t(10)\), uniqueness of decimal expansion proves
that \(D_t=N(Q_t)\). Direct coefficient comparison then gives

\[
Q_{t+1}(x)=D_t(x)+x^{2r+k_t}D_t(x^{-1})\quad(0\le t<10).
\]

This is an algebraic certificate for the unrestricted spacer parameter,
not an inference from a finite trajectory sample. The accompanying checker
performs these identities with sparse two-variable polynomials, with
\(y=x^r\), and explicitly handles every possible collision of their affine
exponents for \(r\) in the claimed range.

The earlier ten ordinary successors are nonpalindromic:

- For \(t=0,1,2,3,9\), there is an internal carry and no final overflow, so
  the no-overflow lemma above applies.
- For \(t=4,6,8\), the least significant normalized digits are respectively
  6, 5, 3, whereas the new leading digit is 1.
- For \(t=5\), the least and most significant normalized digits are 7 and 8.
- For \(t=7\), they are 6 and 7.

Finally, \(Q_{10}\) is symmetric and all its coefficients are at most 9,
including at \(r=5\), where its zero runs are empty. Therefore
\(N(Q_{10})=Q_{10}\) is palindromic. The first positive palindrome time is
exactly 11.

## Reproduction and limits

From the repository root, run:

```sh
python -B proofs/contributions/2026-10-14-overlap-gate/exact_gate_lifetimes.py
```

The script verifies 23 universal sparse-polynomial normalization
certificates. Its separate 264 ordinary-integer controls cover
\(r=1,\ldots,64,127,256,1000\), restricted to \(r\ge5\) for the time-11
claim. Those controls construct actual decimal seeds and use literal
integer reversal and addition, independently of the symbolic carry data.

The universal argument is mathematical plus a small reproducible symbolic
checker. It is not Lean verification. No infinite safe orbit is asserted.
The exact delayed gate remains a useful finite identity, but four of its
five previously unclassified cores now have the finite lifetimes above.
