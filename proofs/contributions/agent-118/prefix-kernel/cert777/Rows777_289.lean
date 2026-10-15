import Rank777
import PrefixChecksBase
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem row_leaf1940_33 : checkRow ranks (fastLongPred 7) [7,7,7,9,4,4,4] 11 = true := by decide +kernel
theorem row_leaf1940_34 : checkRow ranks (fastLongPred 7) [7,7,7,9,4,4,5] 11 = true := by decide +kernel
theorem row_leaf1940_35 : checkRow ranks (fastLongPred 7) [7,7,7,9,4,4,6] 11 = true := by decide +kernel
end Agent118.Cert777
