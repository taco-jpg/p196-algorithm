import CertificateExterior

/-!
A stronger cyclic certificate reduction: if a finite exterior escape proof
covers every bounded even-phase exterior, its necessary-complexity conclusion
needs only the certificate checker.  No canonicality, admissibility, or positive
head premise is added.  Concrete kernel instantiation is supplied separately.
-/

namespace Agent116.CertificateExterior

open Agent109 Agent109.Cert Agent109.Outer P196.Agent7.Finite
open Agent116.Exterior

set_option maxHeartbeats 0

/-- An escape theorem including all bounded exteriors, with no positivity or
maximal-trimming predicate in its hypotheses. -/
def BoundedEscapeAt (cap : Nat) : Prop :=
  ∀ (p : Fin 8) (B : Word), Bounded B → B.length ≤ cap →
    ∃ t, cap < (outerIterate t ⟨2 * (p.val + 1), B⟩).B.length

/-- A checker-valid certificate exceeds any exterior cap possessing an
unrestricted bounded-word escape theorem.  The certificate's own arbitrary
partial trims are canonicalized using the exact outer-map identity. -/
theorem valid_exceeds_cap_unrestricted (cert : Certificate) (hv : Valid cert)
    (cap : Nat) (hexit : BoundedEscapeAt cap) :
    ∃ i, i < cert.P ∧ cap < (stripSuffix (cert.st i).c (cert.st i).B).length := by
  have hB := (hv.2 0 hv.1).2.1
  obtain ⟨p, hp⟩ := certificate_phase_index cert hv
  let B := stripSuffix (cert.st 0).c (cert.st 0).B
  have hbound : Bounded B := stripSuffix_bounded _ _ hB
  have houter : stateOuter (cert.st 0) = ⟨2 * (p.val + 1), B⟩ := by
    change ({c := (cert.st 0).c, B := B} : Outer) = _
    congr 1
  by_cases hlen : B.length ≤ cap
  · obtain ⟨t, ht⟩ := hexit p B hbound hlen
    rw [← houter, certificate_outer_orbit cert hv t] at ht
    exact ⟨t % cert.P, Nat.mod_lt t hv.1, ht⟩
  · exact ⟨0, hv.1, Nat.lt_of_not_ge hlen⟩

/-- Boolean acceptance alone gives the unrestricted complexity obstruction;
realizability is not assumed or concluded. -/
theorem accepted_exceeds_cap_unrestricted (cert : Certificate)
    (hc : check cert = true) (cap : Nat) (hexit : BoundedEscapeAt cap) :
    ∃ i, i < cert.P ∧ cap < (stripSuffix (cert.st i).c (cert.st i).B).length :=
  valid_exceeds_cap_unrestricted cert (check_sound cert hc) cap hexit

end Agent116.CertificateExterior

#print axioms Agent116.CertificateExterior.valid_exceeds_cap_unrestricted
#print axioms Agent116.CertificateExterior.accepted_exceeds_cap_unrestricted
