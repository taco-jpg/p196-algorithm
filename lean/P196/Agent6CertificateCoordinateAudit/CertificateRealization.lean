import P196.Agent6CertificateCoordinateAudit.OuterBridge

/-!
Necessary exterior complexity for finite complementary-band return certificates.
The first-state admissibility hypothesis is retained explicitly: the Boolean
certificate checker alone does not enforce a positive canonical exterior.
-/

namespace Agent116.CertificateExterior

open Agent109 Agent109.Cert Agent109.Outer P196.Agent7.Finite

set_option maxHeartbeats 0

/-- An ordinary realization of a certificate state, above its gap bounds. -/
def Realizes (cert : Certificate) (i : Nat) : Prop :=
  ∃ n G H,
    pairWord n = template (cert.st i).c (cert.st i).B
      (cert.st i).A (cert.st i).C G H ∧
    (cert.lk i).lo ≤ G ∧ (cert.lk i).lo' ≤ H

/-- Realizations propagate along the exact checked template transition. -/
theorem realizes_next (cert : Certificate) (hv : Valid cert) (i : Nat)
    (hi : i < cert.P) (hr : Realizes cert i) :
    Realizes cert ((i + 1) % cert.P) := by
  obtain ⟨n, G, H, hn, hG, hH⟩ := hr
  obtain ⟨hc, hB, hA, hC, hc', hBr, hAr, hCr, _, h2, h2', hlo, hlo'⟩ := hv.2 i hi
  obtain ⟨g, rfl⟩ : ∃ g, G = g + 2 := ⟨G - 2, by omega⟩
  obtain ⟨h, rfl⟩ : ∃ h, H = h + 2 := ⟨H - 2, by omega⟩
  have hs := actual_template_step n _ _ _ _ g h hc hB hA hC hn
  rw [hc', hBr, hAr, hCr, template_trim] at hs
  refine ⟨step n, _, _, hs, ?_, ?_⟩
  · unfold gam at hlo; omega
  · unfold gam at hlo'; omega

/-- A realization at the first state supplies one at every listed state. -/
theorem realizes_all (cert : Certificate) (hv : Valid cert)
    (hzero : Realizes cert 0) : ∀ i, i < cert.P → Realizes cert i := by
  intro i
  induction i with
  | zero => intro _; exact hzero
  | succ i ih =>
    intro hi
    have hn := realizes_next cert hv i (by omega) (ih (by omega))
    simpa only [Nat.mod_eq_of_lt hi] using hn

/-- Initial admissibility is sufficient for actual integer realization. -/
theorem admissible_realizes_zero (cert : Certificate) (hv : Valid cert)
    (H M : Word) (hadm : Admissible0 cert H M) : Realizes cert 0 := by
  obtain ⟨hCe, hM, hev, hB0⟩ := hadm
  obtain ⟨hc, hB, hA, hC, _, _, _, _, _, h2, _, _, _⟩ := hv.2 0 hv.1
  have hCm : Mirr (cert.st 0).C := by
    rw [hCe]
    exact mirr_of_split H M hM hev
  obtain ⟨n, hn⟩ := template_realized _ _ _ _ (cert.lk 0).lo (cert.lk 0).lo'
    hc (by omega) hB hA hC hCm hB0
  exact ⟨n, _, _, hn, Nat.le_refl _, Nat.le_refl _⟩

/-- The exterior of an actual template has a positive first coefficient,
whenever it is nonempty. This follows from canonical integer digits. -/
theorem realized_head_positive (n c : Nat) (B A C : Word) (G H : Nat)
    (hn : pairWord n = template c B A C G H) :
    ∀ b bs, B = b :: bs → 0 < b := by
  intro b bs hb
  have hl := lastPos_pairWord n
  apply hl b
  rw [hn]
  simp only [template, List.getLast?_append, List.getLast?_reverse, hb,
    List.head?_cons, Option.some_or]

/-- Every state of an admissible accepted certificate has a positive exterior.
No positivity assumption is silently added to `check`. -/
theorem admissible_heads_positive (cert : Certificate) (hv : Valid cert)
    (H M : Word) (hadm : Admissible0 cert H M) :
    ∀ i, i < cert.P → ∀ b bs, (cert.st i).B = b :: bs → 0 < b := by
  intro i hi
  obtain ⟨n, G, K, hn, _, _⟩ :=
    realizes_all cert hv (admissible_realizes_zero cert hv H M hadm) i hi
  exact realized_head_positive n _ _ _ _ G K hn

end Agent116.CertificateExterior

#print axioms Agent116.CertificateExterior.realizes_next
#print axioms Agent116.CertificateExterior.realizes_all
#print axioms Agent116.CertificateExterior.admissible_realizes_zero
#print axioms Agent116.CertificateExterior.realized_head_positive
#print axioms Agent116.CertificateExterior.admissible_heads_positive
