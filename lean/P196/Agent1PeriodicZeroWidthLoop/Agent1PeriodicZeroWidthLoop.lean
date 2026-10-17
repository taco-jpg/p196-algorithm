import P196.Agent1PeriodicWidthProjection.Agent1PeriodicWidthLift
import P196.Agent1PeriodicZeroWidthLoop.Agent1PeriodicZeroPath

/-!
A concrete sixteen-edge closed walk in the existing necessary width model,
through the projection of an original-valid, positively realizable template.
The existing full zero-period no-return theorem still applies. Membership
of the chosen abstract edges does not assert that an actual quotient orbit
follows them: outside nine also has a different listed clock-one edge.
-/

namespace Agent1.Periodic
open Agent8

private def zeroWidthBase0 : OuterEdge :=
  ⟨([0,0,0,0],9), 0, none, ([0,0,0,0],18)⟩

private def zeroWidthBase1 : OuterEdge :=
  ⟨([0,0,0,0],18), 1, none, ([0,0,0,0],9)⟩

private theorem zeroWidthBase0_mem : zeroWidthBase0 ∈ outerEdges := by decide
private theorem zeroWidthBase1_mem : zeroWidthBase1 ∈ outerEdges := by decide

/-- The displayed walk starts at interface-width residue two. -/
def zeroWidthNode (t : Nat) : WidthNode :=
  (([0,0,0,0], if t % 2 = 0 then 9 else 18), (2 + t / 2) % 8)

/-- Its selected base edges alternate clock zero and clock one. -/
def zeroWidthEdge (t : Nat) : WidthEdge :=
  liftOuterEdge (if t % 2 = 0 then zeroWidthBase0 else zeroWidthBase1)
    ((2 + t / 2) % 8)

/-- Every selected edge belongs to the unchanged labelled width-edge list. -/
theorem zeroWidthEdge_mem (t : Nat) : zeroWidthEdge t ∈ widthEdges := by
  apply liftOuterEdge_mem
  · split
    · exact zeroWidthBase0_mem
    · exact zeroWidthBase1_mem
  · exact Nat.mod_lt _ (by decide)

/-- Exact sources, targets, clocks, and carry labels for all sixteen edges. -/
theorem zeroWidthEdge_labels (t : Nat) (ht : t < 16) :
    (zeroWidthEdge t).source = zeroWidthNode t ∧
    (zeroWidthEdge t).target = zeroWidthNode (t+1) ∧
    (zeroWidthEdge t).clock = t % 2 ∧
    (zeroWidthEdge t).carries = none := by
  have h : ∀ i : Fin 16,
      (zeroWidthEdge i.val).source = zeroWidthNode i.val ∧
      (zeroWidthEdge i.val).target = zeroWidthNode (i.val+1) ∧
      (zeroWidthEdge i.val).clock = i.val % 2 ∧
      (zeroWidthEdge i.val).carries = none := by decide
  exact h ⟨t, ht⟩

/-- All displayed vertices, including the endpoint, are catalog members. -/
theorem zeroWidthNode_mem (t : Nat) : zeroWidthNode t ∈ widthCatalog := by
  apply (mem_widthCatalog_iff _ _).mpr
  refine ⟨?_, Nat.mod_lt _ (by decide)⟩
  change ([0,0,0,0], if t % 2 = 0 then 9 else 18) ∈ outerCatalog
  split <;> decide

theorem zeroWidthNode_closed : zeroWidthNode 16 = zeroWidthNode 0 := by decide

/-- Exactly eight selected edges have overflow clock one. -/
theorem zeroWidthEdge_clock_sum :
    ((List.range 16).map (fun t => (zeroWidthEdge t).clock)).sum = 8 := by decide

/-- Original validity, including positive exterior and middle parity. -/
theorem zeroWidthLoop_initial_valid : ValidPeriodic [9] [] [0,0,0,0] := by
  constructor
  · simp [Bounded]
  · simp [Bounded]
  · simp [Bounded]
  · rfl
  · rfl
  · simp
  · decide

theorem zeroWidthLoop_initial_projection :
    widthProjection [9] [] [0,0,0,0] = zeroWidthNode 0 := by rfl

