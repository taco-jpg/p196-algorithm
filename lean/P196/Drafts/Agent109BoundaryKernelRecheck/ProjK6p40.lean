import P196.Drafts.Agent109BoundaryKernelRecheck.FastData6

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g6p40 : Graph := ([7634636818, 7634640914] : List Nat).map decodeEdge

theorem pairs6_40 : pairsOK output graph7K T6 B6 H6 (rawNodes fiber g6p40) = true := by
  decide +kernel

end BoundaryCertificateK
