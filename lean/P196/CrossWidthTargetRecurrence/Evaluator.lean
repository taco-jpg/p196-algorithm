import P196.CrossWidthTargetRecurrence.Recurrence

/-!
# Arithmetic evaluation of the ordinary shared-target census

A window of three consecutive counts follows the scalar recurrence.
Its initial values come from the existing kernel-checked census. The
paired-width theorem then identifies the arithmetic evaluator with the
complete target-list length at every natural shorter source width.
-/

set_option autoImplicit false

namespace CrossWidthTargetRecurrence

open CrossWidthTargetCensus

/-- Three consecutive counts, updated by the scalar census recurrence. -/
def countWindow : Nat → Nat × Nat × Nat
  | 0 => (1, 2, 7)
  | k + 1 =>
      let w := countWindow k
      (w.2.1, w.2.2, 2 * w.2.2 + 3 * w.2.1 + w.1)

private theorem initial_counts :
    ((targets 2).length, (targets 4).length, (targets 6).length) =
      (1, 2, 7) := by
  have h := congrArg (fun xs : List Nat => (xs[2]!, xs[4]!, xs[6]!))
    small_target_counts
  change ((targets 2).length, (targets 4).length, (targets 6).length) =
    (1, 2, 7) at h
  exact h

/-- Every component of the computed window is the corresponding exact
ordinary census count at an even shorter source width. -/
theorem countWindow_eq_lengths (k : Nat) :
    countWindow k =
      ((targets (2 * k + 2)).length,
       (targets (2 * (k + 1) + 2)).length,
       (targets (2 * (k + 2) + 2)).length) := by
  induction k with
  | zero => exact initial_counts.symm
  | succ k ih =>
    rw [countWindow, ih]
    exact Prod.ext rfl (Prod.ext rfl (even_count_recurrence k).symm)

/-- Evaluate the number of distinct common ordinary outputs at shorter
source width L using only the three-count arithmetic window. -/
def targetCount (L : Nat) : Nat :=
  if L < 2 then 0 else (countWindow ((L - 2) / 2)).1

/-- The arithmetic evaluator equals the length of the complete,
duplicate-free ordinary target census at every natural source width. -/
theorem targetCount_eq_length (L : Nat) :
    targetCount L = (targets L).length := by
  by_cases hsmall : L < 2
  · rw [targetCount, if_pos hsmall, targets, if_pos hsmall]
    rfl
  · rw [targetCount, if_neg hsmall, countWindow_eq_lengths]
    change (targets (2 * ((L - 2) / 2) + 2)).length = (targets L).length
    by_cases heven : L % 2 = 0
    · have hindex : 2 * ((L - 2) / 2) + 2 = L := by omega
      rw [hindex]
    · have hindex : 2 * ((L - 2) / 2) + 3 = L := by omega
      exact (targets_paired_length ((L - 2) / 2)).trans
        (congrArg (fun W : Nat => (targets W).length) hindex)

/-- Kernel-checked initial values of the arithmetic recurrence evaluator. -/
theorem small_countWindow :
    (List.range 9).map (fun k => (countWindow k).1) =
      [1, 2, 7, 21, 65, 200, 616, 1897, 5842] := by
  decide +kernel

end CrossWidthTargetRecurrence

#print axioms CrossWidthTargetRecurrence.countWindow
#print axioms CrossWidthTargetRecurrence.countWindow_eq_lengths
#print axioms CrossWidthTargetRecurrence.targetCount
#print axioms CrossWidthTargetRecurrence.targetCount_eq_length
#print axioms CrossWidthTargetRecurrence.small_countWindow
