import JobData12
import RangeChecks
import JobData11
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_12_0 : ∀ i : Fin 128, VertexRow ranking12 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_1 : ∀ i : Fin 128, VertexRow ranking12 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_2 : ∀ i : Fin 128, VertexRow ranking12 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_3 : ∀ i : Fin 128, VertexRow ranking12 (384+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_4 : ∀ i : Fin 128, VertexRow ranking12 (512+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_5 : ∀ i : Fin 128, VertexRow ranking12 (640+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_6 : ∀ i : Fin 128, VertexRow ranking12 (768+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_7 : ∀ i : Fin 128, VertexRow ranking12 (896+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_8 : ∀ i : Fin 128, VertexRow ranking12 (1024+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_9 : ∀ i : Fin 128, VertexRow ranking12 (1152+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_10 : ∀ i : Fin 128, VertexRow ranking12 (1280+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_11 : ∀ i : Fin 128, VertexRow ranking12 (1408+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_12 : ∀ i : Fin 128, VertexRow ranking12 (1536+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_13 : ∀ i : Fin 128, VertexRow ranking12 (1664+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_14 : ∀ i : Fin 128, VertexRow ranking12 (1792+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_15 : ∀ i : Fin 128, VertexRow ranking12 (1920+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_16 : ∀ i : Fin 128, VertexRow ranking12 (2048+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_17 : ∀ i : Fin 128, VertexRow ranking12 (2176+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_18 : ∀ i : Fin 128, VertexRow ranking12 (2304+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_19 : ∀ i : Fin 128, VertexRow ranking12 (2432+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_20 : ∀ i : Fin 128, VertexRow ranking12 (2560+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_21 : ∀ i : Fin 128, VertexRow ranking12 (2688+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_22 : ∀ i : Fin 128, VertexRow ranking12 (2816+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_23 : ∀ i : Fin 128, VertexRow ranking12 (2944+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_24 : ∀ i : Fin 128, VertexRow ranking12 (3072+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_25 : ∀ i : Fin 128, VertexRow ranking12 (3200+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_26 : ∀ i : Fin 128, VertexRow ranking12 (3328+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_27 : ∀ i : Fin 128, VertexRow ranking12 (3456+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_28 : ∀ i : Fin 128, VertexRow ranking12 (3584+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_29 : ∀ i : Fin 128, VertexRow ranking12 (3712+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_30 : ∀ i : Fin 128, VertexRow ranking12 (3840+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_31 : ∀ i : Fin 128, VertexRow ranking12 (3968+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_32 : ∀ i : Fin 128, VertexRow ranking12 (4096+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_33 : ∀ i : Fin 128, VertexRow ranking12 (4224+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_34 : ∀ i : Fin 128, VertexRow ranking12 (4352+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_35 : ∀ i : Fin 128, VertexRow ranking12 (4480+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_36 : ∀ i : Fin 128, VertexRow ranking12 (4608+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_37 : ∀ i : Fin 128, VertexRow ranking12 (4736+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_38 : ∀ i : Fin 128, VertexRow ranking12 (4864+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_39 : ∀ i : Fin 128, VertexRow ranking12 (4992+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_40 : ∀ i : Fin 48, VertexRow ranking12 (5120+i.val) := by
  unfold VertexRow
  decide

theorem vertex_12_all : ∀ u, 0 ≤ u → u < 5168 → VertexRow ranking12 u :=
  (join_ranges (fun u => VertexRow ranking12 u) 0 2560 5168 (join_ranges (fun u => VertexRow ranking12 u) 0 1280 2560 (join_ranges (fun u => VertexRow ranking12 u) 0 640 1280 (join_ranges (fun u => VertexRow ranking12 u) 0 256 640 (join_ranges (fun u => VertexRow ranking12 u) 0 128 256 (checked_range (fun u => VertexRow ranking12 u) 0 128 vertex_12_0) (checked_range (fun u => VertexRow ranking12 u) 128 128 vertex_12_1)) (join_ranges (fun u => VertexRow ranking12 u) 256 384 640 (checked_range (fun u => VertexRow ranking12 u) 256 128 vertex_12_2) (join_ranges (fun u => VertexRow ranking12 u) 384 512 640 (checked_range (fun u => VertexRow ranking12 u) 384 128 vertex_12_3) (checked_range (fun u => VertexRow ranking12 u) 512 128 vertex_12_4)))) (join_ranges (fun u => VertexRow ranking12 u) 640 896 1280 (join_ranges (fun u => VertexRow ranking12 u) 640 768 896 (checked_range (fun u => VertexRow ranking12 u) 640 128 vertex_12_5) (checked_range (fun u => VertexRow ranking12 u) 768 128 vertex_12_6)) (join_ranges (fun u => VertexRow ranking12 u) 896 1024 1280 (checked_range (fun u => VertexRow ranking12 u) 896 128 vertex_12_7) (join_ranges (fun u => VertexRow ranking12 u) 1024 1152 1280 (checked_range (fun u => VertexRow ranking12 u) 1024 128 vertex_12_8) (checked_range (fun u => VertexRow ranking12 u) 1152 128 vertex_12_9))))) (join_ranges (fun u => VertexRow ranking12 u) 1280 1920 2560 (join_ranges (fun u => VertexRow ranking12 u) 1280 1536 1920 (join_ranges (fun u => VertexRow ranking12 u) 1280 1408 1536 (checked_range (fun u => VertexRow ranking12 u) 1280 128 vertex_12_10) (checked_range (fun u => VertexRow ranking12 u) 1408 128 vertex_12_11)) (join_ranges (fun u => VertexRow ranking12 u) 1536 1664 1920 (checked_range (fun u => VertexRow ranking12 u) 1536 128 vertex_12_12) (join_ranges (fun u => VertexRow ranking12 u) 1664 1792 1920 (checked_range (fun u => VertexRow ranking12 u) 1664 128 vertex_12_13) (checked_range (fun u => VertexRow ranking12 u) 1792 128 vertex_12_14)))) (join_ranges (fun u => VertexRow ranking12 u) 1920 2176 2560 (join_ranges (fun u => VertexRow ranking12 u) 1920 2048 2176 (checked_range (fun u => VertexRow ranking12 u) 1920 128 vertex_12_15) (checked_range (fun u => VertexRow ranking12 u) 2048 128 vertex_12_16)) (join_ranges (fun u => VertexRow ranking12 u) 2176 2304 2560 (checked_range (fun u => VertexRow ranking12 u) 2176 128 vertex_12_17) (join_ranges (fun u => VertexRow ranking12 u) 2304 2432 2560 (checked_range (fun u => VertexRow ranking12 u) 2304 128 vertex_12_18) (checked_range (fun u => VertexRow ranking12 u) 2432 128 vertex_12_19)))))) (join_ranges (fun u => VertexRow ranking12 u) 2560 3840 5168 (join_ranges (fun u => VertexRow ranking12 u) 2560 3200 3840 (join_ranges (fun u => VertexRow ranking12 u) 2560 2816 3200 (join_ranges (fun u => VertexRow ranking12 u) 2560 2688 2816 (checked_range (fun u => VertexRow ranking12 u) 2560 128 vertex_12_20) (checked_range (fun u => VertexRow ranking12 u) 2688 128 vertex_12_21)) (join_ranges (fun u => VertexRow ranking12 u) 2816 2944 3200 (checked_range (fun u => VertexRow ranking12 u) 2816 128 vertex_12_22) (join_ranges (fun u => VertexRow ranking12 u) 2944 3072 3200 (checked_range (fun u => VertexRow ranking12 u) 2944 128 vertex_12_23) (checked_range (fun u => VertexRow ranking12 u) 3072 128 vertex_12_24)))) (join_ranges (fun u => VertexRow ranking12 u) 3200 3456 3840 (join_ranges (fun u => VertexRow ranking12 u) 3200 3328 3456 (checked_range (fun u => VertexRow ranking12 u) 3200 128 vertex_12_25) (checked_range (fun u => VertexRow ranking12 u) 3328 128 vertex_12_26)) (join_ranges (fun u => VertexRow ranking12 u) 3456 3584 3840 (checked_range (fun u => VertexRow ranking12 u) 3456 128 vertex_12_27) (join_ranges (fun u => VertexRow ranking12 u) 3584 3712 3840 (checked_range (fun u => VertexRow ranking12 u) 3584 128 vertex_12_28) (checked_range (fun u => VertexRow ranking12 u) 3712 128 vertex_12_29))))) (join_ranges (fun u => VertexRow ranking12 u) 3840 4480 5168 (join_ranges (fun u => VertexRow ranking12 u) 3840 4096 4480 (join_ranges (fun u => VertexRow ranking12 u) 3840 3968 4096 (checked_range (fun u => VertexRow ranking12 u) 3840 128 vertex_12_30) (checked_range (fun u => VertexRow ranking12 u) 3968 128 vertex_12_31)) (join_ranges (fun u => VertexRow ranking12 u) 4096 4224 4480 (checked_range (fun u => VertexRow ranking12 u) 4096 128 vertex_12_32) (join_ranges (fun u => VertexRow ranking12 u) 4224 4352 4480 (checked_range (fun u => VertexRow ranking12 u) 4224 128 vertex_12_33) (checked_range (fun u => VertexRow ranking12 u) 4352 128 vertex_12_34)))) (join_ranges (fun u => VertexRow ranking12 u) 4480 4864 5168 (join_ranges (fun u => VertexRow ranking12 u) 4480 4608 4864 (checked_range (fun u => VertexRow ranking12 u) 4480 128 vertex_12_35) (join_ranges (fun u => VertexRow ranking12 u) 4608 4736 4864 (checked_range (fun u => VertexRow ranking12 u) 4608 128 vertex_12_36) (checked_range (fun u => VertexRow ranking12 u) 4736 128 vertex_12_37))) (join_ranges (fun u => VertexRow ranking12 u) 4864 4992 5168 (checked_range (fun u => VertexRow ranking12 u) 4864 128 vertex_12_38) (join_ranges (fun u => VertexRow ranking12 u) 4992 5120 5168 (checked_range (fun u => VertexRow ranking12 u) 4992 128 vertex_12_39) (checked_range (fun u => VertexRow ranking12 u) 5120 48 vertex_12_40)))))))
theorem edge_12_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_2 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_3 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (384+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_4 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (512+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_5 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (640+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_6 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (768+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_7 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (896+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_8 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1024+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_9 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1152+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_10 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1280+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_11 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1408+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_12 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1536+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_13 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1664+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_14 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1792+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_15 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (1920+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_16 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2048+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_17 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2176+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_18 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2304+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_19 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2432+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_20 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2560+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_21 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2688+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_22 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2816+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_23 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (2944+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_24 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3072+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_25 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3200+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_26 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3328+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_27 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3456+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_28 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3584+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_29 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3712+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_30 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3840+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_31 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (3968+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_32 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4096+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_33 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4224+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_34 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4352+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_35 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4480+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_36 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4608+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_37 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4736+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_38 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4864+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_39 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data12 ranking12 (4992+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_40 : ∀ i : Fin 48, ∀ bit : Fin 2, EdgeRow data12 ranking12 (5120+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_12_all : ∀ u, 0 ≤ u → u < 5168 → ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 0 2560 5168 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 0 1280 2560 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 0 640 1280 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 0 256 640 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 0 128 edge_12_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 128 128 edge_12_1)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 256 384 640 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 256 128 edge_12_2) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 384 512 640 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 384 128 edge_12_3) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 512 128 edge_12_4)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 640 896 1280 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 640 768 896 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 640 128 edge_12_5) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 768 128 edge_12_6)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 896 1024 1280 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 896 128 edge_12_7) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1024 1152 1280 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1024 128 edge_12_8) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1152 128 edge_12_9))))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1280 1920 2560 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1280 1536 1920 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1280 1408 1536 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1280 128 edge_12_10) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1408 128 edge_12_11)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1536 1664 1920 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1536 128 edge_12_12) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1664 1792 1920 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1664 128 edge_12_13) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1792 128 edge_12_14)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1920 2176 2560 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1920 2048 2176 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 1920 128 edge_12_15) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2048 128 edge_12_16)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2176 2304 2560 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2176 128 edge_12_17) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2304 2432 2560 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2304 128 edge_12_18) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2432 128 edge_12_19)))))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2560 3840 5168 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2560 3200 3840 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2560 2816 3200 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2560 2688 2816 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2560 128 edge_12_20) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2688 128 edge_12_21)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2816 2944 3200 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2816 128 edge_12_22) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2944 3072 3200 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 2944 128 edge_12_23) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3072 128 edge_12_24)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3200 3456 3840 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3200 3328 3456 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3200 128 edge_12_25) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3328 128 edge_12_26)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3456 3584 3840 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3456 128 edge_12_27) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3584 3712 3840 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3584 128 edge_12_28) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3712 128 edge_12_29))))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3840 4480 5168 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3840 4096 4480 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3840 3968 4096 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3840 128 edge_12_30) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 3968 128 edge_12_31)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4096 4224 4480 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4096 128 edge_12_32) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4224 4352 4480 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4224 128 edge_12_33) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4352 128 edge_12_34)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4480 4864 5168 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4480 4608 4864 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4480 128 edge_12_35) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4608 4736 4864 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4608 128 edge_12_36) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4736 128 edge_12_37))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4864 4992 5168 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4864 128 edge_12_38) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4992 5120 5168 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 4992 128 edge_12_39) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data12 ranking12 u bit.val) 5120 48 edge_12_40)))))))
theorem checked_rank12 : CheckedRank data12 ranking12 := by
  constructor
  · intro u hu
    exact vertex_12_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_12_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_12_0 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_1 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_2 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_3 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_4 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (512+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_5 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (640+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_6 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (768+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_7 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (896+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_8 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1024+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_9 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1152+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_10 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1280+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_11 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1408+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_12 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1536+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_13 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1664+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_14 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1792+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_15 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (1920+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_16 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2048+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_17 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2176+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_18 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2304+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_19 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2432+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_20 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2560+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_21 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2688+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_22 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2816+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_23 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (2944+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_24 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3072+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_25 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3200+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_26 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3328+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_27 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3456+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_28 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3584+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_29 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3712+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_30 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3840+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_31 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (3968+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_32 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4096+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_33 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4224+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_34 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4352+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_35 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4480+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_36 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4608+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_37 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4736+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_38 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4864+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_39 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (4992+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_40 : ∀ i : Fin 128, CoverageRow data11 component11 3350 272 member12 memberIndex12 (5120+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_41 : ∀ i : Fin 15, CoverageRow data11 component11 3350 272 member12 memberIndex12 (5248+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_12_all : ∀ u, 0 ≤ u → u < 5263 → CoverageRow data11 component11 3350 272 member12 memberIndex12 u :=
  (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 0 2688 5263 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 0 1280 2688 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 0 640 1280 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 0 256 640 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 0 128 256 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 0 128 coverage_12_0) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 128 128 coverage_12_1)) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 256 384 640 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 256 128 coverage_12_2) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 384 512 640 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 384 128 coverage_12_3) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 512 128 coverage_12_4)))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 640 896 1280 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 640 768 896 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 640 128 coverage_12_5) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 768 128 coverage_12_6)) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 896 1024 1280 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 896 128 coverage_12_7) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1024 1152 1280 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1024 128 coverage_12_8) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1152 128 coverage_12_9))))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1280 1920 2688 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1280 1536 1920 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1280 1408 1536 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1280 128 coverage_12_10) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1408 128 coverage_12_11)) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1536 1664 1920 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1536 128 coverage_12_12) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1664 1792 1920 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1664 128 coverage_12_13) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1792 128 coverage_12_14)))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1920 2304 2688 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1920 2048 2304 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 1920 128 coverage_12_15) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2048 2176 2304 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2048 128 coverage_12_16) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2176 128 coverage_12_17))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2304 2432 2688 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2304 128 coverage_12_18) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2432 2560 2688 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2432 128 coverage_12_19) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2560 128 coverage_12_20)))))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2688 3968 5263 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2688 3328 3968 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2688 2944 3328 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2688 2816 2944 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2688 128 coverage_12_21) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2816 128 coverage_12_22)) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2944 3072 3328 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 2944 128 coverage_12_23) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3072 3200 3328 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3072 128 coverage_12_24) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3200 128 coverage_12_25)))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3328 3584 3968 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3328 3456 3584 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3328 128 coverage_12_26) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3456 128 coverage_12_27)) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3584 3712 3968 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3584 128 coverage_12_28) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3712 3840 3968 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3712 128 coverage_12_29) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3840 128 coverage_12_30))))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3968 4608 5263 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3968 4224 4608 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3968 4096 4224 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 3968 128 coverage_12_31) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4096 128 coverage_12_32)) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4224 4352 4608 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4224 128 coverage_12_33) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4352 4480 4608 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4352 128 coverage_12_34) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4480 128 coverage_12_35)))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4608 4992 5263 (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4608 4736 4992 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4608 128 coverage_12_36) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4736 4864 4992 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4736 128 coverage_12_37) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4864 128 coverage_12_38))) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4992 5120 5263 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 4992 128 coverage_12_39) (join_ranges (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 5120 5248 5263 (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 5120 128 coverage_12_40) (checked_range (fun u => CoverageRow data11 component11 3350 272 member12 memberIndex12 u) 5248 15 coverage_12_41)))))))
