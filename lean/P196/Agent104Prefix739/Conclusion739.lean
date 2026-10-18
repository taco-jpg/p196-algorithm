import P196.Agent104Prefix739.AllRows739
import P196.Agent104Prefix739.Initial739
import P196.Agent104Prefix739.Short739
import P196.Agent104Prefix739.ActualAncestry

/-! Final application. This module is accepted only after all imported concrete
certificate assemblies and its own axiom audit have successfully compiled. -/
namespace SevenColumnKernel.Finite739

open Lychrel196 SevenColumn.Certificate SevenColumn.Certificate739
open SevenColumnKernel.ActualAncestry SevenColumnKernel.PalindromeBridge

theorem initialCovered :
    ∀ p ∈ targetInitialWords, checkInitial ranks 38 p = true := by
  apply initialWords_checked_of_index_checks ranks 38 initialShortChecked
  intro i hi
  exact initialLongChecked i hi

/-- Every positive ordinary integer reaching a 739-prefix palindrome does so
within 39 reverse-and-add steps. The digit length is not bounded. -/
theorem ancestry_bound39 :
    ∀ A P t, 0 < A → PalindromeStarts739 P → orbit A t = P → t ≤ 39 :=
  ancestry_bound39_of_finite_checks ranks allRows shortChecked initialCovered

/-- All-time avoidance of this restricted palindrome family by 196. -/
theorem no_196_739_palindrome :
    ∀ t, ¬ PalindromeStarts739 (orbit 196 t) :=
  no_196_739_palindrome_of_finite_checks ranks allRows shortChecked initialCovered

#print axioms initialCovered
#print axioms ancestry_bound39
#print axioms no_196_739_palindrome
end SevenColumnKernel.Finite739
