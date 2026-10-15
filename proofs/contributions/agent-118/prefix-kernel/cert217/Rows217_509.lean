import Rank217
import PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2881 : checkRowsBlock ranks (fastLongPred 7) leaf2881 = true := by decide +kernel
theorem row_branch2881 : checkRow ranks (fastLongPred 7) [10,9,3,8,12,18,0] 7 = true := by decide +kernel
end Agent118.Cert217
