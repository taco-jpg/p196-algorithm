import Agent1PeriodicPhase
import Agent1PeriodicNines
import Agent1PeriodicValidity

/-!
The retained59-phase catalog and all124 labelled edges are reified literally.
Kernel-checkable finite specifications are connected to the actual raw period.
Abstract outgoing labels are possibilities; no arbitrary path realizability
or whole-interface cycle is asserted.
-/
namespace Agent1.Periodic
open Agent8

structure PhaseEdge where
  source : Word
  clock : Nat
  carries : Option (Nat × Nat)
  target : Word
  deriving DecidableEq, Repr

/-- Original sorted indexed phase list, without rotation identifications. -/
def phaseCatalog : List Word := [
  [0,0,0,0],
  [0,0,18,18],
  [0,9,18,9],
  [0,18,18,0],
  [1,1,17,17],
  [1,17,17,1],
  [2,2,16,16],
  [2,9,16,9],
  [2,16,16,2],
  [3,3,15,15],
  [3,15,15,3],
  [4,4,14,14],
  [4,9,14,9],
  [4,14,14,4],
  [5,5,13,13],
  [5,13,13,5],
  [6,6,12,12],
  [6,9,12,9],
  [6,12,12,6],
  [7,7,11,11],
  [7,11,11,7],
  [8,8,10,10],
  [8,9,10,9],
  [8,10,10,8],
  [9,0,9,18],
  [9,2,9,16],
  [9,4,9,14],
  [9,6,9,12],
  [9,8,9,10],
  [9,9,9,9],
  [9,10,9,8],
  [9,12,9,6],
  [9,14,9,4],
  [9,16,9,2],
  [9,18,9,0],
  [10,8,8,10],
  [10,9,8,9],
  [10,10,8,8],
  [11,7,7,11],
  [11,11,7,7],
  [12,6,6,12],
  [12,9,6,9],
  [12,12,6,6],
  [13,5,5,13],
  [13,13,5,5],
  [14,4,4,14],
  [14,9,4,9],
  [14,14,4,4],
  [15,3,3,15],
  [15,15,3,3],
  [16,2,2,16],
  [16,9,2,9],
  [16,16,2,2],
  [17,1,1,17],
  [17,17,1,1],
  [18,0,0,18],
  [18,9,0,9],
  [18,18,0,0],
  [18,18,18,18]
]

