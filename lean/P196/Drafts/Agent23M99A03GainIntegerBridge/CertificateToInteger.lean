import P196.Agent2SaturatedProfile.CertificateConsequences
import P196.Drafts.Agent112CertificateAdmissibility.AdmissibleCompat

/-!
Agent #23 — Manager #99 M99-A03: exact gain + certificate-to-integer interface.

This module composes two already-proved interfaces without weakening either:
* Agent #110's checker-derived coordinatewise accumulated gain bounds.
* Agent #112's automatic-admissibility bridge from a checked certificate to a
  strictly positive ordinary decimal Lychrel seed.

No certificate instance is asserted, and no conclusion about 196 is asserted.
-/

namespace Agent23.M99A03

open Agent109 Agent109.Cert Agent110.Accounting

/-- A checker-accepted certificate simultaneously exposes the exact
coordinatewise gain obligations and the ordinary-integer endpoint. -/
theorem checked_certificate_gain_integer_interface (cert : Certificate)
    (hc : check cert = true) :
    0 ≤ totalG cert ∧
    0 ≤ totalH cert ∧
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m := by
  have hg := Agent110.Accounting.totalG_nonneg cert (Agent109.Cert.check_sound cert hc)
  have hh := Agent110.Accounting.totalH_nonneg cert (Agent109.Cert.check_sound cert hc)
  have hm := Agent112.Admissibility.checked_positive_decimal_seed cert hc
  exact ⟨hg, hh, hm⟩

/-- The same bridge retains the actual reverse-and-add seed as an explicit
existential witness, rather than hiding the certificate-to-integer step behind
an abstract existence theorem. -/
theorem checked_certificate_to_positive_lychrel_seed (cert : Certificate)
    (hc : check cert = true) :
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m := by
  exact Agent112.Admissibility.checked_positive_decimal_seed cert hc

#print axioms checked_certificate_gain_integer_interface
#print axioms checked_certificate_to_positive_lychrel_seed

end Agent23.M99A03
