import BJobData5
import RangeChecks
import BJobData4
namespace BroaderJobData
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

theorem vertex_5_7 : ∀ i : Fin 128, VertexRow ranking5 (896+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_8 : ∀ i : Fin 128, VertexRow ranking5 (1024+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_9 : ∀ i : Fin 128, VertexRow ranking5 (1152+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_10 : ∀ i : Fin 128, VertexRow ranking5 (1280+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_11 : ∀ i : Fin 128, VertexRow ranking5 (1408+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_12 : ∀ i : Fin 128, VertexRow ranking5 (1536+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_13 : ∀ i : Fin 128, VertexRow ranking5 (1664+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_14 : ∀ i : Fin 128, VertexRow ranking5 (1792+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_15 : ∀ i : Fin 128, VertexRow ranking5 (1920+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_16 : ∀ i : Fin 128, VertexRow ranking5 (2048+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_17 : ∀ i : Fin 128, VertexRow ranking5 (2176+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_18 : ∀ i : Fin 128, VertexRow ranking5 (2304+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_19 : ∀ i : Fin 128, VertexRow ranking5 (2432+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_20 : ∀ i : Fin 128, VertexRow ranking5 (2560+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_21 : ∀ i : Fin 128, VertexRow ranking5 (2688+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_22 : ∀ i : Fin 128, VertexRow ranking5 (2816+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_23 : ∀ i : Fin 128, VertexRow ranking5 (2944+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_24 : ∀ i : Fin 128, VertexRow ranking5 (3072+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_25 : ∀ i : Fin 128, VertexRow ranking5 (3200+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_26 : ∀ i : Fin 128, VertexRow ranking5 (3328+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_27 : ∀ i : Fin 128, VertexRow ranking5 (3456+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_28 : ∀ i : Fin 128, VertexRow ranking5 (3584+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_29 : ∀ i : Fin 128, VertexRow ranking5 (3712+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_30 : ∀ i : Fin 128, VertexRow ranking5 (3840+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_31 : ∀ i : Fin 128, VertexRow ranking5 (3968+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_32 : ∀ i : Fin 128, VertexRow ranking5 (4096+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_33 : ∀ i : Fin 89, VertexRow ranking5 (4224+i.val) := by
  unfold VertexRow
  decide

theorem vertex_5_all : ∀ u, 0 ≤ u → u < 4313 → VertexRow ranking5 u :=
  (join_ranges (fun u => VertexRow ranking5 u) 0 2176 4313 (join_ranges (fun u => VertexRow ranking5 u) 0 1024 2176 (join_ranges (fun u => VertexRow ranking5 u) 0 512 1024 (join_ranges (fun u => VertexRow ranking5 u) 0 256 512 (join_ranges (fun u => VertexRow ranking5 u) 0 128 256 (checked_range (fun u => VertexRow ranking5 u) 0 128 vertex_5_0) (checked_range (fun u => VertexRow ranking5 u) 128 128 vertex_5_1)) (join_ranges (fun u => VertexRow ranking5 u) 256 384 512 (checked_range (fun u => VertexRow ranking5 u) 256 128 vertex_5_2) (checked_range (fun u => VertexRow ranking5 u) 384 128 vertex_5_3))) (join_ranges (fun u => VertexRow ranking5 u) 512 768 1024 (join_ranges (fun u => VertexRow ranking5 u) 512 640 768 (checked_range (fun u => VertexRow ranking5 u) 512 128 vertex_5_4) (checked_range (fun u => VertexRow ranking5 u) 640 128 vertex_5_5)) (join_ranges (fun u => VertexRow ranking5 u) 768 896 1024 (checked_range (fun u => VertexRow ranking5 u) 768 128 vertex_5_6) (checked_range (fun u => VertexRow ranking5 u) 896 128 vertex_5_7)))) (join_ranges (fun u => VertexRow ranking5 u) 1024 1536 2176 (join_ranges (fun u => VertexRow ranking5 u) 1024 1280 1536 (join_ranges (fun u => VertexRow ranking5 u) 1024 1152 1280 (checked_range (fun u => VertexRow ranking5 u) 1024 128 vertex_5_8) (checked_range (fun u => VertexRow ranking5 u) 1152 128 vertex_5_9)) (join_ranges (fun u => VertexRow ranking5 u) 1280 1408 1536 (checked_range (fun u => VertexRow ranking5 u) 1280 128 vertex_5_10) (checked_range (fun u => VertexRow ranking5 u) 1408 128 vertex_5_11))) (join_ranges (fun u => VertexRow ranking5 u) 1536 1792 2176 (join_ranges (fun u => VertexRow ranking5 u) 1536 1664 1792 (checked_range (fun u => VertexRow ranking5 u) 1536 128 vertex_5_12) (checked_range (fun u => VertexRow ranking5 u) 1664 128 vertex_5_13)) (join_ranges (fun u => VertexRow ranking5 u) 1792 1920 2176 (checked_range (fun u => VertexRow ranking5 u) 1792 128 vertex_5_14) (join_ranges (fun u => VertexRow ranking5 u) 1920 2048 2176 (checked_range (fun u => VertexRow ranking5 u) 1920 128 vertex_5_15) (checked_range (fun u => VertexRow ranking5 u) 2048 128 vertex_5_16)))))) (join_ranges (fun u => VertexRow ranking5 u) 2176 3200 4313 (join_ranges (fun u => VertexRow ranking5 u) 2176 2688 3200 (join_ranges (fun u => VertexRow ranking5 u) 2176 2432 2688 (join_ranges (fun u => VertexRow ranking5 u) 2176 2304 2432 (checked_range (fun u => VertexRow ranking5 u) 2176 128 vertex_5_17) (checked_range (fun u => VertexRow ranking5 u) 2304 128 vertex_5_18)) (join_ranges (fun u => VertexRow ranking5 u) 2432 2560 2688 (checked_range (fun u => VertexRow ranking5 u) 2432 128 vertex_5_19) (checked_range (fun u => VertexRow ranking5 u) 2560 128 vertex_5_20))) (join_ranges (fun u => VertexRow ranking5 u) 2688 2944 3200 (join_ranges (fun u => VertexRow ranking5 u) 2688 2816 2944 (checked_range (fun u => VertexRow ranking5 u) 2688 128 vertex_5_21) (checked_range (fun u => VertexRow ranking5 u) 2816 128 vertex_5_22)) (join_ranges (fun u => VertexRow ranking5 u) 2944 3072 3200 (checked_range (fun u => VertexRow ranking5 u) 2944 128 vertex_5_23) (checked_range (fun u => VertexRow ranking5 u) 3072 128 vertex_5_24)))) (join_ranges (fun u => VertexRow ranking5 u) 3200 3712 4313 (join_ranges (fun u => VertexRow ranking5 u) 3200 3456 3712 (join_ranges (fun u => VertexRow ranking5 u) 3200 3328 3456 (checked_range (fun u => VertexRow ranking5 u) 3200 128 vertex_5_25) (checked_range (fun u => VertexRow ranking5 u) 3328 128 vertex_5_26)) (join_ranges (fun u => VertexRow ranking5 u) 3456 3584 3712 (checked_range (fun u => VertexRow ranking5 u) 3456 128 vertex_5_27) (checked_range (fun u => VertexRow ranking5 u) 3584 128 vertex_5_28))) (join_ranges (fun u => VertexRow ranking5 u) 3712 3968 4313 (join_ranges (fun u => VertexRow ranking5 u) 3712 3840 3968 (checked_range (fun u => VertexRow ranking5 u) 3712 128 vertex_5_29) (checked_range (fun u => VertexRow ranking5 u) 3840 128 vertex_5_30)) (join_ranges (fun u => VertexRow ranking5 u) 3968 4096 4313 (checked_range (fun u => VertexRow ranking5 u) 3968 128 vertex_5_31) (join_ranges (fun u => VertexRow ranking5 u) 4096 4224 4313 (checked_range (fun u => VertexRow ranking5 u) 4096 128 vertex_5_32) (checked_range (fun u => VertexRow ranking5 u) 4224 89 vertex_5_33)))))))
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

theorem edge_5_7 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (896+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_8 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1024+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_9 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1152+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_10 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1280+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_11 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1408+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_12 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1536+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_13 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1664+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_14 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1792+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_15 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (1920+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_16 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2048+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_17 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2176+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_18 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2304+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_19 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2432+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_20 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2560+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_21 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2688+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_22 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2816+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_23 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (2944+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_24 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3072+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_25 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3200+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_26 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3328+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_27 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3456+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_28 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3584+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_29 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3712+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_30 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3840+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_31 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (3968+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_32 : ∀ i : Fin 128, ∀ bit : Fin 2, EdgeRow data5 ranking5 (4096+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_33 : ∀ i : Fin 89, ∀ bit : Fin 2, EdgeRow data5 ranking5 (4224+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_5_all : ∀ u, 0 ≤ u → u < 4313 → ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 2176 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 1024 2176 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 512 1024 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 0 128 edge_5_0) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 128 128 edge_5_1)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 256 128 edge_5_2) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 384 128 edge_5_3))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 512 768 1024 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 512 128 edge_5_4) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 640 128 edge_5_5)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 768 896 1024 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 768 128 edge_5_6) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 896 128 edge_5_7)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1024 1536 2176 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1024 1280 1536 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1024 1152 1280 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1024 128 edge_5_8) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1152 128 edge_5_9)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1280 1408 1536 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1280 128 edge_5_10) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1408 128 edge_5_11))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1536 1792 2176 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1536 1664 1792 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1536 128 edge_5_12) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1664 128 edge_5_13)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1792 1920 2176 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1792 128 edge_5_14) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1920 2048 2176 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 1920 128 edge_5_15) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2048 128 edge_5_16)))))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2176 3200 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2176 2688 3200 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2176 2432 2688 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2176 2304 2432 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2176 128 edge_5_17) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2304 128 edge_5_18)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2432 2560 2688 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2432 128 edge_5_19) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2560 128 edge_5_20))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2688 2944 3200 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2688 2816 2944 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2688 128 edge_5_21) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2816 128 edge_5_22)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2944 3072 3200 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 2944 128 edge_5_23) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3072 128 edge_5_24)))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3200 3712 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3200 3456 3712 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3200 3328 3456 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3200 128 edge_5_25) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3328 128 edge_5_26)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3456 3584 3712 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3456 128 edge_5_27) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3584 128 edge_5_28))) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3712 3968 4313 (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3712 3840 3968 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3712 128 edge_5_29) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3840 128 edge_5_30)) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3968 4096 4313 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 3968 128 edge_5_31) (join_ranges (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 4096 4224 4313 (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 4096 128 edge_5_32) (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data5 ranking5 u bit.val) 4224 89 edge_5_33)))))))
theorem checked_rank5 : CheckedRank data5 ranking5 := by
  constructor
  · intro u hu
    exact vertex_5_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_5_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
