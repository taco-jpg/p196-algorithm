import P196.Drafts.D20261015ScalarHierarchyReviewSourceSnapshots.ScalarPeriods
import P196.Drafts.D20261015ScalarFiniteCertificateFormalPilotArray.JobData0

/-! Exact correspondence of the semantic seven-phase root with finite job
zero. This verifies the encoding only; it does not supply the hierarchy bound. -/

namespace RootBridge

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory ActualPrefixLift
open ScalarFinite ScalarJobData

theorem root_edge_label_bound (u v : Fin 7) (c : Nat)
    (he : ScalarRoot.root.edge u v c) : c ≤ 1 := by
  simp only [ScalarRoot.root, ScalarRoot.rootEdges, List.mem_cons, List.not_mem_nil,
    or_false, Prod.mk.injEq] at he
  rcases he with h | h | h | h | h | h | h | h | h | h <;> omega

theorem root_fields_checked : ∀ p : Fin 7,
    data0.phase p.val = ScalarRoot.root.phase p ∧
    data0.last p.val = ScalarRoot.root.last p ∧
    data0.low p.val = ScalarRoot.root.low p := by
  unfold ScalarRoot.root
  decide

theorem root_edges_checked : ∀ u v : Fin 7, ∀ c : Fin 2,
    ScalarRoot.root.edge u v c.val → (graph data0).edge u.val v.val c.val := by
  unfold ScalarRoot.root graph
  decide

theorem root_realization : Realization ScalarRoot.root (graph data0) Fin.val := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro p _
    exact p.isLt
  · intro p _
    exact (root_fields_checked p).1
  · intro p _
    exact (root_fields_checked p).2.1
  · intro p _
    exact (root_fields_checked p).2.2
  · intro u v c _ _ he
    have hb := root_edge_label_bound u v c he
    exact root_edges_checked u v ⟨c, by omega⟩ he

/-- The finite instance can target job zero directly. Once its path bound
is proved, this bridge discharges the wrappers' exact root certificate. -/
theorem certificate_of_finite_root_bound
    (hbound : ∀ (q : Nat → Nat) (L a s n : Nat) (path : Nat → Nat),
      Admissible L q → 14 ≤ L → ActualPath (graph data0) q L 1 a s path n → n ≤ 659) :
    ScalarPeriods.RootVertexCertificate := by
  intro q L a s n path ha hL hp
  have hencoded := ActualPrefixLift.actual_path_encode ScalarRoot.root (graph data0)
    Fin.val root_realization q L 1 a s n path hp
  exact hbound q L a s n (fun i => (path i).val) ha hL hencoded

end RootBridge
