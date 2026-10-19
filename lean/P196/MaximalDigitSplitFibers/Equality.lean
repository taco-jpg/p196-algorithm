import P196.Agent101DigitSplit.Agent101MultiplicityBounds

/-!
Agent #7. Exact equality in the established digit-splitting maximum.
All counts and the original upper bounds are imported unchanged.
-/

namespace Agent7.MaximalDigitSplitFibers

open Agent101

theorem pairCount_outer_eq_nine_iff (s : Nat) :
    pairCount true s = 9 ↔ s = 9 ∨ s = 10 := by
  by_cases h9 : s ≤ 9 <;> by_cases h18 : s ≤ 18 <;>
    simp [pairCount, h9, h18] <;> omega

theorem pairCount_inner_eq_ten_iff (s : Nat) :
    pairCount false s = 10 ↔ s = 9 := by
  by_cases h9 : s ≤ 9 <;> by_cases h18 : s ≤ 18 <;>
    simp [pairCount, h9, h18] <;> omega

theorem pairProduct_eq_pow_iff (h : List Nat) :
    natProduct (h.map (pairCount false)) = 10 ^ h.length ↔
      ∀ t ∈ h, t = 9 := by
  induction h with
  | nil => simp [natProduct]
  | cons s h ih =>
    constructor
    · intro he
      change pairCount false s * natProduct (h.map (pairCount false)) =
        10 ^ (h.length + 1) at he
      rw [Nat.pow_succ] at he
      have hp := pairProduct_le h
      have hs := pairCount_inner_le s
      have hpos : 0 < 10 ^ h.length := Nat.pow_pos (by decide)
      have hs10 : pairCount false s = 10 := by
        by_cases hs10 : pairCount false s = 10
        · exact hs10
        · have hs9 : pairCount false s ≤ 9 := by omega
          have hb := Nat.mul_le_mul hs9 hp
          omega
      rw [hs10] at he
      have hh : natProduct (h.map (pairCount false)) = 10 ^ h.length := by
        omega
      have hs9 := (pairCount_inner_eq_ten_iff s).mp hs10
      have hh9 := ih.mp hh
      intro t ht
      rcases List.mem_cons.mp ht with rfl | ht
      · exact hs9
      · exact hh9 t ht
    · intro hh
      have hs : s = 9 := hh s (by simp)
      have ht : ∀ t ∈ h, t = 9 := by
        intro t ht
        exact hh t (by simp [ht])
      have hp := ih.mpr ht
      simp [hs, List.map_cons, natProduct, pairCount, hp,
        Nat.pow_succ, Nat.mul_comm]

theorem outerCenter_eq_nine_iff (s : Nat) (c : Option Nat) :
    pairCount true s * centerCount c = 9 ↔
      (s = 9 ∨ s = 10) ∧ centerCount c = 1 := by
  constructor
  · intro he
    have hc := centerCount_le c
    have hc1 : centerCount c = 1 := by
      by_cases hc1 : centerCount c = 1
      · exact hc1
      · have hc0 : centerCount c = 0 := by omega
        simp [hc0] at he
    have hs : pairCount true s = 9 := by simpa [hc1] using he
    exact ⟨(pairCount_outer_eq_nine_iff s).mp hs, hc1⟩
  · rintro ⟨hs, hc⟩
    rw [hc, Nat.mul_one]
    exact (pairCount_outer_eq_nine_iff s).mpr hs

theorem profileCount_max_iff (s : Nat) (h : List Nat) (c : Option Nat) :
    profileCount (s :: h) c = 9 * 10 ^ h.length ↔
      (s = 9 ∨ s = 10) ∧ (∀ t ∈ h, t = 9) ∧ centerCount c = 1 := by
  have ha : pairCount true s * centerCount c ≤ 9 := by
    simpa using Nat.mul_le_mul (pairCount_outer_le s) (centerCount_le c)
  have hp := pairProduct_le h
  have hpos : 0 < 10 ^ h.length := Nat.pow_pos (by decide)
  constructor
  · intro he
    change (pairCount true s * centerCount c) *
      natProduct (h.map (pairCount false)) = 9 * 10 ^ h.length at he
    have ha9 : pairCount true s * centerCount c = 9 := by
      by_cases ha9 : pairCount true s * centerCount c = 9
      · exact ha9
      · have ha8 : pairCount true s * centerCount c ≤ 8 := by omega
        have hb := Nat.mul_le_mul ha8 hp
        omega
    rw [ha9] at he
    have hh : natProduct (h.map (pairCount false)) = 10 ^ h.length := by
      omega
    obtain ⟨hs, hc⟩ := (outerCenter_eq_nine_iff s c).mp ha9
    exact ⟨hs, (pairProduct_eq_pow_iff h).mp hh, hc⟩
  · rintro ⟨hs, hh, hc⟩
    change (pairCount true s * centerCount c) *
      natProduct (h.map (pairCount false)) = 9 * 10 ^ h.length
    rw [(outerCenter_eq_nine_iff s c).mpr ⟨hs, hc⟩,
      (pairProduct_eq_pow_iff h).mpr hh]

#print axioms pairCount_outer_eq_nine_iff
#print axioms pairCount_inner_eq_ten_iff
#print axioms pairProduct_eq_pow_iff
#print axioms outerCenter_eq_nine_iff
#print axioms profileCount_max_iff

end Agent7.MaximalDigitSplitFibers
