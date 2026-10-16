import LeadingWitness
import DigitPerturbation

namespace ModularAutonomy

open Lychrel196 DecimalDigits

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
    change (B + 9 * P) % M = (A + Q) % M at hh
    rw [Nat.add_mod B (9 * P) M, Nat.add_mod A Q M] at hh
    rw [hAC, hBD] at hh
    rw [← Nat.add_mod D (9 * P) M, ← Nat.add_mod C Q M, hsecond] at hh
    have he1 : C + P + 9 * P = C + 100 * Q := by omega
    simpa only [he1] using hh
  have hres := mod_cancel_add_left M C (100 * Q) Q hM hsum
  have hsum2 : (Q + 99 * Q) % M = (Q + 0) % M := by
    have he : Q + 99 * Q = 100 * Q := by omega
    simpa only [he, Nat.add_zero] using hres
  have hz := mod_cancel_add_left M Q (99 * Q) 0 hM hsum2
  exact Nat.dvd_of_mod_eq_zero hz

/-- Exact-width autonomy compares two neighboring pairs.  The first pair
crosses exactly one trailing nine, while the second pair has no carry. -/
theorem eventual_determinism_forces_scaled_99 (M : Nat) (hM : 0 < M)
    (hunit : M % 10 ≠ 0) (hdet : EventualReverseResidueDet M) :
    ∃ k, M ∣ 99 * 10 ^ k := by
  obtain ⟨B, hdet⟩ := hdet
  let L := B + M + 3
  have hL : 3 ≤ L := by dsimp [L]; omega
  have hBL : B ≤ L := by dsimp [L]; omega
  have hMQ : M ≤ 10 ^ (L - 2) := by
    have hp := self_le_ten_pow (L - 2)
    dsimp [L] at hp ⊢
    omega
  have hQ : 2 ≤ 10 ^ (L - 2) := by
    have hp := self_le_ten_pow (L - 2)
    dsimp [L] at hp ⊢
    omega
  have hpow : 10 ^ (L - 1) = 10 ^ (L - 2) * 10 := by
    have he : L - 1 = (L - 2) + 1 := by omega
    rw [he, Nat.pow_succ]
  have hpowL : 10 ^ L = 10 ^ (L - 1) * 10 := by
    have he : L = (L - 1) + 1 := by omega
    conv => lhs; rw [he, Nat.pow_succ]
  have hspace : M + 10 < 10 ^ (L - 1) := by omega
  have hpmod : 10 ^ (L - 1) % 10 = 0 := by rw [hpow]; omega
  have hunits : (10 ^ (L - 1) + 9 + M) % 10 ≤ 8 := by omega
  obtain ⟨e, he⟩ := canonical_of_pow_bounds (10 ^ (L - 1) + 9 + M) L
    (by omega) (by omega) (by rw [hpowL]; omega)
  have heplus := canonical_incrementUnits _ _ e he hunits
  have hn := single_nine_canonical L hL
  have hnplus := single_nine_successor_canonical L hL
  have hmod0 : (10 ^ (L - 1) + 9) % M =
      (10 ^ (L - 1) + 9 + M) % M := by omega
  have hmod1 : (10 ^ (L - 1) + 10) % M =
      (10 ^ (L - 1) + 9 + M + 1) % M := by
    have heq : 10 ^ (L - 1) + 9 + M + 1 = 10 ^ (L - 1) + 10 + M := by omega
    rw [heq]
    omega
  have hAC := hdet L hBL _ _ _ _ hn he hmod0
  have hBD := hdet L hBL _ _ _ _ hnplus heplus hmod1
  have hfirst := single_nine_reverse_increment L hL
  have hsecond := reverse10_succ_of_units_le_eight _ _ e he hunits
  refine ⟨L - 2, ?_⟩
  exact scaled_99_of_difference_residues M _ _ _ _ _ _ hM
    hAC hBD hfirst hsecond (by omega)

#print axioms gcd_ten_eq_one_of_not_two_not_five
#print axioms cancel_ten_power_from_scaled_99
#print axioms self_le_ten_pow
#print axioms mod_cancel_add_left
#print axioms scaled_99_of_difference_residues
#print axioms eventual_determinism_forces_scaled_99

end ModularAutonomy
