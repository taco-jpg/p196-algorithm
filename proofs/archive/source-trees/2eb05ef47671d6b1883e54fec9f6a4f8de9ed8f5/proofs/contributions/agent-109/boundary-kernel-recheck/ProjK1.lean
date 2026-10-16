import ProjK1p0
import ProjK1b0

/-! Agent #109: combination of the chunked kernel checks for graph 1 → graph 2. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g1_split_p : graph1K = g1p0 := by rfl

theorem g1_split_b : graph1K = g1b0 := by rfl

theorem pairs1_all : pairsOK output graph2K T1 B1 H1 (rawNodes fiber graph1K) = true := by
  exact (congrArg (fun G => pairsOK output graph2K T1 B1 H1 (rawNodes fiber G) = true) g1_split_p).mpr
    pairs1_0

theorem buckets1_all : bucketsOK B1 (rawNodes fiber graph1K) = true := by
  exact (congrArg (fun G => bucketsOK B1 (rawNodes fiber G) = true) g1_split_b).mpr
    buckets1_0

theorem projection1_fast :
    Projection fiber output graph1K graph2K (rankT T1) (projT T1) :=
  fast_sound buckets1_all pairs1_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection1_fast
