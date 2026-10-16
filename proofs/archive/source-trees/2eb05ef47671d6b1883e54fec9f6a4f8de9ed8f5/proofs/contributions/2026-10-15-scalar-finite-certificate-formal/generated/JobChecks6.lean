import JobData6
import RangeChecks
import JobData5
namespace ScalarJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_6_0 : ∀ i : Fin 128, VertexRow ranking6 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_1 : ∀ i : Fin 128, VertexRow ranking6 (128+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_2 : ∀ i : Fin 128, VertexRow ranking6 (256+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_3 : ∀ i : Fin 128, VertexRow ranking6 (384+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_4 : ∀ i : Fin 128, VertexRow ranking6 (512+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_5 : ∀ i : Fin 128, VertexRow ranking6 (640+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_6 : ∀ i : Fin 128, VertexRow ranking6 (768+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_7 : ∀ i : Fin 128, VertexRow ranking6 (896+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_8 : ∀ i : Fin 128, VertexRow ranking6 (1024+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_9 : ∀ i : Fin 128, VertexRow ranking6 (1152+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_10 : ∀ i : Fin 128, VertexRow ranking6 (1280+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_11 : ∀ i : Fin 128, VertexRow ranking6 (1408+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_12 : ∀ i : Fin 128, VertexRow ranking6 (1536+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_13 : ∀ i : Fin 128, VertexRow ranking6 (1664+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_14 : ∀ i : Fin 128, VertexRow ranking6 (1792+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_15 : ∀ i : Fin 128, VertexRow ranking6 (1920+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_16 : ∀ i : Fin 128, VertexRow ranking6 (2048+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_17 : ∀ i : Fin 128, VertexRow ranking6 (2176+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_18 : ∀ i : Fin 128, VertexRow ranking6 (2304+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_19 : ∀ i : Fin 128, VertexRow ranking6 (2432+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_20 : ∀ i : Fin 128, VertexRow ranking6 (2560+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_21 : ∀ i : Fin 128, VertexRow ranking6 (2688+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_22 : ∀ i : Fin 128, VertexRow ranking6 (2816+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_23 : ∀ i : Fin 128, VertexRow ranking6 (2944+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_24 : ∀ i : Fin 128, VertexRow ranking6 (3072+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_25 : ∀ i : Fin 128, VertexRow ranking6 (3200+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_26 : ∀ i : Fin 128, VertexRow ranking6 (3328+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_27 : ∀ i : Fin 128, VertexRow ranking6 (3456+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_28 : ∀ i : Fin 128, VertexRow ranking6 (3584+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_29 : ∀ i : Fin 128, VertexRow ranking6 (3712+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_30 : ∀ i : Fin 128, VertexRow ranking6 (3840+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_31 : ∀ i : Fin 128, VertexRow ranking6 (3968+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_32 : ∀ i : Fin 128, VertexRow ranking6 (4096+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_33 : ∀ i : Fin 89, VertexRow ranking6 (4224+i.val) := by
  unfold VertexRow
  decide

theorem vertex_6_all : ∀ u, 0 ≤ u → u < 4313 → VertexRow ranking6 u :=
  (join_ranges (fun u => VertexRow ranking6 u) 0 2176 4313 (join_ranges (fun u => VertexRow ranking6 u) 0 1024 2176 (join_ranges (fun u => VertexRow ranking6 u) 0 512 1024 (join_ranges (fun u => VertexRow ranking6 u) 0 256 512 (join_ranges (fun u => VertexRow ranking6 u) 0 128 256 (checked_range (fun u => VertexRow ranking6 u) 0 128 vertex_6_0) (checked_range (fun u => VertexRow ranking6 u) 128 128 vertex_6_1)) (join_ranges (fun u => VertexRow ranking6 u) 256 384 512 (checked_range (fun u => VertexRow ranking6 u) 256 128 vertex_6_2) (checked_range (fun u => VertexRow ranking6 u) 384 128 vertex_6_3))) (join_ranges (fun u => VertexRow ranking6 u) 512 768 1024 (join_ranges (fun u => VertexRow ranking6 u) 512 640 768 (checked_range (fun u => VertexRow ranking6 u) 512 128 vertex_6_4) (checked_range (fun u => VertexRow ranking6 u) 640 128 vertex_6_5)) (join_ranges (fun u => VertexRow ranking6 u) 768 896 1024 (checked_range (fun u => VertexRow ranking6 u) 768 128 vertex_6_6) (checked_range (fun u => VertexRow ranking6 u) 896 128 vertex_6_7)))) (join_ranges (fun u => VertexRow ranking6 u) 1024 1536 2176 (join_ranges (fun u => VertexRow ranking6 u) 1024 1280 1536 (join_ranges (fun u => VertexRow ranking6 u) 1024 1152 1280 (checked_range (fun u => VertexRow ranking6 u) 1024 128 vertex_6_8) (checked_range (fun u => VertexRow ranking6 u) 1152 128 vertex_6_9)) (join_ranges (fun u => VertexRow ranking6 u) 1280 1408 1536 (checked_range (fun u => VertexRow ranking6 u) 1280 128 vertex_6_10) (checked_range (fun u => VertexRow ranking6 u) 1408 128 vertex_6_11))) (join_ranges (fun u => VertexRow ranking6 u) 1536 1792 2176 (join_ranges (fun u => VertexRow ranking6 u) 1536 1664 1792 (checked_range (fun u => VertexRow ranking6 u) 1536 128 vertex_6_12) (checked_range (fun u => VertexRow ranking6 u) 1664 128 vertex_6_13)) (join_ranges (fun u => VertexRow ranking6 u) 1792 1920 2176 (checked_range (fun u => VertexRow ranking6 u) 1792 128 vertex_6_14) (join_ranges (fun u => VertexRow ranking6 u) 1920 2048 2176 (checked_range (fun u => VertexRow ranking6 u) 1920 128 vertex_6_15) (checked_range (fun u => VertexRow ranking6 u) 2048 128 vertex_6_16)))))) (join_ranges (fun u => VertexRow ranking6 u) 2176 3200 4313 (join_ranges (fun u => VertexRow ranking6 u) 2176 2688 3200 (join_ranges (fun u => VertexRow ranking6 u) 2176 2432 2688 (join_ranges (fun u => VertexRow ranking6 u) 2176 2304 2432 (checked_range (fun u => VertexRow ranking6 u) 2176 128 vertex_6_17) (checked_range (fun u => VertexRow ranking6 u) 2304 128 vertex_6_18)) (join_ranges (fun u => VertexRow ranking6 u) 2432 2560 2688 (checked_range (fun u => VertexRow ranking6 u) 2432 128 vertex_6_19) (checked_range (fun u => VertexRow ranking6 u) 2560 128 vertex_6_20))) (join_ranges (fun u => VertexRow ranking6 u) 2688 2944 3200 (join_ranges (fun u => VertexRow ranking6 u) 2688 2816 2944 (checked_range (fun u => VertexRow ranking6 u) 2688 128 vertex_6_21) (checked_range (fun u => VertexRow ranking6 u) 2816 128 vertex_6_22)) (join_ranges (fun u => VertexRow ranking6 u) 2944 3072 3200 (checked_range (fun u => VertexRow ranking6 u) 2944 128 vertex_6_23) (checked_range (fun u => VertexRow ranking6 u) 3072 128 vertex_6_24)))) (join_ranges (fun u => VertexRow ranking6 u) 3200 3712 4313 (join_ranges (fun u => VertexRow ranking6 u) 3200 3456 3712 (join_ranges (fun u => VertexRow ranking6 u) 3200 3328 3456 (checked_range (fun u => VertexRow ranking6 u) 3200 128 vertex_6_25) (checked_range (fun u => VertexRow ranking6 u) 3328 128 vertex_6_26)) (join_ranges (fun u => VertexRow ranking6 u) 3456 3584 3712 (checked_range (fun u => VertexRow ranking6 u) 3456 128 vertex_6_27) (checked_range (fun u => VertexRow ranking6 u) 3584 128 vertex_6_28))) (join_ranges (fun u => VertexRow ranking6 u) 3712 3968 4313 (join_ranges (fun u => VertexRow ranking6 u) 3712 3840 3968 (checked_range (fun u => VertexRow ranking6 u) 3712 128 vertex_6_29) (checked_range (fun u => VertexRow ranking6 u) 3840 128 vertex_6_30)) (join_ranges (fun u => VertexRow ranking6 u) 3968 4096 4313 (checked_range (fun u => VertexRow ranking6 u) 3968 128 vertex_6_31) (join_ranges (fun u => VertexRow ranking6 u) 4096 4224 4313 (checked_range (fun u => VertexRow ranking6 u) 4096 128 vertex_6_32) (checked_range (fun u => VertexRow ranking6 u) 4224 89 vertex_6_33)))))))
theorem edge_6_0 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_1 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (128+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_2 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (256+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_3 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (384+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_4 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (512+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_5 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (640+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_6 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (768+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_7 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (896+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_8 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1024+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_9 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1152+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_10 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1280+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_11 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1408+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_12 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1536+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_13 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1664+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_14 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1792+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_15 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (1920+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_16 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2048+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_17 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2176+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_18 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2304+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_19 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2432+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_20 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2560+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_21 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2688+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_22 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2816+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_23 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (2944+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_24 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3072+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_25 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3200+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_26 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3328+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_27 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3456+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_28 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3584+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_29 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3712+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_30 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3840+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_31 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (3968+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_32 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data6 ranking6 (4096+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_33 : ∀ i : Fin 89, ∀ bit : Fin 2, EdgeRow data6 ranking6 (4224+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_6_all : ∀ u, 0 ≤ u → u < 4313 → ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 0 2176 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 0 1024 2176 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 0 512 1024 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 0 128 edge_6_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 128 128 edge_6_1)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 256 128 edge_6_2) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 384 128 edge_6_3))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 512 768 1024 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 512 128 edge_6_4) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 640 128 edge_6_5)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 768 896 1024 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 768 128 edge_6_6) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 896 128 edge_6_7)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1024 1536 2176 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1024 1280 1536 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1024 1152 1280 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1024 128 edge_6_8) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1152 128 edge_6_9)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1280 1408 1536 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1280 128 edge_6_10) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1408 128 edge_6_11))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1536 1792 2176 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1536 1664 1792 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1536 128 edge_6_12) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1664 128 edge_6_13)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1792 1920 2176 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1792 128 edge_6_14) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1920 2048 2176 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 1920 128 edge_6_15) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2048 128 edge_6_16)))))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2176 3200 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2176 2688 3200 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2176 2432 2688 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2176 2304 2432 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2176 128 edge_6_17) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2304 128 edge_6_18)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2432 2560 2688 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2432 128 edge_6_19) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2560 128 edge_6_20))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2688 2944 3200 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2688 2816 2944 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2688 128 edge_6_21) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2816 128 edge_6_22)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2944 3072 3200 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 2944 128 edge_6_23) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3072 128 edge_6_24)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3200 3712 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3200 3456 3712 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3200 3328 3456 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3200 128 edge_6_25) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3328 128 edge_6_26)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3456 3584 3712 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3456 128 edge_6_27) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3584 128 edge_6_28))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3712 3968 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3712 3840 3968 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3712 128 edge_6_29) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3840 128 edge_6_30)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3968 4096 4313 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 3968 128 edge_6_31) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 4096 4224 4313 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 4096 128 edge_6_32) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data6 ranking6 u bit.val) 4224 89 edge_6_33)))))))
theorem checked_rank6 : CheckedRank data6 ranking6 := by
  constructor
  · intro u hu
    exact vertex_6_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_6_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_6_0 : ∀ i : Fin 128, CoverageRow data5 component5 459 227 member6 memberIndex6 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_1 : ∀ i : Fin 128, CoverageRow data5 component5 459 227 member6 memberIndex6 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_2 : ∀ i : Fin 128, CoverageRow data5 component5 459 227 member6 memberIndex6 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_3 : ∀ i : Fin 128, CoverageRow data5 component5 459 227 member6 memberIndex6 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_4 : ∀ i : Fin 128, CoverageRow data5 component5 459 227 member6 memberIndex6 (512+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_5 : ∀ i : Fin 128, CoverageRow data5 component5 459 227 member6 memberIndex6 (640+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_6 : ∀ i : Fin 128, CoverageRow data5 component5 459 227 member6 memberIndex6 (768+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_7 : ∀ i : Fin 54, CoverageRow data5 component5 459 227 member6 memberIndex6 (896+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_6_all : ∀ u, 0 ≤ u → u < 950 → CoverageRow data5 component5 459 227 member6 memberIndex6 u :=
  (join_ranges (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 0 512 950 (join_ranges (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 0 256 512 (join_ranges (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 0 128 256 (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 0 128 coverage_6_0) (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 128 128 coverage_6_1)) (join_ranges (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 256 384 512 (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 256 128 coverage_6_2) (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 384 128 coverage_6_3))) (join_ranges (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 512 768 950 (join_ranges (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 512 640 768 (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 512 128 coverage_6_4) (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 640 128 coverage_6_5)) (join_ranges (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 768 896 950 (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 768 128 coverage_6_6) (checked_range (fun u => CoverageRow data5 component5 459 227 member6 memberIndex6 u) 896 54 coverage_6_7))))
theorem field_6_0 : ∀ i : Fin 128, FieldRow data5 data6 member6 (0+i.val) := by
  unfold FieldRow
  decide

theorem field_6_1 : ∀ i : Fin 128, FieldRow data5 data6 member6 (128+i.val) := by
  unfold FieldRow
  decide

theorem field_6_2 : ∀ i : Fin 128, FieldRow data5 data6 member6 (256+i.val) := by
  unfold FieldRow
  decide

theorem field_6_3 : ∀ i : Fin 128, FieldRow data5 data6 member6 (384+i.val) := by
  unfold FieldRow
  decide

theorem field_6_4 : ∀ i : Fin 128, FieldRow data5 data6 member6 (512+i.val) := by
  unfold FieldRow
  decide

theorem field_6_5 : ∀ i : Fin 128, FieldRow data5 data6 member6 (640+i.val) := by
  unfold FieldRow
  decide

theorem field_6_6 : ∀ i : Fin 128, FieldRow data5 data6 member6 (768+i.val) := by
  unfold FieldRow
  decide

theorem field_6_7 : ∀ i : Fin 128, FieldRow data5 data6 member6 (896+i.val) := by
  unfold FieldRow
  decide

theorem field_6_8 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1024+i.val) := by
  unfold FieldRow
  decide

theorem field_6_9 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1152+i.val) := by
  unfold FieldRow
  decide

theorem field_6_10 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1280+i.val) := by
  unfold FieldRow
  decide

theorem field_6_11 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1408+i.val) := by
  unfold FieldRow
  decide

theorem field_6_12 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1536+i.val) := by
  unfold FieldRow
  decide

theorem field_6_13 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1664+i.val) := by
  unfold FieldRow
  decide

theorem field_6_14 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1792+i.val) := by
  unfold FieldRow
  decide

theorem field_6_15 : ∀ i : Fin 128, FieldRow data5 data6 member6 (1920+i.val) := by
  unfold FieldRow
  decide

theorem field_6_16 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2048+i.val) := by
  unfold FieldRow
  decide

theorem field_6_17 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2176+i.val) := by
  unfold FieldRow
  decide

theorem field_6_18 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2304+i.val) := by
  unfold FieldRow
  decide

theorem field_6_19 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2432+i.val) := by
  unfold FieldRow
  decide

