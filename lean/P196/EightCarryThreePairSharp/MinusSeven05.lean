import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 64 through 79.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven_05 :
    covered (extensions 0 7 12 ((quintuples.drop 64).take 16)) minusSevenSextuples = true := by
  apply extensions_cover_of_upper_fin 0 7 12 13 (by decide)
  intro p hp
  change p ∈ [
    ([17, 11, 1, 10, 8], [17, 11, 0, 13, 3]),
    ([17, 11, 1, 10, 16], [17, 11, 0, 13, 11]),
    ([17, 11, 1, 10, 17], [17, 11, 0, 13, 12]),
    ([17, 11, 1, 14, 18], [17, 11, 0, 17, 13]),
    ([17, 11, 10, 10, 7], [17, 11, 9, 13, 2]),
    ([17, 11, 10, 10, 8], [17, 11, 9, 13, 3]),
    ([17, 11, 10, 10, 16], [17, 11, 9, 13, 11]),
    ([17, 11, 10, 10, 17], [17, 11, 9, 13, 12]),
    ([17, 11, 10, 14, 18], [17, 11, 9, 17, 13]),
    ([17, 15, 18, 15, 5], [17, 15, 17, 18, 0]),
    ([17, 15, 18, 15, 6], [17, 15, 17, 18, 1]),
    ([17, 15, 18, 15, 14], [17, 15, 17, 18, 9]),
    ([17, 15, 18, 15, 15], [17, 15, 17, 18, 10]),
    ([18, 0, 6, 4, 8], [18, 0, 5, 7, 3]),
    ([18, 0, 6, 4, 17], [18, 0, 5, 7, 12]),
    ([18, 0, 6, 13, 8], [18, 0, 5, 16, 3])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_minus_seven_05

end EightCarryThreePairSharp.Candidates
