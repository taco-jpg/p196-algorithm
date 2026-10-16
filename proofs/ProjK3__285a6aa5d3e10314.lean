import ProjK3p0
import ProjK3p1
import ProjK3p2
import ProjK3p3
import ProjK3p4
import ProjK3p5
import ProjK3p6
import ProjK3p7
import ProjK3p8
import ProjK3p9
import ProjK3p10
import ProjK3b0
import ProjK3b1
import ProjK3b2

/-! Agent #109: combination of the chunked kernel checks for graph 3 → graph 4. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g3_split_p : graph3K = g3p0 ++ (g3p1 ++ (g3p2 ++ (g3p3 ++ (g3p4 ++ (g3p5 ++ (g3p6 ++ (g3p7 ++ (g3p8 ++ (g3p9 ++ (g3p10)))))))))) := by rfl

theorem g3_split_b : graph3K = g3b0 ++ (g3b1 ++ (g3b2)) := by rfl

theorem pairs3_all : pairsOK output graph4K T3 B3 H3 (rawNodes fiber graph3K) = true := by
  exact (congrArg (fun G => pairsOK output graph4K T3 B3 H3 (rawNodes fiber G) = true) g3_split_p).mpr
    (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_0 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_1 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_2 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_3 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_4 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_5 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_6 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_7 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_8 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs3_9 pairs3_10))))))))))

theorem buckets3_all : bucketsOK B3 (rawNodes fiber graph3K) = true := by
  exact (congrArg (fun G => bucketsOK B3 (rawNodes fiber G) = true) g3_split_b).mpr
    (bucketsOK_graph_append _ _ _ _ buckets3_0 (bucketsOK_graph_append _ _ _ _ buckets3_1 buckets3_2))

theorem projection3_fast :
    Projection fiber output graph3K graph4K (rankT T3) (projT T3) :=
  fast_sound buckets3_all pairs3_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection3_fast
