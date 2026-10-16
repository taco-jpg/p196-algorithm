import Std

/-!
Mirror-pair coefficients for exact-length decimal residue saturation.

For L ≥ 2, the two reference weights have gcd exactly 11 at even
length and exactly 1 at odd length. This result is independent of the
modulus and therefore rules out every higher mandatory power of 11.
The second group of lemmas transports the weights along a multiplicative
period of 10. No coprimality or positivity hypothesis is needed there
once the period equation is supplied.
-/

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

/-- The exact integer relation behind the gcd computation. -/
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

/-- The coefficient gcd is exact, with no modulus hypothesis. -/
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

/-- The claimed three-way gcd, even when the modulus is not coprime to 10. -/
theorem pair_weights_gcd_modulus (q L : Nat) (hL : 2 ≤ L) :
    Nat.gcd q (Nat.gcd (pairWeight0 L) (pairWeight1 L)) =
      if L % 2 = 0 then Nat.gcd q 11 else 1 := by
  rw [pair_weights_gcd L hL]
  by_cases h : L % 2 = 0 <;> simp [h]




 /-- Reduce an exponent modulo any supplied multiplicative period. -/
theorem pow_mod_reduce_period (a q r i : Nat)
    (hperiod : a ^ r % q = 1 % q) :
    a ^ i % q = a ^ (i % r) % q := by
  have hp : ∀ n : Nat, (a ^ r) ^ n % q = 1 % q := by
    intro n
    induction n with
    | zero => rfl
    | succ n ih =>
      rw [Nat.pow_succ, Nat.mul_mod, ih, hperiod, ← Nat.mul_mod, Nat.mul_one]
  calc
    a ^ i % q = a ^ (i % r + r * (i / r)) % q := by rw [Nat.mod_add_div]
    _ = (a ^ (i % r) % q * ((a ^ r) ^ (i / r) % q)) % q := by
      rw [Nat.pow_add, Nat.pow_mul, Nat.mul_mod]
    _ = (a ^ (i % r) % q * (1 % q)) % q := by rw [hp]
    _ = a ^ (i % r) % q := by rw [← Nat.mul_mod, Nat.mul_one]

 theorem pow_mod_period (a q r i j : Nat)
    (hperiod : a ^ r % q = 1 % q)
    (hij : i % r = j % r) :
    a ^ i % q = a ^ j % q := by
  rw [pow_mod_reduce_period a q r i hperiod,
    pow_mod_reduce_period a q r j hperiod, hij]


theorem ten_pow_mod_period (q r i j : Nat)
    (hperiod : 10 ^ r % q = 1 % q)
    (hij : i % r = j % r) :
    10 ^ i % q = 10 ^ j % q :=
  pow_mod_period 10 q r i j hperiod hij

private theorem weight_add_mod_left_cancel (a b c m : Nat)
    (h : (a + b) % m = (a + c) % m) : b % m = c % m := by
  by_cases hm : m = 0
  · subst m
    simpa only [Nat.mod_zero, Nat.add_left_cancel_iff] using h
  · have hmpos : 0 < m := by omega
    have hb := Nat.mod_lt b hmpos
    have hc := Nat.mod_lt c hmpos
    have h1 := Nat.mod_add_mod_eq (a := a) (b := b) (c := m)
    have h2 := Nat.mod_add_mod_eq (a := a) (b := c) (c := m)
    split at h1 <;> split at h2 <;> omega

/-- Subtraction preserves residue equality when both subtractions are exact. -/
theorem sub_mod_congr (N r i j : Nat) (hi : i ≤ N) (hj : j ≤ N)
    (hij : i % r = j % r) : (N - i) % r = (N - j) % r := by
  have hsum : (i + (N - i)) % r = (j + (N - j)) % r := by
    rw [Nat.add_sub_of_le hi, Nat.add_sub_of_le hj]
  rw [Nat.add_mod i (N - i) r, Nat.add_mod j (N - j) r, hij] at hsum
  have hc := weight_add_mod_left_cancel _ _ _ _ hsum
  simpa only [Nat.mod_mod] using hc

/-- Mirror weights agree at indices congruent modulo the decimal period. -/
theorem mirrored_weight_mod_period (q r L i j : Nat)
    (hi : i < L) (hj : j < L)
    (hperiod : 10 ^ r % q = 1 % q)
    (hij : i % r = j % r) :
    (10 ^ i + 10 ^ (L - 1 - i)) % q =
      (10 ^ j + 10 ^ (L - 1 - j)) % q := by
  have hmirror : (L - 1 - i) % r = (L - 1 - j) % r :=
    sub_mod_congr (L - 1) r i j (by omega) (by omega) hij
  rw [Nat.add_mod (10 ^ i) (10 ^ (L - 1 - i)) q,
    Nat.add_mod (10 ^ j) (10 ^ (L - 1 - j)) q,
    ten_pow_mod_period q r i j hperiod hij,
    ten_pow_mod_period q r (L - 1 - i) (L - 1 - j) hperiod hmirror]

theorem mirrored_weight_mod_zero (q r L i : Nat)
    (hi : i < L) (hperiod : 10 ^ r % q = 1 % q)
    (hres : i % r = 0) :
    (10 ^ i + 10 ^ (L - 1 - i)) % q = pairWeight0 L % q := by
  have h := mirrored_weight_mod_period q r L i 0 hi (by omega) hperiod
    (by simpa only [Nat.zero_mod] using hres)
  simpa only [Nat.pow_zero, Nat.sub_zero, pairWeight0] using h

theorem mirrored_weight_mod_one (q r L i : Nat)
    (hL : 2 ≤ L) (hi : i < L) (hperiod : 10 ^ r % q = 1 % q)
    (hres : i % r = 1 % r) :
    (10 ^ i + 10 ^ (L - 1 - i)) % q = pairWeight1 L % q := by
  have h := mirrored_weight_mod_period q r L i 1 hi (by omega) hperiod hres
  have he : L - 1 - 1 = L - 2 := by omega
  simpa only [Nat.pow_one, he, pairWeight1] using h

end ExactLengthResidues

#print axioms ExactLengthResidues.pairWeight0
#print axioms ExactLengthResidues.pairWeight1
#print axioms ExactLengthResidues.ten_pow_mod99
#print axioms ExactLengthResidues.pair_weights_identity
#print axioms ExactLengthResidues.pairWeight0_mod99
#print axioms ExactLengthResidues.pairWeight1_mod99
#print axioms ExactLengthResidues.pair_weights_gcd
#print axioms ExactLengthResidues.pair_weights_gcd_modulus
#print axioms ExactLengthResidues.pow_mod_reduce_period
#print axioms ExactLengthResidues.pow_mod_period
#print axioms ExactLengthResidues.ten_pow_mod_period
#print axioms ExactLengthResidues.sub_mod_congr
#print axioms ExactLengthResidues.mirrored_weight_mod_period
#print axioms ExactLengthResidues.mirrored_weight_mod_zero
#print axioms ExactLengthResidues.mirrored_weight_mod_one
