import resume_growth_eleven

namespace Agent121.CarryWindow
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- An unproved research target, not an assertion of its truth. -/
def ReconstructionWindow (k : Nat) : Prop :=
  ∀ (q r : Nat → Nat) (L : Nat), Admissible L q → Admissible L r →
    (∀ t, t < k → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < L → q i = r i

end Agent121.CarryWindow
