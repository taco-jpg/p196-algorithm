import P196.DigitSumElevenClassification.BlockArithmetic
import P196.DigitSumElevenClassification.Geometry
import P196.Drafts.Agent104ReviewAgent13RealWeights.Family

/-!
Exact ordinary reverse-and-add trajectories for the four sparse residual
profiles at digit sum eleven. The width is arbitrary above the explicit
finite boundary, and every gap arithmetic identity is checked symbolically.
-/

namespace DigitSumElevenClassification

open DecimalDigits FoldedDecimal Lychrel196

/-- The first actual step depends only on the isolated outer and center
coefficients, regardless of the split between the mirrored input digits. -/
theorem outer_profile_step (n : Nat) (d : Nat → Nat) (m c a : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = outerColumns m c a i) :
    step n = a * 10 ^ (2 * m) + (2 * c) * 10 ^ m + a := by
  have hpoint : ∀ i, i < 2 * m + 1 → outerColumns m c a i =
      ((if i = 2 * m then a else 0) + (if i = m then 2 * c else 0)) +
        (if i = 0 then a else 0) := by
    intro i hi
    by_cases hm' : i = m <;> by_cases h0 : i = 0 <;> by_cases ht : i = 2 * m <;>
      simp_all [outerColumns] <;> omega
  rw [step_eq_word_value n d (outerColumns m c a) (2 * m + 1) hcan hcols,
    value_congr _ _ _ hpoint, value_add, value_add,
    Agent13SafeFamily.value_single, Agent13SafeFamily.value_single,
    Agent13SafeFamily.value_single]
  simp [show 2 * m < 2 * m + 1 by omega, show m < 2 * m + 1 by omega,
    show 0 < 2 * m + 1 by omega]

/-- The corresponding exact first-step formula when the residual mass also
occupies the pair immediately adjacent to the center. -/
theorem near_profile_step (n : Nat) (d : Nat → Nat) (m c b : Nat)
    (hm : 2 ≤ m) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = nearColumns m c b i) :
    step n = 10 ^ (2 * m) + b * 10 ^ (m + 1) + (2 * c) * 10 ^ m +
      b * 10 ^ (m - 1) + 1 := by
  have hpoint : ∀ i, i < 2 * m + 1 → nearColumns m c b i =
      ((((if i = 2 * m then 1 else 0) + (if i = m + 1 then b else 0)) +
        (if i = m then 2 * c else 0)) + (if i = m - 1 then b else 0)) +
        (if i = 0 then 1 else 0) := by
    intro i hi
    have heq : i + 1 = m ↔ i = m - 1 := by omega
    simp only [nearColumns, heq]
    clear heq hcan hcols
    by_cases hzero : i = 0
    · subst i
      simp [show (0 : Nat) ≠ m by omega,
        show (0 : Nat) ≠ 2 * m by omega,
        show (0 : Nat) ≠ m + 1 by omega,
        show (0 : Nat) ≠ m - 1 by omega]
    by_cases hcenter : i = m
    · subst i
      simp [show (m : Nat) ≠ 0 by omega,
        show (m : Nat) ≠ 2 * m by omega,
        show (m : Nat) ≠ m + 1 by omega,
        show (m : Nat) ≠ m - 1 by omega]
    by_cases htop : i = 2 * m
    · subst i
      simp [show (2 * m : Nat) ≠ 0 by omega,
        show (2 * m : Nat) ≠ m by omega,
        show (2 * m : Nat) ≠ m + 1 by omega,
        show (2 * m : Nat) ≠ m - 1 by omega]
    by_cases hupper : i = m + 1
    · subst i
      simp [show (m + 1 : Nat) ≠ 0 by omega,
        show (m + 1 : Nat) ≠ m by omega,
        show (m + 1 : Nat) ≠ 2 * m by omega,
        show (m + 1 : Nat) ≠ m - 1 by omega]
    by_cases hlower : i = m - 1
    · subst i
      simp [show (m - 1 : Nat) ≠ 0 by omega,
        show (m - 1 : Nat) ≠ m by omega,
        show (m - 1 : Nat) ≠ 2 * m by omega,
        show (m - 1 : Nat) ≠ m + 1 by omega]
    simp [hzero, hcenter, htop, hupper, hlower]
  rw [step_eq_word_value n d (nearColumns m c b) (2 * m + 1) hcan hcols,
    value_congr _ _ _ hpoint, value_add, value_add, value_add, value_add,
    Agent13SafeFamily.value_single, Agent13SafeFamily.value_single,
    Agent13SafeFamily.value_single, Agent13SafeFamily.value_single,
    Agent13SafeFamily.value_single]
  simp [show 2 * m < 2 * m + 1 by omega, show m + 1 < 2 * m + 1 by omega,
    show m < 2 * m + 1 by omega, show m - 1 < 2 * m + 1 by omega,
    show 0 < 2 * m + 1 by omega]

