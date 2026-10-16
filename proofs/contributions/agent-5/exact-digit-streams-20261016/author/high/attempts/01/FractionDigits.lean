import DigitDefinitions

/-!
Agent #5: exact ordinary decimal long division for the high exterior stream.
The proof uses the actual outgoing normalization carry and integer arithmetic.
-/

namespace Agent5.ExactDigitStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization

/-- Multiplying numerator and denominator by the same positive integer preserves
all digits produced by long division. -/
theorem fractionDigits_scale (n r D s : Nat) (hs : 0 < s) :
    fractionDigits n (s * r) (s * D) = fractionDigits n r D := by
  induction n generalizing r with
  | zero => rfl
  | succ n ih =>
    simp only [fractionDigits, Nat.mul_left_comm 10 s r,
      Nat.mul_div_mul_left _ _ hs, Nat.mul_mod_mul_left, ih]

/-- The proper fraction `t/9` repeats its single decimal digit. -/
theorem fractionDigits_repeat (q t : Nat) (ht : t < 9) :
    fractionDigits q t 9 = List.replicate q t := by
  induction q with
  | zero => rfl
  | succ q ih =>
    have hd : 10 * t / 9 = t := by omega
    have hm : 10 * t % 9 = t := by omega
    simp [fractionDigits, hd, hm, ih]

theorem highValue_cons_digit (x : Nat) (xs : List Nat) :
    highValue (x :: xs) = x * 10 ^ xs.length + highValue xs := by
  change xs.foldl (fun acc b => 10 * acc + b) (10 * 0 + x) = _
  rw [foldl_high]
  simp

/-- A word of ordinary decimal digits has value below its place-value modulus. -/
theorem highValue_lt_pow (W : List Nat) (hW : ∀ x ∈ W, x < 10) :
    highValue W < 10 ^ W.length := by
  induction W with
  | nil => simp [highValue]
  | cons x xs ih =>
    have hx := hW x List.mem_cons_self
    have hxs : ∀ y ∈ xs, y < 10 := by
      intro y hy
      exact hW y (List.mem_cons_of_mem x hy)
    rw [highValue_cons_digit, List.length_cons]
    calc
      x * 10 ^ xs.length + highValue xs <
          x * 10 ^ xs.length + 10 ^ xs.length := Nat.add_lt_add_left (ih hxs) _
      _ = (x + 1) * 10 ^ xs.length := by rw [Nat.add_mul, Nat.one_mul]
      _ ≤ 10 * 10 ^ xs.length := Nat.mul_le_mul_right _ (by omega)
      _ = 10 ^ (xs.length + 1) := by rw [Nat.pow_succ, Nat.mul_comm]

/-- Exact finite decimal expansion with an eventually repeating tail. -/
theorem fractionDigits_of_highValue (W : List Nat) (t q : Nat)
    (hW : ∀ x ∈ W, x < 10) (ht : t < 9) :
    fractionDigits (W.length + q) (9 * highValue W + t) (9 * 10 ^ W.length) =
      W ++ List.replicate q t := by
  induction W with
  | nil => simpa [highValue] using fractionDigits_repeat q t ht
  | cons x xs ih =>
    have hxs : ∀ y ∈ xs, y < 10 := by
      intro y hy
      exact hW y (List.mem_cons_of_mem x hy)
    have hv := highValue_lt_pow xs hxs
    have hp : 0 < 9 * 10 ^ xs.length := Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
    have hr : 9 * highValue xs + t < 9 * 10 ^ xs.length := by omega
    have hnum : 9 * highValue (x :: xs) + t =
        (9 * highValue xs + t) + (9 * 10 ^ xs.length) * x := by
      rw [highValue_cons_digit, Nat.mul_add]
      ac_rfl
    have hden : 9 * 10 ^ (xs.length + 1) = 10 * (9 * 10 ^ xs.length) := by
      rw [Nat.pow_succ]
      ac_rfl
    have hd : ((9 * highValue xs + t) + (9 * 10 ^ xs.length) * x) /
        (9 * 10 ^ xs.length) = x := by
      rw [Nat.add_mul_div_left _ _ hp, Nat.div_eq_of_lt hr, Nat.zero_add]
    have hm : ((9 * highValue xs + t) + (9 * 10 ^ xs.length) * x) %
        (9 * 10 ^ xs.length) = 9 * highValue xs + t := by
      rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hr]
    simp only [List.length_cons, Nat.succ_add, fractionDigits, hnum, hden,
      Nat.mul_div_mul_left _ _ (by decide : 0 < 10), Nat.mul_mod_mul_left, hd, hm]
    rw [fractionDigits_scale _ _ _ 10 (by decide), ih hxs]
    rfl

end Agent5.ExactDigitStreams
