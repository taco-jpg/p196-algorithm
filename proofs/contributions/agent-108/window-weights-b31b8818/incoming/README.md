# Agent 108 actual window incoming theorem

## Frozen source and verification

- Source: `proofs/Agent108WindowIncoming.lean`.
- SHA256: `8929758722b9d66c327654bb182c011b072be6aec100f801349e70040a65b5f6`.
- Author: session `b31b8818`, specialist `claims_inventory`, under the parent Agent 108 claim.
- Successful exact snapshot: `incoming/attempt-04/Agent108WindowIncoming.lean`.
- Real author verification: `--trust=0 -j1 -DElab.async=false`; compile exit 0 and audit exit 0.
- Audit: all 16 public source declarations. The two private helpers are used by public theorems and covered transitively. Every audited declaration uses a subset of `propext`, `Classical.choice`, and `Quot.sound`.
- The module has no `sorry`, `admit`, new `axiom`, `native_decide`, or `ofReduceBool`.
- Non-author reviewer `runtime` has accepted the frozen hash for independent rebuilding and semantic review. Its record is separate from this author verification.

## Exact scope

Fix any `b : Nat`, so the window length is the positive integer `b+1`.
Let `psi : List Nat → ℝ` satisfy the existing `PositivePotential b psi`:
it is positive on every list of exactly `b+1` entries, each at most 18.
Its values on all other lists are unrestricted.

For the original `Agent13ProductWeights.FiniteWord` state `s`, the weight is

```
if s.1 % 2 = 0
then A s.1 * windowProduct b psi (finiteStateHalf s)
else oddWeight s.
```

The hypotheses on the remaining factors are precisely:

```
∀ L, 0 < L → L % 2 = 0 → 0 < A L
∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s.
```

The half-word consists of every represented coefficient at positions
`0, …, s.1/2-1`. `windowProduct` uses every complete consecutive window
of length `b+1`; short half-words have the existing empty-product value 1.
The hypotheses place no restriction on variation of `A` across widths.

The incoming operator in every theorem is exactly the original
`Agent13ProductWeights.incoming`, a sum over its original `safeFiber`.
It includes all actual safe predecessors of every possible source width;
the selected same-width family only supplies a partial sum.

## Mathematical conclusion

Write `w = finiteWindowWeight b A psi oddWeight`,
`C = endpointConstant b k psi`, and `beta = localBeta b psi`.
Both `C` and `beta` are strictly positive under `PositivePotential`.
For every `r : Nat` and every `k > 0`, at the actual safe target

```
t = embeddedTarget (b+1) k r
```

the module proves

```
C * w t * (1 + beta)^r ≤ incoming w t
C * (1 + beta)^r ≤ incoming w t / w t.
```

These are `incoming_window_lower_bound` and `incoming_window_ratio`.
The first is obtained from an exact selected-family sum, not from an
assumed family-total or transition interface.

Fixing `k = 1` makes `C` and `beta` independent of `r`. The module then proves:

```
∀ K : ℝ, ∃ t, SafeState t ∧ K * w t < incoming w t
¬ ∃ K : ℝ, ∀ t, SafeState t → incoming w t ≤ K * w t.
```

These are `no_uniform_window_multiplier` and
`not_exists_uniform_window_bound`.
They concern a one-step incoming-weight bound and do not assert an
infinite nonpalindromic orbit or a result specific to the orbit of 196.

## Proof chain and reused arithmetic

1. `finiteStateHalf_bounded` uses the original finite-digit bound;
   `finiteWindowWeight_pos` uses only legal-window positivity.
2. `choiceBits` reads each member of `choices r` on `Fin r`.
   `choiceBits_ofFn` recovers the full original list, and
   `choiceBits_injective` uses the proved no-duplicates property.
   The resulting finite list sum therefore has no repeated state.
3. `embeddedState_window_weight` and `embeddedTarget_window_weight`
   use the independently authored exact half-word and equal-width bridges.
4. `actual_window_family_total` takes physical buffer length
   `B = 4*(b+1) = b+(3*b+4)` and applies `inputHalf_exact_total`.
   The arbitrary common factor `A t.1` becomes part of the target weight.
   This identity holds for all `b,k,r`, including `k=0` and `r=0`.
5. `embedded_window_family_le_incoming` composes the true finite-choice
   injection with `embeddedState_injective` and reuses
   `embeddedState_spec` for the actual safe transitions. It applies the
   original `partial_sum_le_incoming`; safety requires `k>0` here.
6. The exact sum gives the lower bound, and positivity gives the ratio.
   The already proved real-growth lemma is instantiated with the actual
   target weights and actual incoming values to obtain the final obstruction.

The embedding is a restricted subfamily of the original unbuffered family:
with `p=b+1`, its old number of blocks is `p+(p+1)*r`.
Original arithmetic and finite-safety proofs come from commit
`12a32789056f5eec8247166564ac2ef745c3c9d6`, under
`proofs/contributions/agent-13/folded-product-weights/` and their original
folded-family dependencies. No buffered carry theorem was reproved here.

## Dependency pins

The full source hash map and exact search path are in
`attempt-04/verification.json`. The immediate fixed mathematical APIs are:

| Module | SHA256 |
| --- | --- |
| `Agent108WindowEmbedding` | `1acb5964188bcb7828bec58cbd8b5328ff9d68467e5951eb3a4bf87d78eb4e7f` |
| `Agent108WindowFamilyRatio` | `051dcb42849d9cffb2fec0de77af138b6d7d6c415ff27d65725dcdf9cfcf7afc` |
| `Agent108WindowFamilyProducts` | `d4449500c98887a82dca222af318e8d99e8ef0d1ad5e58719658406c1650fdc8` |
| `Agent108WindowWeights` | `5bc7f457187ad0af4a4f7a340acf7f827b8e89537d73624519805d232c762eae` |
| `Agent108WindowObstruction` | `0dd91993667dddac3740ccadd7b2764cc2e6122121f19bd0a8354a9e0507a90a` |

Mathlib is pinned at `c44e0c8ee63ca166450922a373c7409c5d26b00b`;
Lean is 4.19.0. The author build reused the parent's fresh independent
FamilyRatio dependency closure and the original independently checked
Agent 13 dependency objects. Non-author review rebuilds the new closure.

## Preserved failures

- Attempt 01 stopped before elaboration because the optional
  `Mathlib.Algebra.BigOperators.Fin` object was unavailable. That import
  was removed; the required real finite-sum transport follows directly
  from already imported multiset/list identities.
- Attempt 02 preserved three elaboration rewrite failures.
- Attempt 03 preserved the remaining list-map rewrite failure.
- Attempt 04 resolved these proof elaboration details and passed.

All four attempts retain their exact source and stdout/stderr logs.
No failed attempt is represented as a checked result.
