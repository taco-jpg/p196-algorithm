import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p0
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p1
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p2
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p3
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p4
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p5
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p6
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p7
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p8
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p9
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p10
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p11
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p12
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p13
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p14
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p15
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p16
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p17
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p18
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p19
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p20
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p21
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p22
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p23
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p24
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p25
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p26
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p27
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p28
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p29
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p30
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p31
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p32
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p33
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p34
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p35
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p36
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p37
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p38
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p39
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6p40
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b0
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b1
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b2
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b3
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b4
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b5
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b6
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b7
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b8
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b9
import P196.Drafts.Agent109BoundaryKernelRecheck.ProjK6b10

/-! Agent #109: combination of the chunked kernel checks for graph 6 → graph 7. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g6_split_p : graph6K = g6p0 ++ (g6p1 ++ (g6p2 ++ (g6p3 ++ (g6p4 ++ (g6p5 ++ (g6p6 ++ (g6p7 ++ (g6p8 ++ (g6p9 ++ (g6p10 ++ (g6p11 ++ (g6p12 ++ (g6p13 ++ (g6p14 ++ (g6p15 ++ (g6p16 ++ (g6p17 ++ (g6p18 ++ (g6p19 ++ (g6p20 ++ (g6p21 ++ (g6p22 ++ (g6p23 ++ (g6p24 ++ (g6p25 ++ (g6p26 ++ (g6p27 ++ (g6p28 ++ (g6p29 ++ (g6p30 ++ (g6p31 ++ (g6p32 ++ (g6p33 ++ (g6p34 ++ (g6p35 ++ (g6p36 ++ (g6p37 ++ (g6p38 ++ (g6p39 ++ (g6p40)))))))))))))))))))))))))))))))))))))))) := by rfl

theorem g6_split_b : graph6K = g6b0 ++ (g6b1 ++ (g6b2 ++ (g6b3 ++ (g6b4 ++ (g6b5 ++ (g6b6 ++ (g6b7 ++ (g6b8 ++ (g6b9 ++ (g6b10)))))))))) := by rfl

theorem pairs6_all : pairsOK output graph7K T6 B6 H6 (rawNodes fiber graph6K) = true := by
  exact (congrArg (fun G => pairsOK output graph7K T6 B6 H6 (rawNodes fiber G) = true) g6_split_p).mpr
    (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_0 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_1 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_2 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_3 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_4 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_5 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_6 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_7 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_8 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_9 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_10 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_11 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_12 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_13 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_14 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_15 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_16 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_17 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_18 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_19 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_20 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_21 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_22 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_23 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_24 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_25 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_26 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_27 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_28 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_29 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_30 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_31 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_32 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_33 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_34 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_35 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_36 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_37 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_38 (pairsOK_graph_append _ _ _ _ _ _ _ _ pairs6_39 pairs6_40))))))))))))))))))))))))))))))))))))))))

theorem buckets6_all : bucketsOK B6 (rawNodes fiber graph6K) = true := by
  exact (congrArg (fun G => bucketsOK B6 (rawNodes fiber G) = true) g6_split_b).mpr
    (bucketsOK_graph_append _ _ _ _ buckets6_0 (bucketsOK_graph_append _ _ _ _ buckets6_1 (bucketsOK_graph_append _ _ _ _ buckets6_2 (bucketsOK_graph_append _ _ _ _ buckets6_3 (bucketsOK_graph_append _ _ _ _ buckets6_4 (bucketsOK_graph_append _ _ _ _ buckets6_5 (bucketsOK_graph_append _ _ _ _ buckets6_6 (bucketsOK_graph_append _ _ _ _ buckets6_7 (bucketsOK_graph_append _ _ _ _ buckets6_8 (bucketsOK_graph_append _ _ _ _ buckets6_9 buckets6_10))))))))))

theorem projection6_fast :
    Projection fiber output graph6K graph7K (rankT T6) (projT T6) :=
  fast_sound buckets6_all pairs6_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection6_fast
