import OddComplete

namespace P196.Agent7.ReviewComplete

open P196.Agent9.InverseFibers
open P196.Agent7.OddFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

/-- Exhaustive single-coefficient queries include valid, parity-invalid,
out-of-range, zero, and modulo-aliasing output values. -/
theorem width_one_queries : ∀ n : Fin 25,
    universalOddPreimages 0 [n.val] =
      if n.val % 4 = 0 ∧ 0 < n.val ∧ n.val < 20 then [[n.val / 2]] else [] := by
  decide

/-- The equality guard rejects short, long, asymmetric, odd-center and
out-of-alphabet targets rather than reducing them modulo the alphabets. -/
theorem invalid_target_queries :
    ([[], [1], [2,4], [2,4,2,0], [2,4,3], [21,4,21],
      [11,20,11], [11,1,11]] : List (List Nat)).map (universalOddPreimages 1) =
      List.replicate 8 [] := by
  decide

theorem empty_width_one_target : universalOddPreimages 0 [] = [] := by
  decide

/-- The source center 16, normalized digit 6 and target center 12 are distinct. -/
theorem three_column_explicit_fiber :
    universalOddPreimages 1 [11,12,11] = [[5,16,5]] := by
  decide

theorem three_column_literal_membership : CompleteOddFiber 1 [11,12,11] [5,16,5] := by
  simp [CompleteOddFiber, scan, Agent8.stepWord, Agent8.normalize,
    Agent8.pair, Agent8.zipAdd]

theorem zero_head_excluded :
    universalOddPreimages 1 [0,4,0] = [] ∧
      ¬ CompleteOddFiber 1 [0,4,0] [0,2,0] := by
  constructor
  · decide
  · simp [CompleteOddFiber]

/-- A control for the stronger output-range theorem, whose input need not
be symmetric or coefficient-bounded. -/
theorem unbounded_asymmetric_output_range_control :
    (scan [100,0,0] 0).2 = 0 ∧ Agent8.stepWord [100,0,0] = [1,0,1] := by
  decide

#print axioms width_one_queries
#print axioms invalid_target_queries
#print axioms empty_width_one_target
#print axioms three_column_explicit_fiber
#print axioms three_column_literal_membership
#print axioms zero_head_excluded
#print axioms unbounded_asymmetric_output_range_control

end P196.Agent7.ReviewComplete
