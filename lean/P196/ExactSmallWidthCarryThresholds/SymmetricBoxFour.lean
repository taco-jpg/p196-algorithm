import P196.Agent10EightCarry.DifferenceObservability

/-!
Symmetric integer series of widths four and six under a fourth-smoothing
bound of [-4, 4]. Width four is rigid. At width six, two explicit profiles
and their negatives are the only possible nonzero series. No input bound,
minimal-support assumption, or center-parity assumption is used.
-/

namespace ExactSmallWidthCarryThresholds

open DifferenceObservability

/-- The first zero-extended width-six profile. -/
def core_six_a (i : Nat) : Int :=
  if i = 0 then 1 else if i = 1 then -2 else if i = 2 then 1
  else if i = 3 then 1 else if i = 4 then -2 else if i = 5 then 1 else 0

/-- The second zero-extended width-six profile. -/
def core_six_b (i : Nat) : Int :=
  if i = 0 then 1 else if i = 1 then -1 else if i = 2 then 0
  else if i = 3 then 0 else if i = 4 then -1 else if i = 5 then 1 else 0

private theorem core_six_tails (i : Nat) (hi : 6 ≤ i) :
    core_six_a i = 0 ∧ core_six_b i = 0 := by
  have h0 : i ≠ 0 := by omega
  have h1 : i ≠ 1 := by omega
  have h2 : i ≠ 2 := by omega
  have h3 : i ≠ 3 := by omega
  have h4 : i ≠ 4 := by omega
  have h5 : i ≠ 5 := by omega
  simp [core_six_a, core_six_b, h0, h1, h2, h3, h4, h5]

/-- Symmetric width four is rigid under the fourth-smoothing bound [-4, 4]. -/
theorem smooth_four_box_four_width_four_rigidity
    (f : Series)
    (hz : ∀ i, 4 ≤ i → f i = 0)
    (hs : ∀ i, i < 4 → f i = f (4 - 1 - i))
    (hg : ∀ i, -4 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 4) :
    ∀ i, f i = 0 := by
  have hf2 : f 2 = f 1 := by simpa using hs 2 (by decide)
  have hf3 : f 3 = f 0 := by simpa using hs 3 (by decide)
  have h2 := hg 2
  have h3 := hg 3
  simp [smoothPow, smooth, hf2, hf3] at h2 h3
  have hm : f 0 + 2 * f 1 = 0 := by omega
  have hf01 : f 0 = 0 ∧ f 1 = 0 := by omega
  intro i
  by_cases hi : i < 4
  · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by omega
    rcases hiCases with rfl | rfl | rfl | rfl <;>
      simp [hf2, hf3, hf01.1, hf01.2]
  · exact hz i (by omega)

/-- At width six the fourth-smoothing constraints force one of two profiles,
scaled by a coefficient in {-1, 0, 1}. -/
theorem smooth_four_box_four_width_six_classification
    (f : Series)
    (hz : ∀ i, 6 ≤ i → f i = 0)
    (hs : ∀ i, i < 6 → f i = f (6 - 1 - i))
    (hg : ∀ i, -4 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 4) :
    (-1 ≤ f 0 ∧ f 0 ≤ 1) ∧
      ((∀ i, f i = f 0 * core_six_a i) ∨
        (∀ i, f i = f 0 * core_six_b i)) := by
  have hf3 : f 3 = f 2 := by simpa using hs 3 (by decide)
  have hf4 : f 4 = f 1 := by simpa using hs 4 (by decide)
  have hf5 : f 5 = f 0 := by simpa using hs 5 (by decide)
  have h1 := hg 1
  have h2 := hg 2
  have h3 := hg 3
  have h4 := hg 4
  simp [smoothPow, smooth, hf3, hf4] at h1 h2 h3 h4
  have ha : -1 ≤ f 0 ∧ f 0 ≤ 1 := by omega
  have hab : -1 ≤ f 0 + f 1 ∧ f 0 + f 1 ≤ 1 := by omega
  have habc :
      (f 1 = -2 * f 0 ∧ f 2 = f 0) ∨
      (f 1 = -f 0 ∧ f 2 = 0) := by
    have hsign : f 0 = -1 ∨ f 0 = 0 ∨ f 0 = 1 := by omega
    rcases hsign with hsign | hsign | hsign <;> omega
  refine ⟨ha, ?_⟩
  rcases habc with h | h
  · left
    intro i
    by_cases hi : i < 6
    · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
      rcases hiCases with rfl | rfl | rfl | rfl | rfl | rfl <;>
        simp [core_six_a, hf3, hf4, hf5] <;> omega
    · rw [hz i (by omega), (core_six_tails i (by omega)).1]
      simp
  · right
    intro i
    by_cases hi : i < 6
    · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
      rcases hiCases with rfl | rfl | rfl | rfl | rfl | rfl <;>
        simp [core_six_b, hf3, hf4, hf5] <;> omega
    · rw [hz i (by omega), (core_six_tails i (by omega)).2]
      simp

#print axioms smooth_four_box_four_width_four_rigidity
#print axioms smooth_four_box_four_width_six_classification

end ExactSmallWidthCarryThresholds