/-- Original labelled edge list, including all eight all-nine labels. -/
def phaseEdges : List PhaseEdge := [
  ⟨[0,0,0,0], 0, none, [0,0,0,0]⟩,
  ⟨[0,0,0,0], 1, none, [0,0,0,0]⟩,
  ⟨[0,0,18,18], 0, none, [1,1,17,17]⟩,
  ⟨[0,0,18,18], 1, none, [9,0,9,18]⟩,
  ⟨[0,9,18,9], 0, none, [2,9,16,9]⟩,
  ⟨[0,9,18,9], 1, none, [10,10,8,8]⟩,
  ⟨[0,18,18,0], 0, none, [1,17,17,1]⟩,
  ⟨[0,18,18,0], 1, none, [0,9,18,9]⟩,
  ⟨[1,1,17,17], 0, none, [3,3,15,15]⟩,
  ⟨[1,1,17,17], 1, none, [9,2,9,16]⟩,
  ⟨[1,17,17,1], 0, none, [3,15,15,3]⟩,
  ⟨[1,17,17,1], 1, none, [2,9,16,9]⟩,
  ⟨[2,2,16,16], 0, none, [5,5,13,13]⟩,
  ⟨[2,2,16,16], 1, none, [9,4,9,14]⟩,
  ⟨[2,9,16,9], 0, none, [6,9,12,9]⟩,
  ⟨[2,9,16,9], 1, none, [12,12,6,6]⟩,
  ⟨[2,16,16,2], 0, none, [5,13,13,5]⟩,
  ⟨[2,16,16,2], 1, none, [4,9,14,9]⟩,
  ⟨[3,3,15,15], 0, none, [7,7,11,11]⟩,
  ⟨[3,3,15,15], 1, none, [9,6,9,12]⟩,
  ⟨[3,15,15,3], 0, none, [7,11,11,7]⟩,
  ⟨[3,15,15,3], 1, none, [6,9,12,9]⟩,
  ⟨[4,4,14,14], 0, none, [9,9,9,9]⟩,
  ⟨[4,4,14,14], 1, none, [9,8,9,10]⟩,
  ⟨[4,9,14,9], 0, none, [10,9,8,9]⟩,
  ⟨[4,9,14,9], 1, none, [14,14,4,4]⟩,
  ⟨[4,14,14,4], 0, none, [9,9,9,9]⟩,
  ⟨[4,14,14,4], 1, none, [8,9,10,9]⟩,
  ⟨[5,5,13,13], 0, none, [11,11,7,7]⟩,
  ⟨[5,5,13,13], 1, none, [9,10,9,8]⟩,
  ⟨[5,13,13,5], 0, none, [11,7,7,11]⟩,
  ⟨[5,13,13,5], 1, none, [10,9,8,9]⟩,
  ⟨[6,6,12,12], 0, none, [13,13,5,5]⟩,
  ⟨[6,6,12,12], 1, none, [9,12,9,6]⟩,
  ⟨[6,9,12,9], 0, none, [14,9,4,9]⟩,
  ⟨[6,9,12,9], 1, none, [16,16,2,2]⟩,
  ⟨[6,12,12,6], 0, none, [13,5,5,13]⟩,
  ⟨[6,12,12,6], 1, none, [12,9,6,9]⟩,
  ⟨[7,7,11,11], 0, none, [15,15,3,3]⟩,
  ⟨[7,7,11,11], 1, none, [9,14,9,4]⟩,
  ⟨[7,11,11,7], 0, none, [15,3,3,15]⟩,
  ⟨[7,11,11,7], 1, none, [14,9,4,9]⟩,
  ⟨[8,8,10,10], 0, none, [17,17,1,1]⟩,
  ⟨[8,8,10,10], 1, none, [9,16,9,2]⟩,
  ⟨[8,9,10,9], 0, none, [18,9,0,9]⟩,
  ⟨[8,9,10,9], 1, none, [18,18,0,0]⟩,
  ⟨[8,10,10,8], 0, none, [17,1,1,17]⟩,
  ⟨[8,10,10,8], 1, none, [16,9,2,9]⟩,
  ⟨[9,0,9,18], 0, none, [9,2,9,16]⟩,
  ⟨[9,0,9,18], 1, none, [8,10,10,8]⟩,
  ⟨[9,2,9,16], 0, none, [9,6,9,12]⟩,
  ⟨[9,2,9,16], 1, none, [6,12,12,6]⟩,
  ⟨[9,4,9,14], 0, none, [9,10,9,8]⟩,
  ⟨[9,4,9,14], 1, none, [4,14,14,4]⟩,
  ⟨[9,6,9,12], 0, none, [9,14,9,4]⟩,
  ⟨[9,6,9,12], 1, none, [2,16,16,2]⟩,
  ⟨[9,8,9,10], 0, none, [9,18,9,0]⟩,
  ⟨[9,8,9,10], 1, none, [0,18,18,0]⟩,
  ⟨[9,9,9,9], 0, some (0,0), [18,18,18,18]⟩,
  ⟨[9,9,9,9], 0, some (0,1), [9,9,9,9]⟩,
  ⟨[9,9,9,9], 0, some (1,0), [9,9,9,9]⟩,
  ⟨[9,9,9,9], 0, some (1,1), [0,0,0,0]⟩,
  ⟨[9,9,9,9], 1, some (0,0), [18,18,18,18]⟩,
  ⟨[9,9,9,9], 1, some (0,1), [9,9,9,9]⟩,
  ⟨[9,9,9,9], 1, some (1,0), [9,9,9,9]⟩,
  ⟨[9,9,9,9], 1, some (1,1), [0,0,0,0]⟩,
  ⟨[9,10,9,8], 0, none, [9,0,9,18]⟩,
  ⟨[9,10,9,8], 1, none, [18,0,0,18]⟩,
  ⟨[9,12,9,6], 0, none, [9,4,9,14]⟩,
  ⟨[9,12,9,6], 1, none, [16,2,2,16]⟩,
  ⟨[9,14,9,4], 0, none, [9,8,9,10]⟩,
  ⟨[9,14,9,4], 1, none, [14,4,4,14]⟩,
  ⟨[9,16,9,2], 0, none, [9,12,9,6]⟩,
  ⟨[9,16,9,2], 1, none, [12,6,6,12]⟩,
  ⟨[9,18,9,0], 0, none, [9,16,9,2]⟩,
  ⟨[9,18,9,0], 1, none, [10,8,8,10]⟩,
  ⟨[10,8,8,10], 0, none, [1,17,17,1]⟩,
  ⟨[10,8,8,10], 1, none, [2,9,16,9]⟩,
  ⟨[10,9,8,9], 0, none, [0,9,18,9]⟩,
  ⟨[10,9,8,9], 1, none, [0,0,18,18]⟩,
  ⟨[10,10,8,8], 0, none, [1,1,17,17]⟩,
  ⟨[10,10,8,8], 1, none, [9,2,9,16]⟩,
  ⟨[11,7,7,11], 0, none, [3,15,15,3]⟩,
  ⟨[11,7,7,11], 1, none, [4,9,14,9]⟩,
  ⟨[11,11,7,7], 0, none, [3,3,15,15]⟩,
  ⟨[11,11,7,7], 1, none, [9,4,9,14]⟩,
  ⟨[12,6,6,12], 0, none, [5,13,13,5]⟩,
  ⟨[12,6,6,12], 1, none, [6,9,12,9]⟩,
  ⟨[12,9,6,9], 0, none, [4,9,14,9]⟩,
  ⟨[12,9,6,9], 1, none, [2,2,16,16]⟩,
  ⟨[12,12,6,6], 0, none, [5,5,13,13]⟩,
  ⟨[12,12,6,6], 1, none, [9,6,9,12]⟩,
  ⟨[13,5,5,13], 0, none, [7,11,11,7]⟩,
  ⟨[13,5,5,13], 1, none, [8,9,10,9]⟩,
  ⟨[13,13,5,5], 0, none, [7,7,11,11]⟩,
  ⟨[13,13,5,5], 1, none, [9,8,9,10]⟩,
  ⟨[14,4,4,14], 0, none, [9,9,9,9]⟩,
  ⟨[14,4,4,14], 1, none, [10,9,8,9]⟩,
  ⟨[14,9,4,9], 0, none, [8,9,10,9]⟩,
  ⟨[14,9,4,9], 1, none, [4,4,14,14]⟩,
  ⟨[14,14,4,4], 0, none, [9,9,9,9]⟩,
  ⟨[14,14,4,4], 1, none, [9,10,9,8]⟩,
  ⟨[15,3,3,15], 0, none, [11,7,7,11]⟩,
  ⟨[15,3,3,15], 1, none, [12,9,6,9]⟩,
  ⟨[15,15,3,3], 0, none, [11,11,7,7]⟩,
  ⟨[15,15,3,3], 1, none, [9,12,9,6]⟩,
  ⟨[16,2,2,16], 0, none, [13,5,5,13]⟩,
  ⟨[16,2,2,16], 1, none, [14,9,4,9]⟩,
  ⟨[16,9,2,9], 0, none, [12,9,6,9]⟩,
  ⟨[16,9,2,9], 1, none, [6,6,12,12]⟩,
  ⟨[16,16,2,2], 0, none, [13,13,5,5]⟩,
  ⟨[16,16,2,2], 1, none, [9,14,9,4]⟩,
  ⟨[17,1,1,17], 0, none, [15,3,3,15]⟩,
  ⟨[17,1,1,17], 1, none, [16,9,2,9]⟩,
  ⟨[17,17,1,1], 0, none, [15,15,3,3]⟩,
  ⟨[17,17,1,1], 1, none, [9,16,9,2]⟩,
  ⟨[18,0,0,18], 0, none, [17,1,1,17]⟩,
  ⟨[18,0,0,18], 1, none, [18,9,0,9]⟩,
  ⟨[18,9,0,9], 0, none, [16,9,2,9]⟩,
  ⟨[18,9,0,9], 1, none, [8,8,10,10]⟩,
  ⟨[18,18,0,0], 0, none, [17,17,1,1]⟩,
  ⟨[18,18,0,0], 1, none, [9,18,9,0]⟩,
  ⟨[18,18,18,18], 0, none, [18,18,18,18]⟩,
  ⟨[18,18,18,18], 1, none, [18,18,18,18]⟩
]

