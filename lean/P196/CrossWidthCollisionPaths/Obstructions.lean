import P196.CrossWidthCollisionPaths.Realization

/-!
# The center restrictions are necessary

These two finite traces satisfy every bounded edge and reflection condition.
One has an odd shorter-word center; the other has an odd longer-word center.
The realization equivalence therefore excludes both as ordinary collisions
at their respective specified widths.
-/

set_option autoImplicit false

namespace CrossWidthCollisionPaths

open CrossWidthCollisionStates

/-- A reflected closed trace whose reconstructed shorter center is eleven. -/
def shortCenterPath : Nat → State := fun _ => initial

/-- A reflected closed trace whose reconstructed longer center is eleven. -/
def longCenterPath (i : Nat) : State :=
  if i = 2 then ⟨10, 2, 1⟩ else if i = 3 then ⟨10, 1, 2⟩ else initial

/-- Edge closure and reflection do not imply the shorter center condition. -/
theorem short_center_obstruction :
    Closed 3 shortCenterPath ∧ ¬ Valid 3 shortCenterPath := by
  constructor
  · refine ⟨by decide, rfl, rfl, ?_, ?_⟩
    · intro i _ _
      change Edge initial initial
      decide +kernel
    · intro i _ _
      rfl
  · intro h
    have hc := h.short_center 1 (by decide) (by decide)
    have hbad : shortWord shortCenterPath 1 % 2 ≠ 0 := by decide +kernel
    exact hbad hc

/-- Edge closure and reflection do not imply the longer center condition. -/
theorem long_center_obstruction :
    Closed 4 longCenterPath ∧ ¬ Valid 4 longCenterPath := by
  constructor
  · refine ⟨by decide, by decide +kernel, by decide +kernel, ?_, ?_⟩
    · intro i hi hiL
      have hcases : i = 1 ∨ i = 2 ∨ i = 3 := by omega
      rcases hcases with rfl | rfl | rfl <;> decide +kernel
    · intro i hi hiL
      have hcases : i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
      rcases hcases with rfl | rfl | rfl | rfl <;> decide +kernel
  · intro h
    have hc := h.long_center 2 (by decide) (by decide)
    have hbad : longWord 4 longCenterPath 2 % 2 ≠ 0 := by decide +kernel
    exact hbad hc

end CrossWidthCollisionPaths

#print axioms CrossWidthCollisionPaths.shortCenterPath
#print axioms CrossWidthCollisionPaths.longCenterPath
#print axioms CrossWidthCollisionPaths.short_center_obstruction
#print axioms CrossWidthCollisionPaths.long_center_obstruction
