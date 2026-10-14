# Exact incoming-carry response at finite block collisions

`IncomingCarry.lean` and `CarryTransferNormalForm.lean` prove 24 supporting
theorems for the finite decimal
column dynamics already formalized in `LychrelDigitSums.lean`. These
results identify exactly how a changed incoming carry affects a block.
They do not prove an invariant collision family or a decimal Lychrel number.

## Exact transfer criterion

For a block q of length L whose coefficients lie in {0,...,18}, write
c_a(i) for the carry after i columns when the initial carry is a, and
d_a(i) for the normalized digit in column i. For a,b in {0,1},

\[
c_a(L)\ne c_b(L)
\quad\Longleftrightarrow\quad
a\ne b\ \text{and}\ q_i=9\text{ for every }0\le i<L.
\]

This is `carryIn_ne_iff`. Every finite-block carry transfer is therefore
one of exactly three functions: constant zero, the identity, or constant
one. The identity case occurs exactly for all-nine blocks. The empty
block is included and has identity transfer.

The proof uses the exact decimal recursion. With bounded incoming carries,
the two outgoing carries of one column differ precisely when its
coefficient is nine and its incoming carries differ. Induction supplies
the all-length criterion.

The followup module identifies the transfer class explicitly using the
**last** non-nine coefficient q_j:

\[
c_a(L)=\lfloor q_j/10\rfloor.
\]

Thus q_j<=8 gives the constant-zero transfer and q_j>=10 gives the
constant-one transfer. Coefficients after j are all nine and merely pass
that carry along. `rightmost_nonNine_transfer` formalizes the two cases;
`actual_interval_last_nonNine` proves the statement directly for any
interval of the actual decimal carry computation. This is independent
of the first-non-nine position controlling the digit correction below.

## Exact digit correction

Suppose j is the first position with q_j != 9. Then

\[
d_1(i)-d_0(i)=
\begin{cases}
-9,&i<j,\\
1,&i=j,\\
0,&j<i<L.
\end{cases}
\]

The outgoing carries are equal. This is proved coefficientwise in
`first_nonNine_response_coefficient`, so the corresponding formal
polynomial correction is exactly

\[
R_q(x)=x^j-9\sum_{i=0}^{j-1}x^i.
\]

For an all-nine block, every digit instead changes from nine to zero and
the outgoing carry changes from zero to one:

\[
R_q(x)=-9\sum_{i=0}^{L-1}x^i.
\]

The coefficientwise assertions, including the all-nine edge case, are
Lean-checked; the displayed polynomial equalities are their direct finite
sum reformulation. No polynomial library or unchecked arithmetic tactic
is used in the Lean source.

## Connection to the actual finite word

`carryIn_actual_interval` and `outputIn_actual_interval` identify the block
calculation with the repository's actual decimal operations, initialized
by the carry that really enters the interval. `carryIn_add` proves exact
composition when concatenating blocks.

The final theorems directly address two identical coefficient blocks
occurring at positions a and b inside one finite bounded word:

* `actual_repeated_block_transfer_ne_iff`: the actual outgoing carries
  differ exactly when the actual incoming carries differ and the common
  block consists entirely of nines.
* `actual_repeated_block_output_locality`: after any common non-nine
  coefficient, the two actual output suffixes agree, regardless of the
  incoming carries.

Thus in a collision word B H B, the two copies of B can be analyzed using
their actual incoming carries. Independently resetting either copy to
carry zero would omit the correction above and is generally invalid.

## Reproduction

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

The checker rebuilds the dependency and contribution in a fresh temporary
directory, audits all 24 theorem declarations, rejects proof placeholders
and custom axioms, and checks that the sources did not change during the
run. Permitted axioms are only `propext`, `Classical.choice`, and
`Quot.sound`. The report records SHA-256 and Git blob hashes.
