import GuardPreservationCounterexample

namespace Agent222M99B222

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196 SevenStepOrbit

/-- The actual seven-step pair-word return has width 14 and the exact
    symmetric pair-sum word obtained from the reported seventh iterate. -/
theorem witness_returned_state :
    (iterPairs witnessQ 11 7).1 = 14 ∧
    (∀ i, i < 14 →
      (iterPairs witnessQ 11 7).2 i =
        match i with
        | 0 => 4
        | 1 => 0
        | 2 => 0
        | 3 => 5
        | 4 => 5
        | 5 => 14
        | 6 => 10
        | 7 => 14
        | 8 => 10
        | 9 => 14
        | 10 => 5
        | 11 => 5
        | 12 => 0
        | 13 => 4
        | _ => 0) := by
  constructor
  · decide
  · intro i hi
    interval_cases i <;> decide

theorem witness_returned_width :
    (iterPairs witnessQ 11 7).1 = 14 := by
  exact witness_returned_state.1

#print axioms witness_returned_state
#print axioms witness_returned_width

end Agent222M99B222
