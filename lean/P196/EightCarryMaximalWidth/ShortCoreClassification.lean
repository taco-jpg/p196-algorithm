import P196.Agent10EightCarry.Agent10SmoothingBridge

/-!
Agent #10: exact symmetric cores at widths eleven and twelve.

For either width, an integer sequence whose fourfold smoothing lies in the
unit box is zero or one of the two signs of the displayed core. No bound on
the input coefficients is assumed. The width-eleven core is the existing
`Agent10SmoothingBoundary.witness`; only the width-twelve core is defined here.
These are algebraic classifications, independent of actual carry dynamics.
-/
set_option maxHeartbeats 2000000
namespace EightCarryMaximalWidth
open DifferenceObservability

private theorem algebra_eleven (a0 a1 a2 a3 a4 a5 : Int)
    (h0 : -1 ≤ a0 ∧ a0 ≤ 1)
    (h1 : -1 ≤ 4*a0+a1 ∧ 4*a0+a1 ≤ 1)
    (h2 : -1 ≤ 6*a0+4*a1+a2 ∧ 6*a0+4*a1+a2 ≤ 1)
    (h3 : -1 ≤ 4*a0+6*a1+4*a2+a3 ∧ 4*a0+6*a1+4*a2+a3 ≤ 1)
    (h4 : -1 ≤ a0+4*a1+6*a2+4*a3+a4 ∧ a0+4*a1+6*a2+4*a3+a4 ≤ 1)
    (h5 : -1 ≤ a1+4*a2+6*a3+4*a4+a5 ∧ a1+4*a2+6*a3+4*a4+a5 ≤ 1)
    (h6 : -1 ≤ a2+4*a3+7*a4+4*a5 ∧ a2+4*a3+7*a4+4*a5 ≤ 1)
    (h7 : -1 ≤ 2*a3+8*a4+6*a5 ∧ 2*a3+8*a4+6*a5 ≤ 1) :
    a1 = -3*a0 ∧ a2 = 5*a0 ∧ a3 = -6*a0 ∧ a4 = 6*a0 ∧ a5 = -6*a0 := by
  have hm : a3 = -4*a4-3*a5 := by omega
  simp only [hm] at h3 h4 h5 h6 h7 ⊢
  clear hm h7
  have ha0 : a0 = -1 ∨ a0 = 0 ∨ a0 = 1 := by omega
  have hb1 : 4*a0+a1 = -1 ∨ 4*a0+a1 = 0 ∨ 4*a0+a1 = 1 := by omega
  have hb2 : 6*a0+4*a1+a2 = -1 ∨ 6*a0+4*a1+a2 = 0 ∨ 6*a0+4*a1+a2 = 1 := by omega
  rcases ha0 with ha0 | ha0 | ha0 <;> rcases hb1 with hb1 | hb1 | hb1 <;>
    rcases hb2 with hb2 | hb2 | hb2 <;> omega

private theorem algebra_twelve (a0 a1 a2 a3 a4 a5 : Int)
    (h0 : -1 ≤ a0 ∧ a0 ≤ 1)
    (h1 : -1 ≤ 4*a0+a1 ∧ 4*a0+a1 ≤ 1)
    (h2 : -1 ≤ 6*a0+4*a1+a2 ∧ 6*a0+4*a1+a2 ≤ 1)
    (h3 : -1 ≤ 4*a0+6*a1+4*a2+a3 ∧ 4*a0+6*a1+4*a2+a3 ≤ 1)
    (h4 : -1 ≤ a0+4*a1+6*a2+4*a3+a4 ∧ a0+4*a1+6*a2+4*a3+a4 ≤ 1)
    (h5 : -1 ≤ a1+4*a2+6*a3+4*a4+a5 ∧ a1+4*a2+6*a3+4*a4+a5 ≤ 1)
    (h6 : -1 ≤ a2+4*a3+6*a4+5*a5 ∧ a2+4*a3+6*a4+5*a5 ≤ 1)
    (h7 : -1 ≤ a3+5*a4+10*a5 ∧ a3+5*a4+10*a5 ≤ 1) :
    a1 = -3*a0 ∧ a2 = 5*a0 ∧ a3 = -6*a0 ∧ a4 = 5*a0 ∧ a5 = -2*a0 := by
  have ha0 : a0 = -1 ∨ a0 = 0 ∨ a0 = 1 := by omega
  have hb1 : 4*a0+a1 = -1 ∨ 4*a0+a1 = 0 ∨ 4*a0+a1 = 1 := by omega
  rcases ha0 with ha0 | ha0 | ha0 <;> rcases hb1 with hb1 | hb1 | hb1 <;> omega