theorem field_6_20 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2560+i.val) := by
  unfold FieldRow
  decide

theorem field_6_21 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2688+i.val) := by
  unfold FieldRow
  decide

theorem field_6_22 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2816+i.val) := by
  unfold FieldRow
  decide

theorem field_6_23 : ∀ i : Fin 128, FieldRow data5 data6 member6 (2944+i.val) := by
  unfold FieldRow
  decide

theorem field_6_24 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3072+i.val) := by
  unfold FieldRow
  decide

theorem field_6_25 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3200+i.val) := by
  unfold FieldRow
  decide

theorem field_6_26 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3328+i.val) := by
  unfold FieldRow
  decide

theorem field_6_27 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3456+i.val) := by
  unfold FieldRow
  decide

theorem field_6_28 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3584+i.val) := by
  unfold FieldRow
  decide

theorem field_6_29 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3712+i.val) := by
  unfold FieldRow
  decide

theorem field_6_30 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3840+i.val) := by
  unfold FieldRow
  decide

theorem field_6_31 : ∀ i : Fin 128, FieldRow data5 data6 member6 (3968+i.val) := by
  unfold FieldRow
  decide

theorem field_6_32 : ∀ i : Fin 128, FieldRow data5 data6 member6 (4096+i.val) := by
  unfold FieldRow
  decide

