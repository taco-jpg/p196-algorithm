# Actual maximal-run population renewal (Agent 7)

## Status

WIP after the guarded claim `2e1744f4ddc991559fb906a90be7a8e04949bc3a`. This first checkpoint preserves the exact scope, independent source scouts and original dependency provenance. It does not certify the planned new theorems. Compilation and review results will be recorded separately as they actually complete.

## Mathematical target

For an original `FoldedDecimal.Admissible L q` and fixed extreme coefficient `c = 0` or `c = 18`, partition every maximal run in the actual successor into a newly born run or the exact nonempty descendant of one unique old maximal run. A newly born interval `[a,b)` must satisfy `L ≤ i ∨ q i ≠ c` for each of its indices. This physical-width guard matters because the original coefficient function has arbitrary values outside its finite word.

Following this partition backward should assign every later maximal run a unique founder interval and state time. A birth at transition `s` belongs to state `s+1`. Uniqueness concerns the maximal interval, not a position inside it.

The planned quantitative consequence is: if all initial maximal `c`-runs have length at most `R`, no run is born in the next `t` transitions, and `4*R+1 ≤ t`, the final word has no physical coefficient `c`. Restarting the actual orbit should then prove that eventual absence of births is equivalent to eventual absence of the coefficient; equivalently, arbitrarily late occurrences are equivalent to arbitrarily late births. A common bound handles both extremes. Ordinary-integer meaning is retained through the original canonical representation theorem.

## Reused results and limits

The original `RunAncestry.descendant_step` already gives exact surviving intervals, maximality, containment and absence of merging. `RunAncestry.extinct_uniform` already bounds the lifetime of one initial run. These results are consumed unchanged, along with `iterPairs_admissible`, the existing `ActualHighReturn.iterPairs_add` restart identity, and `iterPairs_representation`. Their statements and provenance remain attributed to the original sources. This contribution owns only the population coverage and its stated temporal consequences.

No theorem here asserts that births eventually cease for any particular orbit. There is no conclusion about the 196 orbit, infinite palindrome avoidance, an improved lifetime potential, population mass or growth rate, or numerical inverse fibers.

## Work split and verification

`gap_inventory` authors `MaximalIntervals.lean` and `RunOrigins.lean`; `odd_counts` authors `RunFounders.lean`; parent `/root` authors `RunRenewal.lean` and `RunRenewalInteger.lean` and is the sole Git writer. The genuine runtime specialist remains a nonauthor of these modules and performs independent semantic/execution review. This is a same-team review, not an unaffiliated external identity.

The selected dependency closure contains ten unchanged original modules and official Lean 4.19.0 `Std`. Source pins, actual commands, failed attempts, successful logs, public theorem audits and complete module-origin axiom inventories will be preserved. Accepted theorem dependencies are restricted to `propext`, `Classical.choice` and `Quot.sound`; compiler implementation constants must be inventoried separately and absent from theorem dependencies.

The isolated branch starts at `755b25cdf6b5e5eb811a9555ffbdc2fdd4c1271e`. Direct user authorization for isolated contribution branches controls this research publication; the single designated main integrator retains the integration role. This task holds no main slot.

