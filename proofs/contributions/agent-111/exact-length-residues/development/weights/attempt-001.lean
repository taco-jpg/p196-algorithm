import Std

namespace ExactLengthResidues

def pairWeight0 (L : Nat) : Nat := 1 + 10 ^ (L - 1)

def pairWeight1 (L : Nat) : Nat := 10 + 10 ^ (L - 2)

theorem ten_pow_mod99 (n : Nat) :
    10 ^ n % 99 = if n % 2 = 0 then 1 else 10 := by
  induction n with
  | zero => decide
  | succ n ih =>
    rw [Nat.pow_succ, Nat.mul_mod, ih]
    by_cases h : n % 2 = 0
    · have hs : (n + 1) % 2 ≠ 0 := by omega
      simp [h, hs]
    · have hs : (n + 1) % 2 = 0 := by omega
      simp [h, hs]

theorem pair_weights_identity (L : Nat) (hL : 2 ≤ L) :
    10 * pairWeight1 L = pairWeight0 L + 99 := by
  have he : L - 1 = (L - 2) + 1 := by omega
  simp only [pairWeight0, pairWeight1, he, Nat.pow_succ]
  omega

theorem pairWeight0_mod99 (L : Nat) (hL : 2 ≤ L) :
    pairWeight0 L % 99 = if L % 2 = 0 then 11 else 2 := by
  unfold pairWeight0
  rw [Nat.add_mod, ten_pow_mod99]
  by_cases h : L % 2 = 0
  · have he : (L - 1) % 2 ≠ 0 := by omega
    simp [h, he]
  · have he : (L - 1) % 2 = 0 := by omega
    simp [h, he]

theorem pairWeight1_mod99 (L : Nat) (hL : 2 ≤ L) :
    pairWeight1 L % 99 = if L % 2 = 0 then 11 else 20 := by
  unfold pairWeight1
  rw [Nat.add_mod, ten_pow_mod99]
  by_cases h : L % 2 = 0
  · have he : (L - 2) % 2 = 0 := by omega
    simp [h, he]
  · have he : (L - 2) % 2 ≠ 0 := by omega
    simp [h, he]

theorem pair_weights_gcd (L : Nat) (hL : 2 ≤ L) :
    Nat.gcd (pairWeight0 L) (pairWeight1 L) =
      if L % 2 = 0 then 11 else 1 := by
  let g := Nat.gcd (pairWeight0 L) (pairWeight1 L)
  have hleft : g ∣ pairWeight0 L := Nat.gcd_dvd_left _ _
  have hright : g ∣ pairWeight1 L := Nat.gcd_dvd_right _ _
  have hidentity : 10 * pairWeight1 L - pairWeight0 L = 99 := by
    have := pair_weights_identity L hL
    omega
  have hd : g ∣ 99 := by
    have hmul := Nat.dvd_trans hright (Nat.dvd_mul_left (pairWeight1 L) 10)
    have hsub := Nat.dvd_sub hmul hleft
    rwa [hidentity] at hsub
  have hg99 : Nat.gcd 99 (pairWeight0 L) =
      if L % 2 = 0 then 11 else 1 := by
    rw [Nat.gcd_rec, pairWeight0_mod99 L hL]
    by_cases h : L % 2 = 0 <;> simp [h]
  apply Nat.dvd_antisymm
  · have hupper := Nat.dvd_gcd hd hleft
    rwa [hg99] at hupper
  · by_cases h : L % 2 = 0
    · simp only [if_pos h]
      apply Nat.dvd_gcd
      · apply Nat.dvd_of_mod_eq_zero
        have hmod := Nat.mod_mod_of_dvd (pairWeight0 L) (show 11 ∣ 99 by decide)
        rw [pairWeight0_mod99 L hL, if_pos h] at hmod
        omega
      · apply Nat.dvd_of_mod_eq_zero
        have hmod := Nat.mod_mod_of_dvd (pairWeight1 L) (show 11 ∣ 99 by decide)
        rw [pairWeight1_mod99 L hL, if_pos h] at hmod
        omega
    · simp [h]

theorem pair_weights_gcd_modulus (q L : Nat) (hL : 2 ≤ L) :
    Nat.gcd q (Nat.gcd (pairWeight0 L) (pairWeight1 L)) =
      if L % 2 = 0 then Nat.gcd q 11 else 1 := by
  rw [pair_weights_gcd L hL]
  by_cases h : L % 2 = 0 <;> simp [h]

end ExactLengthResidues

#print axioms ExactLengthResidues.pairWeight0
#print axioms ExactLengthResidues.pairWeight1
#print axioms ExactLengthResidues.ten_pow_mod99
#print axioms ExactLengthResidues.pair_weights_identity
#print axioms ExactLengthResidues.pairWeight0_mod99
#print axioms ExactLengthResidues.pairWeight1_mod99
#print axioms ExactLengthResidues.pair_weights_gcd
#print axioms ExactLengthResidues.pair_weights_gcd_modulus
