import P196.Agent10EightCarry.ActualCarryObservability

/-!
Reconstruction predicates with one fixed initial width. The width is a
parameter of the input class, rather than an upper bound on several widths.
Every observation includes the terminal carry at the current width. Only
initially active coefficients are requested, and subsequent widths are free.
The threshold function below is classified only on the stated domain 1..8.
-/

namespace ExactSmallWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Active-pair reconstruction from complete carry words at initial width `L`. -/
def PairReconstructionAtWidth (L K : Nat) : Prop :=
  ∀ (q r : Nat → Nat), Admissible L q → Admissible L r →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < L → q i = r i

/-- Next-integer reconstruction from canonical inputs of the same exact width. -/
def NextIntegerReconstructionAtWidth (L K : Nat) : Prop :=
  ∀ (n m : Nat) (d e : Nat → Nat),
    Canonical n d L → Canonical m e L →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) →
    Lychrel196.step n = Lychrel196.step m

/-- The exact thresholds on widths one through eight; no other width is
classified by the value assigned by this definition. -/
def exactWidthThreshold (L : Nat) : Nat :=
  if L = 1 then 4 else if L = 2 then 5
  else if L = 4 ∨ L = 6 then 6 else 7

/-- The existing word-value bridge turns fixed-width pair reconstruction
into next-integer reconstruction without recovering the initial digit split. -/
theorem next_integer_reconstruction_of_pair_reconstruction (L K : Nat)
    (h : PairReconstructionAtWidth L K) : NextIntegerReconstructionAtWidth L K := by
  intro n m d e hn hm hc
  have he := h (columnSum d L) (columnSum e L)
    (NormalizationBridge.canonical_admissible n d L hn)
    (NormalizationBridge.canonical_admissible m e L hm) hc
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

#print axioms next_integer_reconstruction_of_pair_reconstruction

end ExactSmallWidthCarryThresholds
