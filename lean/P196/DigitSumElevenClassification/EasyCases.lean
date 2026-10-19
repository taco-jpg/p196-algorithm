import P196.DigitSumTenTermination.Main

/-!
Two-carry reduction at digit sum eleven and the isolated-center cases
with middle digit five, six, or seven. All conclusions use the ordinary
integer reverse-and-add map through the existing canonical digit bridge.
-/

namespace DigitSumElevenClassification

open DecimalDigits DecimalMass FoldedDecimal Lychrel196
open LowDigitSumTermination DigitSumTenTermination

/-- A high noncentral pair at digit sum at most eleven leaves mass at
most four after one step, so the second step is palindromic. -/
theorem second_step_palindrome_of_noncentral_high
    (n : Nat) (d : Nat → Nat) (L i : Nat)
    (hcan : Canonical n d L) (hs : digitSum n ≤ 11)
    (hi : i < L) (hne : i ≠ L - 1 - i)
    (hq : 10 ≤ columnSum d L i) : Palindrome (step (step n)) := by
  have hreflect : 10 ≤ columnSum d L (L - 1 - i) := by
    rw [← columnSum_symmetric d L i hi]
    exact hq
  have hmass := digitSum_step_add_eighteen_le n d L i (L - 1 - i)
    hcan hi (by omega) hne hq hreflect
  have hn : 0 < n := by
    rw [← hcan.2.2.2]
    exact value_positive d L hcan.1 hcan.2.2.1
  exact step_palindrome_of_digitSum_le_four (step n) (by unfold step; omega) (by omega)

/-- An exterior coefficient at least five, beside an isolated high
center, creates two successor carries. At initial mass eleven this leaves
mass at most eight after two actual steps. -/
theorem second_mass_le_eight_of_high_exterior
    (n : Nat) (d : Nat → Nat) (m i : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hs : digitSum n ≤ 11)
    (hlo : 10 ≤ columnSum d (2 * m + 1) m)
    (hhi : columnSum d (2 * m + 1) m ≤ 18)
    (hsmall : ∀ j, j < 2 * m + 1 → j ≠ m →
      columnSum d (2 * m + 1) j ≤ 8)
    (hi : i < 2 * m + 1) (hic : i ≠ m)
    (hlarge : 5 ≤ columnSum d (2 * m + 1) i) :
    digitSum (step (step n)) ≤ 8 := by
  let q := columnSum d (2 * m + 1)
  have hc : carry q (2 * m + 1) = 0 :=
    central_carry_no_overflow q m hm hlo hhi hsmall
  have hcan' := canonical_next_no_overflow n d (2 * m + 1) hcan hc
  have hnext := central_next_exterior_exact q m hm hlo hhi hsmall
    (columnSum_symmetric d (2 * m + 1)) i hi hic
  simp only [nextColumns, hc, ite_true] at hnext
  have hhigh : 10 ≤ columnSum (output q) (2 * m + 1) i := by
    change 5 ≤ q i at hlarge
    omega
  have hreflect : 10 ≤ columnSum (output q) (2 * m + 1)
      (2 * m + 1 - 1 - i) := by
    rw [← columnSum_symmetric (output q) (2 * m + 1) i hi]
    exact hhigh
  have hone := digitSum_step_add_nine_le n d (2 * m + 1) m hcan (by omega) hlo
  have htwo := digitSum_step_add_eighteen_le (step n) (output q) (2 * m + 1)
    i (2 * m + 1 - 1 - i) hcan' hi (by omega) (by omega) hhigh hreflect
  omega

/-- A high center of at most fourteen and exterior pairs at most six
reach a palindrome within five positive steps at digit sum eleven. -/
theorem central_small_within_five
    (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hs : digitSum n ≤ 11)
    (hlo : 10 ≤ columnSum d (2 * m + 1) m)
    (hhi : columnSum d (2 * m + 1) m ≤ 14)
    (hsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 6) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 5 ∧ Palindrome (orbit n k) := by
  classical
  by_cases hfour : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 4
  · exact ⟨2, by decide, by decide,
      central_two_steps_palindrome n d m hm hcan hlo hhi hfour⟩
  have hex : ∃ i, i < 2 * m + 1 ∧ i ≠ m ∧
      5 ≤ columnSum d (2 * m + 1) i := by
    apply Classical.byContradiction
    intro hnone
    apply hfour
    intro i hi hic
    by_cases hb : columnSum d (2 * m + 1) i ≤ 4
    · exact hb
    · exact False.elim (hnone ⟨i, hi, hic, by omega⟩)
  obtain ⟨i, hi, hic, hlarge⟩ := hex
  have hmass := second_mass_le_eight_of_high_exterior n d m i hm hcan hs hlo
    (by omega) (fun j hj hjc => by have h := hsmall j hj hjc; omega) hi hic hlarge
  have hn : 0 < n := by
    rw [← hcan.2.2.2]
    exact value_positive d (2 * m + 1) hcan.1 hcan.2.2.1
  obtain ⟨k, hkpos, hkbound, hpal⟩ := palindrome_within_three_of_digitSum_le_nine
    (orbit n 2) (orbit_positive n hn 2) (by simpa only [orbit] using Nat.le_trans hmass (by decide : 8 ≤ 9))
  refine ⟨2 + k, by omega, by omega, ?_⟩
  simpa only [LychrelCertificates.orbit_add] using hpal

end DigitSumElevenClassification
