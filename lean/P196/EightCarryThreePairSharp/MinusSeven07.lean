import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 96 through 111.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven_07 :
    covered (extensions 0 7 12 ((quintuples.drop 96).take 16)) minusSevenSextuples = true := by
  apply extensions_cover_of_upper_fin 0 7 12 13 (by decide)
  intro p hp
  change p ∈ [
    ([18, 8, 9, 3, 17], [18, 8, 8, 6, 12]),
    ([18, 8, 17, 15, 7], [18, 8, 16, 18, 2]),
    ([18, 8, 17, 15, 16], [18, 8, 16, 18, 11]),
    ([18, 8, 18, 2, 5], [18, 8, 17, 5, 0]),
    ([18, 8, 18, 3, 8], [18, 8, 17, 6, 3]),
    ([18, 8, 18, 3, 17], [18, 8, 17, 6, 12]),
    ([18, 8, 18, 11, 5], [18, 8, 17, 14, 0]),
    ([18, 8, 18, 11, 14], [18, 8, 17, 14, 9]),
    ([18, 8, 18, 12, 8], [18, 8, 17, 15, 3]),
    ([18, 8, 18, 12, 17], [18, 8, 17, 15, 12]),
    ([18, 9, 15, 4, 8], [18, 9, 14, 7, 3]),
    ([18, 9, 15, 4, 17], [18, 9, 14, 7, 12]),
    ([18, 9, 15, 13, 8], [18, 9, 14, 16, 3]),
    ([18, 9, 15, 13, 17], [18, 9, 14, 16, 12]),
    ([18, 16, 7, 2, 9], [18, 16, 6, 5, 4]),
    ([18, 16, 7, 2, 18], [18, 16, 6, 5, 13])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_minus_seven_07

end EightCarryThreePairSharp.Candidates