theorem coverage_5_0 : ∀ i : Fin 128, CoverageRow data4 component4 459 227 member5 memberIndex5 (0+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_1 : ∀ i : Fin 128, CoverageRow data4 component4 459 227 member5 memberIndex5 (128+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_2 : ∀ i : Fin 128, CoverageRow data4 component4 459 227 member5 memberIndex5 (256+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_3 : ∀ i : Fin 128, CoverageRow data4 component4 459 227 member5 memberIndex5 (384+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_4 : ∀ i : Fin 128, CoverageRow data4 component4 459 227 member5 memberIndex5 (512+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_5 : ∀ i : Fin 128, CoverageRow data4 component4 459 227 member5 memberIndex5 (640+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_6 : ∀ i : Fin 128, CoverageRow data4 component4 459 227 member5 memberIndex5 (768+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_7 : ∀ i : Fin 54, CoverageRow data4 component4 459 227 member5 memberIndex5 (896+i.val) := by
  unfold CoverageRow
  decide

theorem coverage_5_all : ∀ u, 0 ≤ u → u < 950 → CoverageRow data4 component4 459 227 member5 memberIndex5 u :=
  (join_ranges (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 0 512 950 (join_ranges (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 0 256 512 (join_ranges (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 0 128 256 (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 0 128 coverage_5_0) (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 128 128 coverage_5_1)) (join_ranges (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 256 384 512 (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 256 128 coverage_5_2) (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 384 128 coverage_5_3))) (join_ranges (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 512 768 950 (join_ranges (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 512 640 768 (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 512 128 coverage_5_4) (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 640 128 coverage_5_5)) (join_ranges (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 768 896 950 (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 768 128 coverage_5_6) (checked_range (fun u => CoverageRow data4 component4 459 227 member5 memberIndex5 u) 896 54 coverage_5_7))))
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

theorem field_5_7 : ∀ i : Fin 128, FieldRow data4 data5 member5 (896+i.val) := by
  unfold FieldRow
  decide

theorem field_5_8 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1024+i.val) := by
  unfold FieldRow
  decide

theorem field_5_9 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1152+i.val) := by
  unfold FieldRow
  decide

theorem field_5_10 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1280+i.val) := by
  unfold FieldRow
  decide

theorem field_5_11 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1408+i.val) := by
  unfold FieldRow
  decide

theorem field_5_12 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1536+i.val) := by
  unfold FieldRow
  decide

theorem field_5_13 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1664+i.val) := by
  unfold FieldRow
  decide

theorem field_5_14 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1792+i.val) := by
  unfold FieldRow
  decide

theorem field_5_15 : ∀ i : Fin 128, FieldRow data4 data5 member5 (1920+i.val) := by
  unfold FieldRow
  decide

theorem field_5_16 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2048+i.val) := by
  unfold FieldRow
  decide

theorem field_5_17 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2176+i.val) := by
  unfold FieldRow
  decide

theorem field_5_18 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2304+i.val) := by
  unfold FieldRow
  decide

theorem field_5_19 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2432+i.val) := by
  unfold FieldRow
  decide

theorem field_5_20 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2560+i.val) := by
  unfold FieldRow
  decide

theorem field_5_21 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2688+i.val) := by
  unfold FieldRow
  decide

theorem field_5_22 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2816+i.val) := by
  unfold FieldRow
  decide

