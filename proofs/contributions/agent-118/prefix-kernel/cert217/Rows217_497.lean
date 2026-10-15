import Rank217
import PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2841 : checkRowsBlock ranks (fastLongPred 7) leaf2841 = true := by decide +kernel
theorem row_branch2841 : checkRow ranks (fastLongPred 7) [10,9,3,7,4,16,6] 2 = true := by decide +kernel
end Agent118.Cert217
