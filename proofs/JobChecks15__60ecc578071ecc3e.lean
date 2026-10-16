import JobData15
import RangeChecks
import JobData11
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_15_0 : ∀ i : Fin 128, VertexRow ranking15 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_15_1 : ∀ i : Fin 128, VertexRow ranking15 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_15_2 : ∀ i : Fin 128, VertexRow ranking15 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_15_3 : ∀ i : Fin 110, VertexRow ranking15 (384+i.val) := by
  unfold VertexRow
  decide

theorem vertex_15_all : ∀ u, 0 ≤ u → u < 494 → VertexRow ranking15 u :=
  (join_ranges (fun u => VertexRow ranking15 u) 0 256 494 (join_ranges (fun u => VertexRow ranking15 u) 0 128 256 (checked_range (fun u => VertexRow ranking15 u) 0 128 vertex_15_0) (checked_range (fun u => VertexRow ranking15 u) 128 128 vertex_15_1)) (join_ranges (fun u => VertexRow ranking15 u) 256 384 494 (checked_range (fun u => VertexRow ranking15 u) 256 128 vertex_15_2) (checked_range (fun u => VertexRow ranking15 u) 384 110 vertex_15_3)))
theorem edge_15_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data15 ranking15 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_15_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data15 ranking15 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_15_2 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data15 ranking15 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_15_3 : ∀ i : Fin 110, ∀ bit : Fin 2, EdgeRow data15 ranking15 (384+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_15_all : ∀ u, 0 ≤ u → u < 494 → ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val) 0 256 494 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val) 0 128 edge_15_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val) 128 128 edge_15_1)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val) 256 384 494 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val) 256 128 edge_15_2) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data15 ranking15 u bit.val) 384 110 edge_15_3)))
theorem checked_rank15 : CheckedRank data15 ranking15 := by
  constructor
  · intro u hu
    exact vertex_15_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_15_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_15_0 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_1 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_2 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_3 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_4 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (512+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_5 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (640+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_6 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (768+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_7 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (896+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_8 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1024+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_9 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1152+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_10 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1280+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_11 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1408+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_12 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1536+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_13 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1664+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_14 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1792+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_15 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (1920+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_16 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2048+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_17 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2176+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_18 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2304+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_19 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2432+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_20 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2560+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_21 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2688+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_22 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2816+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_23 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (2944+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_24 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3072+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_25 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3200+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_26 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3328+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_27 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3456+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_28 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3584+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_29 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3712+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_30 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3840+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_31 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (3968+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_32 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4096+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_33 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4224+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_34 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4352+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_35 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4480+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_36 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4608+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_37 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4736+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_38 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4864+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_39 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (4992+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_40 : ∀ i : Fin 128, CoverageRow data11 component11 4628 26 member15 memberIndex15 (5120+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_41 : ∀ i : Fin 15, CoverageRow data11 component11 4628 26 member15 memberIndex15 (5248+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_15_all : ∀ u, 0 ≤ u → u < 5263 → CoverageRow data11 component11 4628 26 member15 memberIndex15 u :=
  (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 0 2688 5263 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 0 1280 2688 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 0 640 1280 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 0 256 640 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 0 128 256 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 0 128 coverage_15_0) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 128 128 coverage_15_1)) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 256 384 640 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 256 128 coverage_15_2) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 384 512 640 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 384 128 coverage_15_3) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 512 128 coverage_15_4)))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 640 896 1280 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 640 768 896 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 640 128 coverage_15_5) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 768 128 coverage_15_6)) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 896 1024 1280 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 896 128 coverage_15_7) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1024 1152 1280 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1024 128 coverage_15_8) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1152 128 coverage_15_9))))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1280 1920 2688 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1280 1536 1920 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1280 1408 1536 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1280 128 coverage_15_10) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1408 128 coverage_15_11)) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1536 1664 1920 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1536 128 coverage_15_12) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1664 1792 1920 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1664 128 coverage_15_13) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1792 128 coverage_15_14)))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1920 2304 2688 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1920 2048 2304 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 1920 128 coverage_15_15) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2048 2176 2304 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2048 128 coverage_15_16) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2176 128 coverage_15_17))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2304 2432 2688 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2304 128 coverage_15_18) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2432 2560 2688 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2432 128 coverage_15_19) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2560 128 coverage_15_20)))))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2688 3968 5263 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2688 3328 3968 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2688 2944 3328 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2688 2816 2944 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2688 128 coverage_15_21) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2816 128 coverage_15_22)) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2944 3072 3328 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 2944 128 coverage_15_23) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3072 3200 3328 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3072 128 coverage_15_24) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3200 128 coverage_15_25)))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3328 3584 3968 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3328 3456 3584 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3328 128 coverage_15_26) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3456 128 coverage_15_27)) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3584 3712 3968 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3584 128 coverage_15_28) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3712 3840 3968 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3712 128 coverage_15_29) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3840 128 coverage_15_30))))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3968 4608 5263 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3968 4224 4608 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3968 4096 4224 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 3968 128 coverage_15_31) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4096 128 coverage_15_32)) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4224 4352 4608 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4224 128 coverage_15_33) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4352 4480 4608 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4352 128 coverage_15_34) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4480 128 coverage_15_35)))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4608 4992 5263 (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4608 4736 4992 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4608 128 coverage_15_36) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4736 4864 4992 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4736 128 coverage_15_37) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4864 128 coverage_15_38))) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4992 5120 5263 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 4992 128 coverage_15_39) (join_ranges (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 5120 5248 5263 (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 5120 128 coverage_15_40) (checked_range (fun u => CoverageRow data11 component11 4628 26 member15 memberIndex15 u) 5248 15 coverage_15_41)))))))
