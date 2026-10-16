# Independent source semantic review: spectral injectivity

## Decision and exact review set

**Decision: `PASS_SEMANTIC_REVIEW` for the two source hashes below. No blocking semantic findings.**

Reviewer: Agent #14 / `spectral_semantics`, a genuine separately assigned nonauthor reviewer. The reviewer previously examined the mathematical contract and did not author or modify either Lean proof module. This review inspected both complete source files, their theorem types and proof bodies, the current `CONTRACT.md`, the preserved mathematical source, and the companion Python definition.

| Reviewed module | SHA-256 |
| --- | --- |
| `proofs/Agent14SpectralWeights.lean` | `d691d02f3170db988ac9c5529402f5c09cf83425c7188d78cd0f2a6a8f4568c8` |
| `proofs/Agent14SpectralInjectivity.lean` | `082347eccad303f235a835c65be2dc20062d4457646082575cd192d06601d0c9` |

The exact historical claim and Python bytes were previously compared with main snapshot `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`:

| Mathematical source | SHA-256 |
| --- | --- |
| `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md` | `e4a1e6b61848f473693c36d91d2a453b1dc82b26a347fa76b2a0b9a7e1228e27` |
| `proofs/creative_global_spectral__8de5a77a944d0d04.py` | `393545516c13d41c0416e560ec37bab6b1c1655357ae351b0f960dea76ff7448` |

Source notes lines 27–38 are the selected recurrence, coordinate, and injectivity claim. Python lines 15–26 contain its executable definitions. The prior `review/contract-review.md` records the detailed interpretation and source caveats. The current `CONTRACT.md` correctly specifies natural coefficients, exact recurrence equations, finite-width equality, and the excluded stronger claims.

## Exact endpoint and source correspondence

The endpoint `Agent14.Spectral.coordinate_injective` quantifies over arbitrary `q r : Nat -> Nat` and `L : Nat`. It assumes only:

1. `q i <= 18` and `r i <= 18` at every `i < L`;
2. reflection symmetry of each word at the same ambient width, using `L - 1 - i`;
3. equality of their literal recurrence coordinates at width `L`.

Its conclusion is precisely `forall i, i < L -> q i = r i`.

This supplies the source's static fixed-width injectivity subclaim. The natural-number representation contains exactly the source's nonnegative integer alphabet. It does not omit a necessary lower bound: nonnegativity is enforced by the type. There is no additional assumption about positivity of the outer coefficient, parity of the center, absence of 9, carry behavior, or digit realizability.

The conclusion recovers the coefficient word `q` within the specified finite width. It does not assert equality of the total input functions outside that width, and it does not recover the original decimal integer or its individual digits. For example, the theorem remains consistent with decimal integers 12 and 21 having the same pair-sum word `(3,3)`.

## Complete proof-chain review

### Literal recurrence weights

`T` and `R` have the exact required seeds: `T 0 = 2`, `T 1 = 20`, `R 0 = 1`, and `R 1 = 19`. Both use the source's factor 20 and second-order subtraction.

Although their implementations use natural subtraction, `T_recurrence_exact` and `R_recurrence_exact` prove the corresponding addition equations:

`T(n+2) + T(n) = 20*T(n+1)` and `R(n+2) + R(n) = 20*R(n+1)`.

The proofs obtain the needed subtraction bounds from the preceding monotonicity lemmas. Thus truncation cannot alter either recurrence. Together with the exact seeds, these equations describe the same nonnegative integer sequences as the source. This is a valid implementation choice, explicitly disclosed in the contract.

The positivity and growth lemmas follow from the recurrence equations. `T_growth_from_one` correctly starts with the comparison from `T 1` to `T 2`; it does not assert the false comparison `19*T 0 <= T 1`.

### Central unit and dominance

`oddWeight 0 = 1`, while `oddWeight (n+1) = T (n+1)`. Consequently the increasing odd weights are `1, 20, 398, ...`; `T 0 = 2` is never used as the central weight. `R` provides the even weights `1, 19, 379, ...`.

`prefixSum` is the ordinary recursively defined sum over indices below its bound. It is independent of the property to be proved. `dominates_of_nineteen_growth` uses a positive initial term and nineteenfold growth to derive the strict inequality against eighteen times the earlier sum. The two final instances `oddWeight_dominates` and `R_dominates` prove these growth premises from the concrete recurrences; domination is not an unproved premise of the exported coordinate theorem.

The resulting odd statement includes the central unit exactly once among lower weights and excludes `T 0`. Its first noncentral inequality is `18 < 20`; the even family's corresponding inequality is `18 < 19`.

### Finite weighted encoding

`descendingScore w q n` sums `q i * w (n-1-i)` for `i<n`. `descendingScore_succ` separates the highest weight from the shifted remaining word. Its finite-index congruence explicitly justifies the subtraction and shift indices.

