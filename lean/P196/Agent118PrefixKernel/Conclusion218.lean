import P196.Agent118PrefixKernel.AllRows218
import P196.Agent118PrefixKernel.Initial218
import P196.Agent118PrefixKernel.Short218

/-! Final application for the leading-digit family 218. Accepted only after every
imported check module compiled and the transitive axiom audit passed. -/
namespace Agent118.Finite218

open Lychrel196 DecimalDigits SevenColumn.Certificate Agent118.PrefixKernel Agent118.Cert218

/-- Every positive ordinary integer reaching a palindrome that begins with 218 does so
within 34 reverse-and-add steps. The digit length is not bounded. -/
theorem ancestry_bound34 :
    ∀ A P t, 0 < A → PalindromeStarts3 2 1 8 P → orbit A t = P → t ≤ 34 :=
  ancestry_bound_of_finite_checks 2 1 8 33 (by decide) ranks allRows shortDesc initialCovered

/-- All-time avoidance of this restricted palindrome family by the ordinary orbit of 196. -/
theorem no_196_218_palindrome :
    ∀ t, ¬ PalindromeStarts3 2 1 8 (orbit 196 t) :=
  no_196_of_finite_checks 2 1 8 33 (by decide) (by decide) ranks allRows shortDesc initialCovered

/-- The same statement with the target family unfolded to canonical decimal digits. -/
theorem no_196_218_palindrome_unfolded (t : Nat) :
    ¬ (Palindrome (orbit 196 t) ∧ ∃ e W, Canonical (orbit 196 t) e W ∧ 3 ≤ W ∧
        e (W - 1) = 2 ∧ e (W - 2) = 1 ∧ e (W - 3) = 8) :=
  no_196_218_palindrome t

#print axioms ancestry_bound34
#print axioms no_196_218_palindrome
#print axioms no_196_218_palindrome_unfolded
end Agent118.Finite218
