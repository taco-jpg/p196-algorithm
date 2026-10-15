# Independent review of the mismatch reduction

**PASS** for all 12 new theorem statements and proofs in
`OverflowMismatchReduction.lean`, SHA-256
`b0f827e2372a736757a04c643b1e8667d9982eb24336780b9e9121751d7b6ba0`.
The README correctly states their domain and detection limits. This is a
source and mathematical review; the producer's separate fresh build audits
all 27 contribution declarations, including the 15-theorem interval
dependency. No additional independent compilation is claimed here.

The equivalence uses the coefficient bound `q_i<=18` exactly where needed:
every isolated final carry is binary, so two unequal final carries include
a zero and a positive one. The positive terminal coefficient of the
zero-carry interval is at most nine by its final column equation. Thus it
supplies a coefficient in `1..9`, not merely a zero coefficient. An interval
with positive final carry contains a coefficient at least ten; otherwise
normalization from zero would have zero carry throughout.

Conversely, singleton intervals at a positive coefficient at most nine and
at a coefficient at least ten have final carries zero and positive,
respectively. This direction does not require the global upper bound, and
the source correctly omits that unnecessary premise. The bounded iff and
the reduction to singleton witnesses then follow without any assumption
about word symmetry, interval symmetry, ordering, disjointness, or an
outside positive coefficient. Empty words are permitted by the statement:
both existential conditions are simply false.

The upper bound in the forward direction is material. Outside the binary
carry range, two positive carries can differ without any small positive
coefficient; the theorem does not assert the equivalence for such words.
Likewise, the positive-terminal condition on intervals is essential to
exclude a zero terminal coefficient as the supposed small positive witness.

`mixed_not_badWord` correctly expresses a sufficient certificate against
the two immediate-palindrome predecessor classes. `numeric_mixed_safe`
uses the canonical integer and pair-word representation interface, while
`numeric_orbit_mixed_safe` uses the pair word and physical width at time
`t` and concludes safety at ordinary time `t+1`. It makes no assertion
that the mixed-coefficient property persists to the next pair word.

The retained incompleteness control is accurate: the pair word of 77 is
`(14,14)`. It has no positive coefficient at most nine, hence no allowed
interval mismatch, but its next output 154 is nonpalindromic. Thus the
absence of an interval certificate is not a palindrome test. Longer
positive-terminal intervals give no additional existential detection power,
although they can still be useful when a structural argument already tracks
particular named blocks. The README preserves this distinction.
