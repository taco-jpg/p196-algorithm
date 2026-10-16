import Agent1PeriodicPhaseCatalog

/-!
Literal phase/exterior product choices, retaining every original phase label.
The enumerated carry bits are possibilities only; no independent choice of
these bits or realizability of an arbitrary edge path is asserted.
-/

namespace Agent1.Periodic

open Agent8

abbrev OuterNode := Word × Nat

structure OuterEdge where
  source : OuterNode
  clock : Nat
  carries : Option (Nat × Nat)
  target : OuterNode
  deriving DecidableEq, Repr

/-- Images of the two carry bits compatible with the specified clock,
deduplicated in their original enumeration order. -/
def outerImages (q g : Nat) : List Nat :=
  ((List.range 2).filterMap (fun e =>
    if Agent8.overflow q e = g then some (Agent8.nextExterior q e) else none)).eraseDups

/-- Each original labelled phase edge is paired with its compatible exterior
images. Distinct phase carry labels remain distinct edges. -/
def outerOutputs (s : OuterNode) : List OuterEdge :=
  (phaseEdges.filter (fun e => decide (e.source = s.1))).flatMap (fun e =>
    (outerImages s.2 e.clock).map (fun q' =>
      ⟨s, e.clock, e.carries, (e.target, q')⟩))

/-- The actual incoming bit's exterior image occurs under its actual clock. -/
theorem mem_outerImages_of_actual (q e : Nat) (he : e ≤ 1) :
    Agent8.nextExterior q e ∈ outerImages q (Agent8.overflow q e) := by
  have hc : e = 0 ∨ e = 1 := by omega
  rcases hc with rfl | rfl
  all_goals
    by_cases hclock : Agent8.overflow q 0 = Agent8.overflow q 1
    all_goals
      by_cases himage : Agent8.nextExterior q 0 = Agent8.nextExterior q 1
      all_goals
        simp_all [outerImages, List.range_succ, List.eraseDups,
          List.eraseDups.loop, List.elem, beq_false_of_ne, eq_comm]

/-- A retained phase edge and a compatible exterior image construct exactly
the stated labelled product edge in the literal output enumeration. -/
theorem outerOutputs_mem_of_phaseEdge (s : OuterNode) (e : PhaseEdge)
    (he : e ∈ phaseEdges) (hsource : e.source = s.1) (q' : Nat)
    (hq : q' ∈ outerImages s.2 e.clock) :
    (⟨s, e.clock, e.carries, (e.target, q')⟩ : OuterEdge) ∈ outerOutputs s := by
  unfold outerOutputs
  apply List.mem_flatMap.mpr
  refine ⟨e, ?_, ?_⟩
  · exact List.mem_filter.mpr ⟨he, by simp [hsource]⟩
  · exact List.mem_map.mpr ⟨q', hq, rfl⟩

end Agent1.Periodic

#print axioms Agent1.Periodic.mem_outerImages_of_actual
#print axioms Agent1.Periodic.outerOutputs_mem_of_phaseEdge
