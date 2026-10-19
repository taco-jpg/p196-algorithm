import P196.SevenCarryMaximalWidth.CertificateTools

/-!
Complete finite coverage for the width-seven profile reduction.
There are 512 independently reduced literal obligations in this file.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SevenCarryMaximalWidth.Candidates

theorem cover_minus_three :
    ∀ i : Fin pairs.length, ∀ a : Fin 16,
      Leaf minusThreeTriples
        ((pairs.get i).1 ++ [a.val], (pairs.get i).2 ++ [a.val + 3]) := by
  seven_width_fin 32 =>
    certify_fin16

#print axioms cover_minus_three

end SevenCarryMaximalWidth.Candidates
