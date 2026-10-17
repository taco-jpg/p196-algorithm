import P196.Agent6CertificateCoordinateAudit.CertificateFilter

/-!
Exact boundary controls for the necessary signed-coordinate filter.

The two listed rows below have cancelling, nonzero contributions of opposite
signs, but their first link already violates the original checker's phase
transition.  This is a rejected candidate, not an accepted certificate instance.
The empty and zero-phase controls distinguish a zero sum from the sign tests.
-/

namespace Agent6.CertificateControls

open Agent109.Cert Agent6.CertificateCoordinates Agent6.CertificateFilter

/-- Ordinary lower-bound fields, with no claimed validity of the local links. -/
def controlLink : Link :=
  { j := 0, j1 := 0, j2 := 0, k := 0, lo := 2, lo' := 2 }

/-- Two normalized exteriors with contributions `-11` and `11`. -/
def cancellationCandidate : Certificate :=
  { states := [
      { c := 2, B := [1], A := [], C := [] },
      { c := 16, B := [8], A := [], C := [] }],
    links := [controlLink, controlLink] }

theorem cancellationCandidate_period : cancellationCandidate.P = 2 := rfl

theorem cancellationCandidate_link_count :
    cancellationCandidate.links.length = cancellationCandidate.P := rfl

/-- The shared coordinate projection leaves these two exterior words unchanged. -/
theorem cancellationCandidate_rows :
    rowOuter cancellationCandidate 0 = { c := 2, B := [1] } ∧
      rowOuter cancellationCandidate 1 = { c := 16, B := [8] } := by
  decide +kernel

theorem cancellationCandidate_contributions :
    rowContribution cancellationCandidate 0 = -11 ∧
      rowContribution cancellationCandidate 1 = 11 := by
  decide +kernel

theorem cancellationCandidate_sum_zero :
    rowContributionSum cancellationCandidate = 0 := by
  decide +kernel

/-- Every test in the new necessary filter passes for this explicit candidate. -/
theorem cancellationCandidate_filter_passes :
    coordinateFilter cancellationCandidate = true := by
  decide +kernel

/-- Rejection already follows from the phase equation, for arbitrary link data. -/
theorem cancellationCandidate_first_phase_failure (L L' : Link) :
    ¬ LocalOK (cancellationCandidate.st 0) (cancellationCandidate.st 1) L L' := by
  intro hlocal
  have hphase := hlocal.2.2.2.2.1
  change 4 = 16 at hphase
  omega

/-- The original full checker rejects the candidate despite its filter pass. -/
theorem cancellationCandidate_check_false :
    check cancellationCandidate = false := by
  cases hc : check cancellationCandidate with
  | false => rfl
  | true =>
    have hv := check_sound cancellationCandidate hc
    have hlocal := hv.2 0 (by decide +kernel)
    exact False.elim (cancellationCandidate_first_phase_failure _ _ hlocal)

theorem cancellationCandidate_filteredCheck_false :
    filteredCheck cancellationCandidate = false := by
  rw [filteredCheck_eq_check, cancellationCandidate_check_false]

/-- Passing the necessary filter is not a sufficient acceptance criterion. -/
theorem coordinateFilter_not_sufficient :
    ¬ (∀ cert : Certificate, coordinateFilter cert = true → check cert = true) := by
  intro h
  have hc := h cancellationCandidate cancellationCandidate_filter_passes
  rw [cancellationCandidate_check_false] at hc
  cases hc

/-- The genuinely empty list of rows. -/
def emptyCandidate : Certificate := { states := [], links := [] }

/-- A zero empty sum fails both the sign filter and the original checker. -/
theorem emptyCandidate_boundary :
    emptyCandidate.P = 0 ∧ rowContributionSum emptyCandidate = 0 ∧
      coordinateFilter emptyCandidate = false ∧ check emptyCandidate = false := by
  decide +kernel

/-- Positive listed length without phase positivity; the sole increment is zero. -/
def zeroPhaseCandidate : Certificate :=
  { states := [{ c := 0, B := [], A := [], C := [] }], links := [controlLink] }

/-- Positive length and a zero sum alone still need not supply either sign. -/
theorem zeroPhaseCandidate_boundary :
    zeroPhaseCandidate.P = 1 ∧ rowContributionSum zeroPhaseCandidate = 0 ∧
      rowContribution zeroPhaseCandidate 0 = 0 ∧
      coordinateFilter zeroPhaseCandidate = false ∧ check zeroPhaseCandidate = false := by
  decide +kernel

end Agent6.CertificateControls

#print axioms Agent6.CertificateControls.cancellationCandidate_period
#print axioms Agent6.CertificateControls.cancellationCandidate_link_count
#print axioms Agent6.CertificateControls.cancellationCandidate_rows
#print axioms Agent6.CertificateControls.cancellationCandidate_contributions
#print axioms Agent6.CertificateControls.cancellationCandidate_sum_zero
#print axioms Agent6.CertificateControls.cancellationCandidate_filter_passes
#print axioms Agent6.CertificateControls.cancellationCandidate_first_phase_failure
#print axioms Agent6.CertificateControls.cancellationCandidate_check_false
#print axioms Agent6.CertificateControls.cancellationCandidate_filteredCheck_false
#print axioms Agent6.CertificateControls.coordinateFilter_not_sufficient
#print axioms Agent6.CertificateControls.emptyCandidate_boundary
#print axioms Agent6.CertificateControls.zeroPhaseCandidate_boundary