theorem field_12_0 : ∀ i : Fin 128, FieldRow data11 data12 member12 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_12_1 : ∀ i : Fin 128, FieldRow data11 data12 member12 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_12_2 : ∀ i : Fin 128, FieldRow data11 data12 member12 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_12_3 : ∀ i : Fin 128, FieldRow data11 data12 member12 (384+i.val) := by
  unfold FieldRow
  decide

theorem field_12_4 : ∀ i : Fin 128, FieldRow data11 data12 member12 (512+i.val) := by
  unfold FieldRow
  decide

theorem field_12_5 : ∀ i : Fin 128, FieldRow data11 data12 member12 (640+i.val) := by
  unfold FieldRow
  decide

theorem field_12_6 : ∀ i : Fin 128, FieldRow data11 data12 member12 (768+i.val) := by
  unfold FieldRow
  decide

theorem field_12_7 : ∀ i : Fin 128, FieldRow data11 data12 member12 (896+i.val) := by
  unfold FieldRow
  decide

theorem field_12_8 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1024+i.val) := by
  unfold FieldRow
  decide

theorem field_12_9 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1152+i.val) := by
  unfold FieldRow
  decide

theorem field_12_10 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1280+i.val) := by
  unfold FieldRow
  decide

theorem field_12_11 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1408+i.val) := by
  unfold FieldRow
  decide

