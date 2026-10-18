import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2901 : checkRowsBlock ranks (fastLongPred 7) leaf2901 = true := by decide +kernel
theorem row_branch2901 : checkRow ranks (fastLongPred 7) [10,9,3,9,11,1,9] 3 = true := by decide +kernel
theorem checked_leaf2902 : checkRowsBlock ranks (fastLongPred 7) leaf2902 = true := by decide +kernel
theorem row_branch2902 : checkRow ranks (fastLongPred 7) [10,9,3,9,11,17,6] 3 = true := by decide +kernel
theorem checked_leaf2903 : checkRowsBlock ranks (fastLongPred 7) leaf2903 = true := by decide +kernel
theorem row_branch2903 : checkRow ranks (fastLongPred 7) [10,9,3,9,11,9,4] 18 = true := by decide +kernel
theorem checked_leaf2904 : checkRowsBlock ranks (fastLongPred 7) leaf2904 = true := by decide +kernel
theorem row_branch2904 : checkRow ranks (fastLongPred 7) [10,9,3,9,10,12,9] 12 = true := by decide +kernel
end Agent118.Cert217
