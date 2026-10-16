import Agent1PeriodicValidity

/-!
Finite boundary witnesses for the exact periodic quotient. Every computational
proof below uses kernel reduction. They are not an infinite-orbit argument.
-/
namespace Agent1.Periodic.SafetyBoundary
open Agent8 Agent1.Periodic

def tens : Word := [10,10,10,10]

/-- Both stored remainders may be empty in the original validity domain. -/
theorem tens_valid : ValidPeriodic [] [] tens := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp [Bounded, tens]

/-- Literal exponent-three normalization, including the carried leading digit. -/
theorem tens_normalize :
    normalize (periodicWord [] [] tens 3) 0 = 0 :: List.replicate 24 1 := by
  rfl

/-- The exact raw guard, rather than a guessed transition or displaced center. -/
theorem tens_raw :
    rawOuter [] [] tens = [1,2,2,2] ∧
    rawCenter [] [] tens = List.replicate 9 2 ∧
    rawPeriod [] [] tens = [2,2,2,2] ∧ rawGamma [] [] tens = 1 := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/-- The actual maximal center strip removes one complete mirrored period. -/
theorem tens_quotient :
    quotientOuter [] [] tens = [1,2,2,2] ∧
    quotientCenter [] [] tens = [2] ∧
    outerPeriods [] [] tens = 0 ∧ centerPeriods [] [] tens = 1 := by
  exact ⟨rfl, rfl, rfl, rfl⟩

end Agent1.Periodic.SafetyBoundary
#print axioms Agent1.Periodic.SafetyBoundary.tens_valid
#print axioms Agent1.Periodic.SafetyBoundary.tens_normalize
#print axioms Agent1.Periodic.SafetyBoundary.tens_raw
#print axioms Agent1.Periodic.SafetyBoundary.tens_quotient
