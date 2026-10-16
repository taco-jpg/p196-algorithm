# Agent 8: common-overflow antisymmetric defect transport

## Source and exact claim

Original source: `proofs/research/main_existence_attempt/renewal_pass/constructive/STATUS.md`, section 2, original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, Git blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`. Current source snapshot: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.

Given finite coefficient inputs q and s of the same old width L, write e_i = output(q)_i - output(s)_i using integer subtraction for i < L and zero elsewhere. If e_i = -e_(L-1-i) throughout the old width and both actual terminal carries equal h in {0,1}, their paired successors at their common actual width L+h differ by (1-x^h)e. Thus h=0 gives equality, while h=1 preserves every nonzero finite digit defect as a nonzero successor difference.

## Exact proof contract

A. The statement above is the original general transport claim, not the classification of all delayed-overlap cores.
B. Export an indexed identity for `FoldedDecimal.nextColumns q L` minus `nextColumns s L`; old digit differences are zero-extended using `RawSymmetryObstruction.supported`. Define shift by `previous` for h=1 or a bounded natural shift for a unified h in {0,1}.
C. Reuse `DecimalDigits.output`, `carry`, `FoldedDecimal.nextWidth/nextColumns/representation_next`, `Agent107.SeamCoefficients.actualCoeff`, and `Agent107.PairResponse.nextColumns_actualCoeff`. Preserve imported source bytes and names.
D. Inputs q,s : Nat -> Nat, L : Nat, actual equal terminal carry h in {0,1}, antisymmetry at old width. The abstract coefficient identity does not require bounded coefficients, symmetry of q/s, canonicality, or positivity; ordinary-integer corollaries do require explicit `Canonical` representations and actual pair-word equalities.
E. Universal q,s,L,h first, hypotheses next, every output index i < L+h last. Nonzero difference conclusion starts with an actual witness i<L, not a supplied successor difference.
F. Treat L=0 correctly, both i=0 and i=L in the overflow branch, old digit differences with either sign, redundant input coefficients, and canonical inputs with trailing zeros. `extended` is only valid within its stated width: its constant tail is not a polynomial zero extension.
G. The coefficient equation is the exact coefficientwise form of the stated polynomial identity. Noncancellation must be derived by finite-difference injectivity; a conditional statement assuming that result is not completion.
H. Dependencies are pinned in the generated module manifest. Build the actual import closure before adding exports; preserve any pre-existing build failure separately.
I. Expected namespace `P196.Agent8.CommonOverflowDefect`; endpoints for common-overflow transport, non-overflow cancellation, overflow successor agreement iff normalized digits agree, noncancellation, and actual integer representations.
J. Lean 4.19.0 release `6caaee842e94`; direct clean source builds; `#print axioms` for every export; independent clean rebuild and semantic review; transitive permitted axioms only `propext`, `Classical.choice`, `Quot.sound`. No sorry, admit, native_decide, new mathematical axioms, or unverified oracle. Include a concrete admissible actual-integer witness for nonvacuity.

## Ownership and scope

Task: `agent8-common-overflow-defect-20261016`, successfully published at coordination commit `464ff3d33ed5d1cdefdbe3e5e0c78992ec062efc`. Source branch: `formalize/agent-8/common-overflow-defect-20261016`. Agent107 dependencies and earlier delayed-overlap proofs retain their authorship. No default-branch integration claim is taken. Agent100 Group II, Agent2 time-eleven/fibers, and Agent3/7/9 fiber tasks are separate.

## Current status

ACTIVE_FORMALIZATION. Exact runtime and a Std smoke check passed. New mathematical exports are not yet asserted to compile. This result supplies no infinite safe orbit or proof concerning 196.