/-- The unique positive-leading nonzero core at nominal symmetric width twelve. -/
def core_twelve : Series
  | 0 => 1
  | 1 => -3
  | 2 => 5
  | 3 => -6
  | 4 => 5
  | 5 => -2
  | 6 => -2
  | 7 => 5
  | 8 => -6
  | 9 => 5
  | 10 => -3
  | 11 => 1
  | _ => 0

theorem core_twelve_zero_after (i : Nat) (hi : 12 ≤ i) : core_twelve i = 0 := by
  have he : i = (i-12)+12 := by omega
  rw [he]
  simp [core_twelve]

theorem core_twelve_symmetric : ∀ i : Fin 12,
    core_twelve i.val = core_twelve (11-i.val) := by decide

theorem core_twelve_smooth_bounds (i : Nat) :
    -1 ≤ smoothPow 4 core_twelve i ∧ smoothPow 4 core_twelve i ≤ 1 := by
  rw [← Agent10SmoothingBridge.four_eq_smoothPow]
  have small : ∀ j : Fin 16,
      -1 ≤ Agent10SmoothingBoundary.four core_twelve j.val ∧
      Agent10SmoothingBoundary.four core_twelve j.val ≤ 1 := by decide
  by_cases hi : i < 16
  · exact small ⟨i, hi⟩
  · have h1 : 1 ≤ i := by omega
    have h2 : 2 ≤ i := by omega
    have h3 : 3 ≤ i := by omega
    have h4 : 4 ≤ i := by omega
    simp only [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag,
      if_pos h1, if_pos h2, if_pos h3, if_pos h4]
    rw [core_twelve_zero_after i (by omega),
      core_twelve_zero_after (i-1) (by omega),
      core_twelve_zero_after (i-2) (by omega),
      core_twelve_zero_after (i-3) (by omega),
      core_twelve_zero_after (i-4) (by omega)]
    decide