/-- Only the initial template at copy count three is realized here. -/
theorem zeroWidthLoop_initial_realizable :
    ∃ n d, 0 < n ∧
      DecimalDigits.Canonical n d (periodicWord [9] [] [0,0,0,0] 3).length ∧
      ∀ i, i < (periodicWord [9] [] [0,0,0,0] 3).length →
        DecimalDigits.columnSum d (periodicWord [9] [] [0,0,0,0] 3).length i =
          ((periodicWord [9] [] [0,0,0,0] 3)[i]?).getD 0 :=
  periodicWord_realizable [9] [] [0,0,0,0] 3 zeroWidthLoop_initial_valid (by decide)

/-- The complete labelled closed-walk certificate in the finite projection. -/
theorem zeroWidthLoop_certificate :
    (∀ t, t < 16 → zeroWidthEdge t ∈ widthEdges ∧
      (zeroWidthEdge t).source = zeroWidthNode t ∧
      (zeroWidthEdge t).target = zeroWidthNode (t+1) ∧
      (zeroWidthEdge t).clock = t % 2 ∧ (zeroWidthEdge t).carries = none) ∧
    (∀ t, t ≤ 16 → zeroWidthNode t ∈ widthCatalog) ∧
    zeroWidthNode 16 = zeroWidthNode 0 ∧
    ((List.range 16).map (fun t => (zeroWidthEdge t).clock)).sum = 8 := by
  exact ⟨fun t ht => ⟨zeroWidthEdge_mem t, zeroWidthEdge_labels t ht⟩,
    fun t _ => zeroWidthNode_mem t, zeroWidthNode_closed, zeroWidthEdge_clock_sum⟩

/-- Even though the initial projection lies on that closed walk, every
positive exact full quotient path from this original-valid tuple fails to
return. This does not claim the full path follows the displayed edges. -/
theorem zeroWidthLoop_no_full_return (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hB : B 0 = [9]) (hH : H 0 = [])
    (hw : w 0 = [0,0,0,0]) (hN : 0 < N) :
    ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0) := by
  have hv : ValidPeriodic (B 0) (H 0) (w 0) := by
    rw [hB, hH, hw]
    exact zeroWidthLoop_initial_valid
  exact quotient_path_zero_no_return B H w N hp hv hw hN

/-- A canonically realizable initial projection has the explicit finite
closed walk, but cannot have a positive complete zero-tuple return. The two
statements are side by side; no abstract-walk realization is asserted. -/
theorem zeroWidthLoop_projection_not_sufficient :
    widthProjection [9] [] [0,0,0,0] = zeroWidthNode 0 ∧
    zeroWidthNode 16 = zeroWidthNode 0 ∧
    (∀ t, t < 16 → zeroWidthEdge t ∈ widthEdges ∧
      (zeroWidthEdge t).source = zeroWidthNode t ∧
      (zeroWidthEdge t).target = zeroWidthNode (t+1)) ∧
    (∃ n d, 0 < n ∧
      DecimalDigits.Canonical n d (periodicWord [9] [] [0,0,0,0] 3).length ∧
      ∀ i, i < (periodicWord [9] [] [0,0,0,0] 3).length →
        DecimalDigits.columnSum d (periodicWord [9] [] [0,0,0,0] 3).length i =
          ((periodicWord [9] [] [0,0,0,0] 3)[i]?).getD 0) ∧
    (∀ (B H w : Nat → Word) (N : Nat), QuotientPath B H w N →
      B 0 = [9] → H 0 = [] → w 0 = [0,0,0,0] → 0 < N →
      ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0)) := by
  refine ⟨zeroWidthLoop_initial_projection, zeroWidthNode_closed, ?_,
    zeroWidthLoop_initial_realizable, zeroWidthLoop_no_full_return⟩
  intro t ht
  have h := zeroWidthEdge_labels t ht
  exact ⟨zeroWidthEdge_mem t, h.1, h.2.1⟩

end Agent1.Periodic

#print axioms Agent1.Periodic.zeroWidthEdge_mem
#print axioms Agent1.Periodic.zeroWidthEdge_labels
#print axioms Agent1.Periodic.zeroWidthNode_mem
#print axioms Agent1.Periodic.zeroWidthNode_closed
#print axioms Agent1.Periodic.zeroWidthEdge_clock_sum
#print axioms Agent1.Periodic.zeroWidthLoop_initial_valid
#print axioms Agent1.Periodic.zeroWidthLoop_initial_projection
#print axioms Agent1.Periodic.zeroWidthLoop_initial_realizable
#print axioms Agent1.Periodic.zeroWidthLoop_certificate
#print axioms Agent1.Periodic.zeroWidthLoop_no_full_return
#print axioms Agent1.Periodic.zeroWidthLoop_projection_not_sufficient
