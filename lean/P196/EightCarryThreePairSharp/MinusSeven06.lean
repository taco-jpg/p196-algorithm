import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 80 through 95.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven_06 :
    covered (extensions 0 7 12 ((quintuples.drop 80).take 16)) minusSevenSextuples = true := by
  apply extensions_cover_of_upper_fin 0 7 12 13 (by decide)
  intro p hp
  change p ∈ [
    ([18, 0, 6, 13, 17], [18, 0, 5, 16, 12]),
    ([18, 0, 15, 4, 8], [18, 0, 14, 7, 3]),
    ([18, 0, 15, 4, 17], [18, 0, 14, 7, 12]),
    ([18, 0, 15, 13, 8], [18, 0, 14, 16, 3]),
    ([18, 0, 15, 13, 17], [18, 0, 14, 16, 12]),
    ([18, 7, 7, 2, 9], [18, 7, 6, 5, 4]),
    ([18, 7, 7, 2, 18], [18, 7, 6, 5, 13]),
    ([18, 7, 7, 11, 18], [18, 7, 6, 14, 13]),
    ([18, 7, 16, 2, 9], [18, 7, 15, 5, 4]),
    ([18, 7, 16, 2, 18], [18, 7, 15, 5, 13]),
    ([18, 7, 16, 11, 18], [18, 7, 15, 14, 13]),
    ([18, 8, 8, 6, 7], [18, 8, 7, 9, 2]),
    ([18, 8, 8, 15, 7], [18, 8, 7, 18, 2]),
    ([18, 8, 8, 15, 16], [18, 8, 7, 18, 11]),
    ([18, 8, 9, 2, 5], [18, 8, 8, 5, 0]),
    ([18, 8, 9, 3, 8], [18, 8, 8, 6, 3])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_minus_seven_06

end EightCarryThreePairSharp.Candidates
