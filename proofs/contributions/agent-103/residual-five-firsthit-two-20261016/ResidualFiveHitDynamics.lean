import ResidualFiveFiberConclusion

/-!
# Positive first palindrome time for the residual-five fiber

Agent #103, task `agent103-residual-five-firsthit-two-20261016`.

Every ordinary member of the complete fiber reaches the same intermediate
integer and then the residual-five palindrome.  The intermediate integer has
unequal end digits.  Therefore each fiber member has first positive palindrome
time exactly two.
These statements include `r = 0`; the initial value at time zero is handled
separately.
-/

set_option autoImplicit false

namespace Agent103.ResidualFiveHitDynamics

open Lychrel196 DecimalDigits FoldedDecimal
open Agent119.EightFamilies Agent103.ResidualFive
open Agent103.ResidualFiveFibers

/-- The mirrored digits of `33 0^(2r) 22` sum to `55 0^(2r) 55`. -/
theorem middle_columns (r i : Nat) (hi : i < 2 * r + 4) :
    columnSum (fiveOutputDigit r) (2 * r + 4) i = famDigit 5 r i := by
  unfold columnSum reflected fiveOutputDigit famDigit
  split <;> (try split) <;> (try split) <;> (try split) <;> (try split) <;> omega

/-- The next ordinary reverse-and-add step is the residual-five palindrome. -/
theorem middle_step (r : Nat) : step (middle r) = fam 5 r := by
  calc
    step (middle r) = value (famDigit 5 r) (2 * r + 4) :=
      step_eq_word_value (middle r) (fiveOutputDigit r) (famDigit 5 r)
        (2 * r + 4) (middle_canonical r) (middle_columns r)
    _ = fam 5 r := fam_value 5 r

/-- Its units digit is two while its most significant digit is three. -/
theorem middle_nonpalindrome (r : Nat) : ¬ Palindrome (middle r) := by
  intro hp
  have hc := middle_canonical r
  have hsym := (palindrome_value_iff (fiveOutputDigit r) (2 * r + 4)
    hc.2.1 (Or.inr hc.2.2.1)).mp (by simpa only [hc.2.2.2] using hp)
  have hedge := hsym 0 (by omega)
  rw [fiveOutputDigit_zero,
    show 2 * r + 4 - 1 - 0 = 2 * r + 3 by omega,
    fiveOutputDigit_hi0] at hedge
  omega

/-- The full ordinary-integer fiber has this common value at time one. -/
theorem fiber_orbit_one (r n : Nat) (hn : n ∈ fiber r) :
    orbit n 1 = middle r :=
  (fiber_mem_iff r n).mp hn

/-- The full ordinary-integer fiber has this common value at time two. -/
theorem fiber_orbit_two (r n : Nat) (hn : n ∈ fiber r) :
    orbit n 2 = fam 5 r := by
  change step (orbit n 1) = fam 5 r
  rw [fiber_orbit_one r n hn, middle_step]

theorem fiber_time_one_nonpalindrome (r n : Nat) (hn : n ∈ fiber r) :
    ¬ Palindrome (orbit n 1) := by
  rw [fiber_orbit_one r n hn]
  exact middle_nonpalindrome r

theorem fiber_time_two_palindrome (r n : Nat) (hn : n ∈ fiber r) :
    Palindrome (orbit n 2) := by
  rw [fiber_orbit_two r n hn]
  exact fam_palindrome 5 r (by decide) (by decide)

/-- First positive palindrome time two, in the original orbit semantics. -/
theorem fiber_first_positive_two (r n : Nat) (hn : n ∈ fiber r) :
    ¬ Palindrome (orbit n 1) ∧ Palindrome (orbit n 2) :=
  ⟨fiber_time_one_nonpalindrome r n hn, fiber_time_two_palindrome r n hn⟩

/-- The only strictly positive time below two is excluded explicitly. -/
theorem fiber_no_positive_palindrome_before_two (r n : Nat) (hn : n ∈ fiber r)
    (k : Nat) (hk0 : 0 < k) (hk2 : k < 2) : ¬ Palindrome (orbit n k) := by
  have hk : k = 1 := by omega
  simpa only [hk] using fiber_time_one_nonpalindrome r n hn

#print axioms middle_columns
#print axioms middle_step
#print axioms middle_nonpalindrome
#print axioms fiber_orbit_one
#print axioms fiber_orbit_two
#print axioms fiber_time_one_nonpalindrome
#print axioms fiber_time_two_palindrome
#print axioms fiber_first_positive_two
#print axioms fiber_no_positive_palindrome_before_two

end Agent103.ResidualFiveHitDynamics
