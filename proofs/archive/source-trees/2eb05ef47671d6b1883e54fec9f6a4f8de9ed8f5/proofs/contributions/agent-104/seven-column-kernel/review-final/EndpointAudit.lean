import Conclusion739

open Lychrel196 SevenColumnKernel.PalindromeBridge

-- These examples check the desired theorem types directly, without carrying
-- a hidden certificate, width, reachability, or ancestry-bound hypothesis.
example : ∀ A P t, 0 < A → PalindromeStarts739 P → orbit A t = P → t ≤ 39 :=
  SevenColumnKernel.Finite739.ancestry_bound39

example : ∀ t, ¬ PalindromeStarts739 (orbit 196 t) :=
  SevenColumnKernel.Finite739.no_196_739_palindrome

#check SevenColumnKernel.Finite739.ancestry_bound39
#check SevenColumnKernel.Finite739.no_196_739_palindrome
#check SevenColumnKernel.ActualAncestry.ancestry_bound39_of_finite_checks
#check SevenColumnKernel.ActualAncestry.actual_iterPairs_rank

#print axioms SevenColumnKernel.Finite739.ancestry_bound39
#print axioms SevenColumnKernel.Finite739.no_196_739_palindrome
#print axioms SevenColumnKernel.Finite739.initialCovered
#print axioms SevenColumn.Certificate739.allRows
#print axioms SevenColumn.Certificate739.allRowsFast
#print axioms SevenColumn.Certificate739.initialLongChecked
#print axioms SevenColumn.Certificate739.initialShortChecked
#print axioms SevenColumn.Certificate739.shortChecked
#print axioms SevenColumnKernel.ActualAncestry.actual_iterPairs_rank
#print axioms Lychrel196.no_palindrome_through_100
