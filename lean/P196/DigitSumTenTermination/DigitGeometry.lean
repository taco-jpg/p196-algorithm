import P196.DigitSumTenTermination.CarryMass

/-!
Digit-position separation and canonical width-three classifications for the
digit-sum-ten termination argument. All numeral identities use the existing
ordinary decimal representation.
-/

namespace DigitSumTenTermination

open DecimalDigits DecimalMass

/-- At width at least five, a pair adjacent to the center and the middle
digit omit the positive leading digit, so their mass bound is strict. -/
theorem neighbor_column_add_middle_lt_mass (d : Nat → Nat) (m : Nat)
    (hm : 2 ≤ m) (hlead : 0 < d (2 * m)) (i : Nat)
    (hi : i < 2 * m + 1) (hnear : i + 1 = m ∨ i = m + 1) :
    columnSum d (2 * m + 1) i + d m < wordSum d (2 * m + 1) := by
  have hmass := wordSum_four_le d (2 * m + 1)
    i (2 * m + 1 - 1 - i) m (2 * m)
    hi (by omega) (by omega) (by omega)
    (by omega) (by omega) (by omega)
    (by omega) (by omega) (by omega)
  simp only [columnSum, reflected]
  omega

/-- A canonical three-digit numeral of mass ten with middle digit eight
is either 181 or 280. -/
theorem width_three_middle_eight (n : Nat) (d : Nat → Nat)
    (hcan : Canonical n d 3) (hmass : wordSum d 3 = 10)
    (hmid : d 1 = 8) : n = 181 ∨ n = 280 := by
  have hlead : 0 < d 2 := by simpa using hcan.2.2.1
  have hsum := hmass
  simp [wordSum] at hsum
  have hvalue := hcan.2.2.2
  simp [value] at hvalue
  have hlead_cases : d 2 = 1 ∨ d 2 = 2 := by omega
  rcases hlead_cases with hlead_one | hlead_two
  · left
    omega
  · right
    omega

/-- A canonical three-digit numeral of mass ten with middle digit nine
is 190. -/
theorem width_three_middle_nine (n : Nat) (d : Nat → Nat)
    (hcan : Canonical n d 3) (hmass : wordSum d 3 = 10)
    (hmid : d 1 = 9) : n = 190 := by
  have hlead : 0 < d 2 := by simpa using hcan.2.2.1
  have hsum := hmass
  simp [wordSum] at hsum
  have hvalue := hcan.2.2.2
  simp [value] at hvalue
  omega

end DigitSumTenTermination
