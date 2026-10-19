import P196.ExactSmallWidthCarryThresholds.WidthSixCandidateData

/-!
Finite coverage for the oriented width-six profiles at six observations.
There are 396 independently reduced literal obligations in this file.
The imported finite-index macro isolates each kernel decision.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

theorem cover_a_plus_one :
    ∀ i : Fin secondA.length, ∀ a : Fin 18,
      Leaf thirdA
        ((secondA.get i).1 ++ [a.val + 1], (secondA.get i).2 ++ [a.val]) := by
  seven_width_fin 22 =>
    seven_width_fin 18 =>
      decide +kernel

#print axioms cover_a_plus_one

end ExactSmallWidthCarryThresholds.WidthSixCandidates
