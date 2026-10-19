import P196.FiniteExteriorHistories.Obstruction
import P196.Agent6NormalizedCarryAccounting.NormalizedCarry
import P196.Agent6CertificateCoordinateAudit.ExteriorNormalization

/-!
# Phase padding through the boundary phase eighteen

The existing carry invariance under maximal suffix removal also gives carry
invariance under phase padding. The original high numerator and its actual
denominator then scale together, preserving every high observation. These
padding identities allow arbitrary coefficient words at every phase at most
eighteen. The existing low-padding identity is already fully general.
-/

namespace Agent5.PhaseEighteenIsolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.FiniteExteriorHistories

/-- Appending a phase at most eighteen preserves the actual outgoing carry,
even when the coefficient word is unbounded. -/
theorem phase_padding_carry_of_le_eighteen
    (c : Nat) (B : List Nat) (m : Nat) (hc : c ≤ 18) :
    (normalize (B ++ List.replicate m c).reverse
      (if 10 ≤ c then 1 else 0)).2 =
      (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 := by
  change Agent6.ExteriorCoordinates.overflow c (B ++ List.replicate m c) =
    Agent6.ExteriorCoordinates.overflow c B
  calc
    _ = Agent6.ExteriorCoordinates.overflow c
        (stripSuffix c (B ++ List.replicate m c)) :=
      (Agent6.NormalizedCarry.overflow_stripSuffix_of_le18
        c (B ++ List.replicate m c) hc).symm
    _ = Agent6.ExteriorCoordinates.overflow c (stripSuffix c B) := by
      rw [Agent116.Exterior.stripSuffix_append_replicate]
    _ = Agent6.ExteriorCoordinates.overflow c B :=
      Agent6.NormalizedCarry.overflow_stripSuffix_of_le18 c B hc

/-- Phase padding preserves every literal high prefix through phase eighteen.
Each denominator retains its own width and actual outgoing carry. -/
theorem phase_padding_high_of_le_eighteen
    (c cut : Nat) (B : List Nat) (m : Nat) (hc : c ≤ 18) :
    fractionDigits cut (rhoNum c (B ++ List.replicate m c))
        (9 * 10 ^ (B ++ List.replicate m c).length *
          10 ^ (normalize (B ++ List.replicate m c).reverse
            (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  rw [rhoNum_append_replicate, phase_padding_carry_of_le_eighteen c B m hc,
    List.length_append, List.length_replicate, Nat.pow_add]
  simpa only [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using
    fractionDigits_scale cut (rhoNum c B)
      (9 * 10 ^ B.length *
        10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)
      (10 ^ m) (Nat.pow_pos (by decide))

/-- The original carry and both original finite streams are invariant under
phase padding throughout the natural phase interval from zero to eighteen. -/
theorem sameObservation_phase_padding
    (cut c : Nat) (B : List Nat) (m : Nat) (hc : c ≤ 18) :
    sameObservation cut { c := c, B := B }
      { c := c, B := B ++ List.replicate m c } := by
  exact ⟨phase_padding_carry_of_le_eighteen c B m hc,
    Agent5.TrimmedStreamObservation.phase_padding_low c cut B m,
    phase_padding_high_of_le_eighteen c cut B m hc⟩

/-- Original validity makes the exterior word fixed by maximal phase-suffix
removal, at every natural phase. -/
theorem stripSuffix_eq_of_valid (c : Nat) (B : List Nat)
    (hv : validOuter { c := c, B := B } = true) :
    stripSuffix c B = B := by
  have ht := last_ne_of_valid c B hv
  obtain ⟨m, hm⟩ := Agent109.Outer.stripSuffix_spec c B
  cases m with
  | zero => simpa using hm.symm
  | succ m =>
    exfalso
    apply ht
    rw [hm, List.replicate_succ', ← List.append_assoc, List.getLast?_append]
    simp

#print axioms phase_padding_carry_of_le_eighteen
#print axioms phase_padding_high_of_le_eighteen
#print axioms sameObservation_phase_padding
#print axioms stripSuffix_eq_of_valid

end Agent5.PhaseEighteenIsolation
