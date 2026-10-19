import P196.EightCarryMaximalWidth.Four01
import P196.EightCarryMaximalWidth.Four02
import P196.EightCarryMaximalWidth.Four03
import P196.EightCarryMaximalWidth.Four04
import P196.EightCarryMaximalWidth.Four05
import P196.EightCarryMaximalWidth.Four06
import P196.EightCarryMaximalWidth.Four07
import P196.EightCarryMaximalWidth.Five01
import P196.EightCarryMaximalWidth.Five02
import P196.EightCarryMaximalWidth.Five03
import P196.EightCarryMaximalWidth.Five04
import P196.EightCarryMaximalWidth.Five05
import P196.EightCarryMaximalWidth.Five06
import P196.EightCarryMaximalWidth.Six01
import P196.EightCarryMaximalWidth.Six02
import P196.EightCarryMaximalWidth.Six03
import P196.EightCarryMaximalWidth.Six04
import P196.EightCarryMaximalWidth.Six05
import P196.EightCarryMaximalWidth.Six06
import P196.EightCarryMaximalWidth.Six07
import P196.EightCarryMaximalWidth.Six08
import P196.EightCarryMaximalWidth.SevenFive01
import P196.EightCarryMaximalWidth.SevenFive02
import P196.EightCarryMaximalWidth.SevenSix01
import P196.EightCarryMaximalWidth.SevenSix02

/-!
Complete finite narrowing along both classified short cores.
Each stage assembles separately checked literal extensions. The only
calculations here are finite parent-list partition equalities.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four :
    covered (extensions 0 3 16 triples) quadruples = true := by
  have hpartition : triples =
      ((triples.drop 0).take 20) ++
      ((triples.drop 20).take 20) ++
      ((triples.drop 40).take 20) ++
      ((triples.drop 60).take 20) ++
      ((triples.drop 80).take 20) ++
      ((triples.drop 100).take 20) ++
      ((triples.drop 120).take 20) := by decide +kernel
  rw [hpartition]
  simp only [extensions_append, covered_append,
    cover_four_01, cover_four_02, cover_four_03, cover_four_04, cover_four_05, cover_four_06, cover_four_07, Bool.and_self]

theorem cover_five :
    covered (extensions 5 0 14 quadruples) quintuples = true := by
  have hpartition : quadruples =
      ((quadruples.drop 0).take 20) ++
      ((quadruples.drop 20).take 20) ++
      ((quadruples.drop 40).take 20) ++
      ((quadruples.drop 60).take 20) ++
      ((quadruples.drop 80).take 20) ++
      ((quadruples.drop 100).take 20) := by decide +kernel
  rw [hpartition]
  simp only [extensions_append, covered_append,
    cover_five_01, cover_five_02, cover_five_03, cover_five_04, cover_five_05, cover_five_06, Bool.and_self]

theorem cover_six :
    covered (extensions 0 6 13 quintuples) sextuples = true := by
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
    cover_six_01, cover_six_02, cover_six_03, cover_six_04, cover_six_05, cover_six_06, cover_six_07, cover_six_08, Bool.and_self]

theorem cover_seven_five :
    covered (extensions 5 0 14 sextuples) ([] : List Pair) = true := by
  have hpartition : sextuples =
      ((sextuples.drop 0).take 17) ++
      ((sextuples.drop 17).take 17) := by decide +kernel
  rw [hpartition]
  simp only [extensions_append, covered_append,
    cover_seven_five_01, cover_seven_five_02, Bool.and_self]

theorem cover_seven_six :
    covered (extensions 6 0 13 sextuples) ([] : List Pair) = true := by
  have hpartition : sextuples =
      ((sextuples.drop 0).take 17) ++
      ((sextuples.drop 17).take 17) := by decide +kernel
  rw [hpartition]
  simp only [extensions_append, covered_append,
    cover_seven_six_01, cover_seven_six_02, Bool.and_self]

#print axioms cover_four
#print axioms cover_five
#print axioms cover_six
#print axioms cover_seven_five
#print axioms cover_seven_six

end EightCarryMaximalWidth.Candidates
