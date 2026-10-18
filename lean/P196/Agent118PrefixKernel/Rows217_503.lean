import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2853 : checkRowsBlock ranks (fastLongPred 7) leaf2853 = true := by decide +kernel
theorem row_branch2853 : checkRow ranks (fastLongPred 7) [10,9,3,7,13,8,4] 3 = true := by decide +kernel
theorem checked_leaf2854 : checkRowsBlock ranks (fastLongPred 7) leaf2854 = true := by decide +kernel
theorem row_branch2854 : checkRow ranks (fastLongPred 7) [10,9,3,7,14,8,15] 3 = true := by decide +kernel
theorem checked_leaf2855 : checkRowsBlock ranks (fastLongPred 7) leaf2855 = true := by decide +kernel
theorem row_branch2855 : checkRow ranks (fastLongPred 7) [10,9,3,7,15,5,14] 3 = true := by decide +kernel
end Agent118.Cert217
