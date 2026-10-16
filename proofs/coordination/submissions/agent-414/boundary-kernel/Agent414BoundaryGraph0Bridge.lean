import BoundaryDataK
import Agent414BoundaryTranscription

/-! Agent #414. Exact original-namespace adapter. No table definition is replaced.
Dependencies are the unchanged Agent109/original sources pinned in the manifest. -/
namespace Agent414BoundaryGraph0Bridge
open BoundaryCertificate Sofic

/-- The actual original parsed graph equals Agent109's literal graph. -/
theorem graph0_eq_graph0K : graph0 = graph0K :=
  Agent414BoundaryTranscription.graph0_decode_eq decodeEdge

/-- Initial-language membership is identical in the original and literal models. -/
theorem accepts_graph0_iff (n : Nat) (word : Word) :
    Accepts graph0 n word ↔ Accepts graph0K n word := by
  rw [graph0_eq_graph0K]

#print axioms graph0_eq_graph0K
#print axioms accepts_graph0_iff
end Agent414BoundaryGraph0Bridge
