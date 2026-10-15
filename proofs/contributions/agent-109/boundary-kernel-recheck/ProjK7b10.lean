import FastData7

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g7b10 : Graph := ([7634788423, 7634792519] : List Nat).map decodeEdge

theorem buckets7_10 : bucketsOK B7 (rawNodes fiber g7b10) = true := by
  decide +kernel

end BoundaryCertificateK
