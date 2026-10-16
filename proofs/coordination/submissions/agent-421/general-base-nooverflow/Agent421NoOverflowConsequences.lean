import Agent421NoOverflowRealization

namespace Agent421NoOverflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase

/-- This packages the explicit conclusion, not an extra premise. -/
def TwoStepWitness (b : Int) (q : Nat → Int) (L : Nat) (d : List Int) : Prop :=
  d.length = L ∧ DigitBounds b d ∧ PositiveLast d ∧
  0 < eval b d ∧
  (∀ i, i ≤ L → terminal b 0 (tags ((pairs d).take i)) = carry b q i) ∧
  DigitBounds b (stepDigits b d) ∧ PositiveLast (stepDigits b d) ∧
  DigitBounds b (stepDigits b (stepDigits b d)) ∧
  PositiveLast (stepDigits b (stepDigits b d)) ∧
  eval b (stepDigits b d) = eval b d + reversedValue b d ∧
  eval b (stepDigits b (stepDigits b d)) =
    eval b (stepDigits b d) + reversedValue b (stepDigits b d) ∧
  (stepDigits b (stepDigits b d)).reverse = stepDigits b (stepDigits b d)

theorem even_base_nooverflow (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 8 ≤ b) (heven : b%2 = 0) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hover : carry b q L = 0) :
    ∃ d, TwoStepWitness b q L d := by
  exact same_carries_two_step_palindrome b 1 q L (by omega) (by omega)
    (by omega) hL hq hsym hover

theorem odd_base_nooverflow (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 7 ≤ b) (hodd : b%2 = 1) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hover : carry b q L = 0) :
    ∃ d, TwoStepWitness b q L d := by
  exact same_carries_two_step_palindrome b 2 q L hb (by omega)
    (by omega) hL hq hsym hover

/-- The no-overflow branch needs only b >= 7, stronger than the full source
normalization theorem's even >=10 / odd >=17 thresholds. No overflow claim. -/
theorem every_base_ge_seven_nooverflow (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 7 ≤ b) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hover : carry b q L = 0) :
    ∃ d, TwoStepWitness b q L d := by
  have hpar : b%2 = 0 ∨ b%2 = 1 := by omega
  rcases hpar with he | ho
  · exact even_base_nooverflow b q L (by omega) he hL hq hsym hover
  · exact odd_base_nooverflow b q L hb ho hL hq hsym hover

/-- Exact specialization to the base ranges stated in the source report. -/
theorem source_bases_nooverflow (b : Int) (q : Nat → Int) (L : Nat)
    (hb : (10 ≤ b ∧ b%2 = 0) ∨ (17 ≤ b ∧ b%2 = 1)) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hover : carry b q L = 0) :
    ∃ d, TwoStepWitness b q L d :=
  every_base_ge_seven_nooverflow b q L (by omega) hL hq hsym hover

/-- A sound class cannot include every canonical representative of a complete
no-overflow carry word while asserting nonpalindromicity at positive time two. -/
theorem no_carry_only_second_step_safety (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 7 ≤ b) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hover : carry b q L = 0) :
    ¬ (∀ d : List Int, d.length = L → DigitBounds b d → PositiveLast d →
      (∀ i, i ≤ L → terminal b 0 (tags ((pairs d).take i)) = carry b q i) →
      (stepDigits b (stepDigits b d)).reverse ≠ stepDigits b (stepDigits b d)) := by
  intro hall
  obtain ⟨d, hd⟩ := every_base_ge_seven_nooverflow b q L hb hL hq hsym hover
  rcases hd with ⟨hlen, hbound, hpos, _, hcarry, _, _, _, _, _, _, hpal⟩
  exact hall d hlen hbound hpos hcarry hpal

/-- Base six shows the local low-output estimate cannot simply use b>=6.
This does NOT refute a different normalization scheme or the existence of a
terminating representative in base six. -/
theorem base_six_local_bound_counterexample :
    (norm 6 1 ((0+1)/6) ((0+1)/6)+1)%6 +
    (norm 6 1 ((0+1)/6) ((0+1)/6)+1)%6 = 6 ∧
    ¬ ((norm 6 1 ((0+1)/6) ((0+1)/6)+1)%6 +
      (norm 6 1 ((0+1)/6) ((0+1)/6)+1)%6 ≤ 6-1) := by
  decide

#print axioms even_base_nooverflow
#print axioms odd_base_nooverflow
#print axioms every_base_ge_seven_nooverflow
#print axioms source_bases_nooverflow
#print axioms no_carry_only_second_step_safety
#print axioms base_six_local_bound_counterexample
end Agent421NoOverflow
