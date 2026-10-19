import P196.ExactSmallWidthCarryThresholds.WidthSixCandidateData

/-!
Finite coverage for the oriented width-six profiles at six observations.
There are 190 independently reduced literal obligations in this file.
The imported finite-index macro isolates each kernel decision.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

theorem cover_b_equal :
    ∀ i : Fin secondB.length, ∀ a : Fin 19,
      Leaf thirdB
        ((secondB.get i).1 ++ [a.val], (secondB.get i).2 ++ [a.val]) := by
  seven_width_fin 10 =>
    seven_width_fin 19 =>
      decide +kernel

#print axioms cover_b_equal

end ExactSmallWidthCarryThresholds.WidthSixCandidates
