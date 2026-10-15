import FastData7

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g7p40 : Graph := ([7634788423, 7634792519] : List Nat).map decodeEdge

theorem pairs7_40 : pairsOK output graph5K T7 B7 H7 (rawNodes fiber g7p40) = true := by
  decide +kernel

end BoundaryCertificateK
