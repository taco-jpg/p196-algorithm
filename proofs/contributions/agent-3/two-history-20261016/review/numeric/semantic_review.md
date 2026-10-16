# Independent numeric semantic review

**Result: PASS. No blocking semantic finding.**

Reviewer: Agent #3, `family_cardinality` specialist. Review completed on
2026-10-16. The reviewed subjects are `IntegerInterfaces.lean` 和
`HistorySafety.lean`, including their inherited numeric interfaces from
`NormalizedSafety.lean` 和 `FiniteHorizonTheorem.lean`. The reviewer did not
author either primary subject. The reviewer authored `TwoLayerCertificate.lean`
和 `HistoryFamily.lean`; this report does not independently certify those
modules.

## Actual verification level

This was an independent semantic source review, followed by executable SHA-256
identity checks. No Lean compilation, axiom audit, or numeric simulation was
performed as part of this review. A separate runtime specialist owns the
independent clean build. This report makes no execution claim on that
specialist's behalf.

`source_manifest.json` identifies thirteen inspected sources 和 the extent of
each inspection. All available staged source copies matched the corresponding
repository bytes. `capture_source_manifest.py` checks fixed reviewed hashes;
it rejects changed sources rather than silently transferring this review to
another revision. Its execution establishes source identity only.

The two primary source hashes are:

| Module | SHA-256 |
| --- | --- |
| `IntegerInterfaces.lean` | `bc6d2926cd16c43de990ede025b9ba69e50d1e7e2a578044ad65bdf348e8b4fe` |
| `HistorySafety.lean` | `16ea25b00f12eed305519eb8de73b564bae5ff3a5ddd255895d5485bebfd33ff` |

## Canonical realization 和 positivity

`IntegerRealizes n w` means that some digit function `d` satisfies
`DecimalDigits.Canonical n d w.length`, with its mirrored digit sums equal to
the coefficients of `w` at every in-range position. The original `Canonical`
definition includes all four necessary conditions: positive width, decimal
digits bounded by nine, a positive most significant digit, 和 the equality
`value d w.length = n`. Values of `d` outside the declared width are irrelevant.

Consequently, `integer_realizes_positive` correctly derives `0 < n` using the
original `value_positive`. Canonicality permits a zero units digit. There is no
extra assumption on a chosen digit split, no leading-zero padding of the
declared width, 和 no weaker replacement of the original arithmetic predicate.

`digitList_canonical` preserves these conditions for a list: the explicit suffix
`init ++ [last]` with `0 < last` supplies both nonemptiness 和 a positive most
significant digit. `digitColumn_pair` uses the same least-significant-first
orientation as the original `columnSum`, at reflection index `length - 1 - i`.

## The center condition is retained

`Agent8.CanonicalPair` means a nonempty symmetric list, bounded by eighteen,
with a positive outer coefficient. It does not by itself force an unpaired
central coefficient to be even.

`even_canonical_admissible` correctly takes the separate hypothesis
`w.length % 2 = 0`. For an in-range position, the equation
`i = w.length - 1 - i` would force odd width; thus the exact center obligation
in `FoldedDecimal.Admissible` is vacuous at even width. The theorem passes all
five original admissibility conditions to `valid_word_realizable`.

The actual histories have width `2 * (xs.length + k + 7)`, so their existence
theorem supplies this hypothesis. The post-overflow target has odd width
`2 * m + 2 * k + 3`; its center condition is discharged separately in
`SafetyBridge.target_admissible` by its central coefficient eighteen. The
argument never extrapolates even-width realizability to arbitrary odd words.

## Normalization 和 original arithmetic

The original numeric step is `Lychrel196.step n = n + reverse10 n`.
`DecimalDigits.reverse10_value` connects that reversal to fixed-width digit
reflection under the canonical digit conditions. `step_eq_word_value` therefore
states the exact equality between the next integer 和 the weighted value of
its coefficient word, for every canonical realization.

`digitValue_eq_evalL` uses `value_shift` to identify the original positional
value with `Agent109.evalL`. `Agent109.Compat.normalize_eq` proves equality of
the copied normalization operation with the original `Agent8.normalize`.
Together with `Agent109.evalL_norm`, this gives
`digitValue (normalize w e) = digitValue w + e`. This is a weighted-value
identity for arbitrary natural coefficients; it does not assert that every
such normalization produces decimal digits for arbitrary incoming `e`.

