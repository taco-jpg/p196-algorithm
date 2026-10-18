import P196.Drafts.Agent100GroupIIOverflowSharpness.Agent100GroupIIOverflowProfiles

/-! The concrete Group II upper-exterior overlap bridge.  The redundant
comparison word is not treated as an admissible input.  Its normalized
digits are compared directly, with explicit finite zero extension at the
actual component width, including the appended overflow digit. -/

namespace Agent100.GroupIIOverflow

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open DelayedOverlapGate

/-- Actual normalized digits of the doubled component, zero after its
overflow-dependent width `2*r+7`. -/
def componentDigits (r p u v i : Nat) : Nat :=
  if i < 2 * r + 7 then
    extended (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) i
  else 0

/-- Actual next component pair word, with its irrelevant infinite tail
discarded before an overlap is formed. -/
def finiteNextComponent (r p u v i : Nat) : Nat :=
  if i < 2 * r + 7 then
    nextColumns (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) i
  else 0

theorem component_digits_formula (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, componentDigits r p u v i =
      if i < 2 * r + 6 then
        (component r (2 * p) (2 * u) (2 * v) i + componentDoubleCarry r i) % 10
      else if i = 2 * r + 6 then 1 else 0 := by
  intro i
  by_cases hi : i < 2 * r + 6
  · have hi' : i < 2 * r + 7 := by omega
    simp only [componentDigits, hi', if_true, extended, hi, output]
    rw [component_double_carry r p u v h i (by omega)]
  · by_cases he : i = 2 * r + 6
    · subst i
      have ht : 2 * r + 6 < 2 * r + 7 := by omega
      simp only [componentDigits, ht, if_true, extended, Nat.lt_irrefl, if_false]
      exact component_double_overflow r p u v h
    · have hi' : ¬ i < 2 * r + 7 := by omega
      simp only [componentDigits, hi', if_false, hi, he]

theorem component_digits_zero_after_width (r p u v i : Nat)
    (hi : 2 * r + 7 ≤ i) : componentDigits r p u v i = 0 := by
  simp only [componentDigits, show ¬ i < 2 * r + 7 by omega, if_false]

/-- Direct digit-level normalization, including the new terminal digit.
No canonical realization of the redundant input is assumed. -/
theorem redundant_extended_digits (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      extended (redundant r p u v) (2 * r + 7) i =
        shiftOne (componentDigits r p u v) i := by
  intro i hi
  have hcentral : (2 * (2 * v) + 2) % 10 = (2 * v + 1) % 10 + (2 * v + 1) % 10 := by
    have hv : v = 5 ∨ v = 6 := by unfold UpperDomain at h; omega
    rcases hv with hv | hv <;> subst v <;> decide
  by_cases he : i = 2 * r + 7
  · subst i
    have hs : 2 * r + 7 - 1 = 2 * r + 6 := by omega
    simp only [extended, Nat.lt_irrefl, if_false, redundant_overflow r p u v h,
      shiftOne, component_digits_zero_after_width r p u v (2 * r + 7) (by omega),
      show ¬ 2 * r + 7 = 0 by omega, hs]
    rw [component_digits_formula r p u v h]
    simp
  · have hi' : i < 2 * r + 7 := by omega
    simp only [extended, hi', if_true, output, shiftOne]
    rw [redundant_carry r p u v h i (by omega), component_digits_formula r p u v h]
    by_cases hz : i = 0
    · subst i
      simp only [if_true, Nat.add_zero]
      unfold UpperDomain at h
      simp only [redundant, initial, fiveWord, component, componentDoubleCarry,
        redundantCarry, Nat.mul_assoc, true_or, if_true]
      repeat (first | omega | split)
    · simp only [hz, if_false]
      rw [component_digits_formula r p u v h]
      unfold UpperDomain at h
      simp only [redundant, initial, fiveWord, component, componentDoubleCarry,
        redundantCarry, Nat.mul_assoc, true_or, if_true]
      repeat (first | omega | split)

/-- The adjacent normalized component digits add without another carry. -/
theorem adjacent_normalized_sum_bounded (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 → shiftOne (componentDigits r p u v) i ≤ 9 := by
  intro i hi
  rw [← redundant_extended_digits r p u v h i hi]
  by_cases hi' : i < 2 * r + 7
  · simp only [extended, hi', if_true]
    exact output_bounded _ _
  · simp only [extended, hi', if_false, redundant_overflow r p u v h]
    omega

theorem finite_next_component_columns (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 7 → finiteNextComponent r p u v i =
      columnSum (componentDigits r p u v) (2 * r + 7) i := by
  intro i hi
  have hj : 2 * r + 7 - 1 - i < 2 * r + 7 := by omega
  simp only [finiteNextComponent, hi, if_true, nextColumns,
    component_double_overflow r p u v h, Nat.one_ne_zero, if_false,
    columnSum, reflected, componentDigits, hj]

/-- Pairing the shifted normalized finite digit word is the overlap of
the actual enlarged component pair word. -/
theorem redundant_next_is_finite_overlap (r p u v : Nat)
    (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      nextColumns (redundant r p u v) (2 * r + 7) i =
        shiftOne (finiteNextComponent r p u v) i := by
  intro i hi
  have hj : 2 * r + 8 - 1 - i < 2 * r + 8 := by omega
  simp only [nextColumns, redundant_overflow r p u v h,
    Nat.one_ne_zero, if_false, columnSum, reflected]
  rw [redundant_extended_digits r p u v h i hi,
    redundant_extended_digits r p u v h (2 * r + 8 - 1 - i) hj]
  by_cases hz : i = 0
  · subst i
    have ha : 0 < 2 * r + 7 := by omega
    have hb : 2 * r + 8 - 1 - 0 = 2 * r + 7 := by omega
    have hc : 2 * r + 7 - 1 = 2 * r + 6 := by omega
    rw [hb]
    simp only [shiftOne, if_true, Nat.add_zero,
      component_digits_zero_after_width r p u v (2 * r + 7) (by omega),
      show ¬ 2 * r + 7 = 0 by omega, if_false, hc, Nat.zero_add]
    rw [finite_next_component_columns r p u v h 0 ha]
    simp only [columnSum, reflected, Nat.sub_zero, hc]
  · by_cases he : i = 2 * r + 7
    · subst i
      have ha : 2 * r + 7 - 1 = 2 * r + 6 := by omega
      have hb : 2 * r + 8 - 1 - (2 * r + 7) = 0 := by omega
      have hc : 2 * r + 7 - 1 - (2 * r + 6) = 0 := by omega
      rw [hb]
      simp only [shiftOne, hz, if_false, if_true, Nat.add_zero, ha,
        component_digits_zero_after_width r p u v (2 * r + 7) (by omega), Nat.zero_add,
        finiteNextComponent, Nat.lt_irrefl]
      have hd : 2 * r + 6 < 2 * r + 7 := by omega
      change componentDigits r p u v (2 * r + 6) + componentDigits r p u v 0 =
        finiteNextComponent r p u v (2 * r + 6)
      rw [finite_next_component_columns r p u v h _ hd]
      simp only [columnSum, reflected, hc]
    · have hi' : i < 2 * r + 7 := by omega
      have hip : i - 1 < 2 * r + 7 := by omega
      have hne : ¬ 2 * r + 8 - 1 - i = 0 := by omega
      have h1 : 2 * r + 8 - 1 - i = 2 * r + 7 - i := by omega
      have h2 : 2 * r + 7 - i - 1 = 2 * r + 7 - 1 - i := by omega
      have h3 : 2 * r + 7 - 1 - (i - 1) = 2 * r + 7 - i := by omega
      simp only [shiftOne, hz, hne, if_false]
      rw [finite_next_component_columns r p u v h i hi',
        finite_next_component_columns r p u v h (i - 1) hip]
      simp only [columnSum, reflected, h1, h2, h3]
      omega

end Agent100.GroupIIOverflow

#print axioms Agent100.GroupIIOverflow.component_digits_formula
#print axioms Agent100.GroupIIOverflow.component_digits_zero_after_width
#print axioms Agent100.GroupIIOverflow.redundant_extended_digits
#print axioms Agent100.GroupIIOverflow.adjacent_normalized_sum_bounded
#print axioms Agent100.GroupIIOverflow.finite_next_component_columns
#print axioms Agent100.GroupIIOverflow.redundant_next_is_finite_overlap
