import P196.SharpOddTargetSparsity.ProfileBounds
import P196.OddPredecessorTargetSparsity.Integration

/-!
# Counting the possible leading coefficient blocks

Agent #6: the last decimal-width block is bounded by its admissible
exterior coefficients. The exact cumulative census supplies all earlier
widths, giving a linear bound for each two-digit cutoff interval.
-/

set_option autoImplicit false

namespace SharpOddTargetSparsity

open Agent101 DecimalQuantitativeMass OddPredecessorTargetCensus
open OddPredecessorTargetSparsity

private theorem filter_belowPower_succ (W N : Nat) :
    ((belowPower (W + 1)).filter (fun Y => decide (Y < N))).length =
      ((belowPower W).filter (fun Y => decide (Y < N))).length +
      (noOverflowWords (W + 1)).countP (fun qs => decide (natValue qs < N)) +
      (overflowWords W).countP (fun qs => decide (natValue qs < N)) := by
  have ht : ((targets (W + 1)).filter (fun Y => decide (Y < N))).length =
      (noOverflowWords (W + 1)).countP (fun qs => decide (natValue qs < N)) +
      (overflowWords W).countP (fun qs => decide (natValue qs < N)) := by
    rw [← List.countP_eq_length_filter, targets, if_neg (by omega),
      List.countP_map, List.countP_append, Nat.add_sub_cancel]
    rfl
  rw [belowPower, List.filter_append, List.length_append, ht, Nat.add_assoc]

/-- A cutoff in a given decimal-width block only needs the admitted
outer coefficient groups of that last width. Earlier widths may be
counted in full. -/
theorem below_count_bound (W N a : Nat) (hW : 4 ≤ W)
    (hd : decimalLength (N - 1) = W) (ha : 10 ≤ a) (ha' : a ≤ 99)
    (hN : N ≤ (a + 1) * 10 ^ (W - 2)) :
    (below N).length ≤ (belowPower (W - 1)).length +
      lowBlockCount a * 10 ^ ((W - 3) / 2) +
      highBlockCount a * 10 ^ ((W - 4) / 2) := by
  have hstep : W = (W - 1) + 1 := by omega
  have hparts := filter_belowPower_succ (W - 1) N
  rw [← hstep] at hparts
  have heq : (below N).length =
      ((belowPower W).filter (fun Y => decide (Y < N))).length := by
    rw [below, hd]
  rw [← heq] at hparts
  have hbase := List.length_filter_le (fun Y => decide (Y < N)) (belowPower (W - 1))
  have hlo := count_noOverflow_lt W N a hW ha ha' hN
  have hhi := count_overflow_lt (W - 1) N a (by omega) ha ha'
    (by simpa only [show W - 1 - 1 = W - 2 by omega] using hN)
  rw [show W - 1 - 3 = W - 4 by omega] at hhi
  omega

/-- At an even target width, the complete count is bounded by the
finite even-width coefficient envelope times its power-of-ten scale. -/
theorem below_even_envelope (k N a : Nat)
    (hd : decimalLength (N - 1) = 2 * k + 4)
    (ha : 10 ≤ a) (ha' : a ≤ 99)
    (hN : N ≤ (a + 1) * 10 ^ (2 * k + 2)) :
    9 * (below N).length + 29 ≤ evenEnvelope a * 10 ^ k := by
  have hb := below_count_bound (2 * k + 4) N a (by omega) hd ha ha'
    (by simpa only [show 2 * k + 4 - 2 = 2 * k + 2 by omega] using hN)
  simp only [show 2 * k + 4 - 1 = 2 * k + 3 by omega,
    show (2 * k + 4 - 3) / 2 = k by omega,
    show (2 * k + 4 - 4) / 2 = k by omega] at hb
  have hc := belowPower_count_odd k
  have hm := Nat.mul_le_mul_left 9 hb
  unfold evenEnvelope
  simp only [Nat.mul_add, Nat.add_mul, Nat.mul_assoc] at hm ⊢
  omega

/-- At an odd target width, the longer no-overflow profiles have ten
times as many inner choices as the adjacent overflow profiles. -/
theorem below_odd_envelope (k N a : Nat)
    (hd : decimalLength (N - 1) = 2 * k + 5)
    (ha : 10 ≤ a) (ha' : a ≤ 99)
    (hN : N ≤ (a + 1) * 10 ^ (2 * k + 3)) :
    9 * (below N).length + 29 ≤ oddEnvelope a * 10 ^ k := by
  have hb := below_count_bound (2 * k + 5) N a (by omega) hd ha ha'
    (by simpa only [show 2 * k + 5 - 2 = 2 * k + 3 by omega] using hN)
  simp only [show 2 * k + 5 - 1 = 2 * k + 4 by omega,
    show (2 * k + 5 - 3) / 2 = k + 1 by omega,
    show (2 * k + 5 - 4) / 2 = k by omega, Nat.pow_succ] at hb
  have hc := belowPower_count_even k
  have hm := Nat.mul_le_mul_left 9 hb
  unfold oddEnvelope
  simp only [Nat.mul_add, Nat.add_mul, Nat.mul_assoc,
    Nat.mul_comm, Nat.mul_left_comm] at hm hc ⊢
  omega

end SharpOddTargetSparsity

#print axioms SharpOddTargetSparsity.below_count_bound
#print axioms SharpOddTargetSparsity.below_even_envelope
#print axioms SharpOddTargetSparsity.below_odd_envelope
