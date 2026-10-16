import BJobData14
import RangeChecks
import BJobData10
namespace BroaderJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_14_0 : ∀ i : Fin 128, VertexRow ranking14 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_14_1 : ∀ i : Fin 128, VertexRow ranking14 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_14_2 : ∀ i : Fin 128, VertexRow ranking14 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_14_3 : ∀ i : Fin 110, VertexRow ranking14 (384+i.val) := by
  unfold VertexRow
  decide

theorem vertex_14_all : ∀ u, 0 ≤ u → u < 494 → VertexRow ranking14 u :=
  (join_ranges (fun u => VertexRow ranking14 u) 0 256 494 (join_ranges (fun u => VertexRow ranking14 u) 0 128 256 (checked_range (fun u => VertexRow ranking14 u) 0 128 vertex_14_0) (checked_range (fun u => VertexRow ranking14 u) 128 128 vertex_14_1)) (join_ranges (fun u => VertexRow ranking14 u) 256 384 494 (checked_range (fun u => VertexRow ranking14 u) 256 128 vertex_14_2) (checked_range (fun u => VertexRow ranking14 u) 384 110 vertex_14_3)))
theorem edge_14_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data14 ranking14 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_14_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data14 ranking14 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_14_2 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data14 ranking14 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_14_3 : ∀ i : Fin 110, ∀ bit : Fin 2, EdgeRow data14 ranking14 (384+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_14_all : ∀ u, 0 ≤ u → u < 494 → ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val) 0 256 494 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val) 0 128 edge_14_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val) 128 128 edge_14_1)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val) 256 384 494 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val) 256 128 edge_14_2) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data14 ranking14 u bit.val) 384 110 edge_14_3)))
theorem checked_rank14 : CheckedRank data14 ranking14 := by
  constructor
  · intro u hu
    exact vertex_14_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_14_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_14_0 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_1 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_2 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_3 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_4 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (512+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_5 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (640+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_6 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (768+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_7 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (896+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_8 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1024+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_9 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1152+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_10 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1280+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_11 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1408+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_12 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1536+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_13 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1664+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_14 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1792+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_15 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (1920+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_16 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2048+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_17 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2176+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_18 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2304+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_19 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2432+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_20 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2560+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_21 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2688+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_22 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2816+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_23 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (2944+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_24 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3072+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_25 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3200+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_26 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3328+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_27 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3456+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_28 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3584+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_29 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3712+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_30 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3840+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_31 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (3968+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_32 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4096+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_33 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4224+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_34 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4352+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_35 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4480+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_36 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4608+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_37 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4736+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_38 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4864+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_39 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (4992+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_40 : ∀ i : Fin 128, CoverageRow data10 component10 4628 26 member14 memberIndex14 (5120+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_41 : ∀ i : Fin 15, CoverageRow data10 component10 4628 26 member14 memberIndex14 (5248+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_14_all : ∀ u, 0 ≤ u → u < 5263 → CoverageRow data10 component10 4628 26 member14 memberIndex14 u :=
  (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 0 2688 5263 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 0 1280 2688 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 0 640 1280 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 0 256 640 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 0 128 256 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 0 128 coverage_14_0) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 128 128 coverage_14_1)) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 256 384 640 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 256 128 coverage_14_2) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 384 512 640 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 384 128 coverage_14_3) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 512 128 coverage_14_4)))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 640 896 1280 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 640 768 896 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 640 128 coverage_14_5) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 768 128 coverage_14_6)) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 896 1024 1280 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 896 128 coverage_14_7) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1024 1152 1280 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1024 128 coverage_14_8) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1152 128 coverage_14_9))))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1280 1920 2688 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1280 1536 1920 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1280 1408 1536 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1280 128 coverage_14_10) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1408 128 coverage_14_11)) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1536 1664 1920 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1536 128 coverage_14_12) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1664 1792 1920 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1664 128 coverage_14_13) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1792 128 coverage_14_14)))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1920 2304 2688 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1920 2048 2304 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 1920 128 coverage_14_15) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2048 2176 2304 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2048 128 coverage_14_16) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2176 128 coverage_14_17))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2304 2432 2688 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2304 128 coverage_14_18) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2432 2560 2688 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2432 128 coverage_14_19) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2560 128 coverage_14_20)))))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2688 3968 5263 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2688 3328 3968 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2688 2944 3328 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2688 2816 2944 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2688 128 coverage_14_21) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2816 128 coverage_14_22)) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2944 3072 3328 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 2944 128 coverage_14_23) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3072 3200 3328 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3072 128 coverage_14_24) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3200 128 coverage_14_25)))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3328 3584 3968 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3328 3456 3584 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3328 128 coverage_14_26) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3456 128 coverage_14_27)) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3584 3712 3968 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3584 128 coverage_14_28) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3712 3840 3968 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3712 128 coverage_14_29) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3840 128 coverage_14_30))))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3968 4608 5263 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3968 4224 4608 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3968 4096 4224 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 3968 128 coverage_14_31) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4096 128 coverage_14_32)) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4224 4352 4608 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4224 128 coverage_14_33) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4352 4480 4608 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4352 128 coverage_14_34) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4480 128 coverage_14_35)))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4608 4992 5263 (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4608 4736 4992 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4608 128 coverage_14_36) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4736 4864 4992 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4736 128 coverage_14_37) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4864 128 coverage_14_38))) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4992 5120 5263 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 4992 128 coverage_14_39) (join_ranges (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 5120 5248 5263 (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 5120 128 coverage_14_40) (checked_range (fun u => CoverageRow data10 component10 4628 26 member14 memberIndex14 u) 5248 15 coverage_14_41)))))))
theorem field_14_0 : ∀ i : Fin 128, FieldRow data10 data14 member14 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_14_1 : ∀ i : Fin 128, FieldRow data10 data14 member14 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_14_2 : ∀ i : Fin 128, FieldRow data10 data14 member14 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_14_3 : ∀ i : Fin 110, FieldRow data10 data14 member14 (384+i.val) := by
  unfold FieldRow
  decide

theorem field_14_all : ∀ u, 0 ≤ u → u < 494 → FieldRow data10 data14 member14 u :=
  (join_ranges (fun u => FieldRow data10 data14 member14 u) 0 256 494 (join_ranges (fun u => FieldRow data10 data14 member14 u) 0 128 256 (checked_range (fun u => FieldRow data10 data14 member14 u) 0 128 field_14_0) (checked_range (fun u => FieldRow data10 data14 member14 u) 128 128 field_14_1)) (join_ranges (fun u => FieldRow data10 data14 member14 u) 256 384 494 (checked_range (fun u => FieldRow data10 data14 member14 u) 256 128 field_14_2) (checked_range (fun u => FieldRow data10 data14 member14 u) 384 110 field_14_3)))
theorem lift_14_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_14_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_14_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_14_3 : ∀ i : Fin 110, ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_14_all : ∀ u, 0 ≤ u → u < 494 → ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val) 0 256 494 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val) 0 128 lift_14_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val) 128 128 lift_14_1)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val) 256 384 494 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val) 256 128 lift_14_2) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data10 data14 component10 4628 member14 memberIndex14 u bit.val) 384 110 lift_14_3)))
def lift_certificate14 : LiftCertificate data10 data14 component10 4628 where
  members := member14
  memberIndex := memberIndex14
  count := 26
  size_eq := rfl
  coverage u hu := coverage_14_all u (Nat.zero_le u) hu
  fields u hu := field_14_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_14_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete14 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data10)
      (fun v => component10 v=4628)))) (graph data14)
      (encode lift_certificate14) := lift_realization lift_certificate14
end BroaderJobData
