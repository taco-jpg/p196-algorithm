# Exact detection scope of interval carry mismatch

`OverflowMismatchReduction.lean` proves that, for a finite coefficient word
with every coefficient at most 18, the following are equivalent:

1. Two nonempty intervals with positive terminal coefficients have unequal
   final carries when independently normalized from carry zero.
2. The word contains both a coefficient in 1 through 9 and a coefficient
   at least 10.
3. Two singleton intervals already give such a carry mismatch.

The main declarations are `interval_mismatch_iff_mixed` and
`interval_mismatch_iff_singletons`. The finite word need not be symmetric,
canonical, nonempty, or positive at its outside position for these
equivalences. Coefficients outside the stated width are irrelevant.

## Proof and implications

Under the coefficient bound, every isolated final carry is 0 or 1. Of two
unequal carries, one must therefore be zero. Its positive terminal
coefficient is at most 9. The interval with positive carry must contain a
coefficient at least 10: an interval consisting only of coefficients at
most 9 has carry zero throughout. Conversely, singleton intervals at the
two identified coefficients have unequal final carries.

Thus allowing longer positive-terminal intervals does not increase the
set of words detected by this existential certificate. Longer intervals
remain useful when an argument already tracks named blocks and their
overflow bits. This result clarifies that distinction rather than claiming
a stronger detector.

The module builds on the frozen sibling
`2026-10-14-overflow-mismatch-formal/OverflowMismatch.lean`.
`numeric_mixed_safe` transfers the certificate to an actual canonical
decimal integer, and `numeric_orbit_mixed_safe` applies it at any actual
orbit time using the current physical width.

This sufficient safety test is incomplete. The kernel-checked control
`detection_is_incomplete` uses the pair word ((14,14)) of 77: no permitted
interval mismatch exists, but its output 154 is nonpalindromic. In
particular, absence of the certificate does not imply a palindrome.

## Verification

There are 12 new public theorems. Run:

```sh
python3 check.py /path/to/lean-4.19.0
```

The checker freshly compiles the original `LychrelDigitSums.lean`, the
15-theorem frozen interval module, and this module in an empty temporary
build directory. It audits all 27 contribution theorems for transitive
axioms, checks source hashes before and after the build, and records the
result in `verification.json` with the full output in `compile.log`.
Only the usual Lean axioms `propext`, `Classical.choice`, and `Quot.sound`
are allowed. No prebuilt proof object is used.

The contribution proves an exact finite certificate reduction and
one-step safety corollaries. It does not assert certificate persistence
or an infinite nonpalindromic orbit.
