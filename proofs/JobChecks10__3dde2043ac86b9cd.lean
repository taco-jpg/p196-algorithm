import JobData10
import RangeChecks
import JobData9
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_10_0 : ∀ i : Fin 128, VertexRow ranking10 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_1 : ∀ i : Fin 128, VertexRow ranking10 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_2 : ∀ i : Fin 128, VertexRow ranking10 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_3 : ∀ i : Fin 128, VertexRow ranking10 (384+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_4 : ∀ i : Fin 128, VertexRow ranking10 (512+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_5 : ∀ i : Fin 128, VertexRow ranking10 (640+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_6 : ∀ i : Fin 128, VertexRow ranking10 (768+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_7 : ∀ i : Fin 128, VertexRow ranking10 (896+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_8 : ∀ i : Fin 128, VertexRow ranking10 (1024+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_9 : ∀ i : Fin 128, VertexRow ranking10 (1152+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_10 : ∀ i : Fin 128, VertexRow ranking10 (1280+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_11 : ∀ i : Fin 128, VertexRow ranking10 (1408+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_12 : ∀ i : Fin 117, VertexRow ranking10 (1536+i.val) := by
  unfold VertexRow
  decide

theorem vertex_10_all : ∀ u, 0 ≤ u → u < 1653 → VertexRow ranking10 u :=
  (join_ranges (fun u => VertexRow ranking10 u) 0 768 1653 (join_ranges (fun u => VertexRow ranking10 u) 0 384 768 (join_ranges (fun u => VertexRow ranking10 u) 0 128 384 (checked_range (fun u => VertexRow ranking10 u) 0 128 vertex_10_0) (join_ranges (fun u => VertexRow ranking10 u) 128 256 384 (checked_range (fun u => VertexRow ranking10 u) 128 128 vertex_10_1) (checked_range (fun u => VertexRow ranking10 u) 256 128 vertex_10_2))) (join_ranges (fun u => VertexRow ranking10 u) 384 512 768 (checked_range (fun u => VertexRow ranking10 u) 384 128 vertex_10_3) (join_ranges (fun u => VertexRow ranking10 u) 512 640 768 (checked_range (fun u => VertexRow ranking10 u) 512 128 vertex_10_4) (checked_range (fun u => VertexRow ranking10 u) 640 128 vertex_10_5)))) (join_ranges (fun u => VertexRow ranking10 u) 768 1152 1653 (join_ranges (fun u => VertexRow ranking10 u) 768 896 1152 (checked_range (fun u => VertexRow ranking10 u) 768 128 vertex_10_6) (join_ranges (fun u => VertexRow ranking10 u) 896 1024 1152 (checked_range (fun u => VertexRow ranking10 u) 896 128 vertex_10_7) (checked_range (fun u => VertexRow ranking10 u) 1024 128 vertex_10_8))) (join_ranges (fun u => VertexRow ranking10 u) 1152 1408 1653 (join_ranges (fun u => VertexRow ranking10 u) 1152 1280 1408 (checked_range (fun u => VertexRow ranking10 u) 1152 128 vertex_10_9) (checked_range (fun u => VertexRow ranking10 u) 1280 128 vertex_10_10)) (join_ranges (fun u => VertexRow ranking10 u) 1408 1536 1653 (checked_range (fun u => VertexRow ranking10 u) 1408 128 vertex_10_11) (checked_range (fun u => VertexRow ranking10 u) 1536 117 vertex_10_12)))))
theorem edge_10_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_2 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_3 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (384+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_4 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (512+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_5 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (640+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_6 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (768+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_7 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (896+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_8 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (1024+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_9 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (1152+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_10 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (1280+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_11 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data10 ranking10 (1408+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_12 : ∀ i : Fin 117, ∀ bit : Fin 2, EdgeRow data10 ranking10 (1536+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_10_all : ∀ u, 0 ≤ u → u < 1653 → ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 0 768 1653 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 0 384 768 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 0 128 384 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 0 128 edge_10_0) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 128 256 384 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 128 128 edge_10_1) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 256 128 edge_10_2))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 384 512 768 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 384 128 edge_10_3) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 512 128 edge_10_4) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 640 128 edge_10_5)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 768 1152 1653 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 768 896 1152 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 768 128 edge_10_6) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 896 1024 1152 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 896 128 edge_10_7) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1024 128 edge_10_8))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1152 1408 1653 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1152 1280 1408 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1152 128 edge_10_9) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1280 128 edge_10_10)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1408 1536 1653 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1408 128 edge_10_11) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data10 ranking10 u bit.val) 1536 117 edge_10_12)))))
theorem checked_rank10 : CheckedRank data10 ranking10 := by
  constructor
  · intro u hu
    exact vertex_10_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_10_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_10_0 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_1 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_2 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_3 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_4 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (512+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_5 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (640+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_6 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (768+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_7 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (896+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_8 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1024+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_9 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1152+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_10 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1280+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_11 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1408+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_12 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1536+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_13 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1664+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_14 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1792+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_15 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (1920+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_16 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2048+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_17 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2176+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_18 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2304+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_19 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2432+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_20 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2560+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_21 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2688+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_22 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2816+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_23 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (2944+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_24 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3072+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_25 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3200+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_26 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3328+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_27 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3456+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_28 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3584+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_29 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3712+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_30 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3840+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_31 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (3968+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_32 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4096+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_33 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4224+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_34 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4352+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_35 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4480+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_36 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4608+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_37 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4736+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_38 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4864+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_39 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (4992+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_40 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (5120+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_41 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (5248+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_42 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (5376+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_43 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (5504+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_44 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (5632+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_45 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (5760+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_46 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (5888+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_47 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6016+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_48 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6144+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_49 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6272+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_50 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6400+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_51 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6528+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_52 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6656+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_53 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6784+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_54 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (6912+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_55 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7040+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_56 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7168+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_57 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7296+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_58 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7424+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_59 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7552+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_60 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7680+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_61 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7808+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_62 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (7936+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_63 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8064+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_64 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8192+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_65 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8320+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_66 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8448+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_67 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8576+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_68 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8704+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_69 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8832+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_70 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (8960+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_71 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9088+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_72 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9216+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_73 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9344+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_74 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9472+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_75 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9600+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_76 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9728+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_77 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9856+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_78 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (9984+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_79 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (10112+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_80 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (10240+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_81 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (10368+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_82 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (10496+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_83 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (10624+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_84 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (10752+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_85 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (10880+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_86 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11008+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_87 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11136+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_88 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11264+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_89 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11392+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_90 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11520+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_91 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11648+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_92 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11776+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_93 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (11904+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_94 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (12032+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_95 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (12160+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_96 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (12288+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_97 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (12416+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_98 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (12544+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_99 : ∀ i : Fin 128, CoverageRow data9 component9 10716 87 member10 memberIndex10 (12672+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_100 : ∀ i : Fin 25, CoverageRow data9 component9 10716 87 member10 memberIndex10 (12800+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_10_all : ∀ u, 0 ≤ u → u < 12825 → CoverageRow data9 component9 10716 87 member10 memberIndex10 u :=
  (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 0 6400 12825 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 0 3200 6400 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 0 1536 3200 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 0 768 1536 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 0 384 768 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 0 128 384 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 0 128 coverage_10_0) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 128 256 384 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 128 128 coverage_10_1) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 256 128 coverage_10_2))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 384 512 768 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 384 128 coverage_10_3) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 512 640 768 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 512 128 coverage_10_4) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 640 128 coverage_10_5)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 768 1152 1536 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 768 896 1152 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 768 128 coverage_10_6) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 896 1024 1152 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 896 128 coverage_10_7) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1024 128 coverage_10_8))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1152 1280 1536 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1152 128 coverage_10_9) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1280 1408 1536 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1280 128 coverage_10_10) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1408 128 coverage_10_11))))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1536 2304 3200 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1536 1920 2304 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1536 1664 1920 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1536 128 coverage_10_12) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1664 1792 1920 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1664 128 coverage_10_13) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1792 128 coverage_10_14))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1920 2048 2304 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 1920 128 coverage_10_15) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2048 2176 2304 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2048 128 coverage_10_16) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2176 128 coverage_10_17)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2304 2688 3200 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2304 2432 2688 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2304 128 coverage_10_18) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2432 2560 2688 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2432 128 coverage_10_19) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2560 128 coverage_10_20))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2688 2944 3200 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2688 2816 2944 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2688 128 coverage_10_21) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2816 128 coverage_10_22)) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2944 3072 3200 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 2944 128 coverage_10_23) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3072 128 coverage_10_24)))))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3200 4736 6400 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3200 3968 4736 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3200 3584 3968 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3200 3328 3584 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3200 128 coverage_10_25) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3328 3456 3584 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3328 128 coverage_10_26) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3456 128 coverage_10_27))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3584 3712 3968 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3584 128 coverage_10_28) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3712 3840 3968 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3712 128 coverage_10_29) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3840 128 coverage_10_30)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3968 4352 4736 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3968 4096 4352 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 3968 128 coverage_10_31) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4096 4224 4352 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4096 128 coverage_10_32) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4224 128 coverage_10_33))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4352 4480 4736 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4352 128 coverage_10_34) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4480 4608 4736 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4480 128 coverage_10_35) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4608 128 coverage_10_36))))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4736 5504 6400 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4736 5120 5504 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4736 4864 5120 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4736 128 coverage_10_37) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4864 4992 5120 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4864 128 coverage_10_38) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 4992 128 coverage_10_39))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5120 5248 5504 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5120 128 coverage_10_40) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5248 5376 5504 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5248 128 coverage_10_41) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5376 128 coverage_10_42)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5504 5888 6400 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5504 5632 5888 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5504 128 coverage_10_43) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5632 5760 5888 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5632 128 coverage_10_44) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5760 128 coverage_10_45))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5888 6144 6400 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5888 6016 6144 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 5888 128 coverage_10_46) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6016 128 coverage_10_47)) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6144 6272 6400 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6144 128 coverage_10_48) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6272 128 coverage_10_49))))))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6400 9600 12825 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6400 7936 9600 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6400 7168 7936 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6400 6784 7168 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6400 6528 6784 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6400 128 coverage_10_50) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6528 6656 6784 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6528 128 coverage_10_51) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6656 128 coverage_10_52))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6784 6912 7168 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6784 128 coverage_10_53) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6912 7040 7168 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 6912 128 coverage_10_54) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7040 128 coverage_10_55)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7168 7552 7936 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7168 7296 7552 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7168 128 coverage_10_56) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7296 7424 7552 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7296 128 coverage_10_57) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7424 128 coverage_10_58))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7552 7680 7936 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7552 128 coverage_10_59) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7680 7808 7936 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7680 128 coverage_10_60) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7808 128 coverage_10_61))))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7936 8704 9600 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7936 8320 8704 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7936 8064 8320 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 7936 128 coverage_10_62) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8064 8192 8320 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8064 128 coverage_10_63) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8192 128 coverage_10_64))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8320 8448 8704 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8320 128 coverage_10_65) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8448 8576 8704 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8448 128 coverage_10_66) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8576 128 coverage_10_67)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8704 9088 9600 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8704 8832 9088 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8704 128 coverage_10_68) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8832 8960 9088 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8832 128 coverage_10_69) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 8960 128 coverage_10_70))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9088 9344 9600 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9088 9216 9344 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9088 128 coverage_10_71) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9216 128 coverage_10_72)) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9344 9472 9600 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9344 128 coverage_10_73) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9472 128 coverage_10_74)))))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9600 11264 12825 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9600 10368 11264 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9600 9984 10368 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9600 9728 9984 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9600 128 coverage_10_75) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9728 9856 9984 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9728 128 coverage_10_76) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9856 128 coverage_10_77))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9984 10112 10368 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 9984 128 coverage_10_78) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10112 10240 10368 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10112 128 coverage_10_79) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10240 128 coverage_10_80)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10368 10752 11264 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10368 10496 10752 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10368 128 coverage_10_81) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10496 10624 10752 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10496 128 coverage_10_82) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10624 128 coverage_10_83))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10752 11008 11264 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10752 10880 11008 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10752 128 coverage_10_84) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 10880 128 coverage_10_85)) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11008 11136 11264 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11008 128 coverage_10_86) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11136 128 coverage_10_87))))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11264 12032 12825 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11264 11648 12032 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11264 11392 11648 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11264 128 coverage_10_88) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11392 11520 11648 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11392 128 coverage_10_89) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11520 128 coverage_10_90))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11648 11776 12032 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11648 128 coverage_10_91) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11776 11904 12032 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11776 128 coverage_10_92) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 11904 128 coverage_10_93)))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12032 12416 12825 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12032 12160 12416 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12032 128 coverage_10_94) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12160 12288 12416 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12160 128 coverage_10_95) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12288 128 coverage_10_96))) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12416 12672 12825 (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12416 12544 12672 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12416 128 coverage_10_97) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12544 128 coverage_10_98)) (join_ranges (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12672 12800 12825 (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12672 128 coverage_10_99) (checked_range (fun u => CoverageRow data9 component9 10716 87 member10 memberIndex10 u) 12800 25 coverage_10_100))))))))
