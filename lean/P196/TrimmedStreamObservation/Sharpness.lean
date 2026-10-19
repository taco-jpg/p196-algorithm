import P196.StreamObservationInjectivity.Sharpness

/-!
Agent #5: optimality of the high cutoff despite complete low observation.

The existing phase-two witnesses at every width at least two have equal
low coefficient values. Consequently their entire original low streams
agree, while the high streams agree through the width and differ at the
next digit. Both words satisfy `validOuter`, so terminal trimming does not
permit a shorter uniform high observation even with every low digit known.

This module reuses the existing witness family and its normalization,
validity, and high-prefix proofs. It concerns exterior observations and
does not assert that the witnesses occur along the orbit of 196.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.StreamObservationInjectivity

/-- The existing arbitrary-width witnesses have exactly the same low
coefficient value, not merely the same normalized low digits. -/
theorem sharpWords_lowValue_eq (m : Nat) :
    lowValue (sharpWordA m) = lowValue (sharpWordB m) := by
  have hv := normalize_value_conservation (sharpWordB m) 0
  simpa only [sharpWordB_normalize, Nat.mul_zero, Nat.add_zero] using hv

/-- Every finite cutoff of the two original low streams agrees. -/
theorem sharpWords_low_stream_eq (m lowCut : Nat) :
    adicNumeratorDigits lowCut (zValue 2 (sharpWordA m) - 2) =
      adicNumeratorDigits lowCut (zValue 2 (sharpWordB m) - 2) := by
  simp only [zValue, sharpWordA_length, sharpWordB_length, sharpWords_lowValue_eq]

/-- For each width at least two, complete low observation together with
only that many high digits still fails to identify a valid exterior word.
The next high digit distinguishes the same pair of witnesses. -/
theorem high_cutoff_sharp_with_complete_low (n : Nat) (hn : 2 ≤ n) :
    ∃ A B : List Nat,
      A.length = n ∧ B.length = n ∧ A ≠ B ∧
      (∀ x ∈ A, x ≤ 18) ∧ (∀ x ∈ B, x ≤ 18) ∧
      validOuter { c := 2, B := A } = true ∧
      validOuter { c := 2, B := B } = true ∧
      (∀ lowCut : Nat,
        adicNumeratorDigits lowCut (zValue 2 A - 2) =
          adicNumeratorDigits lowCut (zValue 2 B - 2)) ∧
      fractionDigits n (rhoNum 2 A)
        (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 0).2) =
        fractionDigits n (rhoNum 2 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2) ∧
      fractionDigits (n + 1) (rhoNum 2 A)
        (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 0).2) ≠
        fractionDigits (n + 1) (rhoNum 2 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2) := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 2 := ⟨n - 2, by omega⟩
  refine ⟨sharpWordA m, sharpWordB m, sharpWordA_length m,
    sharpWordB_length m, sharpWords_ne m, sharpWordA_bounded m,
    sharpWordB_bounded m, sharpWordA_valid m, sharpWordB_valid m,
    sharpWords_low_stream_eq m, ?_, sharpWords_high_boundary_ne m⟩
  rw [sharpWordA_high_prefix, sharpWordB_high_prefix]

#print axioms sharpWords_lowValue_eq
#print axioms sharpWords_low_stream_eq
#print axioms high_cutoff_sharp_with_complete_low

end Agent5.TrimmedStreamObservation
