import P196.Agent6CertificateCoordinateAudit.ExteriorNormalization
import P196.Agent114NeutralExteriorPadding.ExteriorPadding

/-!
# Maximal neutral exterior suffixes

This module reuses the existing generic `stripSuffix` implementation and its
proved decomposition and normalization laws.  The suffix depth is expressed
by a natural length difference.  No certificate or decimal existence claim
is made here.
-/

namespace Agent114.NeutralExteriorCanonical

open Agent120.Neutral Agent114.NeutralExteriorPadding

/-- Remove the maximal suffix consisting of the neutral coefficient. -/
def canonB (b : Nat) (B : List Nat) : List Nat :=
  P196.Agent7.Finite.stripSuffix (b - 1) B

/-- The number of removed neutral coefficients. -/
def suffixDepth (b : Nat) (B : List Nat) : Nat :=
  B.length - (canonB b B).length

theorem canonB_length_le (b : Nat) (B : List Nat) :
    (canonB b B).length ≤ B.length :=
  Agent116.Exterior.stripSuffix_length_le (b - 1) B

/-- The computed length difference is the exact neutral suffix depth. -/
theorem canonB_decompose (b : Nat) (B : List Nat) :
    suffixPad b (suffixDepth b B) (canonB b B) = B := by
  obtain ⟨j, hj⟩ := Agent109.Outer.stripSuffix_spec (b - 1) B
  have hlen : B.length = (canonB b B).length + j := by
    simpa only [List.length_append, List.length_replicate] using congrArg List.length hj
  have hd : suffixDepth b B = j := by
    unfold suffixDepth
    omega
  rw [suffixPad, hd]
  exact hj.symm

theorem canonB_suffixPad (b a : Nat) (B : List Nat) :
    canonB b (suffixPad b a B) = canonB b B :=
  Agent116.Exterior.stripSuffix_append_replicate (b - 1) B a

theorem suffixDepth_suffixPad (b a : Nat) (B : List Nat) :
    suffixDepth b (suffixPad b a B) = suffixDepth b B + a := by
  have hle := canonB_length_le b B
  unfold suffixDepth
  rw [canonB_suffixPad]
  simp only [suffixPad, List.length_append, List.length_replicate]
  omega

theorem canonB_idempotent (b : Nat) (B : List Nat) :
    canonB b (canonB b B) = canonB b B :=
  Agent116.Exterior.stripSuffix_idempotent (b - 1) B

theorem suffixDepth_canonB (b : Nat) (B : List Nat) :
    suffixDepth b (canonB b B) = 0 := by
  simp only [suffixDepth, canonB_idempotent, Nat.sub_self]

/-- Empty normalized words are included by the optional-last formulation. -/
theorem canonB_last_ne (b : Nat) (B : List Nat) :
    (canonB b B).getLast? ≠ some (b - 1) := by
  intro h
  exact (Agent116.Exterior.stripSuffix_last (b - 1) B (b - 1) h) rfl

theorem canonB_eq_self_iff (b : Nat) (B : List Nat) :
    canonB b B = B ↔ B.getLast? ≠ some (b - 1) := by
  constructor
  · intro h
    have hn := canonB_last_ne b B
    rwa [h] at hn
  · intro hn
    have hd := canonB_decompose b B
    by_cases hz : suffixDepth b B = 0
    · simpa [suffixPad, hz] using hd
    · have hl : B.getLast? = some (b - 1) := by
        rw [← hd]
        simp [suffixPad, List.getLast?_replicate, hz]
      exact False.elim (hn hl)

/-- Removing a maximal neutral suffix preserves all original A120 hypotheses. -/
theorem canonB_hyp_iff (b : Nat) (B C : List Nat) :
    Hyp b (canonB b B) C ↔ Hyp b B C := by
  have h := hyp_suffixPad_iff (b := b) (B := canonB b B) (C := C) (suffixDepth b B)
  rw [canonB_decompose] at h
  exact h.symm

end Agent114.NeutralExteriorCanonical

#print axioms Agent114.NeutralExteriorCanonical.canonB_decompose
#print axioms Agent114.NeutralExteriorCanonical.suffixDepth_suffixPad
#print axioms Agent114.NeutralExteriorCanonical.canonB_eq_self_iff
#print axioms Agent114.NeutralExteriorCanonical.canonB_hyp_iff
