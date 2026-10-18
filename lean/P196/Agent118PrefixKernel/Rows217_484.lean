import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2807 : checkRowsBlock ranks (fastLongPred 7) leaf2807 = true := by decide +kernel
theorem row_branch2807 : checkRow ranks (fastLongPred 7) [10,9,3,6,4,7,6] 4 = true := by decide +kernel
theorem checked_leaf2808 : checkRowsBlock ranks (fastLongPred 7) leaf2808 = true := by decide +kernel
theorem row_branch2808 : checkRow ranks (fastLongPred 7) [10,9,3,2,11,7,11] 3 = true := by decide +kernel
end Agent118.Cert217
