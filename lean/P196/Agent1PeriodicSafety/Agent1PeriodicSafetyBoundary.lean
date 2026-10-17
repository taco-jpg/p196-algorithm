import P196.Agent1PeriodicSafety.Agent1PeriodicSafety

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

/-- The original safe input flag can become false at its exact successor. -/
theorem tens_safe_source : safePeriodic [] [] tens = true := by decide

theorem tens_unsafe_quotient :
    safePeriodic (quotientOuter [] [] tens) (quotientCenter [] [] tens)
      (rawPeriod [] [] tens) = false := by decide

/-- Validity and safety do not imply safety of the exact quotient transition. -/
theorem safe_valid_transition_counterexample :
    ∃ B H w : Word, ValidPeriodic B H w ∧ safePeriodic B H w = true ∧
      safePeriodic (quotientOuter B H w) (quotientCenter B H w)
        (rawPeriod B H w) = false :=
  ⟨[], [], tens, tens_valid, tens_safe_source, tens_unsafe_quotient⟩

/-- At exponent zero, the stored period alphabet is absent from the word;
the positive-exponent premise in the universal safety theorem is necessary. -/
theorem zero_exponent_counterexample :
    ValidPeriodic [1] [] [18,18,18,18] ∧
      safePeriodic [1] [] [18,18,18,18] = true ∧
      FoldedDecimal.BadWord (periodicWord [1] [] [18,18,18,18] 0).length
        (fun i => ((periodicWord [1] [] [18,18,18,18] 0)[i]?).getD 0) := by
  refine ⟨?_, by decide, Or.inl ?_⟩
  · refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp [Bounded]
  · intro i hi
    have hi2 : i < 2 := hi
    have : i = 0 ∨ i = 1 := by omega
    rcases this with rfl | rfl <;> decide

end Agent1.Periodic.SafetyBoundary
#print axioms Agent1.Periodic.SafetyBoundary.tens_valid
#print axioms Agent1.Periodic.SafetyBoundary.tens_normalize
#print axioms Agent1.Periodic.SafetyBoundary.tens_raw
#print axioms Agent1.Periodic.SafetyBoundary.tens_quotient

#print axioms Agent1.Periodic.SafetyBoundary.tens_safe_source
#print axioms Agent1.Periodic.SafetyBoundary.tens_unsafe_quotient
#print axioms Agent1.Periodic.SafetyBoundary.safe_valid_transition_counterexample
#print axioms Agent1.Periodic.SafetyBoundary.zero_exponent_counterexample
