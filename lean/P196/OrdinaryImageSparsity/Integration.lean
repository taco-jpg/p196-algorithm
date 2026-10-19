import P196.OrdinaryImageSparsity.ProfileCounts
import P196.OrdinaryImageSparsity.Enumeration
import P196.OddPredecessorTargetSparsity.Cutoffs

/-!
# Effective sparsity of the entire positive ordinary reverse-and-add image

Agent #6: the exact finite list includes every positive ordinary image
below the exclusive cutoff once. Its cardinality is bounded by the
existing admissible-profile census. Decimal rounding and the cubic
profile bound give an explicit integer threshold at every cutoff.

These are upper bounds for distinct target integers. They assert no
optimal constant, exact overlap census, or statement about orbit timing.
-/

set_option autoImplicit false

namespace OrdinaryImageSparsity

/-- The cube of the number of distinct positive ordinary targets below
an arbitrary cutoff is at most nine hundred times the square of that cutoff. -/
theorem allBelow_cubic (N : Nat) :
    (allBelow N).length ^ 3 ≤ 900 * N ^ 2 := by
  by_cases hN : N ≤ 1
  · rw [allBelow_eq_nil_small N hN]
    simp
  · let W := DecimalQuantitativeMass.decimalLength (N - 1)
    have hlen : (allBelow N).length ≤ profileCount W :=
      allBelow_length_le N
    have hdecimal : 10 ^ W ≤ 10 * N :=
      OddPredecessorTargetSparsity.cutoff_power_bound N (by omega)
    calc
      (allBelow N).length ^ 3 ≤ profileCount W ^ 3 :=
        Nat.pow_le_pow_left hlen 3
      _ ≤ 9 * 10 ^ (2 * W) := profileCount_cubic W
      _ = 9 * (10 ^ W) ^ 2 := by
        rw [Nat.mul_comm 2 W, Nat.pow_mul]
      _ ≤ 9 * (10 * N) ^ 2 :=
        Nat.mul_le_mul_left 9 (Nat.pow_le_pow_left hdecimal 2)
      _ = 900 * N ^ 2 := by
        rw [Nat.mul_pow]
        simp only [← Nat.mul_assoc]

/-- For any integer denominator, the displayed cubic threshold makes
the proportion of positive ordinary targets at most its reciprocal.
The natural-number inequality also includes denominator zero. -/
theorem allBelow_effectively_sparse (r N : Nat)
    (hN : 900 * r ^ 3 ≤ N) :
    r * (allBelow N).length ≤ N := by
  have hcube : (r * (allBelow N).length) ^ 3 ≤ N ^ 3 := by
    calc
      (r * (allBelow N).length) ^ 3 =
          r ^ 3 * (allBelow N).length ^ 3 := Nat.mul_pow _ _ _
      _ ≤ r ^ 3 * (900 * N ^ 2) :=
        Nat.mul_le_mul_left _ (allBelow_cubic N)
      _ = (900 * r ^ 3) * N ^ 2 := by ac_rfl
      _ ≤ N * N ^ 2 := Nat.mul_le_mul_right _ hN
      _ = N ^ 3 :=
        (Nat.mul_comm N (N ^ 2)).trans (Nat.pow_succ N 2).symm
  by_cases hbound : r * (allBelow N).length ≤ N
  · exact hbound
  · have hlt : N < r * (allBelow N).length := by omega
    have hpow := Nat.pow_lt_pow_left hlt (by decide : 3 ≠ 0)
    omega

end OrdinaryImageSparsity

#print axioms OrdinaryImageSparsity.allBelow_cubic
#print axioms OrdinaryImageSparsity.allBelow_effectively_sparse
