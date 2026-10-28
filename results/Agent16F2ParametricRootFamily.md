# Agent16F2ParametricRootFamily

**PAPER PROOF.** For each integer `r>=1`, let the binary overflow schedule be
`g_r = 1 0^r 11 0^(r+1)` (temporal length `2r+4`, or any cyclic rotation).
The `bauto3` canonical-root first-spatial-column map has a closed time path
in base `b>=2` **iff** `4<=b<=6` when `r=1`, or
`2^(r+1)<=b<=2^(r+2)-3` when `r>=2`. There are **exactly four**
compatible carry assignments for each admissible `(r,b)`, and zero otherwise.

This gives arbitrarily large bases with a *first-coordinate* closure,
not an exterior SCC, a parametric Lychrel certificate, or a base-10 result.
The complete proof is `reports/Agent16F2ParametricRootFamily.md`.
Independent dynamic-programming control for all rotations, r=1..7, and
all b=2..`2^(r+2)+3`:
`python3 calculation/decimal_frontier/lattice_formats/code/agent16_param_f1.py`.
