import P196.Agent6CertificateCoordinateAudit.CertificateExterior
import P196.Agent2SaturatedProfile.CertificateAccounting
import P196.Agent6CoordinateDynamics.CoordinateCycle

/-!
Signed-coordinate necessary conditions for the unchanged Agent109 certificate
checker.  Each listed exterior is maximally suffix-trimmed through the existing
Agent116 projection before its contribution is evaluated.  Acceptance supplies
the entire closed orbit and its positive initial phase; no realization, width,
positive-head, or additional canonicality hypothesis is imposed.
-/

namespace Agent6.CertificateCoordinates

open Agent109.Cert Agent110.Accounting
open P196.Agent7.Finite (Outer)
open Agent6.ExteriorCoordinates

/-- The existing normalized exterior projection of a listed certificate row. -/
def rowOuter (cert : Certificate) (i : Nat) : Outer :=
  Agent116.CertificateExterior.stateOuter (cert.st i)

/-- The signed high-side contribution of a normalized certificate row. -/
def rowContribution (cert : Certificate) (i : Nat) : Int :=
  highContribution (rowOuter cert i).c (rowOuter cert i).B

/-- Total signed contribution over exactly the listed certificate rows. -/
def rowContributionSum (cert : Certificate) : Int :=
  sumPrefix (rowContribution cert) cert.P

private theorem coordinateIter_eq_original (n : Nat) (s : Outer) :
    outerIter n s = Agent109.Outer.outerIter n s := by
  induction n with
  | zero => rfl
  | succ n ih => exact congrArg P196.Agent7.Finite.outerNext ih

/-- The original certificate projection, expressed in the coordinate iterator. -/
theorem rowOuter_orbit (cert : Certificate) (hv : Valid cert) (n : Nat) :
    outerIter n (rowOuter cert 0) = rowOuter cert (n % cert.P) := by
  rw [coordinateIter_eq_original, ← Agent109.Outer.outerIterate_eq]
  exact Agent116.CertificateExterior.certificate_outer_orbit cert hv n

/-- Before the period boundary, the orbit is the exact listed normalized row. -/
theorem rowOuter_orbit_of_lt (cert : Certificate) (hv : Valid cert)
    (i : Nat) (hi : i < cert.P) :
    outerIter i (rowOuter cert 0) = rowOuter cert i := by
  simpa only [Nat.mod_eq_of_lt hi] using rowOuter_orbit cert hv i

/-- A valid certificate supplies a literal closed exterior orbit. -/
theorem rowOuter_closed (cert : Certificate) (hv : Valid cert) :
    outerIter cert.P (rowOuter cert 0) = rowOuter cert 0 := by
  simpa only [Nat.mod_self] using rowOuter_orbit cert hv cert.P

private theorem orbitSum_eq_sumPrefix (f : Outer → Int) (s : Outer) (n : Nat) :
    orbitSum f s n = sumPrefix (fun i => f (outerIter i s)) n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [orbitSum_succ, sumPrefix, ih]

/-- Transport any signed observable from the closed orbit to the listed rows. -/
theorem rowSum_eq_orbitSum (cert : Certificate) (hv : Valid cert)
    (f : Outer → Int) :
    sumPrefix (fun i => f (rowOuter cert i)) cert.P =
      orbitSum f (rowOuter cert 0) cert.P := by
  rw [orbitSum_eq_sumPrefix]
  apply sumPrefix_congr
  intro i hi
  rw [rowOuter_orbit_of_lt cert hv i hi]

/-- The row contribution sum equals the existing literal-orbit contribution sum. -/
theorem rowContributionSum_eq_contributionSum (cert : Certificate) (hv : Valid cert) :
    rowContributionSum cert = contributionSum (rowOuter cert 0) cert.P := by
  exact rowSum_eq_orbitSum cert hv (fun q => highContribution q.c q.B)

/-- The signed contribution cancels over every valid certificate. -/
theorem valid_row_contribution_sum_eq_zero (cert : Certificate) (hv : Valid cert) :
    rowContributionSum cert = 0 := by
  rw [rowContributionSum_eq_contributionSum cert hv]
  exact closed_orbit_contributionSum_eq_zero (rowOuter cert 0) cert.P
    (rowOuter_closed cert hv)

