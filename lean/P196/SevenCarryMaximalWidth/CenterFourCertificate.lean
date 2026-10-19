import P196.SevenCarryMaximalWidth.CertificateTools

/-!
Complete finite coverage for the width-seven profile reduction.
There are 296 independently reduced literal obligations in this file.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SevenCarryMaximalWidth.Candidates

theorem exclude_center_four :
    ∀ i : Fin minusThreeTriples.length, ∀ a : Fin 8,
      Leaf [] ((minusThreeTriples.get i).1 ++ [2 * a.val + 4],
        (minusThreeTriples.get i).2 ++ [2 * a.val]) := by
  seven_width_fin 37 =>
    seven_width_fin 8 =>
      decide +kernel

#print axioms exclude_center_four

end SevenCarryMaximalWidth.Candidates
