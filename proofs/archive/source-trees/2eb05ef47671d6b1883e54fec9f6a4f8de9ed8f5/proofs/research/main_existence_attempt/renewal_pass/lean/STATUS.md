# Checked all-length delayed overlap gate

`DelayedOverlapGate.lean` proves the full two-step gate from
`correlation_pass/constructive/VARIABLE_OVERLAP_AND_GATE.md`, including the
constructive branch's extension of the outside coefficient to p=1,...,4.
All spacer lengths are symbolic. Decimal Lychrel existence remains open.

## Main parameterized statement

For natural parameters satisfying

    r >= 1,  1 <= p <= 4,  u >= 1,  v >= 5,  u+v <= 8,

put

    A  = p · 0^r · (u,v,v,u) · 0^r · p,
    Q  = Phi_1(A),
    A' = 4p · 0^r · (4u+1,4v-19,4v-19,4u+1) · 0^r · 4p.

`Phi_1` is the coefficientwise sum with a shift by one position, without
carry normalization. The component width is 2r+6 and the whole width is
2r+7. The checked exact transitions are

    G(A) = 2A,       G²(A) = A',
    G(Q) = M,        G²(Q) = Phi_1(A').

The middle whole word M has outside coefficients 2p at positions
0,1,2r+5,2r+6; flank coefficients 2u at r+1,r+5; inner coefficients
2(u+v)+1 at r+2,r+4; center 4v-20; and zeros elsewhere. Every whole state
is proved admissible. All required width and final-carry facts are proved.

The final return statements compare coefficients only on the actual finite
width, as required for ordinary decimal representations. The spacer r is
unchanged. The core and outside parameters change exactly as displayed.

## The actual repair mechanism

The file proves, at every coefficient, the nonzero difference

    M - Phi_1(2A) = 0^(r+2) · (1,-20,1) · 0^(r+2).

The formal comparison word `Phi_1(2A)` has center coefficient 4v>18.
`redundant_not_admissible` records this explicitly; the word is normalized
as a redundant coefficient word and is never claimed to be an admissible
pair-word input.

After ordinary carry normalization, the digit difference is exactly

    0^(r+2) · (1,0,-1) · 0^(r+2).

Both final carries are proved zero. This digit difference is antisymmetric
under reflection of their common width and therefore disappears when
mirrored digits are added. `seam_cancels_next` instantiates the general
`columnSum_eq_of_antisymmetric_difference` lemma with this concrete gate.
`intermediate_overlap_fails` proves that the first step really does depart
from independent overlap before the second-step repair.

The carry profiles themselves are fully checked recurrences up to the
symbolic width. They require neither a bounded list of spacer examples
nor an unproved all-index carry hypothesis in any final gate theorem.

## Ordinary decimal realization and palindrome safety

`numeric_two_step_safety` proves that every canonical ordinary decimal
realization of Q has nonpalindromic first and second positive iterates.
`numeric_return` proves that its actual second iterate has the returned
pair word at the stated width. The initial ordinary integer is allowed to
be palindromic; the asserted safety concerns exactly positive times 1,2.

`realized_safe_gate` supplies a positive finite ordinary integer and its
canonical digits for every allowed parameter tuple, together with the
two safety conclusions and exact returned representation. All realization
and arithmetic-interpretation obligations are discharged by existing
proved decimal representation theorems.

The direct third-step characterization is also checked:

    T³(n) is a palindrome  iff  p<=2 and u=1 and v=5.

For the original p=1 gate this recovers termination at positive step three
for the (1,5) core and third-step safety for the other five cores. No later
first-hit classification is imported or claimed here.

The component's first positive ordinary successor is proved palindromic,
so the whole gate's first-step safety is an actual effect of the seam
interaction. It is not inherited from a safe component trajectory.

## Why this is not a renewal certificate

`return_not_in_domain` proves that `(r,4p,4u+1,4v-19)` cannot satisfy the
same gate's domain. The theorem provides neither growth of r nor an exact
later reset to an eligible core and outside context. No infinite safe
orbit, finite Lychrel witness, or result about 196 follows from the gate
alone.

This excludes immediate reuse only of the original six-core `Domain`
defined in this source. It is not a universal exclusion of a second gate:
the separate expanded twenty-core construction admits the handoff
`p=1,(u,v)=(1,6)` to `p=4,(5,5)` and a second return at time four. That
broader written construction is not formalized or assumed here.

The p>=5 overflow-transport formula and later first-hit 4/11 results are
separate constructive contributions. They are not formalized in this file
and are not used as assumptions.

## Source map and reproduction

All 49 new declarations are in `DelayedOverlapGate.lean`. Main entries:

| Declaration | Checked conclusion |
| --- | --- |
| `component_two_step_return` | Exact all-r component return |
| `whole_two_step_return` | Exact all-r delayed overlap repair |
| `coefficient_defect_exact` | Intermediate coefficient error (1,-20,1) |
| `normalized_digit_defect_exact` | Exact normalized digit error (1,0,-1) |
| `seam_cancels_next` | Concrete cancellation after reflection |
| `numeric_two_step_safety` | Positive times 1 and 2 safe for every realization |
| `numeric_return` | Actual second iterate represents the returned word |
| `numeric_third_palindrome_iff` | Exact direct third-step criterion |
| `realized_safe_gate` | Positive finite decimal realization exists |
| `return_not_in_domain` | Immediate reuse of this gate is impossible |

From the project root run:

    python main_existence_attempt/renewal_pass/lean/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The checker freshly compiles the unchanged standalone decimal dependency,
the four unchanged previously audited delay-bridge modules, the new gate
module, and generated `AllAxioms.lean`. Every new theorem is audited
transitively. Only Lean's standard `propext`, `Classical.choice`, and
`Quot.sound` are permitted; all custom axioms, proof placeholders, and
`native_decide` are excluded.

`verification.json` is written only after all compilations, the complete
axiom audit, and before/after source hash comparisons succeed. `compile.log`
records the build output. `development_checks/` and `DEVELOPMENT_NOTES.md`
retain the earlier unsuccessful proof-script routes and their resolution.
No older research source was modified and no remote write was performed.

Fresh rebuild result: **PASS** with Lean 4.19.0. All seven compilations
exited successfully. The decimal dependency took 52.23 seconds, the new
gate module 26.36 seconds, and the complete 49-theorem audit 1.69 seconds.
Every audited declaration depends only on the permitted standard logical
axioms. The new source SHA-256 is
`c24d7774af6487fcab63a4d60cd10aaabb1b270b3dc0f4ac42dd3655b416b112`.
