import AllRows217
import Initial217
import Short217

/-! Final application for the leading-digit family 217. Accepted only after every
imported check module compiled and the transitive axiom audit passed. -/
namespace Agent118.Finite217

open Lychrel196 DecimalDigits SevenColumn.Certificate Agent118.PrefixKernel Agent118.Cert217

/-- Every positive ordinary integer reaching a palindrome that begins with 217 does so
within 23 reverse-and-add steps. The digit length is not bounded. -/
theorem ancestry_bound23 :
    ∀ A P t, 0 < A → PalindromeStarts3 2 1 7 P → orbit A t = P → t ≤ 23 :=
  ancestry_bound_of_finite_checks 2 1 7 22 (by decide) ranks allRows shortDesc initialCovered

/-- All-time avoidance of this restricted palindrome family by the ordinary orbit of 196. -/
theorem no_196_217_palindrome :
    ∀ t, ¬ PalindromeStarts3 2 1 7 (orbit 196 t) :=
  no_196_of_finite_checks 2 1 7 22 (by decide) (by decide) ranks allRows shortDesc initialCovered

/-- The same statement with the target family unfolded to canonical decimal digits. -/
theorem no_196_217_palindrome_unfolded (t : Nat) :
    ¬ (Palindrome (orbit 196 t) ∧ ∃ e W, Canonical (orbit 196 t) e W ∧ 3 ≤ W ∧
        e (W - 1) = 2 ∧ e (W - 2) = 1 ∧ e (W - 3) = 7) :=
  no_196_217_palindrome t

#print axioms ancestry_bound23
#print axioms no_196_217_palindrome
#print axioms no_196_217_palindrome_unfolded
end Agent118.Finite217
