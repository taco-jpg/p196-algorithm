# AA48 target: T12 cut/insertion formalisation

Status: PARTIAL / UNDECIDED. No theorem has been Lean-checked by this agent.

## Exact target

Formalise the T12 cut/insertion reduction for a rooted decimal p12/m9 template. For a fixed candidate triple (J,C,U), prove that any alleged all-width return can be reduced to the reference instance (q,k)=(14,100), with the hypotheses and conclusion stated precisely enough to invoke the existing R12 J40 / R13 J17 non-return results. The reduction must preserve the actual decimal reverse-and-add semantics, clock phase, root, seam, centre parity, and the independently varying exponents; it must not silently discard even-length palindromic centres.

The intended implication has the shape

`UniformReturn(J,C,U) -> ReferenceReturn(J,C,U,14,100)`

where `UniformReturn` means the complete 120 ordinary decimal reverse-and-add steps take the same rooted template family `P(q,k;J,U,C)` to `P(q,k+5;J,U,C)` for every admissible q,k beyond the stated bound, with W9 exponent q fixed and every intermediate phase guarded. `ReferenceReturn` must be a concrete statement about the canonical integer represented by the template, not merely a coefficient-word transition.

## Constraints from the current project brief

- Use the parity-complete mod-11 gate: even-length palindromic C is not pruned by the mod-11 condition.
- The one-epoch seam failures and finite-horizon replays are not certificates.
- The known T12 cut/insertion reduction and census reduction to (14,100) are the assigned route; do not repeat the pi141 cocycle or pi179 SCC dichotomy.
- A successful result must compile in Lean without `sorry`, and must identify exactly which hypotheses are needed by the reference-width contradiction.

## Verification boundary

At the time of writing, the GitHub read API is rate-limited, so the current Lean declarations and latest #475 FEED lines could not be inspected. No declaration names or compilation results are guessed here. This file is a target specification only, not a proof or a result.
