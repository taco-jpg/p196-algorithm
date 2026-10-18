import P196.Drafts.Agent100GroupIIOverflowSharpness.Agent100GroupIIOverflowDefect

/-! Actual two-step component and whole orbits, using their actual widths.
Overlap is always formed after finite zero extension; arbitrary infinite
tails of the pair functions are never part of the comparison. -/

namespace Agent100.GroupIIOverflow

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open DelayedOverlapGate

abbrev componentOrbit (r p u v k : Nat) : Nat × (Nat → Nat) :=
  iterPairs (component r p u v) (2 * r + 6) k

abbrev wholeOrbit (r p u v k : Nat) : Nat × (Nat → Nat) :=
  iterPairs (initial r p u v) (2 * r + 7) k

def finiteWord (L : Nat) (q : Nat → Nat) (i : Nat) : Nat :=
  if i < L then q i else 0

def TwoStepOverlap (r p u v : Nat) : Prop :=
  (wholeOrbit r p u v 2).1 = (componentOrbit r p u v 2).1 + 1 ∧
    ∀ i, i < (wholeOrbit r p u v 2).1 →
      (wholeOrbit r p u v 2).2 i =
        shiftOne (finiteWord (componentOrbit r p u v 2).1
          (componentOrbit r p u v 2).2) i

def FullDomain (r p u v : Nat) : Prop :=
  1 ≤ r ∧ 1 ≤ p ∧ p ≤ 9 ∧ 5 ≤ u ∧ u ≤ 8 ∧ 5 ≤ v ∧ v ≤ 6 ∧ u + v ≤ 13

theorem component_two_step_upper (r p u v : Nat) (h : UpperDomain r p u v) :
    (componentOrbit r p u v 2).1 = 2 * r + 7 ∧
      ∀ i, i < 2 * r + 7 → (componentOrbit r p u v 2).2 i =
        nextColumns (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) i := by
  have he := component_next r p u v h
  have hq : carry (nextColumns (component r p u v) (2 * r + 6)) (2 * r + 6) = 1 :=
    (carry_congr_upto _ _ _ he _ (Nat.le_refl _)).trans (component_double_overflow r p u v h)
  change nextWidth (nextColumns (component r p u v) (2 * r + 6))
      (nextWidth (component r p u v) (2 * r + 6)) = 2 * r + 7 ∧
    ∀ i, i < 2 * r + 7 →
      nextColumns (nextColumns (component r p u v) (2 * r + 6))
        (nextWidth (component r p u v) (2 * r + 6)) i = _
  rw [component_width r p u v h]
  constructor
  · simp only [nextWidth, hq, Nat.one_ne_zero, if_false]
  · intro i _
    simp only [nextColumns, hq, component_double_overflow r p u v h,
      Nat.one_ne_zero, if_false, columnSum, reflected]
    rw [extended_congr_upto _ _ _ he i, extended_congr_upto _ _ _ he (2 * r + 6 + 1 - 1 - i)]

theorem whole_two_step_upper (r p u v : Nat) (h : UpperDomain r p u v) :
    (wholeOrbit r p u v 2).1 = 2 * r + 8 ∧
      ∀ i, i < 2 * r + 8 → (wholeOrbit r p u v 2).2 i =
        nextColumns (GroupII.middle r p u v) (2 * r + 7) i := by
  have he := initial_next r p u v h
  have hq : carry (nextColumns (initial r p u v) (2 * r + 7)) (2 * r + 7) = 1 :=
    (carry_congr_upto _ _ _ he _ (Nat.le_refl _)).trans (middle_overflow r p u v h)
  change nextWidth (nextColumns (initial r p u v) (2 * r + 7))
      (nextWidth (initial r p u v) (2 * r + 7)) = 2 * r + 8 ∧
    ∀ i, i < 2 * r + 8 →
      nextColumns (nextColumns (initial r p u v) (2 * r + 7))
        (nextWidth (initial r p u v) (2 * r + 7)) i = _
  rw [initial_width r p u v h]
  constructor
  · simp only [nextWidth, hq, Nat.one_ne_zero, if_false]
  · intro i _
    simp only [nextColumns, hq, middle_overflow r p u v h,
      Nat.one_ne_zero, if_false, columnSum, reflected]
    rw [extended_congr_upto _ _ _ he i, extended_congr_upto _ _ _ he (2 * r + 7 + 1 - 1 - i)]

