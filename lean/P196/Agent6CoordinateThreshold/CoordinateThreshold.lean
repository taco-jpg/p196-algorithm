import P196.Agent6CoordinateThreshold.ExteriorFactorizationProof

/-!
Agent #6. Exact overflow thresholds for the finite exterior coordinates.

The exterior scan and coordinate definitions are the unchanged Agent7/Agent115
definitions.  The quotient identity uses only c <= 17 and c != 9, with arbitrary
finite natural coefficients.  Coefficient bounds enter only the zero/one
overflow interpretation.  No canonical-head, trimming, even-phase, nonempty-word,
actual-orbit, or cyclic-return hypothesis is silently added.

This module supplies a local arithmetic interface; it asserts no exterior cycle,
infinite safe orbit, or conclusion about 196.
-/

namespace Agent6.ExteriorCoordinates

open P196.Agent7.Finite
open Agent115.ExteriorFactorization

def phaseCarry (c : Nat) : Nat := if 10 ≤ c then 1 else 0

def phaseDigit (c : Nat) : Nat := c - 9 * phaseCarry c

def overflow (c : Nat) (B : List Nat) : Nat :=
  (normalize B.reverse (phaseCarry c)).2

theorem phaseCarry_le_one (c : Nat) : phaseCarry c ≤ 1 := by
  unfold phaseCarry
  split <;> omega

theorem phaseCarry_eq_div_nine (c : Nat) (hc : c ≤ 17) (hc9 : c ≠ 9) :
    phaseCarry c = c / 9 := by
  unfold phaseCarry
  split <;> omega

theorem phaseDigit_identity (c : Nat) :
    9 * phaseCarry c + phaseDigit c = c := by
  unfold phaseDigit phaseCarry
  split <;> omega

theorem phaseDigit_le_eight (c : Nat) (hc : c ≤ 17) (hc9 : c ≠ 9) :
    phaseDigit c ≤ 8 := by
  unfold phaseDigit phaseCarry
  split <;> omega

theorem phaseDigit_pos (c : Nat) (hc0 : 0 < c) :
    0 < phaseDigit c := by
  unfold phaseDigit phaseCarry
  split <;> omega

/-- The scan formula holds for every finite list of natural coefficients. -/
theorem overflow_eq_highValue (c : Nat) (B : List Nat) :
    overflow c B = (highValue B + phaseCarry c) / 10 ^ B.length := by
  unfold overflow
  rw [normalize_eq, List.length_reverse, lowValue_reverse]

/-- Exact floor of rho, expressed with natural-number division. -/
theorem overflow_eq_rho_quotient (c : Nat) (B : List Nat)
    (hc : c ≤ 17) (hc9 : c ≠ 9) :
    overflow c B = rhoNum c B / (9 * 10 ^ B.length) := by
  have hcoord : (9 * highValue B + c) / 9 = highValue B + phaseCarry c := by
    rw [Nat.mul_add_div (by decide : 0 < 9), phaseCarry_eq_div_nine c hc hc9]
  calc
    overflow c B = (highValue B + phaseCarry c) / 10 ^ B.length :=
      overflow_eq_highValue c B
    _ = ((9 * highValue B + c) / 9) / 10 ^ B.length := by rw [hcoord]
    _ = (9 * highValue B + c) / (9 * 10 ^ B.length) :=
      Nat.div_div_eq_div_mul _ _ _
    _ = rhoNum c B / (9 * 10 ^ B.length) := rfl

/-- Bounded pair coefficients make the exact overflow a bit; no phase bound is needed. -/
theorem overflow_le_one (c : Nat) (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18) : overflow c B ≤ 1 := by
  apply normalize_carry_le B.reverse (phaseCarry c)
  · intro x hx
    exact hB x (List.mem_reverse.mp hx)
  · exact phaseCarry_le_one c