/-- Direct checker-facing cancellation, with no additional premise. -/
theorem checked_row_contribution_sum_eq_zero (cert : Certificate)
    (hc : check cert = true) : rowContributionSum cert = 0 :=
  valid_row_contribution_sum_eq_zero cert (check_sound cert hc)

/-- A valid certificate has both a positive and a negative normalized-row
contribution.  Positivity of the initial phase comes from the first checked link. -/
theorem valid_row_both_signs (cert : Certificate) (hv : Valid cert) :
    (∃ i, i < cert.P ∧ 0 < rowContribution cert i) ∧
      (∃ j, j < cert.P ∧ rowContribution cert j < 0) := by
  have hphase : 0 < (rowOuter cert 0).c := by
    change 0 < (cert.st 0).c
    have := (hv.2 0 hv.1).1.1
    omega
  obtain ⟨⟨i, hi, hpos⟩, ⟨j, hj, hneg⟩⟩ :=
    closed_orbit_both_signs_of_pos (rowOuter cert 0) cert.P hphase hv.1
      (rowOuter_closed cert hv)
  constructor
  · refine ⟨i, hi, ?_⟩
    rw [rowOuter_orbit_of_lt cert hv i hi] at hpos
    exact hpos
  · refine ⟨j, hj, ?_⟩
    rw [rowOuter_orbit_of_lt cert hv j hj] at hneg
    exact hneg

/-- Direct checker-facing positive and negative row witnesses. -/
theorem checked_row_both_signs (cert : Certificate) (hc : check cert = true) :
    (∃ i, i < cert.P ∧ 0 < rowContribution cert i) ∧
      (∃ j, j < cert.P ∧ rowContribution cert j < 0) :=
  valid_row_both_signs cert (check_sound cert hc)

/-- The finite signed-coordinate conditions forced by the original checker. -/
theorem checked_coordinate_conditions (cert : Certificate) (hc : check cert = true) :
    rowContributionSum cert = 0 ∧
      (∃ i, i < cert.P ∧ 0 < rowContribution cert i) ∧
      (∃ j, j < cert.P ∧ rowContribution cert j < 0) :=
  ⟨checked_row_contribution_sum_eq_zero cert hc, checked_row_both_signs cert hc⟩

private theorem orbitSum_overflowBit_eq_count (s : Outer) (n : Nat) :
    orbitSum (fun q => (overflowBit q : Int)) s n = (overflowCount s n : Int) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [orbitSum_succ, overflowCount_succ, Int.natCast_add, ih]

/-- The existing weighted balance transported to the exact normalized rows.
The final term counts their overflow indicators; it does not assume equality
with the original checker's unnormalized-row totalGam. -/
theorem checked_row_weighted_balance (cert : Certificate) (hc : check cert = true) :
    sumPrefix (fun i => weightedPhase (rowOuter cert i)) cert.P =
      9 * sumPrefix (fun i => weightedReverse (rowOuter cert i)) cert.P +
        9 * sumPrefix (fun i => (overflowBit (rowOuter cert i) : Int)) cert.P := by
  have hv := check_sound cert hc
  rw [rowSum_eq_orbitSum cert hv weightedPhase,
    rowSum_eq_orbitSum cert hv weightedReverse,
    rowSum_eq_orbitSum cert hv (fun q => (overflowBit q : Int)),
    orbitSum_overflowBit_eq_count]
  exact closed_orbit_weighted_balance (rowOuter cert 0) cert.P (rowOuter_closed cert hv)

end Agent6.CertificateCoordinates

#print axioms Agent6.CertificateCoordinates.rowOuter_orbit
#print axioms Agent6.CertificateCoordinates.rowOuter_orbit_of_lt
#print axioms Agent6.CertificateCoordinates.rowOuter_closed
#print axioms Agent6.CertificateCoordinates.rowSum_eq_orbitSum
#print axioms Agent6.CertificateCoordinates.rowContributionSum_eq_contributionSum
#print axioms Agent6.CertificateCoordinates.valid_row_contribution_sum_eq_zero
#print axioms Agent6.CertificateCoordinates.checked_row_contribution_sum_eq_zero
#print axioms Agent6.CertificateCoordinates.valid_row_both_signs
#print axioms Agent6.CertificateCoordinates.checked_row_both_signs
#print axioms Agent6.CertificateCoordinates.checked_coordinate_conditions
#print axioms Agent6.CertificateCoordinates.checked_row_weighted_balance
