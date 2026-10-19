import P196.TrimmedStreamObservation.Arithmetic
import P196.TrimmedStreamObservation.LowPrefix
import P196.StreamObservationInjectivity.Injectivity

/-!
# Trimmed exterior words from asymmetric observations

Agent #5. At a fixed nonneutral phase and shared width n, terminal trimming
allows recovery from only n low digits and n+1 high digits of the original
coordinate streams. The missing low normalization carry is derived from the
high observation. No positive-head condition or separately known high carry
is required, and the empty word is included.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- A terminal-trimmed bounded word is determined by the first n low digits
and the first n+1 high digits, at a shared width n and nonneutral phase. -/
theorem exterior_eq_of_mixed_prefixes (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length)
    (htA : A.getLast? ≠ some c) (htB : B.getLast? ≠ some c)
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
  have hq := low_carry_eq_of_trimmed_high c A B hc hA hB hlen htA htB hN hhi
  apply Agent5.StreamObservationInjectivity.exterior_eq_of_stream_prefixes
    c A B hc hA hB hlen ?_ hhi
  have ha := adicNumeratorDigits_exterior c A 0 hc hA
  have hb := adicNumeratorDigits_exterior c B 0 hc hB
  simp only [Nat.add_zero, List.replicate_zero, List.append_nil] at ha hb
  rw [ha, hb, hN, hq]

/-- The existing validity predicate supplies the coefficient bounds and
terminal trimming for the asymmetric observation theorem. -/
theorem valid_exterior_eq_of_mixed_prefixes (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hvA : validOuter { c := c, B := A } = true)
    (hvB : validOuter { c := c, B := B } = true)
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
  exact exterior_eq_of_mixed_prefixes c A B hc
    (entries_le_of_valid c A hvA) (entries_le_of_valid c B hvB) hlen
    (last_ne_of_valid c A hvA) (last_ne_of_valid c B hvB) hlo hhi

/-- Larger independent cutoffs remain sufficient once they contain n low
digits and n+1 high digits. -/
theorem exterior_eq_of_mixed_cutoffs (c lowCut highCut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length)
    (htA : A.getLast? ≠ some c) (htB : B.getLast? ≠ some c)
    (hloCut : A.length ≤ lowCut) (hhiCut : A.length + 1 ≤ highCut)
    (hlo : adicNumeratorDigits lowCut (zValue c A - (c : Int)) =
      adicNumeratorDigits lowCut (zValue c B - (c : Int)))
    (hhi : fractionDigits highCut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits highCut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    A = B := by
  have hsumLo : A.length + (lowCut - A.length) = lowCut :=
    Nat.add_sub_of_le hloCut
  have hsumHi : A.length + 1 + (highCut - (A.length + 1)) = highCut :=
    Nat.add_sub_of_le hhiCut
  have low_take (a : Int) :
      (adicNumeratorDigits lowCut a).take A.length =
        adicNumeratorDigits A.length a := by
    simpa only [hsumLo] using
      adicNumeratorDigits_prefix A.length (lowCut - A.length) a
  have high_take (r D : Nat) :
      (fractionDigits highCut r D).take (A.length + 1) =
        fractionDigits (A.length + 1) r D := by
    simpa only [hsumHi] using
      fractionDigits_prefix (A.length + 1) (highCut - (A.length + 1)) r D
  apply exterior_eq_of_mixed_prefixes c A B hc hA hB hlen htA htB
  · have h := congrArg (List.take A.length) hlo
    rw [low_take, low_take] at h
    simpa only [hlen] using h
  · have h := congrArg (List.take (A.length + 1)) hhi
    rw [high_take, high_take] at h
    simpa only [hlen] using h

#print axioms exterior_eq_of_mixed_prefixes
#print axioms valid_exterior_eq_of_mixed_prefixes
#print axioms exterior_eq_of_mixed_cutoffs

end Agent5.TrimmedStreamObservation
