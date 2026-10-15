import JobData4
import RangeChecks
import JobData2
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_4_0 : ∀ i : Fin 128, VertexRow ranking4 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_1 : ∀ i : Fin 128, VertexRow ranking4 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_2 : ∀ i : Fin 105, VertexRow ranking4 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_all : ∀ u, 0 ≤ u → u < 361 → VertexRow ranking4 u :=
  (join_ranges (fun u => VertexRow ranking4 u) 0 128 361 (checked_range (fun u => VertexRow ranking4 u) 0 128 vertex_4_0) (join_ranges (fun u => VertexRow ranking4 u) 128 256 361 (checked_range (fun u => VertexRow ranking4 u) 128 128 vertex_4_1) (checked_range (fun u => VertexRow ranking4 u) 256 105 vertex_4_2)))
theorem edge_4_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_2 : ∀ i : Fin 105, ∀ bit : Fin 2, EdgeRow data4 ranking4 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_all : ∀ u, 0 ≤ u → u < 361 → ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 0 128 361 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 0 128 edge_4_0) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 128 256 361 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 128 128 edge_4_1) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 256 105 edge_4_2)))
theorem checked_rank4 : CheckedRank data4 ranking4 := by
  constructor
  · intro u hu
    exact vertex_4_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_4_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_4_0 : ∀ i : Fin 128, CoverageRow data2 component2 278 19 member4 memberIndex4 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_4_1 : ∀ i : Fin 128, CoverageRow data2 component2 278 19 member4 memberIndex4 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_4_2 : ∀ i : Fin 128, CoverageRow data2 component2 278 19 member4 memberIndex4 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_4_3 : ∀ i : Fin 72, CoverageRow data2 component2 278 19 member4 memberIndex4 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_4_all : ∀ u, 0 ≤ u → u < 456 → CoverageRow data2 component2 278 19 member4 memberIndex4 u :=
  (join_ranges (fun u => CoverageRow data2 component2 278 19 member4 memberIndex4 u) 0 256 456 (join_ranges (fun u => CoverageRow data2 component2 278 19 member4 memberIndex4 u) 0 128 256 (checked_range (fun u => CoverageRow data2 component2 278 19 member4 memberIndex4 u) 0 128 coverage_4_0) (checked_range (fun u => CoverageRow data2 component2 278 19 member4 memberIndex4 u) 128 128 coverage_4_1)) (join_ranges (fun u => CoverageRow data2 component2 278 19 member4 memberIndex4 u) 256 384 456 (checked_range (fun u => CoverageRow data2 component2 278 19 member4 memberIndex4 u) 256 128 coverage_4_2) (checked_range (fun u => CoverageRow data2 component2 278 19 member4 memberIndex4 u) 384 72 coverage_4_3)))
theorem field_4_0 : ∀ i : Fin 128, FieldRow data2 data4 member4 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_4_1 : ∀ i : Fin 128, FieldRow data2 data4 member4 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_4_2 : ∀ i : Fin 105, FieldRow data2 data4 member4 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_4_all : ∀ u, 0 ≤ u → u < 361 → FieldRow data2 data4 member4 u :=
  (join_ranges (fun u => FieldRow data2 data4 member4 u) 0 128 361 (checked_range (fun u => FieldRow data2 data4 member4 u) 0 128 field_4_0) (join_ranges (fun u => FieldRow data2 data4 member4 u) 128 256 361 (checked_range (fun u => FieldRow data2 data4 member4 u) 128 128 field_4_1) (checked_range (fun u => FieldRow data2 data4 member4 u) 256 105 field_4_2)))
theorem lift_4_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_2 : ∀ i : Fin 105, ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_all : ∀ u, 0 ≤ u → u < 361 → ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 u bit.val) 0 128 361 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 u bit.val) 0 128 lift_4_0) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 u bit.val) 128 256 361 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 u bit.val) 128 128 lift_4_1) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data2 data4 component2 278 member4 memberIndex4 u bit.val) 256 105 lift_4_2)))
def lift_certificate4 : LiftCertificate data2 data4 component2 278 where
  members := member4
  memberIndex := memberIndex4
  count := 19
  size_eq := rfl
  coverage u hu := coverage_4_all u (Nat.zero_le u) hu
  fields u hu := field_4_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_4_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete4 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data2)
      (fun v => component2 v=278)))) (graph data4)
      (encode lift_certificate4) := lift_realization lift_certificate4
end ScalarJobData
