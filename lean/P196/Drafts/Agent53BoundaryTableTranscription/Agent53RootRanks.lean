import P196.Drafts.Agent109BoundaryKernelRecheck.BoundaryDataK

/-!
Exact identity of the original root-rank tables and Agent109's literal tables.
Source snapshot: 54ac7c885e54ce74190b85ec82cceca2b23c2e38.
The parser-equation proof method follows Agent414's attributed graph0 bridge;
the original definitions and the target array values remain unchanged.
-/
namespace Agent53BoundaryTables
open BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 5000000

theorem rootRanks0_eq_rootRanks0K : rootRanks0 = rootRanks0K := by
  unfold rootRanks0 rootRanks0K parseNats
  apply congrArg List.toArray
  simp +decide [String.splitOn, String.splitOnAux,
    String.toNat?, String.isNat, String.all, String.any, String.anyAux,
    String.foldl, String.foldlAux]

#print axioms rootRanks0_eq_rootRanks0K
end Agent53BoundaryTables
