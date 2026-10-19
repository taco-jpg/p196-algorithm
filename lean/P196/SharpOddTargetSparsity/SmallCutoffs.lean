import P196.OddPredecessorTargetSparsity.Integration

/-!
# Small cutoffs and the obstruction to constant eight

Agent #6: finite certificates use the existing complete target census.
The cutoff convention is exclusive throughout. All numerical certificates
are checked by the ordinary Lean kernel.
-/

set_option autoImplicit false

namespace SharpOddTargetSparsity

open OddPredecessorTargetSparsity

private theorem width_three_small_count :
    ∀ N : Fin 1001,
      ((belowPower 3).filter (fun Y => decide (Y < N.val))).length ^ 2 ≤
        9 * N.val := by
  decide +kernel

/-- Every cumulative width at most three satisfies the constant-nine
bound at each exclusive numerical cutoff up to one thousand. -/
theorem small_count_bound (W N : Nat) (hW : W ≤ 3) (hN : N ≤ 1000) :
    ((belowPower W).filter (fun Y => decide (Y < N))).length ^ 2 ≤
      9 * N := by
  have hmono :
      ((belowPower W).filter (fun Y => decide (Y < N))).length ≤
        ((belowPower 3).filter (fun Y => decide (Y < N))).length := by
    rcases (show W = 0 ∨ W = 1 ∨ W = 2 ∨ W = 3 by omega) with h | h | h | h
    all_goals subst W
    all_goals
      simp only [belowPower, List.filter_append, List.length_append,
        List.filter_nil, List.length_nil]
    all_goals omega
  calc
    ((belowPower W).filter (fun Y => decide (Y < N))).length ^ 2 ≤
        ((belowPower 3).filter (fun Y => decide (Y < N))).length ^ 2 := by
      simpa only [Nat.pow_two] using Nat.mul_le_mul hmono hmono
    _ ≤ 9 * N := width_three_small_count ⟨N, by omega⟩

/-- Exactly 1269 positive integers below 200000 have odd complete
ordinary reverse-and-add predecessor count. -/
theorem below_two_hundred_thousand : (below 200000).length = 1269 := by
  have hwidth : DecimalQuantitativeMass.decimalLength (200000 - 1) = 6 := by
    simp [DecimalQuantitativeMass.decimalLength]
  unfold below
  rw [hwidth]
  decide +kernel

/-- Constant eight cannot bound the squared complete target count
uniformly over all exclusive numerical cutoffs. -/
theorem below_quadratic_eight_fails :
    ¬ ∀ N : Nat, (below N).length ^ 2 ≤ 8 * N := by
  intro h
  have hbound := h 200000
  rw [below_two_hundred_thousand] at hbound
  exact (by decide : ¬ (1269 ^ 2 ≤ 8 * 200000)) hbound

end SharpOddTargetSparsity

#print axioms SharpOddTargetSparsity.small_count_bound
#print axioms SharpOddTargetSparsity.below_two_hundred_thousand
#print axioms SharpOddTargetSparsity.below_quadratic_eight_fails
