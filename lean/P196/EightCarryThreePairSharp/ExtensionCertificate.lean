import P196.EightCarryThreePairSharp.MinusSeven01
import P196.EightCarryThreePairSharp.MinusSeven02
import P196.EightCarryThreePairSharp.MinusSeven03
import P196.EightCarryThreePairSharp.MinusSeven04
import P196.EightCarryThreePairSharp.MinusSeven05
import P196.EightCarryThreePairSharp.MinusSeven06
import P196.EightCarryThreePairSharp.MinusSeven07
import P196.EightCarryThreePairSharp.MinusSeven08
import P196.EightCarryThreePairSharp.PlusEight01

/-! Complete exclusion of the remaining bounded smoothing branch. -/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp.Candidates
open EightCarryMaximalWidth.Candidates

theorem cover_minus_seven :
    covered (extensions 0 7 12 quintuples) minusSevenSextuples = true := by
  have hpartition : quintuples =
      ((quintuples.drop 0).take 16) ++
      ((quintuples.drop 16).take 16) ++
      ((quintuples.drop 32).take 16) ++
      ((quintuples.drop 48).take 16) ++
      ((quintuples.drop 64).take 16) ++
      ((quintuples.drop 80).take 16) ++
      ((quintuples.drop 96).take 16) ++
      ((quintuples.drop 112).take 16) := by decide +kernel
  rw [hpartition]
  simp only [extensions_append, covered_append,
    cover_minus_seven_01, cover_minus_seven_02, cover_minus_seven_03, cover_minus_seven_04, cover_minus_seven_05, cover_minus_seven_06, cover_minus_seven_07, cover_minus_seven_08, Bool.and_self]

theorem cover_plus_eight :
    covered (extensions 8 0 11 minusSevenSextuples) ([] : List Pair) = true := by
  have hpartition : minusSevenSextuples =
      ((minusSevenSextuples.drop 0).take 20) := by decide +kernel
  rw [hpartition]
  simp only [extensions_append, covered_append,
    cover_plus_eight_01, Bool.and_self]

#print axioms cover_minus_seven
#print axioms cover_plus_eight

end EightCarryThreePairSharp.Candidates
