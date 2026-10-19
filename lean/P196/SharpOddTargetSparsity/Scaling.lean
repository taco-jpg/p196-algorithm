import P196.SharpOddTargetSparsity.Tables
import P196.OddPredecessorTargetSparsity.Integration

/-!
# Decimal interval selection and scaling of the finite bounds

Agent #6: use the width of the largest integer below the exclusive
cutoff. Its leading two digits select one of the finite coefficient
estimates, including when the cutoff is an exact power of ten.
-/

set_option autoImplicit false

namespace SharpOddTargetSparsity

open DecimalDigits DecimalQuantitativeMass Agent101

/-- Every cutoff whose last included integer has at least two digits
lies in a two-digit decimal interval with index from ten to ninety-nine. -/
theorem cutoff_interval (N W : Nat) (hN : 2 ≤ N) (hW : 2 ≤ W)
    (hd : decimalLength (N - 1) = W) :
    ∃ a : Nat, 10 ≤ a ∧ a ≤ 99 ∧
      a * 10 ^ (W - 2) ≤ N ∧ N ≤ (a + 1) * 10 ^ (W - 2) := by
  obtain ⟨d, L, hc⟩ := canonical_exists (N - 1) (by omega)
  have hL := decimalLength_of_canonical (N - 1) d L hc
  have hLW : L = W := by omega
  rw [hLW] at hc
  have hw := canonical_decimalWidth (N - 1) d W hc
  let P := 10 ^ (W - 2)
  let a := (N - 1) / P
  have hp : 0 < P := Nat.pow_pos (by decide)
  have hlo : 10 * P ≤ N - 1 := by
    have h := hw.2.1
    rw [show W - 1 = (W - 2) + 1 by omega, Nat.pow_succ] at h
    simpa only [P, Nat.mul_comm] using h
  have hhi : N - 1 < 100 * P := by
    have h := hw.2.2
    rw [show W = (W - 2) + 2 by omega, Nat.pow_add] at h
    simpa only [P, show (10 : Nat) ^ 2 = 100 by decide, Nat.mul_comm] using h
  have ha : 10 ≤ a := (Nat.le_div_iff_mul_le hp).mpr hlo
  have ha' : a < 100 := (Nat.div_lt_iff_lt_mul hp).mpr hhi
  have hdiv := Nat.div_add_mod (N - 1) P
  have hmod := Nat.mod_lt (N - 1) hp
  have hlow := Nat.mul_div_le (N - 1) P
  have hprod : P * ((N - 1) / P) = a * P := by
    simp only [a, Nat.mul_comm]
  rw [hprod] at hdiv hlow
  refine ⟨a, ha, by omega, ?_, ?_⟩
  · change a * P ≤ N
    omega
  · change N ≤ (a + 1) * P
    rw [Nat.add_mul, Nat.one_mul]
    omega

/-- Scale a finite leading-block inequality to any decimal width, then
compare its interval's lower endpoint with the actual cutoff. -/
theorem scale_envelope_bound (A c k m a N : Nat)
    (hcount : 9 * A + 29 ≤ c * 10 ^ k)
    (hcoefficient : c ^ 2 ≤ 729 * a * 10 ^ m)
    (hcutoff : a * 10 ^ (2 * k + m) ≤ N) :
    A ^ 2 ≤ 9 * N := by
  have hlinear : 9 * A ≤ c * 10 ^ k := by omega
  have hsquare := Nat.pow_le_pow_left hlinear 2
  simp only [Nat.mul_pow, show (9 : Nat) ^ 2 = 81 by decide] at hsquare
  have hscaled := Nat.mul_le_mul_right ((10 ^ k) ^ 2) hcoefficient
  have htotal : 81 * A ^ 2 ≤ 81 * (9 * N) := by
    calc
      81 * A ^ 2 ≤ c ^ 2 * (10 ^ k) ^ 2 := hsquare
      _ ≤ (729 * a * 10 ^ m) * (10 ^ k) ^ 2 := hscaled
      _ = 81 * (9 * (a * 10 ^ (2 * k + m))) := by
        rw [show (729 : Nat) = 81 * 9 by decide,
          Nat.pow_add 10 (2 * k) m, Nat.pow_mul' 10 2 k]
        simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      _ ≤ 81 * (9 * N) := Nat.mul_le_mul_left 81 (Nat.mul_le_mul_left 9 hcutoff)
  exact Nat.le_of_mul_le_mul_left htotal (by decide)

end SharpOddTargetSparsity

#print axioms SharpOddTargetSparsity.cutoff_interval
#print axioms SharpOddTargetSparsity.scale_envelope_bound
