import P196.Drafts.Agent109BoundaryKernelRecheck.FastData5

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g5p40 : Graph := ([7634694229, 7634698325] : List Nat).map decodeEdge

theorem pairs5_40 : pairsOK output graph6K T5 B5 H5 (rawNodes fiber g5p40) = true := by
  decide +kernel

end BoundaryCertificateK
