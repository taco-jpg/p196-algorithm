# Exact first-positive-palindrome-time contract and semantic review

Agent: 11. Branch: `formalize/agent-11/s20261015-coverage`.
Original source snapshot: `74df59c5ecb6cb30fb3c88b1d5b26fdb9526d6c4`.
Source: `proofs/contributions/2026-10-15-seam-persistence-obstruction/SEAM_PERSISTENCE_OBSTRUCTION.md`, first section, equations (1)-(3).
Successful coordination claim: `cee375e58389895f02c272568523ea4bfc2a4785`, a non-force update based on `9a60461035f3cce2035857b6c7e3a755aa213830`.

## Original mathematical claim

For each integer base b>=3, let h=floor((b-1)/2). For every positive canonical base-b numeral whose full reflected pair coefficients q satisfy b-1<=q_i<=b+h-1 and q_0>=b, the first positive palindrome time is exactly one when every q_i=b+1, and exactly two otherwise. There is no restriction on whether the original numeral at time zero is already a palindrome.

This is one original timing claim, not one major claim per generated supporting declaration. The first-output classification is also proved under the larger upper bound 2*b-2; this is accurately labeled a stronger supporting result, not a newly discovered source theorem.

## Lean proposition and interfaces

`Agent11HighBase.numeric_interval_first_hit` quantifies over all b>=3 and every `List Int` satisfying the existing `ReverseAdd.DigitBounds b digits` and `PhysicalWidth.PositiveLast digits`. Its interval hypothesis is applied to the actual `ReverseAdd.pairs digits`, not an unrelated abstract transition state.

`digitOrbit` is iteration of `ordinaryStep`, including after a palindrome. `FirstPositivePalindrome` is the standard positive hitting-time predicate: the stated positive time is palindromic and every smaller positive time is not. Neither definition encodes the requested time as true by construction. `first_positive_unique` proves uniqueness separately.

The final theorem supplies both iff statements and the disjunction that time one or time two occurs. In the same conclusion, for every time t the actual computed output is a canonical positive numeral and its value satisfies the ordinary reverse-add recurrence. `digit_orbit_canonical` and `digit_orbit_value` establish that correspondence for arbitrary canonical inputs, independently of the special interval hypothesis.

## Hypotheses, quantifiers and boundaries

All finite positive widths are included, with no enumeration cutoff. Base three, odd bases, and width one are included. The even central pair coefficient in odd widths follows from the actual reflected digit sums; an impossible symbolic word is not supplied as a numeric witness. The upper bound uses integer division by two, whose exact floor inequalities are proved in `half_base_bounds`. Input leading zeros are excluded by `PositiveLast`; value evaluation of the reversed finite digit list has the ordinary discarded-leading-zero meaning. The actual normalization retains an overflow digit and removes an absent zero terminal slot.

Time zero is deliberately not a candidate. The algorithm continues after a palindrome, as the source stipulates. No initial or first-step nonpalindromicity is smuggled in as a hypothesis. No infinite safe orbit, invariant high region, 196 conclusion or Lychrel witness follows.

## Proof and dependency correspondence

The strong supporting `first_palindrome_iff_constant` uses the already proved actual high carry normalization and the existing all-base palindrome-predecessor classification. Its converse exhibits the exact output with endpoints 1 and internal digits 2. The interval bounds imply every adjacent sum is at most 3*b-3, so the independently stated `second_palindrome_iff_adjacent` theorem supplies a palindromic second output. The first-output iff distinguishes whether this is the first positive hit.

Dependencies remain the same six pinned Std-only base modules plus Agent 11's four preceding modules. No Mathlib or toolchain migration is introduced. Original written mathematical provenance remains with the cited source; Agent 11 supplies the Lean formalization and direct semantic checking.

## Verification procedure and level

The new source was compiled locally, then the entire eleven-module source chain was rebuilt twice in distinct fresh directories. Each successful build audits all 122 theorem declarations and 32 definitions, including the 82 unchanged prerequisite theorems. Agent 11 contributes 40 theorem declarations and eight definitions in this five-module checkpoint; these numbers are audit metadata, not independent mathematical-claim counts.

Run `python3 check.py /absolute/path/to/lean-4.19.0/bin/lean --out /new/audit/directory`. The script rejects unlisted root proof modules, missing or mismatched audit names, failed compilation, changed source hashes, forbidden proof shortcuts and unapproved transitive axioms. Only `propext`, `Classical.choice` and `Quot.sound` are allowed. Every new control uses kernel reduction or ordinary proof terms.

`HighBaseFirstHit.lean` SHA-256: `5116f8b17c507134b3d9ac620bbb93f64921edf378b6e0ae99ae3243e6a8ca13`.

Local build logs, axiom output and failed development attempts are retained for publication. CI must be tied to a commit whose checker actually lists the fifth module; the earlier four-module CI is not evidence for this new endpoint. Separate clean builds and CI are not represented as independent semantic review. Independent review and integration remain explicit subsequent gates.
