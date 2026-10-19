import P196.ExactSmallWidthCarryThresholds.WidthSixCandidateData

/-!
Finite coverage for the oriented width-six profiles at six observations.
There are 23 independently reduced literal obligations in this file.
The imported finite-index macro isolates each kernel decision.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

theorem exclude_a_reflected_fourth :
    ∀ i : Fin thirdA.length,
      Leaf [] ((thirdA.get i).1 ++ [(thirdA.get i).1.getD 2 0],
        (thirdA.get i).2 ++ [(thirdA.get i).2.getD 2 0]) := by
  seven_width_fin 23 =>
    decide +kernel

#print axioms exclude_a_reflected_fourth

end ExactSmallWidthCarryThresholds.WidthSixCandidates
