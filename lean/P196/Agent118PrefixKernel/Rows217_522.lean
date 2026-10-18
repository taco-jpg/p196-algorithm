import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2915 : checkRowsBlock ranks (fastLongPred 7) leaf2915 = true := by decide +kernel
theorem row_branch2915 : checkRow ranks (fastLongPred 7) [10,9,3,11,11,14,14] 3 = true := by decide +kernel
theorem checked_leaf2916 : checkRowsBlock ranks (fastLongPred 7) leaf2916 = true := by decide +kernel
theorem row_branch2916 : checkRow ranks (fastLongPred 7) [10,9,3,11,10,17,18] 1 = true := by decide +kernel
theorem checked_leaf2917 : checkRowsBlock ranks (fastLongPred 7) leaf2917 = true := by decide +kernel
theorem row_branch2917 : checkRow ranks (fastLongPred 7) [10,9,3,15,3,15,15] 3 = true := by decide +kernel
end Agent118.Cert217
