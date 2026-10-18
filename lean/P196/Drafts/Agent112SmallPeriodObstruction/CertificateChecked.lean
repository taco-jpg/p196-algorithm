import P196.Agent2SaturatedProfile.CertificateSaturation
import P196.CertificateToLychrel.AdmissibleHeads

/-! Check-only consumers of Agent #112's automatic-admissibility theorem.
The original Agent112 source is used byte-for-byte, with pinned provenance in
the independent review directory. No concrete accepted certificate is supplied.
-/
namespace Agent110.Checked
open Agent109 Agent109.Cert Agent110.Accounting

/-- All phase classes: acceptance alone forces a nontrivial period. -/
theorem period_at_least_four (cert : Certificate) (hc : check cert = true) :
    4 ≤ cert.P := by
  obtain ⟨H, M, ha⟩ := Agent112.Admissibility.automatic_admissibility cert hc
  have hv := check_sound cert hc
  exact Agent110.Consequences.period_at_least_four cert hv
    (Agent110.CarryBudget.exterior_pos _ (hv.2 0 hv.1).1 ha.2.2.2)

/-- The full six-phase budget from the Boolean check and phase membership only.
Canonical admissibility, positive heads, the exact projected path, and all
numerical accounting conditions are derived, not additional premises. -/
theorem six_phase_constraints (cert : Certificate) (hc : check cert = true)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    totalGam cert = 2 * (totalG cert + totalH cert) ∧
    0 ≤ totalG cert ∧ 0 ≤ totalH cert ∧
    totalG cert % 9 = 0 ∧ totalH cert % 9 = 0 ∧
    totalGam cert % 18 = 0 ∧ 18 ≤ totalGam cert ∧
    2 * totalGam cert ≤ (cert.P : Int) ∧ (cert.P : Int) ≤ 4 * totalGam cert ∧
    cert.P % 6 = 0 ∧ 42 ≤ cert.P := by
  obtain ⟨H, M, ha⟩ := Agent112.Admissibility.automatic_admissibility cert hc
  obtain ⟨hw, hg, hh, hgm, hhm, hom, ho, hlo, hhi, hp6, _⟩ :=
    Agent110.Consequences.checked_six_phase_constraints cert hc H M ha h0
  exact ⟨hw, hg, hh, hgm, hhm, hom, ho, hlo, hhi, hp6,
    Agent110.CertificateSaturation.checked_period_at_least_forty_two cert hc H M ha h0⟩

/-- The saturation restriction still explicitly assumes the actual equality P=2O. -/
theorem saturated_period_constraints (cert : Certificate) (hc : check cert = true)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c)
    (hsat : 2 * totalGam cert = (cert.P : Int)) :
    cert.P % 72 = 0 ∧ 72 ≤ cert.P := by
  obtain ⟨H, M, ha⟩ := Agent112.Admissibility.automatic_admissibility cert hc
  exact Agent110.CertificateSaturation.checked_saturated_period_constraints
    cert hc H M ha h0 hsat

#print axioms period_at_least_four
#print axioms six_phase_constraints
#print axioms saturated_period_constraints
end Agent110.Checked
