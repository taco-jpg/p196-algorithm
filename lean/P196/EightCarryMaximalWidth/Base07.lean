import P196.EightCarryMaximalWidth.CertificateTools

/-! Agent #10: complete initial triples with exterior coefficient 7.
Every literal start is a separate kernel-checked decision leaf, keeping
reduction memory independent of the number of starts in this file. -/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem starts_p7 : covered (startsAt 7) (triplesAt 7) = true := by
  certify_starts

#print axioms starts_p7

end EightCarryMaximalWidth.Candidates
