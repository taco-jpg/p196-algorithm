# Arbitrary-integer representation contract — Agent #4

The preceding two modules passed both clean builds and all 34 exported-declaration audits at commit 9babaabff6df2d817740bca7991a72d34cb58f13, run 38940749519, job 117107454555. This next module closes the remaining arbitrary-input representation obligation. It is SOURCE_PRESENT until the new run succeeds.

## Exact theorem

For every even base b>=4 and every positive natural a, there exist one positive width n and one positive natural z such that both a and z have canonical independently extracted base-b digits of width n; every mirrored digit-pair sum of z is exactly the source's prescribed carry normalization of a; and the complete schoolbook first carry word is identical at every boundary 0<=k<=n.

`normalized_integer_representative` is the target. Unlike the trivial witness z=a, it retains the exact normalized-pair-sum prescription. It formalizes the NORMALIZATION AND REALIZATION source section, not the stronger four-step palindrome theorem.

## Definitions and provenance

`integerDigit` extracts a natural's digits by repeated quotient and remainder, independent of the supplied word representation. `integerDigit_value` proves recovery; strong induction proves every positive natural has a finite canonical representation. `CanonicalNumeral` requires positive width, bounded extracted digits, a nonzero leading digit, and exact evaluated value. `canonical_numeral_bounds` gives the actual base-power interval. `reverseAtWidth` reverses these extracted digits with the now-verified physical width; leading zeroes in the reversed numeral contribute zero. `numeric_reverse_add_arithmetic` ties the carry algorithm to addition of the natural and that reverse.

Source: original normalization report at 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, blob 57716e4f6c25d19d96b8c502237b523b25b5fb52. Branch and serialized ownership remain those in CONTRACT.md. No original theorem is weakened or declared complete by these auxiliary definitions.

## Remaining after this module

Even if the integer normalization endpoint passes, reaching a palindrome within four additions and optimality of that bound remain unformalized by this contribution. Next candidates: exact non-overflow two-step theorem; protected neutral-run update; overflowing normalization membership; two overflow transitions; full numeric composition; all-base sharpness. These are candidates, not exclusive reservations.
