import P196.Drafts.Agent34Sessionc91cAgent34Sessionc91c.RhoCycleTargets

/-!
Agent #115 experimental proof attempt on unchanged OuterFinite.outerNext.
Only declarations that actually compile under pinned Lean 4.19 with --trust=0 plus
an axiom audit may be labeled LEAN-CHECKED; no central 196 result is claimed.
-/
namespace Agent115.RhoCycle

open P196.Agent7.Finite Agent115.ExteriorFactorization Agent6.ExteriorCoordinates

/-- Equality with the original right-side decimal normalization carry. -/
theorem gamma_eq_overflow (s : Outer) :
    gamma s = overflow s.c s.B := by
  change (highValue s.B + phaseCarry s.c) / 10 ^ s.B.length = overflow s.c s.B
  exact (overflow_eq_highValue s.c s.B).symm

/-- A bounded pair word has no high carry greater than one. -/
theorem gamma_le_one (s : Outer)
    (hB : ∀ x ∈ s.B, x ≤ 18) : gamma s ≤ 1 := by
  rw [gamma_eq_overflow]
  exact overflow_le_one s.c s.B hB

/-- Strictly positive gain numerator without any coefficient or width bound. -/
theorem psiNumerator_pos_of_phase_pos (s : Outer) (hc : 0 < s.c) :
    0 < psiNumerator s := by
  have ht := phaseDigit_pos s.c hc
  change 0 < s.c - 9 * (if 10 ≤ s.c then 1 else 0) at ht
  unfold psiNumerator
  dsimp only
  omega

/-- Both rational coordinate denominators are strictly positive. -/
theorem rhoDenominator_pos (s : Outer) : 0 < rhoDenominator s := by
  unfold rhoDenominator
  exact Nat.mul_pos (by decide) (Nat.pow_pos (by decide))

theorem psiDenominator_pos (s : Outer) : 0 < psiDenominator s := by
  unfold psiDenominator
  exact Nat.mul_pos (by decide) (Nat.pow_pos (by decide))

#print axioms gamma_eq_overflow
#print axioms gamma_le_one
#print axioms psiNumerator_pos_of_phase_pos
#print axioms rhoDenominator_pos
#print axioms psiDenominator_pos

end Agent115.RhoCycle
