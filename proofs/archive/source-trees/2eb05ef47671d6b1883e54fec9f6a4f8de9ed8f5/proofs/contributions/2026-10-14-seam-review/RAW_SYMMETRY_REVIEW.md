# Raw isolated normalization and actual palindrome symmetry

The equivalence claimed in the external
`2026-10-14-active-seam-safety.md` is correct on its stated domain,
provided raw symmetry uses the **actual whole output width**, including
padding zeros if necessary. The following proof works for every partition
into nonempty consecutive blocks; it does not infer an all-length result
from finite tests.

Let `Q` be a canonical symmetric coefficient word of length `L`, with
coefficients in `0..18`. In the ordinary pair-word setting its odd center
is even. Write `D` for its ordinary decimal normalization, `e` for its
final carry, and `n=L+e` for the actual output width. Let `E` be the raw
sum of the separately normalized blocks at their original offsets,
including each isolated terminal carry.

For each original column `i`, let `c_i` be the carry leaving that column
in its isolated block normalization. Set

\[
C(x)=\sum_{i=0}^{L-1}c_i x^i.
\]

Each `c_i` is zero or one. The exact isolated-normalization identity is

\[
E(x)=Q(x)+(x-10)C(x).
\tag{1}
\]

Isolated terminal carries must be included in `E` for (1) to hold.
Every coefficient of `E` is nonnegative, and `E(10)=Q(10)=D(10)`.
Consequently `E` has no nonzero coefficient beyond the actual output
width `n`; it may have leading zeros in that width. Define physical
reflection by `R_n F(x)=x^(n-1)F(x^-1)`.

## The reflection argument

Assume the raw polynomial `E` is symmetric at width `n`.

If `e=0`, both `Q` and `E` are symmetric at width `L`. Reflecting (1)
and subtracting gives

\[
(x-10)C(x)=(1-10x)x^{L-2}C(x^{-1}).
\]

Evaluate at `x=1/10`. The right side vanishes, while the nonzero factor
on the left forces `C(1/10)=0`. Since all coefficients of `C` are
nonnegative, `C=0`. No isolated normalization carries at any column,
so every coefficient of `Q` is at most 9. The actual normalization
also has no carries, and `D=Q=E` is palindromic.

If `e=1`, the reflection width is `L+1`, and symmetry of `Q` at width
`L` implies `R_(L+1)Q=xQ`. Reflecting (1) now gives

\[
(1-x)Q(x)+(x-10)C(x)
=(1-10x)x^{L-1}C(x^{-1}).
\]

At `x=1/10` this says

\[
Q(1/10)=11C(1/10).
\tag{2}
\]

To pass from this numerical equality to coefficient equality, let
`b_i` be the incoming carry at column `i` inside its isolated block;
at block starts it is reset to zero. Then
`c_i=floor((q_i+b_i)/10)` with `b_i` in `{0,1}`. Thus

\[
q_i-11c_i\in
\begin{cases}
\{0,\ldots,9\},&c_i=0,\\
\{-2,\ldots,7\},&c_i=1.
\end{cases}
\]

Every coefficient of `Q-11C` lies in `[-2,9]`. Multiply (2) by
`10^(L-1)` and reduce modulo 10. The highest-index coefficient is
divisible by 10; zero is the only such integer in `[-2,9]`. Remove it
and repeat. Hence `Q=11C` coefficientwise. Every coefficient of `Q`
is zero or 11, and its positive outside coefficient is 11. This is
the overflow palindrome-predecessor case. Directly, actual carry out
of a column is one precisely when that coefficient is 11, regardless
of its incoming bit. Thus the actual carry polynomial equals `C`,
and `D=E=(1+x)C`, symmetric at width `L+1`.

This proves raw symmetry implies actual palindrome symmetry. The same
argument applied to the one-block partition, where `E=D`, also proves
the two-case canonical palindrome-predecessor classification used above.

## Converse and the seam mask

If `D` is palindromic, the just-proved classification gives either all
coefficients of `Q` at most 9, or all coefficients in `{0,11}` with
outside 11. In the former case all actual and isolated carries are zero.
In the latter, actual and isolated outgoing carries both equal one
exactly at the 11 coefficients. Therefore the actual and isolated carry
polynomials agree for every partition, and `E=D` is raw symmetric.

Equivalently, with the actual seam mask `K` from the external note,

\[
D=E+(x-10)K,
\qquad
E=R_nE\ \Longleftrightarrow\ D=R_nD,
\]

and either symmetry forces `K=0`. A nonzero `K` therefore certifies a
nonpalindromic ordinary output. The condition `K=0` alone does not
certify a palindrome: for `Q=(12,12)`, even the partition into singleton
blocks has `K=0`, while `D=(2,3,1)` represents the nonpalindrome 132.

No claim here preserves a nonzero seam mask through future iterations.
The external note's finite-step conclusion and stated limitation are
sound. In particular, the conjunction “raw `E` symmetric and actual
`K` nonzero” is impossible on this domain.

## Retained controls

`check_raw_symmetry.py` checks all 3,969 admissible canonical words of
widths one through five and every partition into nonempty consecutive
blocks: **58,221 cases**. It verifies (1), the actual seam identity,
the coefficient bound `-2 <= q_i-11c_i <= 9`, both symmetry directions,
the exact predecessor classification, and the nonzero-mask safety test.
Each whole normalization is also compared with literal integer
evaluation of the coefficient polynomial.

All outcomes are retained in `raw_symmetry_controls.bin.gz`, with its
complete enumeration schema, hash, counts, and explicit seam examples in
`raw_symmetry_controls.json`. These finite checks audit the arithmetic;
the argument above supplies the arbitrary-width proof. Run:

```sh
python -B proofs/contributions/2026-10-14-seam-review/check_raw_symmetry.py
```
