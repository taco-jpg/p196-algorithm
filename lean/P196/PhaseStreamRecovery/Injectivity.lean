import P196.PhaseStreamRecovery.Decoder
import P196.StreamObservationInjectivity.Injectivity

/-!
# Exterior phase and word from finite original streams

Agent #5. The phase decoder removes the supplied common-phase hypothesis
from the existing complete-prefix reconstruction theorem. At a shared width
n, the first n+1 low and high digits identify both the nonneutral phase and
every bounded coefficient. Each observation retains its own original phase
and its own calculated normalization carry. Trimming and positive heads are
not required, and the empty word is included.
-/

namespace Agent5.PhaseStreamRecovery

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Complete finite observations determine the nonneutral phase without a
previously supplied phase equality. -/
theorem phase_eq_of_stream_prefixes (c d : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length)
    (hlo : adicNumeratorDigits (A.length + 1) (zValue c A - (c : Int)) =
      adicNumeratorDigits (B.length + 1) (zValue d B - (d : Int)))
    (hhi : fractionDigits (A.length + 1) (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits (B.length + 1) (rhoNum d B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) :
    c = d := by
  calc
    c = decodePhase A.length
        (adicNumeratorDigits (A.length + 1) (zValue c A - (c : Int)))
        (fractionDigits (A.length + 1) (rhoNum c A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2)) :=
      (decodePhase_correct c A hc hA).symm
    _ = decodePhase B.length
        (adicNumeratorDigits (B.length + 1) (zValue d B - (d : Int)))
        (fractionDigits (B.length + 1) (rhoNum d B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) := by
      rw [hlo, hhi, hlen]
    _ = d := decodePhase_correct d B hd hB

/-- Both the phase and the original coefficient word are identified at a
shared width. The word-recovery step imports the fixed-phase theorem. -/
theorem state_eq_of_stream_prefixes (c d : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length)
    (hlo : adicNumeratorDigits (A.length + 1) (zValue c A - (c : Int)) =
      adicNumeratorDigits (B.length + 1) (zValue d B - (d : Int)))
    (hhi : fractionDigits (A.length + 1) (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits (B.length + 1) (rhoNum d B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) :
    c = d ∧ A = B := by
  have hphase := phase_eq_of_stream_prefixes c d A B hc hd hA hB hlen hlo hhi
  subst d
  exact ⟨rfl, Agent5.StreamObservationInjectivity.exterior_eq_of_stream_prefixes
    c A B hc hA hB hlen hlo hhi⟩

/-- Any common cutoff containing the complete prefixes still identifies
the phase and word, without a common-phase hypothesis. -/
theorem state_eq_of_streams_at_cutoff (c d cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length) (hcut : A.length + 1 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue d B - (d : Int)))
    (hhi : fractionDigits cut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum d B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) :
    c = d ∧ A = B := by
  have hsum : A.length + 1 + (cut - (A.length + 1)) = cut :=
    Nat.add_sub_of_le hcut
  have low_take (a : Int) :
      (adicNumeratorDigits cut a).take (A.length + 1) =
        adicNumeratorDigits (A.length + 1) a := by
    simpa only [hsum] using
      adicNumeratorDigits_prefix (A.length + 1) (cut - (A.length + 1)) a
  have high_take (r D : Nat) :
      (fractionDigits cut r D).take (A.length + 1) =
        fractionDigits (A.length + 1) r D := by
    simpa only [hsum] using
      fractionDigits_prefix (A.length + 1) (cut - (A.length + 1)) r D
  apply state_eq_of_stream_prefixes c d A B hc hd hA hB hlen
  · have h := congrArg (List.take (A.length + 1)) hlo
    rw [low_take, low_take] at h
    simpa only [hlen] using h
  · have h := congrArg (List.take (A.length + 1)) hhi
    rw [high_take, high_take] at h
    simpa only [hlen] using h

#print axioms phase_eq_of_stream_prefixes
#print axioms state_eq_of_stream_prefixes
#print axioms state_eq_of_streams_at_cutoff

end Agent5.PhaseStreamRecovery
