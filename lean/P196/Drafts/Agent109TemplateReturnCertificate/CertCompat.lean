import P196.Agent2SaturatedProfile.ReturnCertificate
import P196.Agent101ProtectedFamily.Compat

/-!
Agent #109: return-certificate soundness restated for the accepted
`Lychrel196` semantics of `LychrelDigitSums.lean`. Conditional only: no
certificate instance is known or claimed.
-/

namespace Agent109.CertCompat

open Agent109 Agent109.Cert

theorem certificate_isLychrel (cert : Certificate) (hc : check cert = true) (n G H : Nat)
    (hn : pairWord n = template (cert.st 0).c (cert.st 0).B (cert.st 0).A (cert.st 0).C G H)
    (hG : (cert.lk 0).lo ≤ G) (hH : (cert.lk 0).lo' ≤ H) :
    Lychrel196.IsLychrel (Lychrel196.step n) := by
  intro k
  rw [Compat.palindrome_eq, Compat.orbit_eq, Compat.step_eq]
  exact certificate_sound cert hc n G H hn hG hH k

theorem certificate_existence_lychrel (cert : Certificate) (hc : check cert = true)
    (H M : Word) (hadm : decide (Admissible0 cert H M) = true) :
    Lychrel196.DecimalLychrelExistence := by
  obtain ⟨m, hm⟩ := certificate_existence cert hc H M hadm
  exact ⟨m, fun k => by rw [Compat.palindrome_eq, Compat.orbit_eq]; exact hm k⟩

end Agent109.CertCompat

#print axioms Agent109.CertCompat.certificate_isLychrel
#print axioms Agent109.CertCompat.certificate_existence_lychrel
