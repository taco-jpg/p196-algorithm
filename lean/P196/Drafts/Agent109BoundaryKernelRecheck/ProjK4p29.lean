import P196.Drafts.Agent109BoundaryKernelRecheck.FastData4

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g4p29 : Graph := ([5671522357, 5671526453, 5671530549, 5688287306, 5688291402, 5688295498, 5688299594, 5688303690, 5688307786, 5705089074, 5705093170, 5705097266, 5705101362, 5721866311, 5721870407, 5721874503, 5721878599] : List Nat).map decodeEdge

theorem pairs4_29 : pairsOK output graph5K T4 B4 H4 (rawNodes fiber g4p29) = true := by
  decide +kernel

end BoundaryCertificateK
