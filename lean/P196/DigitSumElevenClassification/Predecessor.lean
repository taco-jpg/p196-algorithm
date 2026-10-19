import P196.DigitSumElevenClassification.EasyCases

/-!
The exceptional width-nine seeds coalesce after one step. The
nonpalindromic seed 200090000 cannot itself be a positive step output:
an output ending in zero forces an input outer pair sum of ten and hence
an overflowing output with leading digit one.

The finite controls below assert avoidance only through time twelve.
-/

namespace DigitSumElevenClassification

open DecimalDigits DecimalMass FoldedDecimal Lychrel196 DigitSumTenTermination

/-- A zero units digit in a positive ordinary output forces outer
input pair coefficient ten. -/
theorem outer_column_ten_of_zero_units
    (n : Nat) (d : Nat → Nat) (L : Nat) (hcan : Canonical n d L)
    (hz : step n % 10 = 0) : columnSum d L 0 = 10 := by
  have hLpos := hcan.1
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  have hd0 := hcan.2.1 0 (by omega)
  have hdk := hcan.2.1 k (by omega)
  have hlead : 0 < d k := by simpa using hcan.2.2.1
  have hmod : n % 10 = d 0 := by
    rw [← hcan.2.2.2, value_shift]
    omega
  have hrev : reverse10 n % 10 = d k := by
    simpa using AstraModular.reverse10_mod10 n d (k + 1) hcan
  have hpair : (d 0 + d k) % 10 = 0 := by
    calc
      (d 0 + d k) % 10 = (n % 10 + reverse10 n % 10) % 10 := by rw [hmod, hrev]
      _ = (n + reverse10 n) % 10 := (Nat.add_mod n (reverse10 n) 10).symm
      _ = 0 := hz
  have hsum : d 0 + d k = 10 := by omega
  simpa only [columnSum, reflected, Nat.add_sub_cancel, Nat.sub_zero] using hsum

/-- The exceptional nonpalindromic seed has no positive ordinary
reverse-and-add predecessor. -/
theorem no_positive_predecessor_exception (n : Nat) (hn : 0 < n) :
    step n ≠ 200090000 := by
  intro hstep
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hLpos := hcan.1
  have houter := outer_column_ten_of_zero_units n d L hcan (by rw [hstep])
  have hlast : 10 ≤ columnSum d L (L - 1) := by
    have hsym := columnSum_symmetric d L 0 (by omega)
    have heq : columnSum d L (L - 1) = 10 := by
      simpa only [Nat.sub_zero, houter] using hsym.symm
    omega
  have hcarry_low := one_le_carry_of_high_column (columnSum d L) (L - 1) hlast
  have hcarry_high := carry_bounded (columnSum d L) L
    (columnSum_bounded d L hcan.2.1) L (Nat.le_refl L)
  have hindex : L - 1 + 1 = L := by omega
  rw [hindex] at hcarry_low
  have hcarry : carry (columnSum d L) L = 1 := by omega
  have hnext := canonical_next_overflow n d L hcan hcarry
  have hlength := DecimalQuantitativeMass.decimalLength_of_canonical
    (step n) (extended (columnSum d L) L) (L + 1) hnext
  have htarget_length : DecimalQuantitativeMass.decimalLength 200090000 = 9 := by
    simp [DecimalQuantitativeMass.decimalLength]
  rw [hstep, htarget_length] at hlength
  have hL : L = 8 := by omega
  subst L
  have hvalue := hnext.2.2.2
  rw [hstep] at hvalue
  have h0 := output_bounded (columnSum d 8) 0
  have h1 := output_bounded (columnSum d 8) 1
  have h2 := output_bounded (columnSum d 8) 2
  have h3 := output_bounded (columnSum d 8) 3
  have h4 := output_bounded (columnSum d 8) 4
  have h5 := output_bounded (columnSum d 8) 5
  have h6 := output_bounded (columnSum d 8) 6
  have h7 := output_bounded (columnSum d 8) 7
  simp only [value, extended, Nat.reduceLT, if_pos, if_false, hcarry,
    Nat.reducePow, Nat.zero_add, Nat.mul_one, Nat.one_mul] at hvalue
  omega

/-- Both exceptional seeds have digit sum eleven; the smaller seed is
already a palindrome at time zero. -/
theorem exceptional_seed_controls :
    digitSum 100090001 = 11 ∧ digitSum 200090000 = 11 ∧ Palindrome 100090001 := by
  exact ⟨by simp [digitSum], by simp [digitSum], by decide⟩

/-- The two exceptional inputs have the same first ordinary step. -/
theorem exceptional_steps :
    step 100090001 = 200180002 ∧ step 200090000 = 200180002 := by
  decide

/-- Their ordinary orbits agree at every positive time. -/
theorem exceptional_orbits_coalesce (k : Nat) :
    orbit 100090001 (k + 1) = orbit 200090000 (k + 1) := by
  calc
    orbit 100090001 (k + 1) = orbit (step 100090001) k :=
      (orbit_from_step 100090001 k).symm
    _ = orbit (step 200090000) k := by rw [exceptional_steps.1, exceptional_steps.2]
    _ = orbit 200090000 (k + 1) := orbit_from_step 200090000 k

/-- Neither exceptional input reaches a palindrome at positive times
one through twelve; 200090000 is also nonpalindromic at time zero. -/
theorem exceptional_positive_prefix :
    (∀ k, 1 ≤ k → k ≤ 12 → ¬ Palindrome (orbit 100090001 k)) ∧
    (∀ k, k ≤ 12 → ¬ Palindrome (orbit 200090000 k)) := by
  have hfree := noPalindromeFor_sound 13 200090000 (by decide)
  constructor
  · intro k hkpos hkbound
    have heq := exceptional_orbits_coalesce (k - 1)
    have hindex : k - 1 + 1 = k := by omega
    rw [hindex] at heq
    rw [heq]
    exact hfree k (by omega)
  · intro k hkbound
    exact hfree k (by omega)

end DigitSumElevenClassification
