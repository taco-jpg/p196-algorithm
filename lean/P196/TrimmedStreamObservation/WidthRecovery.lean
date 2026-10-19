import P196.StreamObservationInjectivity.Injectivity

/-!
# Finite stream recovery without a shared word width

Appending copies of the phase preserves both original coordinate streams.
After padding to a shared width, the existing complete-prefix injectivity
theorem recovers the padded words. Trimming then recovers their original
widths and coefficients. Positive heads are not required.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Padding by the phase preserves the outgoing high carry for arbitrary
coefficient words. -/
theorem phase_padding_carry (c : Nat) (B : List Nat) (m : Nat)
    (hc : nonneutralPhase c) :
    (normalize (B ++ List.replicate m c).reverse
      (if 10 ≤ c then 1 else 0)).2 =
      (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 := by
  let k : Nat := if 10 ≤ c then 1 else 0
  change (normalize (B ++ List.replicate m c).reverse k).2 =
    (normalize B.reverse k).2
  have hk : k ≤ 1 := by
    dsimp [k]
    split <;> decide
  have hr : (c + k) / 10 = k := (phase_facts c k hc hk).1
  induction m with
  | zero => simp
  | succ m ih =>
      rw [List.replicate_succ', ← List.append_assoc, List.reverse_append,
        show [c].reverse = [c] from rfl, List.singleton_append]
      simpa only [normalize, hr] using ih

/-- Phase padding preserves every finite low observation, for every natural
phase and without coefficient bounds. -/
theorem phase_padding_low (c cut : Nat) (B : List Nat) (m : Nat) :
    adicNumeratorDigits cut (zValue c (B ++ List.replicate m c) - (c : Int)) =
      adicNumeratorDigits cut (zValue c B - (c : Int)) := by
  rw [zValue_append_replicate]

/-- At a nonneutral phase, padding preserves every finite high observation
without coefficient bounds. The numerator and denominator scale together. -/
theorem phase_padding_high (c cut : Nat) (B : List Nat) (m : Nat)
    (hc : nonneutralPhase c) :
    fractionDigits cut (rhoNum c (B ++ List.replicate m c))
      (9 * 10 ^ (B ++ List.replicate m c).length *
        10 ^ (normalize (B ++ List.replicate m c).reverse
          (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  rw [rhoNum_append_replicate, phase_padding_carry c B m hc,
    List.length_append, List.length_replicate, Nat.pow_add]
  have hD :
      9 * (10 ^ B.length * 10 ^ m) *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 =
        10 ^ m * (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
    ac_rfl
  rw [hD]
  exact fractionDigits_scale cut (rhoNum c B)
    (9 * 10 ^ B.length *
      10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)
    (10 ^ m) (Nat.pow_pos (by decide))

private theorem exterior_eq_of_common_prefixes_of_length_le
    (c cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (htB : B.getLast? ≠ some c) (hlen : A.length ≤ B.length)
    (hcut : B.length + 1 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue c B - (c : Int)))
    (hhi : fractionDigits cut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    A = B := by
  obtain ⟨m, hm⟩ : ∃ m, B.length = A.length + m :=
    ⟨B.length - A.length, by omega⟩
  have hp : (A ++ List.replicate m c).length = B.length := by simp [hm]
  have hc18 : c ≤ 18 := (phase_facts c 0 hc (by decide)).2.2.2.2
  have hbound : ∀ x ∈ A ++ List.replicate m c, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hA x hx
    · rw [List.eq_of_mem_replicate hx]
      exact hc18
  have hpad : A ++ List.replicate m c = B := by
    apply Agent5.StreamObservationInjectivity.exterior_eq_of_streams_at_cutoff
      c cut (A ++ List.replicate m c) B hc hbound hB hp
    · rw [hp]
      exact hcut
    · rw [phase_padding_low]
      exact hlo
    · rw [phase_padding_high c cut A m hc]
      exact hhi
  cases m with
  | zero => simpa using hpad
  | succ m =>
      exfalso
      apply htB
      rw [← hpad, List.replicate_succ', ← List.append_assoc, List.getLast?_append]
      simp

/-- Complete observations at a common cutoff recover bounded trimmed words
of arbitrary, potentially different widths. -/
theorem exterior_eq_of_common_prefixes (c cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (htA : A.getLast? ≠ some c) (htB : B.getLast? ≠ some c)
    (hcut : max A.length B.length + 1 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue c B - (c : Int)))
    (hhi : fractionDigits cut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    A = B := by
  have hcutA : A.length + 1 ≤ cut := by
    have := Nat.le_max_left A.length B.length
    omega
  have hcutB : B.length + 1 ≤ cut := by
    have := Nat.le_max_right A.length B.length
    omega
  rcases Nat.le_total A.length B.length with hlen | hlen
  · exact exterior_eq_of_common_prefixes_of_length_le
      c cut A B hc hA hB htB hlen hcutB hlo hhi
  · exact (exterior_eq_of_common_prefixes_of_length_le
      c cut B A hc hB hA htA hlen hcutA hlo.symm hhi.symm).symm

/-- The original validity predicate supplies the coefficient bounds and
trimming needed for recovery without a shared width. -/
theorem valid_exterior_eq_of_common_prefixes (c cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hvA : validOuter { c := c, B := A } = true)
    (hvB : validOuter { c := c, B := B } = true)
    (hcut : max A.length B.length + 1 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue c B - (c : Int)))
    (hhi : fractionDigits cut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    A = B := by
  exact exterior_eq_of_common_prefixes c cut A B hc
    (entries_le_of_valid c A hvA) (entries_le_of_valid c B hvB)
    (last_ne_of_valid c A hvA) (last_ne_of_valid c B hvB) hcut hlo hhi

#print axioms phase_padding_carry
#print axioms phase_padding_low
#print axioms phase_padding_high
#print axioms exterior_eq_of_common_prefixes
#print axioms valid_exterior_eq_of_common_prefixes

end Agent5.TrimmedStreamObservation
