import GuardPreservationCounterexample

namespace Agent222M99B222

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196 SevenStepOrbit

/-- The actual seven-step pair-word return has width 14 and the exact
    returned word reported in the computational witness. -/
theorem witness_returned_state :
    (iterPairs witnessQ 11 7).1 = 14 ∧
    (∀ i, i < 14 →
      (iterPairs witnessQ 11 7).2 i =
        match i with
        | 0 => 3
        | 1 => 5
        | 2 => 9
        | 3 => 15
        | 4 => 15
        | 5 => 9
        | 6 => 5
        | 7 => 3
        | 8 => 5
        | 9 => 9
        | 10 => 15
        | 11 => 15
        | 12 => 9
        | 13 => 5
        | _ => 0) := by
  constructor
  · decide
  · intro i hi
    interval_cases i <;> decide

/-- The returned interface is not merely a symbolic transducer state:
    it is the concrete actual-orbit state whose next guard fails. -/
theorem witness_returned_width :
    (iterPairs witnessQ 11 7).1 = 14 := by
  exact witness_returned_state.1

#print axioms witness_returned_state
#print axioms witness_returned_width

end Agent222M99B222
