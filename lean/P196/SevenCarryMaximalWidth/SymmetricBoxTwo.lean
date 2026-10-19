import P196.Agent10EightCarry.DifferenceObservability

/-!
Short symmetric integer series whose fourth smoothing lies in [-2, 2].
No bound on the input coefficients and no center-parity assumption is needed.
Widths at most four and width six are rigid. At width five, the only
nonzero possibilities are two explicit profiles and their negatives.
-/

namespace SevenCarryMaximalWidth

open DifferenceObservability

/-- The first zero-extended width-five profile. -/
def core_five_a (i : Nat) : Int :=
  if i = 0 then 1 else if i = 1 then -3 else if i = 2 then 4
  else if i = 3 then -3 else if i = 4 then 1 else 0

/-- The second zero-extended width-five profile. -/
def core_five_b (i : Nat) : Int :=
  if i = 0 then 1 else if i = 1 then -2 else if i = 2 then 2
  else if i = 3 then -2 else if i = 4 then 1 else 0

private theorem core_five_tails (i : Nat) (hi : 5 ≤ i) :
    core_five_a i = 0 ∧ core_five_b i = 0 := by
  have h0 : i ≠ 0 := by omega
  have h1 : i ≠ 1 := by omega
  have h2 : i ≠ 2 := by omega
  have h3 : i ≠ 3 := by omega
  have h4 : i ≠ 4 := by omega
  simp [core_five_a, core_five_b, h0, h1, h2, h3, h4]

/-- Symmetric widths at most four cannot support a nonzero integer series
whose fourth smoothing lies in [-2, 2]. -/
theorem smooth_four_box_two_width_le_four
    (f : Series) (R : Nat) (hR : R ≤ 4)
    (hz : ∀ i, R ≤ i → f i = 0)
    (hs : ∀ i, i < R → f i = f (R - 1 - i))
    (hg : ∀ i, -2 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 2) :
    ∀ i, f i = 0 := by
  have hcases : R = 0 ∨ R = 1 ∨ R = 2 ∨ R = 3 ∨ R = 4 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl
  · intro i
    exact hz i (Nat.zero_le i)
  · have hf1 := hz 1 (by decide)
    have hf2 := hz 2 (by decide)
    have h2 := hg 2
    simp [smoothPow, smooth, hf1, hf2] at h2
    have hf0 : f 0 = 0 := by omega
    intro i
    by_cases hi : i = 0
    · simpa only [hi] using hf0
    · exact hz i (by omega)
  · have hf1 : f 1 = f 0 := by simpa using hs 1 (by decide)
    have hf2 := hz 2 (by decide)
    have h2 := hg 2
    simp [smoothPow, smooth, hf1, hf2] at h2
    have hf0 : f 0 = 0 := by omega
    intro i
    by_cases hi : i < 2
    · have hiCases : i = 0 ∨ i = 1 := by omega
      rcases hiCases with rfl | rfl <;> simp [hf1, hf0]
    · exact hz i (by omega)
  · have hf2 : f 2 = f 0 := by simpa using hs 2 (by decide)
    have hf3 := hz 3 (by decide)
    have h1 := hg 1
    have h2 := hg 2
    have h3 := hg 3
    simp [smoothPow, smooth, hf2, hf3] at h1 h2 h3
    have hb : -1 ≤ f 1 ∧ f 1 ≤ 1 := by omega
    have hf01 : f 0 = 0 ∧ f 1 = 0 := by
      have hbCases : f 1 = -1 ∨ f 1 = 0 ∨ f 1 = 1 := by omega
      rcases hbCases with hbCase | hbCase | hbCase <;> omega
    intro i
    by_cases hi : i < 3
    · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 := by omega
      rcases hiCases with rfl | rfl | rfl <;> simp [hf2, hf01.1, hf01.2]
    · exact hz i (by omega)
  · have hf2 : f 2 = f 1 := by simpa using hs 2 (by decide)
    have hf3 : f 3 = f 0 := by simpa using hs 3 (by decide)
    have h1 := hg 1
    have h3 := hg 3
    simp [smoothPow, smooth, hf2, hf3] at h1 h3
    have hf01 : f 0 = 0 ∧ f 1 = 0 := by omega
    intro i
    by_cases hi : i < 4
    · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by omega
      rcases hiCases with rfl | rfl | rfl | rfl <;>
        simp [hf2, hf3, hf01.1, hf01.2]
    · exact hz i (by omega)

