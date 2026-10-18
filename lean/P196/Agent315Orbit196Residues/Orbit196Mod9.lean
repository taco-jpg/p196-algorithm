import P196.Foundations.LychrelDigitSums

namespace Agent315.TemporalColumn99

open Lychrel196

/-- The 196 orbit is trapped forever in the six nonzero units of Z/9Z.
Since 196 ≡ 7 (mod 9) and every reverse-and-add step doubles the residue,
the residue can never become 0 modulo 9. -/
theorem orbit196_mod9_ne_zero (k : Nat) :
    orbit 196 k % 9 ≠ 0 := by
  induction k with
  | zero => decide
  | succ k ih =>
      have hs := step_mod9 (orbit 196 k)
      change step (orbit 196 k) % 9 ≠ 0
      rw [hs]
      omega

/-- Consequently the actual 196 orbit never enters the 9-divisible class. -/
theorem not_dvd9_orbit196 (k : Nat) :
    ¬ 9 ∣ orbit 196 k := by
  intro h
  have hz := Nat.mod_eq_zero_of_dvd h
  exact orbit196_mod9_ne_zero k hz

#print axioms orbit196_mod9_ne_zero
#print axioms not_dvd9_orbit196

end Agent315.TemporalColumn99
