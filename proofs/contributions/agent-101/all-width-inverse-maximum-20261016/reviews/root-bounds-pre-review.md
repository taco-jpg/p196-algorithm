# Source-only independent pre-review: fixed-width bounds and global maximum

## Result and scope

**Source-only semantic pre-review PASS; exact published-source readback and independent runtime verification remain pending.** No mathematical defect was found in the two frozen modules below. This reviewer authored neither module, nor either of the other two new maximum modules. The reviewer authored the older SplitEnumeration and PalindromeFibers dependencies; that authorship is disclosed and does not constitute an independent review of those older modules.

| Module | Frozen SHA256 | Public theorems |
| --- | --- | ---: |
| `Agent101WidthFiberBounds` | `bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2` | 6 |
| `Agent101AllWidthMaximum` | `9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9` | 8 |

Both local source hashes match the frozen pins and the accepted author receipts. The author used explicit `--trust=0` and recorded exit code zero for `bounds/attempt-003` and `upper/attempt-002`. Those existing receipts and complete logs were read; no new Lean invocation was made during this pre-review. The actual source snapshots, full exported-name inventory, dependency hashes, and author evidence identities are retained in [root-bounds-pre-review.json](root-bounds-pre-review.json) and the adjacent `root-bounds-*.lean.txt` snapshots.

## Arbitrary integer lists are covered by a real numeric fiber

`mem_numericFiber_of_same_width_step` starts with an actual canonical finite digit list `ds`, its actual coefficient profile, and an arbitrary number `n` of the same numerical decimal width with the same ordinary `step` value. `decimalWidth_iff_canonical` supplies a canonical representation of `n`. `canonical_to_list` converts that representation into a finite digit list `xs` with exactly the same width and value. The existing `same_width_step_eq_iff_digitPairSums` then gives equality of the complete finite pair-sum lists. Substitution of the representative's profile yields membership in the original `numericFiber` through its complete digit-level membership theorem.

No numerical-target decoder or executable inverse enumeration is assumed by this argument. The representative's profile is obtained from an already given canonical realization, and numerical equality at the same width supplies all other members' profiles. It is not merely a pointwise existence statement for the representative.

`fixed_width_profile_length_le` applies that membership result to **every** element of an arbitrary `Nodup` list `ns`. The cover is the existing complete `numericFiber`, whose length is already exactly `profileCount`. The representative `ds` need not itself occur in `ns`: canonicality, its actual profile, and matching width/output are sufficient to provide a valid cover. The proof therefore also handles an empty counted list without needing to choose a member from it.

For its finite-list cardinality step, the corrected source calls the original public theorem

```text
P196.Agent2.OverflowFibers.nodup_subset_length_le
```

directly. The imported theorem is the generic statement that a duplicate-free list cannot have greater length than a list containing all its members. Its proof removes an included head from the covering list and uses the source list's no-duplicates property to retain coverage of the remaining elements. No no-duplicates premise on the covering list is needed. The corrected module contains no private replacement body.

The imported `Agent2OverflowBound` source has SHA256 `d0d602d806e430babef7350d7c4ccfdb2ccd0c44f34cd700c2e18ec2a851c6be`. Its provenance records original commit `58afcada8047e015b8f4233b96c44c7c5b9c4162` and path `proofs/Agent2OverflowBound.lean`. The three Agent #2 modules and the referenced `PeriodObstructions` source match that provenance's byte hashes. Only the generic list-cover theorem is used here; Agent #2's coefficient-word overflow fiber bound is not being treated as an integer multiplicity bound. Their import chain adds the four registered Std-based modules, with no second decimal foundation.

## The exterior digit-split factor is preserved

`profileCount_cons_outer_le` keeps `pairCount true s` as the exterior factor. It bounds the optional-center count by one and each interior pair count by ten, giving

```text
profileCount (s :: h) c <= pairCount true s * 10^h.length.
```

`fixed_width_preimages_outer_bound` obtains a finite digit list for an actual canonical representative `n` of width `L >= 2`, then applies the already reviewed profile extraction. The extracted exterior coefficient is transported back to the representative's original `columnSum d L 0` using equality of digits at indices zero and `L-1`. Both indices are within the finite width. Arbitrary tails of the original digit function are not compared.

This proves the refined bound for any duplicate-free list of predecessors with the same width and output:

```text
ns.length <= pairCount true s * 10^(L/2 - 1).
```

The uniform fixed-width bound replaces the exterior factor by its established upper bound nine. When `ns` is nonempty, the source selects its actual head as a representative; when it is empty, the bound is immediate.

