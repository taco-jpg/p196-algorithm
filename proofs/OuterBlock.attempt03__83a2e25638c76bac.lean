import Std

/-!
An outer decimal block representing a prescribed residue modulo a divisor
of a power of ten, with a nonzero units digit. All quantifiers concern
ordinary natural numbers. No factorization hypothesis is hidden in the
selection theorem: a proper positive divisor is at most half the dividend.
-/
namespace Agent111.ExactLengthResidues

/-- A positive proper divisor is at most half its positive dividend. -/
theorem twice_le_of_proper_dvd (u N : Nat) (hu : 0 < u)
    (hN : 0 < N) (hd : u ∣ N) (hne : u ≠ N) : 2 * u ≤ N := by
  obtain ⟨v, hv⟩ := hd
  have hv0 : 0 < v := by
    by_cases h : v = 0
    · simp [h] at hv
      omega
    · omega
  have hv1 : v ≠ 1 := by
    intro h
    simp [h] at hv
    exact hne hv.symm
  have hv2 : 2 ≤ v := by omega
  have hmul := Nat.mul_le_mul_left u hv2
  omega

/-- Every positive power of ten is divisible by ten. -/
theorem ten_dvd_pow (k : Nat) (hk : 1 ≤ k) : 10 ∣ 10 ^ k := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : k ≠ 0)
  rw [Nat.pow_succ, Nat.mul_comm]
  exact ⟨10 ^ j, rfl⟩

/-- Select a fixed-width outer block. It may have leading zero padding,
but its units digit is nonzero, so its reflection can be the leading block
of a positive palindrome. -/
theorem outer_block_exists (u k a : Nat) (hu : 0 < u) (hk : 1 ≤ k)
    (hdiv : u ∣ 10 ^ k) (hcompat : ¬ (10 ∣ u ∧ 10 ∣ a)) :
    ∃ A, A < 10 ^ k ∧ A % u = a % u ∧ A % 10 ≠ 0 := by
  have hpow : 0 < 10 ^ k := Nat.pow_pos (by decide)
  have hule : u ≤ 10 ^ k := Nat.le_of_dvd hpow hdiv
  have hr : a % u < u := Nat.mod_lt a hu
  by_cases hlast : (a % u) % 10 = 0
  · have hnot : ¬ 10 ∣ u := by
      intro h10
      have h10a : 10 ∣ a := (Nat.dvd_mod_iff h10).mp
        (Nat.dvd_of_mod_eq_zero hlast)
      exact hcompat ⟨h10, h10a⟩
    have hne : u ≠ 10 ^ k := by
      intro heq
      exact hnot (heq ▸ ten_dvd_pow k hk)
    have hhalf := twice_le_of_proper_dvd u (10 ^ k) hu hpow hdiv hne
    refine ⟨a % u + u, by omega, ?_, ?_⟩
    · simp
    · intro hzero
      have hboth : 10 ∣ a % u + u := Nat.dvd_of_mod_eq_zero hzero
      exact hnot ((Nat.dvd_add_iff_right (Nat.dvd_of_mod_eq_zero hlast)).mpr hboth)
  · exact ⟨a % u, by omega, Nat.mod_eq_of_lt hr, hlast⟩

#print axioms twice_le_of_proper_dvd
#print axioms ten_dvd_pow
#print axioms outer_block_exists


/-- Split a positive modulus into a factor dividing a power of ten and a
factor coprime to ten. The proof strips gcds with ten, without requiring
prime factorization. -/
theorem decimal_modulus_decomposition (M : Nat) (hM : 0 < M) :
    ∃ u q k, 0 < u ∧ 0 < q ∧ 1 ≤ k ∧ M = u * q ∧
      u ∣ 10 ^ k ∧ Nat.gcd q 10 = 1 := by
  induction M using Nat.strongRecOn with
  | ind M ih =>
    by_cases hc : Nat.gcd M 10 = 1
    · exact ⟨1, M, 1, by decide, hM, by decide, by simp, by simp, hc⟩
    · let g := Nat.gcd M 10
      have hg : 0 < g := Nat.gcd_pos_of_pos_right M (by decide)
      have hg2 : 1 < g := by dsimp [g]; omega
      have hgm : g ∣ M := Nat.gcd_dvd_left M 10
      have hgten : g ∣ 10 := Nat.gcd_dvd_right M 10
      have hquotpos : 0 < M / g := Nat.div_pos (Nat.le_of_dvd hM hgm) hg
      have hquotlt : M / g < M := Nat.div_lt_self hM hg2
      obtain ⟨u, q, k, hu, hq, hk, hMquot, hudiv, hqcop⟩ := ih (M / g) hquotlt hquotpos
      have heq : M = (g * u) * q := by
        calc
          M = g * (M / g) := (Nat.mul_div_cancel' hgm).symm
          _ = g * (u * q) := by rw [hMquot]
          _ = (g * u) * q := by simp [Nat.mul_assoc]
      have hdiv : g * u ∣ 10 ^ (k + 1) := by
        have h := Nat.mul_dvd_mul hgten hudiv
        simpa [Nat.pow_succ, Nat.mul_comm] using h
      exact ⟨g * u, q, k + 1, Nat.mul_pos hg hu, hq, by omega, heq, hdiv, hqcop⟩

/-- The two factors furnished above are automatically relatively prime. -/
theorem coprime_of_decimal_factor (u q k : Nat) (hu : u ∣ 10 ^ k)
    (hq : Nat.gcd q 10 = 1) : Nat.gcd u q = 1 := by
  have hpow : Nat.gcd q (10 ^ k) = 1 := Nat.gcd_pow_right_of_gcd_eq_one hq
  have hd : Nat.gcd u q ∣ Nat.gcd q (10 ^ k) :=
    Nat.dvd_gcd (Nat.gcd_dvd_right u q)
      (Nat.dvd_trans (Nat.gcd_dvd_left u q) hu)
  rw [hpow] at hd
  exact Nat.eq_one_of_dvd_one hd

/-- A bundled modulus split including the coprimality used to combine
congruences modulo its two factors. -/
theorem decimal_modulus_decomposition_coprime (M : Nat) (hM : 0 < M) :
    ∃ u q k, 0 < u ∧ 0 < q ∧ 1 ≤ k ∧ M = u * q ∧
      u ∣ 10 ^ k ∧ Nat.gcd q 10 = 1 ∧ Nat.gcd u q = 1 := by
  obtain ⟨u, q, k, hu, hq, hk, heq, hdiv, hcop⟩ := decimal_modulus_decomposition M hM
  exact ⟨u, q, k, hu, hq, hk, heq, hdiv, hcop, coprime_of_decimal_factor u q k hdiv hcop⟩

#print axioms decimal_modulus_decomposition
#print axioms coprime_of_decimal_factor
#print axioms decimal_modulus_decomposition_coprime

end Agent111.ExactLengthResidues

