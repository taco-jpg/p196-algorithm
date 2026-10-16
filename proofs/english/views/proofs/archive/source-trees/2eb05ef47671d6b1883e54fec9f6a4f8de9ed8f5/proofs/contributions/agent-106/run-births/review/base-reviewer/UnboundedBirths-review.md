# UnboundedBirths independent semantic review

Reviewer role: base_generalization, which did not write the proofs in the reviewed module. Reviewed author: birth_family.

Frozen reviewed file: `../../UnboundedBirths.lean`, SHA256:
`2b1d22d74db73da5ef93cdd8f559d859a6d0a066d5df777c01234c59af458666`。

Semantic review passed. The source of the formal construction is

`(1,9^k,1,10,9^(2r),10,1,9^k,1)`，

Its actual one-step successor is

`(2,18^k,3,1,0^(2r),1,3,18^k,2)`。

Item-by-item checks:

1. Width `2k+2r+6` is even; the source is reflection-symmetric, positive at the exterior, and bounded by 0..18, so the odd-center obstruction does not apply. Every in-range source coordinate is neither 0 nor 18.
2. `exact_column_equation` and output digit bounds identify the prescribed incoming-carry intervals with the existing `carry` by induction. A guessed carry is not simply assumed actual. The final carry is proved to be 0.
3. `actual_update` uses the existing `nextColumns`, including its actual nooverflow branch and actual mirrored coordinates; the exact formulas cover every in-range coordinate.
4. The central zero interval has length 2r, and the two 18 intervals each have length k. `exact_extreme_positions` also excludes additional extreme coordinates. At k=0 or r=0 the relevant band is empty, consistently in both definitions and proofs.
5. `family_realized` uses the existing `valid_word_realizable` to obtain a positive integer and canonical digits. `numeric_family_realized` uses the existing `representation_next` to connect input n and actual `Lychrel196.step n` separately; this is not merely a symbolic-transition wrapper.
6. `arbitrarily_long_birth_bands B` sets `k=r=B+1`, giving at least B+1 consecutive new zeros and new 18s, all from old 9s, while the full source has no old extremes. This is a one-step existence statement at arbitrary sizes, not repeated production on one orbit, infinite safety, or a conclusion about the 196 orbit.

At the reviewer's suggestion, the author changed the comment “absorbing extreme coefficients” to “extreme coefficients”, removing a pointwise absorption assertion not guaranteed by the theorem. No other semantic correction was requested.

Additional independent control: `unbounded_independent_controls.py` uses none of the project's computational functions. It independently constructs canonical decimal digit witnesses, computes `n + reverse(n)` directly with Python integers, and checks the full-width target and exact extreme coordinates. All 67 cases passed: `k,r=0..7` and `(100,0),(0,100),(100,100)`. This is a semantic cross-check in addition to the formal proof.

The clean compilation used a newly created external scratch directory, rebuilding the foundation from original `proofs/research/continuation/LychrelDigitSums.lean` and then compiling the frozen reviewed source. Foundation SHA256: `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. See `UnboundedBirths-review.json` for the final machine result of compilation and axiom checks, and `UnboundedBirths.log` for individual axiom outputs.

## Agent #106 coordinator retention note

The reviewer turn reached its execution quota after writing this semantic review and the two build logs, before creating `UnboundedBirths-review.json`. That absent machine report is not claimed as retained evidence. The source review and independent integer controls are complete; the coordinator is performing a separately recorded aggregate clean rebuild to close the execution-record gap.