The one-digit fixed-width lemma is separate. The actual representative has a digit list of length one; profile extraction forces an empty half. The exact profile cover is bounded by `profileCount_single_le`, so the result is at most one. A fictitious exterior pair or the multi-digit formula is not used for width one.

## The global width partition is complete

`predecessor_width_cases` applies Agent #105's actual-step width theorem to a positive predecessor and a canonical representation of its output. The predecessor has width `D` or `D-1`, because the last ordinary carry is zero or one. This is a numerical-width statement, not an assumption about a chosen profile.

For an arbitrary duplicate-free input list satisfying `0 < n` and `step n = Y`, the global proof defines:

- `wide`: filtering by `decimalWidth n D`;
- `short`: filtering by the Boolean complement of the same predicate.

Each filtered list inherits no-duplicates. Every member of `wide` has width `D`. The actual-step width cases and the negated predicate force every member of `short` to have width `D-1`. The existing `length_filter_partition` proves that the two lengths sum to the original list length. Thus no predecessor is dropped from the counting argument, and no assumption that the original list is complete is required.

The branch treatment is exhaustive:

| Partition case | Bound applied |
| --- | --- |
| `wide=[]`, `D-1=1` | The short list has length at most one; this includes the `D=2` overflow-only boundary. |
| `wide=[]`, `D-1!=1` | Since `D>=2`, the short width is at least two; the fixed-width bound and exponent monotonicity apply. |
| `wide!=[]`, `short=[]` | The fixed-width `D` bound applies to the whole remaining list. |
| Both nonempty | Actual short and wide members supply the cross-width exterior constraints. |

The case where both lists are empty is already covered by the first two branches. No element is selected from an empty list.

## The two-width case uses the correct refined factors

Only when both filtered lists are nonempty does the source select `a` from the short list and `b` from the wide list. Their canonical widths are exactly `D-1` and `D`; their actual ordinary outputs are equal. The unchanged Agent #105 results therefore yield:

- the short representative's exterior sum is eleven;
- the wide representative's exterior sum is one;
- the short width is at least two.

The last conclusion discharges the required length premise of the refined short bound. In particular, a one-digit shorter source cannot silently enter the two-width branch. The `D=2` case is handled without applying a length-at-least-two bound to a one-digit input.

The refined exterior counts are exactly `pairCount true 11 = 8` and `pairCount true 1 = 1`. The corresponding sublist bounds are therefore

```text
short.length <= 8 * 10^((D-1)/2 - 1)
wide.length  <=     10^(D/2 - 1).
```

Natural-number division and truncated subtraction are monotone, so the short exponent is at most the long exponent. The source explicitly proves the resulting power inequality and obtains

```text
8 * shortPower + longPower <= 9 * longPower.
```

This is sufficient for the desired global upper bound; the argument does not require an equality of the two exponents or a hidden parity assumption. The coefficient bounds are converted to **integer-list** bounds by the full numeric-fiber cover proved earlier.

## Final quantifiers and one-digit target

`all_width_preimages_bound` quantifies over every target `Y` of decimal width `D >= 2` and every finite `Nodup` list of positive ordinary predecessors of `Y`. It has no representative, decoder, target-profile, or single-input-width assumption in its public statement. Its conclusion is the uniform upper bound `9 * 10^(D/2 - 1)`.

`all_width_inverse_maximum` combines that arbitrary-target upper bound with the previously reviewed MaximumWitnesses theorem. The attainment side retains the equivalence for every `n : Nat`, identifying a complete positive inverse fiber across all widths, together with actual target width, no-duplicates, and the exact cardinality. The upper bound's arbitrary-sublist scope and the witness's completeness scope therefore establish the intended sharp all-width maximum.

For a one-digit target, `predecessor_one_digit_width` excludes the putative width-zero predecessor case using the positive-width component of `decimalWidth`. The one-digit fixed-width bound consequently applies to every positive predecessor. `one_digit_inverse_maximum` pairs that universal bound one with the complete target-two fiber `[1]`.

These are finite one-step inverse statements. No general arbitrary-target decoder, classification of all maximizing targets, sharp bound restricted to the two-width collision class, or infinite-orbit result is introduced by these modules.

## Pending final verification

Together with [pre-review-semantics.md](pre-review-semantics.md), this completes source-level independent review of all four frozen new modules: 36 public theorems and 5 public definitions. The combined **41** public declarations still await this reviewer's independent runtime audit. The original author receipts, current checkout HEAD, and untracked local files do not substitute for exact final published-source readback. The next stage remains the single full fresh build and complete audits against the parent's final published 17-module registry.