`descendingScore_le` bounds the remaining score by eighteen times the corresponding weight prefix. `descendingScore_injective` then uses the strictly smaller tail scores to show equality of the highest coefficients, cancels that common contribution, and recurses. Its induction decreases the finite word length. The generic dominance hypothesis is mathematically meaningful and is discharged by the concrete weight theorems in both spectral applications.

The proof does not assume the equality it seeks, use a bounded enumeration in place of the universal claim, or conclude equality of total functions. At length zero its conclusion is vacuous.

### Exact coordinate formulas and reindexing

`evenCoordinate q m` is definitionally the source sum `sum_(i<m) q(i)*R(m-1-i)`.

`oddCoordinate q m` is literally `q(m) + sum_(i<m) q(i)*T(m-i)`. It is not defined to be an injective code by construction. `oddCoordinate_eq_descending` proves the bridge to a descending score of length `m+1`. In this proof, `i<m` ensures `m-i` is positive on the noncentral summands, so `oddWeight(m-i)=T(m-i)` there; the final summand uses `oddWeight 0 = 1`. The explicit bridge therefore preserves the exact source formula and center.

The two half-word theorems recover indices below `m` and `m+1`, respectively. The even and odd full-word theorems apply the input symmetry only to valid indices and prove that the reflected index lies in the already recovered half. The guarded natural subtractions cannot identify an out-of-range exterior value with a valid reflected coefficient.

### Unified width and parity

`coordinate q L` selects `evenCoordinate q (L/2)` when `L%2=0` and selects `oddCoordinate q (L/2)` otherwise. This agrees exactly with the companion Python branch, including `m=L//2`.

`coordinate_injective` proves `L=2*(L/2)` in the even branch and `L=2*(L/2)+1` in the odd branch, then transfers the original finite bounds and symmetry to the corresponding theorem. It does not strengthen the input domain or change the width during the reduction.

## Boundary and hypothesis checks

| Case or potential overstatement | Finding |
| --- | --- |
| `L=0` | `coordinate_zero` proves value zero. The universal conclusion has no valid index and is vacuous. The definition's documentation calls this an empty-width extension. |
| `L=1` | `coordinate_one` proves `coordinate q 1 = q 0`; only the center exists. No even-center assumption is added. |
| `L=2` | `coordinate_two` proves `coordinate q 2 = q 0`; the full theorem obtains the second entry by symmetry. |
| Odd central coefficient 11 | Admitted by the general theorem, as needed for later possible comparisons with `11c`. |
| Coefficient 9 | Admitted without restriction. No carry-support premise enters the proof. |
| Zero outer coefficient | Admitted at the specified ambient width. Neither theorem asserts that an associated polynomial has degree exactly `L-1`. |
| Values beyond the width | Unconstrained and not included in the conclusion. |
| Different widths | Not compared by the theorem. `(2)` and `(2,2)` may both have coordinate 2. |
| Asymmetric words | Covered only by the half-word helper, whose conclusion concerns the independent half. Full recovery requires explicit symmetry of both words. |
| Decimal integer uniqueness | Not asserted. Only pair-sum coefficients are recovered. |

## Proof-policy inspection and verification boundaries

The reviewed files import `Std` and `Agent14SpectralWeights`, respectively. Full source inspection and a targeted forbidden-construct scan found no `sorry`, `admit`, newly declared mathematical axiom, `native_decide`, `unsafe`, `implemented_by`, or external oracle declaration in these two files. The proof bodies use ordinary inductive arguments, simplification, arithmetic lemmas, `omega`, and kernel-checkable `decide` for elementary base values.

The author development receipt at `development/Agent14SpectralInjectivity/attempt-002/receipt.json` records successful strict compilation for these same two hashes using Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. That receipt was inspected as author evidence; this reviewer did not perform the independent runtime build. The inspected explicit weight audit reports only `propext` and `Quot.sound` in its axiom union. It is not a complete independent transitive audit of both modules.

Accordingly, this file certifies semantic source review, not an independent clean-build or axiom-audit result. The separate runtime specialist's evidence must establish those acceptance gates. The review does not raise either file to integrated status or assert that a repository build target includes it.

After the complete source reads and source-hash capture, additional read-only commands failed before execution because the sandbox could not allocate a mount-marker directory (`No space left on device`). Those failed commands produced no additional verification evidence and do not alter the reviewed source hashes or the semantic analysis above.

## Coverage disposition and remaining review

The reviewed implementation supplies exact coverage of the recurrence-weight dominance and fixed-width integer-coordinate injectivity obligations. No semantic repair to these two source files is requested.

It does not cover evaluation at `10+sqrt(99)`, the `H,J` decomposition, the four evolution equations, neutral-nine carry support, the carry-defect ideal, spectral palindrome criteria, or any invariant or infinite-orbit conclusion about 196. These must remain separate open or partially covered claims.

The proposed decimal wrapper was not yet in the frozen review set. Once its exact source and dependency hashes are supplied, this report should be extended with a separate review of its arithmetic bridge and the precise object its conclusions recover. This pending extension does not change the semantic pass for the two hashes explicitly reviewed above.
