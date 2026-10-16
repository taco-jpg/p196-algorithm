import ExteriorNormalization
import CertificateRealization

/-!
Agent #121: review-only interface compositions for Agent #116 checkpoint 01.
These keep the concrete certificate checker and admissibility hypotheses.
No valid certificate instance, global exterior exclusion or Lychrel witness.
-/
namespace Agent121.Review116
open Agent109 Agent109.Cert
open P196.Agent7.Finite (Outer outerNext stripSuffix)

/-- Exact type contract of the new partial-trim theorem. -/
theorem partial_trim_contract (c c' : Nat) (B B' A C : Word) (j : Nat)
    (hc : Phase c) (hB : Bounded B) (hc' : c' = tOf c + tOf c)
    (htrim : Br c B A C = B' ++ List.replicate j c') :
    outerNext ⟨c, stripSuffix c B⟩ = ⟨c', stripSuffix c' B'⟩ :=
  Agent116.Exterior.outerNext_of_partial_trim c c' B B' A C j hc hB hc' htrim

/-- The positivity result really accepts the existing Boolean checker interface. -/
theorem checked_admissible_head_contract (cert : Certificate)
    (hcheck : check cert = true) (H M : Word) (hadm : Admissible0 cert H M) :
    ∀ i, i < cert.P → ∀ b bs, (cert.st i).B = b :: bs → 0 < b :=
  Agent116.CertificateExterior.admissible_heads_positive cert (check_sound cert hcheck) H M hadm

/-- Review projection; maximal normalization of the certificate exterior. -/
def canonicalOuter (cert : Certificate) (i : Nat) : Outer :=
  ⟨(cert.st i).c, stripSuffix (cert.st i).c (cert.st i).B⟩

/-- An interface test: LocalOK's actual equations supply every partial-trim premise.
This is conditional on the unchanged Boolean checker; it does not supply a certificate.
-/
theorem certificate_step_interface (cert : Certificate) (hcheck : check cert = true)
    (i : Nat) (hi : i < cert.P) :
    outerNext (canonicalOuter cert i) = canonicalOuter cert ((i + 1) % cert.P) := by
  have hv := check_sound cert hcheck
  obtain ⟨hc, hB, _, _, hc', hBr, _, _, _, _, _, _, _⟩ := hv.2 i hi
  exact Agent116.Exterior.outerNext_of_partial_trim _ _ _ _ _ _ (cert.lk i).j
    hc hB hc'.symm hBr

end Agent121.Review116

#print axioms Agent121.Review116.partial_trim_contract
#print axioms Agent121.Review116.checked_admissible_head_contract
#print axioms Agent121.Review116.certificate_step_interface
