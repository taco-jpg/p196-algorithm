import ProjK2p0
import ProjK2p1
import ProjK2p2
import ProjK2p3
import ProjK2b0

/-! Agent #109: combination of the chunked kernel checks for graph 2 → graph 3. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g2_split_p : graph2K = g2p0 ++ (g2p1 ++ (g2p2 ++ (g2p3))) := by rfl

theorem g2_split_b : graph2K = g2b0 := by rfl

theorem pairs2_all : pairsOK output graph3K T2 B2 H2 (rawNodes fiber graph2K) = true := by
  exact (congrArg (fun G => pairsOK output graph3K T2 B2 H2 (rawNodes fiber G) = true) g2_split_p).mpr
    (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs2_0 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs2_1 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs2_2 pairs2_3)))

theorem buckets2_all : bucketsOK B2 (rawNodes fiber graph2K) = true := by
  exact (congrArg (fun G => bucketsOK B2 (rawNodes fiber G) = true) g2_split_b).mpr
    buckets2_0

theorem projection2_fast :
    Projection fiber output graph2K graph3K (rankT T2) (projT T2) :=
  fast_sound buckets2_all pairs2_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection2_fast
