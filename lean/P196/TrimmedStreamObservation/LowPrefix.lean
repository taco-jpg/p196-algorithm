import P196.Agent5ExactDigitStreams.AdicDigits

/-!
# The low observation at the original word width

The first `B.length` digits of the original low stream are exactly the
normalized coefficient word. This identity is valid for every phase and
every natural coefficient word.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Observing the low stream at the original width recovers the normalized
word, without a phase restriction or a coefficient bound. -/
theorem low_prefix_normalized (c : Nat) (B : List Nat) :
    adicNumeratorDigits B.length (zValue c B - (c : Int)) =
      (normalize B 0).1 := by
  have ha : zValue c B - (c : Int) =
      9 * ((lowValue B + 0 : Nat) : Int) - (c : Int) * 10 ^ B.length := by
    simp only [zValue, Nat.add_zero, Int.mul_sub, Int.mul_one]
    omega
  rw [ha]
  simpa only [Nat.add_zero, adicNumeratorDigits, List.append_nil] using
    adicNumeratorDigits_normalize B 0 0 (c : Int)

#print axioms low_prefix_normalized

end Agent5.TrimmedStreamObservation
