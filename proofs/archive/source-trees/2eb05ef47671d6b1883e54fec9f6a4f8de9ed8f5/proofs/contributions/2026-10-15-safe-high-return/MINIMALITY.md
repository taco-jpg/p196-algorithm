# Minimum seed for three safe high-region returns

Agent #1. Evidence label: complete finite certificate, checked by two
implementations. The minimum claim is not presently Lean-certified.

## Exact scope and result

Among positive ordinary decimal integers `n` satisfying all of

- `Q(n), Q(T^2(n)), Q(T^4(n)), Q(T^6(n))` belong to H;
- every output `T(n),...,T^6(n)` is nonpalindromic,

the smallest is **809999999**. It is itself nonpalindromic, so the minimum
is unchanged when safety at time zero is additionally required.

This does not claim minimum among all six-step survivors, all delayed
palindromes, all possible return regions, or Lychrel numbers.

## Exhaustion and why it covers integers

For a canonical pair word of width L, symmetry determines its second half.
In H the exterior belongs to `10..18`, the other paired positions belong
to `9..18`, and an odd-width center must be even, hence one of
`10,12,14,16,18`. Every such word is realizable by ordinary digits: split a
paired coefficient q into most-significant digit max(0,q-9) and opposite
digit q-max(0,q-9); halve the center. The exterior is positive.

The exact counts for widths 1 through 9 are

`5, 9, 45, 90, 450, 900, 4500, 9000, 45000`,

summing to **59,999**. No prefix-rank pruning is used. The programs test
actual normalization, not edges of an overapproximating graph. Exactly one
word succeeds:

`(17,9,18,18,18,18,18,9,17)`.

The first positive integer output depends only on the pair word, because
it is its value at ten. Thus checking one realization covers every
realization's positive-time behavior. Greedily minimizing digits from the
most significant side gives the minimum realization 809999999. Integers
with ten or more digits exceed this number. The finite exhaustion therefore
establishes the global minimum under the stated initial-H hypotheses, not
merely a minimum within an arbitrarily selected seed sample.

## Complete evidence and independent replay

`enumerate_minimal.py` enumerates by width, tail coefficients, exterior,
and center. It uses the carry-based map from `verify_witness.py` and emits
both the count report and the full signed one-byte outcome vector.

`minimality_outcomes.json` preserves all **59,999** outcomes losslessly as
zlib-compressed base64. Code zero means success; -t means the first observed
palindrome occurs at t; +t means the first even-time failure of H occurs at
t. The row-order description and generator reconstruct every corresponding
word. No rows are omitted. Decoded vector SHA-256:

`545b14904d5f783c87fa5c43bc566a3e463e13f5830c3217db29747d3eb46744`.

`independent_minimality.py` does not import the producer or its carry map.
It enumerates half-words in a different numeric order, constructs literal
minimum decimal realizations, runs ordinary integer/string reverse-and-add,
and compares each result at its independently calculated vector address.
It asserts that every address is visited exactly once and that the sole
successful word and minimum seed match. Both programs passed locally.
This is implementation independence, not an independent human review.

Reproduce from this directory:

```
python3 enumerate_minimal.py
python3 independent_minimality.py
```

The supplied scripts reject mismatches rather than silently rewriting
previously stored reports. The all-width family theorem is separately
kernel checked and does not depend on this finite search.
