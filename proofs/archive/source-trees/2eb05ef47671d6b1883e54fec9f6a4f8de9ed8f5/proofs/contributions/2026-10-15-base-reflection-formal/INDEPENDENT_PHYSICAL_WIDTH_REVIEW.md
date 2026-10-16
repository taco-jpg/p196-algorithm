# Independent review of canonical physical width

**PASS** for the frozen 21-theorem `PhysicalWidth.lean` source, SHA-256
`d44882a91123b114b39c2c64dd08f4dca37482210d22f937c4a8aca7867578de`.
The package's fresh producer audit now covers 61 declarations: nine signed
uniqueness prerequisites, 15 reflection theorems, 16 reset-normalization
theorems, and these 21 physical-width theorems. The earlier independent
reviews remain scoped to their respective source checkpoints. This is a
full mathematical/source review, not a claim of an additional compilation.

The terminal carry used to choose the output width is computed from the
continuous, no-reset carry chain. It is not the isolated terminal carry of
the final partition block. `terminal_le_ordinary` proves the latter is no
larger than the former, and both are binary under the coefficient bounds.
Thus when actual normalization does not overflow, the isolated terminal
slot is also zero and may be removed. When actual normalization overflows,
the complete raw placed list is kept at length `L+1`, even if its isolated
terminal coefficient happens to be zero. This is the required common
reflection width.

`atActualWidth` and `actualDigits` select their branch consistently. The
proved idempotence of `ordinaryTags` ensures that removing reset flags
again does not change the terminal bit or the branch. In the no-overflow
branch, both padded lists are explicitly written as their bodies followed
by zero; cancellation of that final slot is justified. In the overflow
branch, the full-list symmetry equivalence from the earlier modules applies.

The reverse implication is substantive: symmetry of ordinary normalization
is applied to the no-reset coefficient stream, giving the low or `{0,b+1}`
classification. Those languages have reset-independent placed output,
yielding symmetry of the arbitrary reset baseline. This argument does not
assume the raw symmetry it is proving.

The normalization result proves canonical digits, rather than merely giving
a length to a padded list. Every continuous-chain body digit lies in
`[0,b-1]`, the terminal carry is zero or one, the exact value is preserved,
and the length is `L + actual_terminal`. `PositiveTerminal` explicitly
excludes an empty list and requires a positive highest input coefficient.
Without overflow, the last coefficient plus nonnegative incoming carry is
positive and smaller than the base, making the highest output digit positive.
With overflow, the highest output digit is one. Consequently the selected
width is the actual positive integer digit width. Symmetry is unnecessary
for these normalization facts; when additionally assumed on the input,
positivity also holds at its other endpoint.

The final `canonical_raw_symmetry` theorem therefore supplies, for every
integer base `b>=3` and every reset pattern on a symmetric coefficient word
bounded by `0..2b-2` with positive terminal coefficient:

- valid nonnegative base-`b` normalized digits with positive leading digit;
- exact numerical value and actual width;
- raw symmetry at that common width if and only if normalized-digit symmetry;
- equality of the raw and normalized lists whenever they are symmetric.

The raw list itself need not initially be a digit list. Its membership in
that digit range follows in the symmetric case from the proved equality,
not from a hidden assumption about overlapping placed terminal carries.

This closes the physical-width and converse-normalization obligations left
open in the preceding independent reset review. The domain is a finite
integer coefficient list; odd-center parity needed to realize a particular
pair word by an ordinary seed is not assumed and is not needed for this
stronger normalization theorem. There is still no separately formalized
nested-block-list decomposition, no direct imported reverse-and-add orbit
bridge, and no all-time persistence theorem in this package.
