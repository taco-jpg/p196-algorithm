import P196.Drafts.Agent1CeilhalfVerification.OuterBlock

namespace ExactLengthResidues

/-- Split a positive modulus into a factor dividing a power of ten and a
factor coprime to ten. The proof strips gcds with ten, without requiring
prime factorization. -/
theorem decimal_modulus_decomposition (M : Nat) (hM : 0 < M) :
    ∃ k u q, 1 ≤ k ∧ 0 < u ∧ 0 < q ∧ M = u * q ∧
      u ∣ 10 ^ k ∧ Nat.gcd q 10 = 1 := by
  induction M using Nat.strongRecOn with
  | ind M ih =>
    by_cases hc : Nat.gcd M 10 = 1
    · exact ⟨1, 1, M, by decide, by decide, hM, by simp, by simp, hc⟩
    · let g := Nat.gcd M 10
      have hg : 0 < g := Nat.gcd_pos_of_pos_right M (by decide)
      have hg2 : 1 < g := by dsimp [g]; omega
      have hgm : g ∣ M := Nat.gcd_dvd_left M 10
      have hgten : g ∣ 10 := Nat.gcd_dvd_right M 10
      have hquotpos : 0 < M / g := Nat.div_pos (Nat.le_of_dvd hM hgm) hg
      have hquotlt : M / g < M := Nat.div_lt_self hM hg2
      obtain ⟨k, u, q, hk, hu, hq, hMquot, hudiv, hqcop⟩ := ih (M / g) hquotlt hquotpos
      have heq : M = (g * u) * q := by
        calc
          M = g * (M / g) := (Nat.mul_div_cancel' hgm).symm
          _ = g * (u * q) := by rw [hMquot]
          _ = (g * u) * q := by simp [Nat.mul_assoc]
      have hdiv : g * u ∣ 10 ^ (k + 1) := by
        have h := Nat.mul_dvd_mul hgten hudiv
        simpa [Nat.pow_succ, Nat.mul_comm] using h
      exact ⟨k + 1, g * u, q, by omega, Nat.mul_pos hg hu, hq, heq, hdiv, hqcop⟩

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
    ∃ k u q, 1 ≤ k ∧ 0 < u ∧ 0 < q ∧ M = u * q ∧
      u ∣ 10 ^ k ∧ Nat.gcd q 10 = 1 ∧ Nat.gcd u q = 1 := by
  obtain ⟨k, u, q, hk, hu, hq, heq, hdiv, hcop⟩ := decimal_modulus_decomposition M hM
  exact ⟨k, u, q, hk, hu, hq, heq, hdiv, hcop, coprime_of_decimal_factor u q k hdiv hcop⟩

#print axioms decimal_modulus_decomposition
#print axioms coprime_of_decimal_factor
#print axioms decimal_modulus_decomposition_coprime

end ExactLengthResidues

