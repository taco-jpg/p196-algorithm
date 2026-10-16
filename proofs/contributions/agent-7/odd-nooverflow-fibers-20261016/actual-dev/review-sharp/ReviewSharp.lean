import OddSharp

namespace P196.Agent7.ReviewSharp

open P196.Agent9.InverseFibers
open P196.Agent7.OddFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

/-- Independent reduction of the canonical enumerator across one full phase. -/
theorem small_global_maxima :
    (List.range 7).map (fun m => (sharpFamily m).length) = [1,1,1,2,3,4,7] := by
  decide

/-- The excluded degenerate fixed-center case would not be an equality. -/
theorem zero_center_width_one_gap :
    fullOddPreimages [] 0 = [] ∧ oddCenterMax 0 0 = 1 := by
  decide

theorem positive_width_one_attainment :
    sharpFamily 0 = [[6]] ∧ Agent8.stepWord [6] = [12] := by
  decide

/-- Every prescribed center at the first positive half-width. -/
theorem first_fixed_center_counts : ∀ v : Fin 10,
    (fullOddPreimages [11] v).length = if v.val % 2 = 0 then 1 else 0 := by
  decide

/-- The ceiling has moved to the odd centers at half-width three. -/
theorem third_fixed_center_counts : ∀ v : Fin 10,
    (fullOddPreimages [11,9,9] v).length = if v.val % 2 = 0 then 1 else 2 := by
  decide

/-- The ceiling has returned to the even centers at half-width six. -/
theorem sixth_fixed_center_counts : ∀ v : Fin 10,
    (fullOddPreimages [11,9,9,9,9,9] v).length = if v.val % 2 = 0 then 7 else 6 := by
  decide

#print axioms small_global_maxima
#print axioms zero_center_width_one_gap
#print axioms positive_width_one_attainment
#print axioms first_fixed_center_counts
#print axioms third_fixed_center_counts
#print axioms sixth_fixed_center_counts

end P196.Agent7.ReviewSharp
