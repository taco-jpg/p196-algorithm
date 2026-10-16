import ResidualFiveFibers
import Agent101PalindromeFibers

/-!
# Initial palindromes in the residual-five fiber

This specializes Agent #101's original complete numeric-fiber criterion from
commit `71691d50497edc83247b3571af276bb0ee438491` to the actual ordinary-integer
fiber `Agent103.ResidualFiveFibers.fiber`. The unique initial palindrome is
the boundary member `1661` at `r = 0`.
-/

namespace Agent103.ResidualFiveFibers

open Lychrel196

/-- A positive number of central pairs puts the odd coefficient `9` in the
prescribed profile. At the boundary all four coefficients are even. -/
theorem profile_all_even_iff (r : Nat) :
    (∀ s ∈ Agent101.coefficientWord (half r) none, s % 2 = 0) ↔ r = 0 := by
  constructor
  · intro he
    cases r with
    | zero => rfl
    | succ r =>
      have h9 : (9 : Nat) ∈ Agent101.coefficientWord (half (r + 1)) none := by
        simp [Agent101.coefficientWord, half, List.replicate_succ]
      have hbad := he 9 h9
      omega
  · rintro rfl
    simp [Agent101.coefficientWord, half]

/-- The original least-significant-first value of the halved boundary
profile `[2, 12, 12, 2]` is the ordinary integer `1661`. -/
theorem profile_halved_zero_value :
    Agent101.natValue
      ((Agent101.coefficientWord (half 0) none).map (fun s => s / 2)) = 1661 := by
  decide

/-- The boundary exception is present in the complete original fiber. -/
theorem fiber_zero_palindrome_member : 1661 ∈ fiber 0 ∧ Palindrome 1661 := by
  apply (Agent101.palindrome_mem_numericFiber_iff (half 0) none 1661).mpr
  refine ⟨?_, (profile_all_even_iff 0).mpr rfl, ?_⟩
  · decide
  · exact profile_halved_zero_value.symm

/-- Complete initial-palindrome classification for a member of this fiber. -/
theorem fiber_palindrome_iff (r n : Nat) (hn : n ∈ fiber r) :
    Palindrome n ↔ r = 0 ∧ n = 1661 := by
  constructor
  · intro hpal
    have hc := (Agent101.palindrome_mem_numericFiber_iff (half r) none n).mp
      ⟨hn, hpal⟩
    have hr := (profile_all_even_iff r).mp hc.2.1
    refine ⟨hr, ?_⟩
    subst r
    exact hc.2.2.trans profile_halved_zero_value
  · rintro ⟨rfl, rfl⟩
    exact fiber_zero_palindrome_member.2

/-- The exhaustive form also records actual membership of the exception. -/
theorem fiber_palindrome_mem_iff (r n : Nat) :
    (n ∈ fiber r ∧ Palindrome n) ↔ r = 0 ∧ n = 1661 := by
  constructor
  · rintro ⟨hn, hpal⟩
    exact (fiber_palindrome_iff r n hn).mp hpal
  · rintro ⟨rfl, rfl⟩
    exact fiber_zero_palindrome_member

/-- Every member with at least one central pair is initially nonpalindromic. -/
theorem fiber_nonpalindrome_of_pos (r n : Nat) (hr : 0 < r) (hn : n ∈ fiber r) :
    ¬ Palindrome n := by
  intro hpal
  have hz := ((fiber_palindrome_iff r n hn).mp hpal).1
  omega

#print axioms profile_all_even_iff
#print axioms profile_halved_zero_value
#print axioms fiber_zero_palindrome_member
#print axioms fiber_palindrome_iff
#print axioms fiber_palindrome_mem_iff
#print axioms fiber_nonpalindrome_of_pos

end Agent103.ResidualFiveFibers
