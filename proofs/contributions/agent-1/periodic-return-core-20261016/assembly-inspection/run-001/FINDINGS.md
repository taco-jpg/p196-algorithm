# Source-only adversarial assembly inspection

Claim: `efe6d4b95f53ad8fbcebf113f8da0616dfa67b22`.
Reviewer: Agent #1 specialist `/root/verification_plan/handoff_boundary`.

**No blocking logical defect found in the pinned OuterRank and ReturnCore source snapshots.** This is source-only inspection of two modules I did not author. It is not independent review of my `Agent1PeriodicZeroPath` module, a new Lean build, a fresh combined dependency verification, an SCC computation, or a claim that the developing sources have passed their authors' pending checks.

Reviewed target snapshots:

- `Agent1PeriodicOuterRank.lean`: SHA-256 `e345ef2c5fe7734f64ead7e971f0ea8b807dfcc2d84e3d50625109871fe10477`.
- `Agent1PeriodicReturnCore.lean`: SHA-256 `42c0ef083800de603417b3863b7c11841022247181c591a60978adc6c2642841`.

Supporting contract snapshots and hashes are in `manifest.json`; the exact files read are retained under `source/`. Line references below refer to these pinned copies.

## Checked boundaries

1. **Off-catalog component default does not imply membership.** OuterRank line 16 defines the total classifier with default label 8. ReturnCore line 20 defines `returnCore` by filtering `outerCatalog`, not by treating every label-8 value as a catalog member. All finite paths enter through explicit initial catalog membership and `quotient_path_valid_catalog` propagates that premise through the endpoint. In particular, removing catalog membership from the initial classification would be invalid: the off-catalog node `([14,14,4,4],0)` also receives default label 8, although its outside value is neither 9 nor 10. The current interface retains the necessary premise.

2. **Clipped rank is positive, and no injectivity is assumed.** OuterRank line 208 uses `132 - min c 131`; the source proof of positivity covers every Nat, including labels beyond 131. The map is intentionally not injective there. ReturnCore never infers component equality merely from rank-function injectivity. It builds the existing `RankCertificate` from the checked strict drop on unequal component labels. Such a drop excludes different labels of equal rank along any used edge, which is exactly what the generic interval theorem requires.

3. **Zero label is used only with catalog membership.** `outerComponent_zero_phase` (OuterRank line 3210) requires both `s ∈ outerCatalog` and label 131. Its use at ReturnCore line 76 passes the original initial `hmem`. The resulting literal zero-phase equality is passed to the existing ZeroPath endpoint together with original initial validity, positive length, and the complete tuple return. This inspection checks that call's premises and conclusion; it does not independently review the reviewer-authored ZeroPath proof.

4. **Zero-step and positive-step claims are separated.** `quotient_return_component_constant` allows N=0 and concludes only equality of component labels for indices `i ≤ N`. The certificate has N+1 vertices, so every strict transition premise corresponds exactly to `i < N`. The core theorem and the initial 9/10 corollary require `0 < N`; the core theorem uses that premise to obtain edge 0 and to justify time 1 within the interval. It cannot exclude a zero-step return.

5. **Complete state return is retained.** Every ReturnCore endpoint takes `B N = B 0 ∧ H N = H 0 ∧ w N = w 0`. The component-closure subproof needs only B and w equality, as expected for that projection. The zero-label exclusion passes all three equalities to the full-interface no-return theorem. No argument substitutes equal widths, equal residues, or mere projection equality for a complete state return.

6. **The correct existing condensation theorem is used.** ReturnCore line 51 calls `CondensationBound.component_interval` with component weights identically 1, ranks `componentRank`, N+1 vertices, and endpoints 0 and N. The exact supporting theorem requires `RankCertificate`, positive weights, endpoint inclusion, and equal endpoint components; it does not require `IntervalBound`. The source supplies precisely these assumptions and does not invoke the separate vertex-count theorem that would require `IntervalBound`. No bound on time spent in a cyclic component is asserted.

7. **Original validity supplies positive outside bounds for the 9/10 wrapper.** ReturnCore line 93 obtains `0 < outside ≤ 18` from the existing `outside_bounds` under full original initial `ValidPeriodic`. It constructs `Fin 19` using the upper bound and passes positivity to `outerCatalog_initial`. Thus membership of the initial phase is proved before applying the catalog-guarded initial classification. Neither outside positivity nor catalog membership is silently inferred from the total component default.

8. **Finite data assembly retains the original lists and edge labels.** OuterRank's 59 node blocks and 59 edge blocks are connected to the original catalog by `rankNodeBlocks_eq` and `rankEdgeBlocks_eq`, each stated as exact list equality with `rfl`. Its structural `RankBlocksAll.flatten` lemma is the straightforward induction over all blocks. A lightweight textual comparison of the pinned block literals found exactly 878 nodes and 1,458 edges, identical to the corresponding catalog blocks in order and in every source/clock/carry/target field after whitespace/trailing-comma normalization. There are exactly 59 local node checks and 59 local edge checks. This comparison is a source-integrity check, not independent kernel verification of the Boolean checks or archived SCC labels.

## Limits and follow-up

No source fix is requested. The statements claim necessary return restrictions only: they do not prove a return exists for outside 9 or 10, identify arbitrary graph paths with realizable interfaces, delete zero graph cycles, or assert termination or safe infinite behavior. The existing abstract zero cycles remain in the copied edge data.

The target authors and parent were informed of this provisional source pass. Subsequent edits need a delta inspection against these pinned hashes. Parent fresh compilation and complete independent review remain separate; any author compile correction should be reflected in that review.

The local literal-comparison command is `python3 check_literals.py`, run from this directory or with an absolute script path; it exited 0, and its exact output is in `check_literals.log`. An initial ad hoc parser assumed an unsplit public literal catalog and stopped with `AssertionError: outerCatalog`; it produced no comparison result. The retained successful script instead parses the actual 59 existing catalog blocks. No Lean process was started by this inspection.

Only this assembly-inspection directory was written. No inspected module, registry, Git state, or external service was modified.
