import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p0
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p1
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p2
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p3
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p4
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p5
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p6
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p7
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p8
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p9
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p10
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p11
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p12
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p13
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p14
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p15
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p16
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p17
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p18
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p19
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p20
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p21
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p22
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p23
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p24
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p25
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p26
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p27
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p28
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p29
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p30
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p31
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p32
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p33
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p34
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p35
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p36
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p37
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p38
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p39
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7p40
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b0
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b1
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b2
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b3
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b4
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b5
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b6
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b7
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b8
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b9
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK7b10

/-! Agent #109: combination of the chunked kernel checks for graph 7 → graph 5. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g7_split_p : graph7K = g7p0 ++ (g7p1 ++ (g7p2 ++ (g7p3 ++ (g7p4 ++ (g7p5 ++ (g7p6 ++ (g7p7 ++ (g7p8 ++ (g7p9 ++ (g7p10 ++ (g7p11 ++ (g7p12 ++ (g7p13 ++ (g7p14 ++ (g7p15 ++ (g7p16 ++ (g7p17 ++ (g7p18 ++ (g7p19 ++ (g7p20 ++ (g7p21 ++ (g7p22 ++ (g7p23 ++ (g7p24 ++ (g7p25 ++ (g7p26 ++ (g7p27 ++ (g7p28 ++ (g7p29 ++ (g7p30 ++ (g7p31 ++ (g7p32 ++ (g7p33 ++ (g7p34 ++ (g7p35 ++ (g7p36 ++ (g7p37 ++ (g7p38 ++ (g7p39 ++ (g7p40)))))))))))))))))))))))))))))))))))))))) := by rfl

theorem g7_split_b : graph7K = g7b0 ++ (g7b1 ++ (g7b2 ++ (g7b3 ++ (g7b4 ++ (g7b5 ++ (g7b6 ++ (g7b7 ++ (g7b8 ++ (g7b9 ++ (g7b10)))))))))) := by rfl

theorem pairs7_all : pairsOK output graph5K T7 B7 H7 (rawNodes fiber graph7K) = true := by
  exact (congrArg (fun G => pairsOK output graph5K T7 B7 H7 (rawNodes fiber G) = true) g7_split_p).mpr
    (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_0 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_1 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_2 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_3 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_4 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_5 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_6 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_7 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_8 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_9 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_10 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_11 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_12 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_13 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_14 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_15 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_16 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_17 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_18 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_19 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_20 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_21 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_22 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_23 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_24 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_25 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_26 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_27 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_28 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_29 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_30 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_31 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_32 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_33 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_34 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_35 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_36 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_37 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_38 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs7_39 pairs7_40))))))))))))))))))))))))))))))))))))))))

theorem buckets7_all : bucketsOK B7 (rawNodes fiber graph7K) = true := by
  exact (congrArg (fun G => bucketsOK B7 (rawNodes fiber G) = true) g7_split_b).mpr
    (bucketsOK_graph_append _ _ _ _ buckets7_0 (bucketsOK_graph_append _ _ _ _ buckets7_1 (bucketsOK_graph_append _ _ _ _ buckets7_2 (bucketsOK_graph_append _ _ _ _ buckets7_3 (bucketsOK_graph_append _ _ _ _ buckets7_4 (bucketsOK_graph_append _ _ _ _ buckets7_5 (bucketsOK_graph_append _ _ _ _ buckets7_6 (bucketsOK_graph_append _ _ _ _ buckets7_7 (bucketsOK_graph_append _ _ _ _ buckets7_8 (bucketsOK_graph_append _ _ _ _ buckets7_9 buckets7_10))))))))))

theorem projection7_fast :
    Projection fiber output graph7K graph5K (rankT T7) (projT T7) :=
  fast_sound buckets7_all pairs7_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection7_fast