theorem field_12_12 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1536+i.val) := by
  unfold FieldRow
  decide

theorem field_12_13 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1664+i.val) := by
  unfold FieldRow
  decide

theorem field_12_14 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1792+i.val) := by
  unfold FieldRow
  decide

theorem field_12_15 : ∀ i : Fin 128, FieldRow data11 data12 member12 (1920+i.val) := by
  unfold FieldRow
  decide

theorem field_12_16 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2048+i.val) := by
  unfold FieldRow
  decide

theorem field_12_17 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2176+i.val) := by
  unfold FieldRow
  decide

theorem field_12_18 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2304+i.val) := by
  unfold FieldRow
  decide

theorem field_12_19 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2432+i.val) := by
  unfold FieldRow
  decide

theorem field_12_20 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2560+i.val) := by
  unfold FieldRow
  decide

theorem field_12_21 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2688+i.val) := by
  unfold FieldRow
  decide

theorem field_12_22 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2816+i.val) := by
  unfold FieldRow
  decide

theorem field_12_23 : ∀ i : Fin 128, FieldRow data11 data12 member12 (2944+i.val) := by
  unfold FieldRow
  decide

theorem field_12_24 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3072+i.val) := by
  unfold FieldRow
  decide

theorem field_12_25 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3200+i.val) := by
  unfold FieldRow
  decide

