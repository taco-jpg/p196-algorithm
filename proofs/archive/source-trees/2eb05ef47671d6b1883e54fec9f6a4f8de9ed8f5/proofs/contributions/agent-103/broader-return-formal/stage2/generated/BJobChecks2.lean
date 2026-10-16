import BJobData2
import RangeChecks
import BJobData1
namespace BroaderJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_2_0 : ∀ i : Fin 128, VertexRow ranking2 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_2_1 : ∀ i : Fin 100, VertexRow ranking2 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_2_all : ∀ u, 0 ≤ u → u < 228 → VertexRow ranking2 u :=
  (join_ranges (fun u => VertexRow ranking2 u) 0 128 228 (checked_range (fun u => VertexRow ranking2 u) 0 128 vertex_2_0) (checked_range (fun u => VertexRow ranking2 u) 128 100 vertex_2_1))
theorem edge_2_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data2 ranking2 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_2_1 : ∀ i : Fin 100, ∀ bit : Fin 2, EdgeRow data2 ranking2 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_2_all : ∀ u, 0 ≤ u → u < 228 → ∀ bit : Fin 2, EdgeRow data2 ranking2 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data2 ranking2 u bit.val) 0 128 228 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data2 ranking2 u bit.val) 0 128 edge_2_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data2 ranking2 u bit.val) 128 100 edge_2_1))
theorem checked_rank2 : CheckedRank data2 ranking2 := by
  constructor
  · intro u hu
    exact vertex_2_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_2_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_2_0 : ∀ i : Fin 128, CoverageRow data1 component1 153 12 member2 memberIndex2 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_2_1 : ∀ i : Fin 128, CoverageRow data1 component1 153 12 member2 memberIndex2 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_2_2 : ∀ i : Fin 29, CoverageRow data1 component1 153 12 member2 memberIndex2 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_2_all : ∀ u, 0 ≤ u → u < 285 → CoverageRow data1 component1 153 12 member2 memberIndex2 u :=
  (join_ranges (fun u => CoverageRow data1 component1 153 12 member2 memberIndex2 u) 0 128 285 (checked_range (fun u => CoverageRow data1 component1 153 12 member2 memberIndex2 u) 0 128 coverage_2_0) (join_ranges (fun u => CoverageRow data1 component1 153 12 member2 memberIndex2 u) 128 256 285 (checked_range (fun u => CoverageRow data1 component1 153 12 member2 memberIndex2 u) 128 128 coverage_2_1) (checked_range (fun u => CoverageRow data1 component1 153 12 member2 memberIndex2 u) 256 29 coverage_2_2)))
theorem field_2_0 : ∀ i : Fin 128, FieldRow data1 data2 member2 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_2_1 : ∀ i : Fin 100, FieldRow data1 data2 member2 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_2_all : ∀ u, 0 ≤ u → u < 228 → FieldRow data1 data2 member2 u :=
  (join_ranges (fun u => FieldRow data1 data2 member2 u) 0 128 228 (checked_range (fun u => FieldRow data1 data2 member2 u) 0 128 field_2_0) (checked_range (fun u => FieldRow data1 data2 member2 u) 128 100 field_2_1))
theorem lift_2_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data1 data2 component1 153 member2 memberIndex2 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_2_1 : ∀ i : Fin 100, ∀ bit : Fin 2, LiftRow data1 data2 component1 153 member2 memberIndex2 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_2_all : ∀ u, 0 ≤ u → u < 228 → ∀ bit : Fin 2, LiftRow data1 data2 component1 153 member2 memberIndex2 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data1 data2 component1 153 member2 memberIndex2 u bit.val) 0 128 228 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data1 data2 component1 153 member2 memberIndex2 u bit.val) 0 128 lift_2_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data1 data2 component1 153 member2 memberIndex2 u bit.val) 128 100 lift_2_1))
def lift_certificate2 : LiftCertificate data1 data2 component1 153 where
  members := member2
  memberIndex := memberIndex2
  count := 12
  size_eq := rfl
  coverage u hu := coverage_2_all u (Nat.zero_le u) hu
  fields u hu := field_2_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_2_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete2 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data1)
      (fun v => component1 v=153)))) (graph data2)
      (encode lift_certificate2) := lift_realization lift_certificate2
end BroaderJobData
