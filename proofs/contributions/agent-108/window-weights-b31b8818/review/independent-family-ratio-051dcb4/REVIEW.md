# Independent review of the exact family ratio

Reviewer: Agent #108 root, a genuine agent distinct from the author
`semantic_scout` of `Agent108WindowFamilyRatio.lean`.

Reviewed source SHA256:
`051dcb42849d9cffb2fec0de77af138b6d7d6c415ff27d65725dcdf9cfcf7afc`.

**Result: PASS for the literal complete-window family ratio and finite total.**

## Execution

`run_review.py` froze eight source modules at their listed exact hashes,
then rebuilt each in dependency order into an initially empty directory.
Every compiler invocation explicitly used `--trust=0`. All eight modules
and the separate complete public-declaration audit exited zero. All 63
public source declarations had matching axiom output, with no axiom
outside `{propext, Classical.choice, Quot.sound}`. See
`review-result.json`, `sources/`, and `logs/` for the exact commands,
frozen source, declaration correspondence and original output.

This reviewer authored the lower-level `FamilyProducts` module, so this
record does not present the reviewer as independent of that dependency's
authorship. Its separate independent review is assigned to
`semantic_scout`. The present fresh rebuild nevertheless covers that
dependency's actual bytes as part of the FamilyRatio proof chain.

## Statement and interpretation

The physical window width is `b+1`; the physical buffer length is `b+c`.
All `b,c,k,r : Nat` are retained in the proved formulas. In particular,
`b=0`, `c=0`, `k=0`, `k<b`, and `r=0` are not excluded. The endpoint
constant depends on `b,k,psi`, and the insertion ratio on `b,psi`; neither
contains the family-size parameter `r` or extra-buffer parameter `c`.

`localBeta` is the product over all complete windows of
`buffer b ++ [14,14,4,4] ++ buffer b`, divided by the all-nine window
potential to the power `b+4`. Its positivity uses only legal coefficient
windows. The denominator has an explicit strictly positive proof.

`inputHalf_product_ratio` proves equality of the actual literal source
product and `endpointConstant * targetProduct * binaryWeight`. It uses
the separately proved source and target product decompositions. The
extra-buffer exponents combine through the proved identity
`c*(n+1)+(b+4)*n = n*(b+c+4)+c`; the two endpoint denominators are
cancelled using explicit nonzero consequences of positive legal windows.

`inputHalf_exact_total` uses the actual recursively enumerated `choices r`
and the proved length of every member to substitute the same target in
each summand. The binary sum is then evaluated by the prior proved
`weighted_family_total` theorem. Its statement is an equality of finite
real sums; no arithmetic-transition premise is hidden in it.

The module proves the promised finite-window weight calculation. Applying
it to the original safe incoming operator additionally requires the
actual long-buffer embedding, distinctness, safe-fiber inclusion and
positive equal-width factor cancellation. Those are separate modules;
they are not certified by this review of FamilyRatio alone.
