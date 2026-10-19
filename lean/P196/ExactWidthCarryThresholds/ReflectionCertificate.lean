import P196.ExactWidthCarryThresholds.WidthTenCandidateData

/-!
One-sided finite coverage for the oriented width-ten profile.
The 37 new literal obligations use the imported seven-observation checker
and finite-index macro. Each leaf is reduced separately by the kernel.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactWidthCarryThresholds.WidthTenCandidates

open SevenCarryMaximalWidth.Candidates

theorem exclude_reflected_sixth :
    ∀ i : Fin quintuples.length,
      Leaf [] ((quintuples.get i).1 ++ [(quintuples.get i).1.getD 4 0],
        (quintuples.get i).2 ++ [(quintuples.get i).2.getD 4 0]) := by
  seven_width_fin 37 =>
    decide +kernel

#print axioms exclude_reflected_sixth

end ExactWidthCarryThresholds.WidthTenCandidates
