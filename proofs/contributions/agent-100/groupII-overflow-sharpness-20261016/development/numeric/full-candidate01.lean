import Agent100GroupIIOverflowSharpness

/-! Ordinary decimal realizations of the upper-exterior Group II family.
All comparisons use the finite width of the actual component orbit. -/

namespace Agent100.GroupIIOverflow

set_option maxHeartbeats 2000000
set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open DelayedOverlapGate

/-- Every upper-domain tuple has a positive ordinary decimal realization. -/
theorem upper_initial_realizable (r p u v : Nat) (h : UpperDomain r p u v) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r p u v i := by
  have ha := initial_admissible r p u v h
  exact valid_word_realizable (initial r p u v) (2 * r + 7)
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2

/-- Every initial decimal realization follows the actual two-step pair state. -/
theorem numeric_two_step_representation (n : Nat) (d : Nat → Nat)
    (r p u v : Nat) (h : UpperDomain r p u v)
    (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = initial r p u v i) :
    ∃ e, Canonical (orbit n 2) e (2 * r + 8) ∧
      ∀ i, i < 2 * r + 8 →
        columnSum e (2 * r + 8) i = (wholeOrbit r p u v 2).2 i := by
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d
    (initial r p u v) (2 * r + 7) 2 hc hr
  have hw := (whole_two_step_upper r p u v h).1
  change Canonical (orbit n 2) e (wholeOrbit r p u v 2).1 at he
  change (∀ i, i < (wholeOrbit r p u v 2).1 →
    columnSum e (wholeOrbit r p u v 2).1 i = (wholeOrbit r p u v 2).2 i) at hrep
  rw [hw] at he hrep
  exact ⟨e, he, hrep⟩

/-- The six-entry signed defect is realized by every initial ordinary integer. -/
theorem numeric_two_step_defect (n : Nat) (d : Nat → Nat)
    (r p u v : Nat) (h : UpperDomain r p u v)
    (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = initial r p u v i) :
    ∃ e, Canonical (orbit n 2) e (2 * r + 8) ∧
      ∀ i, i < 2 * r + 8 →
        (columnSum e (2 * r + 8) i : Int) -
          (shiftOne (finiteWord (componentOrbit r p u v 2).1
            (componentOrbit r p u v 2).2) i : Int) = overflowDefect r i := by
  obtain ⟨e, he, hrep⟩ := numeric_two_step_representation n d r p u v h hc hr
  refine ⟨e, he, ?_⟩
  intro i hi
  rw [hrep i hi]
  exact actual_two_step_defect r p u v h i hi

/-- Ordinary two-step output columns cannot agree on their full prefix
with the finite overlap of the actual two-step component. -/
theorem numeric_two_step_overlap_fails (n : Nat) (d : Nat → Nat)
    (r p u v : Nat) (h : UpperDomain r p u v)
    (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = initial r p u v i) :
    ∃ e, Canonical (orbit n 2) e (2 * r + 8) ∧
      (∀ i, i < 2 * r + 8 →
        (columnSum e (2 * r + 8) i : Int) -
          (shiftOne (finiteWord (componentOrbit r p u v 2).1
            (componentOrbit r p u v 2).2) i : Int) = overflowDefect r i) ∧
      ¬ (∀ i, i < 2 * r + 8 →
        columnSum e (2 * r + 8) i =
          shiftOne (finiteWord (componentOrbit r p u v 2).1
            (componentOrbit r p u v 2).2) i) := by
  obtain ⟨e, he, hd⟩ := numeric_two_step_defect n d r p u v h hc hr
  refine ⟨e, he, hd, ?_⟩
  intro heq
  have hx := hd (r + 1) (by omega)
  rw [heq (r + 1) (by omega)] at hx
  simp only [overflowDefect, true_or, if_true] at hx
  omega

/-- Every upper-domain tuple has a positive initial realization whose actual
second output exhibits the exact finite overlap defect. -/
theorem realized_overflow_defect (r p u v : Nat) (h : UpperDomain r p u v) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 7) ∧
      (∀ i, i < 2 * r + 7 →
        columnSum d (2 * r + 7) i = initial r p u v i) ∧
      (∃ e, Canonical (orbit n 2) e (2 * r + 8) ∧
        (∀ i, i < 2 * r + 8 →
          (columnSum e (2 * r + 8) i : Int) -
            (shiftOne (finiteWord (componentOrbit r p u v 2).1
              (componentOrbit r p u v 2).2) i : Int) = overflowDefect r i) ∧
        ¬ (∀ i, i < 2 * r + 8 →
          columnSum e (2 * r + 8) i =
            shiftOne (finiteWord (componentOrbit r p u v 2).1
              (componentOrbit r p u v 2).2) i)) := by
  obtain ⟨n, d, hn, hc, hr⟩ := upper_initial_realizable r p u v h
  exact ⟨n, d, hn, hc, hr, numeric_two_step_overlap_fails n d r p u v h hc hr⟩

end Agent100.GroupIIOverflow

#print axioms Agent100.GroupIIOverflow.upper_initial_realizable
#print axioms Agent100.GroupIIOverflow.numeric_two_step_representation
#print axioms Agent100.GroupIIOverflow.numeric_two_step_defect
#print axioms Agent100.GroupIIOverflow.numeric_two_step_overlap_fails
#print axioms Agent100.GroupIIOverflow.realized_overflow_defect
