import ProjK5p0
import ProjK5p1
import ProjK5p2
import ProjK5p3
import ProjK5p4
import ProjK5p5
import ProjK5p6
import ProjK5p7
import ProjK5p8
import ProjK5p9
import ProjK5p10
import ProjK5p11
import ProjK5p12
import ProjK5p13
import ProjK5p14
import ProjK5p15
import ProjK5p16
import ProjK5p17
import ProjK5p18
import ProjK5p19
import ProjK5p20
import ProjK5p21
import ProjK5p22
import ProjK5p23
import ProjK5p24
import ProjK5p25
import ProjK5p26
import ProjK5p27
import ProjK5p28
import ProjK5p29
import ProjK5p30
import ProjK5p31
import ProjK5p32
import ProjK5p33
import ProjK5p34
import ProjK5p35
import ProjK5p36
import ProjK5p37
import ProjK5p38
import ProjK5p39
import ProjK5p40
import ProjK5b0
import ProjK5b1
import ProjK5b2
import ProjK5b3
import ProjK5b4
import ProjK5b5
import ProjK5b6
import ProjK5b7
import ProjK5b8
import ProjK5b9
import ProjK5b10

/-! Agent #109: combination of the chunked kernel checks for graph 5 → graph 6. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g5_split_p : graph5K = g5p0 ++ (g5p1 ++ (g5p2 ++ (g5p3 ++ (g5p4 ++ (g5p5 ++ (g5p6 ++ (g5p7 ++ (g5p8 ++ (g5p9 ++ (g5p10 ++ (g5p11 ++ (g5p12 ++ (g5p13 ++ (g5p14 ++ (g5p15 ++ (g5p16 ++ (g5p17 ++ (g5p18 ++ (g5p19 ++ (g5p20 ++ (g5p21 ++ (g5p22 ++ (g5p23 ++ (g5p24 ++ (g5p25 ++ (g5p26 ++ (g5p27 ++ (g5p28 ++ (g5p29 ++ (g5p30 ++ (g5p31 ++ (g5p32 ++ (g5p33 ++ (g5p34 ++ (g5p35 ++ (g5p36 ++ (g5p37 ++ (g5p38 ++ (g5p39 ++ (g5p40)))))))))))))))))))))))))))))))))))))))) := by rfl

theorem g5_split_b : graph5K = g5b0 ++ (g5b1 ++ (g5b2 ++ (g5b3 ++ (g5b4 ++ (g5b5 ++ (g5b6 ++ (g5b7 ++ (g5b8 ++ (g5b9 ++ (g5b10)))))))))) := by rfl

theorem pairs5_all : pairsOK output graph6K T5 B5 H5 (rawNodes fiber graph5K) = true := by
  exact (congrArg (fun G => pairsOK output graph6K T5 B5 H5 (rawNodes fiber G) = true) g5_split_p).mpr
    (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_0 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_1 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_2 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_3 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_4 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_5 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_6 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_7 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_8 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_9 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_10 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_11 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_12 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_13 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_14 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_15 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_16 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_17 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_18 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_19 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_20 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_21 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_22 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_23 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_24 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_25 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_26 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_27 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_28 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_29 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_30 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_31 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_32 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_33 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_34 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_35 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_36 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_37 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_38 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs5_39 pairs5_40))))))))))))))))))))))))))))))))))))))))

theorem buckets5_all : bucketsOK B5 (rawNodes fiber graph5K) = true := by
  exact (congrArg (fun G => bucketsOK B5 (rawNodes fiber G) = true) g5_split_b).mpr
    (bucketsOK_graph_append _ _ _ _ buckets5_0 (bucketsOK_graph_append _ _ _ _ buckets5_1 (bucketsOK_graph_append _ _ _ _ buckets5_2 (bucketsOK_graph_append _ _ _ _ buckets5_3 (bucketsOK_graph_append _ _ _ _ buckets5_4 (bucketsOK_graph_append _ _ _ _ buckets5_5 (bucketsOK_graph_append _ _ _ _ buckets5_6 (bucketsOK_graph_append _ _ _ _ buckets5_7 (bucketsOK_graph_append _ _ _ _ buckets5_8 (bucketsOK_graph_append _ _ _ _ buckets5_9 buckets5_10))))))))))

theorem projection5_fast :
    Projection fiber output graph5K graph6K (rankT T5) (projT T5) :=
  fast_sound buckets5_all pairs5_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection5_fast
