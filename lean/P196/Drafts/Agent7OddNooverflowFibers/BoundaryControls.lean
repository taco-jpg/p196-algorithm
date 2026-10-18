import P196.Drafts.Agent7OddNooverflowFibers.OddCountsPhase

open P196.Agent9.InverseFibers
open P196.Agent7.OddFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

namespace P196.Agent7.OddFibers.ExtensionReview

-- Every prescribed center at the empty-half boundary is covered.
theorem zero_width_counts : ∀ v : Fin 10,
    (oddPreimages [] v 0).length = if v.val % 2 = 0 then 1 else 0 := by
  decide

-- In particular the explicitly selected empty-half witness is positive.
theorem empty_sharp_source :
    oddPreimages [] (sharpCenter 0) 0 = [([], 6)] ∧ Center 6 0 6 := by
  decide

-- A zero fixed-center maximum really can occur at a positive half-width.
theorem zero_maximum_at_width_one :
    oddCenterMax 1 7 = 0 ∧ oddPreimages [11] 7 0 = [] := by
  decide

-- Direct reduction checks both complete cycles, including ties at 2 and 5.
theorem endpoint_two_cycles :
    (List.range 12).map (fun m => (oddEndpoint 6 (nineRun m), oddEndpoint 7 (nineRun m))) =
      [(1,0), (1,0), (1,1), (1,2), (2,3), (4,4),
       (7,6), (11,10), (17,17), (27,28), (44,45), (72,72)] := by
  decide

theorem selected_center_two_cycles :
    (List.range 12).map (fun m => (sharpCenter m).val) =
      [6,6,6,7,7,7,6,6,6,7,7,7] := by
  decide

#print axioms zero_width_counts
#print axioms empty_sharp_source
#print axioms zero_maximum_at_width_one
#print axioms endpoint_two_cycles
#print axioms selected_center_two_cycles

end P196.Agent7.OddFibers.ExtensionReview
