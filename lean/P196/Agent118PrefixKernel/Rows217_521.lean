import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2912 : checkRowsBlock ranks (fastLongPred 7) leaf2912 = true := by decide +kernel
theorem row_branch2912 : checkRow ranks (fastLongPred 7) [10,9,3,10,18,9,7] 3 = true := by decide +kernel
theorem checked_leaf2913 : checkRowsBlock ranks (fastLongPred 7) leaf2913 = true := by decide +kernel
theorem row_branch2913 : checkRow ranks (fastLongPred 7) [10,9,3,9,13,15,3] 3 = true := by decide +kernel
theorem checked_leaf2914 : checkRowsBlock ranks (fastLongPred 7) leaf2914 = true := by decide +kernel
theorem row_branch2914 : checkRow ranks (fastLongPred 7) [10,9,3,11,9,2,13] 3 = true := by decide +kernel
end Agent118.Cert217
