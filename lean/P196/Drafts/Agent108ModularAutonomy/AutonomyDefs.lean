import P196.Foundations.LychrelDigitSums

/-!
Agent #108: exact-width residue determinism for ordinary decimal reversal.
The finite width threshold is uniform in the numbers and their digit words.
This module defines targets; it does not assume the classification theorem.
-/
namespace ModularAutonomy

open Lychrel196 DecimalDigits

/-- Beyond a single width threshold, equal residues and equal exact decimal
width force equal residues of the ordinary reversals. -/
def EventualReverseResidueDet (M : Nat) : Prop :=
  ∃ B, ∀ L, B ≤ L → ∀ n m (d e : Nat → Nat),
    Canonical n d L → Canonical m e L →
    n % M = m % M → reverse10 n % M = reverse10 m % M

/-- The corresponding property for the actual reverse-and-add map. -/
def EventualStepResidueDet (M : Nat) : Prop :=
  ∃ B, ∀ L, B ≤ L → ∀ n m (d e : Nat → Nat),
    Canonical n d L → Canonical m e L →
    n % M = m % M → step n % M = step m % M

end ModularAutonomy