theorem field_6_33 : ∀ i : Fin 89, FieldRow data5 data6 member6 (4224+i.val) := by
  unfold FieldRow
  decide

theorem field_6_all : ∀ u, 0 ≤ u → u < 4313 → FieldRow data5 data6 member6 u :=
  (join_ranges (fun u => FieldRow data5 data6 member6 u) 0 2176 4313 (join_ranges (fun u => FieldRow data5 data6 member6 u) 0 1024 2176 (join_ranges (fun u => FieldRow data5 data6 member6 u) 0 512 1024 (join_ranges (fun u => FieldRow data5 data6 member6 u) 0 256 512 (join_ranges (fun u => FieldRow data5 data6 member6 u) 0 128 256 (checked_range (fun u => FieldRow data5 data6 member6 u) 0 128 field_6_0) (checked_range (fun u => FieldRow data5 data6 member6 u) 128 128 field_6_1)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 256 384 512 (checked_range (fun u => FieldRow data5 data6 member6 u) 256 128 field_6_2) (checked_range (fun u => FieldRow data5 data6 member6 u) 384 128 field_6_3))) (join_ranges (fun u => FieldRow data5 data6 member6 u) 512 768 1024 (join_ranges (fun u => FieldRow data5 data6 member6 u) 512 640 768 (checked_range (fun u => FieldRow data5 data6 member6 u) 512 128 field_6_4) (checked_range (fun u => FieldRow data5 data6 member6 u) 640 128 field_6_5)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 768 896 1024 (checked_range (fun u => FieldRow data5 data6 member6 u) 768 128 field_6_6) (checked_range (fun u => FieldRow data5 data6 member6 u) 896 128 field_6_7)))) (join_ranges (fun u => FieldRow data5 data6 member6 u) 1024 1536 2176 (join_ranges (fun u => FieldRow data5 data6 member6 u) 1024 1280 1536 (join_ranges (fun u => FieldRow data5 data6 member6 u) 1024 1152 1280 (checked_range (fun u => FieldRow data5 data6 member6 u) 1024 128 field_6_8) (checked_range (fun u => FieldRow data5 data6 member6 u) 1152 128 field_6_9)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 1280 1408 1536 (checked_range (fun u => FieldRow data5 data6 member6 u) 1280 128 field_6_10) (checked_range (fun u => FieldRow data5 data6 member6 u) 1408 128 field_6_11))) (join_ranges (fun u => FieldRow data5 data6 member6 u) 1536 1792 2176 (join_ranges (fun u => FieldRow data5 data6 member6 u) 1536 1664 1792 (checked_range (fun u => FieldRow data5 data6 member6 u) 1536 128 field_6_12) (checked_range (fun u => FieldRow data5 data6 member6 u) 1664 128 field_6_13)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 1792 1920 2176 (checked_range (fun u => FieldRow data5 data6 member6 u) 1792 128 field_6_14) (join_ranges (fun u => FieldRow data5 data6 member6 u) 1920 2048 2176 (checked_range (fun u => FieldRow data5 data6 member6 u) 1920 128 field_6_15) (checked_range (fun u => FieldRow data5 data6 member6 u) 2048 128 field_6_16)))))) (join_ranges (fun u => FieldRow data5 data6 member6 u) 2176 3200 4313 (join_ranges (fun u => FieldRow data5 data6 member6 u) 2176 2688 3200 (join_ranges (fun u => FieldRow data5 data6 member6 u) 2176 2432 2688 (join_ranges (fun u => FieldRow data5 data6 member6 u) 2176 2304 2432 (checked_range (fun u => FieldRow data5 data6 member6 u) 2176 128 field_6_17) (checked_range (fun u => FieldRow data5 data6 member6 u) 2304 128 field_6_18)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 2432 2560 2688 (checked_range (fun u => FieldRow data5 data6 member6 u) 2432 128 field_6_19) (checked_range (fun u => FieldRow data5 data6 member6 u) 2560 128 field_6_20))) (join_ranges (fun u => FieldRow data5 data6 member6 u) 2688 2944 3200 (join_ranges (fun u => FieldRow data5 data6 member6 u) 2688 2816 2944 (checked_range (fun u => FieldRow data5 data6 member6 u) 2688 128 field_6_21) (checked_range (fun u => FieldRow data5 data6 member6 u) 2816 128 field_6_22)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 2944 3072 3200 (checked_range (fun u => FieldRow data5 data6 member6 u) 2944 128 field_6_23) (checked_range (fun u => FieldRow data5 data6 member6 u) 3072 128 field_6_24)))) (join_ranges (fun u => FieldRow data5 data6 member6 u) 3200 3712 4313 (join_ranges (fun u => FieldRow data5 data6 member6 u) 3200 3456 3712 (join_ranges (fun u => FieldRow data5 data6 member6 u) 3200 3328 3456 (checked_range (fun u => FieldRow data5 data6 member6 u) 3200 128 field_6_25) (checked_range (fun u => FieldRow data5 data6 member6 u) 3328 128 field_6_26)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 3456 3584 3712 (checked_range (fun u => FieldRow data5 data6 member6 u) 3456 128 field_6_27) (checked_range (fun u => FieldRow data5 data6 member6 u) 3584 128 field_6_28))) (join_ranges (fun u => FieldRow data5 data6 member6 u) 3712 3968 4313 (join_ranges (fun u => FieldRow data5 data6 member6 u) 3712 3840 3968 (checked_range (fun u => FieldRow data5 data6 member6 u) 3712 128 field_6_29) (checked_range (fun u => FieldRow data5 data6 member6 u) 3840 128 field_6_30)) (join_ranges (fun u => FieldRow data5 data6 member6 u) 3968 4096 4313 (checked_range (fun u => FieldRow data5 data6 member6 u) 3968 128 field_6_31) (join_ranges (fun u => FieldRow data5 data6 member6 u) 4096 4224 4313 (checked_range (fun u => FieldRow data5 data6 member6 u) 4096 128 field_6_32) (checked_range (fun u => FieldRow data5 data6 member6 u) 4224 89 field_6_33)))))))
