import P196.DigitSumElevenClassification.Geometry
import P196.DigitSumTenTermination.Main

/-!
The finite width boundaries of the sparse digit-sum-eleven profiles.
Equality of the actual first step transports each checked representative
to every canonical input with the same pair-sum profile.
-/

namespace DigitSumElevenClassification

open DecimalDigits DecimalMass FoldedDecimal Lychrel196

/-- Equal first successors have identical palindromic status at every
positive time; the input itself need not be the chosen representative. -/
theorem palindrome_at_of_first_step_eq (n r k : Nat)
    (hstep : step n = step r) (hk : 0 < k)
    (hpal : Palindrome (orbit r k)) : Palindrome (orbit n k) := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : k ≠ 0)
  rw [← orbit_from_step n j, hstep, orbit_from_step r j]
  exact hpal

set_option maxHeartbeats 2000000 in
/-- The center-eight, outer-mass-three profile at widths three and five. -/
theorem outer_eight_small (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hsmall : m < 3) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = outerColumns m 8 3 i) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 12 ∧ Palindrome (orbit n k) := by
  have hc : m = 1 ∨ m = 2 := by omega
  rcases hc with rfl | rfl
  · refine ⟨6, by decide, by decide,
      palindrome_at_of_first_step_eq n 380 6 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (outerColumns 1 8 3) 3 hcan hcols).trans (by decide)
  · refine ⟨4, by decide, by decide,
      palindrome_at_of_first_step_eq n 30800 4 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (outerColumns 2 8 3) 5 hcan hcols).trans (by decide)

set_option maxHeartbeats 2000000 in
/-- The center-eight adjacent-mass-two profile at widths five and seven. -/
theorem near_eight_small (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 2 ≤ m) (hsmall : m < 4) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = nearColumns m 8 2 i) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 12 ∧ Palindrome (orbit n k) := by
  have hc : m = 2 ∨ m = 3 := by omega
  rcases hc with rfl | rfl
  · refine ⟨8, by decide, by decide,
      palindrome_at_of_first_step_eq n 12800 8 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (nearColumns 2 8 2) 5 hcan hcols).trans (by decide)
  · refine ⟨6, by decide, by decide,
      palindrome_at_of_first_step_eq n 1028000 6 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (nearColumns 3 8 2) 7 hcan hcols).trans (by decide)

set_option maxHeartbeats 2000000 in
/-- The center-nine adjacent-mass-one profile at widths five and seven. -/
theorem near_nine_small (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 2 ≤ m) (hsmall : m < 4) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = nearColumns m 9 1 i) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 12 ∧ Palindrome (orbit n k) := by
  have hc : m = 2 ∨ m = 3 := by omega
  rcases hc with rfl | rfl
  · refine ⟨6, by decide, by decide,
      palindrome_at_of_first_step_eq n 11900 6 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (nearColumns 2 9 1) 5 hcan hcols).trans (by decide)
  · refine ⟨6, by decide, by decide,
      palindrome_at_of_first_step_eq n 1019000 6 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (nearColumns 3 9 1) 7 hcan hcols).trans (by decide)

set_option maxHeartbeats 2000000 in
/-- The center-nine outer-mass-two profile at widths three, five and seven.
Width nine is the separate exceptional profile; larger widths use a
parametric decimal-block trajectory. -/
theorem outer_nine_small (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hsmall : m < 4) (hcan : Canonical n d (2 * m + 1))
    (hcols : ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = outerColumns m 9 2 i) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 12 ∧ Palindrome (orbit n k) := by
  have hc : m = 1 ∨ m = 2 ∨ m = 3 := by omega
  rcases hc with rfl | rfl | rfl
  · refine ⟨4, by decide, by decide,
      palindrome_at_of_first_step_eq n 290 4 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (outerColumns 1 9 2) 3 hcan hcols).trans (by decide)
  · refine ⟨12, by decide, by decide,
      palindrome_at_of_first_step_eq n 20900 12 ?_ (by decide)
        DigitSumTenTermination.threshold_control_20900.2.2.2⟩
    exact (step_eq_word_value n d (outerColumns 2 9 2) 5 hcan hcols).trans (by decide)
  · refine ⟨10, by decide, by decide,
      palindrome_at_of_first_step_eq n 2009000 10 ?_ (by decide) (by decide)⟩
    exact (step_eq_word_value n d (outerColumns 3 9 2) 7 hcan hcols).trans (by decide)

end DigitSumElevenClassification
