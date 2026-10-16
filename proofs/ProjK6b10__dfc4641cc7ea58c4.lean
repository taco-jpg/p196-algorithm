import FastData6

namespace BoundaryCertificateK
open Sofic Sofic.Fast BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def g6b10 : Graph := ([7634636818, 7634640914] : List Nat).map decodeEdge

theorem buckets6_10 : bucketsOK B6 (rawNodes fiber g6b10) = true := by
  decide +kernel

end BoundaryCertificateK
