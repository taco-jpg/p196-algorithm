# Overflow local births: accepted theorem summary

The accepted module is `../../OverflowBirths.lean`, namespace
`RunBirths.Overflow`. It imports the unchanged `LychrelDigitSums` base and
uses its actual recursive carries, `FoldedDecimal.Admissible`, and
`FoldedDecimal.nextColumns` throughout the semantic theorems.

Let `0 < i < L`, suppose the actual final carry is 1, and abbreviate

- `x = q(i-1)`, `y = q(i)`;
- `b = carry q i`, `d = carry q (L-i)`.

The actual interior output is

`G_i = (y+b) mod 10 + (x+d) mod 10`.

The two inner carries are constrained by the adjacent coefficients:
`b = (x+a)/10` and `d = (y+e)/10`, where
`a = carry q (i-1)` and `e = carry q (L-i-1)`.
All four carries are actual computed bits. Symmetry of the admissible
word is used to obtain the second equation. Dropping these equations
would incorrectly admit additional patterns.

## Exact classification

| Output | `(x,y)` | `(b,d)` | Origin |
| --- | --- | --- | --- |
| 0 | `(0,0)` | `(0,0)` | Old equal zero pair |
| 0 | `(9,9)` | `(1,1)` | New zero |
| 0 | `(9,10)` | `(0,1)` | New zero |
| 0 | `(10,9)` | `(1,0)` | New zero |
| 18 | `(18,18)` | `(1,1)` | Old equal eighteen pair |
| 18 | `(9,9)` | `(0,0)` | New eighteen |
| 18 | `(9,8)` | `(1,0)` | New eighteen |
| 18 | `(8,9)` | `(0,1)` | New eighteen |

For each mixed pair, the Lean theorem states only the non-forced carry
condition; the other carry is forced by its adjacent input coefficient.
For the homogeneous 0 and 18 pairs both carry values are forced, so the
Lean statement does not redundantly repeat them.

The proof first characterizes a normalized digit equal to 0 or 9. A sum
of two decimal digits is zero exactly when both are zero, and is eighteen
exactly when both are nine. Combining those digit conditions with the two
actual adjacent carry equations leaves precisely the table above.

The direct birth theorems use the precise predicate
`G_i = c ∧ ¬(x = c ∧ y = c)`. They establish that every overflow birth
of 0 or 18 touches an old 9. Consequently, when both old adjacent entries
are different from 9, output 0 is equivalent to an old 00 pair and output
18 is equivalent to an old 18,18 pair. These are local statements; no
infinite regeneration or ancestry claim is made.

## Actual endpoints

After overflow the output width is `L+1`. Both endpoint coefficients are
exactly `1 + q(0) mod 10`, hence lie between 1 and 10. Neither endpoint can
be 0 or 18. This includes `L=1`, for which there are no interior positions.

## Verification and retained development

Lean 4.19.0 accepted all 11 exported theorems, with the output recorded in
`FullAttempt02.log`. Every exported theorem has a `#print axioms` command.
Only `propext`, `Classical.choice`, and `Quot.sound` appear; the accepted
module contains no `sorry`, `admit`, `native_decide`, or custom axiom.

`LocalAttempt01` through `LocalAttempt03` retain failed direct `omega`
attempts. Their failure was tactic incompleteness for a large modular
case split, not a counterexample to the statements. `LocalAttempt04`
successfully separates the one-digit residue lemmas before applying
linear carry arithmetic. `FullAttempt01` is the first accepted complete
semantic module; `FullAttempt02.log` verifies the final extension with
the direct birth and adjacent-nine consequences.
