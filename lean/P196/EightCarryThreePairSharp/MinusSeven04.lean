import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 48 through 63.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven_04 :
    covered (extensions 0 7 12 ((quintuples.drop 48).take 16)) minusSevenSextuples = true := by
  apply extensions_cover_of_upper_fin 0 7 12 13 (by decide)
  intro p hp
  change p ∈ [
    ([17, 2, 1, 10, 16], [17, 2, 0, 13, 11]),
    ([17, 2, 1, 10, 17], [17, 2, 0, 13, 12]),
    ([17, 2, 1, 14, 18], [17, 2, 0, 17, 13]),
    ([17, 6, 9, 6, 5], [17, 6, 8, 9, 0]),
    ([17, 6, 9, 6, 6], [17, 6, 8, 9, 1]),
    ([17, 6, 18, 15, 5], [17, 6, 17, 18, 0]),
    ([17, 6, 18, 15, 6], [17, 6, 17, 18, 1]),
    ([17, 6, 18, 15, 14], [17, 6, 17, 18, 9]),
    ([17, 6, 18, 15, 15], [17, 6, 17, 18, 10]),
    ([17, 11, 1, 1, 7], [17, 11, 0, 4, 2]),
    ([17, 11, 1, 1, 8], [17, 11, 0, 4, 3]),
    ([17, 11, 1, 1, 16], [17, 11, 0, 4, 11]),
    ([17, 11, 1, 1, 17], [17, 11, 0, 4, 12]),
    ([17, 11, 1, 5, 9], [17, 11, 0, 8, 4]),
    ([17, 11, 1, 5, 18], [17, 11, 0, 8, 13]),
    ([17, 11, 1, 10, 7], [17, 11, 0, 13, 2])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_minus_seven_04

end EightCarryThreePairSharp.Candidates
