import P196.Agent118PrefixKernel.Short777_00
import P196.Agent118PrefixKernel.Short777_01
import P196.Agent118PrefixKernel.Short777_02
import P196.Agent118PrefixKernel.Short777_03
import P196.Agent118PrefixKernel.Short777_04
import P196.Agent118PrefixKernel.Short777_05
import P196.Agent118PrefixKernel.Short777_06
import P196.Agent118PrefixKernel.Short777_07
import P196.Agent118PrefixKernel.Short777_08
import P196.Agent118PrefixKernel.Short777_09
import P196.Agent118PrefixKernel.Short777_10
import P196.Agent118PrefixKernel.Short777_11
import P196.Agent118PrefixKernel.Short777_12
import P196.Agent118PrefixKernel.Short777_13
import P196.Agent118PrefixKernel.Short777_14
import P196.Agent118PrefixKernel.Short777_15
import P196.Agent118PrefixKernel.Short777_16
import P196.Agent118PrefixKernel.Short777_17
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem shortOne : ∀ a : Fin 9, shortDescentOK ranks [2*(a.val+1)] = true := by decide +kernel
theorem shortRest : ∀ a, a < 18 → ShortDescentAt ranks a := by
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
theorem shortDesc : ShortDescent ranks := shortDescent_of_cases ranks shortOne shortRest
#print axioms shortOne
#print axioms shortDesc
end Agent118.Cert777