/-- The outer profile with center 8 reaches a palindrome at the stated
positive time for every width above the finite boundary. -/
theorem outer_eight_large (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 3 ≤ m) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = outerColumns m 8 3 i) :
    Palindrome (orbit n 4) := by
  obtain ⟨g, rfl⟩ : ∃ g : Nat, m = g + 3 := ⟨m - 3, by omega⟩
  have h1 : orbit n 1 = Agent109.evalL (gapWord g [3, 0] [0, 6, 1, 0] [3]) := by
    change step n = _
    rw [outer_profile_step n d (g + 3) 8 3
      (by omega) hcan hcols]
    have hp : 10 ^ (2 * (g + 3)) = 1000000 * 10 ^ (g + g) := by
      rw [show 2 * (g + 3) = (g + g) + 6 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    have hc : 10 ^ (g + 3) = 1000 * 10 ^ g := by
      rw [Nat.pow_add]
      simp [Nat.mul_comm]
    rw [hp, hc]
    simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h2 : orbit n 2 = Agent109.evalL (gapWord g [6, 0] [1, 2, 2, 0] [6]) := by
    change step (orbit n 1) = _
    rw [h1]
    apply step_gapWord
    · exact canon_gapWord g [3, 0] [0, 6, 1, 0] [3] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h3 : orbit n 3 = Agent109.evalL (gapWord g [2, 1] [3, 4, 3, 0] [2, 1]) := by
    change step (orbit n 2) = _
    rw [h2]
    apply step_gapWord
    · exact canon_gapWord g [6, 0] [1, 2, 2, 0] [6] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h4 : orbit n 4 = Agent109.evalL (gapWord g [3, 3] [3, 7, 7, 3] [3, 3]) := by
    change step (orbit n 3) = _
    rw [h3]
    apply step_gapWord
    · exact canon_gapWord g [2, 1] [3, 4, 3, 0] [2, 1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  rw [h4]
  apply palindrome_gapWord
  · exact canon_gapWord g [3, 3] [3, 7, 7, 3] [3, 3] (by simp) (by simp)
      (by simp [Agent109.Canon]) (by decide)
  · simp [gapWord, List.reverse_append, List.reverse_replicate, List.append_assoc]

/-- The near profile with center 8 reaches a palindrome at the stated
positive time for every width above the finite boundary. -/
theorem near_eight_large (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 4 ≤ m) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = nearColumns m 8 2 i) :
    Palindrome (orbit n 6) := by
  obtain ⟨g, rfl⟩ : ∃ g : Nat, m = g + 4 := ⟨m - 4, by omega⟩
  have h1 : orbit n 1 = Agent109.evalL (gapWord g [1, 0] [0, 2, 6, 3, 0, 0] [1]) := by
    change step n = _
    rw [near_profile_step n d (g + 4) 8 2
      (by omega) hcan hcols]
    have hp : 10 ^ (2 * (g + 4)) = 100000000 * 10 ^ (g + g) := by
      rw [show 2 * (g + 4) = (g + g) + 8 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    have hc : 10 ^ (g + 4) = 10000 * 10 ^ g := by
      rw [Nat.pow_add]
      simp [Nat.mul_comm]
    have hhi : 10 ^ (g + 4 + 1) = 100000 * 10 ^ g := by
      rw [show g + 4 + 1 = g + 5 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    have hlo : 10 ^ (g + 4 - 1) = 1000 * 10 ^ g := by
      rw [show g + 4 - 1 = g + 3 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    rw [hp, hc, hhi, hlo]
    simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h2 : orbit n 2 = Agent109.evalL (gapWord g [2, 0] [0, 5, 2, 6, 0, 0] [2]) := by
    change step (orbit n 1) = _
    rw [h1]
    apply step_gapWord
    · exact canon_gapWord g [1, 0] [0, 2, 6, 3, 0, 0] [1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h3 : orbit n 3 = Agent109.evalL (gapWord g [4, 0] [0, 1, 5, 1, 1, 0] [4]) := by
    change step (orbit n 2) = _
    rw [h2]
    apply step_gapWord
    · exact canon_gapWord g [2, 0] [0, 5, 2, 6, 0, 0] [2] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h4 : orbit n 4 = Agent109.evalL (gapWord g [8, 0] [1, 2, 0, 3, 1, 0] [8]) := by
    change step (orbit n 3) = _
    rw [h3]
    apply step_gapWord
    · exact canon_gapWord g [4, 0] [0, 1, 5, 1, 1, 0] [4] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h5 : orbit n 5 = Agent109.evalL (gapWord g [6, 1] [2, 5, 0, 5, 2, 0] [6, 1]) := by
    change step (orbit n 4) = _
    rw [h4]
    apply step_gapWord
    · exact canon_gapWord g [8, 0] [1, 2, 0, 3, 1, 0] [8] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h6 : orbit n 6 = Agent109.evalL (gapWord g [7, 7] [2, 7, 5, 5, 7, 2] [7, 7]) := by
    change step (orbit n 5) = _
    rw [h5]
    apply step_gapWord
    · exact canon_gapWord g [6, 1] [2, 5, 0, 5, 2, 0] [6, 1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  rw [h6]
  apply palindrome_gapWord
  · exact canon_gapWord g [7, 7] [2, 7, 5, 5, 7, 2] [7, 7] (by simp) (by simp)
      (by simp [Agent109.Canon]) (by decide)
  · simp [gapWord, List.reverse_append, List.reverse_replicate, List.append_assoc]

/-- The near profile with center 9 reaches a palindrome at the stated
positive time for every width above the finite boundary. -/
theorem near_nine_large (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 4 ≤ m) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = nearColumns m 9 1 i) :
    Palindrome (orbit n 6) := by
  obtain ⟨g, rfl⟩ : ∃ g : Nat, m = g + 4 := ⟨m - 4, by omega⟩
  have h1 : orbit n 1 = Agent109.evalL (gapWord g [1, 0] [0, 1, 8, 2, 0, 0] [1]) := by
    change step n = _
    rw [near_profile_step n d (g + 4) 9 1
      (by omega) hcan hcols]
    have hp : 10 ^ (2 * (g + 4)) = 100000000 * 10 ^ (g + g) := by
      rw [show 2 * (g + 4) = (g + g) + 8 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    have hc : 10 ^ (g + 4) = 10000 * 10 ^ g := by
      rw [Nat.pow_add]
      simp [Nat.mul_comm]
    have hhi : 10 ^ (g + 4 + 1) = 100000 * 10 ^ g := by
      rw [show g + 4 + 1 = g + 5 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    have hlo : 10 ^ (g + 4 - 1) = 1000 * 10 ^ g := by
      rw [show g + 4 - 1 = g + 3 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    rw [hp, hc, hhi, hlo]
    simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h2 : orbit n 2 = Agent109.evalL (gapWord g [2, 0] [0, 3, 6, 4, 0, 0] [2]) := by
    change step (orbit n 1) = _
    rw [h1]
    apply step_gapWord
    · exact canon_gapWord g [1, 0] [0, 1, 8, 2, 0, 0] [1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h3 : orbit n 3 = Agent109.evalL (gapWord g [4, 0] [0, 7, 2, 8, 0, 0] [4]) := by
    change step (orbit n 2) = _
    rw [h2]
    apply step_gapWord
    · exact canon_gapWord g [2, 0] [0, 3, 6, 4, 0, 0] [2] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h4 : orbit n 4 = Agent109.evalL (gapWord g [8, 0] [0, 5, 5, 5, 1, 0] [8]) := by
    change step (orbit n 3) = _
    rw [h3]
    apply step_gapWord
    · exact canon_gapWord g [4, 0] [0, 7, 2, 8, 0, 0] [4] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h5 : orbit n 5 = Agent109.evalL (gapWord g [6, 1] [1, 0, 1, 1, 2, 0] [6, 1]) := by
    change step (orbit n 4) = _
    rw [h4]
    apply step_gapWord
    · exact canon_gapWord g [8, 0] [0, 5, 5, 5, 1, 0] [8] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h6 : orbit n 6 = Agent109.evalL (gapWord g [7, 7] [1, 2, 2, 2, 2, 1] [7, 7]) := by
    change step (orbit n 5) = _
    rw [h5]
    apply step_gapWord
    · exact canon_gapWord g [6, 1] [1, 0, 1, 1, 2, 0] [6, 1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  rw [h6]
  apply palindrome_gapWord
  · exact canon_gapWord g [7, 7] [1, 2, 2, 2, 2, 1] [7, 7] (by simp) (by simp)
      (by simp [Agent109.Canon]) (by decide)
  · simp [gapWord, List.reverse_append, List.reverse_replicate, List.append_assoc]

/-- The outer profile with center 9 reaches a palindrome at the stated
positive time for every width above the finite boundary. -/
theorem outer_nine_large (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 5 ≤ m) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = outerColumns m 9 2 i) :
    Palindrome (orbit n 10) := by
  obtain ⟨g, rfl⟩ : ∃ g : Nat, m = g + 5 := ⟨m - 5, by omega⟩
  have h1 : orbit n 1 = Agent109.evalL (gapWord g [2, 0, 0, 0] [0, 8, 1, 0, 0, 0] [2]) := by
    change step n = _
    rw [outer_profile_step n d (g + 5) 9 2
      (by omega) hcan hcols]
    have hp : 10 ^ (2 * (g + 5)) = 10000000000 * 10 ^ (g + g) := by
      rw [show 2 * (g + 5) = (g + g) + 10 by omega, Nat.pow_add]
      simp [Nat.mul_comm]
    have hc : 10 ^ (g + 5) = 100000 * 10 ^ g := by
      rw [Nat.pow_add]
      simp [Nat.mul_comm]
    rw [hp, hc]
    simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h2 : orbit n 2 = Agent109.evalL (gapWord g [4, 0, 0, 0] [1, 6, 2, 0, 0, 0] [4]) := by
    change step (orbit n 1) = _
    rw [h1]
    apply step_gapWord
    · exact canon_gapWord g [2, 0, 0, 0] [0, 8, 1, 0, 0, 0] [2] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h3 : orbit n 3 = Agent109.evalL (gapWord g [8, 0, 0, 0] [3, 2, 4, 0, 0, 0] [8]) := by
    change step (orbit n 2) = _
    rw [h2]
    apply step_gapWord
    · exact canon_gapWord g [4, 0, 0, 0] [1, 6, 2, 0, 0, 0] [4] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h4 : orbit n 4 = Agent109.evalL (gapWord g [6, 1, 0, 0] [7, 4, 7, 0, 0, 0] [6, 1]) := by
    change step (orbit n 3) = _
    rw [h3]
    apply step_gapWord
    · exact canon_gapWord g [8, 0, 0, 0] [3, 2, 4, 0, 0, 0] [8] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h5 : orbit n 5 = Agent109.evalL (gapWord g [7, 7, 0, 0] [7, 1, 2, 8, 0, 0] [7, 7]) := by
    change step (orbit n 4) = _
    rw [h4]
    apply step_gapWord
    · exact canon_gapWord g [6, 1, 0, 0] [7, 4, 7, 0, 0, 0] [6, 1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h6 : orbit n 6 = Agent109.evalL (gapWord g [4, 5, 1, 0] [5, 4, 3, 5, 1, 0] [4, 5, 1]) := by
    change step (orbit n 5) = _
    rw [h5]
    apply step_gapWord
    · exact canon_gapWord g [7, 7, 0, 0] [7, 1, 2, 8, 0, 0] [7, 7] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h7 : orbit n 7 = Agent109.evalL (gapWord g [5, 0, 6, 0] [6, 9, 6, 9, 6, 0] [5, 0, 6]) := by
    change step (orbit n 6) = _
    rw [h6]
    apply step_gapWord
    · exact canon_gapWord g [4, 5, 1, 0] [5, 4, 3, 5, 1, 0] [4, 5, 1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h8 : orbit n 8 = Agent109.evalL (gapWord g [1, 1, 1, 1] [2, 9, 3, 9, 3, 1] [1, 1, 1, 1]) := by
    change step (orbit n 7) = _
    rw [h7]
    apply step_gapWord
    · exact canon_gapWord g [5, 0, 6, 0] [6, 9, 6, 9, 6, 0] [5, 0, 6] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h9 : orbit n 9 = Agent109.evalL (gapWord g [2, 2, 2, 2] [3, 2, 3, 3, 3, 4] [2, 2, 2, 2]) := by
    change step (orbit n 8) = _
    rw [h8]
    apply step_gapWord
    · exact canon_gapWord g [1, 1, 1, 1] [2, 9, 3, 9, 3, 1] [1, 1, 1, 1] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  have h10 : orbit n 10 = Agent109.evalL (gapWord g [4, 4, 4, 4] [7, 5, 6, 6, 5, 7] [4, 4, 4, 4]) := by
    change step (orbit n 9) = _
    rw [h9]
    apply step_gapWord
    · exact canon_gapWord g [2, 2, 2, 2] [3, 2, 3, 3, 3, 4] [2, 2, 2, 2] (by simp) (by simp)
        (by simp [Agent109.Canon]) (by decide)
    · simp [evalL_gapWord, Agent109.evalL] <;> omega
  rw [h10]
  apply palindrome_gapWord
  · exact canon_gapWord g [4, 4, 4, 4] [7, 5, 6, 6, 5, 7] [4, 4, 4, 4] (by simp) (by simp)
      (by simp [Agent109.Canon]) (by decide)
  · simp [gapWord, List.reverse_append, List.reverse_replicate, List.append_assoc]

end DigitSumElevenClassification
