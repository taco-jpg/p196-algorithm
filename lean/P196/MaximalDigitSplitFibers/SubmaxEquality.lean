import P196.MaximalDigitSplitFibers.Gap

/-!
Agent #7. Exact equality at the sharp digit-splitting submaximum.
A single inner defect is eight or ten, with all other inner sums nine.
The profile equivalence requires at least one inner pair.
-/

namespace Agent7.MaximalDigitSplitFibers

open Agent101

/-- Exactly one inner sum is eight or ten; every other inner sum is nine. -/
def singleInnerDefect (h : List Nat) : Prop :=
  ∃ a b : List Nat, ∃ t : Nat,
    h = a ++ t :: b ∧ (t = 8 ∨ t = 10) ∧
      (∀ u ∈ a, u = 9) ∧ (∀ u ∈ b, u = 9)

theorem singleInnerDefect_nil : ¬ singleInnerDefect [] := by
  rintro ⟨a, b, t, he, _, _, _⟩
  have hl := congrArg List.length he
  simp only [List.length_nil, List.length_append, List.length_cons] at hl
  omega

theorem singleInnerDefect_cons (s : Nat) (h : List Nat) :
    singleInnerDefect (s :: h) ↔
      ((s = 8 ∨ s = 10) ∧ ∀ t ∈ h, t = 9) ∨
        (s = 9 ∧ singleInnerDefect h) := by
  constructor
  · rintro ⟨a, b, t, he, ht, ha, hb⟩
    cases a with
    | nil =>
      have he' : s = t ∧ h = b := by simpa using he
      rcases he' with ⟨rfl, rfl⟩
      exact Or.inl ⟨ht, hb⟩
    | cons u a =>
      have he' : s = u ∧ h = a ++ t :: b := by simpa using he
      rcases he' with ⟨rfl, he'⟩
      apply Or.inr
      refine ⟨ha s (by simp), a, b, t, he', ht, ?_, hb⟩
      intro v hv
      exact ha v (by simp [hv])
  · rintro (⟨hs, hh⟩ | ⟨hs, hh⟩)
    · exact ⟨[], h, s, rfl, hs, by simp, hh⟩
    · rcases hh with ⟨a, b, t, he, ht, ha, hb⟩
      refine ⟨s :: a, b, t, ?_, ht, ?_, hb⟩
      · exact congrArg (fun xs : List Nat => s :: xs) he
      · intro u hu
        rcases List.mem_cons.mp hu with rfl | hu
        · exact hs
        · exact ha u hu

theorem pairCount_inner_eq_nine_iff (s : Nat) :
    pairCount false s = 9 ↔ s = 8 ∨ s = 10 := by
  by_cases h9 : s ≤ 9 <;> by_cases h18 : s ≤ 18 <;>
    simp [pairCount, h9, h18] <;> omega

