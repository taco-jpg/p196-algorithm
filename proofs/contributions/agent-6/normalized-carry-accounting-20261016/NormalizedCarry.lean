import OuterBridge
import CoordinateThreshold

/-!
Compatibility of the original certificate carry with maximal phase-suffix
removal. The normalization and constant-band facts are Agent109's existing
theorems. The coordinate carry is the unchanged Agent6 definition.

The structural equality needs either a phase at most 18 or a bounded word.
No positive-phase, nonneutrality, canonicality, or nonempty-word assumption
is used. This module supplies interfaces only; it gives no return witness
or overflow-existence theorem.
-/

namespace Agent6.NormalizedCarry

open P196.Agent7.Finite (stripSuffix)
open Agent6.ExteriorCoordinates (overflow)

/-- Agent109's original checker carry is the coordinate carry on the raw word.
This consumes Agent109.Outer.normalize7_eq without a new normalizer proof. -/
theorem gam_eq_overflow (s : Agent109.Cert.State) :
    Agent109.Cert.gam s = overflow s.c s.B := by
  change (Agent109.norm s.B.reverse (Agent109.kOf s.c)).2 =
    (P196.Agent7.Finite.normalize s.B.reverse (Agent109.kOf s.c)).2
  rw [Agent109.Outer.normalize7_eq]

/-- A phase suffix at most 18 preserves its own incoming carry, so removing
the entire suffix preserves the final carry even for unbounded coefficients. -/
theorem overflow_stripSuffix_of_le18 (c : Nat) (B : List Nat) (hc : c ≤ 18) :
    overflow c (stripSuffix c B) = overflow c B := by
  obtain ⟨j, hj⟩ := Agent109.Outer.stripSuffix_spec c B
  have hrev := congrArg List.reverse hj
  simp only [List.reverse_append, List.reverse_replicate] at hrev
  unfold overflow
  simp only [Agent109.Outer.normalize7_eq]
  change (Agent109.norm (stripSuffix c B).reverse (Agent109.kOf c)).2 =
    (Agent109.norm B.reverse (Agent109.kOf c)).2
  rw [hrev, Agent109.norm_append, Agent109.norm_band_tail c j hc]

/-- Boundedness alone suffices for every natural phase. A nonempty removed
suffix contains the phase, which then inherits the coefficient bound. -/
theorem overflow_stripSuffix_of_bounded (c : Nat) (B : List Nat)
    (hB : Agent109.Bounded B) :
    overflow c (stripSuffix c B) = overflow c B := by
  obtain ⟨j, hj⟩ := Agent109.Outer.stripSuffix_spec c B
  cases j with
  | zero =>
      have hsame : B = stripSuffix c B := by simpa using hj
      exact congrArg (overflow c) hsame.symm
  | succ j =>
      have hmem : c ∈ B := by
        rw [hj]
        simp
      exact overflow_stripSuffix_of_le18 c B (hB c hmem)

end Agent6.NormalizedCarry

#print axioms Agent6.NormalizedCarry.gam_eq_overflow
#print axioms Agent6.NormalizedCarry.overflow_stripSuffix_of_le18
#print axioms Agent6.NormalizedCarry.overflow_stripSuffix_of_bounded
