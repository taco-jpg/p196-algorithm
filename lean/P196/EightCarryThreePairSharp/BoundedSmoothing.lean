import P196.Agent10EightCarry.Agent10SmoothingBridge

/-!
Agent #10: the first possible nonzero coefficient under bounded fourfold
smoothing leaves only three prefixes. This is integer linear arithmetic:
the input need not be symmetric or finitely supported. Coefficients through
index eight suffice for the conclusion through index six.
-/

namespace EightCarryThreePairSharp
open DifferenceObservability

/-- With two leading zeros and next coefficient one, the input bound nine
and unit fourth-smoothing bound force one of these three initial patterns. -/
theorem bounded_unit_four_initial_cases (f : Series)
    (h0 : f 0 = 0) (h1 : f 1 = 0) (h2 : f 2 = 1)
    (hb : ∀ i, -9 ≤ f i ∧ f i ≤ 9)
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    f 3 = -3 ∧ f 4 = 5 ∧
      ((f 5 = -6 ∧ (f 6 = 5 ∨ f 6 = 6)) ∨ (f 5 = -7 ∧ f 6 = 8)) := by
  have s3 := hg 3
  have s4 := hg 4
  have s5 := hg 5
  simp only [← Agent10SmoothingBridge.four_eq_smoothPow] at s3 s4 s5
  simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag, h0, h1, h2]
    at s3 s4 s5
  have b5 := hb 5
  have h3 : f 3 = -3 := by omega
  have s6 := hg 6
  simp only [← Agent10SmoothingBridge.four_eq_smoothPow] at s6
  simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag, h0, h1, h2, h3]
    at s6
  have b6 := hb 6
  have h4 : f 4 = 5 := by omega
  have s7 := hg 7
  have s8 := hg 8
  simp only [← Agent10SmoothingBridge.four_eq_smoothPow] at s7 s8
  simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag, h0, h1, h2, h3, h4]
    at s7 s8
  have b7 := hb 7
  have b8 := hb 8
  have h5 : f 5 = -6 ∨ f 5 = -7 := by omega
  refine ⟨h3, h4, ?_⟩
  rcases h5 with h5 | h5
  · left
    exact ⟨h5, by omega⟩
  · right
    exact ⟨h5, by omega⟩

#print axioms bounded_unit_four_initial_cases
end EightCarryThreePairSharp
