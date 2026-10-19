import P196.OddPredecessorTargetSparsity.Cutoffs

/-!
# The decimal-power constant does not hold at every cutoff

Agent #6: an ordinary kernel-checked finite count at the exclusive cutoff
two thousand refutes a uniform constant-five quadratic bound. This
counterexample makes no optimality claim about the constant fifty.
-/

set_option autoImplicit false

namespace OddPredecessorTargetSparsity

/-- Exactly 124 positive integers below 2000 have odd complete
ordinary reverse-and-add predecessor count. -/
theorem below_two_thousand : (below 2000).length = 124 := by
  have hwidth : DecimalQuantitativeMass.decimalLength (2000 - 1) = 4 := by
    simp [DecimalQuantitativeMass.decimalLength]
  unfold below
  rw [hwidth]
  decide +kernel

/-- The constant-five bound at decimal powers cannot be extended to
all numerical cutoffs. -/
theorem below_quadratic_five_fails :
    ¬ ∀ N : Nat, (below N).length ^ 2 ≤ 5 * N := by
  intro h
  have hbound := h 2000
  rw [below_two_thousand] at hbound
  exact (by decide : ¬ (124 ^ 2 ≤ 5 * 2000)) hbound

end OddPredecessorTargetSparsity

#print axioms OddPredecessorTargetSparsity.below_two_thousand
#print axioms OddPredecessorTargetSparsity.below_quadratic_five_fails