theorem field_10_0 : ∀ i : Fin 128, FieldRow data9 data10 member10 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_10_1 : ∀ i : Fin 128, FieldRow data9 data10 member10 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_10_2 : ∀ i : Fin 128, FieldRow data9 data10 member10 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_10_3 : ∀ i : Fin 128, FieldRow data9 data10 member10 (384+i.val) := by
  unfold FieldRow
  decide

theorem field_10_4 : ∀ i : Fin 128, FieldRow data9 data10 member10 (512+i.val) := by
  unfold FieldRow
  decide

theorem field_10_5 : ∀ i : Fin 128, FieldRow data9 data10 member10 (640+i.val) := by
  unfold FieldRow
  decide

theorem field_10_6 : ∀ i : Fin 128, FieldRow data9 data10 member10 (768+i.val) := by
  unfold FieldRow
  decide

theorem field_10_7 : ∀ i : Fin 128, FieldRow data9 data10 member10 (896+i.val) := by
  unfold FieldRow
  decide

theorem field_10_8 : ∀ i : Fin 128, FieldRow data9 data10 member10 (1024+i.val) := by
  unfold FieldRow
  decide

theorem field_10_9 : ∀ i : Fin 128, FieldRow data9 data10 member10 (1152+i.val) := by
  unfold FieldRow
  decide

