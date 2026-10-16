import JobData5
import RangeChecks
import JobData4
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_5_0 : ∀ i : Fin 128, VertexRow ranking5 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_1 : ∀ i : Fin 128, VertexRow ranking5 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_2 : ∀ i : Fin 128, VertexRow ranking5 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_3 : ∀ i : Fin 128, VertexRow ranking5 (384+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_4 : ∀ i : Fin 128, VertexRow ranking5 (512+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_5 : ∀ i : Fin 128, VertexRow ranking5 (640+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_6 : ∀ i : Fin 128, VertexRow ranking5 (768+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_7 : ∀ i : Fin 54, VertexRow ranking5 (896+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_all : ∀ u, 0 ≤ u → u < 950 → VertexRow ranking5 u :=
  (join_ranges (fun u => VertexRow ranking5 u) 0 512 950 (join_ranges (fun u => VertexRow ranking5 u) 0 256 512 (join_ranges (fun u => VertexRow ranking5 u) 0 128 256 (checked_range (fun u => VertexRow ranking5 u) 0 128 vertex_5_0) (checked_range (fun u => VertexRow ranking5 u) 128 128 vertex_5_1)) (join_ranges (fun u => VertexRow ranking5 u) 256 384 512 (checked_range (fun u => VertexRow ranking5 u) 256 128 vertex_5_2) (checked_range (fun u => VertexRow ranking5 u) 384 128 vertex_5_3))) (join_ranges (fun u => VertexRow ranking5 u) 512 768 950 (join_ranges (fun u => VertexRow ranking5 u) 512 640 768 (checked_range (fun u => VertexRow ranking5 u) 512 128 vertex_5_4) (checked_range (fun u => VertexRow ranking5 u) 640 128 vertex_5_5)) (join_ranges (fun u => VertexRow ranking5 u) 768 896 950 (checked_range (fun u => VertexRow ranking5 u) 768 128 vertex_5_6) (checked_range (fun u => VertexRow ranking5 u) 896 54 vertex_5_7))))
theorem edge_5_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_2 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_3 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (384+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_4 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (512+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_5 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (640+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_6 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (768+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_7 : ∀ i : Fin 54, ∀ bit : Fin 2, EdgeRow data5 ranking5 (896+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_all : ∀ u, 0 ≤ u → u < 950 → ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 512 950 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 128 edge_5_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 128 128 edge_5_1)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 256 128 edge_5_2) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 384 128 edge_5_3))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 512 768 950 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 512 128 edge_5_4) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 640 128 edge_5_5)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 768 896 950 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 768 128 edge_5_6) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 896 54 edge_5_7))))
theorem checked_rank5 : CheckedRank data5 ranking5 := by
  constructor
  · intro u hu
    exact vertex_5_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_5_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_5_0 : ∀ i : Fin 128, CoverageRow data4 component4 173 50 member5 memberIndex5 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_1 : ∀ i : Fin 128, CoverageRow data4 component4 173 50 member5 memberIndex5 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_2 : ∀ i : Fin 105, CoverageRow data4 component4 173 50 member5 memberIndex5 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_all : ∀ u, 0 ≤ u → u < 361 → CoverageRow data4 component4 173 50 member5 memberIndex5 u :=
  (join_ranges (fun u => CoverageRow data4 component4 173 50 member5 memberIndex5 u) 0 128 361 (checked_range (fun u => CoverageRow data4 component4 173 50 member5 memberIndex5 u) 0 128 coverage_5_0) (join_ranges (fun u => CoverageRow data4 component4 173 50 member5 memberIndex5 u) 128 256 361 (checked_range (fun u => CoverageRow data4 component4 173 50 member5 memberIndex5 u) 128 128 coverage_5_1) (checked_range (fun u => CoverageRow data4 component4 173 50 member5 memberIndex5 u) 256 105 coverage_5_2)))
theorem field_5_0 : ∀ i : Fin 128, FieldRow data4 data5 member5 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_5_1 : ∀ i : Fin 128, FieldRow data4 data5 member5 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_5_2 : ∀ i : Fin 128, FieldRow data4 data5 member5 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_5_3 : ∀ i : Fin 128, FieldRow data4 data5 member5 (384+i.val) := by
  unfold FieldRow
  decide

theorem field_5_4 : ∀ i : Fin 128, FieldRow data4 data5 member5 (512+i.val) := by
  unfold FieldRow
  decide

theorem field_5_5 : ∀ i : Fin 128, FieldRow data4 data5 member5 (640+i.val) := by
  unfold FieldRow
  decide

theorem field_5_6 : ∀ i : Fin 128, FieldRow data4 data5 member5 (768+i.val) := by
  unfold FieldRow
  decide

theorem field_5_7 : ∀ i : Fin 54, FieldRow data4 data5 member5 (896+i.val) := by
  unfold FieldRow
  decide

theorem field_5_all : ∀ u, 0 ≤ u → u < 950 → FieldRow data4 data5 member5 u :=
  (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 512 950 (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 256 512 (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 128 256 (checked_range (fun u => FieldRow data4 data5 member5 u) 0 128 field_5_0) (checked_range (fun u => FieldRow data4 data5 member5 u) 128 128 field_5_1)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 256 384 512 (checked_range (fun u => FieldRow data4 data5 member5 u) 256 128 field_5_2) (checked_range (fun u => FieldRow data4 data5 member5 u) 384 128 field_5_3))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 512 768 950 (join_ranges (fun u => FieldRow data4 data5 member5 u) 512 640 768 (checked_range (fun u => FieldRow data4 data5 member5 u) 512 128 field_5_4) (checked_range (fun u => FieldRow data4 data5 member5 u) 640 128 field_5_5)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 768 896 950 (checked_range (fun u => FieldRow data4 data5 member5 u) 768 128 field_5_6) (checked_range (fun u => FieldRow data4 data5 member5 u) 896 54 field_5_7))))
theorem lift_5_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_3 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_4 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (512+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_5 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (640+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_6 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (768+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_7 : ∀ i : Fin 54, ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 (896+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_all : ∀ u, 0 ≤ u → u < 950 → ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 0 512 950 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 0 128 lift_5_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 128 128 lift_5_1)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 256 128 lift_5_2) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 384 128 lift_5_3))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 512 768 950 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 512 128 lift_5_4) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 640 128 lift_5_5)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 768 896 950 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 768 128 lift_5_6) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 173 member5 memberIndex5 u bit.val) 896 54 lift_5_7))))
def lift_certificate5 : LiftCertificate data4 data5 component4 173 where
  members := member5
  memberIndex := memberIndex5
  count := 50
  size_eq := rfl
  coverage u hu := coverage_5_all u (Nat.zero_le u) hu
  fields u hu := field_5_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_5_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete5 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data4)
      (fun v => component4 v=173)))) (graph data5)
      (encode lift_certificate5) := lift_realization lift_certificate5
end ScalarJobData
