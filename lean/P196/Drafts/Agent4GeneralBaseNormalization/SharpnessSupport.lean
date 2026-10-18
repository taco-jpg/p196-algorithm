import P196.Drafts.Agent4GeneralBaseNormalization.NoOverflowEndpoint

/-!
Agent #4: kernel-checked schoolbook certificate soundness and numeric digit
mismatch criteria. Concrete universal-base certificate instances are separate.
-/
namespace P196.Agent4.GeneralBase

theorem quotient_remainder_of_column (b x digit carry : Nat)
    (hb : 0 < b) (hd : digit < b) (heq : x = digit + b * carry) :
    x / b = carry ∧ x % b = digit := by
  have hdiv : x / b = carry := by
    apply (Nat.div_eq_iff hb).2
    rw [Nat.mul_comm carry b]
    constructor <;> omega
  have hmod := Nat.mod_add_div x b
  rw [hdiv] at hmod
  exact ⟨hdiv, by omega⟩

theorem certified_carry_word (b n : Nat) (q e c : Nat → Nat)
    (hb : 0 < b) (he : ∀ i < n, e i < b) (hzero : c 0 = 0)
    (hrows : ∀ i < n, q i + c i = e i + b * c (i + 1))
    (k : Nat) (hk : k ≤ n) : arithmeticCarry b q k = c k := by
  induction k with
  | zero => exact hzero.symm
  | succ k ih =>
      simp only [arithmeticCarry]
      rw [ih (by omega)]
      exact (quotient_remainder_of_column b (q k + c k) (e k) (c (k + 1))
        hb (he k (by omega)) (hrows k (by omega))).1

theorem certified_output_digits (b n : Nat) (q e c : Nat → Nat)
    (hb : 0 < b) (he : ∀ i < n, e i < b) (hzero : c 0 = 0)
    (hrows : ∀ i < n, q i + c i = e i + b * c (i + 1))
    (i : Nat) (hi : i < n) : arithmeticOutput b q i = e i := by
  unfold arithmeticOutput
  rw [certified_carry_word b n q e c hb he hzero hrows i (by omega)]
  exact (quotient_remainder_of_column b (q i + c i) (e i) (c (i + 1))
    hb (he i hi) (hrows i hi)).2

theorem certified_value (b n : Nat) (q e c : Nat → Nat)
    (hb : 0 < b) (he : ∀ i < n, e i < b) (hzero : c 0 = 0)
    (hrows : ∀ i < n, q i + c i = e i + b * c (i + 1)) :
    value b e n + c n * b ^ n = value b q n := by
  have h := value_carry_conservation b q n
  have hval := value_congr b n (arithmeticOutput b q) e
    (certified_output_digits b n q e c hb he hzero hrows)
  rw [hval, certified_carry_word b n q e c hb he hzero hrows n (by omega)] at h
  exact h

theorem certified_numeric_step_same_width (b n : Nat) (d e c : Nat → Nat)
    (hb : 0 < b) (hd : ∀ i < n, d i < b) (he : ∀ i < n, e i < b)
    (hzero : c 0 = 0) (hend : c n = 0)
    (hrows : ∀ i < n, pairCoeff n d i + c i = e i + b * c (i + 1)) :
    value b e n = addAtWidth b n (value b d n) := by
  have h := certified_value b n (pairCoeff n d) e c hb he hzero hrows
  simp only [hend, Nat.zero_mul, Nat.add_zero] at h
  unfold addAtWidth
  rw [reverseAtWidth_value b n d hb hd]
  rw [pair_value] at h
  exact h

theorem certified_numeric_step_extra_digit (b n : Nat) (d e c : Nat → Nat)
    (hb : 0 < b) (hd : ∀ i < n, d i < b) (he : ∀ i < n, e i < b)
    (hzero : c 0 = 0) (hend : e n = c n)
    (hrows : ∀ i < n, pairCoeff n d i + c i = e i + b * c (i + 1)) :
    value b e (n + 1) = addAtWidth b n (value b d n) := by
  have h := certified_value b n (pairCoeff n d) e c hb he hzero hrows
  change value b e n + e n * b ^ n = addAtWidth b n (value b d n)
  rw [hend, h]
  unfold addAtWidth
  rw [pair_value, reverseAtWidth_value b n d hb hd]

theorem numeric_nonpalindrome_of_mismatch (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : ∀ i < n, d i < b) (i : Nat) (hi : i < n)
    (hne : d i ≠ d (n - 1 - i)) :
    reverseAtWidth b n (value b d n) ≠ value b d n := by
  intro h
  rw [reverseAtWidth_value b n d hb hd] at h
  have hdigits : integerDigit b (value b (fun j => d (n - 1 - j)) n) i =
      integerDigit b (value b d n) i :=
    congrArg (fun x : Nat => integerDigit b x i) h
  have hrev : ∀ j < n, d (n - 1 - j) < b := by
    intro j hj
    exact hd (n - 1 - j) (by omega)
  rw [integerDigit_value b n (fun j => d (n - 1 - j)) hb hrev i hi,
    integerDigit_value b n d hb hd i hi] at hdigits
  exact hne hdigits.symm

theorem numeric_palindrome_of_symmetric (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : ∀ i < n, d i < b) (hs : Symmetric n d) :
    reverseAtWidth b n (value b d n) = value b d n := by
  rw [reverseAtWidth_value b n d hb hd]
  apply value_congr
  intro i hi
  exact (hs i hi).symm

theorem arithmetic_column_bounds (b : Nat) (q : Nat → Nat) (i : Nat)
    (hb : 0 < b) :
    arithmeticCarry b q (i + 1) * b ≤ q i + arithmeticCarry b q i ∧
      q i + arithmeticCarry b q i ≤ arithmeticCarry b q (i + 1) * b + b - 1 := by
  exact (Nat.div_eq_iff hb).1 (show (q i + arithmeticCarry b q i) / b =
    arithmeticCarry b q (i + 1) from rfl)

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.quotient_remainder_of_column
#print axioms P196.Agent4.GeneralBase.certified_carry_word
#print axioms P196.Agent4.GeneralBase.certified_output_digits
#print axioms P196.Agent4.GeneralBase.certified_value
#print axioms P196.Agent4.GeneralBase.certified_numeric_step_same_width
#print axioms P196.Agent4.GeneralBase.certified_numeric_step_extra_digit
#print axioms P196.Agent4.GeneralBase.numeric_nonpalindrome_of_mismatch
#print axioms P196.Agent4.GeneralBase.numeric_palindrome_of_symmetric
#print axioms P196.Agent4.GeneralBase.arithmetic_column_bounds
