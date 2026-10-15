import BJobData4
import RangeChecks
import BJobData3
namespace BroaderJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_4_0 : ∀ i : Fin 128, VertexRow ranking4 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_1 : ∀ i : Fin 128, VertexRow ranking4 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_2 : ∀ i : Fin 128, VertexRow ranking4 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_3 : ∀ i : Fin 128, VertexRow ranking4 (384+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_4 : ∀ i : Fin 128, VertexRow ranking4 (512+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_5 : ∀ i : Fin 128, VertexRow ranking4 (640+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_6 : ∀ i : Fin 128, VertexRow ranking4 (768+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_7 : ∀ i : Fin 54, VertexRow ranking4 (896+i.val) := by
  unfold VertexRow
  decide

theorem vertex_4_all : ∀ u, 0 ≤ u → u < 950 → VertexRow ranking4 u :=
  (join_ranges (fun u => VertexRow ranking4 u) 0 512 950 (join_ranges (fun u => VertexRow ranking4 u) 0 256 512 (join_ranges (fun u => VertexRow ranking4 u) 0 128 256 (checked_range (fun u => VertexRow ranking4 u) 0 128 vertex_4_0) (checked_range (fun u => VertexRow ranking4 u) 128 128 vertex_4_1)) (join_ranges (fun u => VertexRow ranking4 u) 256 384 512 (checked_range (fun u => VertexRow ranking4 u) 256 128 vertex_4_2) (checked_range (fun u => VertexRow ranking4 u) 384 128 vertex_4_3))) (join_ranges (fun u => VertexRow ranking4 u) 512 768 950 (join_ranges (fun u => VertexRow ranking4 u) 512 640 768 (checked_range (fun u => VertexRow ranking4 u) 512 128 vertex_4_4) (checked_range (fun u => VertexRow ranking4 u) 640 128 vertex_4_5)) (join_ranges (fun u => VertexRow ranking4 u) 768 896 950 (checked_range (fun u => VertexRow ranking4 u) 768 128 vertex_4_6) (checked_range (fun u => VertexRow ranking4 u) 896 54 vertex_4_7))))
theorem edge_4_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_2 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_3 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (384+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_4 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (512+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_5 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (640+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_6 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data4 ranking4 (768+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_7 : ∀ i : Fin 54, ∀ bit : Fin 2, EdgeRow data4 ranking4 (896+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_4_all : ∀ u, 0 ≤ u → u < 950 → ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 0 512 950 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 0 128 edge_4_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 128 128 edge_4_1)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 256 128 edge_4_2) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 384 128 edge_4_3))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 512 768 950 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 512 128 edge_4_4) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 640 128 edge_4_5)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 768 896 950 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 768 128 edge_4_6) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data4 ranking4 u bit.val) 896 54 edge_4_7))))
theorem checked_rank4 : CheckedRank data4 ranking4 := by
  constructor
  · intro u hu
    exact vertex_4_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_4_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_4_0 : ∀ i : Fin 128, CoverageRow data3 component3 117 50 member4 memberIndex4 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_4_1 : ∀ i : Fin 119, CoverageRow data3 component3 117 50 member4 memberIndex4 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_4_all : ∀ u, 0 ≤ u → u < 247 → CoverageRow data3 component3 117 50 member4 memberIndex4 u :=
  (join_ranges (fun u => CoverageRow data3 component3 117 50 member4 memberIndex4 u) 0 128 247 (checked_range (fun u => CoverageRow data3 component3 117 50 member4 memberIndex4 u) 0 128 coverage_4_0) (checked_range (fun u => CoverageRow data3 component3 117 50 member4 memberIndex4 u) 128 119 coverage_4_1))
theorem field_4_0 : ∀ i : Fin 128, FieldRow data3 data4 member4 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_4_1 : ∀ i : Fin 128, FieldRow data3 data4 member4 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_4_2 : ∀ i : Fin 128, FieldRow data3 data4 member4 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_4_3 : ∀ i : Fin 128, FieldRow data3 data4 member4 (384+i.val) := by
  unfold FieldRow
  decide

theorem field_4_4 : ∀ i : Fin 128, FieldRow data3 data4 member4 (512+i.val) := by
  unfold FieldRow
  decide

theorem field_4_5 : ∀ i : Fin 128, FieldRow data3 data4 member4 (640+i.val) := by
  unfold FieldRow
  decide

theorem field_4_6 : ∀ i : Fin 128, FieldRow data3 data4 member4 (768+i.val) := by
  unfold FieldRow
  decide

theorem field_4_7 : ∀ i : Fin 54, FieldRow data3 data4 member4 (896+i.val) := by
  unfold FieldRow
  decide

theorem field_4_all : ∀ u, 0 ≤ u → u < 950 → FieldRow data3 data4 member4 u :=
  (join_ranges (fun u => FieldRow data3 data4 member4 u) 0 512 950 (join_ranges (fun u => FieldRow data3 data4 member4 u) 0 256 512 (join_ranges (fun u => FieldRow data3 data4 member4 u) 0 128 256 (checked_range (fun u => FieldRow data3 data4 member4 u) 0 128 field_4_0) (checked_range (fun u => FieldRow data3 data4 member4 u) 128 128 field_4_1)) (join_ranges (fun u => FieldRow data3 data4 member4 u) 256 384 512 (checked_range (fun u => FieldRow data3 data4 member4 u) 256 128 field_4_2) (checked_range (fun u => FieldRow data3 data4 member4 u) 384 128 field_4_3))) (join_ranges (fun u => FieldRow data3 data4 member4 u) 512 768 950 (join_ranges (fun u => FieldRow data3 data4 member4 u) 512 640 768 (checked_range (fun u => FieldRow data3 data4 member4 u) 512 128 field_4_4) (checked_range (fun u => FieldRow data3 data4 member4 u) 640 128 field_4_5)) (join_ranges (fun u => FieldRow data3 data4 member4 u) 768 896 950 (checked_range (fun u => FieldRow data3 data4 member4 u) 768 128 field_4_6) (checked_range (fun u => FieldRow data3 data4 member4 u) 896 54 field_4_7))))
theorem lift_4_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_3 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_4 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (512+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_5 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (640+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_6 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (768+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_7 : ∀ i : Fin 54, ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 (896+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_4_all : ∀ u, 0 ≤ u → u < 950 → ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 0 512 950 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 0 128 lift_4_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 128 128 lift_4_1)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 256 128 lift_4_2) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 384 128 lift_4_3))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 512 768 950 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 512 128 lift_4_4) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 640 128 lift_4_5)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 768 896 950 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 768 128 lift_4_6) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data3 data4 component3 117 member4 memberIndex4 u bit.val) 896 54 lift_4_7))))
def lift_certificate4 : LiftCertificate data3 data4 component3 117 where
  members := member4
  memberIndex := memberIndex4
  count := 50
  size_eq := rfl
  coverage u hu := coverage_4_all u (Nat.zero_le u) hu
  fields u hu := field_4_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_4_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete4 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data3)
      (fun v => component3 v=117)))) (graph data4)
      (encode lift_certificate4) := lift_realization lift_certificate4
end BroaderJobData
