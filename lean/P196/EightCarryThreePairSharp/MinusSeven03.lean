import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 32 through 47.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven_03 :
    covered (extensions 0 7 12 ((quintuples.drop 32).take 16)) minusSevenSextuples = true := by
  apply extensions_cover_of_upper_fin 0 7 12 13 (by decide)
  intro p hp
  change p ∈ [
    ([14, 7, 13, 5, 18], [14, 7, 12, 8, 13]),
    ([14, 7, 13, 14, 18], [14, 7, 12, 17, 13]),
    ([14, 16, 4, 5, 9], [14, 16, 3, 8, 4]),
    ([14, 16, 4, 5, 18], [14, 16, 3, 8, 13]),
    ([14, 16, 4, 14, 18], [14, 16, 3, 17, 13]),
    ([14, 16, 13, 5, 9], [14, 16, 12, 8, 4]),
    ([14, 16, 13, 5, 18], [14, 16, 12, 8, 13]),
    ([14, 16, 13, 14, 18], [14, 16, 12, 17, 13]),
    ([17, 2, 1, 1, 7], [17, 2, 0, 4, 2]),
    ([17, 2, 1, 1, 8], [17, 2, 0, 4, 3]),
    ([17, 2, 1, 1, 16], [17, 2, 0, 4, 11]),
    ([17, 2, 1, 1, 17], [17, 2, 0, 4, 12]),
    ([17, 2, 1, 5, 9], [17, 2, 0, 8, 4]),
    ([17, 2, 1, 5, 18], [17, 2, 0, 8, 13]),
    ([17, 2, 1, 10, 7], [17, 2, 0, 13, 2]),
    ([17, 2, 1, 10, 8], [17, 2, 0, 13, 3])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_minus_seven_03

end EightCarryThreePairSharp.Candidates
