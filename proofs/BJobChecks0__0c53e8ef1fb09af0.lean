import BJobData0
import RangeChecks
namespace BroaderJobData
open ScalarFinite
set_option maxHeartbeats 0
set_option maxRecDepth 100000
theorem vertex_0_0 : ∀ i : Fin 15, VertexRow ranking0 (0+i.val) := by
  unfold VertexRow
  decide

theorem vertex_0_all : ∀ u, 0 ≤ u → u < 15 → VertexRow ranking0 u :=
  (checked_range (fun u => VertexRow ranking0 u) 0 15 vertex_0_0)
theorem edge_0_0 : ∀ i : Fin 15, ∀ bit : Fin 2, EdgeRow data0 ranking0 (0+i.val) bit.val := by
  unfold EdgeRow
  decide

theorem edge_0_all : ∀ u, 0 ≤ u → u < 15 → ∀ bit : Fin 2, EdgeRow data0 ranking0 u bit.val :=
  (checked_range (fun u => ∀ bit : Fin 2, EdgeRow data0 ranking0 u bit.val) 0 15 edge_0_0)
theorem checked_rank0 : CheckedRank data0 ranking0 := by
  constructor
  · intro u hu
    exact vertex_0_all u (Nat.zero_le u) hu
  · intro u hu bit hb
    exact edge_0_all u (Nat.zero_le u) hu ⟨bit,by omega⟩
end BroaderJobData
