import P196.FiniteExteriorHistories.Obstruction
import P196.Agent101ProtectedFamily.Compat
import P196.Agent6CertificateCoordinateAudit.OuterBridge

/-!
# Ordinary digit observations

The observed carry belongs to the transition from time `t` to time `t + 1`.
The two observed digit prefixes belong to that ordinary successor, using
the canonical least-significant-first digits of the accepted integer orbit.
The elementary numeric adapter also covers zero.
-/

namespace Agent5.OrdinaryExteriorHistories

open Agent115.ExteriorFactorization

/-- The full terminal carry and the separate low and high digit prefixes
of one ordinary reverse-and-add transition. -/
def ordinaryObservation (cut n t : Nat) : Nat × List Nat × List Nat :=
  ((Agent109.norm (Agent109.pairWord (Lychrel196.orbit n t)) 0).2,
    (Agent109.digits (Lychrel196.orbit n (t + 1))).take cut,
    (Agent109.digits (Lychrel196.orbit n (t + 1))).reverse.take cut)

/-- The accepted ordinary successor has exactly the canonical digits of
the normalized mirrored pair word, including its final carry digit. -/
theorem digits_step_eq_normalize (n : Nat) :
    Agent109.digits (Lychrel196.step n) =
      Agent109.normalize (Agent109.pairWord n) 0 := by
  have hvalue : Lychrel196.step n =
      Agent109.evalL (Agent109.normalize (Agent109.pairWord n) 0) := by
    rw [Agent109.Compat.step_eq, Agent109.step_eq_evalL_pair,
      Agent109.evalL_norm, Nat.add_zero]
  rw [hvalue]
  exact Agent109.digits_evalL _
    (Agent109.canon_normalize _ _ (Agent109.bounded_pair_digits n)
      (by decide) (Agent109.lastPos_pairWord n))

/-- Every nonneutral exterior phase is an admissible ordinary template
phase in the existing whole-template realization theorem. -/
theorem phase_of_nonneutral (c : Nat) (hc : nonneutralPhase c) :
    Agent109.Phase c := by
  simp [nonneutralPhase] at hc
  unfold Agent109.Phase
  omega

#print axioms digits_step_eq_normalize
#print axioms phase_of_nonneutral

end Agent5.OrdinaryExteriorHistories