/-- The zero-overflow criterion does not require bounded coefficients. -/
theorem overflow_eq_zero_iff (c : Nat) (B : List Nat)
    (hc : c ≤ 17) (hc9 : c ≠ 9) :
    overflow c B = 0 ↔ rhoNum c B < 9 * 10 ^ B.length := by
  rw [overflow_eq_rho_quotient c B hc hc9]
  exact Nat.div_eq_zero_iff_lt
    (Nat.mul_pos (by decide) (Nat.pow_pos (by decide)))

/-- For bounded pair coefficients, rho crossing one is exactly an overflow. -/
theorem overflow_eq_one_iff (c : Nat) (B : List Nat)
    (hc : c ≤ 17) (hc9 : c ≠ 9) (hB : ∀ x ∈ B, x ≤ 18) :
    overflow c B = 1 ↔ 9 * 10 ^ B.length ≤ rhoNum c B := by
  have hbit := overflow_le_one c B hB
  have hzero := overflow_eq_zero_iff c B hc hc9
  constructor
  · intro hone
    by_cases hlt : rhoNum c B < 9 * 10 ^ B.length
    · have hz := hzero.mpr hlt
      omega
    · omega
  · intro hge
    have hnz : overflow c B ≠ 0 := by
      intro hz
      have := hzero.mp hz
      omega
    omega

/-- Bounded coefficients keep rho strictly below two, including the empty exterior. -/
theorem rhoNum_lt_twice_denominator (c : Nat) (B : List Nat)
    (hc : c ≤ 17) (hc9 : c ≠ 9) (hB : ∀ x ∈ B, x ≤ 18) :
    rhoNum c B < 18 * 10 ^ B.length := by
  have hbit := overflow_le_one c B hB
  rw [overflow_eq_rho_quotient c B hc hc9] at hbit
  have hlt : rhoNum c B / (9 * 10 ^ B.length) < 2 := by omega
  have hden : 0 < 9 * 10 ^ B.length :=
    Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
  have h := (Nat.div_lt_iff_lt_mul hden).mp hlt
  omega

/-- Empty exterior states are included, without an artificial positive-head premise. -/
theorem empty_word_coordinates (c : Nat) :
    overflow c [] = phaseCarry c ∧ rhoNum c [] = c := by
  simp [overflow, normalize, rhoNum, highValue]

/-- The phase restrictions are already necessary on the empty word. -/
theorem empty_word_quotient_iff (c : Nat) :
    (overflow c [] = rhoNum c [] / (9 * 10 ^ ([] : List Nat).length)) ↔
      c ≤ 17 ∧ c ≠ 9 := by
  simp only [List.length_nil, Nat.pow_zero, Nat.mul_one]
  rw [(empty_word_coordinates c).1, (empty_word_coordinates c).2]
  unfold phaseCarry
  split <;> omega

/-- Exact characterization of phases for which the quotient identity holds for every word. -/
theorem quotient_identity_forall_iff (c : Nat) :
    (∀ B : List Nat, overflow c B = rhoNum c B / (9 * 10 ^ B.length)) ↔
      c ≤ 17 ∧ c ≠ 9 := by
  constructor
  · intro h
    exact (empty_word_quotient_iff c).mp (h [])
  · rintro ⟨hc, hc9⟩ B
    exact overflow_eq_rho_quotient c B hc hc9

/-- Neutral phase 9 and the upper boundary 18 cannot be silently admitted. -/
theorem excluded_phase_controls :
    overflow 9 [] = 0 ∧ rhoNum 9 [] / (9 * 10 ^ ([] : List Nat).length) = 1 ∧
    overflow 18 [] = 1 ∧ rhoNum 18 [] / (9 * 10 ^ ([] : List Nat).length) = 2 := by
  decide

/-- The coefficient bound is essential to interpreting every positive carry as one. -/
theorem unbounded_coefficient_control :
    overflow 0 [20] = 2 ∧ 9 * 10 ^ ([20] : List Nat).length ≤ rhoNum 0 [20] := by
  decide

end Agent6.ExteriorCoordinates
