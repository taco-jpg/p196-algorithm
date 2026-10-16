# Independent review of the exact adjacent-sum formalization

PASS for the complete Lean source, mathematical argument, documentation,
fresh-build checker, and saved 13-theorem axiom report. This review did not
repeat the dependency compilation. The reviewed source SHA-256 is
`6a7bca1a9cc0b245e7cef118b447626ccdf91623062a10065abfffac7fb743f8`.

The initial coefficient between ten and eighteen produces carry one.
Every later coefficient between nine and eighteen preserves that carry,
because its total is between ten and nineteen. Thus the physical next width
is exactly `L+1`, not the original width. Both endpoint formulas explicitly
pair the original units output `q 0 - 10` with the terminal overflow digit
one, giving `q 0 - 9` in the range one through nine.

At an internal position `0 < i < L`, reflection in the normalized width
uses the index `L-i`. This is strictly between zero and `L`; the original
symmetry identifies its coefficient with `q (i-1)`. The source explicitly
proves the identity `L-1-(i-1)=L-i` under those bounds. Each of the two
subtracted coefficients is at least nine, so the formula
`q (i-1) + q i - 18` is ordinary subtraction without hidden natural-number
truncation. It follows that the updated word is all at most nine exactly
when every original adjacent sum is at most twenty-seven.

The equivalence handles width one correctly. The internal range is empty,
and the updated word has two equal endpoint coefficients `q 0 - 9`, both
at most nine. No internal formula is applied at an endpoint or outside its
proved range.

For the actual numerical conclusion, the existing representation theorem
supplies the canonical first iterate at its actual changed width. Its low
outer coefficient excludes the overflow-palindrome class with outside
eleven, leaving precisely the all-small class. Thus the theorem is an
if-and-only-if statement about `orbit n 2`; it does not infer that either
the original seed or the first output was nonpalindromic. The large-adjacent
corollary uses the complementary integer threshold twenty-eight correctly.

The ordinary controls exercise equality at twenty-seven, failure at
twenty-eight, and the width-one case. The report matches all thirteen public
declarations, the frozen base source, and the current module; only standard
logical axioms occur, and both numerical control theorems are axiom-free.
The fresh checker differs from the already reviewed high-column checker
only in module names, temporary-directory prefix, and scope text.

This package formalizes the exact decimal reduction. It does not claim
the all-base theorem, a first-hit theorem, preservation of the high-carry
region, or an infinite safe orbit.
