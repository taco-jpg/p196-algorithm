import P196.ExactSmallWidthCarryThresholds.WidthSixCandidateData

/-!
Finite coverage for the oriented width-six profiles at six observations.
There are 136 independently reduced literal obligations in this file.
The imported finite-index macro isolates each kernel decision.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

theorem cover_a_minus_two :
    ∀ i : Fin firstColumns.length, ∀ a : Fin 17,
      Leaf secondA
        ((firstColumns.get i).1 ++ [a.val], (firstColumns.get i).2 ++ [a.val + 2]) := by
  seven_width_fin 8 =>
    seven_width_fin 17 =>
      decide +kernel

#print axioms cover_a_minus_two

end ExactSmallWidthCarryThresholds.WidthSixCandidates
