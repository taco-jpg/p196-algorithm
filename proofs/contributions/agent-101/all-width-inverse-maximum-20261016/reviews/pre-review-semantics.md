# Independent semantic pre-review: profile extraction and maximum witnesses

## Status and independence

**Semantic pre-review PASS; independent runtime verification pending.** No mathematical defect was found in the two frozen sources below. This reviewer authored none of the new all-width maximum modules. The older `Agent101SplitEnumeration` dependency was written by this reviewer in the preceding digit-split task; that prior authorship is disclosed here and is not presented as independent review of that dependency.

No Lean invocation or Git write was performed. The actual source bytes and accepted author receipts were read; the source snapshots are retained beside this report. The recorded author runs explicitly used `--trust=0` and exited zero, but they are author evidence, not this reviewer's independent rebuild.

| Reviewed source | SHA256 | Public declarations |
| --- | --- | ---: |
| `proofs/Agent101ProfileExtraction.lean` | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` | 7 theorems |
| `proofs/Agent101MaximumWitnesses.lean` | `d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7` | 5 definitions and 15 theorems |

The local HEAD observed during this review was `71691d50497edc83247b3571af276bb0ee438491`. The new local sources must not be attributed to that HEAD merely because it is the current checkout. The reported ProfileExtraction publication prefix is `9bf1b2c`; this pre-review has not independently read that commit back. Exact readback of the final published source commit and registry, followed by the single complete fresh build, remains a separate pending stage.

The exact source/dependency hashes, export names, author receipt paths, and review classifications are in [pre-review-source-registry.json](pre-review-source-registry.json). The snapshots are [pre-review-Agent101ProfileExtraction.lean.txt](pre-review-Agent101ProfileExtraction.lean.txt) and [pre-review-Agent101MaximumWitnesses.lean.txt](pre-review-Agent101MaximumWitnesses.lean.txt).

## Profile extraction is an actual finite decomposition

`Agent101.exists_coefficientWord_of_reverse` assumes precisely a finite list `q : List Nat` and its full list equality `q.reverse = q`. Its conclusion is an actual list decomposition `q = coefficientWord h c`, where the existing definition is `h ++ c.toList ++ h.reverse`.

The proof uses strong induction on the actual list length. For a list of length at least two, `exists_wrapDigits` produces its first element, last element, and the finite list between them. Reversing this wrapped list and applying `wrapDigits_injective` gives both equality of the exterior coefficients and the reverse symmetry of the actual interior list. The interior has length two less than the original, so the induction call strictly decreases its natural-number measure. Reattaching the same exterior coefficient gives the claimed decomposition.

Both short-list bases are included. An empty list uses `h=[]`, `c=none`. A singleton `[a]` uses `h=[]`, `c=some a`. Neither the proof nor the theorem adds positivity, digit boundedness, or a realizability condition to arbitrary `q`. Such assumptions would be inappropriate for this finite reconstruction statement.

`coefficientWord_half_length` uses the exact optional-center length, which is zero or one. It therefore obtains `h.length = full.length / 2` for both parities. The division is natural-number division, and the two possible center lengths discharge its parity cases.

`digitPairSums_reverse` establishes the reverse symmetry needed for every actual finite digit-pair-sum list. The two lists zipped together have equal length, and reversing the zip interchanges the summands. Commutativity of addition proves equality at each valid list position. No element is lost through unequal zip lengths.

`digitPairSums_profile` then retains three pieces of actual finite information: the complete pair-sum list equality, the exact half length, and equality of the reconstructed full width with the original digit-list length. Its numerical consequences are supplied later by the preexisting `NumericFibers` interfaces; this theorem itself is a finite-list and length statement.

For `digitPairSums_profile_cons`, the premise `2 <= ds.length` forces the half to be nonempty. The returned tail half has length `ds.length / 2 - 1`, and the exterior coefficient equals the original decimal `columnSum` at index zero. The premise supplies the valid index required by `digitFn_digitPairSums`. In particular, the proof does not choose an unrelated exterior value or silently assume an empty optional center.

## Finite columns and the infinite digit-function tail

The new reconstruction statements compare `List Nat` values, not unrestricted functions `Nat -> Nat`. The older `digitFn` extends a finite list by zero, but the original `columnSum d L i` uses a reflected index involving natural subtraction. At an index outside the represented width, that reflected term can differ from the zero extension of the finite pair-sum list. A function equality at all indices would therefore require an additional justification and is not asserted here.

The relevant existing bridge is explicitly restricted:

```text
digitFn_digitPairSums ds i (hi : i < ds.length)
```

ProfileExtraction applies it only at zero under the length-at-least-two hypothesis. The existing `same_width_step_eq_iff_digitPairSums` also reconstructs a finite list equality from equal columns only at valid positions. The Agent #105 dependency's `canonical_digits_unique` similarly concludes equality only for `i < L`. MaximumWitnesses uses the units digit at a positive target width. None of these uses requires or obtains control of an arbitrary infinite tail.

## The maximizing profile has the stated actual width

`maximumHalf D` contains `D/2` copies of nine. `maximumCenter D` is `none` for even `D` and `some 0` for odd `D`. Consequently `length_maximumWord` proves the exact full length `D` for every natural `D`.

When `D >= 2`, the half has at least one element, and `maximumHalf_cons` exposes a leading half coefficient nine. The complete mirrored word then has first and last coefficients nine. Its coefficients are ordinary digits bounded by nine, and its last digit is positive. `maximumWord_canonical` therefore provides an actual canonical decimal list. `maximumTarget_width` uses the existing canonical-width theorem to establish the numerical interval predicate `decimalWidth (maximumTarget D) D`.

The count uses the original digit-split formula with its exterior correction. An outer pair summing to nine has nine allowed ordered splits because the high digit must be positive; each inner pair summing to nine has ten splits. Both possible centers have count one. Thus `length_maximumPreimages`, under `D >= 2`, is exactly:

```text
9 * 10^(D/2 - 1)
```

The list inherits `Nodup` from the original complete numeric fiber. Its nonemptiness is proved from the positive exact length before it is used to exclude other input widths. The attainment argument therefore cannot rely on an empty witness family.

## Attainment includes every positive input width

`mem_maximumPreimages_fixed` is the complete fixed-width interface, stated for every natural `D` and `n`. The stronger `mem_maximumPreimages`, under `D >= 2`, removes the width condition from the right side:

```text
n in maximumPreimages D <-> 0 < n and step n = maximumTarget D
```

The universal quantifier is genuinely over every `n : Nat`. The reverse implication starts with an arbitrary positive predecessor of the target. It obtains that number's actual canonical width `L` from `canonical_exists`. Independently, positive exact fiber length supplies a member `a` of the displayed list with actual width `D`.

If `L` and `D` differ, the proof invokes the unchanged Agent #105 `cross_width_target_digits` theorem on these two actual canonical inputs. The argument handles both possible width orderings and supplies the canonical digit function of their common numerical output. The theorem forces the target's units digit to be one. The explicitly constructed target has units digit nine, a contradiction. Thus the arbitrary predecessor has width `D` and belongs to the original fixed-width fiber.

This uses a published cross-width restriction without reproducing a numerical-target decoder. The consulted unchanged dependency hashes are:

| Dependency | SHA256 |
| --- | --- |
| `proofs/Agent105WidthSupport9df76b.lean` | `3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7` |
| `proofs/Agent105CrossWidth9df76b.lean` | `a8fe89a91d79809bb3452a39775eb0cc9a06241d37e37c7ef916bf20f265d7a2` |

`all_width_maximum_witness` therefore supplies a target of the specified output width, a duplicate-free list, a membership equivalence with **all** positive ordinary predecessors, and the claimed exact length. The module supplies attainment; the universal upper bound for arbitrary targets belongs to the separate bounds/global modules.

## Boundary checks

| Boundary | Semantic result |
| --- | --- |
| `D=2` | Half `[9]`, no center, target `99`, and nine positive two-digit predecessors. The formula exponent is zero. The permitted splits include the trailing-zero predecessor `90`; only a zero high digit is excluded. |
| Odd `D >= 3` | The center `some 0` contributes one actual interior digit and one realization. The outer nines ensure positivity and full width; this zero is never the only leading digit. |
| `D=1` | The general attaining-width theorem is not applied. `one_digit_preimages` proves the exact positive fiber of target `2` is `[1]`, and `one_digit_maximum_witness` gives its width, no-duplicates, and cardinality one. |
| `D=0` | General list definitions and the fixed-width equivalence remain well formed, but no positive-width attainment theorem is claimed. |

The `D=1` completeness proof uses `n <= step n` to obtain `n <= 2` for an arbitrary positive predecessor of two. It handles `n=1` directly and excludes `n=2` using its actual step value four. Thus the separate witness also ranges across all positive input widths; it does not merely check a single-digit enumeration. The small boundary readings above are deductions from the displayed definitions and proofs, not additional executed Lean tests.

## Next verification stage

The corrected `Agent101WidthFiberBounds` and the complete `Agent101AllWidthMaximum` were still being developed when this pre-review was recorded. They are not covered by this PASS. After the parent supplies a frozen full-source commit and registry, the remaining work is to read those exact sources, verify their published bytes independently, review the global two-width argument, and perform the single fresh complete canonical build plus the required module-origin and public-declaration audits. No current untracked-file status or author incremental result is being substituted for that final stage.
