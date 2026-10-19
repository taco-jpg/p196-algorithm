import P196.OddPredecessorTargetSparsity.DecimalSparsity
import P196.OddPredecessorTargetSparsity.Cutoffs
import P196.OddPredecessorTargetSparsity.Sharpness

/-!
# Effective sparsity at every numerical cutoff

Agent #6: the exact ordinary target enumeration satisfies a uniform
quadratic count bound. An explicit cutoff threshold makes its fraction
at most one over any prescribed positive integer, using Nat inequalities.
-/

set_option autoImplicit false

namespace OddPredecessorTargetSparsity

/-- Below every numerical cutoff, the square of the complete target
count is at most fifty times that cutoff. -/
theorem below_quadratic (N : Nat) : (below N).length ^ 2 ≤ 50 * N := by
  by_cases hN : N ≤ 1
  · rw [below_eq_nil_small N hN]
    simp
  · have hlen : (below N).length ≤
        (belowPower (DecimalQuantitativeMass.decimalLength (N - 1))).length :=
      List.length_filter_le _ _
    calc
      (below N).length ^ 2 ≤
          (belowPower (DecimalQuantitativeMass.decimalLength (N - 1))).length ^ 2 := by
        simpa only [Nat.pow_two] using Nat.mul_le_mul hlen hlen
      _ ≤ 5 * 10 ^ DecimalQuantitativeMass.decimalLength (N - 1) :=
        belowPower_quadratic _
      _ ≤ 5 * (10 * N) := Nat.mul_le_mul_left 5 (cutoff_power_bound N (by omega))
      _ = 50 * N := by simp only [← Nat.mul_assoc]

/-- An explicit threshold bounds the proportion of qualifying target
integers by `1 / r` for every positive integer `r`. The inequality itself
also includes `r = 0` and both empty cutoffs. -/
theorem below_effectively_sparse (r N : Nat) (hN : 50 * r ^ 2 ≤ N) :
    r * (below N).length ≤ N := by
  have hsquare : (r * (below N).length) ^ 2 ≤ N ^ 2 := by
    calc
      (r * (below N).length) ^ 2 = r ^ 2 * (below N).length ^ 2 := Nat.mul_pow _ _ _
      _ ≤ r ^ 2 * (50 * N) := Nat.mul_le_mul_left _ (below_quadratic N)
      _ = (50 * r ^ 2) * N := by simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      _ ≤ N * N := Nat.mul_le_mul_right N hN
      _ = N ^ 2 := (Nat.pow_two N).symm
  by_cases hbound : r * (below N).length ≤ N
  · exact hbound
  · have hlt : N < r * (below N).length := by omega
    have hpos : 0 < r * (below N).length := by omega
    have hleft := Nat.mul_le_mul_right N (Nat.le_of_lt hlt)
    have hright := Nat.mul_lt_mul_of_pos_left hlt hpos
    rw [Nat.pow_two, Nat.pow_two] at hsquare
    omega

end OddPredecessorTargetSparsity

#print axioms OddPredecessorTargetSparsity.below_quadratic
#print axioms OddPredecessorTargetSparsity.below_effectively_sparse