theorem field_5_23 : ∀ i : Fin 128, FieldRow data4 data5 member5 (2944+i.val) := by
  unfold FieldRow
  decide

theorem field_5_24 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3072+i.val) := by
  unfold FieldRow
  decide

theorem field_5_25 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3200+i.val) := by
  unfold FieldRow
  decide

theorem field_5_26 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3328+i.val) := by
  unfold FieldRow
  decide

theorem field_5_27 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3456+i.val) := by
  unfold FieldRow
  decide

theorem field_5_28 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3584+i.val) := by
  unfold FieldRow
  decide

theorem field_5_29 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3712+i.val) := by
  unfold FieldRow
  decide

theorem field_5_30 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3840+i.val) := by
  unfold FieldRow
  decide

theorem field_5_31 : ∀ i : Fin 128, FieldRow data4 data5 member5 (3968+i.val) := by
  unfold FieldRow
  decide

theorem field_5_32 : ∀ i : Fin 128, FieldRow data4 data5 member5 (4096+i.val) := by
  unfold FieldRow
  decide

theorem field_5_33 : ∀ i : Fin 89, FieldRow data4 data5 member5 (4224+i.val) := by
  unfold FieldRow
  decide

theorem field_5_all : ∀ u, 0 ≤ u → u < 4313 → FieldRow data4 data5 member5 u :=
  (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 2176 4313 (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 1024 2176 (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 512 1024 (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 256 512 (join_ranges (fun u => FieldRow data4 data5 member5 u) 0 128 256 (checked_range (fun u => FieldRow data4 data5 member5 u) 0 128 field_5_0) (checked_range (fun u => FieldRow data4 data5 member5 u) 128 128 field_5_1)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 256 384 512 (checked_range (fun u => FieldRow data4 data5 member5 u) 256 128 field_5_2) (checked_range (fun u => FieldRow data4 data5 member5 u) 384 128 field_5_3))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 512 768 1024 (join_ranges (fun u => FieldRow data4 data5 member5 u) 512 640 768 (checked_range (fun u => FieldRow data4 data5 member5 u) 512 128 field_5_4) (checked_range (fun u => FieldRow data4 data5 member5 u) 640 128 field_5_5)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 768 896 1024 (checked_range (fun u => FieldRow data4 data5 member5 u) 768 128 field_5_6) (checked_range (fun u => FieldRow data4 data5 member5 u) 896 128 field_5_7)))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 1024 1536 2176 (join_ranges (fun u => FieldRow data4 data5 member5 u) 1024 1280 1536 (join_ranges (fun u => FieldRow data4 data5 member5 u) 1024 1152 1280 (checked_range (fun u => FieldRow data4 data5 member5 u) 1024 128 field_5_8) (checked_range (fun u => FieldRow data4 data5 member5 u) 1152 128 field_5_9)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 1280 1408 1536 (checked_range (fun u => FieldRow data4 data5 member5 u) 1280 128 field_5_10) (checked_range (fun u => FieldRow data4 data5 member5 u) 1408 128 field_5_11))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 1536 1792 2176 (join_ranges (fun u => FieldRow data4 data5 member5 u) 1536 1664 1792 (checked_range (fun u => FieldRow data4 data5 member5 u) 1536 128 field_5_12) (checked_range (fun u => FieldRow data4 data5 member5 u) 1664 128 field_5_13)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 1792 1920 2176 (checked_range (fun u => FieldRow data4 data5 member5 u) 1792 128 field_5_14) (join_ranges (fun u => FieldRow data4 data5 member5 u) 1920 2048 2176 (checked_range (fun u => FieldRow data4 data5 member5 u) 1920 128 field_5_15) (checked_range (fun u => FieldRow data4 data5 member5 u) 2048 128 field_5_16)))))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 2176 3200 4313 (join_ranges (fun u => FieldRow data4 data5 member5 u) 2176 2688 3200 (join_ranges (fun u => FieldRow data4 data5 member5 u) 2176 2432 2688 (join_ranges (fun u => FieldRow data4 data5 member5 u) 2176 2304 2432 (checked_range (fun u => FieldRow data4 data5 member5 u) 2176 128 field_5_17) (checked_range (fun u => FieldRow data4 data5 member5 u) 2304 128 field_5_18)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 2432 2560 2688 (checked_range (fun u => FieldRow data4 data5 member5 u) 2432 128 field_5_19) (checked_range (fun u => FieldRow data4 data5 member5 u) 2560 128 field_5_20))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 2688 2944 3200 (join_ranges (fun u => FieldRow data4 data5 member5 u) 2688 2816 2944 (checked_range (fun u => FieldRow data4 data5 member5 u) 2688 128 field_5_21) (checked_range (fun u => FieldRow data4 data5 member5 u) 2816 128 field_5_22)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 2944 3072 3200 (checked_range (fun u => FieldRow data4 data5 member5 u) 2944 128 field_5_23) (checked_range (fun u => FieldRow data4 data5 member5 u) 3072 128 field_5_24)))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 3200 3712 4313 (join_ranges (fun u => FieldRow data4 data5 member5 u) 3200 3456 3712 (join_ranges (fun u => FieldRow data4 data5 member5 u) 3200 3328 3456 (checked_range (fun u => FieldRow data4 data5 member5 u) 3200 128 field_5_25) (checked_range (fun u => FieldRow data4 data5 member5 u) 3328 128 field_5_26)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 3456 3584 3712 (checked_range (fun u => FieldRow data4 data5 member5 u) 3456 128 field_5_27) (checked_range (fun u => FieldRow data4 data5 member5 u) 3584 128 field_5_28))) (join_ranges (fun u => FieldRow data4 data5 member5 u) 3712 3968 4313 (join_ranges (fun u => FieldRow data4 data5 member5 u) 3712 3840 3968 (checked_range (fun u => FieldRow data4 data5 member5 u) 3712 128 field_5_29) (checked_range (fun u => FieldRow data4 data5 member5 u) 3840 128 field_5_30)) (join_ranges (fun u => FieldRow data4 data5 member5 u) 3968 4096 4313 (checked_range (fun u => FieldRow data4 data5 member5 u) 3968 128 field_5_31) (join_ranges (fun u => FieldRow data4 data5 member5 u) 4096 4224 4313 (checked_range (fun u => FieldRow data4 data5 member5 u) 4096 128 field_5_32) (checked_range (fun u => FieldRow data4 data5 member5 u) 4224 89 field_5_33)))))))
