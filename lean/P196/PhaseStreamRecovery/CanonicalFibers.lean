import P196.PhaseStreamRecovery.WidthRecovery
import P196.Agent6CertificateCoordinateAudit.ExteriorNormalization

/-!
# Complete fibers of the original exterior stream observations

The original maximal phase-suffix removal preserves every low and high
observation. Its existing idempotence and suffix decomposition give a
canonical representative: equal streams mean equal phases and equal
stripped words. No positive-head, initial trimming, or common-width
assumption is required.

The finite classification needs only one more digit than the longer
stripped word. Since stripping cannot increase length, one more than the
longer original word is also sufficient. The classification concerns the
original exterior streams and makes no ordinary-orbit claim.
-/

namespace Agent5.PhaseStreamRecovery

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Removing the terminal phase suffix preserves every original low
observation, for any natural phase and any coefficient word. -/
theorem stripSuffix_low_stream (c cut : Nat) (B : List Nat) :
    adicNumeratorDigits cut (zValue c (stripSuffix c B) - (c : Int)) =
      adicNumeratorDigits cut (zValue c B - (c : Int)) := by
  obtain ⟨m, hm⟩ := Agent109.Outer.stripSuffix_spec c B
  have h := Agent5.TrimmedStreamObservation.phase_padding_low
    c cut (stripSuffix c B) m
  rw [← hm] at h
  exact h.symm

/-- Removing the terminal phase suffix preserves every original high
observation at a nonneutral phase, without coefficient bounds. Each side
retains its own actual width and calculated outgoing carry. -/
theorem stripSuffix_high_stream (c cut : Nat) (B : List Nat)
    (hc : nonneutralPhase c) :
    fractionDigits cut (rhoNum c (stripSuffix c B))
        (9 * 10 ^ (stripSuffix c B).length *
          10 ^ (normalize (stripSuffix c B).reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  obtain ⟨m, hm⟩ := Agent109.Outer.stripSuffix_spec c B
  have h := Agent5.TrimmedStreamObservation.phase_padding_high
    c cut (stripSuffix c B) m hc
  rw [← hm] at h
  exact h.symm

private theorem streams_eq_of_core_eq (c cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hcore : stripSuffix c A = stripSuffix c B) :
    adicNumeratorDigits cut (zValue c A - (c : Int)) =
        adicNumeratorDigits cut (zValue c B - (c : Int)) ∧
      fractionDigits cut (rhoNum c A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits cut (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  constructor
  · rw [← stripSuffix_low_stream c cut A, ← stripSuffix_low_stream c cut B, hcore]
  · rw [← stripSuffix_high_stream c cut A hc,
      ← stripSuffix_high_stream c cut B hc, hcore]

/-- Complete finite observations agree exactly when both the phase and the
canonical stripped word agree. The cutoff is measured against the stripped
lengths, allowing arbitrary extra terminal phase padding in the inputs. -/
theorem state_streams_eq_iff (c d cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : max (stripSuffix c A).length (stripSuffix d B).length + 1 ≤ cut) :
    (adicNumeratorDigits cut (zValue c A - (c : Int)) =
        adicNumeratorDigits cut (zValue d B - (d : Int)) ∧
      fractionDigits cut (rhoNum c A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits cut (rhoNum d B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) ↔
      c = d ∧ stripSuffix c A = stripSuffix d B := by
  constructor
  · rintro ⟨hlo, hhi⟩
    apply state_eq_of_common_prefixes c d cut (stripSuffix c A) (stripSuffix d B)
      hc hd (Agent116.Exterior.stripSuffix_bounded c A hA)
      (Agent116.Exterior.stripSuffix_bounded d B hB)
      (fun h => Agent116.Exterior.stripSuffix_last c A c h rfl)
      (fun h => Agent116.Exterior.stripSuffix_last d B d h rfl) hcut
    · rw [stripSuffix_low_stream, stripSuffix_low_stream]
      exact hlo
    · rw [stripSuffix_high_stream c cut A hc, stripSuffix_high_stream d cut B hd]
      exact hhi
  · rintro ⟨rfl, hcore⟩
    exact streams_eq_of_core_eq c cut A B hc hcore

/-- Equality at every cutoff has precisely one source of representation
ambiguity: terminal copies of the common phase after the same stripped word. -/
theorem all_streams_eq_iff (c d : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18) :
    (∀ cut : Nat,
      adicNumeratorDigits cut (zValue c A - (c : Int)) =
          adicNumeratorDigits cut (zValue d B - (d : Int)) ∧
        fractionDigits cut (rhoNum c A)
            (9 * 10 ^ A.length *
              10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
          fractionDigits cut (rhoNum d B)
            (9 * 10 ^ B.length *
              10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) ↔
      c = d ∧ stripSuffix c A = stripSuffix d B := by
  constructor
  · intro h
    exact (state_streams_eq_iff c d
      (max (stripSuffix c A).length (stripSuffix d B).length + 1)
      A B hc hd hA hB (Nat.le_refl _)).mp (h _)
  · rintro ⟨rfl, hcore⟩ cut
    exact streams_eq_of_core_eq c cut A B hc hcore

#print axioms stripSuffix_low_stream
#print axioms stripSuffix_high_stream
#print axioms state_streams_eq_iff
#print axioms all_streams_eq_iff

end Agent5.PhaseStreamRecovery