theorem field_12_26 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3328+i.val) := by
  unfold FieldRow
  decide

theorem field_12_27 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3456+i.val) := by
  unfold FieldRow
  decide

theorem field_12_28 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3584+i.val) := by
  unfold FieldRow
  decide

theorem field_12_29 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3712+i.val) := by
  unfold FieldRow
  decide

theorem field_12_30 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3840+i.val) := by
  unfold FieldRow
  decide

theorem field_12_31 : ∀ i : Fin 128, FieldRow data11 data12 member12 (3968+i.val) := by
  unfold FieldRow
  decide

theorem field_12_32 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4096+i.val) := by
  unfold FieldRow
  decide

theorem field_12_33 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4224+i.val) := by
  unfold FieldRow
  decide

theorem field_12_34 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4352+i.val) := by
  unfold FieldRow
  decide

theorem field_12_35 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4480+i.val) := by
  unfold FieldRow
  decide

theorem field_12_36 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4608+i.val) := by
  unfold FieldRow
  decide

theorem field_12_37 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4736+i.val) := by
  unfold FieldRow
  decide

theorem field_12_38 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4864+i.val) := by
  unfold FieldRow
  decide

theorem field_12_39 : ∀ i : Fin 128, FieldRow data11 data12 member12 (4992+i.val) := by
  unfold FieldRow
  decide

