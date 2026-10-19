import P196.ExactSmallWidthCarryThresholds.WidthSixCandidateData

/-!
Finite coverage for the oriented width-six profiles at six observations.
There are 2 independently reduced literal obligations in this file.
The imported finite-index macro isolates each kernel decision.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

theorem exclude_b_reflected_fourth :
    ∀ i : Fin thirdB.length,
      Leaf [] ((thirdB.get i).1 ++ [(thirdB.get i).1.getD 2 0],
        (thirdB.get i).2 ++ [(thirdB.get i).2.getD 2 0]) := by
  seven_width_fin 2 =>
    decide +kernel

#print axioms exclude_b_reflected_fourth

end ExactSmallWidthCarryThresholds.WidthSixCandidates
