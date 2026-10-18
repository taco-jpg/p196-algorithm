import P196.Foundations.LychrelDigitSums

namespace Agent315.TemporalColumn99

open Lychrel196

/-- The 196 orbit never becomes divisible by 3.  This is the exact
modulo-3 shadow of the modulo-9 doubling law: 196 ≡ 1 (mod 3), and
multiplication by 2 permutes the two nonzero classes. -/
theorem orbit196_mod3_ne_zero (k : Nat) :
    orbit 196 k % 3 ≠ 0 := by
  induction k with
  | zero => decide
  | succ k ih =>
      have hs := step_mod9 (orbit 196 k)
      have hs3 := congrArg (fun x : Nat => x % 3) hs
      have hm : orbit 196 (k + 1) % 3 =
          (2 * orbit 196 k) % 3 := by
        change step (orbit 196 k) % 3 = _
        simpa only [Nat.mod_mod_of_dvd _ (by decide : 3 ∣ 9)] using hs3
      rw [hm]
      omega

/-- The corresponding integer-dynamics restriction. -/
theorem not_dvd3_orbit196 (k : Nat) :
    ¬ 3 ∣ orbit 196 k := by
  intro h
  exact orbit196_mod3_ne_zero k (Nat.mod_eq_zero_of_dvd h)

end Agent315.TemporalColumn99
