import P196.Agent10EightCarry.DifferenceObservability

/-!
Agent #10: short symmetric rigidity for fourfold binomial smoothing.
The proof uses only integer linear arithmetic on the two maximal widths,
then symmetric zero padding for smaller widths. The original smoothing
operator and its zero-extension convention are imported unchanged.
-/
set_option maxHeartbeats 10000000
set_option maxRecDepth 100000
namespace EightCarryWidthBound
open DifferenceObservability

private theorem algebra_9 (a0 a1 a2 a3 a4 : Int)
    (h0 : -1 ≤ a0 ∧ a0 ≤ 1)
    (h1 : -1 ≤ 4*a0 + a1 ∧ 4*a0 + a1 ≤ 1)
    (h2 : -1 ≤ 6*a0 + 4*a1 + a2 ∧ 6*a0 + 4*a1 + a2 ≤ 1)
    (h3 : -1 ≤ 4*a0 + 6*a1 + 4*a2 + a3 ∧ 4*a0 + 6*a1 + 4*a2 + a3 ≤ 1)
    (h4 : -1 ≤ a0 + 4*a1 + 6*a2 + 4*a3 + a4 ∧ a0 + 4*a1 + 6*a2 + 4*a3 + a4 ≤ 1)
    (h5 : -1 ≤ a1 + 4*a2 + 7*a3 + 4*a4 ∧ a1 + 4*a2 + 7*a3 + 4*a4 ≤ 1)
    (h6 : -1 ≤ 2*a2 + 8*a3 + 6*a4 ∧ 2*a2 + 8*a3 + 6*a4 ≤ 1)
    : a0 = 0 ∧ a1 = 0 ∧ a2 = 0 ∧ a3 = 0 ∧ a4 = 0 := by
  have ha0 : a0 = -1 ∨ a0 = 0 ∨ a0 = 1 := by omega
  have hb1 : 4*a0 + a1 = -1 ∨ 4*a0 + a1 = 0 ∨ 4*a0 + a1 = 1 := by omega
  rcases ha0 with ha0 | ha0 | ha0 <;> rcases hb1 with hb1 | hb1 | hb1 <;> omega

private theorem algebra_10 (a0 a1 a2 a3 a4 : Int)
    (h0 : -1 ≤ a0 ∧ a0 ≤ 1)
    (h1 : -1 ≤ 4*a0 + a1 ∧ 4*a0 + a1 ≤ 1)
    (h2 : -1 ≤ 6*a0 + 4*a1 + a2 ∧ 6*a0 + 4*a1 + a2 ≤ 1)
    (h3 : -1 ≤ 4*a0 + 6*a1 + 4*a2 + a3 ∧ 4*a0 + 6*a1 + 4*a2 + a3 ≤ 1)
    (h4 : -1 ≤ a0 + 4*a1 + 6*a2 + 4*a3 + a4 ∧ a0 + 4*a1 + 6*a2 + 4*a3 + a4 ≤ 1)
    (h5 : -1 ≤ a1 + 4*a2 + 6*a3 + 5*a4 ∧ a1 + 4*a2 + 6*a3 + 5*a4 ≤ 1)
    (h6 : -1 ≤ a2 + 5*a3 + 10*a4 ∧ a2 + 5*a3 + 10*a4 ≤ 1)
    : a0 = 0 ∧ a1 = 0 ∧ a2 = 0 ∧ a3 = 0 ∧ a4 = 0 := by
  have ha0 : a0 = -1 ∨ a0 = 0 ∨ a0 = 1 := by omega
  rcases ha0 with ha0 | ha0 | ha0 <;> omega


