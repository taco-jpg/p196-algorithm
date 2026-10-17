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
  rcases w with _ | ⟨x0, _ | ⟨x1, _ | ⟨x2, _ | ⟨x3, _ | ⟨x4, xs⟩⟩⟩⟩⟩ <;>
    delta outerComponent outerComponent.match_9 at hc <;>
    dsimp only at hc
  all_goals
    repeat first
      | contradiction
      | rfl
      | (progress simp_all only [Prod.fst])
      | (split at hc)


end Agent1.Periodic

#print axioms Agent1.Periodic.outerComponent_eighteen_phase
