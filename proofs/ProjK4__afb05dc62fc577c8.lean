import ProjK4p0
import ProjK4p1
import ProjK4p2
import ProjK4p3
import ProjK4p4
import ProjK4p5
import ProjK4p6
import ProjK4p7
import ProjK4p8
import ProjK4p9
import ProjK4p10
import ProjK4p11
import ProjK4p12
import ProjK4p13
import ProjK4p14
import ProjK4p15
import ProjK4p16
import ProjK4p17
import ProjK4p18
import ProjK4p19
import ProjK4p20
import ProjK4p21
import ProjK4p22
import ProjK4p23
import ProjK4p24
import ProjK4p25
import ProjK4p26
import ProjK4p27
import ProjK4p28
import ProjK4p29
import ProjK4b0
import ProjK4b1
import ProjK4b2
import ProjK4b3
import ProjK4b4
import ProjK4b5
import ProjK4b6
import ProjK4b7

/-! Agent #109: combination of the chunked kernel checks for graph 4 → graph 5. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g4_split_p : graph4K = g4p0 ++ (g4p1 ++ (g4p2 ++ (g4p3 ++ (g4p4 ++ (g4p5 ++ (g4p6 ++ (g4p7 ++ (g4p8 ++ (g4p9 ++ (g4p10 ++ (g4p11 ++ (g4p12 ++ (g4p13 ++ (g4p14 ++ (g4p15 ++ (g4p16 ++ (g4p17 ++ (g4p18 ++ (g4p19 ++ (g4p20 ++ (g4p21 ++ (g4p22 ++ (g4p23 ++ (g4p24 ++ (g4p25 ++ (g4p26 ++ (g4p27 ++ (g4p28 ++ (g4p29))))))))))))))))))))))))))))) := by rfl

theorem g4_split_b : graph4K = g4b0 ++ (g4b1 ++ (g4b2 ++ (g4b3 ++ (g4b4 ++ (g4b5 ++ (g4b6 ++ (g4b7))))))) := by rfl

theorem pairs4_all : pairsOK output graph5K T4 B4 H4 (rawNodes fiber graph4K) = true := by
  exact (congrArg (fun G => pairsOK output graph5K T4 B4 H4 (rawNodes fiber G) = true) g4_split_p).mpr
    (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_0 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_1 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_2 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_3 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_4 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_5 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_6 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_7 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_8 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_9 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_10 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_11 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_12 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_13 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_14 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_15 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_16 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_17 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_18 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_19 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_20 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_21 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_22 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_23 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_24 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_25 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_26 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_27 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs4_28 pairs4_29)))))))))))))))))))))))))))))

theorem buckets4_all : bucketsOK B4 (rawNodes fiber graph4K) = true := by
  exact (congrArg (fun G => bucketsOK B4 (rawNodes fiber G) = true) g4_split_b).mpr
    (bucketsOK_graph_append _ _ _ _ buckets4_0 (bucketsOK_graph_append _ _ _ _ buckets4_1 (bucketsOK_graph_append _ _ _ _ buckets4_2 (bucketsOK_graph_append _ _ _ _ buckets4_3 (bucketsOK_graph_append _ _ _ _ buckets4_4 (bucketsOK_graph_append _ _ _ _ buckets4_5 (bucketsOK_graph_append _ _ _ _ buckets4_6 buckets4_7)))))))

theorem projection4_fast :
    Projection fiber output graph4K graph5K (rankT T4) (projT T4) :=
  fast_sound buckets4_all pairs4_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection4_fast
