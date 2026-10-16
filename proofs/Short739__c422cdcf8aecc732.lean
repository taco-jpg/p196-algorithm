import Short739_00
import Short739_01
import Short739_02
import Short739_03
import Short739_04
import Short739_05
import Short739_06
import Short739_07
import Short739_08
import Short739_09
import Short739_10
import Short739_11
import Short739_12
import Short739_13
import Short739_14
import Short739_15
import Short739_16
import Short739_17
namespace SevenColumn.Certificate739
open Certificate ShortBoundary
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem shortOne : ∀ a : Fin 9, lookup ranks (nextWord [2*(a.val+1)]) = none := by decide +kernel
theorem shortRest : ∀ a, a < 18 → ShortAt ranks a := by
  intro a ha
  have cases : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨ a = 17 := by omega
  rcases cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact shortAt00
  · exact shortAt01
  · exact shortAt02
  · exact shortAt03
  · exact shortAt04
  · exact shortAt05
  · exact shortAt06
  · exact shortAt07
  · exact shortAt08
  · exact shortAt09
  · exact shortAt10
  · exact shortAt11
  · exact shortAt12
  · exact shortAt13
  · exact shortAt14
  · exact shortAt15
  · exact shortAt16
  · exact shortAt17
theorem shortChecked : ∀ s ∈ shortWords, lookup ranks (nextWord s) = none :=
  shortChecked_of_cases ranks shortOne shortRest
#print axioms shortOne
#print axioms shortChecked
end SevenColumn.Certificate739
