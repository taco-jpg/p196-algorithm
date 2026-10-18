import P196.Drafts.Agent109BoundaryKernelRecheck.FastData0

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g0b0 : Graph := ([4176, 16785439, 33566782, 50348057, 67129400, 83886087, 100692024, 117473305, 134254654, 151035935, 167817296, 184573959] : List Nat).map decodeEdge

theorem buckets0_0 : bucketsOK B0 (rawNodes fiber g0b0) = true := by
  decide +kernel

end BoundaryCertificateK
