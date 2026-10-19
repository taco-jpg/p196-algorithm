import P196.SevenCarryMaximalWidth.CertificateTools

/-!
Complete finite coverage for the width-seven profile reduction.
There are 544 independently reduced literal obligations in this file.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SevenCarryMaximalWidth.Candidates

theorem cover_minus_two :
    ∀ i : Fin pairs.length, ∀ a : Fin 17,
      Leaf minusTwoTriples
        ((pairs.get i).1 ++ [a.val], (pairs.get i).2 ++ [a.val + 2]) := by
  seven_width_fin 32 =>
    seven_width_fin 17 =>
      decide +kernel

#print axioms cover_minus_two

end SevenCarryMaximalWidth.Candidates
