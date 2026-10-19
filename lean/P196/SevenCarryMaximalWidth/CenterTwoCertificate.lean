import P196.SevenCarryMaximalWidth.CertificateTools

/-!
Complete finite coverage for the width-seven profile reduction.
There are 396 independently reduced literal obligations in this file.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SevenCarryMaximalWidth.Candidates

theorem cover_center_two :
    ∀ i : Fin minusTwoTriples.length, ∀ a : Fin 9,
      Leaf centerTwoQuadruples ((minusTwoTriples.get i).1 ++ [2 * a.val + 2],
        (minusTwoTriples.get i).2 ++ [2 * a.val]) := by
  seven_width_fin 44 =>
    seven_width_fin 9 =>
      decide +kernel

#print axioms cover_center_two

end SevenCarryMaximalWidth.Candidates
