import P196.PhaseEighteenIsolation.Rigidity

/-!
# Recovering a bounded word from a low residue and its high value

The published upper-boundary rigidity theorem already contains the missing
modulo-nine argument. Applying it to whichever word reaches its width scale
leaves only the ordinary residue-injective case below that scale.
-/

namespace Agent5.CompleteExteriorFibers

open Agent115.ExteriorFactorization Agent5.ExactDigitStreams

/-- A bounded coefficient word is determined at a shared width by its low
value modulo the width scale and its exact high positional value. -/
theorem eq_of_low_residue_highValue (A B : List Nat)
    (hlen : A.length = B.length)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlow : lowValue A % 10 ^ B.length = lowValue B % 10 ^ B.length)
    (hhigh : highValue A = highValue B) : A = B := by
  by_cases hlargeB : 10 ^ B.length ≤ lowValue B
  · exact (Agent5.PhaseEighteenIsolation.boundary_values_rigidity
      A B 2 hlen hA hB hlargeB hlow
      (congrArg (fun x => x + 2) hhigh) (by decide)).1
  by_cases hlargeA : 10 ^ A.length ≤ lowValue A
  · have hswap : lowValue B % 10 ^ A.length = lowValue A % 10 ^ A.length := by
      simpa only [hlen] using hlow.symm
    exact (Agent5.PhaseEighteenIsolation.boundary_values_rigidity
      B A 2 hlen.symm hB hA hlargeA hswap
      (congrArg (fun x => x + 2) hhigh.symm) (by decide)).1.symm
  have hsmallA : lowValue A < 10 ^ B.length := by
    rw [← hlen]
    omega
  have hsmallB : lowValue B < 10 ^ B.length := by omega
  rw [Nat.mod_eq_of_lt hsmallA, Nat.mod_eq_of_lt hsmallB] at hlow
  exact eq_of_values A B hlen hA hB hlow hhigh

#print axioms eq_of_low_residue_highValue

end Agent5.CompleteExteriorFibers
