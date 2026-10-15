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

end Agent111.ExactLengthResidues
