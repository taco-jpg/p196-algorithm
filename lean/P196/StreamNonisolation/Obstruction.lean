import P196.StreamNonisolation.Extension

/-!
# Limits of recovery from a fixed finite observation

Arbitrarily wide valid extensions rule out a decoder that is correct for
every valid exterior word at one fixed phase and cutoff. The decoder may
be chosen knowing both parameters.

At each individual valid word, the same observations also fail to certify
any finite upper bound on canonical width. This pointwise obstruction
persists when the actual outgoing high carry is supplied as additional
information.
-/

namespace Agent5.StreamNonisolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Even with the phase and cutoff fixed in advance, no function of the two
literal finite streams recovers every original valid exterior state. -/
theorem no_finite_stream_decoder (c cut : Nat)
    (hc : nonneutralPhase c) :
    ¬ ∃ D : List Nat → List Nat → Outer,
      ∀ B : List Nat,
        validOuter { c := c, B := B } = true →
        D (adicNumeratorDigits cut (zValue c B - (c : Int)))
            (fractionDigits cut (rhoNum c B)
              (9 * 10 ^ B.length *
                10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) =
          { c := c, B := B } := by
  rintro ⟨D, hD⟩
  have hempty : validOuter { c := c, B := [] } = true := by
    simp [validOuter]
  obtain ⟨A, hA, _, hwidth, _, hlo, hhi⟩ :=
    arbitrarily_wide_valid_same_prefixes c cut 0 [] hc hempty
  have hzero := hD [] hempty
  have hdecoded := hD A hA
  rw [hlo, hhi] at hdecoded
  have hword : A = [] := congrArg Outer.B (hdecoded.symm.trans hzero)
  simp [hword] at hwidth

/-- For every valid starting word and proposed upper bound, another valid
word has the same phase, actual high carry, and finite streams but exceeds
that bound after maximal phase-suffix removal. Thus these observations
cannot certify any finite upper bound on canonical width. -/
theorem no_finite_core_width_certificate (c cut N : Nat) (B : List Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    ¬ (∀ A : List Nat,
      validOuter { c := c, B := A } = true →
      (normalize A.reverse (if 10 ≤ c then 1 else 0)).2 =
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 →
      adicNumeratorDigits cut (zValue c A - (c : Int)) =
        adicNumeratorDigits cut (zValue c B - (c : Int)) →
      fractionDigits cut (rhoNum c A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits cut (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) →
      (stripSuffix c A).length ≤ N) := by
  intro hbound
  obtain ⟨A, hA, hcanonical, hwidth, hcarry, hlo, hhi⟩ :=
    arbitrarily_wide_valid_same_prefixes c cut N B hc hv
  have hN := hbound A hA hcarry hlo hhi
  rw [hcanonical] at hN
  have hmax := Nat.le_max_right B.length N
  omega

#print axioms no_finite_stream_decoder
#print axioms no_finite_core_width_certificate

end Agent5.StreamNonisolation