theorem upper_component_finite_eq (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, finiteWord (componentOrbit r p u v 2).1 (componentOrbit r p u v 2).2 i =
      finiteNextComponent r p u v i := by
  have hc := component_two_step_upper r p u v h
  intro i
  unfold finiteWord
  rw [hc.1]
  by_cases hi : i < 2 * r + 7
  · simp only [hi, if_true, finiteNextComponent, hc.2 i hi]
  · simp only [hi, if_false, finiteNextComponent]

theorem returned_component_zero_after_width (r p u v i : Nat)
    (hr : 1 ≤ r) (hi : 2 * r + 6 ≤ i) : GroupII.returnedComponent r p u v i = 0 := by
  simp only [GroupII.returnedComponent]
  repeat (first | omega | split)

theorem lower_component_finite_eq (r p u v : Nat) (h : GroupII.Domain r p u v) :
    ∀ i, finiteWord (componentOrbit r p u v 2).1 (componentOrbit r p u v 2).2 i =
      GroupII.returnedComponent r p u v i := by
  have hc := GroupII.component_two_step_return r p u v h
  intro i
  unfold finiteWord
  change (if i < (iterPairs (component r p u v) (2 * r + 6) 2).1 then
    (iterPairs (component r p u v) (2 * r + 6) 2).2 i else 0) = _
  rw [hc.1]
  by_cases hi : i < 2 * r + 6
  · simp only [hi, if_true, hc.2 i hi]
  · simp only [hi, if_false]
    exact (returned_component_zero_after_width r p u v i h.1 (by omega)).symm

theorem lower_two_step_overlap (r p u v : Nat) (h : GroupII.Domain r p u v) :
    TwoStepOverlap r p u v := by
  have hc := GroupII.component_two_step_return r p u v h
  have hq := GroupII.whole_two_step_return r p u v h
  unfold TwoStepOverlap
  change (iterPairs (initial r p u v) (2 * r + 7) 2).1 =
      (iterPairs (component r p u v) (2 * r + 6) 2).1 + 1 ∧ _
  refine ⟨by rw [hq.1, hc.1], ?_⟩
  intro i hi
  have hi' : i < 2 * r + 7 := by simpa only [hq.1] using hi
  change (iterPairs (initial r p u v) (2 * r + 7) 2).2 i = _
  rw [hq.2 i hi']
  simp only [shiftOne, lower_component_finite_eq r p u v h]


/-- The symbolic defect is also the exact defect of the actual two-step
component/whole trajectories at their enlarged physical widths. -/
theorem actual_two_step_defect (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      ((wholeOrbit r p u v 2).2 i : Int) -
        (shiftOne (finiteWord (componentOrbit r p u v 2).1
          (componentOrbit r p u v 2).2) i : Int) = overflowDefect r i := by
  intro i hi
  have hq := whole_two_step_upper r p u v h
  have hf : finiteWord (componentOrbit r p u v 2).1 (componentOrbit r p u v 2).2 =
      finiteNextComponent r p u v := funext (upper_component_finite_eq r p u v h)
  rw [hq.2 i hi, hf]
  exact finite_overlap_defect r p u v h i hi

theorem upper_two_step_overlap_fails (r p u v : Nat) (h : UpperDomain r p u v) :
    ¬ TwoStepOverlap r p u v := by
  intro ho
  have hq := whole_two_step_upper r p u v h
  have hf : finiteWord (componentOrbit r p u v 2).1 (componentOrbit r p u v 2).2 =
      finiteNextComponent r p u v := funext (upper_component_finite_eq r p u v h)
  apply finite_overlap_fails r p u v h
  intro i hi
  have hi' : i < (wholeOrbit r p u v 2).1 := by rw [hq.1]; exact hi
  have he := ho.2 i hi'
  rw [hq.2 i hi, hf] at he
  exact he

/-- Sharpness within the complete stated Group II family.  This does not
classify any other cores, shifts, encodings, or later return times. -/
theorem two_step_overlap_iff (r p u v : Nat) (h : FullDomain r p u v) :
    TwoStepOverlap r p u v ↔ p ≤ 4 := by
  constructor
  · intro ho
    by_cases hp : p ≤ 4
    · exact hp
    · have hu : UpperDomain r p u v := by
        unfold FullDomain at h
        unfold UpperDomain
        omega
      exact False.elim (upper_two_step_overlap_fails r p u v hu ho)
  · intro hp
    have hl : GroupII.Domain r p u v := by
      unfold FullDomain at h
      unfold GroupII.Domain
      omega
    exact lower_two_step_overlap r p u v hl

end Agent100.GroupIIOverflow

#print axioms Agent100.GroupIIOverflow.component_two_step_upper
#print axioms Agent100.GroupIIOverflow.whole_two_step_upper
#print axioms Agent100.GroupIIOverflow.upper_component_finite_eq
#print axioms Agent100.GroupIIOverflow.returned_component_zero_after_width
#print axioms Agent100.GroupIIOverflow.lower_component_finite_eq
#print axioms Agent100.GroupIIOverflow.lower_two_step_overlap

#print axioms Agent100.GroupIIOverflow.actual_two_step_defect
#print axioms Agent100.GroupIIOverflow.upper_two_step_overlap_fails
#print axioms Agent100.GroupIIOverflow.two_step_overlap_iff
