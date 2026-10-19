import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 0 through 19.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_plus_eight_01 :
    covered (extensions 8 0 11 ((minusSevenSextuples.drop 0).take 20)) ([] : List Pair) = true := by
  apply extensions_cover_of_upper_fin 8 0 11 13 (by decide)
  intro p hp
  change p ∈ [
    ([18, 7, 7, 2, 9, 0], [18, 7, 6, 5, 4, 7]),
    ([18, 7, 7, 2, 18, 0], [18, 7, 6, 5, 13, 7]),
    ([18, 7, 7, 2, 18, 9], [18, 7, 6, 5, 13, 16]),
    ([18, 7, 7, 11, 18, 0], [18, 7, 6, 14, 13, 7]),
    ([18, 7, 7, 11, 18, 9], [18, 7, 6, 14, 13, 16]),
    ([18, 7, 16, 2, 9, 0], [18, 7, 15, 5, 4, 7]),
    ([18, 7, 16, 2, 18, 0], [18, 7, 15, 5, 13, 7]),
    ([18, 7, 16, 2, 18, 9], [18, 7, 15, 5, 13, 16]),
    ([18, 7, 16, 11, 18, 0], [18, 7, 15, 14, 13, 7]),
    ([18, 7, 16, 11, 18, 9], [18, 7, 15, 14, 13, 16]),
    ([18, 16, 7, 2, 9, 0], [18, 16, 6, 5, 4, 7]),
    ([18, 16, 7, 2, 18, 0], [18, 16, 6, 5, 13, 7]),
    ([18, 16, 7, 2, 18, 9], [18, 16, 6, 5, 13, 16]),
    ([18, 16, 7, 11, 18, 0], [18, 16, 6, 14, 13, 7]),
    ([18, 16, 7, 11, 18, 9], [18, 16, 6, 14, 13, 16]),
    ([18, 16, 16, 2, 9, 0], [18, 16, 15, 5, 4, 7]),
    ([18, 16, 16, 2, 18, 0], [18, 16, 15, 5, 13, 7]),
    ([18, 16, 16, 2, 18, 9], [18, 16, 15, 5, 13, 16]),
    ([18, 16, 16, 11, 18, 0], [18, 16, 15, 14, 13, 7]),
    ([18, 16, 16, 11, 18, 9], [18, 16, 15, 14, 13, 16])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_plus_eight_01

end EightCarryThreePairSharp.Candidates
