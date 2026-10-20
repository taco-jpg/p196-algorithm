import P196.ResidualFivePredecessorCount.OuterReduction
import P196.ResidualFivePredecessorCount.MiddleCount

set_option autoImplicit false

/-!
# Exact ordinary-predecessor survivor counts in the residual-five fiber

The original fiber has 14 * 10^r distinct target integers. The executable
list `survivors r` keeps exactly those targets which admit at least one
positive ordinary reverse-and-add predecessor, with no restriction on the
predecessor width. Its cardinalities are 1, 0, 1, 1, 2, 3, 5, ... .

This counts targets, not their individual predecessors. It does not exclude
the residual-five palindrome family from the orbit of 196, bound arbitrary
inverse depth, or establish an infinite palindrome-free integer orbit.
-/

namespace P196.ResidualFivePredecessorCount

/-- The original complete fiber filter is precisely the accepted middle
enumeration with its forced two outer digit pairs. -/
theorem survivorWords_eq (r : Nat) :
    survivorWords r = (rawAcceptedWords r).map
      (fun ds => Agent101.wrapDigits 1 1 (Agent101.wrapDigits 6 6 ds)) :=
  survivorWords_outer_reduction r

/-- The empty-middle case has one target, even though that target may
have several different positive ordinary predecessors. -/
theorem survivors_zero : survivors 0 = [1661] := by
  rw [survivors, survivorWords_eq, rawAcceptedWords_zero]
  decide

/-- Exact all-parameter cardinality of the distinct original fiber members
which admit a positive ordinary predecessor. The Fibonacci theorem is
imported from the existing complete folded inverse-path enumeration. -/
theorem survivors_length_succ (r : Nat) :
    (survivors (r + 1)).length = P196.Agent9.InverseFibers.fib r := by
  rw [survivors_length_eq_words, survivorWords_eq, List.length_map]
  exact rawAcceptedWords_length_succ r

/-- The first nonempty middle length has no surviving targets. -/
theorem survivors_one : survivors 1 = [] := by
  apply List.length_eq_zero.mp
  exact survivors_length_succ 0

end P196.ResidualFivePredecessorCount

#print axioms P196.ResidualFivePredecessorCount.mem_survivors
#print axioms P196.ResidualFivePredecessorCount.survivors_nodup
#print axioms P196.ResidualFivePredecessorCount.survivors_zero
#print axioms P196.ResidualFivePredecessorCount.survivors_one
#print axioms P196.ResidualFivePredecessorCount.survivors_length_succ
