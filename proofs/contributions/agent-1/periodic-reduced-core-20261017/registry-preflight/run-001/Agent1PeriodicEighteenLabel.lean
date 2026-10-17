import Agent1PeriodicOuterRank

/-!
The preserved total component-label definition assigns label130 only to
the constant-eighteen phase. This structural converse needs no catalog
membership premise and introduces no new finite graph certificate.
-/

set_option maxHeartbeats 1600000

namespace Agent1.Periodic

theorem outerComponent_eighteen_phase (s : OuterNode)
    (hc : outerComponent s = 130) : s.1 = [18,18,18,18] := by
  rcases s with ⟨w, a⟩
  delta outerComponent at hc
  trace "AFTER_DELTA"
  split at hc <;>
    first
    | assumption
    | rfl
    | contradiction
    | (split at hc <;> contradiction)

end Agent1.Periodic

#print axioms Agent1.Periodic.outerComponent_eighteen_phase