The required bounded-digit conclusion is proved separately for canonical
coefficient words with incoming carry zero. The coefficients are at most
eighteen, symmetry plus positive head gives a positive last coefficient,
`canon_normalize` supplies canonical normalized digits, 和 nonemptiness is
explicitly established. `digitList_realizes_pair` then identifies their actual
column word with `Agent8.pair` of the list. Thus
`integer_realizes_next` transports an arbitrary realization through the
original `Agent8.stepWord` without changing arithmetic semantics.

## Exact timeline

Write `q0 = historyWord0 xs k`, `q1 = historyWord1 xs k`,
`q2 = inputWord (completedBits xs) k`, 和
`N3 = digitValue (Agent8.normalize q2 0)`. Assume `0 < k` 和
`IntegerRealizes n q0`.

| Numeric time | Representation or value | Reason it is not a palindrome |
| --- | --- | --- |
| `0` | The arbitrary original realization `n` of `q0` | The outer coefficient is odd, equal to three. |
| `1` | `orbit n 1` realizes `q1` | Its outer coefficient is odd, equal to seven. |
| `2` | `orbit n 2` realizes `q2` | `q1` contains eighteen, so its next numeric step cannot be a palindrome. |
| `3` | `orbit n 3 = N3` | The pair word of the normalized digits is the common target, whose outer coefficient is five. |
| `3 + s`, for `0 <= s <= k` | `orbit N3 s` | `inputWord_normalized_safe` supplies the entire inclusive interval `0` through `k`. |
| `4` | `digitValue (target (xs.length + 6) k)` | This is inside the safe interval because `k >= 1`; the equality is the common-value conclusion. |

The time-two obstruction is deliberately a statement about the **next**
integer from `q1`. A coefficient eighteen does not assert that every current
realization is nonpalindromic. The imported `iter_not_palindrome_of_run` has
the exact conclusion `orbit n (t + 1)`, so its use with `t = 0` is correct.

For later times, `orbit_add n 3 (t - 3)` has the orientation
`orbit n (3 + (t - 3)) = orbit (orbit n 3) (t - 3)`. In the `t >= 3` branch,
`t <= k + 3` gives `t - 3 <= k`, so the transfer includes both endpoints.
There is no omitted time or added unsupported iterate.

The inherited reservoir bound also matches the indices. The target contains
`2 * k - 1` consecutive eighteens. Its safety theorem needs `1 + 2 * s`
eighteens to exclude numeric time `s + 1`. For `s < k`, this required run fits
inside the available run. At the boundary `k = 1`, the single eighteen gives
the one positive safe step required after time three. The separate odd outer
coefficient supplies safety at time three itself.

## Common time four 和 quantifiers

`history_orbit_three` is an exact integer equality for the given `xs` 和 every
canonical realization of `q0`. Its value can depend on `xs`. Applying the
inherited common-next-value theorem produces time four, where the dependence
on the choices disappears except through `xs.length`. The correction length is
exactly six, yielding `target (xs.length + 6) k`.

Although the function is named `digitValue`, its definition is the positional
weighted sum of any `List Nat`. Applying it to the target is therefore valid
when some coefficients are ten, fourteen, or eighteen. The common time-four
integer is the weighted coefficient value; the statement does not require the
target itself to be a bounded decimal digit list.

`history_integer_realization_package` retains the quantifiers over arbitrary
`xs`, positive `k`, 和 arbitrary `n` satisfying `IntegerRealizes n q0`.
`history_positive_integer_exists` instantiates this stronger theorem only after
obtaining an actual canonical realization from the even-width existence
bridge. No conclusion is restricted to a preferred digit split. The result
proves the finite interval `0` through `k + 3`, for a construction depending on
the prescribed horizon. No infinite-horizon seed or count of all individual
decimal realizations is asserted by the reviewed numeric modules.

## Disposition

No source modification is required by this semantic review. The reviewed
arithmetic interfaces, realization hypotheses, center condition, safety
indices, common time-four value, 和 universal realization quantifiers match
the intended finite-history statement. Lean compilation 和 axiom verification
remain separately attributable to the runtime specialist's evidence.