theorem field_10_10 : ∀ i : Fin 128, FieldRow data9 data10 member10 (1280+i.val) := by
  unfold FieldRow
  decide

theorem field_10_11 : ∀ i : Fin 128, FieldRow data9 data10 member10 (1408+i.val) := by
  unfold FieldRow
  decide

theorem field_10_12 : ∀ i : Fin 117, FieldRow data9 data10 member10 (1536+i.val) := by
  unfold FieldRow
  decide

theorem field_10_all : ∀ u, 0 ≤ u → u < 1653 → FieldRow data9 data10 member10 u :=
  (join_ranges (fun u => FieldRow data9 data10 member10 u) 0 768 1653 (join_ranges (fun u => FieldRow data9 data10 member10 u) 0 384 768 (join_ranges (fun u => FieldRow data9 data10 member10 u) 0 128 384 (checked_range (fun u => FieldRow data9 data10 member10 u) 0 128 field_10_0) (join_ranges (fun u => FieldRow data9 data10 member10 u) 128 256 384 (checked_range (fun u => FieldRow data9 data10 member10 u) 128 128 field_10_1) (checked_range (fun u => FieldRow data9 data10 member10 u) 256 128 field_10_2))) (join_ranges (fun u => FieldRow data9 data10 member10 u) 384 512 768 (checked_range (fun u => FieldRow data9 data10 member10 u) 384 128 field_10_3) (join_ranges (fun u => FieldRow data9 data10 member10 u) 512 640 768 (checked_range (fun u => FieldRow data9 data10 member10 u) 512 128 field_10_4) (checked_range (fun u => FieldRow data9 data10 member10 u) 640 128 field_10_5)))) (join_ranges (fun u => FieldRow data9 data10 member10 u) 768 1152 1653 (join_ranges (fun u => FieldRow data9 data10 member10 u) 768 896 1152 (checked_range (fun u => FieldRow data9 data10 member10 u) 768 128 field_10_6) (join_ranges (fun u => FieldRow data9 data10 member10 u) 896 1024 1152 (checked_range (fun u => FieldRow data9 data10 member10 u) 896 128 field_10_7) (checked_range (fun u => FieldRow data9 data10 member10 u) 1024 128 field_10_8))) (join_ranges (fun u => FieldRow data9 data10 member10 u) 1152 1408 1653 (join_ranges (fun u => FieldRow data9 data10 member10 u) 1152 1280 1408 (checked_range (fun u => FieldRow data9 data10 member10 u) 1152 128 field_10_9) (checked_range (fun u => FieldRow data9 data10 member10 u) 1280 128 field_10_10)) (join_ranges (fun u => FieldRow data9 data10 member10 u) 1408 1536 1653 (checked_range (fun u => FieldRow data9 data10 member10 u) 1408 128 field_10_11) (checked_range (fun u => FieldRow data9 data10 member10 u) 1536 117 field_10_12)))))