/-- Complete labelled possibilities for one phase, with the all-nine boundary
exception separated from the boundary-independent non-nine image. -/
def phaseOutputs (w : Word) : List PhaseEdge :=
  if w = [9,9,9,9] then
    (List.range 2).flatMap fun g =>
      (List.range 2).flatMap fun a =>
        (List.range 2).map fun b =>
          ⟨w, g, some (a,b), List.replicate 4 (18-9*(a+b))⟩
  else (List.range 2).map fun g => ⟨w, g, none, phaseImage w g⟩

/-- Finite specification of the exact archived labels, not just target closure. -/
theorem phaseEdges_spec :
    phaseEdges = phaseCatalog.flatMap phaseOutputs := by decide

theorem phaseCatalog_length : phaseCatalog.length = 59 := by decide
theorem phaseCatalog_nodup : phaseCatalog.Nodup := by decide
theorem phaseEdges_length : phaseEdges.length = 124 := by decide
theorem initial_mem_phaseCatalog : [14,14,4,4] ∈ phaseCatalog := by decide

/-- The finite closure certificate checks every literal archived edge target. -/
theorem phaseEdges_targets_checked :
    phaseEdges.all (fun e => decide (e.target ∈ phaseCatalog)) = true := by decide

theorem phaseEdge_target_mem (e : PhaseEdge) (he : e ∈ phaseEdges) :
    e.target ∈ phaseCatalog := by
  have h := List.all_eq_true.mp phaseEdges_targets_checked e he
  exact of_decide_eq_true h

