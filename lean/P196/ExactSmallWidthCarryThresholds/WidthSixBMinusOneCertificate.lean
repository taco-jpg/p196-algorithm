import P196.ExactSmallWidthCarryThresholds.WidthSixCandidateData

/-!
Finite coverage for the oriented width-six profiles at six observations.
There are 144 independently reduced literal obligations in this file.
The imported finite-index macro isolates each kernel decision.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

theorem cover_b_minus_one :
    ∀ i : Fin firstColumns.length, ∀ a : Fin 18,
      Leaf secondB
        ((firstColumns.get i).1 ++ [a.val], (firstColumns.get i).2 ++ [a.val + 1]) := by
  seven_width_fin 8 =>
    seven_width_fin 18 =>
      decide +kernel

#print axioms cover_b_minus_one

end ExactSmallWidthCarryThresholds.WidthSixCandidates
