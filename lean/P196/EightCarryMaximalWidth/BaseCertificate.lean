import P196.EightCarryMaximalWidth.Base01
import P196.EightCarryMaximalWidth.Base02
import P196.EightCarryMaximalWidth.Base03
import P196.EightCarryMaximalWidth.Base04
import P196.EightCarryMaximalWidth.Base05
import P196.EightCarryMaximalWidth.Base06
import P196.EightCarryMaximalWidth.Base07
import P196.EightCarryMaximalWidth.Base08
import P196.EightCarryMaximalWidth.Base09
import P196.EightCarryMaximalWidth.Base10
import P196.EightCarryMaximalWidth.Base11
import P196.EightCarryMaximalWidth.Base12
import P196.EightCarryMaximalWidth.Base13
import P196.EightCarryMaximalWidth.Base14
import P196.EightCarryMaximalWidth.Base15
import P196.EightCarryMaximalWidth.Base16
import P196.EightCarryMaximalWidth.Base17
import P196.EightCarryMaximalWidth.Base18

/-!
Agent #10: combine the eighteen independently checked exterior rows.
Together they cover every one of the 6,156 admissible initial triples
with difference (0,0,1), retaining all possible eight-observation survivors.
-/

namespace EightCarryMaximalWidth.Candidates

theorem startsAt_cover (p : Nat) (hp : 1 ≤ p) (hp' : p ≤ 18) :
    covered (startsAt p) (triplesAt p) = true := by
  have hcases : p = 1 ∨ p = 2 ∨ p = 3 ∨ p = 4 ∨ p = 5 ∨ p = 6 ∨ p = 7 ∨ p = 8 ∨ p = 9 ∨ p = 10 ∨ p = 11 ∨ p = 12 ∨ p = 13 ∨ p = 14 ∨ p = 15 ∨ p = 16 ∨ p = 17 ∨ p = 18 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact starts_p1
  · exact starts_p2
  · exact starts_p3
  · exact starts_p4
  · exact starts_p5
  · exact starts_p6
  · exact starts_p7
  · exact starts_p8
  · exact starts_p9
  · exact starts_p10
  · exact starts_p11
  · exact starts_p12
  · exact starts_p13
  · exact starts_p14
  · exact starts_p15
  · exact starts_p16
  · exact starts_p17
  · exact starts_p18

#print axioms startsAt_cover

end EightCarryMaximalWidth.Candidates
