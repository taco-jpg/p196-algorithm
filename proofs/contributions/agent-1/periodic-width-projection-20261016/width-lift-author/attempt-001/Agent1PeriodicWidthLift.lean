import Agent1PeriodicOuterCatalog
import Agent1PeriodicWidth

/-!
The compositional width-modulo-eight lift of the original outer/phase catalog.
Each lifted edge keeps its original clock and exceptional carry label. The
actual maximally stripped quotient projects to this finite necessary model.
The list lengths below do not assert reachability, SCCs, saved traversal order,
or realization of an arbitrary abstract path by finite decimal words.
-/

namespace Agent1.Periodic

open Agent8

abbrev WidthNode := OuterNode × Nat

structure WidthEdge where
  source : WidthNode
  clock : Nat
  carries : Option (Nat × Nat)
  target : WidthNode
  deriving DecidableEq, Repr

/-- All eight residues over each original node, in compositional list order. -/
def widthCatalog : List WidthNode :=
  outerCatalog.flatMap (fun s => (List.range 8).map (fun r => (s, r)))

/-- The clock advances the width residue; the other labels are unchanged. -/
def liftOuterEdge (e : OuterEdge) (r : Nat) : WidthEdge :=
  ⟨(e.source, r), e.clock, e.carries, (e.target, (r + e.clock) % 8)⟩

def widthEdges : List WidthEdge :=
  outerEdges.flatMap (fun e => (List.range 8).map (liftOuterEdge e))

/-- Physical head, indexed phase, and exact interface-width residue. -/
def widthProjection (B H w : Word) : WidthNode :=
  ((w, outside B w), widthResidue B H)

private theorem length_eight_lift {α β : Type} (xs : List α) (f : α → Nat → β) :
    (xs.flatMap (fun x => (List.range 8).map (f x))).length = xs.length * 8 := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_map,
      List.length_range, List.length_cons, ih]
    omega

/-- These counts use the already checked base lists, without a new graph search. -/
theorem widthCatalog_length : widthCatalog.length = 7024 := by
  rw [widthCatalog, length_eight_lift, outerCatalog_length]

theorem widthEdges_length : widthEdges.length = 11664 := by
  rw [widthEdges, length_eight_lift, outerEdges_length]

theorem mem_widthCatalog_iff (s : OuterNode) (r : Nat) :
    (s, r) ∈ widthCatalog ↔ s ∈ outerCatalog ∧ r < 8 := by
  constructor
  · intro h
    obtain ⟨s', hs', hr⟩ := List.mem_flatMap.mp h
    obtain ⟨r', hr', heq⟩ := List.mem_map.mp hr
    obtain ⟨rfl, rfl⟩ := Prod.mk.inj heq
    exact ⟨hs', List.mem_range.mp hr'⟩
  · rintro ⟨hs, hr⟩
    exact List.mem_flatMap.mpr
      ⟨s, hs, List.mem_map.mpr ⟨r, List.mem_range.mpr hr, rfl⟩⟩

theorem liftOuterEdge_mem (e : OuterEdge) (he : e ∈ outerEdges)
    (r : Nat) (hr : r < 8) : liftOuterEdge e r ∈ widthEdges :=
  List.mem_flatMap.mpr
    ⟨e, he, List.mem_map.mpr ⟨r, List.mem_range.mpr hr, rfl⟩⟩

/-- Every lifted edge has a listed target with a valid residue. -/
theorem widthEdge_target_mem (e : WidthEdge) (he : e ∈ widthEdges) :
    e.target ∈ widthCatalog := by
  obtain ⟨base, hbase, hr⟩ := List.mem_flatMap.mp he
  obtain ⟨r, _, rfl⟩ := List.mem_map.mp hr
  exact (mem_widthCatalog_iff base.target ((r + base.clock) % 8)).mpr
    ⟨outerEdge_target_mem base hbase, Nat.mod_lt _ (by decide)⟩

/-- The actual quotient projects to a stored lifted edge with the same actual
clock and exceptional all-nine carry label. -/
theorem quotient_width_catalog_edge (B H w : Word)
    (hv : ValidPeriodic B H w) (hs : widthProjection B H w ∈ widthCatalog) :
    ∃ e, e ∈ widthEdges ∧ e.source = widthProjection B H w ∧
      e.clock = rawGamma B H w ∧
      e.carries = (if w = [9,9,9,9] then
        some (leftEntry B, rightEntry B H w) else none) ∧
      e.target = widthProjection (quotientOuter B H w)
        (quotientCenter B H w) (rawPeriod B H w) := by
  have hbase : (w, outside B w) ∈ outerCatalog :=
    ((mem_widthCatalog_iff _ _).mp hs).1
  obtain ⟨e, he, hsource, hclock, hcarries, htarget⟩ :=
    quotient_outer_catalog_edge B H w hv hbase
  refine ⟨liftOuterEdge e (widthResidue B H),
    liftOuterEdge_mem e he _ (widthResidue_lt B H), ?_, hclock, hcarries, ?_⟩
  · change (e.source, widthResidue B H) = ((w, outside B w), widthResidue B H)
    rw [hsource]
  · change (e.target, (widthResidue B H + e.clock) % 8) =
      ((rawPeriod B H w, outside (quotientOuter B H w) (rawPeriod B H w)),
        widthResidue (quotientOuter B H w) (quotientCenter B H w))
    rw [htarget, hclock, ← quotient_widthResidue B H w hv.outer_bounded
      hv.center_bounded hv.period_bounded hv.period_length]

/-- Complete original validity and lifted catalog membership are preserved
together. No abstract edge is asserted to admit a finite-word realization. -/
theorem quotient_valid_in_widthCatalog (B H w : Word)
    (hv : ValidPeriodic B H w) (hs : widthProjection B H w ∈ widthCatalog) :
    ValidPeriodic (quotientOuter B H w) (quotientCenter B H w) (rawPeriod B H w) ∧
      widthProjection (quotientOuter B H w) (quotientCenter B H w)
        (rawPeriod B H w) ∈ widthCatalog := by
  refine ⟨quotient_valid B H w hv, ?_⟩
  obtain ⟨e, he, _, _, _, htarget⟩ := quotient_width_catalog_edge B H w hv hs
  rw [← htarget]
  exact widthEdge_target_mem e he

end Agent1.Periodic

#print axioms Agent1.Periodic.widthCatalog_length
#print axioms Agent1.Periodic.widthEdges_length
#print axioms Agent1.Periodic.mem_widthCatalog_iff
#print axioms Agent1.Periodic.liftOuterEdge_mem
#print axioms Agent1.Periodic.widthEdge_target_mem
#print axioms Agent1.Periodic.quotient_width_catalog_edge
#print axioms Agent1.Periodic.quotient_valid_in_widthCatalog
