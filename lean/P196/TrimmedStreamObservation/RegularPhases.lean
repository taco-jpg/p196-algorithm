import P196.TrimmedStreamObservation.Arithmetic
import P196.TrimmedStreamObservation.LowPrefix
import P196.StreamObservationInjectivity.Injectivity

/-!
Agent #5: asymmetric observation without trimming in the regular phases.

For phases two, four, six, twelve, fourteen, and sixteen, bounded exterior
words of width n are determined by n low digits and n+1 high digits of
their original coordinate streams. The only possible cross-carry phase
exceptions are eight and ten, so no terminal-trimming hypothesis is needed
in the other six nonneutral phases. Zero heads and empty words are included.

The proof recovers the omitted low carry through the arithmetic phase
classification, supplies the missing boundary low digit, and applies the
existing injectivity theorem for complete finite stream observations.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Outside phases eight and ten, bounded exterior words at a shared width
are determined by n low and n+1 high literal digits without any terminal
condition or separately observed carry. -/
theorem exterior_eq_of_mixed_prefixes_of_regular_phase (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hc8 : c ≠ 8) (hc10 : c ≠ 10)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length)
    (hlo : adicNumeratorDigits A.length (zValue c A - (c : Int)) =
      adicNumeratorDigits B.length (zValue c B - (c : Int)))
    (hhi : fractionDigits (A.length + 1) (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    A = B := by
  have hN := hlo
  rw [low_prefix_normalized, low_prefix_normalized] at hN
  have hq := low_carry_eq_of_regular_high c A B hc hc8 hc10 hA hB hlen hN hhi
  apply Agent5.StreamObservationInjectivity.exterior_eq_of_stream_prefixes
    c A B hc hA hB hlen ?_ hhi
  have ha := adicNumeratorDigits_exterior c A 0 hc hA
  have hb := adicNumeratorDigits_exterior c B 0 hc hB
  simp only [Nat.add_zero, List.replicate_zero, List.append_nil] at ha hb
  rw [ha, hb, hN, hq]

#print axioms exterior_eq_of_mixed_prefixes_of_regular_phase

end Agent5.TrimmedStreamObservation
