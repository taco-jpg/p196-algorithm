import P196.EightCarryThreePairSharp.CandidateData

/-!
Complete coverage of parent positions 16 through 31.
The imported coefficient tactic checks each literal separately.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven_02 :
    covered (extensions 0 7 12 ((quintuples.drop 16).take 16)) minusSevenSextuples = true := by
  apply extensions_cover_of_upper_fin 0 7 12 13 (by decide)
  intro p hp
  change p ∈ [
    ([13, 15, 4, 5, 15], [13, 15, 3, 8, 10]),
    ([13, 15, 4, 5, 18], [13, 15, 3, 8, 13]),
    ([13, 15, 4, 14, 6], [13, 15, 3, 17, 1]),
    ([13, 15, 4, 14, 15], [13, 15, 3, 17, 10]),
    ([13, 15, 4, 14, 18], [13, 15, 3, 17, 13]),
    ([13, 15, 13, 5, 6], [13, 15, 12, 8, 1]),
    ([13, 15, 13, 5, 9], [13, 15, 12, 8, 4]),
    ([13, 15, 13, 5, 15], [13, 15, 12, 8, 10]),
    ([13, 15, 13, 5, 18], [13, 15, 12, 8, 13]),
    ([13, 15, 13, 14, 6], [13, 15, 12, 17, 1]),
    ([13, 15, 13, 14, 15], [13, 15, 12, 17, 10]),
    ([13, 15, 13, 14, 18], [13, 15, 12, 17, 13]),
    ([14, 7, 4, 5, 9], [14, 7, 3, 8, 4]),
    ([14, 7, 4, 5, 18], [14, 7, 3, 8, 13]),
    ([14, 7, 4, 14, 18], [14, 7, 3, 17, 13]),
    ([14, 7, 13, 5, 9], [14, 7, 12, 8, 4])
  ] at hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals certify_fin13

#print axioms cover_minus_seven_02

end EightCarryThreePairSharp.Candidates
