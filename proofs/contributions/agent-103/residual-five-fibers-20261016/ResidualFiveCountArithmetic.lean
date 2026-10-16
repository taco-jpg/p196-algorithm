import Std

set_option autoImplicit false

/-!
Arithmetic solution of a conditional recurrence on natural numbers.
This module makes no assertion that a particular digit fiber or filtered
list satisfies the recurrence; that identification is a separate obligation.
-/

namespace Agent103.ResidualFiveCountArithmetic

/-- An additive parity invariant, with no natural-number subtraction. -/
theorem scaled_additive (C : Nat → Nat) (h0 : C 0 = 2)
    (hrec : ∀ r, C (r + 1) + C r = 14 * 10 ^ r) (r : Nat) :
    (r % 2 = 0 → 11 * C r = 14 * 10 ^ r + 8) ∧
    (r % 2 = 1 → 11 * C r + 8 = 14 * 10 ^ r) := by
  induction r with
  | zero => simp [h0]
  | succ r ih =>
      have hs := congrArg (fun n : Nat => 11 * n) (hrec r)
      simp only [Nat.mul_add] at hs
      have hp : 14 * 10 ^ (r + 1) = 10 * (14 * 10 ^ r) := by
        simp only [Nat.pow_succ]
        omega
      constructor
      · intro he
        have ho : r % 2 = 1 := by omega
        have hi := ih.2 ho
        rw [hp]
        omega
      · intro ho
        have he : r % 2 = 0 := by omega
        have hi := ih.1 he
        rw [hp]
        omega

/-- The exact scaled solution, conditional only on the initial value and recurrence. -/
theorem scaled_closed_form (C : Nat → Nat) (h0 : C 0 = 2)
    (hrec : ∀ r, C (r + 1) + C r = 14 * 10 ^ r) (r : Nat) :
    11 * C r =
      if r % 2 = 0 then 14 * 10 ^ r + 8 else 14 * 10 ^ r - 8 := by
  have ha := scaled_additive C h0 hrec r
  by_cases he : r % 2 = 0
  · simp only [he, if_true]
    exact ha.1 he
  · simp only [he, if_false]
    have ho : r % 2 = 1 := by omega
    have hadd := ha.2 ho
    have hbound : 8 ≤ 14 * 10 ^ r := by omega
    omega

/-- The ordinary natural-number division formula for the same conditional solution. -/
theorem closed_form (C : Nat → Nat) (h0 : C 0 = 2)
    (hrec : ∀ r, C (r + 1) + C r = 14 * 10 ^ r) (r : Nat) :
    C r = if r % 2 = 0 then (14 * 10 ^ r + 8) / 11
      else (14 * 10 ^ r - 8) / 11 := by
  have hs := scaled_closed_form C h0 hrec r
  by_cases he : r % 2 = 0
  · simp only [he, if_true] at hs ⊢
    omega
  · simp only [he, if_false] at hs ⊢
    omega

#print axioms scaled_additive
#print axioms scaled_closed_form
#print axioms closed_form

end Agent103.ResidualFiveCountArithmetic
