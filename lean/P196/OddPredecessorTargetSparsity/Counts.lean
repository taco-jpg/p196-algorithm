import P196.OddPredecessorTargetSparsity.Enumeration

/-!
# Exact cumulative census of targets with odd predecessor cardinality

Agent #6: sum the disjoint decimal-width census by adjoining two widths
at a time. The identities keep all arithmetic in natural numbers and
include the exceptional initial widths explicitly.
-/

set_option autoImplicit false

namespace OddPredecessorTargetSparsity

open OddPredecessorTargetCensus

private theorem length_belowPower_add_two (W : Nat) :
    (belowPower (W + 2)).length = (belowPower W).length +
      (targets (W + 1)).length + (targets (W + 2)).length := by
  simp only [belowPower, List.length_append]

/-- There are no positive targets below the width-zero decimal bound. -/
theorem length_belowPower_zero : (belowPower 0).length = 0 := by
  rfl

/-- Exactly four qualifying positive targets are below ten. -/
theorem length_belowPower_one : (belowPower 1).length = 4 := by
  simp only [belowPower, List.length_append, List.length_nil,
    length_targets_one, Nat.zero_add]

/-- Exactly fourteen qualifying positive targets are below one hundred. -/
theorem length_belowPower_two : (belowPower 2).length = 14 := by
  have htwo : (targets 2).length = 10 := by
    simpa using length_targets_even 0
  change (belowPower 1 ++ targets 2).length = 14
  rw [List.length_append, length_belowPower_one, htwo]

/-- Exactly sixty-four qualifying positive targets are below one thousand. -/
theorem length_belowPower_three : (belowPower 3).length = 64 := by
  change (belowPower 2 ++ targets 3).length = 64
  rw [List.length_append, length_belowPower_two, length_targets_three]

/-- Exact cumulative count at every even decimal cutoff of width at least four. -/
theorem belowPower_count_even (k : Nat) :
    9 * (belowPower (2 * k + 4)).length + 29 = 1505 * 10 ^ k := by
  induction k with
  | zero =>
    have hfour : (targets 4).length = 100 := by
      simpa using length_targets_even 1
    have htotal : (belowPower 4).length = 164 := by
      simpa only [length_belowPower_two, length_targets_three, hfour]
        using length_belowPower_add_two 2
    simp only [Nat.mul_zero, Nat.zero_add, Nat.pow_zero, Nat.mul_one, htotal]
  | succ k ih =>
    have hodd := length_targets_odd k
    have heven := length_targets_even (k + 2)
    have hoddWidth : 2 * k + 5 = (2 * k + 4) + 1 := by omega
    have hevenWidth : 2 * (k + 2) + 2 = (2 * k + 4) + 2 := by omega
    rw [hoddWidth] at hodd
    rw [hevenWidth] at heven
    rw [show 2 * (k + 1) + 4 = (2 * k + 4) + 2 by omega,
      length_belowPower_add_two, hodd, heven]
    simp only [Nat.pow_succ]
    omega

/-- Exact cumulative count at every odd decimal cutoff of width at least three. -/
theorem belowPower_count_odd (k : Nat) :
    9 * (belowPower (2 * k + 3)).length + 29 = 605 * 10 ^ k := by
  induction k with
  | zero =>
    simp only [Nat.mul_zero, Nat.zero_add, Nat.pow_zero, Nat.mul_one,
      length_belowPower_three]
  | succ k ih =>
    have heven := length_targets_even (k + 1)
    have hodd := length_targets_odd k
    have hevenWidth : 2 * (k + 1) + 2 = (2 * k + 3) + 1 := by omega
    have hoddWidth : 2 * k + 5 = (2 * k + 3) + 2 := by omega
    rw [hevenWidth] at heven
    rw [hoddWidth] at hodd
    rw [show 2 * (k + 1) + 3 = (2 * k + 3) + 2 by omega,
      length_belowPower_add_two, heven, hodd]
    simp only [Nat.pow_succ]
    omega

end OddPredecessorTargetSparsity

#print axioms OddPredecessorTargetSparsity.length_belowPower_zero
#print axioms OddPredecessorTargetSparsity.length_belowPower_one
#print axioms OddPredecessorTargetSparsity.length_belowPower_two
#print axioms OddPredecessorTargetSparsity.length_belowPower_three
#print axioms OddPredecessorTargetSparsity.belowPower_count_even
#print axioms OddPredecessorTargetSparsity.belowPower_count_odd
