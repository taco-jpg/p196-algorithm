import Rank777
import PrefixChecksBase
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem row_leaf1934_30 : checkRow ranks (fastLongPred 7) [7,7,7,9,2,1,8] 11 = true := by decide +kernel
theorem row_leaf1934_31 : checkRow ranks (fastLongPred 7) [7,7,7,9,2,1,9] 11 = true := by decide +kernel
theorem row_leaf1934_32 : checkRow ranks (fastLongPred 7) [7,7,7,9,2,2,0] 1 = true := by decide +kernel
theorem row_leaf1934_33 : checkRow ranks (fastLongPred 7) [7,7,7,9,2,2,1] 11 = true := by decide +kernel
theorem row_leaf1934_34 : checkRow ranks (fastLongPred 7) [7,7,7,9,2,2,2] 11 = true := by decide +kernel
theorem row_leaf1934_35 : checkRow ranks (fastLongPred 7) [7,7,7,9,2,2,3] 11 = true := by decide +kernel
end Agent118.Cert777
