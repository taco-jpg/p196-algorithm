# Exact adjacent-sum criterion in the high-carry range

`HighCarryReduction.lean` proves an exact criterion for the **actual second
reverse-and-add output** of a canonical decimal integer. Let its symmetric
pair coefficients be (q_0,\ldots,q_{L-1}), with every coefficient between
9 and 18 and (q_0\ge10). Then

\[
 \operatorname{Palindrome}(\operatorname{orbit}(n,2))
 \quad\Longleftrightarrow\quad
 q_{i-1}+q_i\le27\quad(1\le i<L).
\]

This extends the sufficient 9-through-13 coefficient bound in the sibling
`2026-10-15-high-column-formal` contribution. It formalizes the decimal
adjacent-sum reduction developed in
`../2026-10-15-seam-persistence-obstruction/SEAM_PERSISTENCE_OBSTRUCTION.md`.

## Why the reduction is exact

The first addition has carry 1 after every column. Its digits, in increasing
place order, are

\[
 q_0-10,\ q_1-9,\ldots,q_{L-1}-9,\ 1.
\]

Its physical width is therefore exactly (L+1). Set (r_i=q_i-9). Symmetry
of the original pair coefficients makes the next actual pair word

\[
 (r_0,\ r_0+r_1,\ldots,r_{L-2}+r_{L-1},\ r_0).
\]

The two outer coefficients are at most 9. Consequently the special
overflow-palindrome class with outer coefficient 11 cannot occur at this
next step. The original exact palindrome classification leaves precisely
the all-coefficients-at-most-9 condition, equivalent to the adjacent-sum
bound above. At (L=1), the next pair word is ((r_0,r_0)), and the
adjacency condition is correctly vacuous.

## Formal statements and checks

The module contains 13 public theorems. The main theorem is
`numeric_second_palindrome_iff_adjacent`; the corollary
`numeric_large_adjacent_safe_second` proves that an adjacent sum at least
28 forces a nonpalindromic second output. The intermediate theorems give
the actual carries, output digits, width, and all next pair coefficients.

Kernel-checked controls include:

| Seed | First output | Second output | Relevant boundary |
| --- | --- | --- | --- |
| 974 | 1453 | 4994, palindrome | Pair word ((13,14,13)), adjacent sums 27 |
| 77 | 154 | 605, nonpalindrome | Pair word ((14,14)), adjacent sum 28 |
| 9 | 18 | 99, palindrome | Width one, no adjacent inequality |

Run the independent fresh build with Lean 4.19.0:

```sh
python3 check.py /path/to/lean
```

The checker rebuilds the original `LychrelDigitSums.lean` and this module
in a new temporary directory, checks every public theorem's transitive
axioms, rejects unproved declarations and native decision shortcuts, and
records exact source hashes in `verification.json`. `compile.log` records
the build and axiom audit. No existing binary proof objects are used.

The result concerns the output at time 2. It does not assert that the
initial integer or the first output is nonpalindromic, and thus makes no
general first-hit claim. This module does not formalize the all-base
version, polynomial seam identities, or an infinite safe orbit.
