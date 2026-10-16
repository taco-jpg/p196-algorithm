# Independent review of the folded-weight obstruction

**Verdict: PASS, at the stated all-parameter scope.** This is a source and mathematical review of `FOLDED_WEIGHT_OBSTRUCTION.md` and `check_folded_weights.py` at external commit `60d4348349a80c513008df9263905e7955b4ce79`. Four small source/record files are preserved byte-for-byte, with Git blob and SHA-256 identities in `source_manifest.json`. No full finite catalog was replayed in this review, and no Lean verification is claimed.

## Actual dynamics and safety

Each reflected half-word has even width, coefficients at most eighteen, and positive outside coefficient, so a positive ordinary decimal realization exists. A concrete realization chooses each high digit as the smaller of nine and its prescribed pair coefficient, and the opposite low digit as the remainder. No odd-center condition is required at even width. For every realization, its first reverse-and-add output is the coefficient evaluation `E(q)`, so the constructed relation is independent of the chosen realization.

The seven listed inverse edges satisfy the displayed low and high carry equations directly. The initial state `00` imposes both low carry zero and final carry zero. Both four-letter alternatives start and finish at `01`; the terminal fourteen reaches `11`, and the central eighteens retain `11`. Equality of the two center carries joins the reflected fronts into a single actual carry chain. Consequently this is a complete normalization relation, not a path with an unproved center or independently guessed carry. The zero-block case uses the same argument. Distinct binary strings give distinct source half-words, and every source and target has the same width.

Both words contain an eighteen because `k>=1`; this excludes both unsafe predecessor classes. Thus these are legitimate safe incoming sources of a safe target. Their odd outside pair coefficients also force every ordinary realization to be initially nonpalindromic. No assertion of an arbitrarily deep incoming ancestry is used or obtained.

## Product weights

For fixed strictly positive coefficient weights, summing the binary alternatives gives the stated binomial product. Source and target widths agree for every parameter choice, so the arbitrary width factor cancels exactly, even though width varies with the number of blocks. The central factor also cancels. The remaining ratio is a fixed positive prefactor times `(1+beta)^r`, where `beta>0`. This rules out a single finite pointwise incoming-operator bound over all safe targets for every such fixed weight assignment. Allowing additional odd-width predecessors with positive weights cannot invalidate this lower bound.

## Finite-window weights

For a window of length `d`, two changed blocks are separated by `d-1` unchanged nines. Their closest changed positions are distance `d`, so no length-`d` window can contain positions from both blocks. A four-letter block is contained in exactly `d+3` complete windows meeting it: their start positions run from `s-d+1` through `s+3`. The exterior buffers ensure that all these windows exist and contain no changed endpoint. Their all-`U` baseline is an all-nine window, so every insertion contributes the same positive factor `beta`, independent of its location and of the other insertions.

The all-`U` source differs from its target only at the first coefficient and at the coefficient preceding the central eighteen run. The first coefficient belongs to exactly one unpadded window. The second differing coefficient belongs to the windows indexed by the number `j` of trailing eighteens, namely `0<=j<=min(k,d-1)`. This gives exactly the stated endpoint product. Even with zero inserted blocks, the differing endpoint positions are distance `d`, so no complete window sees both. All other windows cancel. Hence the endpoint ratio is independent of `r`, including `r=0`, `d=1`, and the truncated end case `k<d-1`.

The independent insertion factors multiply; summing over all binary choices gives exactly `C_(d,k)*(1+beta)^r`. Strict positivity is needed for every denominator and for `beta>0`. Taking `r` arbitrarily large proves the claimed impossibility. The factorization does not require monotonicity of the potential or the width factors.

## Checker and scope

The checker constructs ordinary digit realizations, applies literal integer reversal and addition, verifies unchanged width and source/target safety, and checks its weight identities with exact integers and rational numbers. Its parameter loops match the retained report: 6,141 unbuffered controls and 1,270 buffered controls. These counts were checked from the loop bounds and record metadata; their recorded hashes were not independently regenerated here.

The conclusion applies to positive, translation-invariant, fixed finite-window products on the folded half-word with arbitrary positive width-only factors. It does not cover position-dependent or length-dependent potentials, vanishing factors, unbounded-range weights, forward contraction, or restriction to sufficiently deep actual image support. It is not a proof of a decimal Lychrel number, nor a general impossibility theorem for weighted approaches. The note states these limits accurately and attributes the prior unweighted fiber results separately.
