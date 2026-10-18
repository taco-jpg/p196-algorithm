import P196.Drafts.Agent109BoundaryKernelRecheck.FastData5

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g5b10 : Graph := ([7634694229, 7634698325] : List Nat).map decodeEdge

theorem buckets5_10 : bucketsOK B5 (rawNodes fiber g5b10) = true := by
  decide +kernel

end BoundaryCertificateK
