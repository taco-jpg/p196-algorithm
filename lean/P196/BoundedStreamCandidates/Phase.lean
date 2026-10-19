import P196.BoundedStreamCandidates.Definitions

/-!
# Executable phase recovery from a bounded low prefix

One digit beyond the coefficient boundary belongs to the constant phase
tail. The published ten-phase formula therefore identifies the last term
of an original prefix of length N+2 whenever the word has length at most N.
The executable parity map recovers the phase from that term, including
empty words and both boundary phases.
-/

namespace Agent5.BoundedStreamCandidates

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.CompleteExteriorFibers

/-- The last term of a sufficiently long original low prefix recovers the
phase among all ten even phases. Only width and coefficient bounds are needed. -/
theorem phaseFromLow_correct (N c : Nat) (B : List Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hB : ∀ x ∈ B, x ≤ 18) (hw : B.length ≤ N) :
    phaseFromLow (originalLow (N + 2) { c := c, B := B }) = c := by
  let q := N + 1 - B.length
  have hq : q ≠ 0 := by dsimp only [q]; omega
  have hlen : B.length + 1 + q = N + 2 := by dsimp only [q]; omega
  have hformula := low_prefix_even_phase c B q hc hB
  rw [hlen] at hformula
  have hlast : (originalLow (N + 2) { c := c, B := B }).getLast? =
      some (c - 9 * (if 10 ≤ c then 1 else 0)) := by
    change (adicNumeratorDigits (N + 2) (zValue c B - (c : Int))).getLast? = _
    rw [hformula]
    simp [List.getLast?_append, List.getLast?_cons, List.getLast?_replicate, hq]
  rw [phaseFromLow, hlast]
  simp only [Option.getD_some]
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

#print axioms phaseFromLow_correct

end Agent5.BoundedStreamCandidates
