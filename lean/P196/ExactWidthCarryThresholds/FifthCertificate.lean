import P196.ExactWidthCarryThresholds.WidthTenCandidateData

/-!
One-sided finite coverage for the oriented width-ten profile.
The 504 new literal obligations use the imported seven-observation checker
and finite-index macro. Each leaf is reduced separately by the kernel.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactWidthCarryThresholds.WidthTenCandidates

open SevenCarryMaximalWidth.Candidates

theorem cover_fifth :
    ∀ i : Fin quadruples.length, ∀ a : Fin 18,
      Leaf quintuples
        ((quadruples.get i).1 ++ [a.val], (quadruples.get i).2 ++ [a.val + 1]) := by
  seven_width_fin 28 =>
    seven_width_fin 18 =>
      decide +kernel

#print axioms cover_fifth

end ExactWidthCarryThresholds.WidthTenCandidates