theorem lift_6_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_3 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_4 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (512+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_5 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (640+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_6 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (768+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_7 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (896+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_8 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1024+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_9 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1152+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_10 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1280+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_11 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1408+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_12 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1536+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_13 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1664+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_14 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1792+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_15 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (1920+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_16 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2048+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_17 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2176+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_18 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2304+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_19 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2432+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_20 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2560+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_21 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2688+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_22 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2816+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_23 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (2944+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_24 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3072+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_25 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3200+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_26 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3328+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_27 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3456+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_28 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3584+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_29 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3712+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_30 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3840+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_31 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (3968+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_32 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (4096+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_33 : ∀ i : Fin 89, ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 (4224+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_6_all : ∀ u, 0 ≤ u → u < 4313 → ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 0 2176 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 0 1024 2176 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 0 512 1024 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 0 128 lift_6_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 128 128 lift_6_1)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 256 128 lift_6_2) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 384 128 lift_6_3))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 512 768 1024 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 512 128 lift_6_4) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 640 128 lift_6_5)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 768 896 1024 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 768 128 lift_6_6) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 896 128 lift_6_7)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1024 1536 2176 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1024 1280 1536 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1024 1152 1280 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1024 128 lift_6_8) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1152 128 lift_6_9)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1280 1408 1536 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1280 128 lift_6_10) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1408 128 lift_6_11))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1536 1792 2176 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1536 1664 1792 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1536 128 lift_6_12) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1664 128 lift_6_13)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1792 1920 2176 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1792 128 lift_6_14) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1920 2048 2176 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 1920 128 lift_6_15) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2048 128 lift_6_16)))))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2176 3200 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2176 2688 3200 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2176 2432 2688 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2176 2304 2432 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2176 128 lift_6_17) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2304 128 lift_6_18)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2432 2560 2688 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2432 128 lift_6_19) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2560 128 lift_6_20))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2688 2944 3200 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2688 2816 2944 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2688 128 lift_6_21) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2816 128 lift_6_22)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2944 3072 3200 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 2944 128 lift_6_23) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3072 128 lift_6_24)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3200 3712 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3200 3456 3712 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3200 3328 3456 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3200 128 lift_6_25) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3328 128 lift_6_26)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3456 3584 3712 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3456 128 lift_6_27) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3584 128 lift_6_28))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3712 3968 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3712 3840 3968 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3712 128 lift_6_29) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3840 128 lift_6_30)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3968 4096 4313 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 3968 128 lift_6_31) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 4096 4224 4313 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 4096 128 lift_6_32) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data5 data6 component5 459 member6 memberIndex6 u bit.val) 4224 89 lift_6_33)))))))
def lift_certificate6 : LiftCertificate data5 data6 component5 459 where
  members := member6
  memberIndex := memberIndex6
  count := 227
  size_eq := rfl
  coverage u hu := coverage_6_all u (Nat.zero_le u) hu
  fields u hu := field_6_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_6_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete6 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data5)
      (fun v => component5 v=459)))) (graph data6)
      (encode lift_certificate6) := lift_realization lift_certificate6
end ScalarJobData
