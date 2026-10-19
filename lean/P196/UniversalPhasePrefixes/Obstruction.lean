import P196.UniversalPhasePrefixes.Extension

/-!
# Limits of phase recovery from finite observations

The universal-phase extension supplies one valid word compatible with
every nonneutral phase at a fixed finite observation. Consequently, no
individual finite observation certifies the phase among unrestricted valid
words, even when the actual outgoing high carry is supplied.

The same pointwise obstruction rules out every phase decoder that receives
that carry and the two literal finite streams. The decoder may be chosen
separately for each cutoff.
-/

namespace Agent5.UniversalPhasePrefixes

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- At every valid target, the actual high carry and two finite observed
prefixes fail to force the phase of all compatible valid states. -/
theorem no_finite_phase_certificate (c cut : Nat) (B : List Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    ¬ (∀ (d : Nat) (A : List Nat),
      nonneutralPhase d →
      validOuter { c := d, B := A } = true →
      (normalize A.reverse (if 10 ≤ d then 1 else 0)).2 =
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 →
      adicNumeratorDigits cut (zValue d A - (d : Int)) =
        adicNumeratorDigits cut (zValue c B - (c : Int)) →
      fractionDigits cut (rhoNum d A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ d then 1 else 0)).2) =
        fractionDigits cut (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) →
      d = c) := by
  intro hcertificate
  obtain ⟨A, _, hA⟩ :=
    arbitrarily_wide_all_phase_same_prefixes c cut 0 B hc hv
  have hc2 : nonneutralPhase 2 := by simp [nonneutralPhase]
  have hc4 : nonneutralPhase 4 := by simp [nonneutralPhase]
  obtain ⟨hv2, _, hcarry2, hlo2, hhi2⟩ := hA 2 hc2
  obtain ⟨hv4, _, hcarry4, hlo4, hhi4⟩ := hA 4 hc4
  have h2 : 2 = c := hcertificate 2 A hc2 hv2 hcarry2 hlo2 hhi2
  have h4 : 4 = c := hcertificate 4 A hc4 hv4 hcarry4 hlo4 hhi4
  omega

/-- No decoder selected for a fixed cutoff can recover the nonneutral
phase of every valid state from its actual high carry and two original
finite stream observations. -/
theorem no_finite_phase_decoder (cut : Nat) :
    ¬ ∃ D : Nat → List Nat → List Nat → Nat,
      ∀ (c : Nat) (B : List Nat),
        nonneutralPhase c →
        validOuter { c := c, B := B } = true →
        D (normalize B.reverse (if 10 ≤ c then 1 else 0)).2
            (adicNumeratorDigits cut (zValue c B - (c : Int)))
            (fractionDigits cut (rhoNum c B)
              (9 * 10 ^ B.length *
                10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) = c := by
  rintro ⟨D, hD⟩
  have hc2 : nonneutralPhase 2 := by simp [nonneutralPhase]
  have hempty : validOuter { c := 2, B := [] } = true := by
    simp [validOuter]
  apply no_finite_phase_certificate 2 cut [] hc2 hempty
  intro d A hd hv hcarry hlo hhi
  have hdecoded := hD d A hd hv
  rw [hlo, hhi, hcarry] at hdecoded
  have hzero := hD 2 [] hc2 hempty
  exact hdecoded.symm.trans hzero

#print axioms no_finite_phase_certificate
#print axioms no_finite_phase_decoder

end Agent5.UniversalPhasePrefixes
