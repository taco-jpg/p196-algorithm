import Std

namespace ModularAutonomy

theorem gcd_ten_eq_one_of_not_two_not_five (M : Nat)
    (h2 : ¬ 2 ∣ M) (h5 : ¬ 5 ∣ M) : Nat.gcd M 10 = 1 := by
  have hr2 : M % 10 % 2 ≠ 0 := by
    rw [Nat.mod_mod_of_dvd M (show 2 ∣ 10 by decide)]
    exact fun h => h2 (Nat.dvd_of_mod_eq_zero h)
  have hr5 : M % 10 % 5 ≠ 0 := by
    rw [Nat.mod_mod_of_dvd M (show 5 ∣ 10 by decide)]
    exact fun h => h5 (Nat.dvd_of_mod_eq_zero h)
  have hr : M % 10 = 1 ∨ M % 10 = 3 ∨ M % 10 = 7 ∨ M % 10 = 9 := by
    omega
  rw [Nat.gcd_comm, Nat.gcd_rec]
  rcases hr with hr | hr | hr | hr <;> rw [hr] <;> decide

theorem cancel_ten_power_from_scaled_99 (M k : Nat)
    (hcop : Nat.gcd M 10 = 1) (hdiv : M ∣ 99 * 10 ^ k) : M ∣ 99 := by
  have hpow : Nat.gcd M (10 ^ k) = 1 :=
    Nat.gcd_pow_right_of_gcd_eq_one hcop
  have h := Nat.dvd_mul_gcd_iff_dvd_mul.mpr hdiv
  simpa only [hpow, Nat.mul_one] using h

theorem self_le_ten_pow (n : Nat) : n ≤ 10 ^ n := by
  induction n with
  | zero => decide
  | succ n ih =>
    have hp : 0 < 10 ^ n := Nat.pow_pos (by decide)
    rw [Nat.pow_succ]
    omega

theorem mod_cancel_add_left (M c a b : Nat) (hM : 0 < M)
    (h : (c + a) % M = (c + b) % M) : a % M = b % M := by
  have ha := Nat.mod_add_mod_eq (a := c) (b := a) (c := M)
  have hb := Nat.mod_add_mod_eq (a := c) (b := b) (c := M)
  have hlt_a := Nat.mod_lt a hM
  have hlt_b := Nat.mod_lt b hM
  split at ha <;> split at hb <;> omega

theorem scaled_99_of_difference_residues
    (M A B C D P Q : Nat) (hM : 0 < M)
    (hAC : A % M = C % M) (hBD : B % M = D % M)
    (hfirst : B + 9 * P = A + Q) (hsecond : D = C + P)
    (hPQ : P = 10 * Q) : M ∣ 99 * Q := by
  have hsum : (C + 100 * Q) % M = (C + Q) % M := by
    have hh := congrArg (fun x => x % M) hfirst
    rw [Nat.add_mod, Nat.add_mod, hAC, hBD, hsecond] at hh
    rw [← Nat.add_mod, ← Nat.add_mod] at hh
    have he1 : C + P + 9 * P = C + 100 * Q := by omega
    simpa only [he1] using hh
  have hres := mod_cancel_add_left M C (100 * Q) Q hM hsum
  have hsum2 : (Q + 99 * Q) % M = (Q + 0) % M := by
    have he : Q + 99 * Q = 100 * Q := by omega
    simpa only [he, Nat.add_zero] using hres
  have hz := mod_cancel_add_left M Q (99 * Q) 0 hM hsum2
  exact Nat.dvd_of_mod_eq_zero hz

#print axioms gcd_ten_eq_one_of_not_two_not_five
#print axioms cancel_ten_power_from_scaled_99
#print axioms self_le_ten_pow
#print axioms mod_cancel_add_left
#print axioms scaled_99_of_difference_residues

end ModularAutonomy
