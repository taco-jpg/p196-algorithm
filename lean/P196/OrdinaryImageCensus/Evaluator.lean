import P196.OrdinaryImageCensus.Counts

/-!
# Arithmetic evaluation of the complete ordinary-image census

The parity formulas evaluate each decimal-width count using a power of
nineteen and the existing arithmetic count of adjacent-width collisions.
The additive census identities justify the natural-number subtraction.
-/

set_option autoImplicit false

namespace OrdinaryImageCensus

open CrossWidthTargetRecurrence

/-- Evaluate the number of distinct positive ordinary outputs with W
decimal digits without constructing their coefficient or target lists. -/
def imageCount (W : Nat) : Nat :=
  if W = 0 then 0
  else if W = 1 then 4
  else if W % 2 = 0 then
    (27 * 19 ^ ((W - 2) / 2) + 1) / 2 - targetCount (W - 1)
  else
    (189 * 19 ^ ((W - 3) / 2) - 1) / 2 - targetCount (W - 1)

/-- The arithmetic evaluator gives the exact length of the complete
ordinary target list at every natural decimal width. -/
theorem imageCount_eq_length (W : Nat) :
    imageCount W = (widthTargets W).length := by
  by_cases hzero : W = 0
  · subst W
    rw [imageCount, if_pos rfl, count_zero]
  by_cases hone : W = 1
  · subst W
    rw [imageCount, if_neg (by decide : (1 : Nat) ≠ 0), if_pos rfl, count_one]
  by_cases heven : W % 2 = 0
  · have hwidth : 2 * ((W - 2) / 2) + 2 = W := by omega
    have hshort : 2 * ((W - 2) / 2) + 1 = W - 1 := by omega
    have hcount := count_even ((W - 2) / 2)
    rw [hwidth, hshort] at hcount
    rw [imageCount, if_neg hzero, if_neg hone, if_pos heven]
    omega
  · have hwidth : 2 * ((W - 3) / 2) + 3 = W := by omega
    have hshort : 2 * ((W - 3) / 2) + 2 = W - 1 := by omega
    have hcount := count_odd ((W - 3) / 2)
    rw [hwidth, hshort] at hcount
    rw [imageCount, if_neg hzero, if_neg hone, if_neg heven]
    omega

/-- Kernel-checked distinct ordinary-image counts through eight digits. -/
theorem small_imageCount :
    (List.range 9).map imageCount =
      [0, 4, 14, 93, 256, 1793, 4872, 34107, 92590] := by
  decide +kernel

end OrdinaryImageCensus

#print axioms OrdinaryImageCensus.imageCount
#print axioms OrdinaryImageCensus.imageCount_eq_length
#print axioms OrdinaryImageCensus.small_imageCount
