import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Exact neutral-band successor lengths

The unchanged Agent120 transition increases each raw block length by its
overflow bit. A checked edge therefore satisfies additive trim accounting.
-/

namespace Agent119.NeutralLengthAccounting

open Agent120.Neutral

theorem nextB_length {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    (nextB b B C).length = B.length + gam b B C := by
  rcases (by have := h.gam_le; omega : gam b B C = 0 ∨ gam b B C = 1) with h0 | h1
  · simp [nextB, h0, length_DB, length_DR]
  · simp [nextB, h1, length_DB, length_DR]

theorem nextC_length {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    (nextC b B C).length = C.length + gam b B C := by
  rcases (by have := h.gam_le; omega : gam b B C = 0 ∨ gam b B C = 1) with h0 | h1
  · simp [nextC, h0, length_DC]
  · simp [nextC, h1, length_DC]

theorem edge_lengths {b : Nat} {E : Edge} (h : edgeOK b E = true) :
    E.B2.length + E.u = E.B.length + gam b E.B E.C ∧
      E.C2.length + 2 * E.v = E.C.length + gam b E.B E.C := by
  obtain ⟨hh, hB, hC⟩ := edgeOK_sound h
  have hBl := nextB_length hh
  have hCl := nextC_length hh
  rw [hB] at hBl
  rw [hC] at hCl
  simp only [List.length_append, List.length_replicate] at hBl hCl
  constructor
  · exact hBl
  · omega

end Agent119.NeutralLengthAccounting

#print axioms Agent119.NeutralLengthAccounting.nextB_length
#print axioms Agent119.NeutralLengthAccounting.nextC_length
#print axioms Agent119.NeutralLengthAccounting.edge_lengths
