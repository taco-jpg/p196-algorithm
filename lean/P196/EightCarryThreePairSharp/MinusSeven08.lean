import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 112 through 127.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven_08 :
    covered (extensions 0 7 12 ((quintuples.drop 112).take 16)) minusSevenSextuples = true := by
  apply extensions_cover_of_upper_fin 0 7 12 13 (by decide)
  intro p hp
  change p ∈ [
    ([18, 16, 7, 11, 18], [18, 16, 6, 14, 13]),
    ([18, 16, 16, 2, 9], [18, 16, 15, 5, 4]),
    ([18, 16, 16, 2, 18], [18, 16, 15, 5, 13]),
    ([18, 16, 16, 11, 18], [18, 16, 15, 14, 13]),
    ([18, 17, 8, 6, 7], [18, 17, 7, 9, 2]),
    ([18, 17, 8, 15, 7], [18, 17, 7, 18, 2]),
    ([18, 17, 8, 15, 16], [18, 17, 7, 18, 11]),
    ([18, 17, 17, 15, 7], [18, 17, 16, 18, 2]),
    ([18, 17, 17, 15, 16], [18, 17, 16, 18, 11]),
    ([18, 17, 18, 2, 5], [18, 17, 17, 5, 0]),
    ([18, 17, 18, 3, 8], [18, 17, 17, 6, 3]),
    ([18, 17, 18, 3, 17], [18, 17, 17, 6, 12]),
    ([18, 17, 18, 11, 5], [18, 17, 17, 14, 0]),
    ([18, 17, 18, 11, 14], [18, 17, 17, 14, 9]),
    ([18, 17, 18, 12, 8], [18, 17, 17, 15, 3]),
    ([18, 17, 18, 12, 17], [18, 17, 17, 15, 12])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_minus_seven_08

end EightCarryThreePairSharp.Candidates
