# Independent review of the persistence obstruction

**PASS** for the all-base written proof and for independent replay of all
185 preserved controls. The proof/source/catalog hashes are recorded in
`independent_audit.json`. The replay imports no producer code: it computes
ordinary reversal as integer arithmetic, digits by powers of the base, and
actual-minus-isolated carry defects by whole-prefix integer quotients.

The high-coefficient carry induction has no exceptional width. With
`b-1 <= q_i <= 2b-2` and `q_0>=b`, the first carry is one and every later
carry is one. The stated first-output digits follow, including the terminal
one and the width-one case. Symmetry of that output forces its endpoint
coefficient to be `b+1` and then successively forces every coefficient to
equal its predecessor. Conversely, the constant `b+1` word gives a
palindrome. This reasoning does not require the narrower upper bound.

The narrower interval `q_i<=b+floor((b-1)/2)-1` puts every normalized digit,
including the terminal one, at most `floor((b-1)/2)`. Their reflected sums
are at most `b-1`, so the next addition has no carry and is a palindrome.
The first *positive* palindrome time is consequently one for the constant
`b+1` word and two otherwise. The distinction from time zero is necessary:
different seeds realizing the same pair word can have different initial
palindromicity. Canonical odd-center parity is explicit, and the proof is
valid for every realizing seed.

For the larger region, set `r_i=q_i-b+1`. Pairing the output digits at their
actual width gives endpoints `r_0` and internal coefficients
`r_(i-1)+r_i`; this uses original reflection at width `L`, which shifts the
index by one relative to the output reflection at width `L+1`. The claimed
adjacent-sum threshold `q_(i-1)+q_i<=3b-3` is therefore exactly the condition
that all updated coefficients are below the base. If one threshold fails,
a positive internal coefficient is at least `b`, while the positive outside
coefficient is at most `b-1`. These two singleton intervals have isolated
final carries one and zero. The previously proved all-base positive-terminal
interval criterion then excludes a palindrome at the next output. All
premises of that criterion hold: the updated word is an actual canonical
pair word, the intervals are nonempty, and both terminal coefficients are
positive. Thus the condition is an iff, not merely sufficient.

The explicit family `B=(b,b)`, `H=(b-1)^(2m)`, `m>=1`, is canonically
realizable in every base `b>=3`: its total and individual block widths are
even, so there is no odd-center parity restriction. The explicit seed has
digits `(b-1)^(m+2) 0^m 11`, and its leading/trailing digits differ. Its
outside pair coefficients are `b`, so the first output is nonpalindromic.
Both the three-block and singleton partitions have carry defect exactly
one at positions `2..2m+1` and zero elsewhere. The digit-mass deficit is
`2m(b-1)` and the reflected-pair deficit is twice that. The first output has
only digits zero and one; its next pair coefficients are at most two, below
every allowed base. Consequently every isolated interval and every partition
at that next word has zero outgoing carry defect. The shorter family and
its stated even-base limitation for canonical singleton exteriors also
check.

The exact two-step obstruction applies to arbitrarily large seam count and
mass deficit. It refutes persistence based solely on those current
statistics; it does not refute more restrictive invariants or make a claim
about the future orbit of 196. The adjacent-sum formula supplies a precise
additional condition for immediate renewal within the specified region,
without assuming that future words remain in that region.

Reproduce the independent finite replay from this directory:

```sh
python -B independent_audit.py
```