theorem pairProduct_submax_iff (h : List Nat) :
    natProduct (h.map (pairCount false)) = 9 * 10 ^ (h.length - 1) ↔
      singleInnerDefect h := by
  induction h with
  | nil =>
    constructor
    · intro he
      simp [natProduct] at he
    · intro he
      exact False.elim (singleInnerDefect_nil he)
  | cons s h ih =>
    change pairCount false s * natProduct (h.map (pairCount false)) =
      9 * 10 ^ h.length ↔ singleInnerDefect (s :: h)
    rw [singleInnerDefect_cons]
    constructor
    · intro he
      have hs := pairCount_inner_le s
      have hp := pairProduct_le h
      have hpos : 0 < 10 ^ h.length := Nat.pow_pos (by decide)
      have hsge : 9 ≤ pairCount false s := by
        by_cases hsge : 9 ≤ pairCount false s
        · exact hsge
        · have hs8 : pairCount false s ≤ 8 := by omega
          have hb := Nat.mul_le_mul hs8 hp
          omega
      have hsCases : pairCount false s = 9 ∨ pairCount false s = 10 := by
        omega
      rcases hsCases with hs9 | hs10
      · rw [hs9] at he
        have hh : natProduct (h.map (pairCount false)) = 10 ^ h.length := by
          omega
        exact Or.inl ⟨(pairCount_inner_eq_nine_iff s).mp hs9,
          (pairProduct_eq_pow_iff h).mp hh⟩
      · rw [hs10] at he
        have hlen : 0 < h.length := by
          cases h with
          | nil => simp [natProduct] at he
          | cons t h => simp
        have hp : 10 ^ h.length = 10 ^ (h.length - 1) * 10 := by
          have hl : (h.length - 1).succ = h.length := by omega
          simpa only [hl] using Nat.pow_succ 10 (h.length - 1)
        rw [hp] at he
        have hh : natProduct (h.map (pairCount false)) =
            9 * 10 ^ (h.length - 1) := by omega
        exact Or.inr ⟨(pairCount_inner_eq_ten_iff s).mp hs10, ih.mp hh⟩
    · rintro (⟨hs, hh⟩ | ⟨hs, hh⟩)
      · rw [(pairCount_inner_eq_nine_iff s).mpr hs,
          (pairProduct_eq_pow_iff h).mpr hh]
      · have hs10 : pairCount false s = 10 :=
          (pairCount_inner_eq_ten_iff s).mpr hs
        have hlen : 0 < h.length := by
          cases h with
          | nil => exact False.elim (singleInnerDefect_nil hh)
          | cons t h => simp
        have hp : 10 ^ h.length = 10 ^ (h.length - 1) * 10 := by
          have hl : (h.length - 1).succ = h.length := by omega
          simpa only [hl] using Nat.pow_succ 10 (h.length - 1)
        rw [hs10, ih.mpr hh, hp]
        omega

theorem profileCount_submax_iff (s : Nat) (h : List Nat) (c : Option Nat)
    (hlen : 0 < h.length) :
    profileCount (s :: h) c = 81 * 10 ^ (h.length - 1) ↔
      (s = 9 ∨ s = 10) ∧ singleInnerDefect h ∧ centerCount c = 1 := by
  have ha : pairCount true s * centerCount c ≤ 9 := by
    simpa using Nat.mul_le_mul (pairCount_outer_le s) (centerCount_le c)
  have hp := pairProduct_le h
  have hpow : 10 ^ h.length = 10 ^ (h.length - 1) * 10 := by
    have hl : (h.length - 1).succ = h.length := by omega
    simpa only [hl] using Nat.pow_succ 10 (h.length - 1)
  have hpos : 0 < 10 ^ (h.length - 1) := Nat.pow_pos (by decide)
  constructor
  · intro he
    change (pairCount true s * centerCount c) *
      natProduct (h.map (pairCount false)) = 81 * 10 ^ (h.length - 1) at he
    have ha9 : pairCount true s * centerCount c = 9 := by
      by_cases ha9 : pairCount true s * centerCount c = 9
      · exact ha9
      · have ha8 : pairCount true s * centerCount c ≤ 8 := by omega
        have hb := Nat.mul_le_mul ha8 hp
        rw [hpow] at hb
        omega
    rw [ha9] at he
    have hh : natProduct (h.map (pairCount false)) =
        9 * 10 ^ (h.length - 1) := by omega
    obtain ⟨hs, hc⟩ := (outerCenter_eq_nine_iff s c).mp ha9
    exact ⟨hs, (pairProduct_submax_iff h).mp hh, hc⟩
  · rintro ⟨hs, hh, hc⟩
    change (pairCount true s * centerCount c) *
      natProduct (h.map (pairCount false)) = 81 * 10 ^ (h.length - 1)
    rw [(outerCenter_eq_nine_iff s c).mpr ⟨hs, hc⟩,
      (pairProduct_submax_iff h).mpr hh]
    omega

#print axioms singleInnerDefect
#print axioms singleInnerDefect_nil
#print axioms singleInnerDefect_cons
#print axioms pairCount_inner_eq_nine_iff
#print axioms pairProduct_submax_iff
#print axioms profileCount_submax_iff

end Agent7.MaximalDigitSplitFibers
