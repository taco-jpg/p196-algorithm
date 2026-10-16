import Agent105Predecessors9df76b

/-!
Agent #105 / session 9df76b: two small kernel controls for the complete
ordinary predecessor list. Canonical target certificates connect each
literal digit list to the actual numerical target in mem_predecessors.
The list equalities use kernel decide; no large reversal is expanded.
-/

namespace Agent105PredecessorControls9df76b

open DecimalDigits Agent101 Agent105Predecessors9df76b

set_option maxRecDepth 100000

/-- The first positive target has no predecessor; the smallest ordinary
and overflowing-singleton images have their complete singleton lists. -/
theorem small_targets :
    (Canonical 1 (digitFn [1]) 1 ∧
      predecessors (digitFn [1]) 1 = []) ∧
    (Canonical 2 (digitFn [2]) 1 ∧
      predecessors (digitFn [2]) 1 = [1]) ∧
    (Canonical 10 (digitFn [0, 1]) 2 ∧
      predecessors (digitFn [0, 1]) 2 = [5]) := by
  refine ⟨⟨?_, by decide⟩, ⟨?_, by decide⟩, ⟨?_, by decide⟩⟩
  · exact (canonicalDigits_iff [1]).mp (by simp [canonicalDigits, digitsBounded])
  · exact (canonicalDigits_iff [2]).mp (by simp [canonicalDigits, digitsBounded])
  · exact (canonicalDigits_iff [0, 1]).mp (by simp [canonicalDigits, digitsBounded])

/-- Both possible source widths occur, in the actual finite enumerator's
order: the width-three branch first, followed by all width-two sources. -/
theorem two_width_121 :
    Canonical 121 (digitFn [1, 2, 1]) 3 ∧
      predecessors (digitFn [1, 2, 1]) 3 =
        [110, 92, 83, 74, 65, 56, 47, 38, 29] := by
  refine ⟨?_, by decide⟩
  exact (canonicalDigits_iff [1, 2, 1]).mp (by simp [canonicalDigits, digitsBounded])

#print axioms small_targets
#print axioms two_width_121

end Agent105PredecessorControls9df76b
