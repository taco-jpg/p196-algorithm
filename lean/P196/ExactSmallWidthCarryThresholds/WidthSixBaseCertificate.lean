import P196.ExactSmallWidthCarryThresholds.WidthSixCandidateData

/-!
Finite coverage for the oriented width-six profiles at six observations.
There are 17 independently reduced literal obligations in this file.
The imported finite-index macro isolates each kernel decision.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

theorem cover_first_columns :
    ∀ a : Fin 17,
      Leaf firstColumns ([a.val + 2], [a.val + 1]) := by
  seven_width_fin 17 =>
    decide +kernel

#print axioms cover_first_columns

end ExactSmallWidthCarryThresholds.WidthSixCandidates
