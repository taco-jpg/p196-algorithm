import P196.Agent118PrefixKernel.AllRows777
import P196.Agent118PrefixKernel.Initial777
import P196.Agent118PrefixKernel.Short777

/-! Final application for the leading-digit family 777. Accepted only after every
imported check module compiled and the transitive axiom audit passed. -/
namespace Agent118.Finite777

open Lychrel196 DecimalDigits SevenColumn.Certificate Agent118.PrefixKernel Agent118.Cert777

/-- Every positive ordinary integer reaching a palindrome that begins with 777 does so
within 25 reverse-and-add steps. The digit length is not bounded. -/
theorem ancestry_bound25 :
    ∀ A P t, 0 < A → PalindromeStarts3 7 7 7 P → orbit A t = P → t ≤ 25 :=
  ancestry_bound_of_finite_checks 7 7 7 24 (by decide) ranks allRows shortDesc initialCovered

/-- All-time avoidance of this restricted palindrome family by the ordinary orbit of 196. -/
theorem no_196_777_palindrome :
    ∀ t, ¬ PalindromeStarts3 7 7 7 (orbit 196 t) :=
  no_196_of_finite_checks 7 7 7 24 (by decide) (by decide) ranks allRows shortDesc initialCovered

/-- The same statement with the target family unfolded to canonical decimal digits. -/
theorem no_196_777_palindrome_unfolded (t : Nat) :
    ¬ (Palindrome (orbit 196 t) ∧ ∃ e W, Canonical (orbit 196 t) e W ∧ 3 ≤ W ∧
        e (W - 1) = 7 ∧ e (W - 2) = 7 ∧ e (W - 3) = 7) :=
  no_196_777_palindrome t

#print axioms ancestry_bound25
#print axioms no_196_777_palindrome
#print axioms no_196_777_palindrome_unfolded
end Agent118.Finite777
