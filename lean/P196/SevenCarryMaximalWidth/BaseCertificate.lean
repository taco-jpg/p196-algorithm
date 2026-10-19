import P196.SevenCarryMaximalWidth.CertificateTools

/-!
Complete finite coverage for the width-seven profile reduction.
There are 324 independently reduced literal obligations in this file.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SevenCarryMaximalWidth.Candidates

theorem cover_pairs :
    ∀ p : Fin 18, ∀ a : Fin 18,
      Leaf pairs ([p.val + 1, a.val + 1], [p.val + 1, a.val]) := by
  seven_width_fin 18 =>
    seven_width_fin 18 =>
      decide +kernel

#print axioms cover_pairs

end SevenCarryMaximalWidth.Candidates
