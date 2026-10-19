import P196.FiniteExteriorHistories.Obstruction

/-!
# Numeric values of the literal boundary observations

The high long-division function is total. At boundary phases its first
coefficient can exceed nine, so its numeric prefix identity must allow
improper fractions. A positive prefix length is essential in that identity.

The low-prefix identity uses the existing arbitrary-phase normalization
theorem. The high-prefix splitting identity cancels the original spatial
and carry-dependent powers, leaving the exact quotient of the remaining
tail. That quotient is not the normalization carry.
-/

namespace Agent5.PhaseEighteenIsolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- A positive prefix of literal long division has the scaled quotient
as its positional value, even when the initial fraction is improper. -/
theorem fractionDigits_value (k r D : Nat) (hD : 0 < D) :
    highValue (fractionDigits (k + 1) r D) = 10 ^ (k + 1) * r / D := by
  induction k generalizing r with
  | zero => simp [fractionDigits, highValue]
  | succ k ih =>
      rw [fractionDigits, highValue_cons, fractionDigits_length, ih]
      have hscale : 10 ^ (k + 1 + 1) * r =
          10 ^ (k + 1) * ((10 * r) % D) +
            (10 ^ (k + 1) * ((10 * r) / D)) * D := by
        calc
          10 ^ (k + 1 + 1) * r = 10 ^ (k + 1) * (10 * r) := by
            rw [Nat.pow_succ, Nat.mul_assoc]
          _ = 10 ^ (k + 1) * ((10 * r) % D + D * ((10 * r) / D)) := by
            rw [Nat.mod_add_div]
          _ = _ := by rw [Nat.mul_add]; ac_rfl
      rw [hscale, Nat.add_mul_div_right _ _ hD]
      ac_rfl

/-- The low observation through a specified initial coefficient block
reads its positional value modulo the corresponding power of ten.
The phase and all coefficients are arbitrary natural numbers. -/
theorem low_prefix_append_value (c : Nat) (X S : List Nat) :
    lowValue (adicNumeratorDigits X.length
      (zValue c (X ++ S) - (c : Int))) = lowValue X % 10 ^ X.length := by
  have hz : zValue c (X ++ S) - (c : Int) =
      9 * (lowValue X : Int) -
        ((c : Int) * 10 ^ S.length - 9 * (lowValue S : Int)) *
          10 ^ X.length := by
    have hpow : (10 : Int) ^ (X.length + S.length) =
        10 ^ X.length * 10 ^ S.length := by
      simpa only [Int.natCast_mul, Int.natCast_pow] using
        congrArg (fun n : Nat => (n : Int)) (Nat.pow_add 10 X.length S.length)
    simp only [zValue, lowValue_append, List.length_append,
      Int.natCast_add, Int.natCast_mul, Int.natCast_pow,
      show ((10 : Nat) : Int) = 10 from rfl,
      hpow, Int.mul_sub, Int.sub_mul, Int.mul_add, Int.mul_one]
    have h1 : (c : Int) * (10 ^ X.length * 10 ^ S.length) =
        ((c : Int) * 10 ^ S.length) * 10 ^ X.length := by ac_rfl
    have h2 : (9 : Int) * (10 ^ X.length * (lowValue S : Int)) =
        (9 * (lowValue S : Int)) * 10 ^ X.length := by ac_rfl
    omega
  have hscan := adicNumeratorDigits_normalize X 0 0
    ((c : Int) * 10 ^ S.length - 9 * (lowValue S : Int))
  simp only [Nat.add_zero, adicNumeratorDigits, List.append_nil] at hscan
  rw [hz, hscan, normalize_eq]
  simp only [Nat.add_zero, lowValue_digitsOf]

/-- At the block length plus the supplied carry shift, the high prefix
reads the block's high value plus the exact quotient of the remaining
tail. This identity imposes no digit or coefficient bounds. -/
theorem high_prefix_append_value (d gamma : Nat) (X S : List Nat)
    (hpositive : 0 < X.length + gamma) :
    highValue (fractionDigits (X.length + gamma) (rhoNum d (X ++ S))
      (9 * 10 ^ (X ++ S).length * 10 ^ gamma)) =
      highValue X + rhoNum d S / (9 * 10 ^ S.length) := by
  have hden : 9 * 10 ^ (X ++ S).length * 10 ^ gamma =
      10 ^ (X.length + gamma) * (9 * 10 ^ S.length) := by
    rw [List.length_append, Nat.pow_add, Nat.pow_add]
    ac_rfl
  have hhigh : highValue (X ++ S) =
      highValue X * 10 ^ S.length + highValue S := by
    unfold highValue
    rw [List.foldl_append, foldl_high]
    rfl
  have hrho : rhoNum d (X ++ S) =
      rhoNum d S + highValue X * (9 * 10 ^ S.length) := by
    simp only [rhoNum, hhigh, Nat.mul_add]
    ac_rfl
  obtain ⟨k, hk⟩ : ∃ k, X.length + gamma = k + 1 :=
    ⟨X.length + gamma - 1, by omega⟩
  have hD : 0 < 9 * 10 ^ (X ++ S).length * 10 ^ gamma :=
    Nat.mul_pos (Nat.mul_pos (by decide) (Nat.pow_pos (by decide)))
      (Nat.pow_pos (by decide))
  rw [hk, fractionDigits_value k _ _ hD, ← hk, hden,
    Nat.mul_div_mul_left _ _ (Nat.pow_pos (by decide)), hrho,
    Nat.add_mul_div_right _ _
      (Nat.mul_pos (by decide) (Nat.pow_pos (by decide)))]
  exact Nat.add_comm _ _

#print axioms fractionDigits_value
#print axioms low_prefix_append_value
#print axioms high_prefix_append_value

end Agent5.PhaseEighteenIsolation
