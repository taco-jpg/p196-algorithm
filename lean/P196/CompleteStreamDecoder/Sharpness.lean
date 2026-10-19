import P196.BoundedStreamCandidates.Definitions

/-!
# A complete competitor can be one coefficient wider

Explicit valid pairs in each boundary phase share their original low
numerator and their original high numerator and denominator. Their actual
carries differ, so equality of the complete streams does not force equal
word widths. These pairs witness the necessity of the width allowance.

The longer phase-eighteen word also occurs in the earlier phase-eight
finite control in TrimmedStreamObservation.Controls. The new control here
is its complete cross-width pairing at phase eighteen.
-/

namespace Agent5.CompleteStreamDecoder

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.BoundedStreamCandidates Agent5.CompleteExteriorFibers

/-- The one-place allowance for a complete competitor is necessary at
both boundary phases, with actual carries one and zero respectively. -/
theorem boundary_width_slack_sharp (c : Nat) (hc : c = 0 ∨ c = 18) :
    ∃ s q : Outer,
      s.c = c ∧ q.c = c ∧ validOuter s = true ∧ validOuter q = true ∧
      q.B.length = s.B.length + 1 ∧ actualCarry s = 1 ∧ actualCarry q = 0 ∧
      sameStreams s q := by
  rcases hc with rfl | rfl
  · refine ⟨{ c := 0, B := [11] }, { c := 0, B := [1, 1] },
      rfl, rfl, by decide, by decide, rfl, rfl, rfl, ?_⟩
    intro cut
    exact ⟨rfl, rfl⟩
  · refine ⟨{ c := 18, B := [11, 9, 7] }, { c := 18, B := [1, 0, 18, 17] },
      rfl, rfl, by decide, by decide, rfl, rfl, rfl, ?_⟩
    intro cut
    exact ⟨rfl, rfl⟩

#print axioms boundary_width_slack_sharp

end Agent5.CompleteStreamDecoder