theorem lift_5_0 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (0+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_1 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (128+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_2 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (256+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_3 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (384+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_4 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (512+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_5 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (640+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_6 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (768+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_7 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (896+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_8 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1024+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_9 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1152+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_10 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1280+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_11 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1408+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_12 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1536+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_13 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1664+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_14 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1792+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_15 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (1920+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_16 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2048+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_17 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2176+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_18 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2304+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_19 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2432+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_20 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2560+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_21 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2688+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_22 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2816+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_23 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (2944+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_24 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3072+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_25 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3200+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_26 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3328+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_27 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3456+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_28 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3584+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_29 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3712+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_30 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3840+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_31 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (3968+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_32 : ∀ i : Fin 128, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (4096+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_33 : ∀ i : Fin 89, ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 (4224+i.val) bit.val := by
  unfold LiftRow
  decide

theorem lift_5_all : ∀ u, 0 ≤ u → u < 4313 → ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val :=
  (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 0 2176 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 0 1024 2176 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 0 512 1024 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 0 256 512 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 0 128 256 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 0 128 lift_5_0) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 128 128 lift_5_1)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 256 384 512 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 256 128 lift_5_2) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 384 128 lift_5_3))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 512 768 1024 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 512 640 768 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 512 128 lift_5_4) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 640 128 lift_5_5)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 768 896 1024 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 768 128 lift_5_6) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 896 128 lift_5_7)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1024 1536 2176 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1024 1280 1536 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1024 1152 1280 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1024 128 lift_5_8) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1152 128 lift_5_9)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1280 1408 1536 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1280 128 lift_5_10) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1408 128 lift_5_11))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1536 1792 2176 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1536 1664 1792 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1536 128 lift_5_12) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1664 128 lift_5_13)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1792 1920 2176 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1792 128 lift_5_14) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1920 2048 2176 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 1920 128 lift_5_15) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2048 128 lift_5_16)))))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2176 3200 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2176 2688 3200 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2176 2432 2688 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2176 2304 2432 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2176 128 lift_5_17) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2304 128 lift_5_18)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2432 2560 2688 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2432 128 lift_5_19) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2560 128 lift_5_20))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2688 2944 3200 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2688 2816 2944 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2688 128 lift_5_21) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2816 128 lift_5_22)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2944 3072 3200 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 2944 128 lift_5_23) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3072 128 lift_5_24)))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3200 3712 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3200 3456 3712 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3200 3328 3456 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3200 128 lift_5_25) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3328 128 lift_5_26)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3456 3584 3712 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3456 128 lift_5_27) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3584 128 lift_5_28))) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3712 3968 4313 (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3712 3840 3968 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3712 128 lift_5_29) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3840 128 lift_5_30)) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3968 4096 4313 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 3968 128 lift_5_31) (join_ranges (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 4096 4224 4313 (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 4096 128 lift_5_32) (checked_range (fun u => ∀ bit : Fin 2, LiftRow data4 data5 component4 459 member5 memberIndex5 u bit.val) 4224 89 lift_5_33)))))))
def lift_certificate5 : LiftCertificate data4 data5 component4 459 where
  members := member5
  memberIndex := memberIndex5
  count := 227
  size_eq := rfl
  coverage u hu := coverage_5_all u (Nat.zero_le u) hu
  fields u hu := field_5_all u (Nat.zero_le u) hu
  transitions u hu bit hb := lift_5_all u (Nat.zero_le u) hu ⟨bit,by omega⟩

theorem lift_complete5 : ActualPrefixLift.Realization
    (bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph data4)
      (fun v => component4 v=459)))) (graph data5)
      (encode lift_certificate5) := lift_realization lift_certificate5
end BroaderJobData
