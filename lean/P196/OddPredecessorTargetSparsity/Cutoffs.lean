import P196.OddPredecessorTargetSparsity.Enumeration

/-!
# Exact enumeration below an arbitrary numerical cutoff

Agent #6: the existing executable decimal length supplies a sufficient
width bound for every target below the cutoff. Filtering the cumulative
census then retains exactly the positive targets of odd predecessor parity.
-/

set_option autoImplicit false

namespace OddPredecessorTargetSparsity

open DecimalDigits Agent101 DecimalQuantitativeMass
open Agent105Predecessors9df76b

/-- The complete odd-predecessor target census below the exclusive cutoff.
Using the width of `N - 1` also handles decimal powers without an extra
width block; zero and one produce empty lists. -/
def below (N : Nat) : List Nat :=
  (belowPower (decimalLength (N - 1))).filter (fun Y => decide (Y < N))

private theorem canonical_width_below_cutoff (Y : Nat) (e : Nat → Nat)
    (K N : Nat) (hY : Canonical Y e K) (hYN : Y < N) :
    K ≤ decimalLength (N - 1) := by
  have hyw := canonical_decimalWidth Y e K hY
  have hYpos : 0 < Y := Nat.lt_of_lt_of_le (Nat.pow_pos (by decide)) hyw.2.1
  obtain ⟨d, W, hc⟩ := canonical_exists (N - 1) (by omega)
  rw [decimalLength_of_canonical (N - 1) d W hc]
  have hnw := canonical_decimalWidth (N - 1) d W hc
  have hylo := hyw.2.1
  have hnupper := hnw.2.2
  by_cases hKW : K ≤ W
  · exact hKW
  · have hp := Nat.pow_le_pow_right (by decide : 0 < 10)
      (show W ≤ K - 1 by omega)
    omega

/-- Filtering preserves the cumulative census's numerical uniqueness. -/
theorem below_nodup (N : Nat) : (below N).Nodup := by
  exact List.Pairwise.filter _ (belowPower_nodup _)

/-- Every enumerated integer is positive and strictly below its cutoff. -/
theorem below_bounds (N Y : Nat) (hY : Y ∈ below N) : 0 < Y ∧ Y < N := by
  obtain ⟨hp, hN⟩ := List.mem_filter.mp hY
  exact ⟨(belowPower_bounds _ Y hp).1, of_decide_eq_true hN⟩

/-- The filtered list has the exact complete positive predecessor-parity
semantics at every numerical cutoff and every canonical target width. -/
theorem mem_below (Y : Nat) (e : Nat → Nat) (K N : Nat)
    (hY : Canonical Y e K) :
    Y ∈ below N ↔ Y < N ∧ (predecessors e K).length % 2 = 1 := by
  rw [below, List.mem_filter, mem_belowPower Y e K _ hY]
  simp only [decide_eq_true_eq]
  constructor
  · rintro ⟨⟨_, hp⟩, hN⟩
    exact ⟨hN, hp⟩
  · rintro ⟨hN, hp⟩
    exact ⟨⟨canonical_width_below_cutoff Y e K N hY hN, hp⟩, hN⟩

/-- The exclusive cutoffs zero and one contain no positive targets. -/
theorem below_eq_nil_small (N : Nat) (hN : N ≤ 1) : below N = [] := by
  apply List.eq_nil_iff_forall_not_mem.mpr
  intro Y hY
  obtain ⟨hpos, hlt⟩ := below_bounds N Y hY
  omega

/-- Rounding the exclusive cutoff to the next decimal power loses a
factor of at most ten. The small empty cutoffs are handled separately. -/
theorem cutoff_power_bound (N : Nat) (hN : 2 ≤ N) :
    10 ^ decimalLength (N - 1) ≤ 10 * N := by
  obtain ⟨d, W, hc⟩ := canonical_exists (N - 1) (by omega)
  rw [decimalLength_of_canonical (N - 1) d W hc]
  have hw := canonical_decimalWidth (N - 1) d W hc
  have hW : W = (W - 1) + 1 := by have hpos := hc.1; omega
  have hm := Nat.mul_le_mul_left 10 hw.2.1
  rw [hW, Nat.pow_succ]
  omega

end OddPredecessorTargetSparsity

#print axioms OddPredecessorTargetSparsity.below
#print axioms OddPredecessorTargetSparsity.below_nodup
#print axioms OddPredecessorTargetSparsity.below_bounds
#print axioms OddPredecessorTargetSparsity.mem_below
#print axioms OddPredecessorTargetSparsity.below_eq_nil_small
#print axioms OddPredecessorTargetSparsity.cutoff_power_bound
