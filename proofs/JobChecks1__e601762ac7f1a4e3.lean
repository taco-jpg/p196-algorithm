import JobData1
import RangeChecks
import JobData0
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_1_0 : ∀ i : Fin 128, VertexRow ranking1 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_1_1 : ∀ i : Fin 5, VertexRow ranking1 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_1_all : ∀ u, 0 ≤ u → u < 133 → VertexRow ranking1 u :=
  (join_ranges (fun u => VertexRow ranking1 u) 0 128 133 (checked_range (fun u => VertexRow ranking1 u) 0 128 vertex_1_0) (checked_range (fun u => VertexRow ranking1 u) 128 5 vertex_1_1))
theorem edge_1_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data1 ranking1 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_1_1 : ∀ i : Fin 5, ∀ bit : Fin 2, EdgeRow data1 ranking1 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_1_all : ∀ u, 0 ≤ u → u < 133 → ∀ bit : Fin 2, EdgeRow data1 ranking1 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data1 ranking1 u bit.val) 0 128 133 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data1 ranking1 u bit.val) 0 128 edge_1_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data1 ranking1 u bit.val) 128 5 edge_1_1))
theorem checked_rank1 : CheckedRank data1 ranking1 := by
  constructor
  · intro u hu
    exact vertex_1_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_1_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_1_0 : ∀ i : Fin 7, CoverageRow data0 component0 0 7 member1 memberIndex1 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_1_all : ∀ u, 0 ≤ u → u < 7 → CoverageRow data0 component0 0 7 member1 memberIndex1 u :=
  (checked_range (fun u => CoverageRow data0 component0 0 7 member1 memberIndex1 u) 0 7 coverage_1_0)
theorem field_1_0 : ∀ i : Fin 128, FieldRow data0 data1 member1 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_1_1 : ∀ i : Fin 5, FieldRow data0 data1 member1 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_1_all : ∀ u, 0 ≤ u → u < 133 → FieldRow data0 data1 member1 u :=
  (join_ranges (fun u => FieldRow data0 data1 member1 u) 0 128 133 (checked_range (fun u => FieldRow data0 data1 member1 u) 0 128 field_1_0) (checked_range (fun u => FieldRow data0 data1 member1 u) 128 5 field_1_1))
theorem lift_1_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data0 data1 component0 0 member1 memberIndex1 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_1_1 : ∀ i : Fin 5, ∀ bit : Fin 2, LiftRow data0 data1 component0 0 member1 memberIndex1 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_1_all : ∀ u, 0 ≤ u → u < 133 → ∀ bit : Fin 2, LiftRow data0 data1 component0 0 member1 memberIndex1 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data0 data1 component0 0 member1 memberIndex1 u bit.val) 0 128 133 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data0 data1 component0 0 member1 memberIndex1 u bit.val) 0 128 lift_1_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data0 data1 component0 0 member1 memberIndex1 u bit.val) 128 5 lift_1_1))
def lift_certificate1 : LiftCertificate data0 data1 component0 0 where
  members := member1
  memberIndex := memberIndex1
  count := 7
  size_eq := rfl
  coverage u hu := coverage_1_all u (Nat.zero_le u) hu
  fields u hu := field_1_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_1_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete1 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data0)
      (fun v => component0 v=0)))) (graph data1)
      (encode lift_certificate1) := lift_realization lift_certificate1
end ScalarJobData