/-- Every actual raw period transition from a catalog phase has an archived
edge with its actual clock and, in the exceptional case, actual entry bits. -/
theorem rawPeriod_catalog_edge (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) (hmem : w ∈ phaseCatalog) :
    ∃ e, e ∈ phaseEdges ∧ e.source = w ∧ e.clock = rawGamma B H w ∧
      e.target = rawPeriod B H w := by
  have hg : rawGamma B H w < 2 := by
    have h := scan_carry_le_one B H w hB hH hw
    change rawGamma B H w ≤ 1 at h
    omega
  by_cases hn : w = [9,9,9,9]
  · subst w
    let a := leftEntry B
    let b := rightEntry B H [9,9,9,9]
    have hab := nines_entry_bits B H hB hH
    have ha : a < 2 := by dsimp [a]; omega
    have hb : b < 2 := by dsimp [b]; omega
    let e : PhaseEdge := ⟨[9,9,9,9], rawGamma B H [9,9,9,9],
      some (a,b), List.replicate 4 (18-9*(a+b))⟩
    refine ⟨e, ?_, rfl, rfl, ?_⟩
    · rw [phaseEdges_spec]
      apply List.mem_flatMap.mpr
      refine ⟨[9,9,9,9], hmem, ?_⟩
      simp only [phaseOutputs, ↓reduceIte]
      apply List.mem_flatMap.mpr
      refine ⟨rawGamma B H [9,9,9,9], List.mem_range.mpr hg, ?_⟩
      apply List.mem_flatMap.mpr
      refine ⟨a, List.mem_range.mpr ha, ?_⟩
      exact List.mem_map.mpr ⟨b, List.mem_range.mpr hb, rfl⟩
    · exact (rawPeriod_nines B H hB hH).symm
  · let e : PhaseEdge := ⟨w, rawGamma B H w, none, phaseImage w (rawGamma B H w)⟩
    refine ⟨e, ?_, rfl, rfl, (rawPeriod_eq_phaseImage B H w hB hH hw hlen hn).symm⟩
    rw [phaseEdges_spec]
    apply List.mem_flatMap.mpr
    refine ⟨w, hmem, ?_⟩
    simp only [phaseOutputs, hn, ↓reduceIte]
    exact List.mem_map.mpr ⟨rawGamma B H w, List.mem_range.mpr hg, rfl⟩

/-- Actual period extraction remains in the checked finite catalog. -/
theorem rawPeriod_mem_phaseCatalog (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) (hmem : w ∈ phaseCatalog) :
    rawPeriod B H w ∈ phaseCatalog := by
  obtain ⟨e, he, _, _, ht⟩ := rawPeriod_catalog_edge B H w hB hH hw hlen hmem
  rw [← ht]
  exact phaseEdge_target_mem e he

/-- Full original quotient validity and its catalog period are preserved
together; the actual quotient interfaces remain unbounded data. -/
theorem quotient_valid_in_phaseCatalog (B H w : Word)
    (hv : ValidPeriodic B H w) (hmem : w ∈ phaseCatalog) :
    ValidPeriodic (quotientOuter B H w) (quotientCenter B H w) (rawPeriod B H w) ∧
      rawPeriod B H w ∈ phaseCatalog :=
  ⟨quotient_valid B H w hv, rawPeriod_mem_phaseCatalog B H w hv.outer_bounded
    hv.center_bounded hv.period_bounded hv.period_length hmem⟩

end Agent1.Periodic
#print axioms Agent1.Periodic.phaseEdges_spec
#print axioms Agent1.Periodic.phaseCatalog_length
#print axioms Agent1.Periodic.phaseCatalog_nodup
#print axioms Agent1.Periodic.phaseEdges_length
#print axioms Agent1.Periodic.initial_mem_phaseCatalog
#print axioms Agent1.Periodic.phaseEdges_targets_checked
#print axioms Agent1.Periodic.phaseEdge_target_mem
#print axioms Agent1.Periodic.rawPeriod_catalog_edge
#print axioms Agent1.Periodic.rawPeriod_mem_phaseCatalog
#print axioms Agent1.Periodic.quotient_valid_in_phaseCatalog
