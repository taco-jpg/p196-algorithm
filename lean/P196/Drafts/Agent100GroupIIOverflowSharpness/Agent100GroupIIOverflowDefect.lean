import P196.Drafts.Agent100GroupIIOverflowSharpness.Agent100GroupIIOverflowBridge
import P196.Agent8CommonOverflowDefect.Agent8DefectTransport

/-! The concrete common-overflow defect of the upper-exterior Group II
family. The general transport identity is imported unchanged from Agent 8.
Only the actual finite component prefix is overlapped. -/

namespace Agent100.GroupIIOverflow

set_option maxHeartbeats 2000000
set_option maxRecDepth 10000

open DecimalDigits FoldedDecimal DelayedOverlapGate
open P196.Agent8.CommonOverflowDefect

/-- Coefficients of x^(r+1) * (1 - x^2 - x^3 + x^5). -/
def overflowDefect (r i : Nat) : Int :=
  if i = r + 1 ∨ i = r + 6 then 1
  else if i = r + 3 ∨ i = r + 4 then -1 else 0

/-- The existing central digit defect is exactly the supported defect
required by the imported common-carry theorem, including both tails. -/
theorem supported_digit_defect (r p u v : Nat) (h : UpperDomain r p u v)
    (i : Nat) :
    oldDigitDefect (GroupII.middle r p u v) (redundant r p u v)
      (2 * r + 7) i = GroupII.digitDefect r i := by
  by_cases hi : i < 2 * r + 7
  · rw [oldDigitDefect_lt _ _ _ _ hi]
    exact normalized_digit_defect_exact r p u v h i hi
  · rw [oldDigitDefect_zero_of_ge _ _ _ _ (by omega)]
    simp only [GroupII.digitDefect]
    repeat (first | omega | split)

/-- Algebraic expansion of this particular five-column digit defect. -/
theorem digit_defect_difference (r i : Nat) :
    GroupII.digitDefect r i - shift (GroupII.digitDefect r) 1 i =
      overflowDefect r i := by
  simp only [shift, GroupII.digitDefect, overflowDefect]
  repeat (first | omega | split)

/-- The same old digit defect now survives as its finite difference.
The redundant input need not be an admissible pair word. -/
theorem middle_redundant_defect (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      (nextColumns (GroupII.middle r p u v) (2 * r + 7) i : Int) -
        (nextColumns (redundant r p u v) (2 * r + 7) i : Int) =
          overflowDefect r i := by
  intro i hi
  have ha := (antisymmetricDefect_iff
    (GroupII.middle r p u v) (redundant r p u v) (2 * r + 7)).mpr
      (normalized_digit_defect_antisymmetric r p u v h)
  have ht := common_carry_transport (GroupII.middle r p u v)
    (redundant r p u v) (2 * r + 7) 1 (Or.inr rfl)
      (middle_overflow r p u v h) (redundant_overflow r p u v h)
      ha i (by omega)
  have he : oldDigitDefect (GroupII.middle r p u v) (redundant r p u v)
      (2 * r + 7) = GroupII.digitDefect r :=
    funext (supported_digit_defect r p u v h)
  rw [he, digit_defect_difference] at ht
  exact ht

/-- Concrete finite overlap difference across the entire enlarged width. -/
theorem finite_overlap_defect (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      (nextColumns (GroupII.middle r p u v) (2 * r + 7) i : Int) -
        (shiftOne (finiteNextComponent r p u v) i : Int) =
          overflowDefect r i := by
  intro i hi
  rw [← redundant_next_is_finite_overlap r p u v h i hi]
  exact middle_redundant_defect r p u v h i hi

/-- A positive defect lies at a valid interior column for every spacer. -/
theorem finite_overlap_witness (r p u v : Nat) (h : UpperDomain r p u v) :
    (nextColumns (GroupII.middle r p u v) (2 * r + 7) (r + 1) : Int) -
      (shiftOne (finiteNextComponent r p u v) (r + 1) : Int) = 1 := by
  have hd := finite_overlap_defect r p u v h (r + 1) (by omega)
  simpa only [overflowDefect, true_or, if_true] using hd

theorem finite_overlap_fails (r p u v : Nat) (h : UpperDomain r p u v) :
    ¬ ∀ i, i < 2 * r + 8 →
      nextColumns (GroupII.middle r p u v) (2 * r + 7) i =
        shiftOne (finiteNextComponent r p u v) i := by
  intro he
  have hd := finite_overlap_witness r p u v h
  rw [he (r + 1) (by omega)] at hd
  omega

end Agent100.GroupIIOverflow

#print axioms Agent100.GroupIIOverflow.supported_digit_defect
#print axioms Agent100.GroupIIOverflow.digit_defect_difference
#print axioms Agent100.GroupIIOverflow.middle_redundant_defect
#print axioms Agent100.GroupIIOverflow.finite_overlap_defect
#print axioms Agent100.GroupIIOverflow.finite_overlap_witness
#print axioms Agent100.GroupIIOverflow.finite_overlap_fails
