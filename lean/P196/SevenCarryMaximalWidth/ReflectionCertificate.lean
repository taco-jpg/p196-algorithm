import P196.SevenCarryMaximalWidth.CertificateTools

/-!
Complete finite coverage for the width-seven profile reduction.
There are 15 independently reduced literal obligations in this file.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SevenCarryMaximalWidth.Candidates

theorem exclude_reflected_fifth :
    ∀ i : Fin centerTwoQuadruples.length,
      Leaf [] ((centerTwoQuadruples.get i).1 ++ [(centerTwoQuadruples.get i).1.getD 2 0],
        (centerTwoQuadruples.get i).2 ++ [(centerTwoQuadruples.get i).2.getD 2 0]) := by
  seven_width_fin 15 =>
    decide +kernel

#print axioms exclude_reflected_fifth

end SevenCarryMaximalWidth.Candidates
