# Agent #101: the unique initial palindrome in protectedSeeds

## Checked theorem

`proofs/Agent101ProtectedPalindrome.lean`, namespace `Agent101.Protected`,
proves the exact equivalence

```lean
(n ∈ protectedSeeds m k ∧ Lychrel196.Palindrome n) ↔
  n = palindromeSeed m k
```

The explicit candidate is defined from finite least-significant-first digits:

```lean
palindromeHalf m k := [7] ++ List.replicate m 7 ++ List.replicate k 9
palindromeDigits m k := palindromeHalf m k ++ (palindromeHalf m k).reverse
palindromeSeed m k := natValue (palindromeDigits m k)
```

The equivalence includes existence as well as uniqueness. Separate exports
`palindromeSeed_mem`, `palindromeSeed_palindrome`, and
`protectedSeeds_palindrome_unique` allow later filtering arguments to use
the result directly. All results hold at `k = 0` as well as positive `k`.
No nonpalindrome-filter count is introduced in this module.

## Proof structure

The module imports the completed protected multiplicity proof and the
generic `Agent101PalindromeFibers` theorem; it does not re-prove the generic
decimal palindrome characterization.

An even coefficient word in Agent #3's family forces every Boolean choice
to be true: a false choice inserts the odd coefficient 5. The sole entirely
even profile has half `[14] ++ replicate m 14 ++ replicate k 18`.
Halving its mirrored coefficients yields exactly the displayed candidate.

The profile has positive exact multiplicity `5 * 5 ^ m`. The generic
half-profile existence theorem therefore supplies both canonical membership
and actual numerical palindromicity. Conversely, the generic palindrome
fiber equivalence forces the same even profile and the same halved digits.
This establishes exactly one initial palindrome in the complete numerical
union, without treating coefficient words as original digit lists.

## Verification

Final source SHA-256:
`1a662e360011f41d156efd9b5d62cc2acb18078486bcea6cab52b03aec18d295`.

The final module was compiled with Lean 4.19.0, release commit
`6caaee842e94`, using `--trust=0 -j1 -DElab.async=false`. The process exited 0.
All 15 declarations have explicit axiom audits, and the final output contains
only `propext`, `Classical.choice`, and `Quot.sound`. No new axiom, `sorryAx`,
`native_decide`, or `Lean.ofReduceBool` occurs in the checked module or audit.

`verification.json` records the source and direct dependency hashes, compiler
hash, command, build paths, audited declarations, and verification scope.
These are author-local proof checks; independent full-closure review is
recorded separately. `palindrome_v04_pass.lean.txt` preserves the first
complete checked source checkpoint.

## Preserved unsuccessful attempts

- Version 1 was started before its freshly compiled generic dependency was
  available and failed at import resolution; its source equals version 2.
- Version 2 exposed a looping simplification that rewrote a Boolean list
  into `replicate` beneath its own length expression.
- Version 3 used a congruence helper unavailable in Std. The accepted version
  uses an explicit head rewrite and `congrArg (List.cons true)` instead.

Their source snapshots and logs are retained as rejected development
evidence. Any `sorryAx` in these unsuccessful logs denotes a rejected proof
placeholder and is absent from the final successful audit.

No compiled objects or runtime copies are retained in this directory.
