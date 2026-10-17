import Agent105DecoderLocal9df76b

set_option autoImplicit false

/-!
# Residual-five predecessor filter: the exact local nine-sum transition table

This is an incremental WIP source checkpoint for Agent #103's specific
residual-five fiber. It reuses Agent #105's original ValidEdge/decodePair
semantics and does not alter the generic decoder.

The table classifies every valid scanner edge whose two target digits sum
to nine. It is the finite arithmetic layer needed before proving the
accepted-word recurrence. No 196 reachability or exclusion claim is made.
-/

namespace Agent103.ResidualFivePredecessorFilter

open Agent105DecoderLocal9df76b

/-- Exact local transition table for a mirrored pair of digits summing to
nine. The four state bits are incoming low/high carries; the final two
fields are the outgoing low/high carries. -/
theorem validEdge_sum_nine_iff
    {u v a b : Nat} {E : Edge}
    (hsum : u + v = 9) (ha : a ≤ 1) (hb : b ≤ 1) :
    ValidEdge u v a b E ↔
      (a = 0 ∧ b = 0 ∧ u = 4 ∧ v = 5 ∧
        E.coeff = 4 ∧ E.low = 0 ∧ E.high = 1) ∨
      (a = 0 ∧ b = 1 ∧ u = 9 ∧ v = 0 ∧
        E.coeff = 9 ∧ E.low = 0 ∧ E.high = 1) ∨
      (a = 0 ∧ b = 1 ∧ u = 4 ∧ v = 5 ∧
        E.coeff = 14 ∧ E.low = 1 ∧ E.high = 1) ∨
      (a = 1 ∧ b = 1 ∧ u = 5 ∧ v = 4 ∧
        E.coeff = 14 ∧ E.low = 1 ∧ E.high = 0) ∨
      (a = 1 ∧ b = 0 ∧ u = 0 ∧ v = 9 ∧
        E.coeff = 9 ∧ E.low = 1 ∧ E.high = 0) ∨
      (a = 1 ∧ b = 0 ∧ u = 5 ∧ v = 4 ∧
        E.coeff = 4 ∧ E.low = 0 ∧ E.high = 0) := by
  cases E with
  | mk q lo hi =>
    simp only [ValidEdge]
    constructor
    · rintro ⟨hq, hlo, hhi, hleft, hright⟩
      have ha_cases : a = 0 ∨ a = 1 := by omega
      have hb_cases : b = 0 ∨ b = 1 := by omega
      have hlo_cases : lo = 0 ∨ lo = 1 := by omega
      have hhi_cases : hi = 0 ∨ hi = 1 := by omega
      rcases ha_cases with rfl | rfl <;>
        rcases hb_cases with rfl | rfl <;>
        rcases hlo_cases with rfl | rfl <;>
        rcases hhi_cases with rfl | rfl
      all_goals simp_all <;> omega
    · intro h
      rcases h with h | h | h | h | h | h
      all_goals rcases h with ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩
      all_goals decide

/-- Each transition table row is realized by the original executable
decoder, not by a replacement relation. -/
theorem decodePair_sum_nine_00 :
    decodePair 4 5 0 0 = some ⟨4, 0, 1⟩ := by
  apply decodePair_complete
  simp [ValidEdge]

theorem decodePair_sum_nine_01a :
    decodePair 9 0 0 1 = some ⟨9, 0, 1⟩ := by
  apply decodePair_complete
  simp [ValidEdge]

theorem decodePair_sum_nine_01b :
    decodePair 4 5 0 1 = some ⟨14, 1, 1⟩ := by
  apply decodePair_complete
  simp [ValidEdge]

theorem decodePair_sum_nine_11 :
    decodePair 5 4 1 1 = some ⟨14, 1, 0⟩ := by
  apply decodePair_complete
  simp [ValidEdge]

theorem decodePair_sum_nine_10a :
    decodePair 0 9 1 0 = some ⟨9, 1, 0⟩ := by
  apply decodePair_complete
  simp [ValidEdge]

theorem decodePair_sum_nine_10b :
    decodePair 5 4 1 0 = some ⟨4, 0, 0⟩ := by
  apply decodePair_complete
  simp [ValidEdge]

#print axioms validEdge_sum_nine_iff
#print axioms decodePair_sum_nine_00
#print axioms decodePair_sum_nine_01a
#print axioms decodePair_sum_nine_01b
#print axioms decodePair_sum_nine_11
#print axioms decodePair_sum_nine_10a
#print axioms decodePair_sum_nine_10b

end Agent103.ResidualFivePredecessorFilter