theorem field_12_40 : ∀ i : Fin 48, FieldRow data11 data12 member12 (5120+i.val) := by
  unfold FieldRow
  decide

theorem field_12_all : ∀ u, 0 ≤ u → u < 5168 → FieldRow data11 data12 member12 u :=
  (join_ranges (fun u => FieldRow data11 data12 member12 u) 0 2560 5168 (join_ranges (fun u => FieldRow data11 data12 member12 u) 0 1280 2560 (join_ranges (fun u => FieldRow data11 data12 member12 u) 0 640 1280 (join_ranges (fun u => FieldRow data11 data12 member12 u) 0 256 640 (join_ranges (fun u => FieldRow data11 data12 member12 u) 0 128 256 (checked_range (fun u => FieldRow data11 data12 member12 u) 0 128 field_12_0) (checked_range (fun u => FieldRow data11 data12 member12 u) 128 128 field_12_1)) (join_ranges (fun u => FieldRow data11 data12 member12 u) 256 384 640 (checked_range (fun u => FieldRow data11 data12 member12 u) 256 128 field_12_2) (join_ranges (fun u => FieldRow data11 data12 member12 u) 384 512 640 (checked_range (fun u => FieldRow data11 data12 member12 u) 384 128 field_12_3) (checked_range (fun u => FieldRow data11 data12 member12 u) 512 128 field_12_4)))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 640 896 1280 (join_ranges (fun u => FieldRow data11 data12 member12 u) 640 768 896 (checked_range (fun u => FieldRow data11 data12 member12 u) 640 128 field_12_5) (checked_range (fun u => FieldRow data11 data12 member12 u) 768 128 field_12_6)) (join_ranges (fun u => FieldRow data11 data12 member12 u) 896 1024 1280 (checked_range (fun u => FieldRow data11 data12 member12 u) 896 128 field_12_7) (join_ranges (fun u => FieldRow data11 data12 member12 u) 1024 1152 1280 (checked_range (fun u => FieldRow data11 data12 member12 u) 1024 128 field_12_8) (checked_range (fun u => FieldRow data11 data12 member12 u) 1152 128 field_12_9))))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 1280 1920 2560 (join_ranges (fun u => FieldRow data11 data12 member12 u) 1280 1536 1920 (join_ranges (fun u => FieldRow data11 data12 member12 u) 1280 1408 1536 (checked_range (fun u => FieldRow data11 data12 member12 u) 1280 128 field_12_10) (checked_range (fun u => FieldRow data11 data12 member12 u) 1408 128 field_12_11)) (join_ranges (fun u => FieldRow data11 data12 member12 u) 1536 1664 1920 (checked_range (fun u => FieldRow data11 data12 member12 u) 1536 128 field_12_12) (join_ranges (fun u => FieldRow data11 data12 member12 u) 1664 1792 1920 (checked_range (fun u => FieldRow data11 data12 member12 u) 1664 128 field_12_13) (checked_range (fun u => FieldRow data11 data12 member12 u) 1792 128 field_12_14)))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 1920 2176 2560 (join_ranges (fun u => FieldRow data11 data12 member12 u) 1920 2048 2176 (checked_range (fun u => FieldRow data11 data12 member12 u) 1920 128 field_12_15) (checked_range (fun u => FieldRow data11 data12 member12 u) 2048 128 field_12_16)) (join_ranges (fun u => FieldRow data11 data12 member12 u) 2176 2304 2560 (checked_range (fun u => FieldRow data11 data12 member12 u) 2176 128 field_12_17) (join_ranges (fun u => FieldRow data11 data12 member12 u) 2304 2432 2560 (checked_range (fun u => FieldRow data11 data12 member12 u) 2304 128 field_12_18) (checked_range (fun u => FieldRow data11 data12 member12 u) 2432 128 field_12_19)))))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 2560 3840 5168 (join_ranges (fun u => FieldRow data11 data12 member12 u) 2560 3200 3840 (join_ranges (fun u => FieldRow data11 data12 member12 u) 2560 2816 3200 (join_ranges (fun u => FieldRow data11 data12 member12 u) 2560 2688 2816 (checked_range (fun u => FieldRow data11 data12 member12 u) 2560 128 field_12_20) (checked_range (fun u => FieldRow data11 data12 member12 u) 2688 128 field_12_21)) (join_ranges (fun u => FieldRow data11 data12 member12 u) 2816 2944 3200 (checked_range (fun u => FieldRow data11 data12 member12 u) 2816 128 field_12_22) (join_ranges (fun u => FieldRow data11 data12 member12 u) 2944 3072 3200 (checked_range (fun u => FieldRow data11 data12 member12 u) 2944 128 field_12_23) (checked_range (fun u => FieldRow data11 data12 member12 u) 3072 128 field_12_24)))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 3200 3456 3840 (join_ranges (fun u => FieldRow data11 data12 member12 u) 3200 3328 3456 (checked_range (fun u => FieldRow data11 data12 member12 u) 3200 128 field_12_25) (checked_range (fun u => FieldRow data11 data12 member12 u) 3328 128 field_12_26)) (join_ranges (fun u => FieldRow data11 data12 member12 u) 3456 3584 3840 (checked_range (fun u => FieldRow data11 data12 member12 u) 3456 128 field_12_27) (join_ranges (fun u => FieldRow data11 data12 member12 u) 3584 3712 3840 (checked_range (fun u => FieldRow data11 data12 member12 u) 3584 128 field_12_28) (checked_range (fun u => FieldRow data11 data12 member12 u) 3712 128 field_12_29))))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 3840 4480 5168 (join_ranges (fun u => FieldRow data11 data12 member12 u) 3840 4096 4480 (join_ranges (fun u => FieldRow data11 data12 member12 u) 3840 3968 4096 (checked_range (fun u => FieldRow data11 data12 member12 u) 3840 128 field_12_30) (checked_range (fun u => FieldRow data11 data12 member12 u) 3968 128 field_12_31)) (join_ranges (fun u => FieldRow data11 data12 member12 u) 4096 4224 4480 (checked_range (fun u => FieldRow data11 data12 member12 u) 4096 128 field_12_32) (join_ranges (fun u => FieldRow data11 data12 member12 u) 4224 4352 4480 (checked_range (fun u => FieldRow data11 data12 member12 u) 4224 128 field_12_33) (checked_range (fun u => FieldRow data11 data12 member12 u) 4352 128 field_12_34)))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 4480 4864 5168 (join_ranges (fun u => FieldRow data11 data12 member12 u) 4480 4608 4864 (checked_range (fun u => FieldRow data11 data12 member12 u) 4480 128 field_12_35) (join_ranges (fun u => FieldRow data11 data12 member12 u) 4608 4736 4864 (checked_range (fun u => FieldRow data11 data12 member12 u) 4608 128 field_12_36) (checked_range (fun u => FieldRow data11 data12 member12 u) 4736 128 field_12_37))) (join_ranges (fun u => FieldRow data11 data12 member12 u) 4864 4992 5168 (checked_range (fun u => FieldRow data11 data12 member12 u) 4864 128 field_12_38) (join_ranges (fun u => FieldRow data11 data12 member12 u) 4992 5120 5168 (checked_range (fun u => FieldRow data11 data12 member12 u) 4992 128 field_12_39) (checked_range (fun u => FieldRow data11 data12 member12 u) 5120 48 field_12_40)))))))
