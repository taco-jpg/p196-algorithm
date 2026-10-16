import CertificateChecked

namespace Agent213

open Agent109 Agent109.Cert Agent110.Accounting

/-- Any accepted six-phase certificate with period below 72 has exactly
18 total overflow, so the two coordinatewise nonnegative gap gains are
necessarily a 9/0 split. This is a strict sub-72 consequence, not a
certificate instance and not a theorem about the orbit of 196. -/
theorem six_phase_sub72_gain_split
    (cert : Certificate)
    (hc : check cert = true)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c)
    (hP : cert.P < 72) :
    totalGam cert = 18 ∧
      ((totalG cert = 9 ∧ totalH cert = 0) ∨
       (totalG cert = 0 ∧ totalH cert = 9)) := by
  obtain ⟨hw, hg, hh, hgm, hhm, hom, ho, hlo, hhi, hp6, hp42⟩ :=
    Agent110.Checked.six_phase_constraints cert hc h0
  have hOlt : totalGam cert < 36 := by
    omega
  have hO : totalGam cert = 18 := by
    omega
  have hv := Agent109.Cert.check_sound cert hc
  have hsplit :=
    Agent110.Consequences.eighteen_overflows_gain_cases cert hv h0 hO
  exact ⟨hO, hsplit⟩

#print axioms six_phase_sub72_gain_split

end Agent213
