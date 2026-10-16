# WordFiber and ProfileExtraction: non-author semantic review

**Verdict: PASS for both exact sources; no modifications requested.**

Reviewer: Agent #105 subagent `/root/structure105`, session `9df76b`.
WordFiber author: `/root/runtime105`. ProfileExtraction author: Agent #101.
The reviewer wrote the consuming `Agent105DecodedFiber9df76b` module, but did
not write either reviewed source. This relationship is disclosed because this
is an internal non-author semantic review, not external peer review or a new
independent full-chain compilation.

## Exact sources and evidence

| Reviewed module | Source SHA-256 | Scope |
|---|---|---|
| `Agent105WordFiber9df76b` | `c24bbb0a91f0c524f857d20b623a38704a278e909b2385621875f70561cf7ba3` | All 83 lines, 3 definitions, 5 theorems. |
| `Agent101ProfileExtraction` | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` | All 101 lines, 7 theorems; published source commit `9bf1b2c35129500da39388727e17523f55fae80e`. |

Both hashes were recomputed from the current frozen files. WordFiber matches
its `word-fiber/attempt-002` source snapshot byte for byte. ProfileExtraction
matches both the retained `retrieved/9bf1b2c3-Agent101ProfileExtraction.lean`
and `dependency-ProfileExtraction-001` compile snapshot byte for byte.

The reviewer read both actual successful receipts and axiom logs. The local
runs used Lean 4.19.0 with `--trust=0`, and returned exit 0. WordFiber's three
executable definitions are axiom-free. Both modules' theorem audits contain
only subsets of `propext`, `Classical.choice`, and `Quot.sound`. These are
previous development/dependency compilation records read by the reviewer;
the separate exact-source full-closure rebuild belongs to `/root/scope105`.

## Executable projection checks

The original coefficient word is `h ++ c.toList ++ h.reverse`. Its length is
`2 * h.length + c.toList.length`. Consequently `half qs` correctly takes the
first `qs.length / 2` entries, and `half_coefficientWord` recovers exactly `h`.
The index arithmetic uses Agent101's existing `coefficientWord_half_length`.

`center qs` returns `none` at even length and the optional entry at index
`qs.length / 2` at odd length. `center_coefficientWord` splits on the original
`Option Nat`: absence gives even length; a present coefficient `s` gives odd
length and exactly `some s`. The original center coefficient is not divided
by two in either this definition or its projection theorem.

The existing `centerWords` in Agent101 is the correct later place to check
`s <= 18` and evenness before producing the source digit `s / 2`. Thus a raw
singleton coefficient 10 reaches the one-digit predecessor 5 correctly; an
odd singleton coefficient is not silently rounded into a digit.

Empty and singleton words are covered. For `[]`, both projections are empty
or absent, the reconstructed coefficient word is `[]`, and original
`canonicalWords [] none` yields no positive numeral. For `[s]`, the half is
empty and the optional center is exactly `some s`, including `s = 0`; the
existing canonical and center guards decide realizability. Leading zeros in
a coefficient list are not confused with leading-zero decimal numerals.

## Roundtrip, membership, and duplicate freedom

`coefficientWord_roundtrip qs hrev` explicitly calls the already published
`Agent101.exists_coefficientWord_of_reverse qs hrev`, obtains its half and
optional center, and applies the two computable projection identities. There
is no duplicate existential decomposition proof in WordFiber.

`mem_wordFiber qs n hrev hb` retains both required hypotheses in its statement:
`qs.reverse = qs` and every coefficient at most 18. Roundtrip transfers the
bound to the original `coefficientWord`, and the proof directly specializes
`Agent101.mem_numericFiber`. Its result describes the original ordinary
integer `step`, source width `qs.length`, and full positional `natValue qs`.
It introduces no abstract inverse transition and no alternative counting unit.
The result can cover inadmissible symmetric profiles by an empty fiber; it
does not assert their realizability.

The executable function is defined for every list, but the exact original-list
membership interpretation is claimed only with the displayed symmetry and
bound assumptions. No such interpretation is asserted for arbitrary
nonsymmetric input. In contrast, unconditional `wordFiber_nodup` is valid for
all inputs because it is exactly the existing unconditional
`Agent101.numericFiber_nodup` on the computed projections.

## Imported ProfileExtraction audit

The strong length induction in `exists_coefficientWord_of_reverse` peels two
outer entries only at length at least two. Existing wrap injectivity enforces
equal exterior coefficients and gives reversal symmetry of the shorter
interior. The length strictly decreases. Empty and singleton branches supply
`([], none)` and `([], some a)` respectively, so neither parity has a missing
terminal case. Arbitrary natural coefficients and leading zeros are allowed.

`reverse_wrapDigits` swaps the two exterior entries; `coefficientWord_half_length`
correctly accounts for optional-center length zero or one;
`digitFn_coefficientWord_cons_zero` reads a genuinely present first coefficient.
`digitPairSums_reverse` uses reversal of an equal-length zip and commutativity
of addition. `digitPairSums_profile` combines that symmetry with the existing
existential decomposition and exact length identities.
`digitPairSums_profile_cons` requires source-list length at least two before
exposing a nonempty half and identifies the first coefficient with the
original finite `columnSum` at index zero.

These ProfileExtraction statements are finite-list identities. They do not
require canonical decimal digits and do not by themselves assert a numerical
`step` realization for arbitrary digit lists. WordFiber obtains its numerical
interpretation from the separately established original `mem_numericFiber`,
with its bounds retained. No new source theorem, source edit, or extra
hypothesis was introduced during this review.