/-- The width-five coefficient constraints force one of two profiles,
scaled by a coefficient in {-1, 0, 1}. -/
theorem smooth_four_box_two_five_classification
    (f : Series)
    (hz : ∀ i, 5 ≤ i → f i = 0)
    (hs : ∀ i, i < 5 → f i = f (5 - 1 - i))
    (hg : ∀ i, -2 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 2) :
    (-1 ≤ f 0 ∧ f 0 ≤ 1) ∧
      ((∀ i, f i = f 0 * core_five_a i) ∨
        (∀ i, f i = f 0 * core_five_b i)) := by
  have hf3 : f 3 = f 1 := by simpa using hs 3 (by decide)
  have hf4 : f 4 = f 0 := by simpa using hs 4 (by decide)
  have h1 := hg 1
  have h2 := hg 2
  have h3 := hg 3
  have h4 := hg 4
  simp [smoothPow, smooth, hf3, hf4] at h1 h2 h3 h4
  have ha : -1 ≤ f 0 ∧ f 0 ≤ 1 := by omega
  have habc :
      (f 1 = -3 * f 0 ∧ f 2 = 4 * f 0) ∨
      (f 1 = -2 * f 0 ∧ f 2 = 2 * f 0) := by
    have hsign : f 0 = -1 ∨ f 0 = 0 ∨ f 0 = 1 := by omega
    rcases hsign with hsign | hsign | hsign <;> omega
  refine ⟨ha, ?_⟩
  rcases habc with h | h
  · left
    intro i
    by_cases hi : i < 5
    · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
      rcases hiCases with rfl | rfl | rfl | rfl | rfl <;>
        simp [core_five_a, hf3, hf4] <;> omega
    · rw [hz i (by omega), (core_five_tails i (by omega)).1]
      simp
  · right
    intro i
    by_cases hi : i < 5
    · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
      rcases hiCases with rfl | rfl | rfl | rfl | rfl <;>
        simp [core_five_b, hf3, hf4] <;> omega
    · rw [hz i (by omega), (core_five_tails i (by omega)).2]
      simp

/-- Symmetric width six is rigid under the fourth-smoothing bound [-2, 2]. -/
theorem smooth_four_box_two_six_rigidity
    (f : Series)
    (hz : ∀ i, 6 ≤ i → f i = 0)
    (hs : ∀ i, i < 6 → f i = f (6 - 1 - i))
    (hg : ∀ i, -2 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 2) :
    ∀ i, f i = 0 := by
  have hf3 : f 3 = f 2 := by simpa using hs 3 (by decide)
  have hf4 : f 4 = f 1 := by simpa using hs 4 (by decide)
  have hf5 : f 5 = f 0 := by simpa using hs 5 (by decide)
  have h1 := hg 1
  have h2 := hg 2
  have h3 := hg 3
  have h4 := hg 4
  simp [smoothPow, smooth, hf3, hf4] at h1 h2 h3 h4
  have hf0 : f 0 = 0 := by omega
  have hf1 : f 1 = 0 := by omega
  have hf2 : f 2 = 0 := by omega
  intro i
  by_cases hi : i < 6
  · have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
    rcases hiCases with rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [hf0, hf1, hf2, hf3, hf4, hf5]
  · exact hz i (by omega)

/-- Complete classification through width six. Every nonzero profile has
width five and equals one of the two explicit cores or its negative. -/
theorem smooth_four_box_two_short_classification
    (f : Series) (R : Nat) (hR : R ≤ 6)
    (hz : ∀ i, R ≤ i → f i = 0)
    (hs : ∀ i, i < R → f i = f (R - 1 - i))
    (hg : ∀ i, -2 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 2) :
    (∀ i, f i = 0) ∨
      (R = 5 ∧
        ((∀ i, f i = core_five_a i) ∨
          (∀ i, f i = -core_five_a i) ∨
          (∀ i, f i = core_five_b i) ∨
          (∀ i, f i = -core_five_b i))) := by
  have hcases : R ≤ 4 ∨ R = 5 ∨ R = 6 := by omega
  rcases hcases with hsmall | rfl | rfl
  · exact Or.inl (smooth_four_box_two_width_le_four f R hsmall hz hs hg)
  · have h := smooth_four_box_two_five_classification f hz hs hg
    have hsign : f 0 = 0 ∨ f 0 = 1 ∨ f 0 = -1 := by omega
    rcases hsign with hzero | hpos | hneg
    · left
      intro i
      rcases h.2 with ha | hb
      · simpa [hzero] using ha i
      · simpa [hzero] using hb i
    · right
      refine ⟨rfl, ?_⟩
      rcases h.2 with ha | hb
      · left
        intro i
        simpa [hpos] using ha i
      · right
        right
        left
        intro i
        simpa [hpos] using hb i
    · right
      refine ⟨rfl, ?_⟩
      rcases h.2 with ha | hb
      · right
        left
        intro i
        simpa [hneg] using ha i
      · right
        right
        right
        intro i
        simpa [hneg] using hb i
  · exact Or.inl (smooth_four_box_two_six_rigidity f hz hs hg)

#print axioms smooth_four_box_two_width_le_four
#print axioms smooth_four_box_two_five_classification
#print axioms smooth_four_box_two_six_rigidity
#print axioms smooth_four_box_two_short_classification

end SevenCarryMaximalWidth
