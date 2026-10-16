import NormalizedCarry
import CertificateCoordinates

/-!
Connect the existing normalized exterior-coordinate observables to the original
Agent109 certificate carry and Agent110 band-gain accounting.  The state-level
bridge needs only bounded raw exterior coefficients: phases 0, 9, 18, and larger
natural phases remain included.  The checker-facing balances use the unchanged
checker alone, and do not assert that any accepting certificate exists.
-/

namespace Agent6.CertificateCarryAccounting

open Agent109 Agent109.Cert Agent110.Accounting
open Agent116.CertificateExterior
open Agent6.ExteriorCoordinates Agent6.CertificateCoordinates

/-- The normalized exterior indicator is the original numerical carry when the
raw exterior word is bounded.  No bound on the phase or interior words is needed. -/
theorem overflowBit_stateOuter (s : State) (hB : Bounded s.B) :
    overflowBit (stateOuter s) = gam s := by
  have hcarry : overflow (stateOuter s).c (stateOuter s).B = gam s := by
    change overflow s.c (P196.Agent7.Finite.stripSuffix s.c s.B) = gam s
    rw [Agent6.NormalizedCarry.overflow_stripSuffix_of_bounded s.c s.B hB,
      ← Agent6.NormalizedCarry.gam_eq_overflow s]
  have hgam : gam s ≤ 1 := gamma_le s.c s.B s.A s.C hB
  unfold overflowBit
  rw [← overflow_eq_highValue, hcarry]
  split <;> omega

/-- On exactly the listed rows, bounded raw exterior words identify the new
indicator sum with the original carry total.  No checker premise is required. -/
theorem rowOverflowSum_eq_totalGam_of_bounded (cert : Certificate)
    (hB : ∀ i, i < cert.P → Bounded (cert.st i).B) :
    sumPrefix (fun i => (overflowBit (rowOuter cert i) : Int)) cert.P =
      totalGam cert := by
  unfold totalGam
  apply sumPrefix_congr
  intro i hi
  exact congrArg (fun n : Nat => (n : Int))
    (overflowBit_stateOuter (cert.st i) (hB i hi))

/-- Original validity supplies each raw row's coefficient bound. -/
theorem valid_rowOverflowSum_eq_totalGam (cert : Certificate) (hv : Valid cert) :
    sumPrefix (fun i => (overflowBit (rowOuter cert i) : Int)) cert.P =
      totalGam cert := by
  apply rowOverflowSum_eq_totalGam_of_bounded
  intro i hi
  exact (hv.2 i hi).2.1

/-- Direct checker endpoint for normalized versus original carry accounting. -/
theorem checked_rowOverflowSum_eq_totalGam (cert : Certificate)
    (hc : check cert = true) :
    sumPrefix (fun i => (overflowBit (rowOuter cert i) : Int)) cert.P =
      totalGam cert :=
  valid_rowOverflowSum_eq_totalGam cert (check_sound cert hc)

/-- The previously checked coordinate balance, now expressed using the original
certificate's carry total rather than an unconnected normalized indicator sum. -/
theorem checked_weighted_balance_totalGam (cert : Certificate)
    (hc : check cert = true) :
    sumPrefix (fun i => weightedPhase (rowOuter cert i)) cert.P =
      9 * sumPrefix (fun i => weightedReverse (rowOuter cert i)) cert.P +
        9 * totalGam cert := by
  rw [← checked_rowOverflowSum_eq_totalGam cert hc]
  exact checked_row_weighted_balance cert hc

/-- Reuse Agent110's exact band-gain accounting in the normalized coordinate
balance.  The only input remains acceptance by the original checker. -/
theorem checked_weighted_balance_gains (cert : Certificate)
    (hc : check cert = true) :
    sumPrefix (fun i => weightedPhase (rowOuter cert i)) cert.P =
      9 * sumPrefix (fun i => weightedReverse (rowOuter cert i)) cert.P +
        18 * (totalG cert + totalH cert) := by
  have hb := checked_weighted_balance_totalGam cert hc
  have hg := totalGam_eq_twice_gains cert (check_sound cert hc)
  omega

end Agent6.CertificateCarryAccounting

#print axioms Agent6.CertificateCarryAccounting.overflowBit_stateOuter
#print axioms Agent6.CertificateCarryAccounting.rowOverflowSum_eq_totalGam_of_bounded
#print axioms Agent6.CertificateCarryAccounting.valid_rowOverflowSum_eq_totalGam
#print axioms Agent6.CertificateCarryAccounting.checked_rowOverflowSum_eq_totalGam
#print axioms Agent6.CertificateCarryAccounting.checked_weighted_balance_totalGam
#print axioms Agent6.CertificateCarryAccounting.checked_weighted_balance_gains
