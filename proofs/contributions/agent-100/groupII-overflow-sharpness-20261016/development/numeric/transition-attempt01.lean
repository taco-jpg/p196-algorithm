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

end Agent100.GroupIIOverflow

#print axioms Agent100.GroupIIOverflow.upper_initial_realizable
#print axioms Agent100.GroupIIOverflow.numeric_two_step_representation
