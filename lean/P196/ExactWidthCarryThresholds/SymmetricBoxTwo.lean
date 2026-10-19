import P196.Agent10EightCarry.DifferenceObservability

/-!
Symmetric integer series of width eight whose fourth smoothing lies in
[-2, 2]. The constraints force a scalar multiple of one explicit core,
with scalar in {-1, 0, 1}. No input coefficient bound is assumed.
-/

namespace ExactWidthCarryThresholds

open DifferenceObservability

/-- The zero-extended width-eight core. -/
def core_eight (i : Nat) : Int :=
  if i = 0 then 1 else if i = 1 then -2 else if i = 2 then 2
  else if i = 3 then -1 else if i = 4 then -1 else if i = 5 then 2
  else if i = 6 then -2 else if i = 7 then 1 else 0

private theorem core_eight_tail (i : Nat) (hi : 8 ≤ i) : core_eight i = 0 := by
  have h0 : i ≠ 0 := by omega
  have h1 : i ≠ 1 := by omega
  have h2 : i ≠ 2 := by omega
  have h3 : i ≠ 3 := by omega
  have h4 : i ≠ 4 := by omega
  have h5 : i ≠ 5 := by omega
  have h6 : i ≠ 6 := by omega
  have h7 : i ≠ 7 := by omega
  simp [core_eight, h0, h1, h2, h3, h4, h5, h6, h7]

/-- The fourth-smoothing bound [-2, 2] forces a symmetric width-eight
series to be zero or one of the two signs of `core_eight`. -/
theorem smooth_four_box_two_width_eight_classification
    (f : Series)
    (hz : ∀ i, 8 ≤ i → f i = 0)
    (hs : ∀ i, i < 8 → f i = f (8 - 1 - i))
    (hg : ∀ i, -2 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 2) :
    (-1 ≤ f 0 ∧ f 0 ≤ 1) ∧ ∀ i, f i = f 0 * core_eight i := by
  have hf4 : f 4 = f 3 := by simpa using hs 4 (by decide)
  have hf5 : f 5 = f 2 := by simpa using hs 5 (by decide)
  have hf6 : f 6 = f 1 := by simpa using hs 6 (by decide)
  have hf7 : f 7 = f 0 := by simpa using hs 7 (by decide)
  have h1 := hg 1
  have h2 := hg 2
  have h3 := hg 3
  have h4 := hg 4
  have h5 := hg 5
  simp [smoothPow, smooth, hf4, hf5] at h1 h2 h3 h4 h5
  have ha : -1 ≤ f 0 ∧ f 0 ≤ 1 := by omega
  have habcd : f 1 = -2 * f 0 ∧ f 2 = 2 * f 0 ∧ f 3 = -f 0 := by
    have hsign : f 0 = -1 ∨ f 0 = 0 ∨ f 0 = 1 := by omega
    rcases hsign with hsign | hsign | hsign <;> omega
  refine ⟨ha, ?_⟩
  intro i
  by_cases hi : i < 8
  · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨
        i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 := by omega
    rcases hiCases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [core_eight, hf4, hf5, hf6, hf7] <;> omega
  · rw [hz i (by omega), core_eight_tail i (by omega)]
    simp

#print axioms smooth_four_box_two_width_eight_classification

end ExactWidthCarryThresholds
