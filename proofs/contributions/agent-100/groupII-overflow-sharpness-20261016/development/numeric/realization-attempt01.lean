import Agent100GroupIIOverflowProfiles

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

end Agent100.GroupIIOverflow

#print axioms Agent100.GroupIIOverflow.upper_initial_realizable
