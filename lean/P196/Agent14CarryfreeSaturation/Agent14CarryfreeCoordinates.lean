import P196.Agent14CarryfreeSaturation.Agent14CarryfreeDigits

/-!
# Literal coefficient evaluations of the carry-free witnesses

This file connects the actual reflected digit columns to Q(1) and Q(-1)
in Theorem 3 of proofs/research/astra_spectral_carry_quotient.md, source
blob eac5b8f61385a615d9cc3e7796a4d698c66b716b at source-map commit
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5. All alternating arithmetic is
over Int. No quotient-ring presentation or orbit assertion is introduced.
-/

namespace Agent14.Carryfree

open DecimalDigits DecimalMass

/-- Literal finite evaluation of the natural coefficient word in Int. -/
def coefficientEval (q : Nat → Nat) : Nat → Int → Int
  | 0, _ => 0
  | L + 1, x => coefficientEval q L x + (q L : Int) * x ^ L

/-- Evaluation at one is the original finite coefficient sum. -/
theorem eval_one (q : Nat → Nat) (L : Nat) :
    coefficientEval q L 1 = (wordSum q L : Int) := by
  induction L with
  | zero => rfl
  | succ L ih =>
      have hp : (1 : Int) ^ L = 1 := by
        simpa only [Nat.one_pow] using (Int.natCast_pow 1 L).symm
      simp only [coefficientEval, wordSum, ih, hp, Int.mul_one, Int.ofNat_add]

/-- Evaluation depends only on coefficients inside the specified width. -/
theorem coefficientEval_congr (q r : Nat → Nat) (L : Nat) (x : Int)
    (h : ∀ i, i < L → q i = r i) :
    coefficientEval q L x = coefficientEval r L x := by
  induction L with
  | zero => rfl
  | succ L ih =>
      simp only [coefficientEval, ih (fun i hi => h i (by omega)), h L (by omega)]

/-- Coefficient addition is literal addition of the evaluated sums. -/
theorem coefficientEval_add (q r : Nat → Nat) (L : Nat) (x : Int) :
    coefficientEval (fun i => q i + r i) L x =
      coefficientEval q L x + coefficientEval r L x := by
  induction L with
  | zero => rfl
  | succ L ih =>
      simp only [coefficientEval, ih, Int.ofNat_add, Int.add_mul]
      omega

/-- A coefficient at a single position contributes its exact monomial. -/
theorem coefficientEval_spike (k a L : Nat) (x : Int) :
    coefficientEval (spike k a) L x =
      if k < L then (a : Int) * x ^ k else 0 := by
  induction L with
  | zero => simp [coefficientEval]
  | succ L ih =>
      rw [coefficientEval, ih]
      by_cases hk : k < L
      · have hne : L ≠ k := by omega
        simp [spike, hk, hne, show k < L + 1 by omega]
      · by_cases he : k = L
        · subst k
          simp [spike]
        · have hne : L ≠ k := by omega
          have hnot : ¬ k < L + 1 := by omega
          simp [spike, hk, hne, hnot]

/-- The sign of a monomial evaluated at minus one is fixed by its parity. -/
theorem neg_one_pow_parity (k : Nat) :
    (-1 : Int) ^ k = if k % 2 = 0 then 1 else -1 := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [Int.pow_succ, ih]
      by_cases h : k % 2 = 0
      · have hs : (k + 1) % 2 ≠ 0 := by omega
        simp [h, hs]
      · have hs : (k + 1) % 2 = 0 := by omega
        simp [h, hs]

/-- The original pair-sum identity supplies Q(1) for every digit word. -/
theorem columns_eval_one (d : Nat → Nat) (L : Nat) :
    coefficientEval (columnSum d L) L 1 = 2 * (wordSum d L : Int) := by
  rw [eval_one, wordSum_columns]
  omega

/-- For an actual canonical input, Q(1) is twice its ordinary digit sum. -/
theorem canonical_columns_eval_one (n : Nat) (d : Nat → Nat) (L : Nat)
    (hd : Canonical n d L) :
    coefficientEval (columnSum d L) L 1 = 2 * (digitSum n : Int) := by
  have hs : digitSum n = wordSum d L := by
    rw [← hd.2.2.2]
    exact digitSum_value d L hd.2.1
  rw [columns_eval_one, hs]

/-- The exact alternating evaluation of the odd-width source polynomial.
The width-five central collision is retained by the coefficient formula. -/
theorem odd_columns_eval_neg_one (a b c L : Nat)
    (hL : 5 ≤ L) (hodd : L % 2 = 1) :
    coefficientEval (columnSum (threeDigits a b c L) L) L (-1) =
      2 * ((a : Int) - (b : Int) + (c : Int)) := by
  have h0 : 0 < L := by omega
  have h1 : 1 < L := by omega
  have h2 : 2 < L := by omega
  have hL1 : L - 1 < L := by omega
  have hL2 : L - 2 < L := by omega
  have hL3 : L - 3 < L := by omega
  have hp1 : (-1 : Int) ^ (L - 1) = 1 := by
    rw [neg_one_pow_parity]
    simp [show (L - 1) % 2 = 0 by omega]
  have hp2 : (-1 : Int) ^ (L - 2) = -1 := by
    rw [neg_one_pow_parity]
    simp [show (L - 2) % 2 ≠ 0 by omega]
  have hp3 : (-1 : Int) ^ (L - 3) = 1 := by
    rw [neg_one_pow_parity]
    simp [show (L - 3) % 2 = 0 by omega]
  have hcoeff :
      coefficientEval (columnSum (threeDigits a b c L) L) L (-1) =
        coefficientEval
          (fun i => spike 0 a i + spike (L - 1) a i + spike 1 b i +
            spike (L - 2) b i + spike 2 c i + spike (L - 3) c i) L (-1) := by
    apply coefficientEval_congr
    intro i hi
    exact threeDigits_column_formula a b c L i hL hi
  rw [hcoeff]
  simp [coefficientEval_add, coefficientEval_spike, h0, h1, h2, hL1, hL2, hL3,
    hp1, hp2, hp3, Int.pow_succ] <;> omega

/-- At even width the source polynomial has zero alternating evaluation.
This concerns the pair-sum polynomial, not the input integer modulo eleven. -/
theorem even_columns_eval_neg_one (a L : Nat)
    (hL : 2 ≤ L) (heven : L % 2 = 0) :
    coefficientEval (columnSum (oneDigit a L) L) L (-1) = 0 := by
  have h0 : 0 < L := by omega
  have hL1 : L - 1 < L := by omega
  have hp : (-1 : Int) ^ (L - 1) = -1 := by
    rw [neg_one_pow_parity]
    simp [show (L - 1) % 2 ≠ 0 by omega]
  have hcoeff :
      coefficientEval (columnSum (oneDigit a L) L) L (-1) =
        coefficientEval (fun i => spike 0 a i + spike (L - 1) a i) L (-1) := by
    apply coefficientEval_congr
    intro i hi
    exact oneDigit_column_formula a L i hL hi
  rw [hcoeff]
  simp [coefficientEval_add, coefficientEval_spike, h0, hL1, hp, Int.pow_succ] <;> omega

#print axioms coefficientEval
#print axioms eval_one
#print axioms coefficientEval_congr
#print axioms coefficientEval_add
#print axioms coefficientEval_spike
#print axioms neg_one_pow_parity
#print axioms columns_eval_one
#print axioms canonical_columns_eval_one
#print axioms odd_columns_eval_neg_one
#print axioms even_columns_eval_neg_one

end Agent14.Carryfree