/-- Width eleven has only the zero sequence and the two signs of the existing
boundary witness. The leading coefficient determines the entire sequence. -/
theorem smooth_four_eleven_classification (f : Series)
    (hz : ∀ i, 11 ≤ i → f i = 0)
    (hs : ∀ i, i < 11 → f i = f (10-i))
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    (-1 ≤ f 0 ∧ f 0 ≤ 1) ∧
      ∀ i, f i = f 0 * Agent10SmoothingBoundary.witness i := by
  have h0 := hg 0
  have h1 := hg 1
  have h2 := hg 2
  have h3 := hg 3
  have h4 := hg 4
  have h5 := hg 5
  have h6 := hg 6
  have h7 := hg 7
  simp only [← Agent10SmoothingBridge.four_eq_smoothPow] at h0 h1 h2 h3 h4 h5 h6 h7
  simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag]
    at h0 h1 h2 h3 h4 h5 h6 h7
  have s6 : f 6 = f 4 := by simpa using hs 6 (by decide)
  have s7 : f 7 = f 3 := by simpa using hs 7 (by decide)
  have hhalf := algebra_eleven (f 0) (f 1) (f 2) (f 3) (f 4) (f 5)
    h0 (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
  have hfirst : ∀ i, i < 6 → f i = f 0 * Agent10SmoothingBoundary.witness i := by
    intro i hi
    have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
    rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [Agent10SmoothingBoundary.witness] <;> omega
  refine ⟨h0, ?_⟩
  intro i
  by_cases hi : i < 11
  · by_cases hh : i < 6
    · exact hfirst i hh
    · rw [hs i hi, Agent10SmoothingBoundary.witness_symmetric ⟨i, hi⟩]
      exact hfirst (10-i) (by omega)
  · rw [hz i (by omega), Agent10SmoothingBoundary.witness_zero_after i (by omega)]
    simp

/-- Width twelve likewise has one nonzero core up to sign, without an input
coefficient bound or a minimal-support premise. -/
theorem smooth_four_twelve_classification (f : Series)
    (hz : ∀ i, 12 ≤ i → f i = 0)
    (hs : ∀ i, i < 12 → f i = f (11-i))
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    (-1 ≤ f 0 ∧ f 0 ≤ 1) ∧ ∀ i, f i = f 0 * core_twelve i := by
  have h0 := hg 0
  have h1 := hg 1
  have h2 := hg 2
  have h3 := hg 3
  have h4 := hg 4
  have h5 := hg 5
  have h6 := hg 6
  have h7 := hg 7
  simp only [← Agent10SmoothingBridge.four_eq_smoothPow] at h0 h1 h2 h3 h4 h5 h6 h7
  simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag]
    at h0 h1 h2 h3 h4 h5 h6 h7
  have s6 : f 6 = f 5 := by simpa using hs 6 (by decide)
  have s7 : f 7 = f 4 := by simpa using hs 7 (by decide)
  have hhalf := algebra_twelve (f 0) (f 1) (f 2) (f 3) (f 4) (f 5)
    h0 (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
  have hfirst : ∀ i, i < 6 → f i = f 0 * core_twelve i := by
    intro i hi
    have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
    rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;> simp [core_twelve] <;> omega
  refine ⟨h0, ?_⟩
  intro i
  by_cases hi : i < 12
  · by_cases hh : i < 6
    · exact hfirst i hh
    · rw [hs i hi, core_twelve_symmetric ⟨i, hi⟩]
      exact hfirst (11-i) (by omega)
  · rw [hz i (by omega), core_twelve_zero_after i (by omega)]
    simp

/-- The three alternatives at width eleven, as equalities of functions. -/
theorem smooth_four_eleven_cases (f : Series)
    (hz : ∀ i, 11 ≤ i → f i = 0)
    (hs : ∀ i, i < 11 → f i = f (10-i))
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    f = (fun _ => 0) ∨ f = Agent10SmoothingBoundary.witness ∨
      f = (fun i => -Agent10SmoothingBoundary.witness i) := by
  obtain ⟨hb, he⟩ := smooth_four_eleven_classification f hz hs hg
  have hc : f 0 = 0 ∨ f 0 = 1 ∨ f 0 = -1 := by omega
  rcases hc with hc | hc | hc
  · exact Or.inl (funext fun i => by simpa [hc] using he i)
  · exact Or.inr (Or.inl (funext fun i => by simpa [hc] using he i))
  · exact Or.inr (Or.inr (funext fun i => by simpa [hc] using he i))

/-- The three alternatives at width twelve, as equalities of functions. -/
theorem smooth_four_twelve_cases (f : Series)
    (hz : ∀ i, 12 ≤ i → f i = 0)
    (hs : ∀ i, i < 12 → f i = f (11-i))
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    f = (fun _ => 0) ∨ f = core_twelve ∨ f = (fun i => -core_twelve i) := by
  obtain ⟨hb, he⟩ := smooth_four_twelve_classification f hz hs hg
  have hc : f 0 = 0 ∨ f 0 = 1 ∨ f 0 = -1 := by omega
  rcases hc with hc | hc | hc
  · exact Or.inl (funext fun i => by simpa [hc] using he i)
  · exact Or.inr (Or.inl (funext fun i => by simpa [hc] using he i))
  · exact Or.inr (Or.inr (funext fun i => by simpa [hc] using he i))

#print axioms core_twelve_zero_after
#print axioms core_twelve_symmetric
#print axioms core_twelve_smooth_bounds
#print axioms smooth_four_eleven_classification
#print axioms smooth_four_twelve_classification
#print axioms smooth_four_eleven_cases
#print axioms smooth_four_twelve_cases
end EightCarryMaximalWidth
