import Saturation

namespace ExactLengthResidues

open Lychrel196 DecimalDigits

theorem two_five_factor_dvd_ten_pow (alpha beta k : Nat)
    (halpha : alpha ≤ k) (hbeta : beta ≤ k) :
    2 ^ alpha * 5 ^ beta ∣ 10 ^ k := by
  have hd := Nat.mul_dvd_mul (Nat.pow_dvd_pow 2 halpha)
    (Nat.pow_dvd_pow 5 hbeta)
  rw [← Nat.mul_pow] at hd
  exact hd

theorem saturation_explicit_bound (alpha beta q r : Nat)
    (hq : 0 < q) (hcop : Nat.gcd q 10 = 1)
    (hr : 0 < r) (hperiod : 10 ^ r % q = 1 % q) :
    SaturationAbove ((2 ^ alpha * 5 ^ beta) * q)
      (2 * max 1 (max alpha beta) + 4 * q * r) := by
  let k := max 1 (max alpha beta)
  let u := 2 ^ alpha * 5 ^ beta
  have hk : 1 ≤ k := Nat.le_max_left _ _
  have halpha : alpha ≤ k :=
    Nat.le_trans (Nat.le_max_left alpha beta) (Nat.le_max_right 1 (max alpha beta))
  have hbeta : beta ≤ k :=
    Nat.le_trans (Nat.le_max_right alpha beta) (Nat.le_max_right 1 (max alpha beta))
  have hu : 0 < u := Nat.mul_pos (Nat.pow_pos (by decide)) (Nat.pow_pos (by decide))
  have hdiv : u ∣ 10 ^ k := two_five_factor_dvd_ten_pow alpha beta k halpha hbeta
  exact saturation_of_split (u * q) k u q r hk hu hq rfl hdiv
    (coprime_of_decimal_factor u q k hdiv hcop) hr hperiod

theorem exact_length_palindrome_residues_explicit (alpha beta q r L a : Nat)
    (hq : 0 < q) (hcop : Nat.gcd q 10 = 1)
    (hr : 0 < r) (hperiod : 10 ^ r % q = 1 % q)
    (hL : 2 * max 1 (max alpha beta) + 4 * q * r ≤ L) :
    (∃ p d, 0 < p ∧ Canonical p d L ∧ Palindrome p ∧
      p % ((2 ^ alpha * 5 ^ beta) * q) = a % ((2 ^ alpha * 5 ^ beta) * q)) ↔
      (¬ (10 ∣ (2 ^ alpha * 5 ^ beta) * q ∧ 10 ∣ a) ∧
        (L % 2 = 0 → Nat.gcd ((2 ^ alpha * 5 ^ beta) * q) 11 ∣ a)) := by
  exact palindrome_residue_iff_of_saturation
    ((2 ^ alpha * 5 ^ beta) * q)
    (2 * max 1 (max alpha beta) + 4 * q * r) L a
    (saturation_explicit_bound alpha beta q r hq hcop hr hperiod) hL

end ExactLengthResidues

#print axioms ExactLengthResidues.two_five_factor_dvd_ten_pow
#print axioms ExactLengthResidues.saturation_explicit_bound
#print axioms ExactLengthResidues.exact_length_palindrome_residues_explicit
