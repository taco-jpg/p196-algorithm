# Isolated overflow mismatch certifies one safe output

`OverflowMismatch.lean` formalizes and extends the overflow-mismatch part
of the external stream's
[collision safety corollary at commit `4c3970c04f7997db76f82a5806168b2d0790cfb3`](https://github.com/taco-jpg/p196-algorithm/blob/4c3970c04f7997db76f82a5806168b2d0790cfb3/proofs/research/main_existence_attempt/renewal_pass/external_review/COLLISION_SAFETY_COROLLARY.md).
It imports only the existing frozen `LychrelDigitSums.lean` dependency.

The extension allows **any two coefficient intervals** of the whole pair
word. They need not be symmetric, disjoint, equal in length, or members of
a particular partition. Each must be nonempty, lie inside the whole word,
and have a positive terminal coefficient.

## Main statement

Coefficients are indexed from least to most significant. Define

```text
isolatedCarry q start length = carry (fun i => q (start+i)) length.
```

The existing decimal carry recursion starts at zero, so this is the final
carry obtained by independently normalizing that interval. It is not the
carry inherited from the preceding columns of the whole word.

`numeric_palindrome_interval_carries_equal` proves that if the actual
ordinary output `n + reverse10 n` is palindromic, the two isolated final
carries are equal. `numeric_mismatch_safe` gives its contrapositive:

```text
two positive-terminal intervals with unequal isolated final carries
  → n + reverse10 n is nonpalindromic.
```

The numerical theorem requires a canonical decimal representation of `n`
and agreement of `q` with its mirrored digit sums inside the actual width.
Values of `q` outside that width are irrelevant. `numeric_orbit_mismatch_safe`
applies the same criterion at any actual orbit time, using `iterPairs` and
the corresponding changing width. It assumes the two interval certificates
at that time; it does not assert that they persist.

## Proof

The existing exact one-step classification has two palindromic predecessor
classes. In the first, all coefficients are at most nine; every isolated
zero-start normalization therefore ends with carry zero. In the second,
all coefficients are zero or eleven. A positive terminal coefficient must
then be eleven, and `(11+c)/10 = 1` for either incoming carry bit. Thus every
eligible interval ends with carry one.

`badWord_interval_carries_equal` proves this directly from the exact
`BadWord` predicate. It makes no symmetry assumption about the intervals.
`canonical_badWord_of_palindrome` transfers the original ordinary-integer
classification to the supplied whole pair word. The remaining statements
compose these facts and take the contrapositive.

## Checked ordinary examples and the essential hypothesis

All rows below are Lean-checked, including canonical seed representations.
Safety in the first two rows is derived using the new theorem.

| Seed and output | Compared intervals | Isolated carries | Result |
|---|---|---|---|
| `22900 → 23822` | `(2,2)` and `(18)` | `0` and `1` | Nonpalindromic |
| `12966 → 79887` | `(7,8)` and `(18)` | `0` and `1` | Nonpalindromic; the first interval is not symmetric |
| `99022 → 121121` | `(11,11)` and `(0)` | `1` and `0` | Palindromic; the second interval has zero terminal coefficient and is excluded |

The last row preserves the external counterexample. Dropping terminal
positivity would make the safety implication false even for a canonical
whole pair word. Positivity at the starting coefficient is not required by
the new theorem.

This package does not formalize the entire polynomial identity
`G(BHB) = S`, its equivalence with seam closure, or the active-seam criterion.
It proves the stronger arbitrary-interval overflow-mismatch implication.
It supplies no infinite recurrence, Lychrel witness, or proof of the 196
conjecture.

## Reproduction

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

The checker copies and freshly compiles the exact original dependency and
new module, then audits every new public theorem's transitive axioms.
It rejects proof placeholders, additional axioms, and `native_decide`,
permitting only Lean's standard logical axioms. `verification.json` records
the source SHA256 and Git blob hashes, results, and theorem count;
`compile.log` retains the complete compiler and audit output.

Development record: one proof initially used the unavailable `conv_lhs`
tactic and was replaced with an explicit equality calculation. The main
criterion and orbit bridge then compiled. Concrete interval predicates
needed an explicit decidability instance for kernel evaluation; after that
addition all examples compiled without warnings. The saved verification
report is a fresh rebuild of the final sources.
