import CertificateCoordinates

/-!
An executable necessary filter for the unchanged Agent109 return checker.

Every tested quantity uses the exact normalized listed rows from
`Agent116.CertificateExterior.stateOuter`. The filter checks signed-beta
cancellation and the occurrence of both signs. Passing this filter alone does
not establish a local transition, full certificate validity, or realization.
`filteredCheck_eq_check` proves that using it as a precheck preserves the
original Boolean checker's answer for every candidate, including period zero.
-/

namespace Agent6.CertificateFilter

open Agent109.Cert Agent6.CertificateCoordinates

/-- Finite, executable signed-coordinate conditions on normalized rows. -/
def coordinateFilter (cert : Certificate) : Bool :=
  decide (rowContributionSum cert = 0) &&
    (List.range cert.P).any (fun i => decide (0 < rowContribution cert i)) &&
    (List.range cert.P).any (fun i => decide (rowContribution cert i < 0))

/-- Exact proposition represented by the finite Boolean computation. -/
theorem coordinateFilter_eq_true_iff (cert : Certificate) :
    coordinateFilter cert = true ↔
      rowContributionSum cert = 0 ∧
      (∃ i, i < cert.P ∧ 0 < rowContribution cert i) ∧
      (∃ j, j < cert.P ∧ rowContribution cert j < 0) := by
  simp only [coordinateFilter, Bool.and_eq_true, decide_eq_true_eq,
    List.any_eq_true, List.mem_range]
  constructor
  · rintro ⟨⟨hz, hp⟩, hn⟩
    exact ⟨hz, hp, hn⟩
  · rintro ⟨hz, hp, hn⟩
    exact ⟨⟨hz, hp⟩, hn⟩

/-- Acceptance by the original full checker implies all filter conditions. -/
theorem checked_coordinateFilter (cert : Certificate) (hc : check cert = true) :
    coordinateFilter cert = true := by
  apply (coordinateFilter_eq_true_iff cert).2
  exact checked_coordinate_conditions cert hc

/-- A failing filter is a proved rejection by the original checker. -/
theorem check_eq_false_of_coordinateFilter_eq_false (cert : Certificate)
    (hf : coordinateFilter cert = false) : check cert = false := by
  cases hc : check cert with
  | false => rfl
  | true =>
    have ht := checked_coordinateFilter cert hc
    rw [hf] at ht
    cases ht

/-- A sign witness forces a positive listed period without any checker premise. -/
theorem period_pos_of_coordinateFilter (cert : Certificate)
    (hf : coordinateFilter cert = true) : 0 < cert.P := by
  obtain ⟨_, ⟨i, hi, _⟩, _⟩ := (coordinateFilter_eq_true_iff cert).1 hf
  omega

/-- Empty certificates fail the filter; a zero empty sum cannot pass alone. -/
theorem coordinateFilter_eq_false_of_period_zero (cert : Certificate)
    (hp : cert.P = 0) : coordinateFilter cert = false := by
  simp [coordinateFilter, hp]

/-- A candidate precheck using the new filter and the original checker. -/
def filteredCheck (cert : Certificate) : Bool :=
  coordinateFilter cert && check cert

/-- Adding the necessary filter preserves the original answer for every input. -/
theorem filteredCheck_eq_check (cert : Certificate) :
    filteredCheck cert = check cert := by
  cases hc : check cert with
  | false => simp [filteredCheck, hc]
  | true => simp [filteredCheck, hc, checked_coordinateFilter cert hc]

end Agent6.CertificateFilter

#print axioms Agent6.CertificateFilter.coordinateFilter_eq_true_iff
#print axioms Agent6.CertificateFilter.checked_coordinateFilter
#print axioms Agent6.CertificateFilter.check_eq_false_of_coordinateFilter_eq_false
#print axioms Agent6.CertificateFilter.period_pos_of_coordinateFilter
#print axioms Agent6.CertificateFilter.coordinateFilter_eq_false_of_period_zero
#print axioms Agent6.CertificateFilter.filteredCheck_eq_check
