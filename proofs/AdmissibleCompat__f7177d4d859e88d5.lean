import AdmissibleHeads
import CertCompat

/-!
Agent #112: full automatic-admissibility endpoint using the repository's
original decimal reverse-and-add definitions. Conditional on a successful
finite certificate check, not a certificate instance and not a P196 theorem.
-/
namespace Agent112.Admissibility
open Agent109 Agent109.Cert

/-- Every listed state of a valid cyclic certificate is realized by an ordinary
integer at every positive first-band length and every second-band length. -/
theorem valid_state_realized (cert : Certificate) (hv : Valid cert)
    (i : Nat) (hi : i < cert.P) (G H : Nat) (hG : 0 < G) :
    ∃ n, pairWord n = template (cert.st i).c (cert.st i).B (cert.st i).A (cert.st i).C G H := by
  obtain ⟨hc, hB, hA, hC, _⟩ := hv.2 i hi
  exact template_realized _ _ _ _ G H hc hG hB hA hC
    (valid_center_mirr cert hv i hi) (valid_headPos cert hv i hi)

/-- A checked certificate alone suffices for the original ordinary-decimal
existence proposition. The finite certificate itself remains to be found. -/
theorem checked_certificate_decimal_existence (cert : Certificate)
    (hc : check cert = true) : Lychrel196.DecimalLychrelExistence := by
  obtain ⟨H, M, ha⟩ := automatic_admissibility cert hc
  exact Agent109.CertCompat.certificate_existence_lychrel cert hc H M (by simpa using ha)

/-- The resulting ordinary seed is strictly positive; zero is not smuggled
into the existential conclusion. This is still conditional on a checked certificate. -/
theorem checked_positive_decimal_seed (cert : Certificate) (hc : check cert = true) :
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m := by
  obtain ⟨m, hm⟩ := checked_certificate_decimal_existence cert hc
  refine ⟨m, ?_, hm⟩
  cases m with
  | zero => exact False.elim (hm 0 rfl)
  | succ m => exact Nat.zero_lt_succ m

end Agent112.Admissibility
#print axioms Agent112.Admissibility.valid_state_realized
#print axioms Agent112.Admissibility.checked_certificate_decimal_existence

#print axioms Agent112.Admissibility.checked_positive_decimal_seed
