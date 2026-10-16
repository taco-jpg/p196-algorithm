import GuardPreservationCounterexample

/-!
The exact returned pair state after the first guarded seven-step return.

Correction: an earlier draft listed a non-symmetric word
(4,0,0,5,5,14,10,14,10,14,5,5,0,4), which is not the pair-sum word of any
integer. The actual seventh iterate 14002278733003 has mirrored pair sums
(4,4,0,3,5,9,15,15,9,5,3,0,4,4): prefix (4,4,0) is restored, and the middle
is Agent #12's returned middle (3,5,9,15,15,9,5,3).
-/

namespace Agent222M99B222

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196 SevenStepOrbit

/-- The actual seven-step pair-word return has width 14 and the exact
    symmetric pair-sum word of the seventh iterate 14002278733003. -/
theorem witness_returned_state :
    (iterPairs witnessQ 11 7).1 = 14 ∧
    (List.range 14).map (iterPairs witnessQ 11 7).2 =
      [4, 4, 0, 3, 5, 9, 15, 15, 9, 5, 3, 0, 4, 4] := by
  decide

theorem witness_returned_width :
    (iterPairs witnessQ 11 7).1 = 14 :=
  witness_returned_state.1

#print axioms witness_returned_state
#print axioms witness_returned_width

end Agent222M99B222
