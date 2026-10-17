# Independent semantic review: actual decimal width support

Reviewer: Agent #105 / session 9df76b / scope105. The reviewer did not author this module. Review target: `proofs/Agent105WidthSupport9df76b.lean`, frozen SHA-256 `3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7`. This is a semantic source review; the independent full-chain Lean replay has its own verification record.

**Result: semantic review passes for all seven declared theorems. No change requested.**

## Representation and dependency boundary

`DecimalDigits.Canonical n d L` asserts positive finite width, decimal bounds for every coordinate below L, a strictly positive leading digit, and equality of the finite positional value with n. Therefore the module genuinely concerns positive ordinary integers. It does not identify arbitrary zero-padded words with canonical decimal widths. No theorem constrains or identifies the unused infinite tail of a digit function.

`Lychrel196.step` is the existing ordinary integer reverse-and-add operation. `canonical_next_no_overflow` and `canonical_next_overflow` already provide its actual canonical digits and widths; these are the semantic bridges used by this module. No replacement transition relation or symbolic recurrence is introduced.

Inspected dependencies: original foundation source SHA-256 `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`, Git blob `c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506`; Agent101NumericFibers at published commit `326645944168ad2b035a1e653b61527d79684156`, source SHA-256 `bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97`, Git blob `164ade8c8b42e9b6e7f67e36f7e1c60086787208`.

## Theorem-by-theorem assessment

| Theorem | Semantic assessment |
| --- | --- |
| `canonical_width_unique` | Both representations are converted by Agent101.canonical_decimalWidth to the actual interval `10^(L-1) ≤ n < 10^L` with positive width. Agent101.decimalWidth_unique applies to the same n; the conclusion is genuine width equality. |
| `canonical_digits_unique` | Original value_injective applies at a common L to two bounded decimal digit functions having the same finite value. The conclusion is correctly restricted to `i < L`; no unsupported function equality is asserted. |
| `canonical_width_and_digits_unique` | Width equality is proved first, after which the fixed-width digit uniqueness theorem applies. The bound for each digit equality remains the actual common width. |
| `canonical_step_width` | Actual terminal carry is 0 or 1 because each input column sum is at most 18. The corresponding original canonical_next theorem gives width L or L+1; uniqueness transfers this to any canonical output representation. Thus `W = L + carry ... L` includes its exact numerical meaning. |
| `step_width_cases` | The paired conclusions retain which actual carry case produces each possible width. This is stronger and more precise than an unlabelled numerical-width disjunction. |
| `canonical_step_exists` | Supplies the original `output` digits in the zero-carry case and `extended` digits in the one-carry case, with finite width `L + finalCarry`. It is an actual ordinary step witness. |
| `cross_width_carries` | A canonical representation of the common output yields `L + c = K + e`. Both terminal carries are natural numbers at most one, and `L < K`. These integer constraints force `K = L+1`, `c = 1`, and `e = 0`. No palindrome hypothesis or restriction to a particular target is used. |

## Boundary checks and scope

Width zero and integer zero are excluded by the Canonical hypotheses. Positive one-digit inputs remain covered by the general width statements. Trailing zero digits in the ordinary integer input are allowed; the actual reverse10 bridge handles their disappearance on reversal. Output width equality is applied only after both outputs are identified as the same integer through the given step equality.

The module makes no claim that different-width collisions must be palindromic, that an output has at most two integer predecessors, or that any orbit avoids palindromes indefinitely. It supplies width and carry constraints used by the separate at-most-two-profile theorem. Source and statement inspection found no circular use of that later theorem and no additional mathematical axiom. The final module-origin audit remains the authoritative exhaustive axiom check.
