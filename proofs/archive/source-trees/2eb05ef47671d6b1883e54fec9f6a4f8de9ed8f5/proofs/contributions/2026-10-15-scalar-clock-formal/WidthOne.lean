import ScalarOrbit

/-! Width-one admissible words cannot complete any rotation of the scalar
seven-clock. These are actual carry and width calculations, not independent
choices of boundary controls. -/

namespace WidthOne

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory ScalarOrbit

theorem control_at_width_one (q : Nat → Nat) (L t : Nat)
    (hw : widthAt q L t = 1) : controlAt q L t = false := by
  change (iterPairs q L t).1 = 1 at hw
  simp [ScalarOrbit.controlAt, ActualScalar.actualControl, hw, carry]

theorem control_at_width_two_seven (q : Nat → Nat) (L t : Nat)
    (hw : widthAt q L t = 2) (ho : outerAt q L t = 7) :
    controlAt q L t = false := by
  change (iterPairs q L t).1 = 2 at hw
  change (iterPairs q L t).2 0 = 7 at ho
  simp [ScalarOrbit.controlAt, ActualScalar.actualControl, hw, carry, ho]

theorem outer_after_width_one (q : Nat → Nat) (L t : Nat)
    (ha : Admissible L q) (hw : widthAt q L t = 1) :
    outerAt q L (t+1) = (ScalarClock.step (outerAt q L t) false).1 := by
  have h := congrArg Prod.fst (actual_step_at q L t ha)
  simp only [Prod.fst] at h
  rw [control_at_width_one q L t hw] at h
  exact h

theorem outer_after_width_two_seven (q : Nat → Nat) (L t : Nat)
    (ha : Admissible L q) (hw : widthAt q L t = 2)
    (ho : outerAt q L t = 7) : outerAt q L (t+1) = 14 := by
  have h := congrArg Prod.fst (actual_step_at q L t ha)
  simp only [Prod.fst] at h
  rw [control_at_width_two_seven q L t hw ho, ho] at h
  simpa [ScalarClock.step] using h

/-- No even width-one starting coefficient completes any clock rotation. -/
theorem no_complete_period (q : Nat → Nat) (s : Nat)
    (ha : Admissible 1 q) : ¬ ClockSegment q 1 0 s 7 := by
  intro hc
  have hp : ∀ t, t ≤ 7 → outerAt q 1 t = ScalarClock.phase (s+t) := by
    intro t ht
    simpa only [Nat.zero_add] using hc t ht
  have h0 := hp 0 (by decide)
  have h1 := hp 1 (by decide)
  have h2 := hp 2 (by decide)
  have h3 := hp 3 (by decide)
  have h4 := hp 4 (by decide)
  have e0 := overflow_at_of_phase q 1 0 (s+0) ha h0
  have e1 := overflow_at_of_phase q 1 1 (s+1) ha h1
  have e2 := overflow_at_of_phase q 1 2 (s+2) ha h2
  have w0 : widthAt q 1 0 = 1 := rfl
  have w1 := widthAt_succ q 1 0 ha
  have w2 := widthAt_succ q 1 1 ha
  have w3 := widthAt_succ q 1 2 ha
  simp only [Nat.reduceAdd] at w1 w2 w3
  have heven : outerAt q 1 0 % 2 = 0 := ha.2.2.2.2 0 (by decide) (by decide)
  have hb : s % 7 < 7 := Nat.mod_lt _ (by decide)
  have hcases : s % 7 = 0 ∨ s % 7 = 1 ∨ s % 7 = 2 ∨ s % 7 = 3 ∨
      s % 7 = 4 ∨ s % 7 = 5 ∨ s % 7 = 6 := by omega
  rcases hcases with h | h | h | h | h | h | h
  all_goals simp [ScalarClock.phase, ScalarClock.phaseValue, Nat.add_mod, h] at h0 h1 h2 h3 h4
  all_goals simp [ScalarClock.overflow, ScalarClock.overflowValue, Nat.add_mod, h] at e0 e1 e2
  all_goals first
    | omega
    | have hv := outer_after_width_one q 1 0 ha w0
      simpa [ScalarClock.step, h0, h1] using hv
    | have hw : widthAt q 1 1 = 2 := by omega
      have hv := outer_after_width_two_seven q 1 1 ha hw h1
      simp only [Nat.reduceAdd] at hv
      omega
    | have hw : widthAt q 1 2 = 2 := by omega
      have hv := outer_after_width_two_seven q 1 2 ha hw h2
      simp only [Nat.reduceAdd] at hv
      omega
    | have hw : widthAt q 1 3 = 2 := by omega
      have hv := outer_after_width_two_seven q 1 3 ha hw h3
      simp only [Nat.reduceAdd] at hv
      omega

theorem zero_complete_periods (q : Nat → Nat) (s R : Nat)
    (ha : Admissible 1 q) (hc : ClockSegment q 1 0 s (7*R)) : R = 0 := by
  by_cases hn : R = 0
  · exact hn
  · exfalso
    apply no_complete_period q s ha
    intro i hi
    exact hc i (by omega)

end WidthOne
