import P196.Agent2SaturatedProfile.CertificateConsequences

/-!
Agent #13 — M99-A03: coordinatewise gap-gain interface.

This file does not assert that a qualifying return certificate exists.
It packages the already-proved accounting implication in the exact form
needed by the return-construction obligation: acceptance of a return
certificate forces each accumulated gap gain to be nonnegative.

The distinction between accumulated gap gains and per-step local gains is
intentional. No claim that every local delta is nonnegative is made.
-/

namespace Agent13.M99A03

open Agent109 Agent109.Cert Agent110.Accounting

/-- A checker-qualifying return certificate has nonnegative accumulated gain
in each independent gap coordinate. -/
theorem qualifying_return_coordinatewise_nonnegative
    (cert : Certificate) (hcheck : check cert = true) :
    0 ≤ totalG cert ∧ 0 ≤ totalH cert := by
  have hv := check_sound cert hcheck
  exact ⟨totalG_nonneg cert hv, totalH_nonneg cert hv⟩

#print axioms qualifying_return_coordinatewise_nonnegative

end Agent13.M99A03
