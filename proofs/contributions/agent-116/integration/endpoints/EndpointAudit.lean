import Agent116All

/-! Exact endpoint type audit. Dependencies are reused only from the separately
recorded independent fresh 137-module build; Agent116All is recompiled here. -/
namespace Agent116.IntegrationEndpoints
open Agent109 Agent109.Cert Agent109.Outer P196.Agent7.Finite

 theorem accepted_exterior_gt_three
    (cert : Certificate) (hc : check cert = true) :
    ∃ i, i < cert.P ∧ 3 < (stripSuffix (cert.st i).c (cert.st i).B).length :=
  Agent116.CertificateExterior.accepted_exceeds_three cert hc

 theorem reject_normalized_cap_three
    (cert : Certificate)
    (hsmall : ∀ i, i < cert.P →
      (stripSuffix (cert.st i).c (cert.st i).B).length ≤ 3) :
    check cert = false :=
  Agent116.CertificateExterior.check_eq_false_of_normalized_cap_three cert hsmall

 theorem reject_raw_cap_three
    (cert : Certificate)
    (hsmall : ∀ i, i < cert.P → (cert.st i).B.length ≤ 3) :
    check cert = false :=
  Agent116.CertificateExterior.check_eq_false_of_raw_cap_three cert hsmall

 theorem actual_orbit_exact_scope
    (n : Nat) (p : Fin 8) (B A C : Word) (g h : Nat)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hlen : B.length ≤ 3)
    (hvalid : validOuter ⟨2 * (p.val + 1), B⟩ = true)
    (hg : 18 ≤ g) (hh : 18 ≤ h)
    (hn : pairWord n = Agent8.template (2 * (p.val + 1)) B A C g h) :
    ∃ i, i ≤ 9 ∧ ∃ c' B' A' C' G H, 3 < B'.length ∧
      B' = (outerIterate i ⟨2 * (p.val + 1), B⟩).B ∧
      pairWord (Lychrel196.orbit n i) = Agent8.template c' B' A' C' G H :=
  Agent116.ActualCap3.lychrel_cap3_exit n p B A C g h hB hA hC hlen hvalid hg hh hn

 theorem valid_outer_exit_nine (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 3) (hdigit : ∀ x ∈ B, x ≤ 18)
    (hvalid : validOuter {c := 2 * (p.val + 1), B := B} = true) :
    ∃ i, i ≤ 9 ∧
      3 < (outerIterate i {c := 2 * (p.val + 1), B := B}).B.length :=
  P196.Agent116.Cap3.cap3_exit_witness p B hlen hdigit hvalid

 theorem unrestricted_outer_exit_ten (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 3) (hdigit : ∀ x ∈ B, x ≤ 18) :
    ∃ i, i ≤ 10 ∧
      3 < (outerIterate i {c := 2 * (p.val + 1), B := B}).B.length :=
  P196.Agent116.Cap3.cap3_all_exit_witness p B hlen hdigit

 theorem complete_three_digit_encoding (B : List Nat)
    (hlen : B.length ≤ 3) (hdigit : ∀ x ∈ B, x ≤ 18) :
    ∃ k : Fin 7240, P196.Agent116.Cap3.decodeWord3 k.val = B :=
  P196.Agent116.Cap3.decode_complete B hlen hdigit

 theorem exact_valid_first_exit :
    (∀ i, i ≤ 8 → (outerIterate i {c := 8, B := [11, 9]}).B.length ≤ 3) ∧
      3 < (outerIterate 9 {c := 8, B := [11, 9]}).B.length :=
  P196.Agent116.Cap3.cap3_sharp_first_exit

 theorem exact_unrestricted_first_exit :
    (∀ i, i ≤ 9 → (outerIterate i {c := 6, B := [0]}).B.length ≤ 3) ∧
      3 < (outerIterate 10 {c := 6, B := [0]}).B.length :=
  P196.Agent116.Cap3.cap3_all_sharp_first_exit

end Agent116.IntegrationEndpoints

#print axioms Agent116.CertificateExterior.accepted_exceeds_three
#print axioms Agent116.CertificateExterior.check_eq_false_of_normalized_cap_three
#print axioms Agent116.CertificateExterior.check_eq_false_of_raw_cap_three
#print axioms Agent116.ActualCap3.lychrel_cap3_exit

#check Agent116.IntegrationEndpoints.accepted_exterior_gt_three
#print axioms Agent116.IntegrationEndpoints.accepted_exterior_gt_three

#check Agent116.IntegrationEndpoints.reject_normalized_cap_three
#print axioms Agent116.IntegrationEndpoints.reject_normalized_cap_three

#check Agent116.IntegrationEndpoints.reject_raw_cap_three
#print axioms Agent116.IntegrationEndpoints.reject_raw_cap_three

#check Agent116.IntegrationEndpoints.actual_orbit_exact_scope
#print axioms Agent116.IntegrationEndpoints.actual_orbit_exact_scope

#check Agent116.IntegrationEndpoints.valid_outer_exit_nine
#print axioms Agent116.IntegrationEndpoints.valid_outer_exit_nine

#check Agent116.IntegrationEndpoints.unrestricted_outer_exit_ten
#print axioms Agent116.IntegrationEndpoints.unrestricted_outer_exit_ten

#check Agent116.IntegrationEndpoints.complete_three_digit_encoding
#print axioms Agent116.IntegrationEndpoints.complete_three_digit_encoding

#check Agent116.IntegrationEndpoints.exact_valid_first_exit
#print axioms Agent116.IntegrationEndpoints.exact_valid_first_exit

#check Agent116.IntegrationEndpoints.exact_unrestricted_first_exit
#print axioms Agent116.IntegrationEndpoints.exact_unrestricted_first_exit
