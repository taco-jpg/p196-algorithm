import P196.BoundedStreamCandidates.Arithmetic

/-!
# Recovery for the actual carry guess

Padding a valid word by its own phase gives a positive known width without
changing either original stream or its calculated high carry. The two
prefix-value identities then expose the low residue and the exact high
value at that width. Modulo-nine selection and the published positional
decoder recover the padded word, and suffix removal returns the original
valid word. This step permits every natural phase at most eighteen.
-/

namespace Agent5.BoundedStreamCandidates

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.StreamObservationInjectivity
open Agent5.PhaseEighteenIsolation Agent5.BidirectionalWordDecoder

/-- The candidate corresponding to the actual calculated carry recovers
every valid word within the supplied width bound. The phase may be odd;
its restriction to the ten even phases belongs to the final list decoder. -/
theorem candidateAtCarry_correct (N c : Nat) (B : List Nat)
    (hc : c ≤ 18) (hv : validOuter { c := c, B := B } = true)
    (hw : B.length ≤ N) :
    candidateAtCarry N c (actualCarry { c := c, B := B })
      (originalLow (N + 2) { c := c, B := B })
      (originalHigh (N + 2) { c := c, B := B }) =
      { c := c, B := B } := by
  let M := N + 1
  let g := actualCarry { c := c, B := B }
  let low := originalLow (N + 2) { c := c, B := B }
  let high := originalHigh (N + 2) { c := c, B := B }
  let X := B ++ List.replicate (M - B.length) c
  have hB := entries_le_of_valid c B hv
  have hMpos : 0 < M := by omega
  have hwM : B.length ≤ M := by omega
  have hXlen : X.length = M := by
    simp only [X, List.length_append, List.length_replicate]
    exact Nat.add_sub_of_le hwM
  have hX : ∀ x ∈ X, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hB x hx
    · rw [List.eq_of_mem_replicate hx]
      exact hc
  have hg : g ≤ 1 := normalize_carry_le B.reverse
    (if 10 ≤ c then 1 else 0)
    (fun x hx => hB x (List.mem_reverse.mp hx)) (by split <;> decide)
  have hcarry : actualCarry { c := c, B := X } = g :=
    phase_padding_carry_of_le_eighteen c B (M - B.length) hc
  have hpadLow : originalLow (N + 2) { c := c, B := X } = low :=
    Agent5.TrimmedStreamObservation.phase_padding_low c (N + 2) B (M - B.length)
  have hpadHigh : originalHigh (N + 2) { c := c, B := X } = high :=
    phase_padding_high_of_le_eighteen c (N + 2) B (M - B.length) hc
  have hR : lowValue (low.take M) = lowValue X % 10 ^ M := by
    rw [← hpadLow]
    change lowValue ((adicNumeratorDigits (N + 2)
      (zValue c X - (c : Int))).take M) = lowValue X % 10 ^ M
    rw [show N + 2 = M + 1 by omega, adicNumeratorDigits_prefix]
    have h := low_prefix_append_value c X []
    simpa only [List.append_nil, hXlen] using h
  have hH : highValue (high.take (M + g)) = highValue X + c / 9 := by
    rw [← hpadHigh]
    change highValue ((fractionDigits (N + 2) (rhoNum c X)
      (9 * 10 ^ X.length * 10 ^ actualCarry { c := c, B := X })).take (M + g)) =
      highValue X + c / 9
    rw [hcarry, show N + 2 = (M + g) + (1 - g) by omega, fractionDigits_prefix]
    have h := high_prefix_append_value c g X [] (by rw [hXlen]; omega)
    have hempty : rhoNum c [] = c := by simp [rhoNum, highValue]
    simpa only [List.append_nil, List.length_nil, Nat.pow_zero, Nat.mul_one,
      hempty, hXlen] using h
  have hV : lowValue X < 2 * 10 ^ M := by
    have h := highValue_lt X.reverse (fun x hx => hX x (List.mem_reverse.mp hx))
    rw [highValue_reverse_word, List.length_reverse, hXlen] at h
    omega
  have hrestore := restoreLow_correct M (lowValue X) (highValue X) hV
    (lowValue_highValue_mod_nine X)
  have hX90 : ∀ x ∈ X, x ≤ 90 := by
    intro x hx
    have := hX x hx
    omega
  have hdecoded : decodeValues M
      (restoreLow M (lowValue X % 10 ^ M) (highValue X)) (highValue X) = X := by
    rw [hrestore]
    simpa only [hXlen] using decodeValues_correct X hX90
  have hstrip : stripSuffix c X = B := by
    simp only [X, Agent116.Exterior.stripSuffix_append_replicate,
      stripSuffix_eq_of_valid c B hv]
  change ({ c := c, B := stripSuffix c (decodeValues M
      (restoreLow M (lowValue (low.take M)) (highValue (high.take (M + g)) - c / 9))
      (highValue (high.take (M + g)) - c / 9)) } : Outer) = { c := c, B := B }
  simp only [hR, hH, Nat.add_sub_cancel_right, hdecoded, hstrip]

#print axioms candidateAtCarry_correct

end Agent5.BoundedStreamCandidates
