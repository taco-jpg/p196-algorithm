# Independent source semantic review: spectral injectivity

## Decision and exact review set

**Decision: `PASS_SEMANTIC_REVIEW` for the three source hashes below. No blocking semantic findings.**

Reviewer: Agent #14 / `spectral_semantics`, a genuine separately assigned nonauthor reviewer. The reviewer previously examined the mathematical contract and did not author or modify any of the three Lean proof modules. This review inspected all three complete source files, their theorem types and proof bodies, the relevant original decimal definitions and lemmas, the current `CONTRACT.md`, the preserved mathematical source, and the companion Python definition.

| Reviewed module | SHA-256 |
| --- | --- |
| `proofs/Agent14SpectralWeights.lean` | `d691d02f3170db988ac9c5529402f5c09cf83425c7188d78cd0f2a6a8f4568c8` |
| `proofs/Agent14SpectralInjectivity.lean` | `082347eccad303f235a835c65be2dc20062d4457646082575cd192d06601d0c9` |
| `proofs/Agent14SpectralDecimal.lean` | `c3bc01e978d9bd3e90fc8c6b7a185432f02db94184eaec324bbb3f762fb978a2` |

The exact historical claim and Python bytes were previously compared with main snapshot `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`:

| Mathematical source | SHA-256 |
| --- | --- |
| `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md` | `e4a1e6b61848f473693c36d91d2a453b1dc82b26a347fa76b2a0b9a7e1228e27` |
| `proofs/creative_global_spectral__8de5a77a944d0d04.py` | `393545516c13d41c0416e560ec37bab6b1c1655357ae351b0f960dea76ff7448` |
| Original decimal interface: `proofs/LychrelDigitSums__0810ace083af80c5.lean` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |

The original decimal interface was additionally compared byte-for-byte with the same pinned main snapshot during this review. Its Git blob is `8a865176625283648a8a20dd2411ed77670eb0a2`. The wrapper's reviewed mathematical interfaces are `DecimalDigits.value`, `reflected`, `columnSum`, `columnSum_symmetric`, `columnSum_bounded`, `Canonical`, and `FoldedDecimal.Admissible` from that preserved source. This is a review of the relevant interfaces and proof bodies, not an independent audit of every declaration in the historical module.

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

## Original decimal interface and wrapper review

The original `DecimalDigits.columnSum d L i` is `d i + d (L-1-i)`, with least-significant-first digit order. Its original `columnSum_bounded` theorem obtains the bound 18 from digit bounds 9 at both reflected indices. Its original `columnSum_symmetric` theorem proves reflection symmetry at every valid index. The wrapper reuses these declarations directly; it does not introduce a replacement digit model.

The original `DecimalDigits.Canonical n d L` consists of positive width, digit bounds within the width, a positive leading digit, and the exact evaluation equation `value d L = n`. The original `FoldedDecimal.Admissible L q` consists of positive width, positive outer coefficient, the bound 18, reflection symmetry, and even coefficients at fixed points of reflection. Those original conditions remain unchanged.

### `admissible_coordinate_injective`

The two premise projections `hq.2.2.1` and `hq.2.2.2.1` are exactly the coefficient-bound and symmetry fields of the original admissibility definition, and the corresponding `hr` projections serve the second word. The theorem concludes equality only for `i<L`. Positive width, positive outer coefficient, and central parity are retained as properties of the original admissible domain, but are not falsely made necessary for the general coordinate theorem.

### `canonical_column_sums_injective`

This theorem takes two original canonical representations at the same width, together with equality of their pair-sum coordinates. `hd.2.1` and `he.2.1` supply precisely the original digit bounds. The original bound and symmetry theorems discharge every premise of `coordinate_injective` for the two `columnSum` words.

Its conclusion is equality of the **column sums** at all indices below `L`. It does not claim `n=p`, `d=e`, or uniqueness across different widths. Therefore it is a faithful decimal corollary of the static theorem, with the necessary arithmetic bridge to the original definition of mirrored pair sums included.

### Exact controls and the nonuniqueness witness

`coordinate_196_column_sums` uses digits 6, 9, and 1 at indices 0, 1, and 2. The original `columnSum` therefore gives `(7,18,7)`, and the original odd formula gives `18 + 7*20 = 158`. Values of the digit function outside width three do not enter the statement. This is an exact finite coordinate control, not a proof about subsequent orbit states or carries.

`distinct_canonical_inputs_same_coordinate` gives explicit canonical witnesses for 12 and 21 at width two. Their least-significant-first digit words are `(2,1)` and `(1,2)`, respectively; both produce pair-sum word `(3,3)` and coordinate 3. The witnesses prove all original canonical fields, explicitly prove `12 != 21`, and prove equal coordinates. The bounded-digit proofs are ordinary case splits; the concrete arithmetic uses kernel-checkable `decide`.

All four wrapper declarations have the advertised semantic scope. The wrapper introduces neither a new definition of admissibility or canonical representation nor an assumption hiding an unproved dynamical statement.

## Proof-policy inspection and verification boundaries

The weight and injectivity files import `Std` and `Agent14SpectralWeights`, respectively. The decimal wrapper imports `Agent14SpectralInjectivity` and the original `LychrelDigitSums` module. Full source inspection and a targeted forbidden-construct scan found no `sorry`, `admit`, newly declared mathematical axiom, `native_decide`, `unsafe`, `implemented_by`, or external oracle declaration in the three new source files. The proof bodies use ordinary inductive arguments, simplification, arithmetic lemmas, `omega`, and kernel-checkable `decide` for elementary base values.

The author development receipt at `development/Agent14SpectralInjectivity/attempt-002/receipt.json` records successful strict compilation for these same two hashes using Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. That receipt was inspected as author evidence; this reviewer did not perform the independent runtime build. The inspected explicit weight audit reports only `propext` and `Quot.sound` in its axiom union. It is not a complete independent transitive audit of both modules.

The decimal wrapper's author build was still pending when its semantic review was requested; this reviewer does not assert a successful wrapper compilation. The selected runtime build must also verify that the imported module named `LychrelDigitSums` is built from the exact original source hash listed above.

Accordingly, this file certifies semantic source review, not an independent clean-build or axiom-audit result. The separate runtime specialist's evidence must establish those acceptance gates for all three modules and their imported dependency chain. The review does not raise any file to integrated status or assert that a repository build target includes it.

After the initial two-module source reads and source-hash capture, additional read-only commands temporarily failed before execution because the sandbox could not allocate a mount-marker directory (`No space left on device`). Those failed commands produced no verification evidence. The wrapper and relevant original definitions were subsequently read through an approved read-only execution escalation, without changing the sandbox or deleting any files. All three final source hashes and the original decimal-source hash were then independently captured, and the decimal source was confirmed to match pinned main.

## Coverage disposition and remaining review

The reviewed implementation supplies exact coverage of the recurrence-weight dominance and fixed-width integer-coordinate injectivity obligations, with corollaries for the original admissible words and canonical decimal pair-sum words. No semantic repair to these three source files is requested.

It does not cover evaluation at `10+sqrt(99)`, the `H,J` decomposition, the four evolution equations, neutral-nine carry support, the carry-defect ideal, spectral palindrome criteria, or any invariant or infinite-orbit conclusion about 196. These must remain separate open or partially covered claims.

The decimal-wrapper extension is included in this report for its exact frozen hash. Remaining acceptance work consists of the actual final selected-source build, complete dependency/axiom audit, and publication/integration evidence. Any subsequent modification to a reviewed source requires a new hash-specific review or an explicit review of its delta.
