import JobData3
import RangeChecks
import JobData2
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_3_0 : ∀ i : Fin 128, VertexRow ranking3 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_3_1 : ∀ i : Fin 100, VertexRow ranking3 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_3_all : ∀ u, 0 ≤ u → u < 228 → VertexRow ranking3 u :=
  (join_ranges (fun u => VertexRow ranking3 u) 0 128 228 (checked_range (fun u => VertexRow ranking3 u) 0 128 vertex_3_0) (checked_range (fun u => VertexRow ranking3 u) 128 100 vertex_3_1))
theorem edge_3_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data3 ranking3 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_3_1 : ∀ i : Fin 100, ∀ bit : Fin 2, EdgeRow data3 ranking3 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_3_all : ∀ u, 0 ≤ u → u < 228 → ∀ bit : Fin 2, EdgeRow data3 ranking3 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data3 ranking3 u bit.val) 0 128 228 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data3 ranking3 u bit.val) 0 128 edge_3_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data3 ranking3 u bit.val) 128 100 edge_3_1))
theorem checked_rank3 : CheckedRank data3 ranking3 := by
  constructor
  · intro u hu
    exact vertex_3_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_3_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_3_0 : ∀ i : Fin 128, CoverageRow data2 component2 234 12 member3 memberIndex3 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_3_1 : ∀ i : Fin 128, CoverageRow data2 component2 234 12 member3 memberIndex3 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_3_2 : ∀ i : Fin 128, CoverageRow data2 component2 234 12 member3 memberIndex3 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_3_3 : ∀ i : Fin 72, CoverageRow data2 component2 234 12 member3 memberIndex3 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_3_all : ∀ u, 0 ≤ u → u < 456 → CoverageRow data2 component2 234 12 member3 memberIndex3 u :=
  (join_ranges (fun u => CoverageRow data2 component2 234 12 member3 memberIndex3 u) 0 256 456 (join_ranges (fun u => CoverageRow data2 component2 234 12 member3 memberIndex3 u) 0 128 256 (checked_range (fun u => CoverageRow data2 component2 234 12 member3 memberIndex3 u) 0 128 coverage_3_0) (checked_range (fun u => CoverageRow data2 component2 234 12 member3 memberIndex3 u) 128 128 coverage_3_1)) (join_ranges (fun u => CoverageRow data2 component2 234 12 member3 memberIndex3 u) 256 384 456 (checked_range (fun u => CoverageRow data2 component2 234 12 member3 memberIndex3 u) 256 128 coverage_3_2) (checked_range (fun u => CoverageRow data2 component2 234 12 member3 memberIndex3 u) 384 72 coverage_3_3)))
theorem field_3_0 : ∀ i : Fin 128, FieldRow data2 data3 member3 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_3_1 : ∀ i : Fin 100, FieldRow data2 data3 member3 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_3_all : ∀ u, 0 ≤ u → u < 228 → FieldRow data2 data3 member3 u :=
  (join_ranges (fun u => FieldRow data2 data3 member3 u) 0 128 228 (checked_range (fun u => FieldRow data2 data3 member3 u) 0 128 field_3_0) (checked_range (fun u => FieldRow data2 data3 member3 u) 128 100 field_3_1))
theorem lift_3_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data2 data3 component2 234 member3 memberIndex3 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_3_1 : ∀ i : Fin 100, ∀ bit : Fin 2, LiftRow data2 data3 component2 234 member3 memberIndex3 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_3_all : ∀ u, 0 ≤ u → u < 228 → ∀ bit : Fin 2, LiftRow data2 data3 component2 234 member3 memberIndex3 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data2 data3 component2 234 member3 memberIndex3 u bit.val) 0 128 228 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data2 data3 component2 234 member3 memberIndex3 u bit.val) 0 128 lift_3_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data2 data3 component2 234 member3 memberIndex3 u bit.val) 128 100 lift_3_1))
def lift_certificate3 : LiftCertificate data2 data3 component2 234 where
  members := member3
  memberIndex := memberIndex3
  count := 12
  size_eq := rfl
  coverage u hu := coverage_3_all u (Nat.zero_le u) hu
  fields u hu := field_3_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_3_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete3 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data2)
      (fun v => component2 v=234)))) (graph data3)
      (encode lift_certificate3) := lift_realization lift_certificate3
end ScalarJobData
