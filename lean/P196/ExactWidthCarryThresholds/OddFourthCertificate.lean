import P196.ExactWidthCarryThresholds.WidthTenCandidateData

/-!
One-sided finite coverage for the oriented width-ten profile.
The 352 new literal obligations use the imported seven-observation checker
and finite-index macro. Each leaf is reduced separately by the kernel.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactWidthCarryThresholds.WidthTenCandidates

open SevenCarryMaximalWidth.Candidates

theorem cover_odd_fourth :
    ∀ i : Fin minusTwoTriples.length, ∀ a : Fin 8,
      Leaf oddFourthQuadruples
        ((minusTwoTriples.get i).1 ++ [2 * a.val + 3],
          (minusTwoTriples.get i).2 ++ [2 * a.val + 1]) := by
  seven_width_fin 44 =>
    seven_width_fin 8 =>
      decide +kernel

#print axioms cover_odd_fourth

end ExactWidthCarryThresholds.WidthTenCandidates
