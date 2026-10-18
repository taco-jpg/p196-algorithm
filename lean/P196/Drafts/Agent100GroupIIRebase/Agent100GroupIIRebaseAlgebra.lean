import P196.Drafts.Agent100GroupIIOverflowSharpness.Agent100GroupIIOverflowSharpness

/-! Signed correction for the actual upper-domain Group II second whole word.
This module proves only integer identities.  Nonnegativity and admissibility
of the natural-number component are separate obligations. -/

namespace Agent100.GroupIIRebase

open DecimalDigits FoldedDecimal DelayedOverlapGate RawSymmetryObstruction
open Agent100.GroupIIOverflow

set_option maxHeartbeats 2000000
set_option maxRecDepth 10000

/-- Coefficients of x^(r+1) * (1 - x - x^3 + x^4). -/
def rebaseDelta (r i : Nat) : Int :=
  if i = r + 1 ∨ i = r + 5 then 1
  else if i = r + 2 ∨ i = r + 4 then -1 else 0

/-- The correction is added to the finite, actually widened second component. -/
def rebasedInt (r p u v i : Nat) : Int :=
  (finiteNextComponent r p u v i : Int) + rebaseDelta r i

/-- This definition alone makes no assertion that truncation preserves the
signed coefficient.  That requires a separate nonnegativity proof. -/
def rebasedComponent (r p u v i : Nat) : Nat :=
  Int.toNat (rebasedInt r p u v i)

/-- The four-site correction has exactly the previously checked overlap
defect after adding its left-zero-extended previous coefficient. -/
theorem rebase_delta_overlap (r i : Nat) (hr : 1 ≤ r) :
    rebaseDelta r i + previous (rebaseDelta r) i = overflowDefect r i := by
  cases i with
  | zero => simp [previous, rebaseDelta, overflowDefect]
  | succ i =>
    simp only [previous, rebaseDelta, overflowDefect]
    repeat (first | omega | split)

/-- The signed correction uses the actual second component at every index,
including its zero-extended right tail. -/
theorem rebasedInt_actual_component (r p u v : Nat) (h : UpperDomain r p u v)
    (i : Nat) :
    rebasedInt r p u v i =
      (finiteWord (componentOrbit r p u v 2).1
        (componentOrbit r p u v 2).2 i : Int) + rebaseDelta r i := by
  rw [upper_component_finite_eq r p u v h i]
  rfl

/-- Concrete signed expansion for this correction, with the left boundary
handled by the original previous operator. -/
theorem rebasedInt_overlap (r p u v i : Nat) (hr : 1 ≤ r) :
    rebasedInt r p u v i + previous (rebasedInt r p u v) i =
      (shiftOne (finiteNextComponent r p u v) i : Int) + overflowDefect r i := by
  have hd := rebase_delta_overlap r i hr
  cases i with
  | zero =>
    simp [previous, shiftOne, rebasedInt] at hd ⊢
    omega
  | succ i =>
    simp [previous, shiftOne, rebasedInt] at hd ⊢
    omega

/-- The symbolic second whole word is the signed overlap throughout its
complete physical width, including the new terminal column. -/
theorem finite_whole_rebasedInt (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      (nextColumns (GroupII.middle r p u v) (2 * r + 7) i : Int) =
        rebasedInt r p u v i + previous (rebasedInt r p u v) i := by
  intro i hi
  have hd := finite_overlap_defect r p u v h i hi
  have he := rebasedInt_overlap r p u v i h.1
  omega

/-- The same equality for the actual two-step whole orbit.  It remains an
Int identity; no nonnegative inverse or admissible component is assumed. -/
theorem actual_whole_rebasedInt (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      ((wholeOrbit r p u v 2).2 i : Int) =
        rebasedInt r p u v i + previous (rebasedInt r p u v) i := by
  intro i hi
  have hd := actual_two_step_defect r p u v h i hi
  have hf : finiteWord (componentOrbit r p u v 2).1
      (componentOrbit r p u v 2).2 = finiteNextComponent r p u v :=
    funext (upper_component_finite_eq r p u v h)
  rw [hf] at hd
  have he := rebasedInt_overlap r p u v i h.1
  omega

end Agent100.GroupIIRebase

#print axioms Agent100.GroupIIRebase.rebase_delta_overlap
#print axioms Agent100.GroupIIRebase.rebasedInt_actual_component
#print axioms Agent100.GroupIIRebase.rebasedInt_overlap
#print axioms Agent100.GroupIIRebase.finite_whole_rebasedInt
#print axioms Agent100.GroupIIRebase.actual_whole_rebasedInt