/-- The final odd and even widths each have five independent coefficients. -/
private theorem smooth_four_nine_or_ten (f : Series) (L : Nat)
    (hL : L = 9 ∨ L = 10)
    (hz : ∀ i, L ≤ i → f i = 0)
    (hs : ∀ i, i < L → f i = f (L - 1 - i))
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    ∀ i, f i = 0 := by
  have h0 := hg 0
  have h1 := hg 1
  have h2 := hg 2
  have h3 := hg 3
  have h4 := hg 4
  have h5 := hg 5
  have h6 := hg 6
  simp [smoothPow, smooth] at h0 h1 h2 h3 h4 h5 h6
  have hhalf : f 0 = 0 ∧ f 1 = 0 ∧ f 2 = 0 ∧ f 3 = 0 ∧ f 4 = 0 := by
    rcases hL with rfl | rfl
    · have s5 := hs 5 (by decide)
      have s6 := hs 6 (by decide)
      simp at s5 s6
      exact algebra_9 (f 0) (f 1) (f 2) (f 3) (f 4)
        (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
    · have s5 := hs 5 (by decide)
      have s6 := hs 6 (by decide)
      simp at s5 s6
      exact algebra_10 (f 0) (f 1) (f 2) (f 3) (f 4)
        (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
  have hfirst : ∀ i, i < 5 → f i = 0 := by
    intro i hi
    have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
    rcases hc with rfl | rfl | rfl | rfl | rfl <;> omega
  intro i
  by_cases hi : i < L
  · by_cases hif : i < 5
    · exact hfirst i hif
    · rw [hs i hi]
      exact hfirst (L - 1 - i) (by omega)
  · exact hz i (by omega)

/-- Insert one zero before the input sequence. -/
private def prependZero (f : Series) : Series :=
  fun i => if i = 0 then 0 else f (i - 1)

private theorem smoothPow_prependZero (k : Nat) (f : Series) :
    ∀ i, smoothPow k (prependZero f) i = prependZero (smoothPow k f) i := by
  induction k with
  | zero => intro i; rfl
  | succ k ih =>
    intro i
    cases i with
    | zero => simp [smoothPow, smooth, ih, prependZero]
    | succ i =>
      cases i with
      | zero => simp [smoothPow, smooth, ih, prependZero]
      | succ i => simp [smoothPow, smooth, ih, prependZero]

/-- Symmetric zero padding preserves support and the unit output bound. -/
private theorem prependZero_preserves (f : Series) (L : Nat)
    (hz : ∀ i, L ≤ i → f i = 0)
    (hs : ∀ i, i < L → f i = f (L - 1 - i))
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    (∀ i, L + 2 ≤ i → prependZero f i = 0) ∧
    (∀ i, i < L + 2 → prependZero f i = prependZero f (L + 2 - 1 - i)) ∧
    (∀ i, -1 ≤ smoothPow 4 (prependZero f) i ∧
      smoothPow 4 (prependZero f) i ≤ 1) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i hi
    have hi0 : i ≠ 0 := by omega
    simp [prependZero, hi0, hz (i - 1) (by omega)]
  · intro i hi
    by_cases hi0 : i = 0
    · subst i
      have hm : L + 2 - 1 - 0 = L + 1 := by omega
      rw [hm]
      simp [prependZero, hz L (Nat.le_refl L)]
    · by_cases hil : i = L + 1
      · subst i
        have hm : L + 2 - 1 - (L + 1) = 0 := by omega
        rw [hm]
        simp [prependZero, hz L (Nat.le_refl L)]
      · have hm0 : L + 2 - 1 - i ≠ 0 := by omega
        have he : L + 2 - 1 - i - 1 = L - 1 - (i - 1) := by omega
        simp only [prependZero, if_neg hi0, if_neg hm0, he]
        exact hs (i - 1) (by omega)
  · intro i
    rw [smoothPow_prependZero]
    by_cases hi : i = 0
    · simp [prependZero, hi]
    · simpa [prependZero, hi] using hg (i - 1)

/-- Every symmetric integer input of width at most ten vanishes when its
fourfold smoothing lies in the unit box. No input coefficient bound is needed. -/
theorem smooth_four_short_symmetric (f : Series) (L : Nat)
    (hL : L ≤ 10)
    (hz : ∀ i, L ≤ i → f i = 0)
    (hs : ∀ i, i < L → f i = f (L - 1 - i))
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    ∀ i, f i = 0 := by
  by_cases hlast : L = 9 ∨ L = 10
  · exact smooth_four_nine_or_ten f L hlast hz hs hg
  · have hnext : L + 2 ≤ 10 := by omega
    have hp := prependZero_preserves f L hz hs hg
    have hh := smooth_four_short_symmetric (prependZero f) (L + 2) hnext
      hp.1 hp.2.1 hp.2.2
    intro i
    simpa [prependZero] using hh (i + 1)
termination_by 10 - L
decreasing_by omega

#print axioms smooth_four_short_symmetric
end EightCarryWidthBound
