import P196.BoundedStreamCandidates.Definitions

/-!
# The low coordinate from a finite original prefix

At a fixed width, one additional low term reads the low value plus a
common phase shift modulo the next width scale. Bounded coefficients put
both low values below that scale, so cancellation recovers the exact
value. Phase padding then transports the result to unequal original
widths without any high-stream, carry, or validity assumption.
-/

namespace Agent5.CompleteStreamDecoder

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.BoundedStreamCandidates
open Agent5.PhaseEighteenIsolation

private theorem eq_of_shifted_mod_eq (Q a x y : Nat)
    (hx : x < Q) (hy : y < Q) (h : (x + a) % Q = (y + a) % Q) : x = y := by
  have hX := Nat.mod_add_mod_eq (a := x) (b := a) (c := Q)
  have hY := Nat.mod_add_mod_eq (a := y) (b := a) (c := Q)
  rw [Nat.mod_eq_of_lt hx] at hX
  rw [Nat.mod_eq_of_lt hy] at hY
  split at hX <;> split at hY <;> omega

private theorem low_boundary_value (c : Nat) (B : List Nat) :
    lowValue (originalLow (B.length + 1) { c := c, B := B }) =
      (lowValue B + 10 ^ B.length * c) % 10 ^ (B.length + 1) := by
  have h := low_prefix_append_value c (B ++ [c]) []
  have hsingle : lowValue [c] = c := by simp [lowValue]
  simpa only [originalLow, List.append_nil, List.length_append, List.length_singleton,
    zValue_append_band, lowValue_append, hsingle] using h

private theorem lowValue_eq_of_low_boundary (c : Nat) (A B : List Nat)
    (hlen : A.length = B.length)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlo : originalLow (A.length + 1) { c := c, B := A } =
      originalLow (A.length + 1) { c := c, B := B }) :
    lowValue A = lowValue B := by
  have h := congrArg lowValue hlo
  have hBreading := low_boundary_value c B
  rw [← hlen] at hBreading
  rw [low_boundary_value c A, hBreading] at h
  have hVA := highValue_lt A.reverse
    (fun x hx => hA x (List.mem_reverse.mp hx))
  have hVB := highValue_lt B.reverse
    (fun x hx => hB x (List.mem_reverse.mp hx))
  rw [highValue_reverse_word, List.length_reverse] at hVA
  rw [highValue_reverse_word, List.length_reverse, ← hlen] at hVB
  have hP : 0 < 10 ^ A.length := Nat.pow_pos (by decide)
  apply eq_of_shifted_mod_eq (10 ^ A.length * 10) (10 ^ A.length * c)
    (lowValue A) (lowValue B) (by omega) (by omega)
  simpa only [Nat.pow_succ] using h

/-- At a fixed phase at most eighteen, an original low prefix reaching
beyond both word boundaries determines the exact centered low coordinate.
The coefficient words need not have positive heads or trimmed suffixes. -/
theorem zValue_eq_of_low_prefix (c cut : Nat) (A B : List Nat)
    (hc : c ≤ 18)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : max A.length B.length + 2 ≤ cut)
    (hlo : originalLow cut { c := c, B := A } =
      originalLow cut { c := c, B := B }) :
    zValue c A = zValue c B := by
  let M := max A.length B.length + 1
  let X := A ++ List.replicate (M - A.length) c
  let Y := B ++ List.replicate (M - B.length) c
  have hAM : A.length ≤ M := by
    have := Nat.le_max_left A.length B.length
    omega
  have hBM : B.length ≤ M := by
    have := Nat.le_max_right A.length B.length
    omega
  have hXlen : X.length = M := by
    simp only [X, List.length_append, List.length_replicate]
    exact Nat.add_sub_of_le hAM
  have hYlen : Y.length = M := by
    simp only [Y, List.length_append, List.length_replicate]
    exact Nat.add_sub_of_le hBM
  have hX : ∀ x ∈ X, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hA x hx
    · rw [List.eq_of_mem_replicate hx]
      exact hc
  have hY : ∀ x ∈ Y, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hB x hx
    · rw [List.eq_of_mem_replicate hx]
      exact hc
  have hpA : originalLow cut { c := c, B := X } =
      originalLow cut { c := c, B := A } :=
    Agent5.TrimmedStreamObservation.phase_padding_low c cut A (M - A.length)
  have hpB : originalLow cut { c := c, B := Y } =
      originalLow cut { c := c, B := B } :=
    Agent5.TrimmedStreamObservation.phase_padding_low c cut B (M - B.length)
  have hpadded := hpA.trans (hlo.trans hpB.symm)
  have hprefix : originalLow (M + 1) { c := c, B := X } =
      originalLow (M + 1) { c := c, B := Y } := by
    have h := congrArg (List.take (M + 1)) hpadded
    change (adicNumeratorDigits cut (zValue c X - (c : Int))).take (M + 1) =
      (adicNumeratorDigits cut (zValue c Y - (c : Int))).take (M + 1) at h
    rw [show cut = (M + 1) + (cut - (M + 1)) by omega] at h
    simpa only [adicNumeratorDigits_prefix] using h
  have hvalues := lowValue_eq_of_low_boundary c X Y (hXlen.trans hYlen.symm)
    hX hY (by simpa only [hXlen] using hprefix)
  have hz : zValue c X = zValue c Y := by
    simp only [zValue, hvalues, hXlen, hYlen]
  simpa only [X, Y, zValue_append_replicate] using hz

#print axioms zValue_eq_of_low_prefix

end Agent5.CompleteStreamDecoder