theorem field_15_0 : ∀ i : Fin 128, FieldRow data11 data15 member15 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_15_1 : ∀ i : Fin 128, FieldRow data11 data15 member15 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_15_2 : ∀ i : Fin 128, FieldRow data11 data15 member15 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_15_3 : ∀ i : Fin 110, FieldRow data11 data15 member15 (384+i.val) := by
  unfold FieldRow
  decide

theorem field_15_all : ∀ u, 0 ≤ u → u < 494 → FieldRow data11 data15 member15 u :=
  (join_ranges (fun u => FieldRow data11 data15 member15 u) 0 256 494 (join_ranges (fun u => FieldRow data11 data15 member15 u) 0 128 256 (checked_range (fun u => FieldRow data11 data15 member15 u) 0 128 field_15_0) (checked_range (fun u => FieldRow data11 data15 member15 u) 128 128 field_15_1)) (join_ranges (fun u => FieldRow data11 data15 member15 u) 256 384 494 (checked_range (fun u => FieldRow data11 data15 member15 u) 256 128 field_15_2) (checked_range (fun u => FieldRow data11 data15 member15 u) 384 110 field_15_3)))
theorem lift_15_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_15_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_15_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_15_3 : ∀ i : Fin 110, ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_15_all : ∀ u, 0 ≤ u → u < 494 → ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val) 0 256 494 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val) 0 128 lift_15_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val) 128 128 lift_15_1)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val) 256 384 494 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val) 256 128 lift_15_2) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data15 component11 4628 member15 memberIndex15 u bit.val) 384 110 lift_15_3)))
def lift_certificate15 : LiftCertificate data11 data15 component11 4628 where
  members := member15
  memberIndex := memberIndex15
  count := 26
  size_eq := rfl
  coverage u hu := coverage_15_all u (Nat.zero_le u) hu
  fields u hu := field_15_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_15_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete15 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data11)
      (fun v => component11 v=4628)))) (graph data15)
      (encode lift_certificate15) := lift_realization lift_certificate15
end ScalarJobData
