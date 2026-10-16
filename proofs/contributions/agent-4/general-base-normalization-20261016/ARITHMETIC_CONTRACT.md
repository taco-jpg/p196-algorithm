# Arithmetic bridge — Agent #4

This extends the normalization/realization contract, without claiming the source's four-step theorem. Source and ownership pins are in CONTRACT.md. GeneralBaseNormalization.lean at 9c456f53a277158376edbe628e30e163e3c223d1 passed actual Lean 4.19.0 checking twice (run 38939965220, job 117104824303), with 18 declarations and only propext/Quot.sound. The arithmetic extension remains SOURCE_PRESENT until its own build succeeds.

## Exact targets

1. Threshold carry equals `(q+c)/b` under base >=2, `q <= 2*(b-1)`, and `c <=1`. Original digit-pair bounds are proved, never silently assumed for arbitrary coefficients.
2. The actual recursive quotient-carry word agrees with the threshold word, at all boundaries including zero and final overflow.
3. For any finite positive-width canonical digit vector and even base >=4, construct another vector with the same actual width and the same entire first quotient-carry word; its pair sums are exactly the prescribed normalization.
4. With `value(b,d,n) = sum_{i<n} d_i*b^i`, prove schoolbook carry conservation and `value(pairCoeff) = value(d)+value(reflect(d))`. Reflection uses the physical input width; leading zeroes on reversal contribute zero, rather than changing the input width.
5. Bounded digits and a positive leading digit imply `b^(n-1) <= value(d) < b^n`. Thus canonical width is an arithmetic fact, not an arbitrary state annotation.

## Boundaries and semantic scope

Carry conservation includes width zero and does not require positivity; the representative theorem requires n>0 and bounded digits. Canonical representation of an arbitrary input natural and correspondence with its independently extracted digits will be documented separately if not yet supplied. None of these declarations asserts future safety, palindrome avoidance, four-step normalization termination, sharpness, or a Lychrel witness.

## Verification

`python3 check.py /absolute/path/to/lean /new/audit/directory` builds both listed modules twice in separate fresh directories with only those newly built local dependencies on LEAN_PATH. Each exported theorem must have an inspected axiom report. No source-only count is a proof count. The CI's separately pinned historical baseline remains unchanged. Independent review is not supplied by these author-controlled checks.
