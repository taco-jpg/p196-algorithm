import ProjK0p0
import ProjK0b0

/-! Agent #109: combination of the chunked kernel checks for graph 0 → graph 1. -/

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem g0_split_p : graph0K = g0p0 := by rfl

theorem g0_split_b : graph0K = g0b0 := by rfl

theorem pairs0_all : pairsOK output graph1K T0 B0 H0 (rawNodes fiber graph0K) = true := by
  exact (congrArg (fun G => pairsOK output graph1K T0 B0 H0 (rawNodes fiber G) = true) g0_split_p).mpr
    pairs0_0

theorem buckets0_all : bucketsOK B0 (rawNodes fiber graph0K) = true := by
  exact (congrArg (fun G => bucketsOK B0 (rawNodes fiber G) = true) g0_split_b).mpr
    buckets0_0

theorem projection0_fast :
    Projection fiber output graph0K graph1K (rankT T0) (projT T0) :=
  fast_sound buckets0_all pairs0_all

end BoundaryCertificateK

#print axioms BoundaryCertificateK.projection0_fast