theorem lift_12_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_3 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_4 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (512+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_5 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (640+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_6 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (768+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_7 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (896+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_8 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1024+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_9 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1152+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_10 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1280+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_11 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1408+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_12 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1536+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_13 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1664+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_14 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1792+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_15 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (1920+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_16 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2048+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_17 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2176+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_18 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2304+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_19 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2432+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_20 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2560+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_21 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2688+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_22 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2816+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_23 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (2944+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_24 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3072+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_25 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3200+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_26 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3328+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_27 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3456+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_28 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3584+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_29 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3712+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_30 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3840+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_31 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (3968+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_32 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4096+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_33 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4224+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_34 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4352+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_35 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4480+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_36 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4608+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_37 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4736+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_38 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4864+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_39 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (4992+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_40 : ∀ i : Fin 48, ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 (5120+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_12_all : ∀ u, 0 ≤ u → u < 5168 → ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 0 2560 5168 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 0 1280 2560 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 0 640 1280 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 0 256 640 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 0 128 lift_12_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 128 128 lift_12_1)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 256 384 640 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 256 128 lift_12_2) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 384 512 640 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 384 128 lift_12_3) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 512 128 lift_12_4)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 640 896 1280 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 640 768 896 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 640 128 lift_12_5) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 768 128 lift_12_6)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 896 1024 1280 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 896 128 lift_12_7) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1024 1152 1280 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1024 128 lift_12_8) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1152 128 lift_12_9))))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1280 1920 2560 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1280 1536 1920 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1280 1408 1536 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1280 128 lift_12_10) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1408 128 lift_12_11)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1536 1664 1920 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1536 128 lift_12_12) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1664 1792 1920 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1664 128 lift_12_13) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1792 128 lift_12_14)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1920 2176 2560 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1920 2048 2176 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 1920 128 lift_12_15) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2048 128 lift_12_16)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2176 2304 2560 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2176 128 lift_12_17) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2304 2432 2560 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2304 128 lift_12_18) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2432 128 lift_12_19)))))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2560 3840 5168 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2560 3200 3840 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2560 2816 3200 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2560 2688 2816 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2560 128 lift_12_20) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2688 128 lift_12_21)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2816 2944 3200 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2816 128 lift_12_22) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2944 3072 3200 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 2944 128 lift_12_23) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3072 128 lift_12_24)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3200 3456 3840 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3200 3328 3456 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3200 128 lift_12_25) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3328 128 lift_12_26)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3456 3584 3840 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3456 128 lift_12_27) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3584 3712 3840 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3584 128 lift_12_28) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3712 128 lift_12_29))))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3840 4480 5168 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3840 4096 4480 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3840 3968 4096 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3840 128 lift_12_30) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 3968 128 lift_12_31)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4096 4224 4480 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4096 128 lift_12_32) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4224 4352 4480 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4224 128 lift_12_33) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4352 128 lift_12_34)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4480 4864 5168 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4480 4608 4864 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4480 128 lift_12_35) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4608 4736 4864 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4608 128 lift_12_36) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4736 128 lift_12_37))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4864 4992 5168 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4864 128 lift_12_38) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4992 5120 5168 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 4992 128 lift_12_39) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data11 data12 component11 3350 member12 memberIndex12 u bit.val) 5120 48 lift_12_40)))))))
def lift_certificate12 : LiftCertificate data11 data12 component11 3350 where
  members := member12
  memberIndex := memberIndex12
  count := 272
  size_eq := rfl
  coverage u hu := coverage_12_all u (Nat.zero_le u) hu
  fields u hu := field_12_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_12_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete12 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data11)
      (fun v => component11 v=3350)))) (graph data12)
      (encode lift_certificate12) := lift_realization lift_certificate12
end ScalarJobData
