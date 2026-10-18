import P196.Drafts.Agent112CertificateAdmissibility.AdmissibleCompat
import P196.Drafts.Agent112EventualRealizability.EventualCompat

namespace Agent21.M99A01

/-- M99-A01 exact conditional certificate-to-positive-seed interface.
This does not instantiate a certificate. -/
theorem checked_certificate_positive_seed (cert : Agent109.Cert.Certificate)
    (hc : Agent109.Cert.check cert = true) :
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m := by
  exact Agent112.Admissibility.checked_positive_decimal_seed cert hc

/-- M99-A01 exact finite-word-to-ordinary-orbit interface.
No concrete safe word or certificate instance is supplied. -/
theorem arbitrary_word_eventual_realization (w : Agent109.Word)
    (hp : 0 < Agent109.evalL w) :
    ∃ t n, 1 ≤ t ∧ 0 < n ∧
      ∀ k, Agent109.pairWord (Lychrel196.orbit n k) =
        Agent8.orbit w (t + k) := by
  exact Agent112.Eventual.original_arbitrary_eventual_realization w hp

end Agent21.M99A01