theorem lift_10_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_3 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_4 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (512+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_5 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (640+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_6 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (768+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_7 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (896+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_8 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (1024+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_9 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (1152+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_10 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (1280+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_11 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (1408+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_12 : ∀ i : Fin 117, ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 (1536+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_10_all : ∀ u, 0 ≤ u → u < 1653 → ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 0 768 1653 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 0 384 768 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 0 128 384 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 0 128 lift_10_0) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 128 256 384 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 128 128 lift_10_1) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 256 128 lift_10_2))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 384 512 768 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 384 128 lift_10_3) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 512 128 lift_10_4) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 640 128 lift_10_5)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 768 1152 1653 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 768 896 1152 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 768 128 lift_10_6) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 896 1024 1152 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 896 128 lift_10_7) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1024 128 lift_10_8))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1152 1408 1653 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1152 1280 1408 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1152 128 lift_10_9) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1280 128 lift_10_10)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1408 1536 1653 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1408 128 lift_10_11) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data9 data10 component9 10716 member10 memberIndex10 u bit.val) 1536 117 lift_10_12)))))
def lift_certificate10 : LiftCertificate data9 data10 component9 10716 where
  members := member10
  memberIndex := memberIndex10
  count := 87
  size_eq := rfl
  coverage u hu := coverage_10_all u (Nat.zero_le u) hu
  fields u hu := field_10_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_10_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete10 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data9)
      (fun v => component9 v=10716)))) (graph data10)
      (encode lift_certificate10) := lift_realization lift_certificate10
end ScalarJobData
