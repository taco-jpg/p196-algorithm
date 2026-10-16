import CertificateUnrestricted
import Cap3AllBounds

/-!
Kernel-certified obstruction to every accepted return certificate whose
normalized exteriors have length at most three.  Acceptance is the only premise:
canonical realizability and a positive leading coefficient are not required.
The escape premise of the generic theorem is discharged by the complete
unrestricted cap-three finite proof, including zero-leading and untrimmed words.
-/

namespace Agent116.CertificateExterior

open Agent109 Agent109.Cert P196.Agent7.Finite
open Agent116.Exterior

/-- The unrestricted kernel cap-three graph supplies the generic escape
contract, including every bounded zero-leading or untrimmed exterior. -/
theorem boundedEscapeAt_three : BoundedEscapeAt 3 := by
  intro p B hB hlen
  obtain ⟨t, _, ht⟩ := P196.Agent116.Cap3.cap3_all_exit_witness p B hlen hB
  exact ⟨t, ht⟩

/-- Every Boolean-accepted return certificate contains a state with at least
four exterior coefficients after maximal constant-suffix trimming. -/
theorem accepted_exceeds_three (cert : Certificate) (hc : check cert = true) :
    ∃ i, i < cert.P ∧ 3 < (stripSuffix (cert.st i).c (cert.st i).B).length :=
  accepted_exceeds_cap_unrestricted cert hc 3 boundedEscapeAt_three

/-- The actual certificate checker rejects every cyclic candidate confined to
normalized exterior cap three.  Empty certificates are covered as well. -/
theorem check_eq_false_of_normalized_cap_three (cert : Certificate)
    (hsmall : ∀ i, i < cert.P →
      (stripSuffix (cert.st i).c (cert.st i).B).length ≤ 3) : check cert = false := by
  cases hc : check cert with
  | false => rfl
  | true =>
    obtain ⟨i, hi, hlarge⟩ := accepted_exceeds_three cert hc
    have hle := hsmall i hi
    omega

/-- In particular, an input search restricted to raw exterior length at most
three cannot produce an accepted certificate, irrespective of its gap data. -/
theorem check_eq_false_of_raw_cap_three (cert : Certificate)
    (hsmall : ∀ i, i < cert.P → (cert.st i).B.length ≤ 3) : check cert = false := by
  apply check_eq_false_of_normalized_cap_three cert
  intro i hi
  exact Nat.le_trans (stripSuffix_length_le _ _) (hsmall i hi)

end Agent116.CertificateExterior

#print axioms Agent116.CertificateExterior.boundedEscapeAt_three
#print axioms Agent116.CertificateExterior.accepted_exceeds_three
#print axioms Agent116.CertificateExterior.check_eq_false_of_normalized_cap_three
#print axioms Agent116.CertificateExterior.check_eq_false_of_raw_cap_three
