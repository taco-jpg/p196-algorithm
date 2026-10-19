import P196.EightCarryMaximalWidth.CertificateTools

/-! Agent #10: complete initial triples with exterior coefficient 18.
Every literal start is a separate kernel-checked decision leaf, keeping
reduction memory independent of the number of starts in this file. -/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem starts_p18 : covered (startsAt 18) (triplesAt 18) = true := by
  certify_starts

#print axioms starts_p18

end EightCarryMaximalWidth.Candidates
